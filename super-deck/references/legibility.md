# Legibility standard for research decks

Use for report-to-deck composition. For faithful restyling, preserve the requested wording and scope; split slides or adjust layout rather than silently editing content.

## Approved reference

`../assets/legibility-reference.pdf` contains seven unchanged slides from the Greek insurance distribution deck. On 16 October 2026 the user described the deck as “great and high quality” and asked to make this legibility reproducible through the skill. Original slide numbers: 1, 2, 4, 13, 20, 30 and 50. They demonstrate cover hierarchy, narrative columns, a labeled chart, target economics, an earnings bridge, a scenario table and readable references.

Use their hierarchy, spacing and density as a visual benchmark. Do not reuse insurance claims, assumptions, source IDs or dates in another deck. Approval concerns presentation legibility; it does not set a universal slide count or independently validate financial assumptions. The reference’s table-heavy mix is not a target: chart opportunities should be assessed independently for each new deck. For the current modes, original-color logo and inline title emphasis, use `../assets/composition-reference.pdf` and the [design rules](design.md#visual-modes-and-headline-emphasis).

## Compose for an unfamiliar reader

- Use a supported takeaway as the title when appropriate. A short subtitle identifies scope, unit, period or the question being answered. Avoid titles that claim more than the displayed values show.
- Color a meaningful title phrase violet within the same text flow. Natural line wrapping is fine; emphasis alone never requires a new line or a smaller title.
- Explain in dependency order: opportunity and terms, evidence, economics or mechanisms, scenarios, implications and decisions. Adapt to the subject rather than forcing a fixed business-plan outline.
- Separate facts, assumptions and calculations visibly. Define unfamiliar acronyms and denominators before relying on them. Label changes in scenario, timing, population or measurement basis at the point of comparison.
- Choose the form by the reader’s task using the guidance below. Charts can communicate precise comparisons through direct value labels; precision alone is not a reason to choose a table. Use editorial columns for parallel qualitative ideas and a sequence for a process.
- Move exhaustive detail to the appendix while preserving the qualification needed to interpret a main-slide conclusion. Never hide a material caveat in tiny source text.

## Choose the visual by the reader’s task

During storyboarding, identify the relationship the reader should understand. A table in the source report is data, not a layout instruction. When a chart would make that relationship easier to see, use it on the main slide and retain exact supporting values in labels, notes or an appendix table as needed. Avoid repeating the entire table beside the chart unless the two serve distinct reader tasks.

| Reader task | Useful starting form |
|---|---|
| Compare size or rank categories | Bars or dots; horizontal bars for long category names |
| See change over time | Lines for a comparable time series; columns for a few discrete periods |
| Explain movement from a starting total to an ending total | Waterfall with signed contributions and labeled endpoints |
| Compare base, bull and downside across scales | Grouped bars, dot plots or small multiples with consistent axes |
| Understand parts of a whole | Stacked bars; 100% stacks only when shares are the question and denominators are clear |
| Explore two-input sensitivity | Heatmap with readable values and labeled inputs; show direction and the reference case |
| Compare ranges or uncertainty | Range / interval plot; distinguish scenario bounds from statistical confidence |
| Understand timing or sequence | Timeline or phased process diagram |
| Look up exact figures, compare mixed units or read contractual detail | Table, or separate charts for genuinely comparable measures |

Examples from the approved deck: EBITDA bridges are candidates for waterfalls; funding, earnings and carry by acquisition scale for grouped bars or small multiples; entry/exit sensitivities for heatmaps; acquisition cohorts and integration ramps for a timeline. These are reusable choices, not a requirement to reuse that deck’s subject matter or retrofit every existing table.

Use a short sentence or a prominent number for a single fact when a chart adds no information. Do not impose a minimum chart share, invent missing data, or sacrifice a useful table just for variety. Preserve explicit user instructions for faithful restyling.

## Practical density defaults

These are starting points at 1920 × 1080, not quotas or permission to discard content. User-specified density and slide limits take precedence.

| Component | Starting point |
|---|---|
| Narrative | One takeaway; 2–3 columns; one short paragraph per column, usually 40–65 words |
| Main table | Usually 3–6 data rows and 3–5 columns; split when cells become paragraphs |
| Appendix table | Up to about 9–10 short rows when fit-to-screen inspection confirms readability |
| Source appendix | Usually two references per slide, with full clickable URLs and useful limitations |
| Title / subtitle | 72px serif / 32px Inter; move content below wrapped headings |
| Body / table | 30–32px Inter / 28–29px Inter; 26px for compact appendix rows only |
| Chart labels | Usually 26–30px for categories and key values; 22–24px for secondary ticks; test at fit-to-screen size |
| Explanatory note | 24px Inter; reserve 18px for citations and footer metadata |
| Table spacing | About 14–18px vertical padding; quiet horizontal rules, no boxed grid |

Use `../assets/deck-report.css` after `deck-base.css` and `deck-layout.css`, then load `../assets/deck-modes.css` for the current palette and 8% side margins (153.6px at 1920). Preserve evidence/footer separation. Historical 120px-margin exports remain references for reading comfort, not the new default. Custom templates should reproduce the same measured geometry.

Repair crowding in this order: remove verbal repetition without losing meaning; improve column widths and wrapping; split independent messages or table groups; move supporting detail to the appendix. Reduce decorative spacing only where comfortable. Do not solve overflow with whole-slide scaling, clipped containers, tiny notes or shrinking fonts below the role’s readable size.

## Acceptance gate

1. **Geometry:** after fonts load, measure title/subtitle, content, notes, evidence and footer rectangles. Check horizontal and vertical bounds. Content and notes must end above the evidence strip; wrapped headings need a visible gap before content. Check scroll dimensions too; `overflow:hidden` is not evidence of a fit.
2. **Fit-to-screen:** render the exported PDF, not only HTML. Inspect every page at a landscape tablet-like size, approximately 1024 × 576 or an equivalent full-page view. Titles, takeaways, row labels, chart labels and key numbers should be readable without zooming. Split crowded series or categories into small multiples rather than shrinking labels. Inspect full-resolution images for ambiguous symbols, sources and dense rows. Contact sheets locate outliers but are insufficient for unreadable cells. Do not claim actual iPad testing without using an iPad.
3. **Visual comparison:** compare representative narrative, numeric and source slides with the approved reference. Look for hierarchy, comfortable line lengths, consistent margins, deliberate whitespace and minimal decoration. Match reading comfort rather than paragraph lengths mechanically.
   Check each mode used against the composition reference: white carries detail; dark concentrates a claim with readable body/citations; violet reaches every edge, including header and footer. Confirm the logo retains its original colors and opacity throughout. Check that headline accents are inline and any wraps are natural.
4. **Artifact integrity:** confirm page count, selectable text, rendered fonts and clickable source destinations. Check units, row alignment, formatting and scenario labels against the source/model. For charts, reconcile plotted values, labels and totals; verify axes, denominators and comparable series. Review numeric tables for missed visual explanations before finalizing. Use section bookmarks for long PDFs when supported.
5. **Repair:** re-export and inspect changed pages and any pages affected by shared styles. Keep a short private record of checks actually performed.
