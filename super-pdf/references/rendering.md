# Rendering and inputs

## Design geometry

All dimensions below are points. A4 portrait; margins left/right 44, top 88, bottom 51. Wordmark width 88, height 28.865, bottom-left at `(44, page_height - 59)`. Header rule at `page_height - 73`; footer rule at y=37; footer/page number baseline y=24. Logo keeps its aspect ratio and transparency.

| Element | Font | Size / leading | Spacing |
|---|---|---|---|
| Main title | Instrument Serif | 32 / 34 | after 12 |
| Section heading | Instrument Serif | 22 / 26 | before 17, after 9; keep with next |
| Body and lists | Inter Regular | 10 / 14.7 | after 9 |
| Body emphasis | Inter Semibold 600 | inherits size | pure black |
| Subtitle metadata | Spline Sans Mono | 8.2 / 12 | after 15, violet |
| Running header/footer | Spline Sans Mono | 6.8 | short enough to avoid logo/page number |
| Table cell | Inter Regular | 8.7 / 12.8 | padding 8 each side |
| First table column | Inter Regular | 8.3 / 12.8 | preserves source emphasis |
| Table header | Spline Sans Mono | 7.8 / 11 | pale background |
| Reference heading | Inter Semibold | 9 / 13 | after 4, black |
| Reference prose | Inter Regular | 8.6 / 12.2 | after 4 |
| Reference URL | Inter Regular | 8 / 10.5 | after 4, violet; allow wrapping |

Tables repeat their header row after page breaks, use 0.5pt hairline rules and white body cells. Right-align numeric columns according to the Markdown alignment row or explicit config. Total-row styling is opt-in, not inferred from the number of columns. Three-column narrative tables default to 23%/35%/42%; other tables default to equal widths. Override by content and inspect.

## Renderer interface

`render_report.py` reads a Markdown report, a JSON config, optional JSON reference data, and the skill's bundled assets. It emits a PDF and `.export.json` manifest next to it. Dependencies: Python 3, ReportLab, pypdf. Use the available bundled runtime. It does not browse or fabricate missing citations.

Supported Markdown: `#` title, `##` section headings, ordinary paragraphs, flat numbered/bullet lists, pipe tables, `**bold**`, `*italic*`, and inline links. Blank lines separate paragraphs. A subtitle is treated as metadata only when its exact text matches `config.subtitle`. The original example's date/topic and budget paths are not defaults.

Complex/nested lists, code, blockquotes, images, deeper headings, raw HTML and other advanced Markdown require an intentional renderer adaptation. The helper rejects common unsupported blocks. Inspect the source for other unsupported syntax before running. Table cells cannot contain literal unescaped pipes. Link labels should be plain text; complex/nested markup requires adaptation. The renderer normalizes en/em/nonbreaking dashes to printable ASCII hyphens; preserve their meaning when checking text.

Local links must resolve to an explicitly supplied attachment. The renderer labels these with their actual embedded filename; it never invents a budget attachment. Attachment files are embedded as inert bytes, not executed. HTTP(S) links remain live. For general hyperlinks that are not evidence (for example a product's navigation), adapt the reference coverage check deliberately rather than inventing an evidentiary citation.

### Config

Paths in attachments can be absolute or relative to the config file. Table keys are one-based occurrence numbers in the report; column indices are zero-based. `title`, `running_header` and `footer` are required. Keep the running header short; the script checks its width.

```json
{
  "title": "Report title",
  "author": "Author or organisation",
  "running_header": "REPORT TOPIC  /  SHORT SUBTOPIC",
  "footer": "Report type  |  Actual report date",
  "subtitle": "Exact optional subtitle line from the Markdown",
  "tables": {
    "2": {
      "widths": [0.29, 0.10, 0.15, 0.16, 0.15, 0.15],
      "right_columns": [1, 2, 3, 4, 5],
      "total_row": true
    }
  },
  "attachments": [
    {"path": "calculations.json", "name": "calculations.json"}
  ]
}
```

A sourced report requires references unless the user explicitly requests their omission; only then set `omit_sources: true`. For an unsourced report, neither reference data nor this flag is needed.

### Sources appendix

Use first-citation order and deduplicate sources while retaining alternative cited URLs. Each source entry requires `author`, `date`, `title`, `url`, `note`. Other fields are optional. Numbering is generated, not hardcoded. Include full journal/publisher details and DOI in `detail` when verified. Use `n.d.` for an unknown publication date, and explicitly identify a descriptive title if the original title could not be established. Only claim a retrieval/inspection date supported by records.

```json
{
  "title": "Sources appendix",
  "intro": "Scope, evidence cutoff and access conventions verified for this report.",
  "entries": [
    {
      "author": "Verified author or publishing organisation",
      "date": "Established year/version, or n.d.",
      "title": "Verified source title",
      "detail": "Journal, volume, issue, pages, DOI or document version where verified.",
      "url": "https://example.org/report",
      "extra_urls": ["https://example.org/report.pdf"],
      "note": "How the report uses the source, relevant locator, evidence type and material limitations.",
      "report_labels": ["Visible in-text link label"],
      "source_id": "Optional existing source-register ID"
    }
  ],
  "supplements": [
    {
      "title": "Calculation provenance",
      "text": "Who prepared the calculations, when, their empirical inputs, assumptions and limits.",
      "attachments": ["calculations.json"]
    }
  ]
}
```

The appendix starts on a new page and inherits the logo and running furniture. It distinguishes evidence of effectiveness from implementation descriptions and modelling assumptions when those distinctions matter to the source report. It does not refresh evidence merely by reprinting references. Do not claim unacquired sources were reviewed, and do not pad the bibliography with search leads unused in the report.

## Quality checks

- Verify all original words/figures survive in correct reading order, with no leftover Markdown markers. Repeated table headers, running furniture and line wrapping are layout, not content changes.
- Inspect every new/changed rendered page. For unchanged pages, pixel equality with a previously inspected export can establish preservation.
- Check actual embedded font names and text fill colours. Inter Semibold must not share the regular font's internal PostScript name; unique file names alone do not fix the deduplication problem.
- Compare every external citation destination to the appendix; inspect long displayed URLs for clipping, while preserving their exact link targets.
- Check attachment names and byte hashes; retain the original assets as appropriate.
- Keep meaningful validation small. The renderer's structural assertions and manifest do not substitute for visual inspection.

## Asset provenance

The logo is the user's supplied `brayl-logo.png` from `brayl-memo-code.zip`, approved for this report skin. It is not an open-source asset or a statement of permission for unrelated external branding.

Fonts: Instrument Serif and Spline Sans Mono from the official Google Fonts repository; Inter from the user's installed Inter variable fonts. Inter instances use optical size 14 and weights 400/600. Names were made unique per weight/style. Preserve the bundled static instances to reproduce the approved appearance. Font source locations:

- https://github.com/google/fonts/tree/main/ofl/instrumentserif
- https://github.com/google/fonts/tree/main/ofl/splinesansmono
- https://github.com/rsms/inter

The initial style reference was the user's approved 15-page employer-programme PDF; its report content, dates, references, financial assumptions and page count are not part of this reusable skin.
