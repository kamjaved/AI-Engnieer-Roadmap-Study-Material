# ClaimLens Lite — mock data, layer by layer

*Written 22 Oct 2026 for the Simplified Plan ("Lite"). Companion to `ClaimLens_Simplified_Plan.md`.*

## 0. Read this first

- **What this is.** A small, realistic sample of the data at every layer: the 5 downloaded files, the human-curated inputs, the generated files, and the final PostgreSQL tables with 3 to 12 rows each.
- **It was actually run.** I wrote the build script, ran it on a local **PostgreSQL 16**, and pasted the real query output below. Rules R1 to R4 were executed against the tables; the findings, buckets and "dollars at risk" in the claims come from that run, not from my typing.
- **What is real and what is not.**

| Marker | Meaning |
|---|---|
| ✅ **Layout** | File layout and column names checked against a CMS page this session (PTP columns A to G, MUE four headers, ICD-10-CM order file positions, national table field names from the plan). |
| 🧪 **Illustrative values** | **Every number and most code pairs are invented to look plausible.** The utilization figures, charges, MUE values, MAI values, PTP indicators (except 29806/29822, which AAOS documents as indicator 1 since 2002-07-01) are **not CMS values**. Do not quote them. |
| ⚠️ **Placeholder text** | Policy snippets 2 and 4 are placeholders; the Policy Manual passages must be copied by your PO. I have not read the manual. |

- **The sample claims are 6 (not hundreds).** One per error slice: CLEAN, E1 (PTP), E2 (MUE), E3 (duplicate), E4 (fee outlier), E6 (note does not document a service).

---

## 1. The layers at a glance

```text
LAYER 0  RAW DOWNLOADS (5 files, never edited)
   1 national utilization (API JSON)   2 NCCI PTP (4 ZIPs)   3 NCCI MUE   4 ICD-10-CM order file   5 NCCI Policy Manual PDF
        |                                   |                    |              |                         |
        v                                   v                    v              v                         v
LAYER 1  HUMAN-CURATED INPUTS (small CSV files in git, reviewed by PO/QA)
   dx_map.csv (code -> plausible diagnoses, + mismatch list)   policy_snippets.csv (15-30 passages)   app_users.csv
        |
        v
LAYER 2  GENERATED FILES (`make data`, fixed seed, identical on every laptop)
   ref_code.csv  ref_ptp.csv  ref_mue.csv  ref_dx.csv  |  gold_test.jsonl  gold_labels.jsonl  gold_manifest.json (sha256)
        |
        v
LAYER 3  POSTGRESQL (9 tables from the plan + ref_dx + app_users)
   reference: ref_code ref_ptp ref_mue ref_dx policy_snippets app_users
   operational: claims claim_lines findings reviews audit_events
        |
        v
LAYER 4  RUNTIME OUTPUTS (written by the app while it runs)
   findings (R1-R4 + Decision-1)   memo   bucket + dollars at risk   reviews (examiner, supervisor)   audit_events
```

| Layer | Owner | Format | Size in the real project | How it is rebuilt |
|---|---|---|---|---|
| 0 | Dev 2 (once) | JSON, ZIP of txt/xlsx, CSV, fixed-width txt, PDF | National table 13,463 rows ✅; PTP is the largest file | Download again for a new quarter |
| 1 | PO + QA | CSV in git | ~300 dx_map rows, 15 to 30 snippets | Edit and review in pull requests |
| 2 | Dev 2 | CSV + JSONL | ~300 codes; 300 gold + 300 dev claims | `make data` (fixed seed) |
| 3 | Dev 3 | PostgreSQL | Hundreds of PTP rows after filtering; hundreds of claims | `make seed` (idempotent load) |
| 4 | The app | PostgreSQL rows | Grows with use | Not rebuilt; append-only audit |

**Hard rule:** labels (`gold_labels.jsonl`) are **never** loaded into PostgreSQL. The app must not be able to see the answer key.

---

## 2. Layer 0 — the five downloads, as they look

### 2.1 National utilization table (data.cms.gov API) → JSON

- **Where:** data.cms.gov API for "Medicare Physician & Other Practitioners – by Geography and Service", filter `Rndrng_Prvdr_Geo_Lvl=National`, page with `size` and `offset`. National level has 13,463 rows ✅ (plan). Dataset id: `<dataset-uuid>` (look it up in the catalog).
- **Format:** a JSON array, **every value is a string**, including numbers.
- **We keep:** office (`O`) and facility (`F`) rows only, codes that also appear in the MUE table, top ~300 by `Tot_Srvcs`.
- **Trap:** the data is the 2023 release ✅, so a code deleted since 2023 may be missing from the MUE table; the join to MUE drops it (that is intended).

Two records (of the 10 in the sample file) 🧪:

```json
[
  {
    "Rndrng_Prvdr_Geo_Lvl": "National",
    "HCPCS_Cd": "99213",
    "HCPCS_Desc": "Established patient office or other outpatient visit, low complexity",
    "Place_Of_Srvc": "O",
    "Tot_Srvcs": "118400000",
    "Tot_Bene_Day_Srvcs": "118100000",
    "Avg_Sbmtd_Chrg": "145.20",
    "Avg_Mdcr_Alowd_Amt": "88.10",
    "Avg_Mdcr_Pymt_Amt": "69.40"
  },
  {
    "Rndrng_Prvdr_Geo_Lvl": "National",
    "HCPCS_Cd": "29881",
    "HCPCS_Desc": "Knee arthroscopy with meniscectomy (medial or lateral)",
    "Place_Of_Srvc": "F",
    "Tot_Srvcs": "410000",
    "Tot_Bene_Day_Srvcs": "408000",
    "Avg_Sbmtd_Chrg": "2450.00",
    "Avg_Mdcr_Alowd_Amt": "578.00",
    "Avg_Mdcr_Pymt_Amt": "462.00"
  }
]
```

