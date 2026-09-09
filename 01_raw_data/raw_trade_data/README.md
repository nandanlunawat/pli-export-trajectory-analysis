# raw_trade_data/

MEIDB responses, cached verbatim. **Never overwritten, never edited.**

Naming: `meidb_export_<HSLEVEL>_<YYYY>_<MM>_<CURRENCY>_<retrievalYYYYMMDD>.html`

Every file's contents are the raw server response. Parsing happens downstream in
`05_analysis/`; nothing in this folder is ever a parsed or corrected artefact.

Under the DGCI&S Dynamic Data Revision Policy every release restates prior months
of the current fiscal year, so a refresh RE-PULLS the whole window into a new
retrieval-dated set. Appending to an existing set is prohibited.

Expected size for the full build: ~300 requests across HS-4/6/8, roughly 1 GB.

EMPTY at design time. Populated only after checks C1 and C2 pass.
