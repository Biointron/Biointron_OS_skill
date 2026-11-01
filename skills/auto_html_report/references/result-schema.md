# Result JSON Field Guide

Read this guide when mapping input data to a report. Follow SKILL.md for presentation, chart selection, image handling, language, and delivery. Field names below are exact input keys, not customer-facing labels.

## Input shapes

Accept either a business payload containing `meta` and `samples`, or a response that contains that payload:

- A direct payload may use `meta`, `stats`, and `samples`, or `meta`, `assays`, and `samples`. A missing `stats` object does not invalidate the latter shape.
- In a response envelope, the payload is under `result`.
- In an additional transport wrapper containing `http_status` and `data`, the payload is under `data.result`.

The payload must be an object. `samples` must be an array of objects. Resolve invalid structure, explicit failure, or contradictory status before creating a normal customer report. Do not silently discard malformed rows.

For the supported success envelope, `success` is the Boolean `true` and `code` is the number `200`. Do not treat a nonempty string as Boolean success or assume undocumented status codes have the same meaning. If status metadata is incomplete but the payload is usable, describe the limitation without inventing a success state. Transport metadata does not belong in the customer report.

Descriptions, schema placeholders, and illustrative structures are not experimental results. An empty sample array means no sample records were supplied; do not invent results or completion status.

## Values, identity, and missing data

- Distinguish an absent key, an empty string, an empty array, and `null` from valid numeric `0` and Boolean `false`.
- Preserve source text markers such as `NaN`, `N/A`, `NA`, and `/`. They may count as returned fields, but not as finite numerical measurements.
- Measurements can be numbers or strings, including scientific notation and values with units. Preserve source precision. Parse only clearly defined finite numerical values for plotting or calculations; do not coerce the whole payload to floating point.
- Preserve limit qualifiers such as `<` and `>`. Do not remove them and plot the remaining number as an exact measurement.
- `meta.assay_list` describes assay categories, not completion for every sample. Count categories, configurations, sample records, and controls separately.
- Retain each original row and its identity. Repeated names, missing identifiers, and duplicate identifiers do not authorize merging records.
- Reconcile requested order scope, `meta.order_id`, and any row-level `Order_ID`. Compare declared sample counts with actual rows without silently replacing either count.
- Prefer sample names and customer-facing identifiers for display. Internal identifiers, operational positions, raw field paths, and transport metadata stay out of the delivered HTML and CSV, including hidden content and embedded raw payloads.

## Order and sample fields

These fields occur in the nested-module input shape. Preserve spaces, punctuation, and capitalization when reading keys. For example, `Conc.` is one literal key, not a nested path.

| Exact field | Type | Meaning and handling |
| --- | --- | --- |
| `meta.order_id` | String | Order identifier |
| `meta.customer_name` | String | Customer name supplied for the report |
| `meta.project_name` | String | Order-level project name |
| `meta.assay_list` | Array of strings | Declared assay categories; it may be empty |
| `meta.report_version` | String | Supplied report or payload version |
| `stats.n_samples` | Number | Declared sample count; may be empty or zero and does not replace actual row count |
| `samples[].Project ID` | String | Customer-facing project or sample identifier |
| `samples[].PPB ID` | String | Customer-facing sample or project identifier |
| `samples[].DPP ID` | String | Internal tracking identifier; exclude from customer output by default |
| `samples[].Samples Name` | String | Original sample name |
| `samples[].Tag` | String | Optional sample label |
| `samples[].Conc.` | Number or string | Concentration; a fixed unit is not established by this key |
| `samples[].Lot No.` | String | Lot identifier |
| `samples[].Molecular weight` | Number or string | Molecular weight; confirm the unit from the input |
| `samples[].PI` | String | PI-related field; confirm its definition before expanding the label or interpreting it |
| `samples[].Order_ID` | String | Row-level order identifier |
| `samples[].IsControl` | Boolean or string | Control flag; string values require an explicit mapping, not a nonempty-string test |
| `samples[].Expression_mg_per_mL` | Number or string | Expression value associated with mg/mL; preserve or clarify the supplied unit |

## Column-driven input

When `assays` is present, each item declares a configuration with `assay_type`, a display `label`, and ordered `columns`. Optional selectors include `ligand`, `target`, `cell`, `index`, and `unit`.

Create one Data Summary column group per configuration, in declaration order. Read each metric using the exact key in `columns`. Display labels can be translated; lookup keys cannot be translated, lowercased, split on punctuation, or stripped of units. Multiple configurations of one assay type remain separate.

### Fixed identity columns and metadata

| Exact field | Report use |
| --- | --- |
| `samples[].project_id` | Project ID; retain its value and original row identity |
| `samples[].project_name` | Sample name; do not substitute the order-level project name |
| `samples[].expression_level_mg_L` | Expression in mg/L, preserving source precision |
| `meta.sample_count_total` | Declared sample count; reconcile with the actual sample rows, excluding separate controls |
| `meta.report_generated_at` | Supplied report-generation date; not automatically an experiment date or the current file-creation date |