### 2.2 NCCI PTP, practitioner (4 ZIPs) → tab-delimited text or xlsx

- **Where:** CMS NCCI page, "Practitioner PTP Edits", quarterly (2026 Q4 files are effective 1 Oct 2026 ✅). Accept the licence prompt if shown.
- **Layout ✅ (CMS MLN):** Column A = Column 1 code, B = Column 2 code, C = "in existence before 1996" flag, D = effective date, E = deletion date, F = modifier indicator (0, 1, 9), G = rationale category.
- **Format traps:** a few **notes rows** above the real header; dates as `YYYYMMDD`; deletion date `*` when none; four files to concatenate; if it arrives only as `.xlsx`, convert once to CSV/Parquet and never re-read the xlsx.

Sample (tabs shown as `|`), 🧪 except the first row:

```
ILLUSTRATIVE LAYOUT - Practitioner PTP edits, effective 20261001
(notes rows - the real file has several explanatory rows here; inspect before parsing)

Column 1 | Column 2 | *=in existence prior to 1996 | Effective Date | Deletion Date *=no data | Modifier 0=not allowed 1=allowed 9=not applicable | PTP Edit Rationale
29806 | 29822 |  | 20020701 | * | 1 | Standards of medical / surgical practice
29881 | 29877 | * | 20120101 | * | 0 | Standards of medical / surgical practice
97140 | 97530 |  | 20200101 | * | 1 | Standards of medical / surgical practice
97110 | 97140 | * | 20050101 | 20240101 | 1 | Standards of medical / surgical practice
93000 | 36415 |  | 20180101 | * | 9 | Standards of medical / surgical practice
99214 | 99213 | * | 19960101 | * | 1 | Mutually exclusive procedures
27447 | 27486 |  | 20150101 | * | 1 | Standards of medical / surgical practice
```

### 2.3 NCCI MUE, practitioner → CSV/xlsx

- **Layout ✅ (CMS MLN), exact four headers:** `HCPCS/CPT Code`, `Practitioner Services MUE Values`, `MUE Adjudication Indicator (MAI)`, `MUE Rationale`. There is **no modifier column** and no date column in the table.
- **Trap:** the MAI arrives as **text with its label** ("3 Date of Service Edit: Clinical"), not a bare number. We take the first character.

```
ILLUSTRATIVE LAYOUT - Practitioner services MUE table, effective 20261001
HCPCS/CPT Code,Practitioner Services MUE Values,MUE Adjudication Indicator (MAI),MUE Rationale
99213,1,3 Date of Service Edit: Clinical,Clinical: Data
99214,1,3 Date of Service Edit: Clinical,Clinical: Data
97110,8,3 Date of Service Edit: Clinical,Clinical: Data
97140,4,3 Date of Service Edit: Clinical,Clinical: Data
97530,4,3 Date of Service Edit: Clinical,Clinical: Data
36415,3,1 Line Edit,Nature of Service/Procedure
93000,1,3 Date of Service Edit: Clinical,Code Descriptor / CPT Instruction
29881,1,2 Date of Service Edit: Policy,Anatomic Consideration
29877,1,2 Date of Service Edit: Policy,Anatomic Consideration
27447,1,2 Date of Service Edit: Policy,Anatomic Consideration
```

### 2.4 ICD-10-CM code descriptions (CMS/CDC "order file") → fixed-width text

- **Layout ✅ (CMS order-file layout):** order number columns 1-5; code 7-13 **without dot**; header flag column 15 (`0` = header, not valid for claims; `1` = valid); short description 17-76 (60 chars); long description from column 78. Lines are never longer than 400 characters.
- **Trap:** parse by **position**, not by splitting on spaces. Header rows (flag 0, e.g. `E11`) must not be accepted as diagnosis codes.

```
11231 E11     0 Type 2 diabetes mellitus                                     Type 2 diabetes mellitus
11245 E119    1 Type 2 diabetes mellitus without complications               Type 2 diabetes mellitus without complications
13902 H259    1 Unspecified age-related cataract                             Unspecified age-related cataract
14120 I10     1 Essential (primary) hypertension                             Essential (primary) hypertension
36511 M1711   1 Unilateral primary osteoarthritis, right knee                Unilateral primary osteoarthritis, right knee
36702 M23211  1 Derang ant horn medial mensc d/t old tear/inj, right knee    Derangement of anterior horn of medial meniscus due to old tear or injury, right knee
37104 M5450   1 Low back pain, unspecified                                   Low back pain, unspecified
```

### 2.5 NCCI Policy Manual (PDF) → no table at all

A PDF is **not parsed by code** in Lite. Your PO reads it and copies 15 to 30 passages into `policy_snippets.csv` (Layer 1), with chapter, section and page. That file is what the memo is allowed to cite.

---

## 3. Layer 1 — curated inputs (small, human-reviewed, in git)

### 3.1 `dx_map.csv` (also the E5 ground truth)

For each procedure code, 2 or 3 plausible diagnoses, plus a few deliberate **mismatches** for error type E5. The build **fails** if any code is missing from the ICD file or is not billable.

