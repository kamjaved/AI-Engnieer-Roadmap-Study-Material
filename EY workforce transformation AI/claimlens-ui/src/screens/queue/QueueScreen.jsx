import { Upload } from 'lucide-react';
import { useClaimLens } from '../../context/useClaimLens';
import QueueSummaryStrip from './QueueSummaryStrip';
import QueueFilters from './QueueFilters';
import QueueTable from './QueueTable';

/** Examiner work queue (§3.5 #2, F8). */
export default function QueueScreen() {
  const { setActiveScreen } = useClaimLens();

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900">Examiner Work Queue</h1>
          <p className="text-sm text-slate-500 mt-0.5">
            Prioritized pre-payment review queue sorted by Risk Bucket (
            <span className="font-semibold text-rose-600">RED</span> →{' '}
            <span className="font-semibold text-amber-600">AMBER</span> →{' '}
            <span className="font-semibold text-emerald-600">GREEN</span>) and Dollars at Risk.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => setActiveScreen('submit')}
            className="px-4 py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold rounded-xl shadow-sm shadow-indigo-500/20 transition flex items-center gap-2 cursor-pointer"
          >
            <Upload className="w-4 h-4" /> Submit New Claim
          </button>
        </div>
      </div>

      <QueueSummaryStrip />
      <QueueFilters />
      <QueueTable />
    </div>
  );
}
