import { useClaimLens } from '../../context/useClaimLens';
import FindingsTab from './FindingsTab';
import MemoTab from './MemoTab';
import AuditTab from './AuditTab';

/** Right-hand tabbed analysis panel. */
export default function AnalysisPanel() {
  const { selectedClaim, detailTab, setDetailTab } = useClaimLens();

  return (
    <div className="lg:col-span-8 bg-white border border-slate-200 rounded-2xl shadow-2xs flex flex-col overflow-hidden">
      {/* Sub-Navigation Tabs */}
      <div className="flex border-b border-slate-200 bg-slate-50/70 p-1.5 gap-1.5">
        <button
          onClick={() => setDetailTab('findings')}
          className={`px-4 py-2 text-xs font-semibold rounded-xl transition cursor-pointer ${
            detailTab === 'findings'
              ? 'bg-white text-indigo-700 shadow-xs border border-slate-200/80'
              : 'text-slate-600 hover:text-slate-900'
          }`}
        >
          1. Rules & Decision-1 Probabilities ({selectedClaim.findings.length})
        </button>
        <button
          onClick={() => setDetailTab('memo')}
          className={`px-4 py-2 text-xs font-semibold rounded-xl transition cursor-pointer ${
            detailTab === 'memo'
              ? 'bg-white text-indigo-700 shadow-xs border border-slate-200/80'
              : 'text-slate-600 hover:text-slate-900'
          }`}
        >
          2. Grounded Finding Memo (RAG)
        </button>
        <button
          onClick={() => setDetailTab('audit')}
          className={`px-4 py-2 text-xs font-semibold rounded-xl transition cursor-pointer ${
            detailTab === 'audit'
              ? 'bg-white text-indigo-700 shadow-xs border border-slate-200/80'
              : 'text-slate-600 hover:text-slate-900'
          }`}
        >
          3. Hash-Chained Audit Trail ({selectedClaim.audit_events.length})
        </button>
      </div>

      {detailTab === 'findings' && <FindingsTab />}
      {detailTab === 'memo' && <MemoTab />}
      {detailTab === 'audit' && <AuditTab />}
    </div>
  );
}
