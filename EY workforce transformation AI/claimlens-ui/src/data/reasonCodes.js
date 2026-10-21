// Standardised denial reason codes (dropdown in the Claim Review screen).
export const REASON_CODES = [
  { code: 'NCCI-PTP', label: 'NCCI-PTP: Procedure-to-Procedure unbundled pair violation' },
  { code: 'MUE-UNITS', label: 'MUE-UNITS: Medically Unlikely Edit max daily/line units exceeded' },
  { code: 'DUPLICATE', label: 'DUPLICATE: Exact duplicate service line on same DOS/Provider' },
  { code: 'DOC-INSUFFICIENT', label: 'DOC-INSUFFICIENT: Encounter note fails to document billed service' },
  { code: 'DX-MISMATCH', label: 'DX-MISMATCH: Diagnosis does not plausibly support procedure' },
  { code: 'EM-OVERCODED', label: 'EM-OVERCODED: E/M complexity billed exceeds documented visit' },
  { code: 'FEE-OUTLIER', label: 'FEE-OUTLIER: Charge exceeds 99th percentile of peer submissions' },
  { code: 'MOD-INVALID', label: 'MOD-INVALID: Missing or invalid NCCI/PFS modifier' },
];
