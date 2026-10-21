import { useClaimLens } from '../../context/useClaimLens';
import BucketBadge from '../../components/common/BucketBadge';
import StatusBadge from '../../components/common/StatusBadge';

export default function ClaimHeaderCard() {
  const { selectedClaim } = useClaimLens();

  return (
    <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-2xs flex flex-wrap items-center justify-between gap-4">
      <div className="space-y-1.5">
        <div className="flex flex-wrap items-center gap-3">
          <h1 className="text-2xl font-bold font-mono text-slate-900">{selectedClaim.id}</h1>
          <BucketBadge bucket={selectedClaim.bucket} isQa={selectedClaim.is_qa_sample} />
          <StatusBadge status={selectedClaim.status} />
        </div>
        <div className="text-xs text-slate-600 flex flex-wrap gap-5 pt-0.5">
          <span>
            Patient Token: <strong className="font-mono text-slate-900">{selectedClaim.patient_token}</strong>{' '}
            ({selectedClaim.patient_age}yo {selectedClaim.patient_sex})
          </span>
          <span>
            Billing NPI: <strong className="font-mono text-slate-900">{selectedClaim.billing_npi}</strong>
          </span>
          <span>
            DOS: <strong className="font-mono text-slate-900">{selectedClaim.dos_from}</strong>
          </span>
          <span>
            Source: <strong className="uppercase text-slate-900">{selectedClaim.source}</strong>
          </span>
        </div>
      </div>

      <div className="flex items-center gap-6">
        <div className="text-right">
          <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
            Total Billed
          </div>
          <div className="text-xl font-bold font-mono text-slate-800 mt-0.5">
            ${selectedClaim.total_charge.toFixed(2)}
          </div>
        </div>
        <div className="text-right border-l border-slate-200 pl-6">
          <div className="text-[11px] font-semibold text-rose-600 uppercase tracking-wider">
            Dollars at Risk
          </div>
          <div className="text-2xl font-bold font-mono text-rose-600 mt-0.5">
            ${selectedClaim.dollars_at_risk.toFixed(2)}
          </div>
        </div>
      </div>
    </div>
  );
}
