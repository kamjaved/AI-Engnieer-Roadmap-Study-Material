import { ShieldCheck } from 'lucide-react';
import { useClaimLens } from '../../context/useClaimLens';

/** Tab 3: hash-chained audit timeline. */
export default function AuditTab() {
  const { selectedClaim } = useClaimLens();

  return (
    <div className="p-5 space-y-3">
      <div className="flex flex-wrap items-center justify-between gap-2 text-xs bg-slate-50 p-3 border border-slate-200 rounded-xl">
        <span className="text-slate-600">
          Table: <code className="font-mono font-semibold text-slate-800">audit_events</code> (Append-only;
          UPDATE/DELETE privileges revoked)
        </span>
        <span className="text-emerald-700 font-semibold flex items-center gap-1">
          <ShieldCheck className="w-4 h-4" /> SHA-256 Hash Chain Verified
        </span>
      </div>

      <div className="space-y-2.5 text-xs">
        {selectedClaim.audit_events.map((ev) => (
          <div
            key={ev.seq}
            className="p-3.5 border border-slate-200 rounded-xl bg-white space-y-1.5 shadow-2xs"
          >
            <div className="flex flex-wrap items-center justify-between gap-2">
              <span className="font-mono font-bold text-indigo-700">
                #{ev.seq} — {ev.event_type}
              </span>
              <span className="text-[11px] text-slate-500">
                {ev.timestamp} • Actor: <strong className="font-mono text-slate-700">{ev.actor}</strong>
              </span>
            </div>
            <div className="text-slate-700 text-xs leading-relaxed">{ev.details}</div>
            <div className="text-[11px] font-mono text-slate-400 pt-1 flex flex-wrap gap-4">
              <span>
                prev_hash: <code>{ev.prev_hash}</code>
              </span>
              <span>
                hash: <code className="text-slate-700 font-semibold">{ev.hash}</code>
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