```csv
hcpcs_cd,icd10_code,role,reviewed_by,reviewed_on
99213,I10,supports,PO,2026-10-08
99213,E119,supports,PO,2026-10-08
99214,E119,supports,PO,2026-10-08
99214,I10,supports,PO,2026-10-08
97110,M5450,supports,PO,2026-10-08
97140,M5450,supports,PO,2026-10-08
97530,M1711,supports,PO,2026-10-08
29881,M23211,supports,PO,2026-10-08
29877,M23211,supports,PO,2026-10-08
29881,H259,mismatch,PO,2026-10-08
97140,H259,mismatch,PO,2026-10-08
36415,E119,supports,PO,2026-10-08
93000,I10,supports,PO,2026-10-08
```

### 3.2 `policy_snippets.csv`

```csv
id,rule_id,text,source_doc,manual_section,page,source_url
PS-R1-01,R1_PTP,"If a provider reports the two codes of an edit pair for the same beneficiary on the same date of service, the Column One code is eligible for payment, but the Column Two code is denied unless a modifier is reported where the modifier indicator allows it.",CMS web page: Medicare NCCI PTP edits,,,https://www.cms.gov/medicare/coding-billing/national-correct-coding-initiative-ncci-edits/medicare-ncci-procedure-procedure-ptp-edits
PS-R1-02,R1_PTP,Modifier indicator 0: no modifier can bypass the edit. Indicator 1: an NCCI-associated modifier may bypass it when the circumstances justify it. Indicator 9: the edit does not apply.,PLACEHOLDER - PO replaces with verbatim NCCI Policy Manual passage,TBD (Chapter I),TBD,
PS-R2-01,R2_MUE,An MUE is the maximum units of service reported for a HCPCS/CPT code on the vast majority of appropriately reported claims by the same provider for the same beneficiary on the same date of service.,CMS web page: Medicare NCCI Medically Unlikely Edits,,,https://www.cms.gov/medicare/coding-billing/national-correct-coding-initiative-ncci-edits/medicare-ncci-medically-unlikely-edits
PS-R4-01,R4_FEE,"Billed charges are normally above the Medicare payment amount, so a charge is compared with the average submitted charge for the same code, not with the Medicare fee schedule amount.","PLACEHOLDER - ClaimLens design note, not a CMS quote",,,
```

Snippet `PS-R1-01` and `PS-R2-01` are paraphrases of text from the CMS PTP and MUE web pages ✅. `PS-R1-02` and `PS-R4-01` are ⚠️ placeholders: your PO replaces them with verbatim manual passages and fills `manual_section` and `page`.

### 3.3 `app_users.csv` (dev login, Days 1 to 12)

```csv
name,role
Alex Rivera,Examiner
Dana Sterling,Supervisor
Priya Nair,Admin
```

---

## 4. Layer 2 — what the build produces

### 4.1 Build log (real output)

```
national rows in: 10  kept (O/F and in MUE): 10  distinct codes: 9
MUE rows kept (code in vocabulary): 9
PTP rows in: 7  kept (both codes in vocabulary): 5
dx_map rows: 13  all valid+billable; ref_dx rows: 6
```

Reading the log: 10 national rows kept (9 codes, 99213 appears as both `O` and `F`); 9 MUE rows kept (27447 dropped: not in the vocabulary); **PTP 7 rows in, 5 kept**. The two dropped PTP rows are `29806/29822` and `27447/27486`, because one of their codes is not in our vocabulary. The rule: **both codes must be in `ref_code`**, otherwise the E1 injector could not place the pair on a claim.

### 4.2 `ref_code.csv` (first rows)

```csv
code,place_of_srvc,description,tot_srvcs,tot_bene_day_srvcs,units_per_day,avg_sbmtd_chrg,avg_mdcr_alowd_amt,avg_mdcr_pymt_amt,source_release
99213,O,"Established patient office or other outpatient visit, low complexity",118400000,118100000,1.0,145.20,88.10,69.40,CMS-PUF-National-2023
99214,O,"Established patient office or other outpatient visit, moderate complexity",96000000,95800000,1.0,205.60,128.30,101.20,CMS-PUF-National-2023
97110,O,"Therapeutic exercises, each 15 minutes",31000000,10900000,2.84,85.40,29.10,23.00,CMS-PUF-National-2023
97140,O,"Manual therapy techniques, each 15 minutes",22500000,9300000,2.42,70.30,26.40,20.90,CMS-PUF-National-2023
```

`units_per_day` = `Tot_Srvcs` ÷ `Tot_Bene_Day_Srvcs`. For 97140 that is 22,500,000 ÷ 9,300,000 = **2.42 units a day** 🧪, which is what the generator samples around for clean claims.

### 4.3 `ref_ptp.csv`, `ref_mue.csv`, `ref_dx.csv`

```csv
column1,column2,effective_date,deletion_date,modifier_indicator,rationale,table_version
29881,29877,2012-01-01,,0,Standards of medical / surgical practice,NCCI-2026Q4
97140,97530,2020-01-01,,1,Standards of medical / surgical practice,NCCI-2026Q4
97110,97140,2005-01-01,2024-01-01,1,Standards of medical / surgical practice,NCCI-2026Q4
93000,36415,2018-01-01,,9,Standards of medical / surgical practice,NCCI-2026Q4
99214,99213,1996-01-01,,1,Mutually exclusive procedures,NCCI-2026Q4
```

