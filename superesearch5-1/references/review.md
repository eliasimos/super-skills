# Review, synthesis and effort

## Evidence-backed judgment

For each approved pillar, record 0 (materially fails), 1 (meets the requirement with a nonmaterial weakness), or 2 (well supported for the requested stage), with evidence and a brief reason. List material findings separately with the affected requirement, artifact location and needed correction. Latest reviews replace scores, never accumulate. Scores are diagnostic, not empirical confidence or reward tokens. No points for length, source counts or repeating requirements.

Use the phase's actual standard: objective-linked, specific and actionable routes for sourcing planning; source coverage for discovery; brief fidelity/source use/feasibility for execution planning, and supported results for execution. Review proportionate effort alongside usefulness. Missing identification may support a conditional answer if the brief allows it; missing feasible required work cannot be replaced by caveats. A zero or unresolved material finding blocks qualification regardless of total score. For execution and synthesis, trace planned source commitments to inspected evidence and actual analytical use. Accept a justified rejection or access blocker only with its consequence and feasible alternatives addressed; unexplained omissions or unjustified replacement with assumptions require repair. Record this in existing reviews. Merely citing a source does not demonstrate its planned use.

Check whether useful available data was left unused, including gaps the execution plan overlooked. Apply SKILL.md’s acquisition rule: return acquisition omissions for targeted repair unless the evidence supports an exception. In existing completeness rows, trace acquired evidence → analysis → finding; inspect the underlying artifacts, not just source-use declarations. A wholly hypothetical model cannot pass merely because assumptions are disclosed and arithmetic works. Judges and the finisher must assess whether residual gaps still permit answering the original decision objective; fulfilling a weakened plan is insufficient.

Each judge assesses independently before seeing others' judgments. Different role prompts do not guarantee independent errors; record actual models and roles when available. Same-model workers are acceptable; do not claim a diverse-model jury unless one ran. Disputes return to evidence. The coordinator requests specialist reconsideration rather than editing scores or declaring a majority correct. A reviewer updates its own verdict after a supported resolution.

## From candidates to one answer

1. Review all three candidates and synthesize their strongest supported findings. Resolve material contradictions before settling the conclusion; scores inform review, not winner selection. If the combined answer cannot meet the brief, repair or report a blocker.
2. Identify each useful contribution, its originating artifact and supporting evidence. An otherwise weak candidate can contribute a sound component, but that component must be separately checked before incorporation.
3. Reconcile definitions, denominators, scenario assumptions, evidence periods and calculations. Do not average incompatible conclusions or splice figures from different scenarios into one case. Rerun derived results when integration changes their inputs. Keep distinct plausible alternatives labeled separately.
4. Preserve a compact contribution record beside the final answer. It is process evidence, not a compulsory section of the user-facing memo.
5. Have all three judges review the final artifact, its dependency manifest and decisive underlying evidence. Candidate defects relevant to included findings must be resolved in the synthesis; discarding the rest of a candidate is not a resolution. Any subsequent substantive change invalidates affected reviews. Release only after all required final reviews pass and artifacts are unchanged.

Do not require a contribution from every worker. The synthesis may draw from one candidate if the others add no supported value. Record every included contribution, even when using one candidate throughout. Never invent consensus; retain material uncertainty and dissent in the answer where it affects the decision.

## Targeted repairs

Each repair finding names the defect, affected requirement and artifact location, and what correction would resolve it. Repair that defect and dependent results; preserve unaffected findings, evidence and text. Explain what changed and why in the existing resubmission record. Broader rewrites require a demonstrated dependency or inconsistency, not merely a preference to start over.

Preserve the previous version. The coordinator compares the revision against it; judges verify that the defect is fixed and previously satisfied requirements remain satisfied. Recheck affected claims and downstream calculations. Structural review invalidation may require a fresh verdict, not a full research rerun.

Honor any applicable user-set or approved phase ceiling, including coordination and reviews; do not invent a discovery budget or consume a ceiling as a target. Stop discovery when qualified coverage is sufficient for execution planning. If a ceiling is reached first, report the remaining gaps without claiming completeness. Before extending effort, identify the unresolved requirement and why the next action could change the result. When progress stalls, switch approach within scope/budget or report the blocker. Budget exhaustion never converts an unqualified answer into a passing one.

## Artifacts and source additions

Use a run folder under `03-execution/superesearch5-1/<run-id>/` in this repository, or an equivalent local folder elsewhere. Preserve versioned brief/source/plan snapshots with canonical paths; these are reproducibility copies, not competing editable briefs. Keep worker and judge artifacts separate. Record dependencies (evidence, code, data and result files) with their hashes when submitting; checking answer prose alone is insufficient.

