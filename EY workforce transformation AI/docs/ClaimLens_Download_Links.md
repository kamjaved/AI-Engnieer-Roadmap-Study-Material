# ClaimLens — Exact download links

How to read the status column:
- ✅ **Tested** = I requested the URL and it answered with the file (status 200 and the size shown).
- 📄 **From CMS page** = the URL was copied from the official CMS page this session, but my environment cannot reach cms.gov (it returned 403 to every cms.gov request), so I could not test it. A 403 from my side does not mean the link is broken. Click it once to confirm.
- ⚠️ = something to know before you click.

**Three things to know first**
1. **The two NCCI PTP links (and possibly others on cms.gov) open an AMA licence page first.** You click "Accept" once, then the file downloads. It is not literally one click. The MUE, ICD-10 and Policy Manual links did not show a licence step on their CMS pages.
2. **Do not `git clone` the milwaukeedata repo.** It holds 18 sample folders and is large. Download only the files you need from `1-sample-10000` using the links below.
3. **There is no single repo or page that has all of these files.** The milwaukeedata repo covers the DE-SynPUF claims only (Blueprint 1, item D1). Every other file comes from CMS.

---

## A. Simplified plan: the 5 downloads

| # | File | What it is | Direct link | Status |
|---|---|---|---|---|
| 1 | **CMS national utilization table** (13,463 rows, national level only) | Code list with descriptions, units, office/facility mix, typical charges | Page 1: https://data.cms.gov/data-api/v1/dataset/6fea9d79-0129-4e4c-b1b8-23cd86a4f435/data?size=5000&offset=0&filter[Rndrng_Prvdr_Geo_Lvl]=National <br> Page 2: change `offset=5000` <br> Page 3: change `offset=10000` | Filter and field names ✅ tested through a fetch tool (found_rows 13,463). `offset` paging ⚠️ not tested. Saves as JSON, not CSV. |
| 1b | *Backup for #1:* full 2023 CSV (all 268,350 rows; you filter `Rndrng_Prvdr_Geo_Lvl == "National"` in code) | Same data, larger file | https://data.cms.gov/sites/default/files/2025-04/3b718a11-a28d-4c38-a13b-2c6eeb649980/MUP_PHY_R25_P05_V20_D23_Geo.csv | 📄 file size not known |
| 2 | **NCCI PTP edits, practitioner, Q4 2026** (4 ZIPs, 2,637,645 rows total) | Code-pair rules | f1: https://www.cms.gov/license/ama?file=/files/zip/medicare-ncci-2026q4-practitioner-ptp-edits-ccipra-v323r0-f1.zip <br> f2: https://www.cms.gov/license/ama?file=/files/zip/medicare-ncci-2026q4-practitioner-ptp-edits-ccipra-v323r0-f2.zip <br> f3: https://www.cms.gov/license/ama?file=/files/zip/medicare-ncci-2026q4-practitioner-ptp-edits-ccipra-v323r0-f3.zip <br> f4: https://www.cms.gov/license/ama?file=/files/zip/medicare-ncci-2026q4-practitioner-ptp-edits-ccipra-v323r0-f4.zip | 📄 AMA licence click-through. Download all four. Inspect the contents before writing a parser (I have not opened them). |
| 3 | **NCCI MUE table, practitioner, Q4 2026** | Unit limits | https://www.cms.gov/files/zip/medicare-ncci-2026-q4-practitioner-services-mue-table.zip | 📄 |
| 4 | **ICD-10-CM 2027 code descriptions (tabular order)** | Valid diagnosis codes | https://www.cms.gov/files/zip/2027-code-descriptions-tabular-order.zip | 📄 |
| 5 | **NCCI Policy Manual 2026, all chapters (one PDF)** | The PO copies 15–30 passages from it | https://www.cms.gov/files/document/2026-ncci-medicare-policy-manual-all-chapters.pdf | 📄 |

---

## B. Blueprint 1: all 13 items (D1–D13)

### D1 — DE-SynPUF Sample 1 (8 files)

**Option 1 (recommended): the milwaukeedata GitHub repo.** Same file names as CMS, as plain CSV (no unzipping). All sizes match what GitHub reported.

