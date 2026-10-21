// Pipeline state order (used for the status stepper).
export const STATE_MACHINE_ORDER = [
  'RECEIVED',
  'EXTRACTING',
  'NEEDS_FIELD_VERIFICATION',
  'VALIDATING',
  'RULE_CHECKING',
  'AI_SCORING',
  'EXPLAINING',
  'READY_FOR_REVIEW',
  'DENIAL_RECOMMENDED',
  'DENIAL_CONFIRMED',
];
