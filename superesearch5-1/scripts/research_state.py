#!/usr/bin/env python3
"""Coordinator-owned, stdlib-only v5 research evidence and approval ledger.
See ../references/state-cli.md. This records attestations, not identity or truth.
"""
import argparse
import copy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys

WORKERS = ('worker1', 'worker2', 'worker3')
JUDGES = ('adherence', 'correctness', 'plausibility')
LANES = ('literature', 'free_data', 'gated_data', 'alternative', 'tools')
APPROVALS = {'question': 'question', 'objective': 'brief', 'sourcing_plan': 'sourcing_plan',
             'sources': 'sources', 'plan': 'plan'}

class Invalid(ValueError):
    pass

def need(ok, message):
    if not ok:
        raise Invalid(message)

def text(value):
    return isinstance(value, str) and bool(value.strip())

def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

def attestation(p):
    need(text(p.get('message')) and text(p.get('reference')), 'Explicit human message and reference required')
    return {'message': p['message'], 'reference': p['reference']}

class ResearchState:
    def __init__(self, root):
        self._fresh_cache = set()
        self.root = Path(root).resolve()
        self.path = self.root / 'research-state.json'
        need(not self.path.is_symlink(), 'Ledger cannot be a symlink')
        self.s = json.loads(self.path.read_text()) if self.path.exists() else None
        if self.s is not None:
            need(self.s.get('version') == 5, 'Expected v5 ledger')

    def snapshot(self, name):
        need(text(name), 'Artifact path required')
        p = (self.root / name).resolve()
        need(p.is_relative_to(self.root) and p.is_file(), 'Artifact must be a regular file inside run')
        need(p != self.path and not p.is_relative_to(self.root / '.state-artifacts'), 'Reserved ledger/archive path')
        data = p.read_bytes()
        return {'path': str(p.relative_to(self.root)), 'sha256': hashlib.sha256(data).hexdigest()}

    def fresh(self, kind):
        need(kind in self.s['nodes'], 'Missing artifact: ' + kind)
        node = self.s['nodes'][kind]
        if kind in self._fresh_cache:
            return node
        need(self.snapshot(node['artifact']['path']) == node['artifact'], 'Artifact changed: ' + kind)
        for snap in node.get('files', []):
            need(self.snapshot(snap['path']) == snap, 'Dependency file changed: ' + snap['path'])
        for review in node.get('reviews', {}).values():
            for snap in review.get('table_files', []):
                need(self.snapshot(snap['path']) == snap, 'Review evidence changed: ' + snap['path'])
        for dep, expected in node['dependencies'].items():
            self.fresh(dep)
            need(digest(self.s['nodes'][dep]) == expected, 'Stale dependency: ' + dep)
        self._fresh_cache.add(kind)
        return node

    def invalidate(self, kind):
        self._fresh_cache = set()
        removed = {kind}
        while True:
            extra = {k for k, n in self.s['nodes'].items() if set(n['dependencies']) & removed}
            if extra <= removed:
                break
            removed |= extra
        for k in removed:
            self.s['nodes'].pop(k, None)
        self.s.pop('delivery', None)
        self.s.pop('finisher', None)
        self.s.pop('blocker', None)

    def descendants(self, kind):
        node = self.s['nodes'][kind]
        self.invalidate(kind)
        self.s['nodes'][kind] = node

    def autonomous(self):
        return self.s['nodes'].get('brief', {}).get('metadata', {}).get('mode') == 'autonomous'

    def approved(self, kind):
        node = self.fresh(kind)
        if kind in ('sourcing_plan', 'sources', 'plan'):
            self.approved('brief')
            if kind in ('sourcing_plan', 'sources', 'plan'):
                need(self.qualified(kind), 'Independent review must pass: ' + kind)
            if self.autonomous():
                return
        need('approval' in node, 'Explicit human approval required: ' + kind)

    def context(self, kind):
        node = self.fresh(kind)
        return digest({'dependencies': node['dependencies'], 'files': node.get('files', []),
                       'metadata': node['metadata'], 'generation': node['generation'],
                       'pillars': self.s.get('pillars', []), 'reader_test': node.get('reader_test')})

    def required_judges(self, kind):
        if kind == 'plan':
            return ('plan_reviewer',)
        if kind in ('sourcing_plan', 'sources') or kind.startswith('addendum:'):
            return ('source_reviewer',)
        need(kind == 'synthesis' or kind.startswith('execution:'), 'Artifact is not reviewable')
        return JUDGES

    def reviewed(self, kind):
        node = self.fresh(kind)
        need(set(node['reviews']) == set(self.required_judges(kind)), 'Missing current independent reviews: ' + kind)
        for r in node['reviews'].values():
            for snap in r.get('table_files', []):
                need(self.snapshot(snap['path']) == snap, 'Review evidence changed: ' + snap['path'])
            need(r['target_hash'] == node['artifact']['sha256'] and r['context_hash'] == self.context(kind), 'Stale review: ' + kind)
        return node

    def qualified(self, kind):
        node = self.reviewed(kind)
        if kind == 'synthesis':
            self.reader_pass()
            need('backbone' not in node['metadata'] and node['metadata'].get('contributions'),
                 'Re-register legacy synthesis with complete contribution provenance')
        for r in node['reviews'].values():
            if kind.startswith('execution:') or kind == 'synthesis':
                need('execution_completeness' in r, 'Execution completeness review required')
            if kind == 'synthesis':
                need('objective_completeness' in r, 'Objective completeness review required')
            if kind == 'plan':
                need('plan_objective' in r, 'Plan-to-objective review required')
        return all(self.tables_pass(r) and not r['findings'] and all(c['passed'] for c in r.get('contribution_checks', {}).values())
                   and all(v['score'] >= 1 for v in r['scores'].values())
                   for r in node['reviews'].values())

    def reader_pass(self):
        node = self.fresh('synthesis')
        record = node.get('reader_test')
        need(record and record['target_hash'] == node['artifact']['sha256'],
             'Current independent reader test required before final judging')
        need(all(r['status'] == 'answered' for r in record['answers'].values()),
             'Reader could not recover every required answer: repair partial/missing outputs')

    def record_reader_test(self, p):
        node = self.fresh('synthesis')
        need(p.get('target_hash') == node['artifact']['sha256'], 'Reader test must bind current synthesis')
        identities = {r['reviewer'] for n in self.s['nodes'].values() for r in n['reviews'].values()}
        need(text(p.get('reviewer')) and p['reviewer'] not in identities,
             'Reader must be independent of existing judges')
        answers = p.get('answers')
        need(isinstance(answers, dict) and set(answers) == set(self.requirements()),
             'Reader must attempt every approved requirement exactly once')
        body = (self.root / node['artifact']['path']).read_text()
        for row in answers.values():
            need(row.get('status') in ('answered', 'partial', 'missing'), 'Invalid reader answer status')
            need(text(row.get('answer')) and text(row.get('scope')),
                 'Record the recovered answer and its actual scope, not a passing rationale')
            need(isinstance(row.get('gap'), str), 'Reader gap field required')
            if row['status'] == 'answered':
                need(not row['gap'].strip(), 'An answered requirement cannot retain a material gap')
            else:
                need(text(row['gap']), 'Partial/missing answers require a targeted repair description')
            quote = row.get('quote')
            need(isinstance(quote, str), 'Reader quote field required')
            if row['status'] != 'missing':
                need(text(quote) and quote in body, 'Recovered answer needs an exact excerpt from the delivered synthesis')
        self.descendants('synthesis')
        node['reviews'] = {}
        node['reader_test'] = copy.deepcopy(p)

    def requirements(self):
        reqs = self.fresh('brief')['metadata'].get('requirements')
        need(isinstance(reqs, dict) and reqs, 'Register all approved requirement IDs and text')
        return reqs

    def tasks(self):
        tasks = self.fresh('plan')['metadata'].get('tasks')
        need(isinstance(tasks, dict) and tasks, 'Register execution-plan commitments')
        return tasks

    def check_table(self, rows, expected, execution=False, planning=False):
        need(isinstance(rows, dict) and set(rows) == set(expected), 'Completeness table must cover every expected ID exactly once')
        files = []
        for row in rows.values():
            need(isinstance(row, dict) and text(row.get('reason')) and text(row.get('location')), 'Every row needs reason and evidence location')
            files.append(self.snapshot(row.get('artifact')))
            need(isinstance(row.get('findings'), list) and all(text(x) for x in row['findings']), 'Every row needs a findings list')
            if execution:
                need(row.get('status') in ('completed', 'justified_exception', 'unfinished'), 'Invalid execution status')
                if row['status'] == 'justified_exception':
                    need(text(row.get('consequence')) and text(row.get('alternatives')), 'Exception requires consequence and alternatives considered')
            else:
                need(type(row.get('score')) is int and row['score'] in (0, 1, 2), 'Completeness score must be 0/1/2')
            if planning:
                ids = row.get('tasks')
                need(isinstance(ids, list) and ids and len(ids) == len(set(ids)) and all(x in self.tasks() for x in ids), 'Map each requirement to existing plan tasks')
                need(text(row.get('inputs')) and text(row.get('output')), 'Plan mapping needs inputs and expected output')
        return files

    @staticmethod
    def tables_pass(record):
        return all(not row['findings'] and (row.get('score', 1) >= 1)
                   and row.get('status') != 'unfinished'
                   for name in ('plan_objective', 'objective_completeness', 'execution_completeness')
                   for row in record.get(name, {}).values())

    def completion_context(self):
        self.fresh('synthesis')
        return digest(self.s['nodes']['synthesis'])

    def fresh_finisher(self):
        record = self.s.get('finisher')
        need(record and record['synthesis_hash'] == self.completion_context(), 'Current independent finisher verdict required')
        for snap in record['table_files']:
            need(self.snapshot(snap['path']) == snap, 'Finisher evidence changed')
        return record

    def finisher_pass(self):
        need(self.qualified('synthesis'), 'Final judge reviews must pass first')
        record = self.fresh_finisher()
        need(record['passed'] and not record['findings'] and self.tables_pass(record), 'Finisher found unresolved completion gaps')

    def render_tables(self):
        # Derived view only; JSON in the ledger remains authoritative.
        def esc(x):
            return str(x).replace('|', r'\|').replace('\n', '<br>')
        out = []
        records = [(kind + ' / ' + judge, r) for kind, node in self.s['nodes'].items()
                   for judge, r in node['reviews'].items()]
        if self.s.get('finisher'):
            records.append(('Work finisher', self.s['finisher']))
        for label, record in records:
            for name in ('plan_objective', 'execution_completeness', 'objective_completeness'):
                if name not in record:
                    continue
                out.extend(['## ' + label + ': ' + name, '', '| ID | Score/status | Evidence | Reason / gaps |', '|---|---|---|---|'])
                for key, row in record[name].items():
                    detail = row['reason'] + '; ' + '; '.join(row['findings'])
                    if name == 'plan_objective':
                        detail += '; tasks: ' + ', '.join(row['tasks']) + '; inputs: ' + row['inputs'] + '; output: ' + row['output']
                    if row.get('status') == 'justified_exception':
                        detail += '; consequence: ' + row['consequence'] + '; alternatives: ' + row['alternatives']
                    out.append('| ' + ' | '.join(map(esc, [key, row.get('status', row.get('score')), row['artifact'] + ' / ' + row['location'], detail])) + ' |')
                out.append('')
        return '\n'.join(out)

    def all_three(self, prefix):
        for worker in WORKERS:
            self.reviewed(prefix + ':' + worker)

    def put(self, kind, artifact, dependencies, metadata=None, files=None):
        for dep in dependencies:
            self.fresh(dep)
        snap = self.snapshot(artifact)
        need(files is None or isinstance(files, list), 'files must be a list of local paths')
        file_snaps = [self.snapshot(f) for f in (files or [])]
        self.invalidate(kind)
        self.s['nodes'][kind] = {'artifact': snap, 'generation': self.s['revision'] + 1, 'dependencies': {
            d: digest(self.s['nodes'][d]) for d in dependencies}, 'metadata': metadata or {}, 'files': file_snaps, 'reviews': {}}

    def register(self, p):
        kind = p.get('kind', '')
        base = ['question', 'brief']
        metadata = {}
        files = p.get('files', [])
        need(isinstance(files, list), 'files must be a list of local paths')
        if kind == 'sourcing_plan':
            self.approved('brief')
            deps = base
        elif kind.startswith('lane:'):
            need(kind.split(':')[1] in LANES, 'Unknown searcher lane')
            self.approved('sourcing_plan')
            deps = base + ['sourcing_plan']
        elif kind == 'sources':
            self.approved('sourcing_plan')
            deps = base + ['sourcing_plan'] + ['lane:' + lane for lane in LANES]
        elif kind.startswith('addendum:'):
            need(text(kind.split(':', 1)[1]), 'Addendum identifier required')
            self.approved('plan')
            need(text(p.get('reason')), 'Explain why evidence is within approved method')
            metadata = {'reason': p['reason']}
            deps = base + ['sources', 'plan']
        elif kind == 'plan':
            self.approved('sources')
            need(self.qualified('sources'), 'Sources must pass independent review')
            deps = base + ['sourcing_plan', 'sources']
            tasks = p.get('tasks')
            need(isinstance(tasks, dict) and tasks, 'Plan task IDs required')
            for key, task in tasks.items():
                need(text(key) and isinstance(task, dict) and text(task.get('description')), 'Task needs ID and description')
                reqs = task.get('requirements')
                need(isinstance(reqs, list) and reqs and len(reqs) == len(set(reqs)) and all(r in self.requirements() for r in reqs), 'Task must map to approved requirements')
                need(isinstance(task.get('sources'), list) and all(text(x) for x in task['sources']), 'Task sources must be source IDs; may be empty for nonsource tasks')
            metadata = {'tasks': tasks}
        elif kind.startswith('execution:'):
            need(kind.split(':')[1] in WORKERS, 'Unknown worker')
            self.approved('plan')
            deps = base + ['sources', 'plan'] + [k for k, n in self.s['nodes'].items() if k.startswith('addendum:') and n.get('accepted')]
        elif kind == 'synthesis':
            self.all_three('execution')
            need('backbone' not in p, 'Use verified contributions, not a selected backbone')
            need(text(p.get('reason')), 'Explain how supported findings combine to answer the brief')
            contributions = p.get('contributions')
            need(isinstance(contributions, list) and contributions, 'Identify every included contribution; at least one is required')
            for c in contributions:
                need(isinstance(c, dict) and c.get('worker') in WORKERS, 'Contribution worker required')
                self.reviewed('execution:' + c['worker'])
                need(text(c.get('location')) and text(c.get('use')) and text(c.get('verification')),
                     'Identify contribution location, use and local verification artifact')
                files = files + [c['verification']]
            metadata = {k: p[k] for k in ('reason', 'contributions')}
            deps = base + ['sources', 'plan'] + ['execution:' + w for w in WORKERS]
        else:
            raise Invalid('Unknown artifact kind')
        self.put(kind, p.get('artifact'), deps, metadata, files)

    def apply(self, command, payload=None):
        # Failed commands do not mutate even an in-memory coordinator instance.
        self._fresh_cache = set()
        previous = copy.deepcopy(self.s)
        try:
            return self._apply(command, payload or {})
        except Exception:
            self.s = previous
            self._fresh_cache = set()
            raise

    def _apply(self, command, p):
        if command == 'init':
            need(self.s is None, 'Run already initialized')
            self.s = {'version': 5, 'revision': 0, 'nodes': {}, 'history': [], 'pillars': []}
            self.put('question', p.get('question'), [], files=p.get('files'))
        else:
            need(self.s is not None, 'Initialize run first')
            if command == 'render':
                self._apply('check', {})
                return {'markdown': self.render_tables()}
            if command in ('status', 'check'):
                if command == 'check':
                    for k in self.s['nodes']:
                        self.fresh(k)
                    if self.s.get('finisher'):
                        self.fresh_finisher()
                    if self.s.get('delivery'):
                        self.finisher_pass()
                return self.status()
            if command == 'approve':
                kind = APPROVALS.get(p.get('kind'))
                need(kind is not None, 'Unknown approval kind')
                node = self.fresh(kind)
                need(not (self.autonomous() and kind in ('sourcing_plan', 'sources', 'plan')),
                     'Autonomous stages use internal gates, not human approval records')
                if kind in ('sourcing_plan', 'sources', 'plan'):
                    need(self.qualified(kind), 'Independent review must pass before user approval')
                need(p.get('target_hash') == node['artifact']['sha256'] and p.get('context_hash') == self.context(kind),
                     'Approval must bind the exact displayed artifact and context')
                approval = dict(attestation(p), target_hash=p['target_hash'], context_hash=p['context_hash'])
                if node.get('approval') == approval:
                    return self.status()
                self.descendants(kind)
                node['approval'] = approval
            elif command == 'permit-brief':
                current = self.fresh('brief')
                need(p.get('target_hash') == current['artifact']['sha256'] and p.get('context_hash') == self.context('brief'),
                     'Brief permission must bind the displayed current brief and context')
                self.s['brief_permission'] = dict(attestation(p), brief_hash=digest(self.s['nodes']['brief']),
                    proposed={'artifact': self.snapshot(p.get('artifact')), 'pillars': p.get('pillars'), 'requirements': p.get('requirements'),
                              'mode': p.get('mode', current['metadata']['mode']),
                              'files': [self.snapshot(f) for f in p.get('files', [])]})
            elif command in ('objective', 'revise-brief'):
                self.approved('question')
                if command == 'objective':
                    need('brief' not in self.s['nodes'], 'Use permit-brief then revise-brief')
                else:
                    permission = self.s.get('brief_permission')
                    need(permission and permission['brief_hash'] == digest(self.s['nodes'].get('brief')), 'Record explicit brief revision permission BEFORE registration')
                mode = p.get('mode', self.s['nodes'].get('brief', {}).get('metadata', {}).get('mode', 'autonomous'))
                need(mode in ('autonomous', 'interactive'), 'Mode must be autonomous or interactive')
                requirements = p.get('requirements')
                need(isinstance(requirements, dict) and requirements and all(text(k) and text(x) for k, x in requirements.items()), 'Register every approved requirement ID and text')
                pillars = p.get('pillars')
                need(isinstance(pillars, list) and pillars and all(text(x) for x in pillars) and len(set(pillars)) == len(pillars), 'Unique nonempty pillar IDs required')
                if command == 'revise-brief':
                    proposed = {'artifact': self.snapshot(p.get('artifact')), 'pillars': pillars, 'requirements': requirements, 'mode': mode,
                                'files': [self.snapshot(f) for f in p.get('files', [])]}
                    need(proposed == permission['proposed'], 'Revision differs from the explicitly permitted brief draft')
                self.put('brief', p.get('artifact'), ['question'], {'pillars': pillars, 'requirements': requirements, 'mode': mode}, p.get('files'))
                self.s['pillars'] = pillars
                self.s.pop('brief_permission', None)
            elif command == 'revise-question':
                self.put('question', p.get('question'), [], files=p.get('files'))
                self.s['pillars'] = []
                self.s.pop('brief_permission', None)
            elif command == 'register':
                self.register(p)
            elif command == 'reader-test':
                self.record_reader_test(p)
            elif command == 'review':
                kind = p.get('target')
                need(isinstance(kind, str), 'Review target required')
                node = self.fresh(kind)
                need(p.get('judge') in self.required_judges(kind), 'Unknown judge for target')
                need(p.get('target_hash') == node['artifact']['sha256'] and p.get('context_hash') == self.context(kind), 'Review must bind current artifact and context hashes')
                scores = p.get('scores')
                need(isinstance(scores, dict) and set(scores) == set(self.s['pillars']), 'Score every current pillar exactly once')
                for value in scores.values():
                    need(isinstance(value, dict) and type(value.get('score')) is int and value['score'] in (0, 1, 2), 'Scores must be integer 0/1/2')
                    need(text(value.get('reason')) and text(value.get('evidence')), 'Each score requires reason and evidence location')
                if kind == 'synthesis':
                    self.reader_pass()
                    need(p.get('reviewer') != node['reader_test']['reviewer'], 'Reader cannot also be a final judge')
                    checks = p.get('contribution_checks')
                    expected = {str(i) for i in range(len(node['metadata']['contributions']))}
                    need(isinstance(checks, dict) and set(checks) == expected, 'Final judges must check each imported contribution by zero-based index')
                    for c in checks.values():
                        need(isinstance(c, dict) and type(c.get('passed')) is bool and text(c.get('reason')) and text(c.get('evidence')),
                             'Contribution check needs passed boolean, reason, evidence')
                table_files = []
                if kind.startswith('execution:') or kind == 'synthesis':
                    table_files += self.check_table(p.get('execution_completeness'), self.tasks(), execution=True)
                if kind == 'synthesis':
                    table_files += self.check_table(p.get('objective_completeness'), self.requirements())
                if kind == 'plan':
                    table_files += self.check_table(p.get('plan_objective'), self.requirements(), planning=True)
                findings = p.get('findings')
                need(isinstance(findings, list), 'Explicit material findings list required')
                for finding in findings:
                    need(isinstance(finding, dict) and all(text(finding.get(k)) for k in ('id', 'description', 'evidence', 'severity')), 'Finding needs id, description, evidence and severity')
                    need(finding['severity'] in ('material', 'critical'), 'All recorded findings are blocking material/critical findings')
                need(len({f['id'] for f in findings}) == len(findings), 'Finding IDs must be unique')
                need(text(p.get('reviewer')), 'Record independent reviewer identity/role attestation')
                self.descendants(kind)
                node.pop('approval', None)
                node.pop('accepted', None)
                node['reviews'][p['judge']] = dict(copy.deepcopy(p), table_files=table_files)
            elif command == 'accept-addendum':
                kind = p.get('target', '')
                need(kind.startswith('addendum:') and self.qualified(kind), 'Reviewed qualifying addendum required')
                self.approved('plan')
                self.descendants(kind)
                for worker in WORKERS:
                    self.invalidate('execution:' + worker)
                self.s['nodes'][kind]['accepted'] = True
            elif command == 'budget':
                need(text(p.get('limit')) and text(p.get('used')) and text(p.get('remaining')) and text(p.get('decision')), 'Record overall limit, used, remaining, decision')
                self.s['budget'] = copy.deepcopy(p)
            elif command == 'finish':
                need(self.qualified('synthesis'), 'Final synthesis reviews must pass before finishing')
                need(p.get('synthesis_hash') == self.completion_context(), 'Finisher must bind current reviewed synthesis')
                need(p.get('reviewer') != self.s['nodes']['synthesis']['reader_test']['reviewer'], 'Reader cannot also be finisher')
                reviewers = {r['reviewer'] for n in self.s['nodes'].values() for r in n['reviews'].values()}
                need(text(p.get('reviewer')) and p['reviewer'] not in reviewers, 'Use a separate independent work finisher')
                need(type(p.get('passed')) is bool and text(p.get('reason')), 'Finisher requires verdict and reason')
                need(isinstance(p.get('findings'), list) and all(text(x) for x in p['findings']), 'Finisher findings required')
                table_files = self.check_table(p.get('objective_completeness'), self.requirements())
                table_files += self.check_table(p.get('execution_completeness'), self.tasks(), execution=True)
                self.s['finisher'] = dict(copy.deepcopy(p), table_files=table_files)
                self.s.pop('delivery', None)
            elif command == 'deliver':
                need(self.qualified('synthesis'), 'Actual final synthesis must pass all three final judges; otherwise stop with blocker')
                self.finisher_pass()
                self.s['delivery'] = {'synthesis_hash': digest(self.s['nodes']['synthesis'])}
            elif command == 'stop':
                need(text(p.get('reason')), 'Blocker reason required')
                self.s['blocker'] = {'artifact': self.snapshot(p.get('artifact')), 'reason': p['reason']}
                self.s.pop('delivery', None)
            else:
                raise Invalid('Unknown command: ' + command)
        self.s['revision'] += 1
        self.s['history'].append({'revision': self.s['revision'], 'at': datetime.now(timezone.utc).isoformat(),
            'command': command, 'payload': copy.deepcopy(p),
            'state': copy.deepcopy({k: v for k, v in self.s.items() if k != 'history'})})
        self.save()
        return self.status()

    def save(self):
        archive = self.root / '.state-artifacts'
        need(not archive.is_symlink(), 'Archive cannot be a symlink')
        archive.mkdir(exist_ok=True)
        snapshots = [snap for n in self.s['nodes'].values() for snap in [n['artifact']] + n.get('files', [])]
        snapshots += [snap for n in self.s['nodes'].values() for r in n['reviews'].values() for snap in r.get('table_files', [])]
        snapshots += self.s.get('finisher', {}).get('table_files', [])
        if 'blocker' in self.s:
            snapshots.append(self.s['blocker']['artifact'])
        for snap in snapshots:
            dest = archive / snap['sha256']
            need(not dest.is_symlink(), 'Archive entry cannot be a symlink')
            if not dest.exists():
                data = (self.root / snap['path']).read_bytes()
                need(hashlib.sha256(data).hexdigest() == snap['sha256'], 'Artifact changed during save')
                dest.write_bytes(data)
        tmp = self.root / '.research-state.tmp'
        need(not tmp.is_symlink(), 'Temporary ledger cannot be a symlink')
        tmp.write_text(json.dumps(self.s, indent=2) + '\n')
        tmp.replace(self.path)

    def status(self):
        nodes = {}
        for kind, node in self.s['nodes'].items():
            item = {'target_hash': node['artifact']['sha256'], 'approved': 'approval' in node,
                    'reviews': copy.deepcopy(node['reviews']), 'metadata': node['metadata'],
                    'artifact': node['artifact'], 'files': node.get('files', []),
                    'reader_test': copy.deepcopy(node.get('reader_test'))}
            try:
                item['context_hash'] = self.context(kind)
                item['fresh'] = True
                if kind in ('sourcing_plan', 'sources', 'plan', 'synthesis') or kind.startswith(('execution:', 'addendum:')):
                    try:
                        item['qualified'] = self.qualified(kind)
                    except Invalid as e:
                        item.update(qualified=False, review_gate=str(e))
            except (Invalid, OSError) as e:
                item.update(fresh=False, error=str(e))
            nodes[kind] = item
        completion = {'fresh': False, 'deliverable': False}
        if self.s.get('finisher'):
            try:
                self.fresh_finisher()
                completion['fresh'] = True
                self.finisher_pass()
                completion['deliverable'] = True
            except (Invalid, OSError) as error:
                completion['error'] = str(error)
        return {'revision': self.s['revision'], 'nodes': nodes, 'completion': completion,
                'completion_context': self.completion_context() if 'synthesis' in self.s['nodes'] and nodes.get('synthesis', {}).get('fresh') else None,
                'finisher': self.s.get('finisher'), 'delivery': self.s.get('delivery'), 'blocker': self.s.get('blocker'), 'budget': self.s.get('budget')}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('run')
    parser.add_argument('command')
    parser.add_argument('payload', nargs='?')
    args = parser.parse_args()
    try:
        payload = json.loads(Path(args.payload).read_text()) if args.payload else {}
        need(isinstance(payload, dict), 'Payload must be a JSON object')
        print(json.dumps(ResearchState(args.run).apply(args.command, payload), indent=2))
    except (Invalid, OSError, ValueError, KeyError, TypeError) as e:
        print('error: ' + str(e), file=sys.stderr)
        return 2
    return 0

if __name__ == '__main__':
    sys.exit(main())
