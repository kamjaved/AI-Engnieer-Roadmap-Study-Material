import { Filter, Search } from 'lucide-react';
import { useClaimLens } from '../../context/useClaimLens';

export default function QueueFilters() {
  const {
    bucketFilter,
    setBucketFilter,
    statusFilter,
    setStatusFilter,
    checkFilter,
    setCheckFilter,
    searchQuery,
    setSearchQuery,
  } = useClaimLens();

  return (
    <div className="bg-white border border-slate-200 p-4 rounded-2xl shadow-2xs flex flex-wrap items-center gap-3">
      <div className="flex items-center gap-1.5 text-xs font-semibold text-slate-600 mr-1">
        <Filter className="w-4 h-4 text-indigo-600" /> Filter Queue:
      </div>

      <select
        value={bucketFilter}
        onChange={(e) => setBucketFilter(e.target.value)}
        className="border border-slate-200 rounded-xl px-3 py-2 text-xs font-medium bg-slate-50 hover:bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500/20"
      >
        <option value="ALL">Risk Bucket: All</option>
        <option value="RED">RED (Hard Hit)</option>
        <option value="AMBER">AMBER (Uncertain)</option>
        <option value="GREEN">GREEN (5% QA)</option>
        <option value="PENDING">PENDING (OCR Verify)</option>
        <option value="REJECTED">REJECTED (Format Error)</option>
      </select>

      <select
        value={statusFilter}
        onChange={(e) => setStatusFilter(e.target.value)}
        className="border border-slate-200 rounded-xl px-3 py-2 text-xs font-medium bg-slate-50 hover:bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500/20"
      >
        <option value="ALL">Workflow Status: All</option>
        <option value="NEEDS_FIELD_VERIFICATION">NEEDS_FIELD_VERIFICATION</option>
        <option value="READY_FOR_REVIEW">READY_FOR_REVIEW</option>
        <option value="DENIAL_RECOMMENDED">DENIAL_RECOMMENDED</option>
        <option value="DENIAL_CONFIRMED">DENIAL_CONFIRMED</option>
        <option value="APPROVED">APPROVED</option>
        <option value="RECORDS_REQUESTED">RECORDS_REQUESTED</option>
        <option value="REJECTED_INVALID">REJECTED_INVALID</option>
      </select>

      <select
        value={checkFilter}
        onChange={(e) => setCheckFilter(e.target.value)}
        className="border border-slate-200 rounded-xl px-3 py-2 text-xs font-medium bg-slate-50 hover:bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500/20"
      >
        <option value="ALL">Rule / AI Check: All</option>
        <option value="R1_PTP">R1_PTP (NCCI Procedure Pair)</option>
        <option value="R2_MUE">R2_MUE (Medically Unlikely Units)</option>
        <option value="R3_FEE">R3_FEE (Charge Outlier &gt; p99)</option>
        <option value="R4_DUP">R4_DUP (Duplicate Service Line)</option>
        <option value="AI_DECISION_1">AI_DECISION_1 (Note / DX / E&M)</option>
      </select>

      <div className="flex-1 min-w-[220px] relative">
        <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Search Claim ID, Patient Token, NPI, or finding..."
          className="w-full pl-9 pr-3 py-2 text-xs border border-slate-200 rounded-xl bg-slate-50 focus:bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500/20"
        />
      </div>

      <button
        onClick={() => {
          setBucketFilter('ALL');
          setStatusFilter('ALL');
          setCheckFilter('ALL');
          setSearchQuery('');
        }}
        className="px-3 py-2 text-xs font-medium text-slate-600 hover:text-slate-900 border border-slate-200 rounded-xl hover:bg-slate-50 transition cursor-pointer"
      >
        Reset
      </button>
    </div>
  );
}
