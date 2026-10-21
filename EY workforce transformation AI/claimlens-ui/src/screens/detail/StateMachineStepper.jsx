import { Fragment } from 'react';
import { Activity, ChevronRight } from 'lucide-react';
import { useClaimLens } from '../../context/useClaimLens';
import { STATE_MACHINE_ORDER } from '../../data/stateMachine';

/** Top state-machine progression bar (§4.1). */
export default function StateMachineStepper() {
  const { selectedClaim, simulateStaleVersion, setSimulateStaleVersion } = useClaimLens();

  return (
    <div className="bg-white border border-slate-200 rounded-2xl p-4 shadow-2xs">
      <div className="flex flex-wrap items-center justify-between gap-2 mb-3">
        <span className="text-xs font-semibold text-slate-500 flex items-center gap-1.5">
          <Activity className="w-4 h-4 text-indigo-600" />
          Claim State Machine Progression (§4.1 Canonical Lifecycle)
        </span>
        <div className="flex items-center gap-4 text-xs">
          <span className="text-slate-500">
            Optimistic Concurrency:{' '}
            <strong className="font-mono text-slate-800">row_version={selectedClaim.row_version}</strong>
          </span>
          <label className="flex items-center gap-1.5 text-xs text-slate-600 cursor-pointer">
            <input
              type="checkbox"
              checked={simulateStaleVersion}
              onChange={(e) => setSimulateStaleVersion(e.target.checked)}
              className="rounded text-indigo-600"
            />
            Simulate 409 Conflict
          </label>
        </div>
      </div>
      <div className="flex flex-wrap items-center gap-1.5 text-[11px]">
        {STATE_MACHINE_ORDER.map((st, idx) => {
          const isCurrent = selectedClaim.status === st;
          return (
            <Fragment key={st}>
              <span
                className={`px-2.5 py-1 rounded-lg font-medium transition ${
                  isCurrent
                    ? 'bg-indigo-600 text-white font-bold shadow-xs ring-2 ring-indigo-600/20'
                    : 'bg-slate-100 text-slate-500'
                }`}
              >
                {st.replace(/_/g, ' ')}
              </span>
              {idx < STATE_MACHINE_ORDER.length - 1 && (
                <ChevronRight className="w-3.5 h-3.5 text-slate-300" />
              )}
            </Fragment>
          );
        })}
        {['APPROVED', 'RECORDS_REQUESTED', 'REJECTED_INVALID'].includes(selectedClaim.status) && (
          <span className="px-2.5 py-1 bg-slate-900 text-white font-bold rounded-lg ml-1">
            {selectedClaim.status}
          </span>
        )}
      </div>
    </div>
  );
}