| File | Direct link | Size | Status |
|---|---|---|---|
| Beneficiary summary 2008 | https://raw.githubusercontent.com/milwaukeedata/desynpuf/master/1-sample-10000/DE1_0_2008_Beneficiary_Summary_File_Sample_1.csv | 1.25 MB | ✅ |
| Beneficiary summary 2009 | https://raw.githubusercontent.com/milwaukeedata/desynpuf/master/1-sample-10000/DE1_0_2009_Beneficiary_Summary_File_Sample_1.csv | 1.25 MB | ✅ |
| Beneficiary summary 2010 | https://raw.githubusercontent.com/milwaukeedata/desynpuf/master/1-sample-10000/DE1_0_2010_Beneficiary_Summary_File_Sample_1.csv | 1.21 MB | ✅ |
| **Carrier claims 1A** | https://raw.githubusercontent.com/milwaukeedata/desynpuf/master/1-sample-10000/DE1_0_2008_to_2010_Carrier_Claims_Sample_1A.csv | 105 MB | ✅ (header line read: it is the DE-SynPUF carrier layout) |
| **Carrier claims 1B** | https://raw.githubusercontent.com/milwaukeedata/desynpuf/master/1-sample-10000/DE1_0_2008_to_2010_Carrier_Claims_Sample_1B.csv | 107 MB | ✅ |
| Inpatient claims | https://raw.githubusercontent.com/milwaukeedata/desynpuf/master/1-sample-10000/DE1_0_2008_to_2010_Inpatient_Claims_Sample_1.csv | 1.4 MB | ✅ |
| Outpatient claims | https://raw.githubusercontent.com/milwaukeedata/desynpuf/master/1-sample-10000/DE1_0_2008_to_2010_Outpatient_Claims_Sample_1.csv | 13.9 MB | ✅ |
| Prescription drug events | https://raw.githubusercontent.com/milwaukeedata/desynpuf/master/1-sample-10000/DE1_0_2008_to_2010_Prescription_Drug_Events_Sample_1.csv | 36 MB | ✅ |

⚠️ The repo's README is inconsistent about whether each sample has 10,000 or 20,000 patients, and it names the folder `sample-10000`. **I did not count rows**, so I cannot say whether it is the complete CMS Sample 1 or a subset. Run `wc -l` on the carrier files after downloading. The repo is a third-party copy, so use it for convenience only; the CMS originals below are the authority.

Download all 8 from a terminal (Git Bash / macOS / Linux):
```bash
mkdir -p data/raw/desynpuf && cd data/raw/desynpuf
B=https://raw.githubusercontent.com/milwaukeedata/desynpuf/master/1-sample-10000
for f in DE1_0_2008_Beneficiary_Summary_File_Sample_1.csv DE1_0_2009_Beneficiary_Summary_File_Sample_1.csv DE1_0_2010_Beneficiary_Summary_File_Sample_1.csv \
         DE1_0_2008_to_2010_Carrier_Claims_Sample_1A.csv DE1_0_2008_to_2010_Carrier_Claims_Sample_1B.csv \
         DE1_0_2008_to_2010_Inpatient_Claims_Sample_1.csv DE1_0_2008_to_2010_Outpatient_Claims_Sample_1.csv \
         DE1_0_2008_to_2010_Prescription_Drug_Events_Sample_1.csv; do curl -L -O "$B/$f"; done
```

**Option 2: the CMS originals (ZIP)** — 📄 from the CMS Sample 1 page
- Beneficiary 2008: https://www.cms.gov/research-statistics-data-and-systems/downloadable-public-use-files/synpufs/downloads/de1_0_2008_beneficiary_summary_file_sample_1.zip
- Beneficiary 2009: https://www.cms.gov/research-statistics-data-and-systems/downloadable-public-use-files/synpufs/downloads/de1_0_2009_beneficiary_summary_file_sample_1.zip
- Beneficiary 2010: https://www.cms.gov/research-statistics-data-and-systems/statistics-trends-and-reports/synpufs/downloads/de1_0_2010_beneficiary_summary_file_sample_20.zip ⚠️ the file name says `sample_20`; CMS lists it under Sample 1. Check it.
- Carrier 1A: http://downloads.cms.gov/files/DE1_0_2008_to_2010_Carrier_Claims_Sample_1A.zip
- Carrier 1B: http://downloads.cms.gov/files/DE1_0_2008_to_2010_Carrier_Claims_Sample_1B.zip
- Inpatient: https://www.cms.gov/research-statistics-data-and-systems/downloadable-public-use-files/synpufs/downloads/de1_0_2008_to_2010_inpatient_claims_sample_1.zip
- Outpatient: https://www.cms.gov/research-statistics-data-and-systems/downloadable-public-use-files/synpufs/downloads/de1_0_2008_to_2010_outpatient_claims_sample_1.zip
- Prescription drug events: http://downloads.cms.gov/files/DE1_0_2008_to_2010_Prescription_Drug_Events_Sample_1.zip

### D2–D13

