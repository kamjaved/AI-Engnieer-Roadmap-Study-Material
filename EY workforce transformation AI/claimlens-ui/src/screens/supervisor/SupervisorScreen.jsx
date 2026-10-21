import { useClaimLens } from '../../context/useClaimLens';
import SupervisorClaimCard from './SupervisorClaimCard';

/** Supervisor sign-off inbox (§3.5 #6, §4.2 Step 8 - HITL Point #3). */
export default function SupervisorScreen() {
  const { currentUser, setCurrentRole, triggerToast, supervisorQueue } = useClaimLens();

  return (
    <div className="max-w-6xl mx-auto space-y-5">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900">
            Supervisor Sign-Off Inbox (HITL Point #3)
          </h1>
          <p className="text-sm text-slate-500 mt-0.5">
            Enforces Four-Eyes Principle:{' '}
            <code className="font-mono text-xs bg-slate-100 px-1.5 py-0.5 rounded">
              POST /claims/&#123;id&#125;/signoff
            </code>{' '}
            requires <strong className="text-slate-700">Supervisor</strong> role AND{' '}
            <code className="font-mono text-xs">actor_oid ≠ examiner_oid</code>.
          </p>
        </div>

        {/* Role Helper Banner */}
        <div className="flex items-center gap-3 bg-white border border-slate-200 rounded-2xl px-4 py-2.5 text-xs shadow-2xs">
          <span className="text-slate-600">
            Active Persona:{' '}
            <strong className="text-slate-900">
              {currentUser.name} ({currentUser.role})
            </strong>
          </span>
          {currentUser.role !== 'Supervisor' && (
            <button
              onClick={() => {
                setCurrentRole('Supervisor');
                triggerToast('Switched to Supervisor role (Dana Sterling) to test Four-Eyes Sign-Off.');
              }}
              className="px-3 py-1 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold rounded-lg transition cursor-pointer"
            >
              Switch to Supervisor
            </button>
          )}
        </div>
      </div>

      {supervisorQueue.length === 0 ? (
        <div className="bg-white border border-slate-200 rounded-2xl p-12 text-center text-sm text-slate-500 shadow-2xs">
          No claims currently waiting in <code className="font-mono">DENIAL_RECOMMENDED</code> status.
          Recommend a denial from Claim Detail to test this queue.
        </div>
      ) : (
        <div className="space-y-4">
          {supervisorQueue.map((claim) => (
            <SupervisorClaimCard key={claim.id} claim={claim} />
          ))}
        </div>
      )}
    </div>
  );
}