```csv
code,mue_value,mai,rationale,table_version
99213,1,3,Clinical: Data,NCCI-2026Q4
99214,1,3,Clinical: Data,NCCI-2026Q4
97110,8,3,Clinical: Data,NCCI-2026Q4
97140,4,3,Clinical: Data,NCCI-2026Q4
97530,4,3,Clinical: Data,NCCI-2026Q4
36415,3,1,Nature of Service/Procedure,NCCI-2026Q4
93000,1,3,Code Descriptor / CPT Instruction,NCCI-2026Q4
29881,1,2,Anatomic Consideration,NCCI-2026Q4
29877,1,2,Anatomic Consideration,NCCI-2026Q4
```

```csv
code,short_desc,long_desc,billable,table_version
E119,Type 2 diabetes mellitus without complications,Type 2 diabetes mellitus without complications,True,ICD10CM-FY2027
H259,Unspecified age-related cataract,Unspecified age-related cataract,True,ICD10CM-FY2027
I10,Essential (primary) hypertension,Essential (primary) hypertension,True,ICD10CM-FY2027
M1711,"Unilateral primary osteoarthritis, right knee","Unilateral primary osteoarthritis, right knee",True,ICD10CM-FY2027
M23211,"Derang ant horn medial mensc d/t old tear/inj, right knee","Derangement of anterior horn of medial meniscus due to old tear or injury, right knee",True,ICD10CM-FY2027
M5450,"Low back pain, unspecified","Low back pain, unspecified",True,ICD10CM-FY2027
```

Notice `97110 / 97140` has a **deletion date of 2024-01-01**. It is in the table on purpose: a claim with a 2026 date of service must **not** be flagged by it (claim 103 below proves that).

### 4.4 The gold file: `gold_test.jsonl` (one claim per line, no answers inside)

Claim 102 (E1 slice) as stored:

```json
{
  "external_ref": "SYN-837P-000102",
  "patient": {
    "token": "SYN-PT-000977",
    "age": 64,
    "sex": "M"
  },
  "billing_npi": "1457392813",
  "dos_from": "2026-10-06",
  "dos_to": "2026-10-06",
  "lines": [
    {
      "line_no": 1,
      "dos": "2026-10-06",
      "place_of_service": "22",
      "code": "29881",
      "modifiers": [
        "RT"
      ],
      "units": 1,
      "charge": 2400.0,
      "dx_codes": [
        "M23211"
      ],
      "rendering_npi": "1245319599"
    },
    {
      "line_no": 2,
      "dos": "2026-10-06",
      "place_of_service": "22",
      "code": "29877",
      "modifiers": [
        "RT"
      ],
      "units": 1,
      "charge": 1150.0,
      "dx_codes": [
        "M23211"
      ],
      "rendering_npi": "1245319599"
    }
  ],
  "encounter_note": null
}
```

The NPIs are **valid** (they pass the Luhn check with prefix 80840 ✅). The patient is a token, never a real person.

### 4.5 `gold_labels.jsonl` (the answer key, kept outside the database)

```json
{"claim_ref": "SYN-837P-000101", "error_type": "CLEAN", "line_nos": [], "expected_check_id": null, "expected_flag": false}
{"claim_ref": "SYN-837P-000102", "error_type": "E1", "line_nos": [2], "expected_check_id": "R1_PTP", "expected_flag": true}
{"claim_ref": "SYN-837P-000103", "error_type": "E2", "line_nos": [2], "expected_check_id": "R2_MUE", "expected_flag": true}
{"claim_ref": "SYN-837P-000105", "error_type": "E3", "line_nos": [2], "expected_check_id": "R3_DUP", "expected_flag": true}
{"claim_ref": "SYN-837P-000106", "error_type": "E4", "line_nos": [1], "expected_check_id": "R4_FEE", "expected_flag": true}
{"claim_ref": "SYN-837P-000104", "error_type": "E6", "line_nos": [2], "expected_check_id": "AI_NOTE_DOC", "expected_flag": true}
```

### 4.6 `gold_manifest.json` (freeze record)

```json
{
  "file": "gold_test.jsonl",
  "claims": 6,
  "seed": 20261008,
  "table_version": "NCCI-2026Q4",
  "frozen_on": "2026-10-08 (Day 6)",
  "sha256": "a335bc82ff113b30c92fe01abbf27c645953ede02d7ec239b85ad3f820556f32"
}
```

On Day 6 the team freezes the file, records the SHA-256, and **never tunes on it**. The real project has 300 gold claims and a second 300-claim dev set with a different seed.

### 4.7 How each error slice is made (the six in this sample)

| Slice | Injector action | Sample claim | What the rules/AI should do |
|---|---|---|---|
| CLEAN | Nothing; rejected if it trips any rule | 101 | GREEN |
| E1 | Add the Column 2 code of an active PTP pair on the same date | 102 | R1 flags line 2 |
| E2 | Units above the MUE | 103 | R2 flags line 2 |
| E3 | Copy a line | 105 | R3 flags the copy |
| E4 | Multiply a charge by 4 to 8× (here 6×) | 106 | R4 soft flag |
| E6 | Note that omits a billed service | 104 | Decision-1 `note_documents_all_services` low |

---

## 5. Layer 3 — the final PostgreSQL tables

Schema file: `layer3_postgres/schema.sql`. Row counts after the load:

```
        t        | count 
-----------------+-------
 ref_code        |    10
 ref_ptp         |     5
 ref_mue         |     9
 ref_dx          |     6
 policy_snippets |     4
 app_users       |     3
 claims          |     6
 claim_lines     |    11
 findings        |    12
 reviews         |     3
 audit_events    |    33
(11 rows)
```

