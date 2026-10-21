import { Sliders } from 'lucide-react';
import { useClaimLens } from '../../context/useClaimLens';

/** Routing thresholds configuration (§3.4 F16, §8.2). */
export default function ThresholdConfig() {
  const { thresholds, setThresholds, triggerToast } = useClaimLens();

  return (
    <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-2xs space-y-4">
      <div className="flex items-center justify-between border-b border-slate-100 pb-3">
        <span className="text-xs font-bold uppercase tracking-wider text-slate-700 flex items-center gap-1.5">
          <Sliders className="w-4 h-4 text-indigo-600" /> Routing Thresholds (config/routing.yaml)
        </span>
        <span className="text-[11px] text-slate-400">Tuned on dev_set</span>
      </div>

      <div className="space-y-3 text-xs">
        <div className="flex justify-between items-center">
          <span className="text-slate-600 font-medium">CU Field Confidence Gate (HITL #1)</span>
          <input
            type="number"
            step="0.05"
            value={thresholds.fieldConfidence}
            onChange={(e) =>
              setThresholds({ ...thresholds, fieldConfidence: parseFloat(e.target.value) || 0.8 })
            }
            className="w-20 border border-slate-300 rounded-lg px-2.5 py-1 text-right font-mono font-bold"
          />
        </div>
        <div className="flex justify-between items-center">
          <span className="text-slate-600 font-medium">Decision-1 p(documented) RED Cutoff</span>
          <input
            type="number"
            step="0.05"
            value={thresholds.noteDocRed}
            onChange={(e) => setThresholds({ ...thresholds, noteDocRed: parseFloat(e.target.value) || 0.3 })}
            className="w-20 border border-slate-300 rounded-lg px-2.5 py-1 text-right font-mono font-bold"
          />
        </div>
        <div className="flex justify-between items-center">
          <span className="text-slate-600 font-medium">Decision-1 p(documented) GREEN Cutoff</span>
          <input
            type="number"
            step="0.05"
            value={thresholds.noteDocGreen}
            onChange={(e) =>
              setThresholds({ ...thresholds, noteDocGreen: parseFloat(e.target.value) || 0.7 })
            }
            className="w-20 border border-slate-300 rounded-lg px-2.5 py-1 text-right font-mono font-bold"
          />
        </div>
        <div className="flex justify-between items-center">
          <span className="text-slate-600 font-medium">R3 Fee Outlier Peer Percentile</span>
          <input
            type="number"
            value={thresholds.feeOutlierPercentile}
            onChange={(e) =>
              setThresholds({ ...thresholds, feeOutlierPercentile: parseInt(e.target.value, 10) || 99 })
            }
            className="w-20 border border-slate-300 rounded-lg px-2.5 py-1 text-right font-mono font-bold"
          />
        </div>
      </div>

      <button
        onClick={() => triggerToast('Updated config/routing.yaml thresholds (applied to worker routing).')}
        className="w-full py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold rounded-xl shadow-xs transition cursor-pointer"
      >
        Save Threshold Configuration
      </button>
    </div>
  );
}
