import { ShieldCheck, Lock } from 'lucide-react';
import { useClaimLens } from '../../context/useClaimLens';
import BucketBadge from '../../components/common/BucketBadge';
import StatusBadge from '../../components/common/StatusBadge';

/** One claim waiting for sign-off, with the four-eyes check computed from the current persona. */
export default function SupervisorClaimCard({ claim }) {
  const { currentUser, openClaim, handleSupervisorDecision } = useClaimLens();

  const isSamePerson = claim.recommended_by_oid === currentUser.oid;
  const isSupervisor = currentUser.role === 'Supervisor';
  const canSignOff = isSupervisor && !isSamePerson;

  return (
    <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-2xs space-y-4">
      <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-100 pb-4">
        <div className="flex items-center gap-3">
          <span className="text-xl font-bold font-mono text-slate-900">{claim.id}</span>
          <BucketBadge bucket={claim.bucket} />
          <StatusBadge status={claim.status} />
        </div>
        <div className="text-xs font-mono">
          <span className="text-rose-600 font-bold text-sm">
            $ at Risk: ${claim.dollars_at_risk.toFixed(2)}
          </span>{' '}
          <span className="text-slate-400">/ Total: ${claim.total_charge.toFixed(2)}</span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs bg-slate-50 p-4 border border-slate-200/80 rounded-xl">
        <div className="space-y-1.5">
          <div className="text-[11px] font-bold uppercase tracking-wider text-slate-400">
            Recommended By Examiner
          </div>
          <div className="font-bold text-slate-900 text-sm">{claim.recommended_by_name}</div>
          <div className="text-[11px] font-mono text-slate-500">OID: {claim.recommended_by_oid}</div>
          <div className="pt-1">
            Reason Code:{' '}
            <span className="px-2 py-0.5 bg-rose-100 border border-rose-200 rounded-md font-mono text-rose-800 font-bold">
              {claim.recommended_reason}
            </span>
          </div>
        </div>
        <div className="space-y-1.5">
          <div className="text-[11px] font-bold uppercase tracking-wider text-slate-400">
            Examiner Rationale & Memo Summary
          </div>
          <div className="text-slate-900 font-semibold">"{claim.recommended_comment}"</div>
          <div className="text-slate-600 text-xs leading-relaxed">{claim.memo?.summary}</div>
        </div>
      </div>

      {/* Four-Eyes Enforcement Status Bar */}
      <div className="flex flex-wrap items-center justify-between gap-4 pt-1">
        <div className="text-xs">
          {canSignOff ? (
            <span className="inline-flex items-center gap-1.5 text-emerald-700 font-semibold bg-emerald-50 px-3 py-1.5 rounded-xl border border-emerald-200">
              <ShieldCheck className="w-4 h-4" />
              Four-Eyes Policy Satisfied: Supervisor OID ({currentUser.oid.slice(0, 6)}) ≠ Examiner OID (
              {claim.recommended_by_oid?.slice(0, 6)})
            </span>
          ) : (
            <span className="inline-flex items-center gap-1.5 text-rose-700 font-semibold bg-rose-50 px-3 py-1.5 rounded-xl border border-rose-200">
              <Lock className="w-4 h-4" />
              Four-Eyes Guard Active: Cannot sign off as {currentUser.name} ({currentUser.role}). Switch to
              Supervisor Dana Sterling.
            </span>
          )}
        </div>

        <div className="flex flex-wrap items-center gap-2.5">
          <button
            onClick={() => openClaim(claim)}
            className="px-3.5 py-2 text-xs font-semibold border border-slate-200 rounded-xl hover:bg-slate-50 text-slate-700 cursor-pointer"
          >
            Inspect Full Claim
          </button>
          <button
            disabled={!canSignOff}
            onClick={() => handleSupervisorDecision(claim, 'return')}
            className={`px-3.5 py-2 text-xs font-semibold border rounded-xl transition ${
              canSignOff
                ? 'border-slate-300 bg-white hover:bg-slate-50 text-slate-800 cursor-pointer'
                : 'border-slate-200 bg-slate-100 text-slate-400 cursor-not-allowed'
            }`}
          >
            Return to Queue
          </button>
          <button
            disabled={!canSignOff}
            onClick={() => handleSupervisorDecision(claim, 'confirm')}
            className={`px-4 py-2 text-xs font-semibold rounded-xl transition ${
              canSignOff
                ? 'bg-rose-600 text-white hover:bg-rose-500 shadow-sm shadow-rose-500/20 cursor-pointer'
                : 'bg-slate-200 text-slate-400 cursor-not-allowed'
            }`}
          >
            Confirm Denial (DENIAL_CONFIRMED)
          </button>
        </div>
      </div>
    </div>
  );
}
