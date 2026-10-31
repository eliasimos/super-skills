# Super Skills

**Deep research on steroids.**

A collection of four agent skills for investigating consequential questions and turning the findings into readable reports and presentations. Two skills conduct research; two turn existing material into Brayl-branded PDFs and decks.

A skill is a folder of instructions, reference material and, where useful, executable helpers and design assets. These are workflows for a capable AI agent with tools—not a standalone application, model or hosted research service.

## What's included

| Skill | What it does | When to use it |
| --- | --- | --- |
| [Super 5-1](superesearch5-1/SKILL.md) | Coordinates specialist sourcing, three independent analyses, independent judges and a final completion review. | Research that calls for competing approaches and explicit review gates. |
| [Super 5-9d](superesearch5-9d/SKILL.md) | One researcher maps the required answers, acquires primary-source figures, analyzes them and checks a substantive formal report. | Research you want a single agent to carry through, with its own checks disclosed. |
| [Super PDF](super-pdf/SKILL.md) | Converts or restyles reports as Brayl portrait PDFs, preserving content, citations and emphasis. | A finished report needs a polished, consistent PDF. |
| [Super Deck](super-deck/SKILL.md) | Builds or restyles landscape research decks with bundled typography, layouts and visual references. | Existing findings need a presentation or landscape PDF deck. |

## How the research works

Both research workflows begin by refining the question and obtaining approval of the objective. That approved brief defines the scope, expected outputs and completion standard. Research then proceeds autonomously within those limits; interactive checkpoints are available when requested.

**Super 5-1** uses five sourcing specialties: literature, free datasets, gated datasets, alternative sources, and code/tools/technical documentation. It reviews the sourcing and execution plans, runs three independent analyses, judges the results and synthesizes the strongest supported findings. A separate reader and work finisher check the final output. Its Python state helper records artifacts, approvals and review gates. It requires actual subagents; writing several role labels into one conversation is not equivalent.

**Super 5-9d** keeps the entire investigation with one researcher. It distinguishes the results the question requires from supporting detail, extracts complete source figures, commits to estimates with ranges and fallbacks where needed, and writes one substantive report with an optional short abstract. It checks coverage, repeated meaning and consequential claims against the original evidence. It does not claim independent review.

Both preserve the distinction between observed evidence, analysis, assumptions and unknowns. Review gates and state records support the process; they do not prove that a conclusion is correct. Paid access and outreach require their own authorization.

## From research to publication

Use either research skill to produce the substantive report. Then use **Super PDF** or **Super Deck** to format that material.

- **Super PDF:** white A4 pages, Brayl wordmark on every page, Instrument Serif headings, Inter body text, selective semibold emphasis, violet accents and a full sources appendix for sourced reports. Includes a Markdown-to-PDF renderer.
- **Super Deck:** landscape editorial layouts with white, midnight and pale-violet modes, original-color Brayl marks, readable charts and tables, and bundled reference slides. Content and legibility determine slide count unless you specify a limit.

The formatting skills preserve the source's meaning, figures, caveats and evidence date. They do not conduct fresh research or validate the underlying findings. Request the formats you need; an HTML/PDF deck is not an editable PowerPoint.

## Getting started

1. Clone or download this repository.
2. Copy each complete skill folder you want into your agent's supported skill directory. Keep its references, assets, scripts and metadata together.
3. Invoke the skill by its folder/frontmatter name and provide the question or source report.

Example requests for an agent that supports `$skill-name` invocation:

```text
$superesearch5-1 Investigate whether [opportunity] is attractive for [decision-maker].
Help me refine the question and objective before starting research.
```

```text
$superesearch5-9d Assess [question] as of [date].
Use [geography, constraints and evidence requirements] and produce a sourced report.
```

```text
$super-pdf Turn this report into a Brayl PDF, preserving its wording and sources.
```

```text
$super-deck Turn this report into a landscape PDF deck.
Explain the findings clearly and include the sources appendix.
```

For an existing research project, supply its current brief, evidence and latest answer or review. The skills should resume the selected action without repeating completed intake.

## Runtime requirements

| Skill | Required environment |
| --- | --- |
| Super 5-1 | Agent with search, file and code tools plus subagent support; Python 3.9+ for the standard-library state helper. |
| Super 5-9d | Agent with search, retrieval, file and code tools; no delegated research agents. |
| Super PDF | Python with `reportlab` and `pypdf`; Poppler or an equivalent page renderer for visual inspection. |
| Super Deck | Host browser/PDF rendering tools, or native presentation authoring tools for editable slides. |

Each folder bundles its required method, references, helper code and assets. Host tools, user evidence and project-specific recording rules remain environment inputs. Each bundle declares `self_contained: true` in `agents/packaging.json`.

## Snapshot and validation

Packaged on **31 October 2026** from the latest local versions available at that time. Super Deck includes the 26 October visual-mode and headline updates.

For portability, Super 5-1's research-method dependency is included locally and its machine-specific CLI paths are parameterized. Super PDF includes local validation guidance in place of an external skill dependency. The original helper code and design assets are preserved. `bundle-manifest.json` records source-file and packaged-file SHA-256 hashes.

Checks performed for this snapshot:

- Each skill validated in an isolated copy with sibling skills absent.
- Skill frontmatter, internal Markdown links and CSS asset paths checked.
- All **27 existing Super 5-1 state-helper tests passed**.
- Super PDF rendered a sample report successfully, with text extraction checked. This smoke test is not a visual review of every possible output.

The repository contains the four skills and their supporting material. The deck PDFs are intentional design references, not research templates or current evidence. The original research corpus, experiment results and workspace history are not included.

## Asset rights

Bundled fonts retain their SIL Open Font License notices in each `assets/fonts` directory. Brayl marks are supplied branding assets; publication here does not grant unrelated branding or trademark rights. The project uses the [MIT License](LICENSE) selected for this repository; bundled third-party assets retain their own notices.
