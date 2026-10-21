import { ShieldAlert, Layers } from 'lucide-react';
import { useClaimLens } from '../../context/useClaimLens';

export default function SyntheticBanner() {
  const { showDemoBar, setShowDemoBar } = useClaimLens();

  return (
    <div className="bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 text-slate-200 text-xs py-2 px-5 flex flex-wrap items-center justify-between gap-2 border-b border-slate-800">
      <div className="flex items-center gap-2.5">
        <span className="px-2 py-0.5 bg-amber-400/20 text-amber-300 border border-amber-400/30 font-semibold rounded-full text-[11px] flex items-center gap-1">
          <ShieldAlert className="w-3 h-3 text-amber-400" />
          SYNTHETIC DATA
        </span>
        <span className="text-slate-300">
          CMS DE-SynPUF + Luhn NPIs. ClaimLens provides decision support only; human examiners own all
          adjudication decisions.
        </span>
      </div>
      <div className="flex items-center gap-4 text-xs text-slate-300">
        <span className="hidden md:inline-flex items-center gap-1.5 text-slate-400 font-mono text-[11px]">
          <Layers className="w-3.5 h-3.5 text-indigo-400" />
          PTP-v32.3 • MUE-2026Q4 • PFREV26D
        </span>
        <button
          onClick={() => setShowDemoBar(!showDemoBar)}
          className="px-2.5 py-0.5 rounded-full bg-white/10 hover:bg-white/20 text-white font-medium text-[11px] transition cursor-pointer"
        >
          {showDemoBar ? 'Hide Demo Walkthrough' : 'Show 8-Step Walkthrough'}
        </button>
      </div>
    </div>
  );
}