For new evidence within the reviewed method and approved brief, retain a versioned addendum. The independent source reviewer checks its qualification and provenance; the coordinator records its impact and shares accepted additions with all workers. A change to the objective, essential assumptions, exclusions or required outputs needs explicit user approval. Method repairs within those boundaries need renewed internal plan review; interactive mode also requires plan approval. Recheck dependent claims without repeating unchanged research. The state helper describes how to bind addenda and replacement artifacts to the affected reviews.

Source-list checks review what was found against what was planned. Do not approve based on named categories alone: a generic API page is not automatically a usable historical-data route, and a paper without inspected methods is not a calibrated model input. Carry valid blocked routes and uncertainty honestly; do not require every lane to yield the same number of sources.

## Reader test before final judging

Use a fresh reader agent with no inherited conversation. Supply only the approved brief, the actual reader-facing synthesis and this test; withhold plans, effort records, author self-assessments and previous verdicts. This is a task-performance test, not another request to award a score.

For each approved requirement, have the reader extract the answer they can actually use, its actual scope (population, period, denominator or other relevant boundary), and an exact supporting excerpt. Classify it as `answered`, `partial` or `missing`. A conditional estimate can satisfy the brief; a catalog of components that requires the reader to perform new analysis cannot substitute for a requested integrated result. Missing evidence and unreadable/missing presentation are different defects; name which repair is needed. Do not require charts or numerical outputs when the brief does not ask for them. For visual outputs, inspect the rendered exhibit too; retain an equivalent textual result in the synthesis so excerpts are machine-checkable.

Record the result using `reader-test` before final judges see it. The helper blocks final judging and release on any partial/missing requirement, binds the test to the synthesis, and invalidates all final verdicts when the test changes. Repair the named gap and repeat with a fresh reader; do not have the coordinator rewrite a failed extraction into a pass. If the reader misunderstood, improve the deliverable or request evidence-backed reconsideration by a fresh reader. When progress stalls, use the existing blocker path rather than lowering the standard.

After a passing reader test, judges verify that recovered answers match the approved scope and are supported by the data; successful extraction does not establish truth. The finisher remains separate from the reader and judges. Exact excerpt checks enforce traceability, not semantic correctness or actual agent independence.

## Completeness and final release

Judges and the work finisher apply SKILL.md's reader-facing memo standard to the actual final artifact. First read it without relying on the brief or conversation: can a new reader identify the question, understand the summary, follow defined terms and assumptions, see what evidence and work produced the findings, and understand the recommendation's limits? Then check that explanation against the supporting records. Record specific missing premises, unexplained terms or dependencies on prior artifacts in the existing review; return material comprehension gaps for targeted repair before delivery. A correct conclusion alone does not satisfy this check, and a link or glossary does not replace explanation where it is needed.

Also verify that accessibility edits preserve the supported analytical specificity required by SKILL.md. Compare the synthesis with its included candidate findings and supporting analysis; return material losses of precision, evidence, method, scenario distinctions or caveats for repair. Omitting unsupported or irrelevant material remains appropriate.

Use the existing review JSON as the authoritative record; `render` generates readable tables. Do not maintain a second manual table. Pillar scores remain, but do not substitute for individual approved requirement IDs or plan commitment IDs.

- **Execution → plan:** workers propose one row per planned task/source-use commitment; judges verify artifacts and mark completed, justified_exception or unfinished. Exceptions state evidence, alternatives considered and the consequence.
- **Final answer → objective:** each final judge independently scores every approved requirement 0/1/2 with an artifact/location, reason and unresolved findings. A justified execution exception does not automatically satisfy the objective.
- **Plan → objective:** the independent plan reviewer maps every requirement to planned task IDs, sources/inputs and expected output, scoring 0/1/2 with evidence and gaps before execution.

For pilots and inconclusive comparisons, judges and the finisher inspect the coordinator's sufficiency decision against the original objective. Require concrete dispositions for promising feasible extensions of coverage or method. If materially useful, authorized work remains, return a targeted expansion or method repair even when all sampled rows and planned tasks are complete. Difficulty with one sample does not establish that the broader question is unanswerable; a conditional fallback needs an evidence-backed stopping rationale. Do not demand exhaustive searching or a minimum row count. Work necessary to meet the existing brief cannot be deferred to the offer of optional extensions in the final response.

Every required row must be present. A zero, unfinished task or unresolved material finding blocks qualification. The separate work finisher verifies both completion tables and their underlying evidence after final judging. It cannot dismiss judge findings; return repairs to the coordinator and obtain affected re-reviews. Delivery requires the current finisher pass. Changed artifacts, dependencies or judge verdicts require renewed verification. No new human approval gate is added.
