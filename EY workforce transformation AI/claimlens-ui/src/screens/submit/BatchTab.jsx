export default function BatchTab() {
  return (
    <div className="space-y-4">
      <div className="text-xs text-indigo-950 bg-indigo-50/70 p-4 border border-indigo-100 rounded-xl leading-relaxed">
        <strong>POST /claims/batch (Admin / CLI Eval Harness)</strong> — Runs{' '}
        <code className="font-mono">gold_test.jsonl</code> (1,000 frozen claims) or{' '}
        <code className="font-mono">dev_set.jsonl</code> (2,000 claims) through the exact same worker pipeline
        code (§4.4).
      </div>
      <div className="p-5 border border-slate-200 rounded-2xl bg-slate-50 space-y-2.5 text-xs">
        <div>
          <span className="text-slate-500">Selected Dataset:</span>{' '}
          <strong className="font-mono text-slate-900">Blob gold/gold_test.jsonl</strong> (1,000 claims,
          frozen Day 6)
        </div>
        <div>
          <span className="text-slate-500">SHA-256 Lineage Hash:</span>{' '}
          <code className="font-mono text-[11px] bg-white px-2 py-0.5 rounded border border-slate-200">
            e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
          </code>
        </div>
        <div>
          <span className="text-slate-500">Stratified Slices:</span>{' '}
          <span className="font-medium text-slate-800">
            CLEAN (400), E1-NEG (100), E1/E1-HARD (100), E2 (100), E3 (75), E4 (75), E5 (75), E6 (50), E7 (25)
          </span>
        </div>
      </div>
    </div>
  );
}
