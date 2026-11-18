# Fictional UCI-shaped row mappings — MM-M1b projection test card

**Status:** deliberately invented in-Python fixtures. No UCI source
workbook, customer's dataset, personal data, account or external
retail observations were downloaded for these tests.

| Property | Reviewed convention |
| --- | --- |
| Location | [Unit fixtures](../../../tests/unit/test_uci_retail_projection.py) and [integration fixtures](../../../tests/integration/test_uci_retail_projection_flow.py), created by tests in memory |
| Schema | `InvoiceNo`, `StockCode`, `Quantity`, `InvoiceDate` with deliberately extra `CustomerID`, `Description`, `UnitPrice`, `Country` fields in selected tests |
| Date window | Invented transaction timestamps in January 2011 for `SKU-A` / `SKU-B` |
| Invoice types | Fictional ordinary invoices (`536365` etc.) and cancellations prefixed `C` |
| Quantity semantics | Integer signed invoice-line quantities, **not** observed latent demand, available stock or causal business outcomes |
| Privacy boundary | Extra customer/description/price fields are not read or copied to `ProductDayUnits` or the receipt |
| Source rights | Not applicable to fabricated fixtures; the mere resemblance to UCI headers does **not** authorize the original dataset |
| Source publication time | **Unknown**. No `available_on` is generated from `InvoiceDate` |
| Stable line identity | None. Identical lines are intentionally not deduplicated; this may overcount true real-world sales if supplied by an unreviewed source |
| Output | Sorted positive invoice-line units per stock code and transaction day, plus excluded-row counters |

The [real UCI candidate review](UCI_ONLINE_RETAIL_SOURCE_REVIEW.md)
remains subject to license attribution, customer-identifier
handling, a trusted original file hash, bounded XLSX reading,
returns and duplicate policy, and a transparent model objective.

Read [the source walkthrough](../UCI_RETAIL_PROJECTION.md)
and [the change request](../changes/MM-M1B-uci-shaped-transaction-projection.md).
No empirical forecasting/model benchmark is claimed.
