# M5 source due diligence — candidate only, NOT approved ingestion

**Review date:** 2026-11-18.
**Status:** `proposed / permission-unverified`, **no real dataset ingested**.
**Decision:** **NO-GO for automated download, committed mirrors or production
data use until a human reviewer independently verifies the actual
license and terms for the intended use.** This is a technical
discovery checkpoint, not legal advice or a legal approval.

## Source paths reviewed

| Candidate source | What was visible | Authorization still needed |
| --- | --- | --- |
| [Official M5 Forecasting — Accuracy data page](https://www.kaggle.com/competitions/m5-forecasting-accuracy/data) | Original competition data location, with dataset description and license section | Confirm the exact dataset license, competition-specific rules, accepted Kaggle account terms and whether separate research/product/commercial use is permitted |
| [Official M5 competition rules](https://www.kaggle.com/competitions/m5-forecasting-accuracy/rules) | Rules page exists, but the complete relevant text was not independently retrievable in this review | Read and retain the currently applicable data-access, non-commercial/research, redistribution and downstream model terms |
| [Zenodo record 10.5281/zenodo.12636070](https://zenodo.org/records/12636070) | Open deposit created 2024-07-03, listing a 48 MB archive and describing the dataset as taken from Kaggle | Establish whether the depositor had redistribution rights and whether the license applies to the **underlying Walmart/M5 data**, not just metadata or repository wrapper |
| [Kaggle general terms](https://www.kaggle.com/terms) | General platform terms exist | These **do not by themselves replace** the competition-specific dataset use grant |

**Critical distinction:** an open download, a file digest,
a research paper with a Creative Commons license, or
a third-party statement of `CC BY` **does not
establish that the original underlying competition
data may be redistributed or used commercially**.
The accessible Zenodo HTML did not provide a license
grant that this review could independently verify.
Do not interpret this observation as a definitive
legal conclusion about the true license.

The future MirrorMind product is not automatically
within the same permitted scope as a private academic
benchmark, a Kaggle competition entry, a published
article or an educational demonstration.

## Gates before any real-data experiment or ingestion

1. **Document the actual source rights:** identify
   rights holder, exact grant/licence text, applicable
   jurisdiction, user/account acceptance and conditions
   for the specific *research versus commercial*
   purpose; store an approved internal reference to
   the authorization evidence, not passwords or secrets.
2. **Confirm distribution scope:** decide whether
   MirrorMind may download, retain, transform, publish,
   train or redistribute any data or trained artifact;
   absence of evidence is a **stop**, not an implicit
   grant.
3. **Minimize:** use only an approved bounded subset;
   do not commit raw M5 data or third-party mirrors
   into the repository merely to simplify CI.
4. **Create a signed-off dataset card:** capture
   exact source URL, timestamp, content hash, snapshot
   version, retention, data sensitivity and reviewer;
   use [the data card template](../DATASET_CARD_TEMPLATE.md).
5. **Resolve temporal truth:** original M5 sales are
   historical observations, not inherently verified
   day-by-day *publication vintages*. If source
   publication times cannot be reconstructed,
   mark this limitation, avoid fabricated
   `available_on` labels and disclose the risk
   in experimental backtests.
6. **Independent model/evaluation review:** lock a
   real holdout before tuning, report missing/zero
   conventions, baseline and units, and do not
   assert inventory or lost-demand observations that
   the source does not actually contain.

The current `stage_csv_snapshot` hash comparison and
`backtest_staged_snapshot` as-of checks are **only
structural algorithms**. They do not perform rights
verification and must not be used to mark this
candidate `authorized`.

## Next decision to request from the operator

Either supply verifiable permission for the original
M5 source and the intended project use, or select a
different dataset with demonstrably appropriate
permissions. After human review, open a **separate**
source-specific adapter PR with a limited snapshot,
independent hashes, dataset card, permission
evidence, publication-time assumptions and
reproducible tests. Keep any external dataset out
of git until the distribution scope is explicitly
approved.

No access token, login, data archive or real
source snapshot is contained in this note.
