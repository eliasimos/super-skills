---
name: super-deck
description: Create or restyle landscape research decks in Brayl’s editorial slide design, using as many slides as the content requires. Use for Brayl decks or when the user invokes super-deck; not for new research or portrait memos.
---

# Super Deck

Turn existing research into a Brayl landscape deck, or restyle an existing deck. Use the bundled editorial layouts, readable report typography and white / midnight / pale-violet modes. This skill does not conduct the underlying research. Preserve the user’s current content, output format, any explicitly requested slide count and approval scope.

## Start from the right material

- Use the authoritative editable content and existing sources. Treat supplied code as a design reference unless the user also requests its content. The original code contained illustrative research-agent examples; do not import mock scores, buyer claims, demo disclaimers or the example’s date into a real report.
- Keep canonical research and prior exports unchanged. Work in a separate export/build directory. No research lifecycle changes are needed for formatting alone.
- Read [design and rendering](references/design.md). Use the bundled CSS, mark and local fonts. If the user supplies newer design code, inspect it and prefer their current instructions.

## Build the complete deck

For report-to-deck work, apply the [legibility standard](references/legibility.md). It captures the user-approved Greek insurance deck’s narrative density, table treatment and fit-to-screen checks. Its content and slide count are not a template for future research.

Before layout, give each narrative slide one reader question and one supported takeaway. Explain unfamiliar terms and denominators before comparisons that depend on them. Put exhaustive scenarios, methods and source detail in a labeled appendix; keep material qualifications beside the claims they constrain. Split competing messages before reducing text size.

Choose the visual mode by its role in the argument: white explains and carries evidence; midnight concentrates a consequential claim; pale violet introduces a real chapter or opening. White remains dominant. Avoid consecutive dark slides by default; do not impose an act count or a color quota. Keep one primary visual structure per slide.

Highlight one meaningful phrase of a slide title in violet. Keep it inline with the rest of the title and let the sentence wrap naturally; emphasis does not require a second line. Preserve the logo’s original colors in every mode. Violet covers the entire slide, including header and footer. See the [mode and headline rules](references/design.md#visual-modes-and-headline-emphasis) and load `assets/deck-modes.css` last.

Choose the visual form by the reader’s task. For quantitative takeaways about trends, magnitude, composition, contributions or sensitivity, prefer a chart when it makes the relationship easier to see. Use tables when exact-value lookup or mixed textual detail is the primary task. Follow the [chart-selection guidance](references/legibility.md#choose-the-visual-by-the-readers-task); do not default to tables because the inputs arrived as rows. There is no chart quota.

Use as many slides as needed to cover the supplied report clearly, including its sources appendix. Let content and readability determine length; do not impose a default slide cap or compress a complete report into a short sample. Honor an explicit user slide limit.

Produce the complete requested deck by default, without a mandatory preview or design-approval checkpoint. Make a preview only when the user requests one, and follow their requested scope and review process.

Deliver only the requested formats. A PDF deck does not require an unsolicited PPTX. When an editable deck is requested, use host presentation tools with native text, charts and tables; an HTML/PDF export is not an editable PowerPoint. The bundled [rendering guidance](references/design.md#pdf-first-implementation) covers the format-specific requirements without loading another skill.

## Content and sources

- For restyling, preserve wording, numbers, units, caveats, table rows, chart categories and selective emphasis. If creating a deck from a report, condense deliberately without changing meaning. Never add unsupported callout metrics to fill space.
- Keep evidence distinct from analysis. Preserve uncertainty and the original research date; an export date must not imply refreshed evidence.
- Use source links in footnotes and retain detailed notes. For the complete sourced deck, include a full sources appendix unless the user specifies otherwise. Count it within any explicitly agreed slide limit. Each distinct cited source needs publisher/author, title, established date/version, full clickable URL and useful limitations from existing records. Do not invent missing metadata. For a user-requested preview, clickable source IDs may suffice; retain the full appendix for the complete deck.

## Verify and deliver

Check both geometry and reading comfort: a slide that technically fits can still be illegible. Use the fit-to-screen gate in the legibility standard and compare representative narrative, chart, table and source slides against the bundled approved reference. Review numeric tables for relationships that a chart would reveal more clearly, and charts for accurate scales and readable labels. Re-render and recheck changed slides. For long PDFs, add section bookmarks when supported.

Inspect every delivered slide at readable size after rendering the final output. Fix clipping, overlap, crowding, broken wrapping and footer collisions; prefer better layout to smaller type. Compare text and chart values with the input, verify page count and link destinations, and confirm fonts actually rendered. Check every mode used: original-color logos, readable dark prose and sources, violet through all four corners, and inline title emphasis without an artificial break.

This bundle is self-contained. Host authoring/rendering tools, installed browser/PDF libraries, artifact lifecycle hooks when supplied by the host, and the user’s research are environment inputs. Required design guidance, styles, fonts, licenses and visual references live inside this directory; no sibling skill or external helper is required.

Open the PDF when supported and return a concise link/citation. If the user requested a preview with a review checkpoint, state what remains before full production. Keep build files and validation logs private unless requested. Do not claim native PowerPoint testing unless performed.
