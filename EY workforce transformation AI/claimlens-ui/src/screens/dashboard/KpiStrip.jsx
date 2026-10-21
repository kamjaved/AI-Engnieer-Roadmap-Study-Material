import { KPI_CARDS } from '../../data/evalMetrics';

/** Business KPI cards (§11.2). */
export default function KpiStrip() {
  return (
    <div className="grid grid-cols-2 md:grid-cols-6 gap-3.5">
      {KPI_CARDS.map((k) => (
        <div key={k.label} className="bg-white border border-slate-200 rounded-2xl p-4 shadow-2xs">
          <div className="text-[11px] font-semibold text-slate-400 uppercase">{k.label}</div>
          <div className={`text-2xl font-bold font-mono ${k.valueClass} mt-1`}>{k.value}</div>
          <div className={`text-[11px] ${k.subClass} mt-0.5`}>{k.sub}</div>
        </div>
      ))}
    </div>
  );
}