Keep the identity, name, and expression columns even when individual fields are missing. Do not mix expression units in one column without an explicit conversion and explanation. `show_uptiter=false` does not hide, clear, or replace `expression_level_mg_L`; `uptiter` is a separate field and cannot be used to infer expression without an explicit definition.

### Configuration-to-record matching

The module paths below are relative to one sample object and apply to the column-driven shape. Select the record first, then read its declared columns.

| `assay_type` | Sample module | Selection rule |
| --- | --- | --- |
| `cge` | `cGE` object | Read declared columns such as `Purity (%)` and `Risk` |
| `octet` | `Octet` object | Read declared columns; retain numerical kinetics and `Outcome` independently |
| `carterra` | `Carterra` array | Match both `ligand` and `index`; never use array position or the first target as a fallback |
| `spr_biacore` | `spr_biacore` object | Read declared columns |
| `dsf` | `DSF` object | Read declared columns; use units explicitly included in their labels |
| `ac_sins` | `AC-SINS` object | Read declared columns; preserve wavelength or red-shift units supplied in those labels |
| `bvp_elisa` | `PSR_BVP` array | Match both `target` and `index`; keep BVP and Insulin configurations separate rather than seeking a separate top-level Insulin module |
| `ique` | `ique` array | Match `cell` exactly; a configuration index is not an array position |
| `SEC_HPLC` | `SEC_HPLC` object | Read all declared columns, including columns with empty values |
| `SEC_UPLC` | `SEC_UPLC` object | Read declared columns |
| `elisa` | `elisa` object | Read declared columns; verify the record's `cell` when the configuration specifies it |
| `PAIA` | `PAIA[channel]` array | Extract the channel from `RFU_<channel>`, then match `index` within that channel's array |
| `dls` | `dls` object | Read declared columns such as `RH (nm)` and `Scattering` |

A missing match produces missing results in that configuration, not values borrowed from another target. Resolve multiple matches or selector conflicts; do not take the first row, average records, or overwrite them silently. Extend the mapping only when the input defines the module, selectors, and display fields. Do not publish unknown keys merely because they exist.

Use a unit included in a column name for that column. Apply a separate `unit` only to the metric it explicitly describes: an EC50 unit does not apply to Hill or r2, and an iQue EC50 unit does not transfer to ELISA.

Read assessment keys exactly as declared, including `Risk`, `Insulin Risk`, `Outcome`, or `Fit validity`. Preserve numerical results alongside source assessments such as `no binding`, and preserve `N/A` alongside `OK` when both occur. Do not reconcile these combinations by changing either value or inventing a grading threshold.

### Kinetic field pairing

SPR and BLI use only double-logarithmic kinetic plots with dissociation rate `k_d` on the horizontal axis and association rate `k_a` on the vertical axis. Keep the titles SPR (K_D) or BLI (K_D), followed by platform and target. Use these exact column-driven fields:

| Assay | Horizontal dissociation rate | Vertical association rate | Independently retained source K_D |
| --- | --- | --- | --- |
| BLI Octet | `Octet["kdis (1/s)"]` | `Octet["ka (1/Ms)"]` | `Octet["KD (M)"]` |
| SPR Carterra | `kd (s-1)` in the matched target/index record | `ka (M-1s-1)` in that same record | `KD (M)` in that same record |
| SPR Biacore | `spr_biacore["kd (1/s)"]` | `spr_biacore["ka (1/Ms)"]` | `spr_biacore["KD (M)"]` |

These labels establish dissociation units of 1/s, association units of 1/(M*s), and K_D units of M. Confirm units for other input shapes instead of assuming that similar key names define them. In the nested-module shape, the corresponding keys are `kd_s`, `ka_M_s`, and `kd_M`; rate units require explicit confirmation.

Each plotted point must pair two positive finite rates from the same sample, platform, and target. Do not substitute K_D for `k_d`, borrow another target's rate, or infer a missing rate from K_D. Constant-K_D lines express `K_D = k_d / k_a`; they are not acceptance criteria and do not replace source K_D values.

The name-sorted and value-descending views for ordinary metrics change only chart order. Keep Data Summary and full result tables in source row order. Do not create those sample-axis K_D views for SPR or BLI.

### Separate control records

`QC_data` contains arrays grouped by `assay_type`, independently of `samples`. Control rows usually contain `project_id`, `project_name`, and metric columns directly; do not search for a second nested sample module inside them.

Select `QC_data[assay_type]`, then apply the relevant target or condition selectors. In particular, match both `target` and `index` for `QC_data.bvp_elisa` so that distinct configurations cannot share results accidentally.

When controls appear in Data Summary:

- Retain each supplied record and its usable identity, clearly marked as a control.
- Fill only its own configuration columns. Missing expression or unrelated assay values remain missing.
- Do not combine repeated names across assays or targets into a synthetic sample, and do not fill controls from sample records.
- Keep control counts separate from sample counts. A visibility switch changes the view, not either dataset.
- Use a separate control table when identity or configuration membership cannot be established reliably.