Short IDs below (8 characters) are the first part of a UUID; the database stores the full value.

### 5.1 `ref_code`  (10 rows, 3 shown)
```
 code  | pos |              description               | tot_srvcs | upd  |  sbmtd  | allowed 
-------+-----+----------------------------------------+-----------+------+---------+---------
 29881 | F   | Knee arthroscopy with meniscectomy (me |    410000 | 1.00 | 2450.00 |  578.00
 97140 | O   | Manual therapy techniques, each 15 min |  22500000 | 2.42 |   70.30 |   26.40
 99213 | O   | Established patient office or other ou | 118400000 | 1.00 |  145.20 |   88.10
(3 rows)
```
Primary key `(code, place_of_srvc)`. `avg_sbmtd_chrg` is the baseline for rule R4.

### 5.2 `ref_ptp`  (5 rows, all shown)
```
 col1  | col2  |    eff     |    del     | ind |            rationale             | table_version 
-------+-------+------------+------------+-----+----------------------------------+---------------
 29881 | 29877 | 2012-01-01 |            | 0   | Standards of medical / surgical  | NCCI-2026Q4
 93000 | 36415 | 2018-01-01 |            | 9   | Standards of medical / surgical  | NCCI-2026Q4
 97110 | 97140 | 2005-01-01 | 2024-01-01 | 1   | Standards of medical / surgical  | NCCI-2026Q4
 97140 | 97530 | 2020-01-01 |            | 1   | Standards of medical / surgical  | NCCI-2026Q4
 99214 | 99213 | 1996-01-01 |            | 1   | Mutually exclusive procedures    | NCCI-2026Q4
(5 rows)
```
Empty `del` = still active (`deletion_date IS NULL`). `table_version` ties every finding to the quarter that produced it.

### 5.3 `ref_mue`  (9 rows, 3 shown)
```
 code  | mue_value | mai |       rationale        | table_version 
-------+-----------+-----+------------------------+---------------
 29881 |         1 |   2 | Anatomic Consideration | NCCI-2026Q4
 97140 |         4 |   3 | Clinical: Data         | NCCI-2026Q4
 99213 |         1 |   3 | Clinical: Data         | NCCI-2026Q4
(3 rows)
```

### 5.4 `ref_dx`  (6 rows, 3 shown)  — *addition to the plan, see section 8*
```
  code  |                    short_desc                    | billable | table_version  
--------+--------------------------------------------------+----------+----------------
 E119   | Type 2 diabetes mellitus without complications   | t        | ICD10CM-FY2027
 H259   | Unspecified age-related cataract                 | t        | ICD10CM-FY2027
 M23211 | Derang ant horn medial mensc d/t old tear/inj, r | t        | ICD10CM-FY2027
(3 rows)
```

### 5.5 `policy_snippets`  (4 rows, 3 shown)
```
    id    | rule_id |                                   text                                    |             source_doc             |      sect       | page 
----------+---------+---------------------------------------------------------------------------+------------------------------------+-----------------+------
 PS-R1-01 | R1_PTP  | If a provider reports the two codes of an edit pair for the same benef... | CMS web page: Medicare NCCI PTP ed |                 | 
 PS-R1-02 | R1_PTP  | Modifier indicator 0: no modifier can bypass the edit. Indicator 1: an... | PLACEHOLDER - PO replaces with ver | TBD (Chapter I) | TBD
 PS-R2-01 | R2_MUE  | An MUE is the maximum units of service reported for a HCPCS/CPT code o... | CMS web page: Medicare NCCI Medica |                 | 
(3 rows)
```

### 5.6 `app_users`  (3 rows)  — *addition to the plan*
```
    id    |     name      |    role    
----------+---------------+------------
 a17c609d | Priya Nair    | Admin
 db50b92a | Alex Rivera   | Examiner
 2bc2ef1d | Dana Sterling | Supervisor
(3 rows)
```

### 5.7 `claims`  (6 rows)
```
    id    |  external_ref   |      status      | bucket |  risk   |  total  | patient_token | billing_npi |  dos_from  | has_note | has_memo | syn 
----------+-----------------+------------------+--------+---------+---------+---------------+-------------+------------+----------+----------+-----
 b0590f62 | SYN-837P-000101 | APPROVED         | GREEN  |    0.00 |  212.00 | SYN-PT-000412 | 1457392813  | 2026-10-05 | t        | t        | t
 70a53c1e | SYN-837P-000102 | DENIAL_CONFIRMED | RED    | 1150.00 | 3550.00 | SYN-PT-000977 | 1457392813  | 2026-10-06 | f        | t        | t
 4d93bc4a | SYN-837P-000103 | READY_FOR_REVIEW | RED    |  544.00 |  796.00 | SYN-PT-001203 | 1457392813  | 2026-10-07 | f        | t        | t
 72ed00cc | SYN-837P-000104 | READY_FOR_REVIEW | AMBER  |   45.00 |  250.00 | SYN-PT-000731 | 1457392813  | 2026-10-08 | t        | t        | t
 96b3400b | SYN-837P-000105 | READY_FOR_REVIEW | RED    |   92.00 |  184.00 | SYN-PT-000208 | 1457392813  | 2026-10-09 | f        | t        | t
 e0e58069 | SYN-837P-000106 | READY_FOR_REVIEW | AMBER  |  870.00 |  870.00 | SYN-PT-000555 | 1457392813  | 2026-10-09 | f        | t        | t
(6 rows)
```

