# Brayl deck design and rendering

## Reusable assets

- `../assets/deck-base.css`: plain CSS extracted from the user’s supplied React deck. Tailwind-only setup, viewer chrome and animations are omitted. It supplies layout primitives, not report content.
- `../assets/deck-layout.css`: local font faces, resets and the higher-header/lower-footer adaptation. Load after the base CSS.
- `../assets/deck-modes.css`: current palette, whole-slide modes, inline title accent and 8% margins. Load last, after report defaults and before deliberate slide-specific layout overrides. Keep custom colors tied to its tokens.
- `../assets/brayl-mark.png`: supplied six-dot Brayl mark, used without redrawing. Preserve its original colors and full opacity on every canvas, including dark slides. Do not whiten, invert, dim or recolor it. This deck design uses the mark rather than the memo’s full wordmark.
- `../assets/fonts/`: Instrument Serif, Inter and Spline Sans Mono with licenses. Resolve URLs relative to the CSS or embed fonts as data URLs for a self-contained HTML file.
- `../assets/reference-preview.pdf`: seven-slide visual reference from the State of AI work. It is an example of the design, not reusable factual content or evidence of approval for full production.
- `../assets/composition-reference.pdf`: six-slide palette/composition study incorporating the 26 October 2026 feedback: original-color dark-slide logo, full-canvas violet, and inline title emphasis. Use it for those treatments; its insurance content is not a template or refreshed evidence.

## Visual modes and headline emphasis

| Mode / article class | Argument role | Treatment |
|---|---|---|
| White / `slide--light` (also the default) | Explanation, evidence, comparisons and most body slides | White canvas, `#1a1a2e` ink, restrained rules |
| Midnight / `slide--dark` | A decisive proposition, constraint or trade-off | `oklch(0.14 0.025 265)` canvas, `#e8e8f0` headline, `rgba(226,226,242,.88)` body, light rules |
| Pale violet / `slide--violet` | Opening or a genuine chapter transition | `#e4e4ff` edge to edge, dark ink, sparse composition |

White carries the detail. Use midnight selectively and usually with less material than its neighboring analytical slides. Recompose for a single consequential claim rather than recoloring a dense page. Violet is structural, not a fourth kind of evidence panel. An opening may use it, but every report does not need an act structure. A useful sequence is orientation, reasoning, emphasis, application; it is not a fixed slide recipe or quota.

Apply the mode to the entire slide, including the header and footer. Violet has no white bands, inset violet content panel or dark footer. Dark body text, tables, labels and citations must all use light mode-aware values. The logo is the exception to recoloring: the original asset stays identical across modes. Existing web shells must match the slide surface; the React component names and `isDark` registry are implementation details, not dependencies of this skill.

For a normal claim title, choose one short, meaningful phrase to emphasize in `#7c7cff`: the implication, decisive verb phrase or key contrast. Keep the title a continuous sentence. Use an inline span (or an inline italic run when appropriate), preserving normal spaces and natural wrapping. Do not insert `<br>`, a block element or `white-space:nowrap` merely to isolate the accent; do not reduce headline size to force a single line. Neutral reference labels or titles that gain nothing from emphasis can stay plain.

```html
<h1 class="slide-title">A focused program <span class="title-accent">merits diligence</span></h1>
```

Keep one primary visual structure per slide: a ledger, chart, diagram, comparison or concluding statement. Supporting prose and citations should serve that same claim. Prefer rectangular blocks, hairline rules and whitespace; omit decorative gradients, dotted backgrounds, rounded-card grids, generic icons and dashboard widgets. Existing legacy CSS classes are compatibility assets, not invitations to use every visual treatment.

The transferable rules concern color, emphasis, composition and evidence. Do not import the fungibility deck’s seven-act narrative, Standard / Pro labels, grade geometry or provisional technical propositions into unrelated research.

## Geometry and type

For report composition, load `../assets/deck-base.css`, `../assets/deck-layout.css`, `../assets/deck-report.css`, then `../assets/deck-modes.css`, and follow [legibility](legibility.md). The bundled `../assets/legibility-reference.pdf` provides seven user-approved examples of report readability; use it as a visual benchmark, never as factual content for another report. Its older white-only palette and 120px margins do not override the current mode rules.

Use a fixed **1920 × 1080 (16:9)** canvas. At other resolutions scale all dimensions proportionally. Light defaults: white paper, ink `#1a1a2e`, secondary text `#555568`, violet `#7c7cff`, dark chart series `#151824`, links `#6868d8`, rules `#e1e1e8`. In dark mode use the corresponding `--slide-*` tokens; do not carry hardcoded black labels or dark chart series onto a midnight field.

| Element | Reference position/size |
|---|---|
| Side margins | 8% of canvas width: 153.6 px at 1920; about 1613 px usable width |
| Header | top 28 px, height 76 px, bottom rule |
| Mark | 34 × 52 px, preserve aspect ratio |
| Topic header | Spline Sans Mono, 20 px, right aligned |
| Title block | begins at y=140 px |
| Slide title | Instrument Serif 72 px, line-height 1.08 |
| Subtitle | Inter 32 px, line-height 1.38; 22 px below title |
| Main content | usually y=355–390 px through y=930 px |
| Body | Inter 32 px, line-height 1.38 |
| Content headings | Inter 38–42 px; regular by default in supplied design |
| Tables | Inter 28–29 px; mono header 23–24 px |
| Evidence strip | 67 px from bottom, Inter 18 px, top rule |
| Footer | 24 px from bottom, mono 18 px |

