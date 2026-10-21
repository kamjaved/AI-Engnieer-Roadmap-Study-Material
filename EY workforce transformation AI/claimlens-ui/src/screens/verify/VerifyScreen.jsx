import { AlertTriangle } from 'lucide-react';
import { useClaimLens } from '../../context/useClaimLens';
import StatusBadge from '../../components/common/StatusBadge';
import ScannedFormPreview from './ScannedFormPreview';
import ExtractedFieldsInspector from './ExtractedFieldsInspector';

/** Field verification (§3.5 #4, F4, F17 - HITL Point #1). */
export default function VerifyScreen() {
  const { thresholds } = useClaimLens();

  return (
    <div className="max-w-7xl mx-auto space-y-5">
      <div className="bg-amber-50 border border-amber-200 rounded-2xl p-4 flex flex-wrap items-center justify-between gap-4 shadow-2xs">
        <div className="flex items-start gap-3">
          <div className="p-2 rounded-xl bg-amber-100 text-amber-700 mt-0.5">
            <AlertTriangle className="w-5 h-5 shrink-0" />
          </div>
          <div>
            <div className="text-xs font-bold uppercase tracking-wider text-amber-900">
              Human Approval Point #1 — Low-Confidence Extraction Gate (Threshold &lt;{' '}
              {thresholds.fieldConfidence.toFixed(2)})
            </div>
            <div className="text-xs text-amber-800 mt-0.5 leading-relaxed">
              Azure Content Understanding analyzer{' '}
              <code className="font-mono bg-white/80 px-1.5 py-0.5 rounded">claimlens-cms1500</code> extracted
              Box 24G <code className="font-mono font-bold">units = 8</code> with confidence{' '}
              <strong>0.64</strong>. Verify against the scanned bill bounding box before rules execute.
            </div>
          </div>
        </div>
        <StatusBadge status="NEEDS_FIELD_VERIFICATION" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <ScannedFormPreview />
        <ExtractedFieldsInspector />
      </div>
    </div>
  );
}
