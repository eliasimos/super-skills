# State CLI: exact contract

The coordinator alone writes this v5 ledger. Use a new run folder; earlier ledgers are not migrated automatically. Agents return artifacts and review payloads; this helper does not run agents, search, authenticate humans, judge semantic truth, or infer approval. Use Python 3.9+; no packages or network needed.

Resolve the helper from the directory containing the loaded `SKILL.md`. Set `SKILL_DIR` to the absolute directory containing this skill:

```sh
python3 "${SKILL_DIR}/scripts/research_state.py" RUN COMMAND [PAYLOAD.json]
python3 -m unittest discover -s "${SKILL_DIR}/tests" -v
```

Use absolute paths for RUN and PAYLOAD when running from another directory. If the skill moves, derive the helper path from its new directory. A failed lookup of `scripts/research_state.py` in the repository or exploration root does not mean the helper is missing. Check the resolved file and actual execution error before reporting a dependency failure; fix it before advancing gated work. Do not substitute a handwritten ledger.

For a run already using a manual ledger, preserve it and its artifacts. Reconstruct helper state in stage order using the actual saved approvals and review provenance. Reuse approvals only where they apply to the registered version; never fabricate missing hashes, approval messages or passing reviews. Obtain fresh reviews where the saved review cannot be bound to current artifacts. Run `check` before continuing; retain completed research rather than rerunning it merely to rebuild state.

`RUN` must already exist. Payload is a JSON object stored in a file. Commands return JSON; validation errors exit 2 without changing ledger state. `research-state.json` contains active nodes, approval/review records, and full historical states. `.state-artifacts/<sha256>` retains registered artifact bytes across revisions. One coordinator, one writer: simultaneous ledger writes are unsupported.

Artifact paths must identify existing regular files inside RUN. Absolute in-run paths work; escapes, external symlink targets, ledger files and archive files are refused. Every artifact registration accepts optional `files: ["evidence.csv", ...]`. **List every local content-bearing dependency** that the artifact relies on; the helper cannot infer prose links, remote content, or omitted files. These files are hashed and archived too. Use versioned filenames to preserve readable originals. Archive copies preserve prior bytes even when a working file is overwritten.

## Ordered commands

1. `init`: `{"question":"question.md"}`. Registers only the refined question.
2. `approve`: `{"kind":"question","target_hash":"from displayed question status","context_hash":"from displayed question status","message":"verbatim user confirmation","reference":"conversation/message locator"}`. Explicit human confirmation is required before objective registration.
3. `objective`: `{"artifact":"brief.md","pillars":["p1","p2"],"requirements":{"R1":"First approved requirement","R2":"Second approved requirement"}}`. Add `"mode":"autonomous"` (default) or `"mode":"interactive"`. The displayed brief contains the objective, acceptance criteria, pillars and mode, including authorization to proceed after approval. IDs are unique, nonempty strings.
4. `approve`, kind `objective`. Same hash/message/reference fields, for the displayed brief and mode. No work proceeds without this human approval.
5. `register`: `{"kind":"sourcing_plan","artifact":"sourcing-plan.md"}`. **One coordinator plan**, no sourcing-plan competition. Obtain a passing `source_reviewer` review before starting any search lane. The same independent reviewer later reviews the actual source list; no extra table or agent role is required.
6. In interactive mode only, `approve`, kind `sourcing_plan`. Autonomous mode proceeds under objective authorization.
7. Register five searcher artifacts, one per exact lane: `lane:literature`, `lane:free_data`, `lane:gated_data`, `lane:alternative`, `lane:tools`. Example: `{"kind":"lane:tools","artifact":"search-tools.md"}`.
8. `register`: `{"kind":"sources","artifact":"sources.md","files":["evidence.csv"]}`. Requires all five lanes. This is the combined source set, including access/provenance/caveats and dispositions.
9. `review` sources with judge `source_reviewer`, independent of the searchers/coordinator. See review schema below. The coordinator must keep the source set internal until this review passes; the CLI gates planning but cannot control what someone displays in chat.
10. Share a source-list update. In interactive mode only, obtain and record `approve`, kind `sources`. Both modes require the current source review to pass before planning.
11. Register the coordinator execution plan: `{"kind":"plan","artifact":"execution-plan.md","tasks":{"T1":{"description":"Use S001 to answer R1","requirements":["R1"],"sources":["S001"]},"T2":{"description":"Resolve R2","requirements":["R2"],"sources":[]}}}`. Requires qualifying reviewed sources, plus source-list approval in interactive mode. Plan content follows the execution-planning instruction in SKILL.md. No worker proposals. One independent `plan_reviewer` reviews this plan using the review schema; it must qualify before execution.
12. Share the reviewed plan. In interactive mode only, obtain and record `approve`, kind `plan`. Autonomous mode proceeds after the internal review passes.
13. Register `execution:worker1`, `execution:worker2`, `execution:worker3`; all run the reviewed plan. All three judges review each execution, nine current reviews total, including planned source use.
14. Register the actual composed answer using the synthesis schema below.
15. Run and register the independent `reader-test` below; repair partial/missing answers before proceeding. All three judges review **that synthesis**, including every imported contribution. Execution reviews do not count as final reviews.
16. `finish` with the independent verifier payload below, then `deliver`, no payload. Delivery requires both qualifying final reviews and a current finisher pass. Otherwise use `stop` and report the blocker.
17. Before the turn-ending final response, complete the extension-planner assignment in `SKILL.md` and collect its `extensions.md`. This is an actual subagent action outside the CLI; `deliver` neither launches it nor verifies that it ran. Present the accepted answer followed by the planner's offer, or disclose a concrete delegation blocker. No additional user approval is needed to prepare proposals; launching proposed research still needs authorization.

