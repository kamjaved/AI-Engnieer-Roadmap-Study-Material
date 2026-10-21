import { Play } from 'lucide-react';
import { useClaimLens } from '../../context/useClaimLens';
import PdfUploadTab from './PdfUploadTab';
import JsonPasteTab from './JsonPasteTab';
import BatchTab from './BatchTab';

/** Submit a claim: PDF scan, structured JSON, or batch (§3.5 #3, F2, F3, F4). */
export default function SubmitScreen() {
  const { setActiveScreen, submitTab, setSubmitTab, handleCreateClaim } = useClaimLens();

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900">Submit Claim to Pipeline</h1>
          <p className="text-sm text-slate-500 mt-0.5">
            Asynchronous claim ingestion returning{' '}
            <code className="font-mono text-xs bg-slate-100 px-1.5 py-0.5 rounded">HTTP 202 Accepted</code>{' '}
            and queuing worker execution.
          </p>
        </div>
        <button
          onClick={() => setActiveScreen('queue')}
          className="px-3.5 py-2 text-xs font-semibold border border-slate-200 rounded-xl bg-white hover:bg-slate-50 text-slate-700 shadow-2xs cursor-pointer"
        >
          ← Back to Work Queue
        </button>
      </div>

      {/* 3 Input Path Tabs */}
      <div className="bg-white border border-slate-200 rounded-2xl shadow-2xs overflow-hidden">
        <div className="grid grid-cols-1 sm:grid-cols-3 border-b border-slate-200 bg-slate-50/70 p-1.5 gap-1.5">
          <button
            onClick={() => setSubmitTab('pdf')}
            className={`py-2.5 px-4 text-xs font-semibold rounded-xl transition cursor-pointer ${
              submitTab === 'pdf'
                ? 'bg-white text-indigo-700 shadow-xs border border-slate-200/80'
                : 'text-slate-600 hover:text-slate-900 hover:bg-white/60'
            }`}
          >
            1. Upload Scanned Bill (PDF / PNG)
          </button>
          <button
            onClick={() => setSubmitTab('json')}
            className={`py-2.5 px-4 text-xs font-semibold rounded-xl transition cursor-pointer ${
              submitTab === 'json'
                ? 'bg-white text-indigo-700 shadow-xs border border-slate-200/80'
                : 'text-slate-600 hover:text-slate-900 hover:bg-white/60'
            }`}
          >
            2. Paste Structured JSON (837P)
          </button>
          <button
            onClick={() => setSubmitTab('batch')}
            className={`py-2.5 px-4 text-xs font-semibold rounded-xl transition cursor-pointer ${
              submitTab === 'batch'
                ? 'bg-white text-indigo-700 shadow-xs border border-slate-200/80'
                : 'text-slate-600 hover:text-slate-900 hover:bg-white/60'
            }`}
          >
            3. Batch Evaluation Run (JSONL)
          </button>
        </div>

        <div className="p-6 space-y-6">
          {submitTab === 'pdf' && <PdfUploadTab />}
          {submitTab === 'json' && <JsonPasteTab />}
          {submitTab === 'batch' && <BatchTab />}

          <div className="flex justify-end gap-3 pt-4 border-t border-slate-100">
            <button
              onClick={() => setActiveScreen('queue')}
              className="px-4 py-2.5 text-xs font-semibold border border-slate-200 rounded-xl hover:bg-slate-50 text-slate-600 cursor-pointer"
            >
              Cancel
            </button>
            <button
              onClick={handleCreateClaim}
              className="px-5 py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold rounded-xl shadow-sm shadow-indigo-500/20 flex items-center gap-2 cursor-pointer"
            >
              <Play className="w-3.5 h-3.5 fill-current" /> Submit to Pipeline (202 Accepted)
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
