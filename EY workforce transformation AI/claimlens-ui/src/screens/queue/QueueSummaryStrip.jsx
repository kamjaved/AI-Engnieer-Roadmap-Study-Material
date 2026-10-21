import { Layers, XCircle, AlertTriangle, CheckCircle2, DollarSign } from 'lucide-react';
import { useClaimLens } from '../../context/useClaimLens';

export default function QueueSummaryStrip() {
  const { claims } = useClaimLens();

  return (
    <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
      <div className="bg-white border border-slate-200/90 p-4 rounded-2xl shadow-2xs">
        <div className="flex items-center justify-between text-xs font-semibold text-slate-500">
          <span>TOTAL IN QUEUE</span>
          <Layers className="w-4 h-4 text-slate-400" />
        </div>
        <div className="text-2xl font-bold text-slate-900 mt-2">{claims.length}</div>
        <div className="text-xs text-slate-500 mt-1">Professional (CMS-1500)</div>
      </div>

      <div className="bg-white border border-rose-200 p-4 rounded-2xl shadow-2xs relative overflow-hidden">
        <div className="absolute top-0 left-0 w-1 h-full bg-rose-500" />
        <div className="flex items-center justify-between text-xs font-semibold text-rose-700">
          <span>RED BUCKET (HARD HIT)</span>
          <XCircle className="w-4 h-4 text-rose-500" />
        </div>
        <div className="text-2xl font-bold text-rose-700 mt-2">
          {claims.filter((c) => c.bucket === 'RED').length}
        </div>
        <div className="text-xs text-slate-500 mt-1">Confident rule / AI violation</div>
      </div>

      <div className="bg-white border border-amber-200 p-4 rounded-2xl shadow-2xs relative overflow-hidden">
        <div className="absolute top-0 left-0 w-1 h-full bg-amber-500" />
        <div className="flex items-center justify-between text-xs font-semibold text-amber-800">
          <span>AMBER BUCKET</span>
          <AlertTriangle className="w-4 h-4 text-amber-500" />
        </div>
        <div className="text-2xl font-bold text-amber-800 mt-2">
          {claims.filter((c) => c.bucket === 'AMBER').length}
        </div>
        <div className="text-xs text-slate-500 mt-1">Soft outlier / uncertain band</div>
      </div>

      <div className="bg-white border border-emerald-200 p-4 rounded-2xl shadow-2xs relative overflow-hidden">
        <div className="absolute top-0 left-0 w-1 h-full bg-emerald-500" />
        <div className="flex items-center justify-between text-xs font-semibold text-emerald-700">
          <span>GREEN (5% QA SAMPLE)</span>
          <CheckCircle2 className="w-4 h-4 text-emerald-500" />
        </div>
        <div className="text-2xl font-bold text-emerald-700 mt-2">
          {claims.filter((c) => c.bucket === 'GREEN').length}
        </div>
        <div className="text-xs text-slate-500 mt-1">Template memo (0 LLM cost)</div>
      </div>

      <div className="bg-gradient-to-br from-slate-900 to-indigo-950 text-white p-4 rounded-2xl shadow-sm">
        <div className="flex items-center justify-between text-xs font-semibold text-indigo-200">
          <span>FLAGGED $ AT RISK</span>
          <DollarSign className="w-4 h-4 text-indigo-300" />
        </div>
        <div className="text-2xl font-bold font-mono text-white mt-2">
          ${claims.reduce((acc, c) => acc + Number(c.dollars_at_risk || 0), 0).toFixed(2)}
        </div>
        <div className="text-xs text-slate-300 mt-1">Sum of flagged service lines</div>
      </div>
    </div>
  );
}
