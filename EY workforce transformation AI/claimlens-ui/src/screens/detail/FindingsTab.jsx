import { CheckCircle2, Cpu, Sparkles } from 'lucide-react';
import { useClaimLens } from '../../context/useClaimLens';

/** Tab 1: deterministic rule findings (Layer 2) + Decision-1 probabilities (Layer 3). */
export default function FindingsTab() {
  const { selectedClaim, thresholds, handleToggleOverrideFinding } = useClaimLens();

  return (
    <div className="p-5 space-y-5">
      {/* Deterministic Rule Findings */}
      <div className="space-y-3">
        <div className="text-xs font-bold uppercase tracking-wider text-slate-600 flex items-center justify-between">
          <span className="flex items-center gap-1.5">
            <Cpu className="w-4 h-4 text-indigo-600" />
            Layer 2: Deterministic Rules Engine (claimlens_rules — Pure Python)
          </span>
          <span className="text-[11px] font-normal text-slate-400">100% Auditable Table Lookups</span>
        </div>

        {selectedClaim.findings.filter((f) => f.check_type === 'RULE').length === 0 ? (
          <div className="p-4 border border-emerald-200 rounded-xl bg-emerald-50/50 text-xs font-medium text-emerald-800 flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
            Zero deterministic rule violations across R1 (PTP), R2 (MUE), R3 (Fee), R4 (Duplicate), and R5
            (Modifier).
          </div>
        ) : (
          selectedClaim.findings
            .filter((f) => f.check_type === 'RULE')
            .map((f) => (
              <div
                key={f.id}
                className={`p-4 border rounded-xl text-xs space-y-2.5 transition ${
                  f.overridden
                    ? 'border-slate-200 bg-slate-50 opacity-75'
                    : f.severity === 'HARD'
                      ? 'border-rose-200 bg-rose-50/40'
                      : 'border-amber-200 bg-amber-50/40'
                }`}
              >
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <div className="flex items-center gap-2">
                    <span
                      className={`px-2.5 py-0.5 font-mono font-bold text-[11px] rounded-md ${
                        f.severity === 'HARD' ? 'bg-rose-600 text-white' : 'bg-amber-600 text-white'
                      }`}
                    >
                      {f.check_id}
                    </span>
                    <span className="font-bold text-slate-900">
                      {f.severity} SEVERITY • Line #{f.line_nos.join(', #')}
                    </span>
                    {f.overridden && (
                      <span className="px-2 py-0.5 bg-amber-200 text-amber-900 text-[10px] font-bold rounded-full">
                        OVERRIDDEN BY EXAMINER
                      </span>
                    )}
                  </div>
                  <div className="flex items-center gap-2.5">
                    <span className="text-[11px] font-mono text-slate-500">{f.table_version}</span>
                    <button
                      onClick={() => handleToggleOverrideFinding(f.id)}
                      className="px-2.5 py-1 border border-slate-300 rounded-lg bg-white hover:bg-slate-50 text-slate-700 text-[11px] font-semibold shadow-2xs cursor-pointer"
                    >
                      {f.overridden ? 'Undo Override' : 'Override Finding'}
                    </button>
                  </div>
                </div>

                <div className="p-2.5 bg-white border border-slate-200/80 rounded-lg font-mono text-[11px] text-slate-700 overflow-x-auto">
                  {JSON.stringify(f.details)}
                </div>
              </div>
            ))
        )}
      </div>

      {/* Layer 3: Microsoft-Decision-1 Typed Probabilistic Checks (§8.2) */}
      {selectedClaim.findings
        .filter((f) => f.check_type === 'AI')
        .map((aiFinding) => {
          const d = aiFinding.details;
          return (
            <div key={aiFinding.id} className="border-t border-slate-100 pt-5 space-y-3">
              <div className="flex flex-wrap items-center justify-between gap-2 text-xs">
                <span className="font-bold uppercase tracking-wider text-slate-600 flex items-center gap-1.5">
                  <Sparkles className="w-4 h-4 text-indigo-600" />
                  Layer 3: Microsoft-Decision-1 Probabilities
                </span>
                <span className="text-[11px] font-mono text-slate-400">
                  {aiFinding.model_deployment} • {aiFinding.question_set_version}
                </span>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-3.5 text-xs">
                {/* Question 1: note_documents_all_services (noul) */}
                <div className="p-4 border border-slate-200 rounded-xl bg-slate-50/50 space-y-2.5">
                  <div className="flex justify-between items-start gap-1">
                    <span className="font-bold text-slate-800">1. Note Documents Services</span>
                    <span className="text-[10px] font-mono px-1.5 py-0.5 bg-slate-200/80 rounded text-slate-600">
                      noul
                    </span>
                  </div>
                  <div className="text-xl font-bold font-mono text-slate-900">
                    p(true) = {(d.note_documents_all_services.p_true * 100).toFixed(0)}%
                  </div>
                  <div className="w-full h-2.5 bg-slate-200 rounded-full overflow-hidden">
                    <div
                      className={`h-full rounded-full transition-all ${
                        d.note_documents_all_services.p_true < thresholds.noteDocRed
                          ? 'bg-rose-500'
                          : d.note_documents_all_services.p_true < thresholds.noteDocGreen
                            ? 'bg-amber-500'
                            : 'bg-emerald-500'
                      }`}
                      style={{ width: `${d.note_documents_all_services.p_true * 100}%` }}
                    />
                  </div>
                  <div className="text-[10px] text-slate-400 font-mono">
                    RED &lt; {thresholds.noteDocRed} | GREEN ≥ {thresholds.noteDocGreen}
                  </div>
                  {d.note_documents_all_services.note && (
                    <div className="text-[11px] text-rose-800 bg-rose-50 p-2 border border-rose-200 rounded-lg leading-snug">
                      {d.note_documents_all_services.note}
                    </div>
                  )}
                </div>

                {/* Question 2: diagnosis_supports_services (choice) */}
                <div className="p-4 border border-slate-200 rounded-xl bg-slate-50/50 space-y-2.5">
                  <div className="flex justify-between items-start gap-1">
                    <span className="font-bold text-slate-800">2. Dx Supports Services</span>
                    <span className="text-[10px] font-mono px-1.5 py-0.5 bg-slate-200/80 rounded text-slate-600">
                      choice
                    </span>
                  </div>
                  <div className="text-xs font-semibold text-slate-700">
                    Top Choice:{' '}
                    <span className="font-mono font-bold text-indigo-700 underline">
                      {d.diagnosis_supports_services.choice}
                    </span>
                  </div>
                  <div className="space-y-1.5 text-[11px]">
                    {Object.entries(d.diagnosis_supports_services.probabilities).map(([opt, prob]) => (
                      <div key={opt}>
                        <div className="flex justify-between font-mono text-slate-600 mb-0.5">
                          <span>{opt}</span>
                          <span className="font-semibold">{(prob * 100).toFixed(0)}%</span>
                        </div>
                        <div className="w-full h-1.5 bg-slate-200 rounded-full overflow-hidden">
                          <div
                            className="h-full bg-indigo-600 rounded-full"
                            style={{ width: `${prob * 100}%` }}
                          />
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Question 3: em_level_consistent (choice) */}
                <div className="p-4 border border-slate-200 rounded-xl bg-slate-50/50 space-y-2.5">
                  <div className="flex justify-between items-start gap-1">
                    <span className="font-bold text-slate-800">3. E/M Level Consistency</span>
                    <span className="text-[10px] font-mono px-1.5 py-0.5 bg-slate-200/80 rounded text-slate-600">
                      choice
                    </span>
                  </div>
                  <div className="text-xs font-semibold text-slate-700">
                    Top Choice:{' '}
                    <span className="font-mono font-bold text-indigo-700 underline">
                      {d.em_level_consistent.choice}
                    </span>
                  </div>
                  <div className="space-y-1.5 text-[11px]">
                    {Object.entries(d.em_level_consistent.probabilities).map(([opt, prob]) => (
                      <div key={opt}>
                        <div className="flex justify-between font-mono text-slate-600 mb-0.5">
                          <span>{opt}</span>
                          <span className="font-semibold">{(prob * 100).toFixed(0)}%</span>
                        </div>
                        <div className="w-full h-1.5 bg-slate-200 rounded-full overflow-hidden">
                          <div
                            className="h-full bg-indigo-600 rounded-full"
                            style={{ width: `${prob * 100}%` }}
                          />
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          );
        })}
    </div>
  );
}