Never fabricate human approvals for autonomous internal gates: the helper rejects such records. Internal stage authorization follows the approved brief; source/plan reviews remain distinct from human approvals. Approval kinds in interactive mode are exactly `question`, `objective`, `sourcing_plan`, `sources`, `plan`. Every approval also requires exact `target_hash` and `context_hash` from the displayed version’s `status`, plus nonempty verbatim human `message` and `reference`. These fields are attestations, not identity checks or proof that the text grants permission. The coordinator must obtain real, applicable approval. Repeating an identical current approval is idempotent; changing an approval invalidates dependents.

## Current-context reviews and qualification

Use `status` immediately before reviewing to obtain the target's `target_hash` and `context_hash`. A review payload is:

```json
{
  "target": "execution:worker1",
  "judge": "correctness",
  "reviewer": "independent correctness reviewer",
  "target_hash": "copy exact target_hash from status",
  "context_hash": "copy exact context_hash from status",
  "scores": {
    "p1": {"score": 2, "reason": "Why this score follows", "evidence": "source/result and exact section or row"},
    "p2": {"score": 1, "reason": "Adequate with this limitation", "evidence": "source/result and exact location"}
  },
  "findings": []
}
```

Every current pillar appears exactly once, with integer `0`, `1` or `2`, a reason and evidence location. Interpret these as fail, adequate and strong under the stage rubric. There is no accumulating competition score, tournament winner, survival rule or numeric claim of truth. `status` exposes review payloads, current qualification and missing-review blockers, enabling workers to read the full review table.

Material findings use `{"id":"F1","severity":"material","description":"Problem","evidence":"Location"}`; severity can also be `critical`. **Every finding blocks qualification**, even with all scores 2. No coordinator override can dismiss findings through this helper. Repair the artifact and re-review, or have the responsible judge issue an evidence-backed corrected review. Preserve rationale in its reason/evidence. History retains the old review. There is no fixed number of repairs.

A target qualifies only with every required current review, every pillar scoring at least 1 and no findings. Sourcing plans, source sets and addenda require `source_reviewer`; the execution plan requires `plan_reviewer`; executions and final synthesis require all three specialist judges. Reviewer identity strings record the coordinator's attestation of independence; staffing and genuine independent judgment remain coordinator responsibilities.

Reviews bind artifact bytes, registration generation, supporting-file hashes, metadata, pillar IDs and recursively bound upstream dependencies. Even identical-content resubmission gets a new generation; copying an old review cannot satisfy the new context. Editing a registered file in place makes it stale: `check` and dependent transitions refuse it until appropriately re-registered and reviewed.

## Final synthesis and imported components

```json
{
  "kind": "synthesis",
  "artifact": "final-answer.md",
  "reason": "How these verified findings combine to answer the objective",
  "contributions": [
    {"worker":"worker1", "location":"execution section 4, rows 8–10", "use":"Cross-check used in final section 2", "verification":"component-verification.md"}
  ],
  "files": ["final-calculations.csv"]
}
```

All three executions must have nine current reviews. No overall winner or qualifying backbone is required. List every included contribution (at least one), with its exact location/use and a local verification artifact; that artifact is hashed and archived. Components from a candidate with other defects may be used only after checking the component and resolving any findings relevant to its use. Final judges verify every contribution and the whole answer against the brief. Do not require all workers to contribute or combine incompatible results. Source-use compliance remains a substantive judge check; unexplained omissions are blocking findings. Legacy `backbone` submissions are rejected; re-register an existing synthesis with complete contribution provenance and renew final reviews.