One row in full (claim 102, expanded). Note `raw_payload` (the claim exactly as received), `memo` (JSON), `trace_id`, and `synthetic = t`:

```
-[ RECORD 1 ]---+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
id              | 70a53c1e-4902-576a-8fa2-55b94433a266
external_ref    | SYN-837P-000102
source          | json
status          | DENIAL_CONFIRMED
bucket          | RED
dollars_at_risk | 1150.00
patient_token   | SYN-PT-000977
patient_age     | 64
patient_sex     | M
billing_npi     | 1457392813
dos_from        | 2026-10-06
dos_to          | 2026-10-06
total_charge    | 3550.00
raw_payload     | {"lines": [{"dos": "2026-10-06", "code": "29881", "units": 1, "charge": 2400.0, "line_no": 1, "dx_codes": ["M23211"], "modifiers": ["RT"], "rendering_npi": "1245319599", "place_of_service": "22"}, {"dos": "2026-10-06", "code": "29877", "units": 1, "charge": 1150.0, "line_no": 2, "dx_codes": ["M23211"], "modifiers": ["RT"], "rendering_npi": "1245319599", "place_of_service": "22"}], "dos_to": "2026-10-06", "patient": {"age": 64, "sex": "M", "token": "SYN-PT-000977"}, "dos_from": "2026-10-06", "billing_npi": "1457392813", "external_ref": "SYN-837P-000102", "encounter_note": null}
encounter_note  | 
memo            | {"summary": "Line 2 (29877) is the Column 2 code of a PTP pair with line 1 (29881). The edit has modifier indicator 0, so the RT modifier cannot bypass it.", "citations": ["PS-R1-01", "PS-R1-02"], "prompt_version": "memo-lite-v1", "model_deployment": "chat-claimlens", "suggested_action": "recommend_denial"}
trace_id        | 1673cc4ee48d9e7ba8d547786f608756
synthetic       | t
created_at      | 2026-10-12 08:22:00+00
updated_at      | 2026-10-12 10:25:00+00
```

### 5.8 `claim_lines`  (11 rows)
```
  claim   | ln |    dos     | pos | code  | modifiers | units | charge  | dx_codes | rendering_npi 
----------+----+------------+-----+-------+-----------+-------+---------+----------+---------------
 4d93bc4a |  1 | 2026-10-07 | 11  | 97110 | {}        |     3 |  252.00 | {M5450}  | 1245319599
 4d93bc4a |  2 | 2026-10-07 | 11  | 97140 | {}        |     8 |  544.00 | {M5450}  | 1245319599
 70a53c1e |  1 | 2026-10-06 | 22  | 29881 | {RT}      |     1 | 2400.00 | {M23211} | 1245319599
 70a53c1e |  2 | 2026-10-06 | 22  | 29877 | {RT}      |     1 | 1150.00 | {M23211} | 1245319599
 72ed00cc |  1 | 2026-10-08 | 11  | 99214 | {}        |     1 |  205.00 | {I10}    | 1245319599
 72ed00cc |  2 | 2026-10-08 | 11  | 93000 | {}        |     1 |   45.00 | {I10}    | 1245319599
 96b3400b |  1 | 2026-10-09 | 11  | 97530 | {}        |     1 |   92.00 | {M1711}  | 1245319599
 96b3400b |  2 | 2026-10-09 | 11  | 97530 | {}        |     1 |   92.00 | {M1711}  | 1245319599
 b0590f62 |  1 | 2026-10-05 | 11  | 99214 | {}        |     1 |  198.00 | {E119}   | 1245319599
 b0590f62 |  2 | 2026-10-05 | 11  | 36415 | {}        |     1 |   14.00 | {E119}   | 1245319599
 e0e58069 |  1 | 2026-10-09 | 11  | 99213 | {}        |     1 |  870.00 | {I10}    | 1245319599
(11 rows)
```

### 5.9 `findings`  (12 rows, the 6 that matter shown)
```
    id    |  claim   |  check_id   | sev  | line_nos |          tv           |                                        details                                         
----------+----------+-------------+------+----------+-----------------------+----------------------------------------------------------------------------------------
 3eb146f6 | b0590f62 | AI_NOTE_DOC | INFO | {1,2}    |                       | {"p_true": 0.93, "p_false": 0.07, "question": "note_documents_all_services", "uncertai
 0e05b481 | 70a53c1e | R1_PTP      | HARD | {2}      | NCCI-2026Q4           | {"why": "indicator 0: no modifier can bypass", "column1": "29881", "column2": "29877",
 1ed5a99b | 4d93bc4a | R2_MUE      | HARD | {2}      | NCCI-2026Q4           | {"mai": 3, "code": "97140", "mue_value": 4, "units_summed": 8}
 fddc2bda | 72ed00cc | AI_NOTE_DOC | SOFT | {2}      |                       | {"p_true": 0.41, "p_false": 0.59, "question": "note_documents_all_services", "uncertai
 eba06073 | 96b3400b | R3_DUP      | HARD | {2}      |                       | {"key": ["97530", "2026-10-09", "1245319599", "()"], "duplicate_of_line": 1}
 bc26f65d | e0e58069 | R4_FEE      | SOFT | {1}      | CMS-PUF-National-2023 | {"k": 3.0, "avg_sbmtd_chrg": 145.2, "charge_per_unit": 870.0}
(6 rows)
```

One rule finding in full (R1 on claim 102):

