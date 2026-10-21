const statusMap = {
  NEEDS_FIELD_VERIFICATION: 'bg-amber-50 text-amber-800 border-amber-200',
  READY_FOR_REVIEW: 'bg-indigo-50 text-indigo-700 border-indigo-200',
  DENIAL_RECOMMENDED: 'bg-purple-50 text-purple-700 border-purple-200',
  DENIAL_CONFIRMED: 'bg-rose-100 text-rose-800 border-rose-300',
  APPROVED: 'bg-emerald-50 text-emerald-700 border-emerald-200',
  RECORDS_REQUESTED: 'bg-orange-50 text-orange-800 border-orange-200',
  REJECTED_INVALID: 'bg-slate-200 text-slate-700 border-slate-300',
};

export default function StatusBadge({ status }) {
  return (
    <span
      className={`inline-flex items-center px-2.5 py-1 rounded-md text-xs font-medium border ${
        statusMap[status] || 'bg-slate-100 text-slate-700 border-slate-200'
      }`}
    >
      {status.replace(/_/g, ' ')}
    </span>
  );
}
