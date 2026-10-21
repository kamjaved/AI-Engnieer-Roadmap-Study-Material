// Mock evaluation numbers shown on the Eval & KPIs screen.
// Replace with the output of `claimlens eval run --set gold_test` when the backend exists.

export const KPI_CARDS = [
  {
    label: 'Error Capture',
    value: '96.8%',
    valueClass: 'text-slate-900',
    sub: 'Target ≥ 95% ✓',
    subClass: 'text-emerald-600 font-medium',
  },
  {
    label: 'Examiner Focus',
    value: '49.2%',
    valueClass: 'text-slate-900',
    sub: '% GREEN (FN: 0.8%)',
    subClass: 'text-slate-500',
  },
  {
    label: '$ At Risk / 1K',
    value: '$184.4K',
    valueClass: 'text-indigo-600',
    sub: 'Synthetic dollars',
    subClass: 'text-slate-500',
  },
  {
    label: 'Latency p50/p95',
    value: '3.4s / 11.8s',
    valueClass: 'text-slate-900',
    sub: 'Target < 20.0s ✓',
    subClass: 'text-emerald-600 font-medium',
  },
  {
    label: 'Cost / Claim',
    value: '$0.0038',
    valueClass: 'text-slate-900',
    sub: 'Decision-1 + Memo',
    subClass: 'text-slate-500',
  },
  {
    label: 'Groundedness',
    value: '100% / 4.6★',
    valueClass: 'text-slate-900',
    sub: 'Target ≥ 4.0/5.0 ✓',
    subClass: 'text-emerald-600 font-medium',
  },
];

export const GOLD_SLICES = [
  {
    slice: 'CLEAN',
    sliceClass: 'text-emerald-700',
    description: 'Untouched clean synthetic claims (expect GREEN)',
    count: '400',
    precision: '0.992',
    recall: '0.995',
    override: '0.5%',
  },
  {
    slice: 'E1-NEG',
    sliceClass: 'text-emerald-700',
    description: 'PTP Ind 1 pair WITH valid modifier 59 (Negative control)',
    count: '100',
    precision: '1.000',
    recall: '1.000',
    override: '0.0%',
  },
  {
    slice: 'E1 + E1-HARD',
    sliceClass: 'text-rose-700',
    description: 'PTP pair missing mod OR Ind 0 with mod 59 (R1_PTP)',
    count: '100',
    precision: '1.000',
    recall: '1.000',
    override: '1.0%',
  },
  {
    slice: 'E2',
    sliceClass: 'text-rose-700',
    description: 'MUE units exceeded (single line MAI=1 & split-day MAI=2/3)',
    count: '100',
    precision: '1.000',
    recall: '0.990',
    override: '1.0%',
  },
  {
    slice: 'E3',
    sliceClass: 'text-rose-700',
    description: 'Duplicate line (same patient, code, DOS, rendering NPI)',
    count: '75',
    precision: '1.000',
    recall: '1.000',
    override: '0.0%',
  },
  {
    slice: 'E4',
    sliceClass: 'text-amber-700',
    description: 'Charge outlier 4–8x peer p99 (R3_FEE soft flag)',
    count: '75',
    precision: '0.946',
    recall: '0.960',
    override: '6.4%',
  },
  {
    slice: 'E5',
    sliceClass: 'text-indigo-700',
    description: 'Diagnosis mismatch (unrelated body system — Decision-1)',
    count: '75',
    precision: '0.892',
    recall: '0.906',
    override: '5.3%',
  },
  {
    slice: 'E6',
    sliceClass: 'text-indigo-700',
    description: 'Encounter note omits billed service (Decision-1)',
    count: '50',
    precision: '0.918',
    recall: '0.900',
    override: '4.0%',
  },
  {
    slice: 'E7',
    sliceClass: 'text-indigo-700',
    description: 'E/M over-coding (99215 billed on brief low-MDM note)',
    count: '25',
    precision: '0.880',
    recall: '0.880',
    override: '8.0%',
  },
];

export const CALIBRATION_BINS = [
  {
    bin: '0.1',
    pred: 10,
    emp: 12,
  },
  {
    bin: '0.3',
    pred: 30,
    emp: 28,
  },
  {
    bin: '0.5',
    pred: 50,
    emp: 47,
  },
  {
    bin: '0.7',
    pred: 70,
    emp: 73,
  },
  {
    bin: '0.9',
    pred: 90,
    emp: 89,
  },
];