Each final review additionally includes `contribution_checks`, indexed by the contributions' zero-based position:

```json
"contribution_checks": {
  "0": {"passed": true, "reason": "Checked this component independently", "evidence": "verification section 3 and final section 2"}
}
```

Every final judge must check every included component. A false check blocks delivery regardless of pillar scores. This permits sound, independently checked components without treating a weak candidate's full answer as qualified.

## Revision, addenda, budget and stopping

- `permit-brief`: `{"message":"verbatim explicit permission to revise this brief draft","reference":"user-message locator","artifact":"brief-v2.md","pillars":["p1","p2"],"requirements":{"R1":"First approved requirement","R2":"Second approved requirement"}}`. Also include `target_hash` and `context_hash` of the displayed **current brief**, obtained from `status`. Record this **before** registering a changed authoritative brief. Permission binds both the current brief and the proposed artifact, pillar IDs, mode and optional `files`; changed draft bytes or dependencies cannot reuse permission. It is consumed once. Draft proposed changes elsewhere first. `mode` defaults to the current mode on revision; changing it requires the same explicit brief permission and approval.
- `revise-brief`: `{"artifact":"brief-v2.md","pillars":["p1","p2"],"requirements":{"R1":"First approved requirement","R2":"Second approved requirement"}}`. Requires recorded permission. Preserves the confirmed question, invalidates downstream active records and removes objective approval. If the revision permission explicitly approved the displayed new objective, record that same message as its approval without asking twice; otherwise obtain objective approval. `objective` cannot overwrite an existing brief.
- `revise-question`: `{"question":"question-v2.md"}`. Clears downstream active work and approvals; the new question must be explicitly confirmed before another objective is registered.
- Re-registering any ordinary node replaces its active version and invalidates its dependent nodes, reviews and approvals, retaining history/bytes. Unaffected upstream and sibling nodes remain. This structural invalidation is conservative: it does not require repeating unchanged research. Reuse retained artifacts after checking applicability. In autonomous mode, in-scope stage revisions need current internal reviews, not invented human reapprovals. In interactive mode, re-register an unchanged stage under prior user authorization only if that authorization still covers the current work; record the compatibility reason alongside its original message/reference. Never reuse an old approval for a materially changed stage. Review replacement clears that node's approval/accepted state and invalidates dependents. It does not silently preserve approval of a changed review judgment.
- Additional evidence within a reviewed execution method: register `{"kind":"addendum:unique-id","artifact":"extra-sources.md","reason":"Why this evidence stays within the reviewed method and approved brief","files":["extra-data.csv"]}`. This requires a qualifying plan and any mode-required human approval. Obtain an independent `source_reviewer` review, then `accept-addendum`: `{"target":"addendum:unique-id"}`. This coordinator acceptance does **not** bypass source or plan gates. It preserves existing question/objective and any interactive stage approvals, but invalidates executions and synthesis so all workers recheck under the additional evidence and all nine execution plus three final reviews are renewed. New executions depend on every accepted addendum. Re-registering/re-reviewing an accepted addendum invalidates the dependent work. Brief changes require explicit user permission. Method changes within the brief require plan re-registration and review (plus approval in interactive mode), not an evidence-only addendum.
- `budget`: `{"limit":"approved overall budget, units and approval locator","used":"usage to date","remaining":"remaining budget","decision":"continue targeted repair or stop, with reason"}`. Coordinator record only: no metering or fixed repair cap. Update at meaningful checkpoints; do not misrepresent estimated usage as measured.
- `stop`: `{"artifact":"blocker.md","reason":"What prevented a qualified final answer"}`. Records a blocker and clears delivery. Explain missing evidence, unresolved findings, exhausted budget or required user action in the artifact. No unchecked answer substitutes for a blocker.
- `status`: no payload; reports nodes, hashes, freshness, full reviews, qualification, budget, blocker and recorded delivery. A recorded delivery is historical authorization at its last successful gate; inspect freshness or run `check` before relying on it after any external file edit.
- `check`: no payload; verifies all active artifact/dependency bytes and returns status. Incomplete research is allowed; this validates freshness, not completion. `deliver` performs the final completion gate.

Freshness checks memoize repeated dependency traversal within a command only; the cache is discarded before every command and on mutations, so later file edits are not hidden by persistent caching.

Run `check` after recording each stage and before delivery. The helper preserves internal history; the repository lifecycle, source register, intervention ledger and round-yield updates still follow their own protocols.

## Structured completeness records

