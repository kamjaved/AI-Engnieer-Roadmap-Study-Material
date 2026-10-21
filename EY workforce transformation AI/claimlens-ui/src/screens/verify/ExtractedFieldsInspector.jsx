import { AlertTriangle, CheckCircle2 } from 'lucide-react';
import { useClaimLens } from '../../context/useClaimLens';

/** Right pane: editable extracted fields with confidence scores. */
export default function ExtractedFieldsInspector() {
  const {
    selectedClaim,
    verifyNpiInput,
    setVerifyNpiInput,
    verifyUnitsInput,
    setVerifyUnitsInput,
    simulateStaleVersion,
    setSimulateStaleVersion,
    handleCompleteVerification,
  } = useClaimLens();

  return (
    <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-2xs flex flex-col justify-between space-y-5">
      <div className="space-y-4">
        <div className="flex items-center justify-between border-b border-slate-100 pb-3">
          <span className="text-xs font-bold text-slate-800">
            Extracted Fields Inspector (
            <code className="font-mono text-indigo-600">PATCH /claims/{selectedClaim.id}/fields</code>)
          </span>
          <span className="text-xs font-mono px-2.5 py-0.5 bg-slate-100 border border-slate-200 rounded-md text-slate-600">
            row_version: {selectedClaim.row_version}
          </span>
        </div>

        <div className="space-y-3 text-xs">
          <div className="grid grid-cols-3 items-center gap-3 p-3 border border-slate-200/80 rounded-xl bg-slate-50/60">
            <span className="font-medium text-slate-600">Patient Token (Box 2)</span>
            <input
              type="text"
              readOnly
              value="SYN-PT-90412"
              className="border border-slate-200 rounded-lg px-3 py-1.5 bg-white font-mono text-slate-700"
            />
            <span className="text-emerald-700 font-semibold text-right">Conf: 0.99 ✓</span>
          </div>

          <div className="grid grid-cols-3 items-center gap-3 p-3 border border-slate-200/80 rounded-xl bg-slate-50/60">
            <span className="font-medium text-slate-600">Billing NPI (Box 33)</span>
            <input
              type="text"
              value={verifyNpiInput}
              onChange={(e) => setVerifyNpiInput(e.target.value)}
              className="border border-slate-300 rounded-lg px-3 py-1.5 bg-white font-mono font-bold text-slate-900"
            />
            <span className="text-emerald-700 font-semibold text-right">Conf: 0.97 ✓ (Luhn)</span>
          </div>

          <div className="grid grid-cols-3 items-center gap-3 p-3 border border-slate-200/80 rounded-xl bg-slate-50/60">
            <span className="font-medium text-slate-600">Line 1 CPT 97110 Units</span>
            <input
              type="number"
              readOnly
              value={2}
              className="border border-slate-200 rounded-lg px-3 py-1.5 bg-white font-mono text-slate-700"
            />
            <span className="text-emerald-700 font-semibold text-right">Conf: 0.95 ✓</span>
          </div>

          {/* Highlighted Low-Confidence Field */}
          <div className="p-4 border-2 border-rose-500/80 rounded-2xl bg-amber-50/70 space-y-3">
            <div className="flex flex-wrap items-center justify-between gap-2">
              <span className="font-bold text-rose-950 flex items-center gap-1.5">
                <AlertTriangle className="w-4 h-4 text-rose-600" />
                Line 2 (CPT 97140) — Box 24G Units of Service
              </span>
              <span className="px-2.5 py-0.5 bg-rose-600 text-white text-[10px] font-bold rounded-full">
                CONFIDENCE: 0.64 (&lt; 0.80 GATE)
              </span>
            </div>
            <p className="text-xs text-slate-700 leading-relaxed">
              OCR extracted <code className="font-mono font-bold">8</code> units from blurred ink. Leaving as{' '}
              <code className="font-mono font-bold">8</code> will trigger a false MUE violation (MUE limit for
              97140 is 4). Correcting to <code className="font-mono font-bold">2</code> matches the bill and
              clinical note.
            </p>
            <div className="flex flex-wrap items-center gap-2.5 pt-1">
              <label className="font-bold text-slate-900">Verified Units:</label>
              <input
                type="number"
                min={1}
                max={20}
                value={verifyUnitsInput}
                onChange={(e) => setVerifyUnitsInput(e.target.value)}
                className="w-20 border-2 border-indigo-600 rounded-xl px-3 py-1.5 bg-white text-sm font-mono font-bold text-center"
              />
              <button
                onClick={() => setVerifyUnitsInput(2)}
                className="px-3 py-1.5 text-xs font-semibold border border-emerald-300 rounded-xl bg-emerald-50 text-emerald-800 hover:bg-emerald-100 transition cursor-pointer"
              >
                Set to 2 (Fix OCR Error)
              </button>
              <button
                onClick={() => setVerifyUnitsInput(8)}
                className="px-3 py-1.5 text-xs font-semibold border border-rose-300 rounded-xl bg-rose-50 text-rose-800 hover:bg-rose-100 transition cursor-pointer"
              >
                Keep 8 (Test MUE Flag)
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="border-t border-slate-100 pt-4 flex flex-wrap items-center justify-between gap-3">
        <label className="flex items-center gap-2 text-xs text-slate-600 cursor-pointer">
          <input
            type="checkbox"
            checked={simulateStaleVersion}
            onChange={(e) => setSimulateStaleVersion(e.target.checked)}
            className="rounded text-indigo-600"
          />
          Simulate 409 Conflict (stale row_version)
        </label>

        <button
          onClick={handleCompleteVerification}
          className="px-5 py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold rounded-xl shadow-sm shadow-indigo-500/20 flex items-center gap-2 transition cursor-pointer"
        >
          <CheckCircle2 className="w-4 h-4" /> Confirm Fields & Resume Pipeline
        </button>
      </div>
    </div>
  );
}