Keep clear separation between heading, middle content and evidence/footer. Multi-line titles need a lower content start; do not blindly keep a fixed y-position that overlaps the subtitle. Retain generous whitespace on sparse slides. On dense slides, adjust column proportions and paragraph placement before reducing type.

Use Inter Semibold 600 in the mode’s main ink only for retained or intentional selective emphasis. Avoid synthetic 700-weight bold. Keep the tested Instrument Serif / Inter / Spline Sans Mono stack: the web guide’s DM Sans / DM Mono switch was not part of this trial. Its responsive pixel sizes must not be copied into the fixed PDF canvas.

## Layout vocabulary

- Cover: compact violet kicker, large serif title (reference 126 px), muted 42 px subtitle, two-part metadata row separated by a quiet rule. Do not copy the example’s topic or date.
- Violet bridge: vertically centered title and one short explanatory paragraph; no statistics grid or dark panel. Use the entire canvas and preserve header/footer alignment. Only add evidence if the bridge itself makes an external empirical claim.
- Narrative/opportunity: flat columns with quiet top rules, headings and separated paragraphs. Reference classes `editorial-columns`, `summary-columns`.
- Tables: open rows, minimal horizontal rules, dark rule under header; no boxed grid or decorative cells. Preserve all rows and qualifications.
- Charts: violet and dark series, explicit units, readable axes and data labels; optional right-side evidence callout separated by a vertical rule. Every callout must be supported by the source content. Use real values, not the original demo indices.
- Process: `deck-journey` with numbered stages; `roadmap-four` offers a lighter timeline variant. Use only when the content is genuinely sequential.
- Sources: compact, consistent, ruled footnotes with source identifiers and live links; use the available bottom space without colliding with the footer. Keep material caveats beside the claim, not buried in citations. In a complete deck retain readable full references in an appendix. Do not add ad hoc body-level `Sources:` paragraphs or squeeze a full bibliography into one slide. Source text must change to the readable light tokens on dark slides.

## Chart construction

Choose chart types using the [reader-task guidance](legibility.md#choose-the-visual-by-the-readers-task), not the limited chart examples bundled in the CSS. The provided two-bar layout is one example, not the only supported chart form.

- Give the plot enough of the content area to carry the explanation. Prefer direct category and value labels over distant legends when practical. Put units, period and scenario basis where the reader sees them with the plot.
- Use violet for emphasis and dark/neutral series for comparison, with consistent meanings across the deck. Distinguish series through text, position or line style as well as color. In heatmaps, use a legible sequential or diverging scale suited to the values; do not rely on color alone to convey results.
- Start magnitude bars at zero. Use common axes for comparable small multiples. Make any non-zero line-chart scale explicit; avoid dual axes unless essential and clearly explained. Do not connect incompatible survey panels or vintages into an apparent continuous trend.
- Reconcile waterfall endpoints to signed contributions. Use stacks only for additive components with a common denominator. Clearly distinguish estimates, scenario ranges and historical observations. Keep material caveats with the chart.
- Preserve the role-based type sizes in the legibility standard. If labels collide, change orientation, shorten labels without changing meaning, or split the chart; do not merely shrink text. Avoid 3D effects, decorative gradients and unnecessary gridlines.
- For PDF-only work, prefer vector SVG or browser-native vector charts with selectable labels where supported. For editable PPTX, use host presentation tools to create native editable charts and tables. Always reconcile the rendered chart to its underlying data; never approximate values for visual effect.

## PDF-first implementation

For PDF-only decks and previews, adapting the provided HTML/CSS directly preserves the design well. Build static semantic HTML using the relevant classes; React and the original viewer are not needed for export. Use an `article.slide-content` per slide with `deck-slide-header`, title/subtitle, the selected content layout, `.evidence` and `deck-slide-footer`.

Print with a local headless browser using `@page { size:1920px 1080px; margin:0; }`, exact print colors, and page breaks after each article. Wait for `document.fonts.ready` and layout/paint completion before rendering. Use installed/bundled dependencies; discover their paths rather than hardcoding a particular runtime release. If Playwright’s browser is absent, an installed Chrome channel may work. Respect sandbox escalation requirements; do not change browser profiles or install a new stack unnecessarily. Run the host’s artifact-start hook if the environment supplies one; it is not a sibling-skill dependency.

Check the resulting PDF page count and render it using Poppler or an available PDF renderer. Inspect each page, not only browser screenshots. Browser PDF preserves selectable text and vector charts better than flattening each page to a PNG. A fixed visual PDF is an acceptable fallback when needed, but do not present it as editable source.

For native PPTX authoring, use the available host presentation API or installed authoring library. Reproduce the reviewed geometry with editable text, tables and charts; use a colored text run for inline headline emphasis. Register the supplied fonts in the actual rendering engine, not just an unrelated canvas library. Verify font names in the output and visually compare rendered slides. If fonts are not embedded, provide the font/license bundle and explain that they should be installed for editing. If the host cannot create the requested editable format, state that limitation rather than substituting a flattened PDF as editable output.