```
-[ RECORD 1 ]--------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
id                   | 0e05b481-3505-5380-9ce1-c1f1515c054c
claim_id             | 70a53c1e-4902-576a-8fa2-55b94433a266
line_nos             | {2}
check_id             | R1_PTP
check_type           | RULE
severity             | HARD
details              | {"why": "indicator 0: no modifier can bypass", "column1": "29881", "column2": "29877", "deletion_date": null, "effective_date": "2012-01-01", "modifiers_seen": ["RT", "RT"], "modifier_indicator": "0"}
table_version        | NCCI-2026Q4
model_deployment     | 
question_set_version | 
created_at           | 2026-10-12 08:22:21+00
```

One AI finding in full (Decision-1 on claim 104). In the real project these numbers come from the model; **here they are mock values**:

```
-[ RECORD 1 ]--------+-----------------------------------------------------------------------------------------------------
check_id             | AI_NOTE_DOC
severity             | SOFT
line_nos             | {2}
details              | {"p_true": 0.41, "p_false": 0.59, "question": "note_documents_all_services", "uncertain_band": true}
model_deployment     | decision1-claimlens
question_set_version | qset-lite-v1
```

### 5.10 `reviews`  (3 rows)
```
    id    |  claim   |    role    |      action      |  reason  |                       comment                        |       created_at       
----------+----------+------------+------------------+----------+------------------------------------------------------+------------------------
 ad886f2b | b0590f62 | Examiner   | APPROVE          |          | No findings. GREEN claim, approved.                  | 2026-10-12 08:40:00+00
 42bb903d | 70a53c1e | Examiner   | RECOMMEND_DENIAL | NCCI-PTP | Line 2 is Column 2 of an indicator-0 pair with line  | 2026-10-12 08:52:00+00
 eb4af293 | 70a53c1e | Supervisor | CONFIRM_DENIAL   | NCCI-PTP | Confirmed. Pair verified in table NCCI-2026Q4.       | 2026-10-12 09:57:00+00
(3 rows)
```

### 5.11 `audit_events`  (33 rows, claim 102 shown)
```
 id |  claim   |     actor     |       event_type        |        model        |    prompt    |     tv      |       at       
----+----------+---------------+-------------------------+---------------------+--------------+-------------+----------------
  6 | 70a53c1e | system        | CLAIM_RECEIVED          |                     |              |             | 10-12 08:22:00
  7 | 70a53c1e | system        | RULES_RUN               |                     |              | NCCI-2026Q4 | 10-12 08:22:20
  8 | 70a53c1e | system        | DECISION1_SCORED        | decision1-claimlens | qset-lite-v1 |             | 10-12 08:22:24
  9 | 70a53c1e | system        | BUCKETED                |                     |              |             | 10-12 08:22:26
 10 | 70a53c1e | system        | MEMO_GENERATED          | chat-claimlens      | memo-lite-v1 |             | 10-12 08:22:40
 32 | 70a53c1e | Alex Rivera   | REVIEW_RECOMMEND_DENIAL |                     |              |             | 10-12 08:52:00
 33 | 70a53c1e | Dana Sterling | REVIEW_CONFIRM_DENIAL   |                     |              |             | 10-12 09:57:00
(7 rows)
```

Plain append-only table: the app role gets INSERT and SELECT only (no UPDATE or DELETE). Lite has no hash chain.

---

## 6. Layer 4 — what the run did to the six claims

| Claim | Slice | What happened | Bucket | At risk |
|---|---|---|---|---|
| 101 | CLEAN | No rule hit. Note check p = 0.93 (INFO). Examiner approved. | GREEN | $0.00 |
| 102 | E1 | R1: `29881` → `29877` is an **indicator 0** pair, so `RT` does not bypass. Examiner recommended denial, supervisor (a different person) confirmed. | RED | $1,150.00 |
| 103 | E2 | R2: 97140 has **8 units**, MUE is 4 (MAI 3). The pair `97110/97140` was **not** flagged because its deletion date (2024-01-01) is before the date of service. | RED | $544.00 |
| 104 | E6 | No rule hit. Decision-1 `p(documented) = 0.41`: top option 0.59 is below 0.60, so it is in the **uncertain band**. | AMBER | $45.00 |
| 105 | E3 | R3: line 2 duplicates line 1. | RED | $92.00 |
| 106 | E4 | R4: $870.00 vs average $145.20 (6×, threshold 3×). Soft flag. | AMBER | $870.00 |

**The queue query** (RED first, then AMBER, by dollars at risk) for claims waiting for review:

```
  external_ref   | bucket | dollars_at_risk |      status      
-----------------+--------+-----------------+------------------
 SYN-837P-000103 | RED    |          544.00 | READY_FOR_REVIEW
 SYN-837P-000105 | RED    |           92.00 | READY_FOR_REVIEW
 SYN-837P-000106 | AMBER  |          870.00 | READY_FOR_REVIEW
 SYN-837P-000104 | AMBER  |           45.00 | READY_FOR_REVIEW
(4 rows)
```

**Four-eyes proof** (the two actions on claim 102 come from two different users and roles):

```
      action      |     name      | actor_role 
------------------+---------------+------------
 RECOMMEND_DENIAL | Alex Rivera   | Examiner
 CONFIRM_DENIAL   | Dana Sterling | Supervisor
(2 rows)
```

---

## 7. One fact, traced from download to decision

