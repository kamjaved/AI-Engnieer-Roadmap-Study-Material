import { BookOpen } from 'lucide-react';
import { useClaimLens } from '../../context/useClaimLens';

/** Tab 2: grounded finding memo with policy citations. */
export default function MemoTab() {
  const { selectedClaim } = useClaimLens();

  return (
    <div className="p-5 space-y-4">
      {!selectedClaim.memo ? (
        <div className="p-5 border border-slate-200 rounded-xl text-xs text-slate-500">
          No memo generated (Claim stopped prior to Step 6 EXPLAINING).
        </div>
      ) : (
        <>
          <div className="bg-slate-50 border border-slate-200 rounded-xl p-3.5 flex flex-wrap items-center justify-between gap-2 text-xs">
            <div className="text-slate-600">
              Model:{' '}
              <strong className="font-mono text-slate-900">{selectedClaim.memo.model_deployment}</strong> •
              Schema: <code className="font-mono">FindingMemo</code>
            </div>
            <div className="flex items-center gap-2">
              <span className="px-2.5 py-0.5 bg-emerald-50 border border-emerald-200 rounded-full text-emerald-700 text-[11px] font-semibold">
                ✓ Citations & IDs Verified
              </span>
              <span className="px-2.5 py-0.5 bg-indigo-600 text-white rounded-full font-mono text-[11px] font-semibold">
                suggested: {selectedClaim.memo.suggested_action}
              </span>
            </div>
          </div>

          <div className="p-4 border border-indigo-100 rounded-xl bg-indigo-50/30 space-y-1.5">
            <div className="text-[11px] font-bold uppercase tracking-wider text-indigo-600">
              Executive Finding Summary
            </div>
            <p className="text-sm text-slate-900 leading-relaxed font-medium">{selectedClaim.memo.summary}</p>
          </div>

          {selectedClaim.memo.explanations.length > 0 && (
            <div className="space-y-3">
              <div className="text-xs font-bold uppercase tracking-wider text-slate-500">
                Per-Finding Explanations & NCCI Policy Manual 2026 RAG Citations
              </div>
              {selectedClaim.memo.explanations.map((exp) => (
                <div
                  key={exp.finding_id}
                  className="p-4 border border-slate-200 rounded-xl bg-slate-50/50 space-y-3"
                >
                  <div className="text-xs font-bold text-slate-800 flex items-center gap-2">
                    <span>Finding Reference:</span>
                    <span className="px-2 py-0.5 bg-white border border-slate-200 rounded-md font-mono text-indigo-700">
                      {exp.finding_id}
                    </span>
                  </div>
                  <p className="text-xs text-slate-700 leading-relaxed">{exp.plain_explanation}</p>
                  <div className="space-y-2 pt-1">
                    {exp.citations.map((cit) => (
                      <div
                        key={cit.chunk_id}
                        className="p-3 bg-white border-l-4 border-indigo-600 rounded-r-xl shadow-2xs text-xs space-y-1"
                      >
                        <div className="text-[11px] font-bold text-slate-800 flex flex-wrap justify-between gap-2">
                          <span className="flex items-center gap-1.5 text-indigo-900">
                            <BookOpen className="w-3.5 h-3.5 text-indigo-600" />
                            {cit.chapter} — Page {cit.page}
                          </span>
                          <span className="font-mono text-slate-400">chunk: {cit.chunk_id}</span>
                        </div>
                        <div className="text-xs text-slate-600 italic leading-relaxed">"{cit.excerpt}"</div>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          )}
        </>
      )}
    </div>
  );
}
