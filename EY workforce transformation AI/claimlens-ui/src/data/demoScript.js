// 8-step demo walkthrough shown in the jump bar.
export const DEMO_SCRIPT_STEPS = [
  {
    step: 1,
    title: '1. Queue & Problem',
    desc: 'Examiner queue sorted by Bucket & $ at risk',
    screen: 'queue',
  },
  {
    step: 2,
    title: '2. Bill PDF Verification',
    desc: 'Low-confidence unit OCR (<0.80) fixed by human',
    screen: 'verify',
    claimId: 'CLM-2026-00042',
  },
  {
    step: 3,
    title: '3. RED Claim (PTP Ind 0)',
    desc: 'Hard NCCI edit + RAG policy memo',
    screen: 'detail',
    claimId: 'CLM-2026-00104',
  },
  {
    step: 4,
    title: '4. AMBER Claim (Decision-1)',
    desc: 'Missing ECG in note + E/M overcoding probabilities',
    screen: 'detail',
    claimId: 'CLM-2026-00108',
  },
  {
    step: 5,
    title: '5. GREEN Negative Control',
    desc: 'Valid Mod 59 bypasses PTP Ind 1 (Precision test)',
    screen: 'detail',
    claimId: 'CLM-2026-00112',
  },
  {
    step: 6,
    title: '6. Prompt Injection Guardrail',
    desc: 'Red-team note blocked by Prompt Shields + R3 Fee',
    screen: 'detail',
    claimId: 'CLM-2026-00119',
  },
  {
    step: 7,
    title: '7. Four-Eyes Supervisor Sign-Off',
    desc: 'Supervisor confirms denial recommendation',
    screen: 'supervisor',
    claimId: 'CLM-2026-00089',
  },
  {
    step: 8,
    title: '8. Eval Report & Calibration',
    desc: 'Gold set P/R, ECE reliability plot & thresholds',
    screen: 'dashboard',
  },
];