```text
CMS PTP file row   29881 | 29877 | * | 20120101 | * | 0 | ...        (Layer 0, illustrative)
  -> filter: both codes in vocabulary                                  (Layer 2 build)
  -> ref_ptp row  (29881, 29877, 2012-01-01, NULL, '0', NCCI-2026Q4)   (Layer 3)
  -> claim 102 has lines 29881 and 29877 on 2026-10-06                 (gold_test.jsonl -> claims)
  -> R1 joins the pair, date 2012-01-01 <= DOS < no deletion           (rule run)
  -> finding R1_PTP, HARD, details = the matched row, table_version    (findings)
  -> bucket RED, at risk $1,150.00                                     (claims)
  -> memo cites PS-R1-01 and PS-R1-02                                  (claims.memo)
  -> examiner RECOMMEND_DENIAL (NCCI-PTP) -> supervisor CONFIRM_DENIAL (reviews + audit_events)
```

Every arrow is a row you can query, which is what makes the denial memo defensible.

---

## 8. What building this sample exposed (decisions for the team)

| # | Finding | Why it matters | Suggested resolution |
|---|---|---|---|
| 1 | The plan's 9 tables have **no home for ICD-10 descriptions**, but Decision-1 needs `dx_desc`. | Without it the AI input is missing text. | Add the tiny `ref_dx` table (built from `dx_map` × ICD file). |
| 2 | The plan puts the memo "on findings", but a memo is **per claim**. | Duplicating it across findings invites inconsistency. | Store it as `claims.memo` (used here). Your call. |
| 3 | The dev login needs **seeded users**, which are not in the 9 tables. | Four-eyes needs two distinct actor IDs. | Add `app_users` (used here), or a config file. |
| 4 | **Rule numbering differs.** Blueprint 1: R3 = fee outlier, R4 = duplicate. Lite: **R3 = duplicate, R4 = fee outlier**. | Mixed numbering breaks tests, reason codes and the UI prototype. | Pick one scheme now and rename in code and docs. |
| 5 | The plan says "SQLite fallback, avoid Postgres-only features", but this schema uses `text[]`, `jsonb`, `uuid`. | The fallback will not run this DDL. | Either drop the SQLite fallback, or store arrays/JSON as JSON text and uuid as text. Decide on Day 1. |
| 6 | **Most NPIs in the React prototype fail the Luhn check.** Of 8 distinct NPIs in its mock claims, only 2 pass (`1245319599`, `1679543219`); `1234567890` is the deliberate bad one. | A real validator would reject claims 00104, 00089, 00108 and 00119 on arrival, and claim 00042 has one failing NPI (`1982654328`). | Generate NPIs with the prefix-80840 Luhn rule (the build script has `make_npi`). |
| 7 | Rules R1/R2 will score ~100% on this gold set by construction (the injector and the rules read the same tables). | The plan already warns about this (§3.5). | Report false-positive rate and Decision-1 accuracy instead. |
| 8 | `dollars_at_risk` = sum of charges on flagged lines (Blueprint rule). For E2 this counts the **whole** 97140 line ($544), not just the excess units. | It overstates the amount at risk. | Keep for the demo; note it. A tighter rule could price only units above the MUE. |
| 9 | Time zones: timestamps are stored `timestamptz` in UTC. | The UI must convert to local time. | Convert only in the UI. |
| 10 | The R4 threshold (`k = 3`) is **my assumption**; the plan only says "compare to `Avg_Sbmtd_Chrg`". | E4 multiplies by 4 to 8×, so 3× catches it, but false positives on legitimate high charges are possible. | Make `k` a config value; tune on the dev set, not on gold. |

---

## 9. Re-run it yourself

The folder `claimlens_lite_sample/` (zip) contains the raw files, curated files, generated files, schema, both scripts and the saved psql output.

```bash
# needs a PostgreSQL 14+ server you can create a database on
uv init sample && cd sample && uv add "psycopg[binary]"
export CLAIMLENS_ADMIN_DSN="host=localhost user=postgres dbname=postgres"
export CLAIMLENS_DSN="host=localhost user=postgres dbname=claimlens_lite"
uv run python tools/build_all.py      # raw -> generated -> PostgreSQL, runs R1-R4
uv run python tools/dump.py           # re-creates the query outputs shown above
```

The scripts drop and recreate the database `claimlens_lite`, so run them against a throw-away server.

---

## Sources for the layouts

- CMS, [How to use the Medicare NCCI, chapter 2](https://www.cms.gov/Outreach-and-Education/MLN/Educational-Tools/MLN901346-How-to-use-the-Medicare-NCCI/ncci-medicare/chapter_2_using_the_ncci_tools/) (PTP columns A to G; MUE table's four headers)
- CMS, [ICD-10-CM/PCS order files layout](https://www.cms.gov/files/document/icd-10-cm-pcs-order-files-fy17-pdf.pdf) (fixed-width positions)
- CMS, [Medicare NCCI PTP edits](https://www.cms.gov/medicare/coding-billing/national-correct-coding-initiative-ncci-edits/medicare-ncci-procedure-procedure-ptp-edits) and [MUE](https://www.cms.gov/medicare/coding-billing/national-correct-coding-initiative-ncci-edits/medicare-ncci-medically-unlikely-edits) pages (definitions, quarterly files)
- AAOS, [What is NCCI PTP](https://www.aaos.org/globalassets/quality-and-practice-resources/coding-and-reimbursement/resident-guide/resident-guide-coding-reference-tools_what-is-ncci-ptp.pdf) (29806/29822, indicator 1)
- John D. Cook, [NPI and its checksum](https://www.johndcook.com/blog/2024/06/26/npi-number/)
- `ClaimLens_Simplified_Plan.md` §3 to §5 (national table fields and counts, generator steps, table list)
