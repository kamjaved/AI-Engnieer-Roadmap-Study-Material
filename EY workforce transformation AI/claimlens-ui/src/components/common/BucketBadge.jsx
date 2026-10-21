const styles = {
  RED: 'bg-rose-50 text-rose-700 border-rose-200 ring-1 ring-rose-500/10',
  AMBER: 'bg-amber-50 text-amber-800 border-amber-200 ring-1 ring-amber-500/10',
  GREEN: 'bg-emerald-50 text-emerald-700 border-emerald-200 ring-1 ring-emerald-500/10',
  PENDING: 'bg-sky-50 text-sky-700 border-sky-200 ring-1 ring-sky-500/10',
  REJECTED: 'bg-slate-100 text-slate-700 border-slate-300',
};

const dotStyles = {
  RED: 'bg-rose-500 animate-pulse',
  AMBER: 'bg-amber-500',
  GREEN: 'bg-emerald-500',
  PENDING: 'bg-sky-500 animate-pulse',
  REJECTED: 'bg-slate-400',
};

export default function BucketBadge({ bucket, isQa = false }) {
  return (
    <span
      className={`inline-flex items-center gap-1.5 px-2.5 py-1 text-xs font-semibold border rounded-full shadow-2xs ${
        styles[bucket] || styles.PENDING
      }`}
    >
      <span className={`w-2 h-2 rounded-full ${dotStyles[bucket] || 'bg-slate-400'}`} />
      <span>{bucket}</span>
      {isQa && (
        <span className="ml-0.5 text-[10px] font-bold px-1.5 py-0.2 bg-emerald-600 text-white rounded-full">
          5% QA
        </span>
      )}
    </span>
  );
}
