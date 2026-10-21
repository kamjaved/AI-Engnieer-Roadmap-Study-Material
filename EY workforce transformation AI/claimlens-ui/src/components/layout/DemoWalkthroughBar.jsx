import { Play } from 'lucide-react';
import { useClaimLens } from '../../context/useClaimLens';
import { DEMO_SCRIPT_STEPS } from '../../data/demoScript';
import StatusBadge from '../common/StatusBadge';

export default function DemoWalkthroughBar() {
  const {
    showDemoBar,
    selectedClaim,
    selectedClaimId,
    activeScreen,
    setSelectedClaimId,
    setCurrentRole,
    setActiveScreen,
  } = useClaimLens();

  if (!showDemoBar) return null;

  return (
    <div className="bg-indigo-950/5 border-b border-indigo-100 px-5 py-3">
      <div className="max-w-7xl mx-auto">
        <div className="flex flex-wrap items-center justify-between gap-2 mb-2">
          <span className="text-xs font-semibold text-indigo-950 flex items-center gap-1.5">
            <span className="w-5 h-5 rounded-full bg-indigo-600 text-white flex items-center justify-center">
              <Play className="w-3 h-3 fill-current" />
            </span>
            Interactive Demo Walkthrough (Click any scenario to jump directly):
          </span>
          <div className="flex items-center gap-2 text-xs text-slate-600">
            <span>Active Claim:</span>
            <span className="font-mono font-semibold text-indigo-700 bg-white px-2 py-0.5 rounded-md border border-indigo-200">
              {selectedClaim.id}
            </span>
            <StatusBadge status={selectedClaim.status} />
          </div>
        </div>
        <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-8 gap-2">
          {DEMO_SCRIPT_STEPS.map((s) => {
            const isActive = activeScreen === s.screen && (!s.claimId || selectedClaimId === s.claimId);
            return (
              <button
                key={s.step}
                onClick={() => {
                  if (s.claimId) setSelectedClaimId(s.claimId);
                  if (s.step === 7) setCurrentRole('Supervisor');
                  setActiveScreen(s.screen);
                }}
                className={`text-left p-2.5 rounded-xl border transition-all cursor-pointer ${
                  isActive
                    ? 'bg-white border-indigo-600 ring-2 ring-indigo-600/20 shadow-xs'
                    : 'bg-white/70 border-slate-200/90 hover:bg-white hover:border-indigo-300'
                }`}
              >
                <div
                  className={`text-xs font-bold truncate ${isActive ? 'text-indigo-700' : 'text-slate-800'}`}
                >
                  {s.title}
                </div>
                <div className="text-[11px] text-slate-500 truncate mt-0.5">{s.desc}</div>
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
}
