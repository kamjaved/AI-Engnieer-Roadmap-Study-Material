import { ArrowRight } from 'lucide-react';
import { useClaimLens } from '../../context/useClaimLens';
import BucketBadge from '../../components/common/BucketBadge';
import StatusBadge from '../../components/common/StatusBadge';

export default function QueueTable() {
  const { filteredClaims, selectedClaimId, openClaim } = useClaimLens();

  return (
    <div className="bg-white border border-slate-200 rounded-2xl shadow-2xs overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-slate-50/80 border-b border-slate-200 text-[11px] font-semibold uppercase tracking-wider text-slate-500">
              <th className="py-3.5 px-4">Claim ID / Source</th>
              <th className="py-3.5 px-4">Patient / Billing NPI</th>
              <th className="py-3.5 px-4">Risk Bucket</th>
              <th className="py-3.5 px-4">Primary Finding</th>
              <th className="py-3.5 px-4 text-right">$ at Risk</th>
              <th className="py-3.5 px-4 text-right">Total Billed</th>
              <th className="py-3.5 px-4">Pipeline Status</th>
              <th className="py-3.5 px-4">Received</th>
              <th className="py-3.5 px-4 text-right">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 text-xs">
            {filteredClaims.map((claim) => {
              const isSelected = selectedClaimId === claim.id;
              return (
                <tr
                  key={claim.id}
                  onClick={() => openClaim(claim)}
                  className={`hover:bg-indigo-50/40 cursor-pointer transition-colors ${
                    isSelected ? 'bg-indigo-50/60' : ''
                  }`}
                >
                  <td className="py-3.5 px-4">
                    <div className="font-mono font-bold text-slate-900 text-sm">{claim.id}</div>
                    <div className="text-[11px] text-slate-500 flex items-center gap-1.5 mt-0.5">
                      <span className="px-1.5 py-0.2 bg-slate-100 border border-slate-200 rounded text-[10px] font-semibold uppercase text-slate-600">
                        {claim.source}
                      </span>
                      <span className="font-mono">{claim.external_ref}</span>
                    </div>
                  </td>
                  <td className="py-3.5 px-4">
                    <div className="font-medium text-slate-800">{claim.patient_token}</div>
                    <div className="text-[11px] font-mono text-slate-500 mt-0.5">
                      NPI: {claim.billing_npi}
                    </div>
                  </td>
                  <td className="py-3.5 px-4">
                    <BucketBadge bucket={claim.bucket} isQa={claim.is_qa_sample} />
                  </td>
                  <td className="py-3.5 px-4">
                    <span className="inline-flex items-center px-2.5 py-1 bg-slate-100/90 border border-slate-200 rounded-lg font-mono text-slate-800 text-xs font-medium">
                      {claim.top_finding}
                    </span>
                  </td>
                  <td className="py-3.5 px-4 font-mono text-right font-bold text-sm">
                    <span className={claim.dollars_at_risk > 0 ? 'text-rose-600' : 'text-slate-400'}>
                      ${claim.dollars_at_risk.toFixed(2)}
                    </span>
                  </td>
                  <td className="py-3.5 px-4 font-mono text-right text-slate-600 font-medium">
                    ${claim.total_charge.toFixed(2)}
                  </td>
                  <td className="py-3.5 px-4">
                    <StatusBadge status={claim.status} />
                  </td>
                  <td className="py-3.5 px-4 text-xs text-slate-500">
                    <div className="font-medium text-slate-700">{claim.age} ago</div>
                    <div className="font-mono text-[10px] text-slate-400">row_v{claim.row_version}</div>
                  </td>
                  <td className="py-3.5 px-4 text-right">
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        openClaim(claim);
                      }}
                      className={`px-3 py-1.5 font-semibold text-xs rounded-xl transition inline-flex items-center gap-1.5 shadow-2xs cursor-pointer ${
                        claim.status === 'NEEDS_FIELD_VERIFICATION'
                          ? 'bg-amber-600 hover:bg-amber-500 text-white'
                          : 'bg-indigo-600 hover:bg-indigo-500 text-white'
                      }`}
                    >
                      {claim.status === 'NEEDS_FIELD_VERIFICATION' ? 'Verify OCR' : 'Inspect'}
                      <ArrowRight className="w-3.5 h-3.5" />
                    </button>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