Customer output contains only defined display fields and appropriate identity columns. Exclude `elisaPlateNo`, `elisaHoleNo`, `positions`, `colors`, internal task identifiers, and other operational metadata from visible content, hidden content, and exports. A `colors` field is not a grading rule. Controls do not replace sample results or experimental images.

## Nested-module input

This shape stores assay fields directly within named modules in each sample. Assessment fields are strings; other measurements can be numbers or strings. Preserve the input module name and exact key spelling when resolving aliases.

### cGE

| Field | Meaning and handling |
| --- | --- |
| `purity_no_r` | Purity field described as without replicate handling |
| `purity_r` | Purity field described as with replicate handling |
| `purity_Outcome` | Reported purity assessment |

The suffixes do not establish non-reduced versus reduced conditions. Confirm the meaning when needed and do not invent percentage units. Image fields may also occur in the module.

### DSF

`tonset` is the onset-temperature field. `tm1`, `tm2`, `tm3`, and `tm4` contain melting-temperature results. `outcome` is the reported assessment. This shape does not establish a fixed temperature unit; use an explicitly supplied unit or state that it is unspecified.

### BLI_octet or BLI

| Field | Meaning |
| --- | --- |
| `response` | Main binding response |
| `kd_M` | Equilibrium dissociation constant K_D in M |
| `kd_error` | K_D fitting error |
| `ka_M_s` | Association rate k_a |
| `ka_error` | Association-rate fitting error |
| `kd_s` | Dissociation rate k_d, distinct from `kd_M` |
| `kdis_error` | Dissociation-rate fitting error |
| `full_r_2` | Overall fit R-squared |
| `rss` | Residual sum of squares |
| `rsskd` | K_D-related residual metric |
| `rss_r_2` | Residual-related R-squared metric |
| `outcome` | Reported binding assessment |

Do not infer undocumented units or fit-acceptance thresholds from suffixes. If both `BLI_octet` and `BLI` occur, retain them separately and resolve their relationship rather than overwriting or duplicating records.

### SPR_Carterra or Carterra

The module is keyed by actual target name. Each target contains `kd_M`, `ka_M_s`, `kd_s`, `outcome`, and any associated image fields. K_D is in M; confirm rate units before plotting. Preserve target names exactly and report each target separately. Do not merge targets, normalize spaces in their keys, or reuse one target's image for another.

Both module names are supported when their structure matches this shape. A generic `SPR` module does not by itself establish the same mapping. If multiple aliases coexist, resolve their relationship explicitly.

### PSR_BVP

- `Signal_1` and `Signal_2` are separate objects, each with `signal` and any associated image fields.
- Module-level `mfi`, `sb_data`, `score`, and `outcome` remain distinct from signal-level measurements.
- `mfi` represents mean fluorescence intensity or the explicitly defined equivalent metric. `sb_data` is a signal/background-related field; `score` is a supplied score.
- No formula is defined here for deriving `score` from individual signals. Preserve the supplied results without inventing that calculation.

### ACSINS

`wavelength` can represent a score or a wavelength-related result; its meaning is not sufficiently defined to label it universally as wavelength or nm. `red_shift` is a red-shift field, commonly associated with nm but requiring confirmation from the supplied data. `Outcome`, with this capitalization, is the reported assessment.

## Image and operational fields

| Field | Type | Handling |
| --- | --- | --- |
| `src` | String | Embedded image data or an image reference; inspect its actual format before decoding or resolving it |
| `title` | String | Supplied image or curve title |
| `plate_name` | String | Operational plate name; use for association when necessary, not customer display by default |
| `well` | String | Operational well position |
| `plate` | String | Operational plate identifier, distinct from plate name |

Image fields may occur within an assay, a target, or a signal. Retain their original association. Absence of embedded images does not rule out separately supplied image files; inspect both the payload and any additional `image_paths` information.

Resolve relative file references against the input file's directory or a directory explicitly provided for the task. A path on another machine is not automatically readable locally. Do not expose local paths or access credentials in the customer report.

When no images are supplied, omit the image section, empty image cards, missing-image placeholders, and zero-image statistics. Insert an image only after confirming readability, format, and sample/assay/target association. Report supplied-but-unusable images in the delivery note; add a short note to the affected assay only when the missing image changes interpretation. Do not describe unseen curves or reconstruct experimental images from numerical results. Numerical comparison charts remain independent of original image availability.

## Interpretation boundaries

Read assessment keys exactly: `purity_Outcome` for nested cGE, `Outcome` for nested ACSINS, and `outcome` for nested DSF, BLI, Carterra, and PSR_BVP. For column-driven input, use the keys declared in `columns` instead.

Preserve the strength and meaning of source assessments when translating. Keep the original wording when interpretation is uncertain. No acceptance thresholds, scoring formula, or experimental-completion contract is defined by this guide. Missing results do not establish failure, a negative finding, or an unfinished experiment.

For an unfamiliar field or module, require enough definition to establish its meaning and whether it belongs in a customer report. Preserve the source data while resolving ambiguity; do not silently publish unknown operational fields. Use a localized missing-result label for absent numerical results, and apply the separate image-availability rules to images.
