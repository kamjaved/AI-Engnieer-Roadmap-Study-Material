import { Upload, CheckCircle2 } from 'lucide-react';
import { useClaimLens } from '../../context/useClaimLens';

export default function PdfUploadTab() {
  const { pdfScanMode, setPdfScanMode } = useClaimLens();

  return (
    <>
      <div className="text-xs text-indigo-950 bg-indigo-50/70 p-4 border border-indigo-100 rounded-xl leading-relaxed">
        <strong className="font-semibold">POST /claims/upload</strong> → Stores PDF in Azure Blob Storage{' '}
        <code className="font-mono bg-white px-1.5 py-0.5 rounded border border-indigo-100">bills/</code> →
        Worker invokes Azure Content Understanding custom analyzer{' '}
        <code className="font-mono bg-white px-1.5 py-0.5 rounded border border-indigo-100">
          claimlens-cms1500
        </code>{' '}
        (completion model: <code className="font-mono">gpt-5.2</code>,{' '}
        <code className="font-mono">estimateFieldSourceAndConfidence: true</code>).
      </div>

      <div className="border-2 border-dashed border-indigo-200 rounded-2xl bg-slate-50/60 p-8 text-center space-y-2 hover:border-indigo-400 transition">
        <div className="w-12 h-12 rounded-2xl bg-indigo-100 text-indigo-600 flex items-center justify-center mx-auto mb-2">
          <Upload className="w-6 h-6" />
        </div>
        <div className="text-sm font-bold text-slate-800">Drop CMS-1500 style PDF or PNG scan here</div>
        <div className="text-xs text-slate-500">
          Ready sample file:{' '}
          <span className="font-mono font-semibold text-slate-700">cms1500_rendered_sample_042.pdf</span>{' '}
          (Boxes 21 & 24A–24J)
        </div>
      </div>

      <div className="space-y-3">
        <label className="text-xs font-semibold uppercase tracking-wider text-slate-500">
          Simulate Content Understanding Extraction Confidence Outcome
        </label>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <button
            onClick={() => setPdfScanMode('noisy')}
            className={`p-4 text-left border rounded-2xl transition cursor-pointer ${
              pdfScanMode === 'noisy'
                ? 'border-amber-500 bg-amber-50/50 ring-2 ring-amber-500/20'
                : 'border-slate-200 hover:border-slate-300'
            }`}
          >
            <div className="text-xs font-bold text-slate-900 flex items-center justify-between">
              <span>Option A: Noisy Scan (Confidence &lt; 0.80)</span>
              {pdfScanMode === 'noisy' && <CheckCircle2 className="w-4 h-4 text-amber-600" />}
            </div>
            <p className="text-xs text-slate-600 mt-1.5 leading-relaxed">
              Simulates ±2° rotation + blur where Box 24G <code className="font-mono">units</code> confidence
              is <code className="font-mono font-bold text-amber-800">0.64</code>. Routes to{' '}
              <code className="font-mono">NEEDS_FIELD_VERIFICATION</code> (Human Approval Point #1).
            </p>
          </button>
          <button
            onClick={() => setPdfScanMode('clean')}
            className={`p-4 text-left border rounded-2xl transition cursor-pointer ${
              pdfScanMode === 'clean'
                ? 'border-emerald-500 bg-emerald-50/50 ring-2 ring-emerald-500/20'
                : 'border-slate-200 hover:border-slate-300'
            }`}
          >
            <div className="text-xs font-bold text-slate-900 flex items-center justify-between">
              <span>Option B: Clean Rendered PDF (All ≥ 0.80)</span>
              {pdfScanMode === 'clean' && <CheckCircle2 className="w-4 h-4 text-emerald-600" />}
            </div>
            <p className="text-xs text-slate-600 mt-1.5 leading-relaxed">
              All critical fields pass confidence gate. Advances automatically through Rules + Decision-1 to{' '}
              <code className="font-mono">READY_FOR_REVIEW</code>.
            </p>
          </button>
        </div>
      </div>
    </>
  );
}
