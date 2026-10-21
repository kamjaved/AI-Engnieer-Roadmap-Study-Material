import { GOLD_SLICES } from '../../data/evalMetrics';

/** Gold-set slice table + Decision-1 vs GPT benchmark (§8.2 / B23). */
export default function GoldSetBreakdown() {
  return (
    <div className="lg:col-span-7 bg-white border border-slate-200 rounded-2xl p-5 shadow-2xs space-y-4 overflow-x-auto">
      <div className="flex items-center justify-between border-b border-slate-100 pb-3">
        <span className="text-xs font-bold uppercase tracking-wider text-slate-700">
          Gold Test Set Breakdown (1,000 Frozen Claims)
        </span>
        <span className="text-xs font-mono text-indigo-600 bg-indigo-50 px-2.5 py-0.5 rounded-md">
          claimlens eval run --set gold_test
        </span>
      </div>

      <table className="w-full text-left border-collapse text-xs">
        <thead>
          <tr className="bg-slate-50 border-b border-slate-200 text-[11px] font-semibold uppercase text-slate-500">
            <th className="py-2.5 px-3">Slice</th>
            <th className="py-2.5 px-3">Planted Error / Control Type</th>
            <th className="py-2.5 px-3 text-right">Count</th>
            <th className="py-2.5 px-3 text-right">Precision</th>
            <th className="py-2.5 px-3 text-right">Recall</th>
            <th className="py-2.5 px-3 text-right">Override %</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-100">
          {GOLD_SLICES.map((s) => (
            <tr key={s.slice}>
              <td className={`py-2.5 px-3 font-mono font-bold ${s.sliceClass}`}>{s.slice}</td>
              <td className="py-2.5 px-3 text-slate-600">{s.description}</td>
              <td className="py-2.5 px-3 font-mono text-right">{s.count}</td>
              <td className="py-2.5 px-3 font-mono text-right font-semibold">{s.precision}</td>
              <td className="py-2.5 px-3 font-mono text-right font-semibold">{s.recall}</td>
              <td className="py-2.5 px-3 font-mono text-right text-slate-500">{s.override}</td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* B23: Decision-1 vs GPT Structured Output Comparison */}
      <div className="pt-4 border-t border-slate-100 space-y-2.5">
        <div className="text-xs font-bold uppercase tracking-wider text-slate-600">
          §8.2 / B23 Benchmark: Microsoft-Decision-1 vs. GPT Structured-Output Fallback
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5 text-xs">
          <div className="p-3.5 border border-indigo-200 rounded-xl bg-indigo-50/40 space-y-1">
            <div className="font-bold text-indigo-950">Microsoft-Decision-1 (systemone)</div>
            <div className="text-slate-600">
              AUROC: <strong className="font-mono text-slate-900">0.948</strong> • Calibration ECE:{' '}
              <strong className="font-mono text-emerald-700">0.031</strong>
            </div>
            <div className="text-slate-600">
              Latency: <strong className="font-mono text-slate-900">410 ms</strong> • Cost/1k claims:{' '}
              <strong className="font-mono text-slate-900">$0.14</strong>
            </div>
          </div>
          <div className="p-3.5 border border-slate-200 rounded-xl bg-slate-50 space-y-1">
            <div className="font-bold text-slate-700">GPT Structured-Output Fallback</div>
            <div className="text-slate-600">
              AUROC: <strong className="font-mono text-slate-900">0.912</strong> • Calibration ECE:{' '}
              <strong className="font-mono text-rose-600">0.142 (Overconfident)</strong>
            </div>
            <div className="text-slate-600">
              Latency: <strong className="font-mono text-slate-900">1,850 ms</strong> • Cost/1k claims:{' '}
              <strong className="font-mono text-slate-900">$2.90</strong>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
