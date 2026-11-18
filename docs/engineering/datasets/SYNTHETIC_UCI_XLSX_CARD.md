# Invented XLSX fixtures for the offline UCI-shaped reader

**Classification:** synthetic, generated in memory or temporary
test directories. **No actual UCI workbook, customer record,
retailer invoice or downloaded source was used.**

| Property | Evidence and limits |
| --- | --- |
| Fixture construction | [Unit test builders](../../../tests/unit/test_uci_workbook.py) create minimal `openpyxl.Workbook` data in `BytesIO`; [integration test](../../../tests/integration/test_uci_workbook_flow.py) creates a temporary XLSX that is immediately consumed |
| Layout | Single `Online Retail` worksheet, exact eight UCI-style headers in the fixed expected order |
| Example source dates | Invented January 2011 naive transaction datetimes |
| Product code | `SKU-A` / `SKU-B`, invented identifiers |
| Customer IDs | Numerical **fictional** placeholder values included only to prove they do not appear in the projection |
| Amounts | Fictional integer quantities and arbitrary prices; neither revenue nor real demand can be inferred |
| Cancellations | Fictional `C` invoices and negative/zero quantities test exclusion counters |
| ZIP safety cases | Created malicious **test archives** with an external-link entry or highly compressed test part; not actual hostile customer files |
| Publication history | **Absent**: `InvoiceDate` is a transaction event and no `available_on` is assigned |
| Source license | No external license is needed for invented fixture values; the original [UCI source rights review](UCI_ONLINE_RETAIL_SOURCE_REVIEW.md) remains a separate prerequisite for actual data |
| Reproducibility | Deterministic source **content and expected counters**; binary XLSX byte hashes may vary with library/time metadata and are compared only within the same test execution |

The produced `UciWorkbookReadResult`
includes an in-memory product-day projection and a SHA-256
of the compressed input. A matching caller-supplied
hash demonstrates only byte equality; it does **not**
authenticate a producer, a data license or the underlying
customer rights.

Tests enforce resource guards and error handling on
small workbooks; they do not establish complete safety
against malicious XML/ZIP parsers, the ability to ingest
the full original 541,909-row file, accurate cancellation
reconciliation or empirical forecast quality.

Read [the source-method guide](../UCI_WORKBOOK_READER.md),
[change request](../changes/MM-M1B-bounded-uci-xlsx-reader.md)
and [full dataset card template](../DATASET_CARD_TEMPLATE.md).
