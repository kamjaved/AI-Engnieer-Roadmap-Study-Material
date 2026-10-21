import { XCircle } from 'lucide-react';
import { useClaimLens } from '../../context/useClaimLens';

/** Shown only for claims rejected at the format-validation step. */
export default function ValidationErrorsBanner() {
  const { selectedClaim } = useClaimLens();

  if (!(selectedClaim.status === 'REJECTED_INVALID' && selectedClaim.validation_errors)) return null;

  return (
    <div className="bg-slate-900 text-white rounded-2xl p-5 space-y-2.5 text-xs shadow-sm">
      <div className="font-bold text-rose-400 flex items-center gap-2 text-sm">
        <XCircle className="w-5 h-5 text-rose-400" />
        Step 2 Hard Format Validation Rejection (Rejected Before Rules / AI)
      </div>
      <ul className="list-disc pl-5 space-y-1 text-slate-200 font-mono">
        {selectedClaim.validation_errors.map((err, i) => (
          <li key={i}>{err}</li>
        ))}
      </ul>
    </div>
  );
}
