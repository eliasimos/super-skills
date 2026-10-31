# PDF validation and delivery

Use the host's bundled Python and Poppler tools when available. The renderer requires `reportlab` and `pypdf`; `pdftoppm` renders pages for visual review. Host artifact lifecycle hooks and output citation syntax are environment inputs, not dependencies on another skill.

Render every final page to PNG, for example `pdftoppm -png report.pdf review/page`. Inspect at readable scale for clipped text, overlap, crowded tables, missing glyphs, poor wrapping, incorrect emphasis, page furniture and logos. Text extraction does not establish visual fidelity. Re-render and inspect affected pages after repairs.

Compare extracted text, numerical values, citations and attachments with the authoritative inputs. Confirm embedded fonts and link targets. Do not claim visual QA from a structural manifest alone. If rendering is unavailable, disclose the missing dependency and leave visual verification explicitly incomplete.

Return the final PDF through the host's supported artifact citation or a clickable absolute file path. Keep temporary renders and build metadata separate from the final deliverable. No other skill or external helper is required.