| ID | File | Direct link | Status |
|---|---|---|---|
| D2 | DE-SynPUF Codebook (PDF) | https://www.cms.gov/files/document/de-10-codebook.pdf-0 <br> (also the User Document: https://www.cms.gov/research-statistics-data-and-systems/downloadable-public-use-files/synpufs/downloads/synpuf_dug.pdf) | 📄 |
| D3 | NCCI PTP practitioner, Q4 2026, 4 ZIPs | Same four links as table A, item 2 | 📄 AMA licence click-through |
| D4 | NCCI MUE practitioner, Q4 2026 | https://www.cms.gov/files/zip/medicare-ncci-2026-q4-practitioner-services-mue-table.zip | 📄 |
| D5 | PFS National Payment Amount File PFREV26D | https://www.cms.gov/files/zip/pfrev26d-posted-08-25-2026.zip <br> (detail page: https://www.cms.gov/medicare/payment/fee-schedules/physician/national-payment-amount-file/pfrev26d) | 📄 ⚠️ the page mentions QP and non-QP versions but lists only this one file. Open the ZIP and check what is inside before relying on the "-nonQP" assumption in the blueprint. |
| D6 | PFS Relative Value File RVU26D | https://www.cms.gov/files/zip/rvu26d-updated-08-26-2026.zip | 📄 |
| D7 | Physician & Other Practitioners — by Provider and Service | Page only (no direct file link found): https://data.cms.gov/provider-summary-by-type-of-service/medicare-physician-other-practitioners/medicare-physician-other-practitioners-by-provider-and-service | ⚠️ very large. **Use the national table (item 1 in table A) instead**; it gives the same per-code fields at national level. |
| D8 | ICD-10-CM 2027 code descriptions | https://www.cms.gov/files/zip/2027-code-descriptions-tabular-order.zip | 📄 |
| D9 | 2018 ICD-10-CM GEMs | https://www.cms.gov/medicare/coding/icd10/downloads/2018-icd-10-cm-general-equivalence-mappings.zip | 📄 |
| D10 | NCCI Policy Manual 2026 (one PDF) | https://www.cms.gov/files/document/2026-ncci-medicare-policy-manual-all-chapters.pdf | 📄 |
| D11 | MTSamples (Kaggle) | https://www.kaggle.com/datasets/tboyle10/medicaltranscriptions | ⚠️ not opened this session. Kaggle needs a free login to download `mtsamples.csv`. No login-free mirror found. |
| D12 | katanaml-org/invoices-donut-data-v1 (Hugging Face) | Page: https://huggingface.co/datasets/katanaml-org/invoices-donut-data-v1 <br> Files: `data/test-00000-of-00001-56af6bd5ff7eb34d.parquet` (10.4 MB), `data/train-00000-of-00001-a5c51039eab2980a.parquet` (167 MB), `data/validation-00000-of-00001-b8a5c4a6237baf25.parquet` (19.9 MB) | File names and sizes ✅ from the Hugging Face file listing. Download URL format would be `https://huggingface.co/datasets/katanaml-org/invoices-donut-data-v1/resolve/main/<path>`, ⚠️ not tested (my environment blocks that host). |
| D13 | Blank CMS-1500 form | **No downloadable file found.** The CMS 1500 page says the form is available but links no file: https://www.cms.gov/medicare/billing/electronicbillingeditrans/1500 | ⚠️ Only a layout reference; skip it. The simplified plan does not use it. |

**Not in Blueprint 1's D-list but used by the simplified plan:** the national utilization table (table A, item 1).

---

## C. What I could not verify
- Whether any cms.gov link works from your network. Open each once and confirm the file name.
- The contents and row counts of every file (I only read the header of Carrier 1A).
- Whether `offset` paging works on the CMS API (the filter and field names did work).
- Kaggle and Hugging Face download URLs.
- Whether EY's network blocks any of these hosts (GitHub raw, cms.gov, data.cms.gov, Hugging Face, Kaggle). Test all five hosts on the first day.

**Sources:** [milwaukeedata/desynpuf](https://github.com/milwaukeedata/desynpuf) · [CMS DE-SynPUF Sample 1](https://www.cms.gov/data-research/statistics-trends-and-reports/medicare-claims-synthetic-public-use-files/cms-2008-2010-data-entrepreneurs-synthetic-public-use-file-de-synpuf/de10-sample-1) · [CMS NCCI PTP edits](https://www.cms.gov/medicare/coding-billing/national-correct-coding-initiative-ncci-edits/medicare-ncci-procedure-procedure-ptp-edits) · [CMS NCCI MUEs](https://www.cms.gov/medicare/coding-billing/national-correct-coding-initiative-ncci-edits/medicare-ncci-medically-unlikely-edits) · [CMS NCCI Policy Manual](https://www.cms.gov/medicare/coding-billing/national-correct-coding-initiative-ncci-edits/medicare-ncci-policy-manual) · [CMS ICD-10 codes](https://www.cms.gov/medicare/coding-billing/icd-10-codes) · [CMS ICD-10 archive](https://www.cms.gov/medicare/coding-billing/icd-10-codes/icd-10-cm-icd-10-pcs-gem-archive) · [CMS RVU26D](https://www.cms.gov/medicare/payment/fee-schedules/physician/pfs-relative-value-files/rvu26d) · [CMS National Payment Amount File](https://www.cms.gov/medicare/payment/fee-schedules/physician/national-payment-amount-file) · [data.cms.gov Geography and Service](https://catalog.data.gov/dataset/medicare-physician-other-practitioners-by-geography-and-service) · [Hugging Face invoices dataset](https://huggingface.co/datasets/katanaml-org/invoices-donut-data-v1)
