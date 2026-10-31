# Temporal fit of research evidence

**5 October 2026 · Proposed reusable policy · R22 documentary evidence**

Assess **a source’s use for a particular claim and question**, rather than giving every document a freshness score. Authority, relevance, access and temporal fit remain separate. A respected old source can be appropriate; a new source can describe old data or be wrong. The original project research (historical provenance, not bundled) links originals and limitations. This policy is not an implemented scheduler or a calibrated decay model.

## 1. Infer the question’s time contract

The lead infers this from the prompt/context; ask the user only if an ambiguity changes the answer materially. Save it with the refined brief and allow later editing.

| Question mode | Evidence must answer |
| --- | --- |
| Current decision | What applies at the named as-of date, region/entity and configuration? |
| Historical reconstruction | What happened during the target period, using admissible scholarship/evidence available now? |
| Knowledge as of a past date | What could have been known by that cutoff? Later revisions or discoveries cannot silently enter the answer. |
| Trend/comparison | Which observations and vintages are comparable across the target intervals? |
| Forecast | What is observed, what is projected, and when was the forecast made? |

An ancient target period does not require ancient publication. A modern excavation may improve historical reconstruction but be inadmissible to a question about what scholars knew in 1996. A backtest using revised data available only later has the same issue. Preserve approximate periods, BCE labels, date granularity and timezone; never fabricate a precise timestamp.

## 2. Keep the clocks separate

Capture available fields once; missing values stay explicitly unknown with their provenance.

| Field | Meaning / common mistake |
| --- | --- |
| Target time | Period/date the question asks about; not automatically today |
| Evidence time / coverage | When measurements/events occurred; a 2026 report may contain 2019 observations |
| Effective validity | When a rule, offer or contract applies, if established; an unknown end does not mean valid forever |
| Publication / substantive revision | When the source was released or materially changed; footer/search/snippet dates are not reliable substitutes |
| Knowledge availability / vintage | When the information could be known, including revisions; not the measurement date |
| Retrieval / version check | When we downloaded or inspected it; not proof of any of the above |
| Version / supersession | Exact edition/model/API/jurisdiction, correction/retraction/replacement links, scoped claim affected |
| Expected update / resolution | Publisher’s schedule and observation granularity; promises are not observed adherence |

Attach a basis to each date: original labeled field/passage, versioned metadata or verified capture. A header, crawler timestamp, file mtime or copyright year is only that kind of metadata. A catalog-record revision may leave the underlying dataset unchanged. A hash/ETag/304 can validate a representation while its claims remain outdated.

Keep immutable acquired evidence separate from revisable claim-use assessments. Do not overwrite a dated observation to make it current. A present capture cannot reconstruct a missing historical snapshot.

## 3. Infer freshness needs per claim family

| Family | Starting review policy |
| --- | --- |
| Historical scholarship / stable mechanism | Prefer authority, method, target-period coverage and current scholarly/correction context. No age-only exclusion. Recheck when new evidence or disputed interpretation could change the answer. |
| Version-bound behavior / law / permissions | Match exact version, jurisdiction and effective dates. Check amendments, deprecation, expiry or revocation at consequential decision points. Old issue date alone is not expiry. |
| Live state / price / availability | Obtain an explicit observation/as-of date close enough for the intended action. Recheck at decision publication and before a materially later commitment. Distinguish asking price from a quote and advertised state from verified availability. |
| Measurements / statistics / benchmarks | Match collection period, definitions, entities and methodology; record released vintage/revisions. An old benchmark may describe its experiment but cannot automatically rank today’s systems. |
| Plans / forecasts | Record announcement and forecast dates; do not turn a planned completion into an observed outcome when its deadline passes. |

These are starting policies, not universal thresholds. If a numerical window is useful, save its rationale, claim family, stakes, publisher cadence, source of the rule and review trigger. Mark inferred windows as provisional. A publisher’s legally explicit expiry differs from our reminder to recheck. Do not invent a half-life, annual quality penalty or accuracy probability.

## 4. Source verifier: assess admissibility for this use

Return the source role, temporal evidence, rationale and next check. Useful labels are:

- **Suitable for the target**, with explicit scope/as-of/version and uncertainties.
- **Historical only for this proposed current use**, while retaining possible other roles.
- **Needs revalidation** because a consequential version/state may have changed.
- **Unknown** because required dates, lineage or historical snapshots are absent.
- **Contradicted/superseded for this use** only when evidence identifies the conflict or replacement.

These labels do not certify factual truth. “No update found” is not “no update exists.” A newer source must still pass authority/method checks and can be worse evidence. Preserve a source useful for historical analysis, mechanisms or a different claim rather than rejecting the whole document. Correction/retraction notice participation is incomplete; silence cannot prove clean status.

## 5. Goal verifier and next-search queue

Check whether **material claims jointly answer the same temporal question**. Matching an entity identifier is insufficient if its owner, rights, definitions or service configuration changed between observations. Temporal overlap alone also does not establish causality or current capacity.

Identify unsupported present-tense promotion, hindsight, incompatible vintages, expiry/forecasts treated as facts, and false rejection of useful older evidence. A satisfactory report can answer with a dated scope or explicitly say the current/private state is unresolved.

Prioritize refreshes where a change could alter the recommendation or invalidate an important join. Retrieve a material amendment, newer measurement or changed acquisition route; do not recrawl the entire corpus every round. An unchanged fetch/cache hit alone adds no new research evidence. A newly established contract boundary or scoped amendment can add information; record the effect once.

Retained answers carry as-of dates and evidence/version links. Revalidate affected claims and downstream answers after a relevant revision; do not silently rewrite historical results. Numerical reminders and event checks are future scheduling design, not automatically installed monitors.

## 6. Evaluation cases

Include pairs where publication age alone gives the wrong decision: authoritative old historical source versus weak new summary; fresh report with old data; refreshed catalog with unchanged dataset; old API description for an exact old-version question versus a current-version question; future announcement; known correction; unknown dates; revised economic series in a backtest; and a valid older permit with no evidence of renewal/expiry status.

Measure incorrect current claims, hindsight leakage, incompatible temporal joins, valuable-old-source rejection, date fabrication, unsupported “no change” conclusions and refresh cost/latency. Date-aware retrieval success and full-answer correctness are separate. Historical QA results inform test design without establishing current deep-research performance.
