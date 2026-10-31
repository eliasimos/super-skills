import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('research_state', Path(__file__).resolve().parents[1] / 'scripts/research_state.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class StateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.state = m.ResearchState(self.root)
        self.serial = 0
        self.state.apply('init', {'question': self.file('Question')})

    def file(self, content='Evidence'):
        self.serial += 1
        name = f'artifact-{self.serial}.md'
        (self.root / name).write_text(content + str(self.serial))
        return name

    def approve(self, kind):
        node = self.state.apply('status')['nodes'][m.APPROVALS[kind]]
        return self.state.apply('approve', {'kind': kind, 'message': 'I approve this version.', 'reference': 'user-message-1',
            'target_hash': node['target_hash'], 'context_hash': node['context_hash']})

    def register(self, kind, **extra):
        if kind == 'plan':
            extra.setdefault('tasks', {'T1': {'description': 'Inspect S1 and calculate result', 'requirements': ['R1'], 'sources': ['S1']}})
        return self.state.apply('register', {'kind': kind, 'artifact': self.file(kind), **extra})

    def reader(self, status='answered', **changes):
        node = self.state.s['nodes']['synthesis']
        row = {'status': status, 'answer': 'Recovered result', 'scope': 'Approved scope',
               'quote': (self.root / node['artifact']['path']).read_text(),
               'gap': '' if status == 'answered' else 'Integrated answer absent'}
        row.update(changes)
        return self.state.apply('reader-test', {'reviewer': 'fresh-reader',
            'target_hash': node['artifact']['sha256'], 'answers': {'R1': row}})

    def review(self, kind, judge, findings=None, score=2):
        if kind == 'synthesis' and not self.state.s['nodes'][kind].get('reader_test'):
            self.reader()
        board = self.state.apply('status')['nodes'][kind]
        return self.state.apply('review', {'target': kind, 'judge': judge, 'reviewer': 'independent-' + judge,
            'target_hash': board['target_hash'], 'context_hash': board['context_hash'],
            'scores': {'p1': {'score': score, 'reason': 'Supported', 'evidence': 'artifact section 1'}},
            **self.tables(kind), 'findings': findings or [], 'contribution_checks': {str(i): {'passed': True, 'reason': 'Checked component', 'evidence': 'verification section 1'}
                for i in range(len(self.state.s['nodes'][kind]['metadata'].get('contributions', [])))}})

    def tables(self, kind):
        path = self.state.s['nodes'][kind]['artifact']['path']
        row = {'artifact': path, 'location': 'section 1', 'reason': 'Checked against originals', 'findings': []}
        result = {}
        if kind.startswith('execution:') or kind == 'synthesis':
            result['execution_completeness'] = {'T1': dict(row, status='completed')}
        if kind == 'synthesis':
            result['objective_completeness'] = {'R1': dict(row, score=2)}
        if kind == 'plan':
            result['plan_objective'] = {'R1': dict(row, score=2, tasks=['T1'], inputs='S1 records', output='Decision estimate')}
        return result

    def finish(self, **changes):
        data = {'reviewer': 'separate-finisher', 'passed': True, 'reason': 'Independently verified completeness',
                'synthesis_hash': self.state.apply('status')['completion_context'], 'findings': [], **self.tables('synthesis')}
        data.update(changes)
        return self.state.apply('finish', data)

    def all_reviews(self, kind):
        for judge in m.JUDGES:
            self.review(kind, judge)

    def objective(self):
        self.approve('question')
        self.state.apply('objective', {'artifact': self.file('Brief'), 'pillars': ['p1'], 'requirements': {'R1': 'Answer the decision'}, 'mode': 'interactive'})
        self.approve('objective')

    def sources(self):
        self.objective()
        self.register('sourcing_plan')
        self.review('sourcing_plan', 'source_reviewer')
        self.approve('sourcing_plan')
        for lane in m.LANES:
            self.register('lane:' + lane)
        self.register('sources')
        self.review('sources', 'source_reviewer')
        self.approve('sources')

    def plan(self):
        self.sources()
        self.register('plan')
        self.review('plan', 'plan_reviewer')
        self.approve('plan')

    def components(self):
        return [{'worker': 'worker1', 'location': 'section 2', 'use': 'Supported finding',
                 'verification': self.file('Independent component verification')}]

    def synthesis(self):
        self.plan()
        for worker in m.WORKERS:
            self.register('execution:' + worker)
            self.all_reviews('execution:' + worker)
        self.register('synthesis', reason='Most complete supported answer',
                      contributions=[{'worker': 'worker1', 'location': 'section 2', 'use': 'Boundary case', 'verification': self.file('Component verification')}])

    def test_reader_partial_blocks_unanimous_passing_review(self):
        self.synthesis()
        self.reader('partial')
        for judge in m.JUDGES:
            with self.assertRaises(m.Invalid):
                self.review('synthesis', judge)
        with self.assertRaises(m.Invalid):
            self.state.apply('deliver')

    def test_reader_missing_cannot_be_bypassed_by_direct_review(self):
        self.synthesis()
        node = self.state.apply('status')['nodes']['synthesis']
        with self.assertRaisesRegex(m.Invalid, 'reader test required'):
            self.state.apply('review', {'target': 'synthesis', 'judge': 'adherence',
                'reviewer': 'independent-adherence', 'target_hash': node['target_hash'],
                'context_hash': node['context_hash'],
                'scores': {'p1': {'score': 2, 'reason': 'All fine', 'evidence': 'Report'}}})

    def test_reader_quote_must_exist(self):
        self.synthesis()
        with self.assertRaises(m.Invalid):
            self.reader(quote='An invented result absent from report')

    def test_reader_replacement_invalidates_release(self):
        self.synthesis()
        self.all_reviews('synthesis')
        self.finish()
        self.state.apply('deliver')
        self.reader('missing', quote='')
        self.assertFalse(self.state.s['nodes']['synthesis']['reviews'])
        self.assertNotIn('finisher', self.state.s)
        self.assertNotIn('delivery', self.state.s)

    def test_question_and_approval_sequence(self):
        with self.assertRaises(m.Invalid):
            self.state.apply('objective', {'artifact': self.file(), 'pillars': ['p1'], 'requirements': {'R1': 'Answer the decision'}, 'mode': 'interactive'})
        self.approve('question')
        self.state.apply('objective', {'artifact': self.file(), 'pillars': ['p1'], 'requirements': {'R1': 'Answer the decision'}, 'mode': 'interactive'})
        with self.assertRaises(m.Invalid):
            self.register('sourcing_plan')
        self.approve('objective')
        self.register('sourcing_plan')
        with self.assertRaises(m.Invalid):
            self.register('lane:tools')
        with self.assertRaises(m.Invalid):
            self.state.apply('approve', {'kind': 'sourcing_plan'})

    def test_approval_binds_displayed_version(self):
        board = self.state.apply('status')['nodes']['question']
        question = self.state.s['nodes']['question']['artifact']['path']
        self.state.apply('revise-question', {'question': question})
        with self.assertRaises(m.Invalid):
            self.state.apply('approve', {'kind': 'question', 'message': 'Approved', 'reference': 'user-1',
                'target_hash': board['target_hash'], 'context_hash': board['context_hash']})
        self.approve('question')

    def test_five_lanes_and_review_before_sources_approval(self):
        self.objective()
        self.register('sourcing_plan')
        self.review('sourcing_plan', 'source_reviewer')
        self.approve('sourcing_plan')
        for lane in m.LANES[:-1]:
            self.register('lane:' + lane)
        with self.assertRaises(m.Invalid):
            self.register('sources')
        self.register('lane:tools')
        self.register('sources')
        with self.assertRaises(m.Invalid):
            self.approve('sources')
        with self.assertRaises(m.Invalid):
            self.register('plan')
        self.review('sources', 'source_reviewer')
        self.approve('sources')
        self.register('plan')

    def test_interactive_plan_requires_review_and_user_approval(self):
        self.sources()
        self.register('plan')
        with self.assertRaises(m.Invalid):
            self.register('execution:worker1')
        with self.assertRaises(m.Invalid):
            self.review('plan', 'adherence')
        with self.assertRaises(m.Invalid):
            self.register('proposal:worker1')
        with self.assertRaises(m.Invalid):
            self.approve('plan')
        self.review('plan', 'plan_reviewer')
        self.approve('plan')
        self.register('execution:worker1')
        self.register('plan')
        self.assertNotIn('execution:worker1', self.state.s['nodes'])
        with self.assertRaises(m.Invalid):
            self.register('execution:worker1')

    def test_nine_execution_reviews_and_actual_final_required(self):
        self.plan()
        for worker in m.WORKERS:
            self.register('execution:' + worker)
            for judge in m.JUDGES:
                if (worker, judge) != ('worker3', 'plausibility'):
                    self.review('execution:' + worker, judge)
        with self.assertRaises(m.Invalid):
            self.register('synthesis', reason='Best', contributions=self.components())
        self.review('execution:worker3', 'plausibility')
        self.register('synthesis', reason='Best', contributions=self.components())
        with self.assertRaises(m.Invalid):
            self.state.apply('deliver')
        self.review('synthesis', 'adherence')
        self.review('synthesis', 'correctness')
        with self.assertRaises(m.Invalid):
            self.state.apply('deliver')
        self.review('synthesis', 'plausibility')
        self.finish()
        self.state.apply('deliver')
        self.assertIsNotNone(self.state.s['delivery'])

    def test_critical_failure_blocks_high_scores(self):
        self.synthesis()
        self.all_reviews('synthesis')
        self.review('synthesis', 'correctness', [{'id': 'f1', 'description': 'Fatal error',
                     'evidence': 'section 1', 'severity': 'critical'}])
        with self.assertRaises(m.Invalid):
            self.state.apply('deliver')
        self.state.apply('stop', {'artifact': self.file('Blocker'), 'reason': 'Unresolved critical finding'})
        self.assertIn('blocker', self.state.s)

    def test_changed_final_content_and_stale_review_refused(self):
        self.synthesis()
        self.all_reviews('synthesis')
        old = self.state.apply('status')['nodes']['synthesis']
        self.register('synthesis', reason='Revised', contributions=self.components())
        with self.assertRaises(m.Invalid):
            self.state.apply('review', {'target': 'synthesis', 'judge': 'adherence',
                'target_hash': old['target_hash'], 'context_hash': old['context_hash']})
        self.all_reviews('synthesis')
        (self.root / self.state.s['nodes']['synthesis']['artifact']['path']).write_text('tampered')
        with self.assertRaises(m.Invalid):
            self.state.apply('deliver')
        with self.assertRaises(m.Invalid):
            self.state.apply('check')

    def test_brief_revision_permission_and_history_preserved(self):
        self.sources()
        question = self.state.s['nodes']['question'].copy()
        oldbrief = self.state.s['nodes']['brief']['artifact']['sha256']
        with self.assertRaises(m.Invalid):
            self.state.apply('revise-brief', {'artifact': self.file(), 'pillars': ['p1'], 'requirements': {'R1': 'Answer the decision'}, 'mode': 'interactive'})
        draft = self.file('Proposed brief')
        current = self.state.apply('status')['nodes']['brief']
        self.state.apply('permit-brief', {'message': 'Please revise the brief for this new scope.', 'reference': 'user-2', 'artifact': draft, 'pillars': ['p1'], 'requirements': {'R1': 'Answer the decision'},
            'target_hash': current['target_hash'], 'context_hash': current['context_hash']})
        with self.assertRaises(m.Invalid):
            self.state.apply('revise-brief', {'artifact': self.file('Other draft'), 'pillars': ['p1'], 'requirements': {'R1': 'Answer the decision'}, 'mode': 'interactive'})
        self.state.apply('revise-brief', {'artifact': draft, 'pillars': ['p1'], 'requirements': {'R1': 'Answer the decision'}, 'mode': 'interactive'})
        self.assertEqual(self.state.s['nodes']['question'], question)
        self.assertEqual(set(self.state.s['nodes']), {'question', 'brief'})
        self.assertNotIn('approval', self.state.s['nodes']['brief'])
        self.assertTrue((self.root / '.state-artifacts' / oldbrief).is_file())
        self.assertTrue(any('sources' in e['state']['nodes'] for e in self.state.s['history']))
        with self.assertRaises(m.Invalid):
            self.state.apply('revise-brief', {'artifact': self.file(), 'pillars': ['p1'], 'requirements': {'R1': 'Answer the decision'}, 'mode': 'interactive'})

    def test_revised_sources_preserves_upstream_invalidates_downstream(self):
        self.synthesis()
        upstream = {k: self.state.s['nodes'][k].copy() for k in ('question', 'brief', 'sourcing_plan', 'lane:tools')}
        self.register('sources')
        for k, value in upstream.items():
            self.assertEqual(self.state.s['nodes'][k], value)
        self.assertNotIn('plan', self.state.s['nodes'])
        self.assertNotIn('synthesis', self.state.s['nodes'])
        self.assertFalse(self.state.s['nodes']['sources']['reviews'])
        self.assertNotIn('approval', self.state.s['nodes']['sources'])

    def test_addendum_keeps_approvals_and_forces_execution_recheck(self):
        self.synthesis()
        original = {k: self.state.s['nodes'][k].copy() for k in ('question', 'brief', 'sourcing_plan', 'sources', 'plan')}
        self.register('addendum:extra', reason='More evidence under approved method')
        with self.assertRaises(m.Invalid):
            self.state.apply('accept-addendum', {'target': 'addendum:extra'})
        self.review('addendum:extra', 'source_reviewer')
        self.state.apply('accept-addendum', {'target': 'addendum:extra'})
        for k, node in original.items():
            self.assertEqual(node, self.state.s['nodes'][k])
        self.assertNotIn('synthesis', self.state.s['nodes'])
        self.assertNotIn('execution:worker1', self.state.s['nodes'])
        self.register('execution:worker1')
        self.assertIn('addendum:extra', self.state.s['nodes']['execution:worker1']['dependencies'])

    def test_files_and_generation_bind_reviews(self):
        self.plan()
        evidence = self.file('Evidence table')
        self.register('execution:worker1', files=[evidence])
        old = self.state.apply('status')['nodes']['execution:worker1']
        artifact = self.state.s['nodes']['execution:worker1']['artifact']['path']
        self.state.apply('register', {'kind': 'execution:worker1', 'artifact': artifact, 'files': [evidence]})
        new = self.state.apply('status')['nodes']['execution:worker1']
        self.assertEqual(old['target_hash'], new['target_hash'])
        self.assertNotEqual(old['context_hash'], new['context_hash'])
        with self.assertRaises(m.Invalid):
            self.state.apply('review', {'target': 'execution:worker1', 'judge': 'correctness',
                'target_hash': old['target_hash'], 'context_hash': old['context_hash']})
        (self.root / evidence).write_text('Changed evidence')
        with self.assertRaises(m.Invalid):
            self.state.apply('check')

    def test_component_synthesis_and_failed_verification(self):
        self.plan()
        for worker in m.WORKERS:
            self.register('execution:' + worker)
            self.all_reviews('execution:' + worker)
            self.review('execution:' + worker, 'adherence', [{
                'id': 'gap', 'severity': 'material',
                'description': 'A separate required section is missing', 'evidence': 'Candidate section 5'}])
        # No whole candidate qualifies; verified components can still form a complete answer.
        with self.assertRaises(m.Invalid):
            self.register('synthesis', reason='No provenance', contributions=[])
        with self.assertRaises(m.Invalid):
            self.register('synthesis', backbone='worker1', reason='Old schema', contributions=self.components())
        parts=self.components()+[{'worker': 'worker2', 'location': 'section 5', 'use': 'Fill missing section',
                                 'verification': self.file('Checked second component')}]
        self.register('synthesis', reason='Complementary verified findings', contributions=parts)
        self.all_reviews('synthesis')
        payload=dict(self.state.s['nodes']['synthesis']['reviews']['correctness'])
        payload['contribution_checks']['1']={'passed': False, 'reason': 'Source assumption unresolved', 'evidence': 'Section 5'}
        self.state.apply('review', payload)
        with self.assertRaises(m.Invalid):
            self.state.apply('deliver')
        self.review('synthesis', 'correctness')
        self.finish()
        self.state.apply('deliver')


    def test_autonomous_full_flow_and_review_gates(self):
        self.approve('question')
        self.state.apply('objective', {'artifact': self.file('Brief: autonomous after approval'),
                                      'pillars': ['p1'], 'requirements': {'R1': 'Answer the decision'}, 'mode': 'autonomous'})
        with self.assertRaises(m.Invalid):
            self.register('sourcing_plan')
        self.approve('objective')
        self.register('sourcing_plan')
        with self.assertRaises(m.Invalid):
            self.approve('sourcing_plan')
        self.review('sourcing_plan', 'source_reviewer')
        for lane in m.LANES:
            self.register('lane:' + lane)
        self.register('sources')
        with self.assertRaises(m.Invalid):
            self.register('plan')
        self.review('sources', 'source_reviewer')
        self.register('plan')
        with self.assertRaises(m.Invalid):
            self.register('execution:worker1')
        self.review('plan', 'plan_reviewer', [{'id': 'p', 'severity': 'material',
            'description': 'Method does not answer brief', 'evidence': 'Plan section 1'}])
        with self.assertRaises(m.Invalid):
            self.register('execution:worker1')
        self.register('plan')
        self.review('plan', 'plan_reviewer')
        for worker in m.WORKERS:
            self.register('execution:' + worker)
            self.all_reviews('execution:' + worker)
        self.register('synthesis', reason='Supported answer', contributions=self.components())
        self.all_reviews('synthesis')
        self.finish()
        self.state.apply('deliver')
        for kind in ('sourcing_plan', 'sources', 'plan'):
            self.assertNotIn('approval', self.state.s['nodes'][kind])
        self.review('plan', 'plan_reviewer', score=0)
        self.assertNotIn('delivery', self.state.s)
        self.assertNotIn('execution:worker1', self.state.s['nodes'])

    def test_mode_is_bound_to_objective_approval(self):
        self.objective()
        with self.assertRaises(m.Invalid):
            self.state.apply('objective', {'artifact': self.file(), 'pillars': ['p1'], 'requirements': {'R1': 'Answer the decision'}, 'mode': 'autonomous'})
        with self.assertRaises(m.Invalid):
            self.state.apply('revise-brief', {'artifact': self.file(), 'pillars': ['p1'], 'requirements': {'R1': 'Answer the decision'}, 'mode': 'autonomous'})

    def test_completeness_and_finisher_gate(self):
        self.synthesis()
        self.all_reviews('synthesis')
        with self.assertRaises(m.Invalid):
            self.state.apply('deliver')
        with self.assertRaises(m.Invalid):
            self.finish(objective_completeness={})
        with self.assertRaises(m.Invalid):
            self.finish(reviewer='independent-correctness')
        self.finish(passed=False, findings=['One material check remains'])
        with self.assertRaises(m.Invalid):
            self.state.apply('deliver')
        self.finish()
        self.state.apply('deliver')
        self.review('synthesis', 'correctness')
        with self.assertRaises(m.Invalid):
            self.state.apply('deliver')
        self.finish()
        self.assertIn('objective_completeness', self.state.apply('render')['markdown'])
        self.assertIn('execution_completeness', self.state.apply('render')['markdown'])

    def test_missing_and_unfinished_rows_block(self):
        self.synthesis()
        self.all_reviews('synthesis')
        data = dict(self.state.s['nodes']['synthesis']['reviews']['correctness'])
        data['execution_completeness'] = {}
        with self.assertRaises(m.Invalid):
            self.state.apply('review', data)
        data.update(self.tables('synthesis'))
        data['execution_completeness']['T1']['status'] = 'unfinished'
        self.state.apply('review', data)
        with self.assertRaises(m.Invalid):
            self.finish()
        data['execution_completeness']['T1'].update(status='justified_exception')
        with self.assertRaises(m.Invalid):
            self.state.apply('review', data)
        data['execution_completeness']['T1'].update(consequence='Result remains conditional', alternatives='Alternate source unavailable')
        data['objective_completeness']['R1']['score'] = 0
        self.state.apply('review', data)
        with self.assertRaises(m.Invalid):
            self.finish()

    def test_completeness_evidence_edit_invalidates_review(self):
        self.synthesis()
        self.all_reviews('synthesis')
        evidence = self.file('Verified dataset')
        data = dict(self.state.s['nodes']['synthesis']['reviews']['correctness'])
        data.update(self.tables('synthesis'))
        data['objective_completeness']['R1']['artifact'] = evidence
        self.state.apply('review', data)
        self.finish()
        (self.root / evidence).write_text('Changed dataset')
        with self.assertRaises(m.Invalid):
            self.state.apply('deliver')

    def test_plan_requires_complete_objective_mapping(self):
        self.sources()
        self.register('plan')
        self.review('plan', 'plan_reviewer')
        data=dict(self.state.s['nodes']['plan']['reviews']['plan_reviewer'])
        data['plan_objective']={}
        with self.assertRaises(m.Invalid):
            self.state.apply('review', data)
        data.update(self.tables('plan'))
        data['plan_objective']['R1']['score']=0
        self.state.apply('review', data)
        with self.assertRaises(m.Invalid):
            self.approve('plan')

    def test_upstream_review_evidence_invalidates_finish(self):
        self.plan()
        for worker in m.WORKERS:
            self.register('execution:' + worker)
            self.all_reviews('execution:' + worker)
        evidence = self.file('Execution review evidence')
        data=dict(self.state.s['nodes']['execution:worker1']['reviews']['correctness'])
        data['execution_completeness']['T1']['artifact']=evidence
        self.state.apply('review', data)
        self.register('synthesis', reason='Verified findings', contributions=self.components())
        self.all_reviews('synthesis')
        self.finish()
        (self.root / evidence).write_text('Changed upstream evidence')
        with self.assertRaises(m.Invalid):
            self.state.apply('deliver')
        with self.assertRaises(m.Invalid):
            self.state.apply('check')
        self.assertFalse(self.state.apply('status')['completion']['deliverable'])

    def test_finisher_evidence_change_after_delivery(self):
        self.synthesis()
        self.all_reviews('synthesis')
        evidence=self.file('Finisher evidence')
        rows=self.tables('synthesis')['objective_completeness']
        rows['R1']['artifact']=evidence
        self.finish(objective_completeness=rows)
        self.state.apply('deliver')
        (self.root / evidence).write_text('Changed finisher evidence')
        with self.assertRaises(m.Invalid):
            self.state.apply('check')
        self.assertFalse(self.state.apply('status')['completion']['fresh'])
        with self.assertRaises(m.Invalid):
            self.state.apply('deliver')

    def test_sourcing_plan_review_before_search(self):
        self.approve('question')
        self.state.apply('objective', {'artifact': self.file('Autonomous brief'), 'pillars': ['p1'],
                                      'requirements': {'R1': 'Answer decision'}, 'mode': 'autonomous'})
        self.approve('objective')
        self.register('sourcing_plan')
        with self.assertRaises(m.Invalid):
            self.register('lane:literature')
        self.review('sourcing_plan', 'source_reviewer', [{'id': 'F1', 'severity': 'material',
            'description': 'Search route lacks an objective and concrete next action', 'evidence': 'Plan section 1'}])
        with self.assertRaises(m.Invalid):
            self.register('lane:literature')
        self.register('sourcing_plan')
        self.review('sourcing_plan', 'source_reviewer')
        self.register('lane:literature')
        self.review('sourcing_plan', 'source_reviewer', score=0)
        self.assertNotIn('lane:literature', self.state.s['nodes'])
        with self.assertRaises(m.Invalid):
            self.register('lane:literature')

    def test_path_safety_and_transactional_failure(self):
        self.objective()
        revision = self.state.s['revision']
        for path in ('../outside.md', 'research-state.json'):
            with self.assertRaises(m.Invalid):
                self.state.apply('register', {'kind': 'sourcing_plan', 'artifact': path})
        with tempfile.NamedTemporaryFile() as external:
            (self.root / 'escape.md').symlink_to(external.name)
            with self.assertRaises(m.Invalid):
                self.state.apply('register', {'kind': 'sourcing_plan', 'artifact': 'escape.md'})
        self.assertEqual(self.state.s['revision'], revision)
        self.assertNotIn('sourcing_plan', self.state.s['nodes'])

    def test_review_mutation_invalidates_approval_and_descendants(self):
        self.plan()
        self.review('sources', 'source_reviewer', score=0)
        with self.assertRaises(m.Invalid):
            self.register('plan')
        self.assertNotIn('plan', self.state.s['nodes'])

if __name__ == '__main__':
    unittest.main()