Register `requirements` as every approved requirement ID → exact requirement text on `objective` and brief-revision permission/registration. This inventory is separate from `pillars` and binds the approval. Register all execution tasks and source-use commitments in plan `tasks`, each with `description`, applicable `requirements` IDs, and `sources` IDs (empty only for tasks without source work). Judges/finisher compare these inventories with the actual brief and plan to detect omitted commitments; code cannot extract their meaning. Existing runs missing inventories must re-register affected artifacts under applicable authorization; preserve history and renew affected reviews rather than silently inventing completion.

Every execution review includes `execution_completeness`. Each final synthesis judge includes both `execution_completeness` and `objective_completeness`. Examples (repeat for **every** expected ID):

```json
{
  "objective_completeness": {
    "R1": {"score": 2, "artifact": "final-answer.md", "location": "section 2", "reason": "Evidence answers R1", "findings": []}
  },
  "execution_completeness": {
    "T1": {"status": "completed", "artifact": "results.csv", "location": "rows 2–12", "reason": "Planned calculation reproduced", "findings": []}
  }
}
```

`artifact` must be an existing local in-run evidence file; referenced bytes are hashed, checked and archived with the review. `location` identifies the relevant section/rows. `findings` is a list of unresolved material-gap descriptions (empty when none). Execution statuses are `completed`, `justified_exception`, `unfinished`. An exception additionally requires nonempty `alternatives` and `consequence`. Rows with a zero score, unfinished status or findings do not pass. These tables complement existing pillar scores, contribution checks and material findings; none overrides another. Use the existing artifact, location and reason fields to trace acquisition through analysis to findings; use exception fields for attempt evidence, alternatives and consequences under SKILL.md. Register the acquired files as dependencies. These are substantive review requirements, not automatically verified by populated fields; no additional table or schema is required.

Each `plan_reviewer` review also requires `plan_objective`, with every approved requirement exactly once:

```json
{"plan_objective":{"R1":{"tasks":["T1"],"inputs":"S001 auction records","output":"Cost estimate or explicit conditional bound","score":2,"artifact":"execution-plan.md","location":"task T1","reason":"Method can resolve R1","findings":[]}}}
```

Mapped task IDs must exist. Missing rows, zero scores or material gaps block plan qualification and execution.

After final reviews pass, `status` supplies `completion_context`. A separate finisher submits:

```json
{
  "reviewer": "independent work-finisher agent identity",
  "synthesis_hash": "copy completion_context from current status",
  "passed": true,
  "reason": "Independently verified both tables against brief, plan and artifacts",
  "findings": [],
  "objective_completeness": {"R1":{"score":2,"artifact":"final-answer.md","location":"section 2","reason":"Verified answer","findings":[]}},
  "execution_completeness": {"T1":{"status":"completed","artifact":"results.csv","location":"rows 2–12","reason":"Verified work","findings":[]}}
}
```

Use command `finish`. Include all IDs, not only the illustrative rows. The finisher must be separate from authors and judges; the helper rejects reused reviewer identities but cannot authenticate agent independence. A negative verdict or nonpassing row blocks delivery. Repair and renew affected reviews, then finish again. Internal artifact/review mutations invalidate the finisher conservatively; edited evidence also prevents delivery. A recorded prior delivery is historical, not a current completeness certificate.

`render` returns `{"markdown":"..."}` with all recorded completeness tables and finisher rows. Save/display this derived text in the existing review package; JSON remains authoritative. `status` includes the finisher verdict. This adds no user approval stage or mandatory standalone document.

## Reader-test payload

Run `reader-test` after synthesis registration and before final judging:

```json
{"reviewer":"fresh-reader-agent-id","target_hash":"current synthesis target_hash","answers":{"R1":{"status":"answered","answer":"The actual answer recovered from the report","scope":"Its population, period and other relevant limits","quote":"Exact excerpt from the synthesis file","gap":""}}}
```

Include every approved requirement ID. Status is `answered`, `partial`, or `missing`; partial/missing needs a specific nonempty `gap`. Answered/partial requires an exact nonempty excerpt from the synthesis file; missing may use an empty quote and describe the absent answer. A gap cannot coexist with answered. The helper validates structure and excerpt presence, not meaning. The reader must inspect figures where relevant, with equivalent results in the synthesis text. Registering a replacement test clears final reviews, finisher and delivery. Synthesis/dependency changes invalidate the test through existing freshness and registration gates. A reader cannot also be a final judge or finisher.

Older runs remain on disk unchanged. Previously accepted runs without a reader test cannot obtain a new passing qualification/delivery under this helper until tested and re-reviewed. Do not rewrite historical approvals or claim they originally passed this test.
