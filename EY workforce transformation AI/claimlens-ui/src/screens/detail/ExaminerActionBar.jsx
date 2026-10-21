import { UserCheck, Check, FileWarning, XCircle } from 'lucide-react';
import { useClaimLens } from '../../context/useClaimLens';
import { REASON_CODES } from '../../data/reasonCodes';

/** Examiner action bar (HITL Point #2 - §3.5 #5, F10). */
export default function ExaminerActionBar() {
  const {
    selectedClaim,
    currentUser,
    selectedReasonCode,
    setSelectedReasonCode,
    actionComment,
    setActionComment,
    handleExaminerReview,
  } = useClaimLens();

  return (
    <div className="bg-white border-2 border-indigo-600/80 rounded-2xl p-5 shadow-md space-y-4">
      <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-100 pb-3">
        <div className="text-xs font-bold uppercase tracking-wider text-indigo-950 flex items-center gap-2">
          <UserCheck className="w-4 h-4 text-indigo-600" />
          Human Approval Point #2 — Examiner Adjudication Recommendation (
          <code className="font-mono text-indigo-600">POST /claims/{selectedClaim.id}/review</code>)
        </div>
        <span className="text-xs text-slate-500">
          Signed in as: <strong className="text-slate-800">{currentUser.name}</strong> ({currentUser.role})
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-12 gap-4 items-end">
        <div className="md:col-span-4">
          <label className="block text-xs font-semibold text-slate-700 mb-1.5">
            Standardized Reason Code (Required for Denial)
          </label>
          <select
            value={selectedReasonCode}
            onChange={(e) => setSelectedReasonCode(e.target.value)}
            className="w-full border border-slate-300 rounded-xl px-3 py-2 text-xs font-medium bg-slate-50 focus:bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500/20"
          >
            {REASON_CODES.map((rc) => (
              <option key={rc.code} value={rc.code}>
                {rc.label}
              </option>
            ))}
          </select>
        </div>

        <div className="md:col-span-4">
          <label className="block text-xs font-semibold text-slate-700 mb-1.5">
            Examiner Audit Note / Rationale
          </label>
          <input
            type="text"
            value={actionComment}
            onChange={(e) => setActionComment(e.target.value)}
            placeholder="Cite line numbers or documentation gap..."
            className="w-full border border-slate-300 rounded-xl px-3 py-2 text-xs bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500/20"
          />
        </div>

        <div className="md:col-span-4 flex flex-wrap gap-2 justify-end">
          <button
            onClick={() => handleExaminerReview('approve')}
            className="px-4 py-2.5 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold rounded-xl shadow-xs transition flex items-center gap-1.5 cursor-pointer"
          >
            <Check className="w-4 h-4" /> Approve
          </button>
          <button
            onClick={() => handleExaminerReview('request_records')}
            className="px-4 py-2.5 bg-amber-500 hover:bg-amber-400 text-white text-xs font-semibold rounded-xl shadow-xs transition flex items-center gap-1.5 cursor-pointer"
          >
            <FileWarning className="w-4 h-4" /> Request Records
          </button>
          <button
            onClick={() => handleExaminerReview('recommend_denial')}
            className="px-4 py-2.5 bg-rose-600 hover:bg-rose-500 text-white text-xs font-semibold rounded-xl shadow-xs transition flex items-center gap-1.5 cursor-pointer"
          >
            <XCircle className="w-4 h-4" /> Recommend Denial
          </button>
        </div>
      </div>
    </div>
  );
}
