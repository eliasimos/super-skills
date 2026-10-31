# Capture an exploration's demonstrated method

Create or update `explorations/<id>/.agents/skills/<domain-task>/SKILL.md` after a useful worked example. This repository's user has requested capture during ongoing research. Preserve existing local skills; extend the relevant one instead of creating competing instructions.

## What to extract

- The task and decision stage the method supports, its required inputs and success criterion.
- Useful source routes and holder types, fields and joins, domain checks, inference limits and when to change routes.
- The repeated procedure that produced the result, including failed checks that exposed meaningful traps.
- A compact output/evidence packet and the question or action that follows it.
- Links to the worked example, retained evidence and consequential user steering, with date and validation status.

Separate reusable steps from case inputs. A Greek parcel skill can encode electrical units and industrial-park screening; an individual plot's coordinates, cost assumptions and actual availability stay in its records. A stock-selection skill can encode demonstrated screening/enrichment steps; one selected stock does not establish investment performance. Domain standards come from the brief and evidence, not from the general skill.

Mark the first method **provisional**, state which stage succeeded and name unverified outcomes. Preserve uncertainties, counterexamples and excluded uses. Do not turn a single favorable observation into a universal threshold or a calibrated success rate.

## Keep it usable and scoped

Write concise YAML `name` and `description` plus actionable instructions. The description and body must identify the exploration/domain and when the skill applies. Put conditional details in references only when they help; avoid copying the source catalogue or research history into the skill.

Add a conditional pointer in the exploration entry or applicable `AGENTS.md` so later agents load it for this task. Keep it local to that exploration. General promotion requires evidence that a method transfers to other briefs; do not install project rules globally.

Reuse existing scripts. Add a small helper only when a demonstrated repeated extraction, transformation or check benefits from deterministic execution. Source ranking, novelty judgments and unsupported inference should not become automated facts.

## Validate and improve

Check skill structure and link resolution. On the next relevant case within the authorized research, use the skill and record missing steps, corrections, failure modes and the resulting decision. Preserve the first example's validation limits. Update the method from observed results and substantive feedback.

This replay checks usability; it is not a controlled measurement of causal benefit. To claim fewer interventions or greater accuracy, define a comparable evaluation and measure those outcomes. Record method changes in the existing intervention/process records without counting them as new source evidence.
