# Data card — staged 35-day weekly fixture with late publication

**Status: invented, local and unverified. Not approved source evidence.**

- **Path:** [`examples/staged-weekly-availability.csv`](../../../examples/staged-weekly-availability.csv).
- **Producer:** manually generated, no retailer, individual,
  customer transaction, dataset provider or external collection.
- **Usage:** local regression and teaching only, not licensed
  evidence for business decisions or a training sample.
- **Shape:** exact `series_id,observed_on,available_on,units`,
  35 chronological daily rows, one fictional `item-A` series.
- **Calendar:** January 1 through February 4, 2025 inclusive.
- **Target units:** repeating seven-day integers
  `[2,4,6,8,10,12,14]`. These are **not** observed sales
  or estimates of latent demand.
- **Declared delayed release:** January 27 recorded as
  first available January 31; all other values same-day.
- **Integrity:** code computes SHA-256 from the supplied
  fixture only. It does not attest a real source or
  independent producer.
- **Privacy:** no real personal or commercial records
  included. No real permission is implied for other files.
- **Revision history:** nonexistent; changes to raw CSV
  produce new hashes and require review.

This CSV demonstrates the difference between
event dates and as-of publication dates. The four
February scored origins are selected *because* the
lag-7 input set is complete by their origin; three
prior origins abstain. A future real-world dataset
must supply verified releases, a stable provenance
record, access/retention approvals and an independent
untouched holdout. The full
[data card template](../DATASET_CARD_TEMPLATE.md)
remains unfulfilled for any real source.

See [the source-method guide](../M1_STAGED_ROLLING_BASELINES.md)
and the [synthetic model card](../model_cards/STAGED_WEEKLY_BASELINES.md).
