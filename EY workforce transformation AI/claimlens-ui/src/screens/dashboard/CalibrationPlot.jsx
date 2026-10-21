import { CALIBRATION_BINS } from '../../data/evalMetrics';

/** Decision-1 reliability plot (predicted probability vs empirical accuracy). */
export default function CalibrationPlot() {
  return (
    <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-2xs space-y-3">
      <div className="flex justify-between items-center text-xs">
        <span className="font-bold uppercase tracking-wider text-slate-700">Decision-1 Calibration Plot</span>
        <span className="px-2 py-0.5 bg-emerald-50 text-emerald-700 border border-emerald-200 rounded-full font-mono font-semibold">
          ECE = 0.031
        </span>
      </div>
      <p className="text-xs text-slate-500">
        Compares predicted probability bins against empirical accuracy on E5/E6/E7 + CLEAN slices (§11.1).
      </p>
      <div className="h-36 border border-slate-200 rounded-xl bg-slate-50/70 p-4 flex items-end justify-between gap-3 font-mono text-[10px]">
        {CALIBRATION_BINS.map((b) => (
          <div key={b.bin} className="flex-1 flex flex-col items-center gap-1.5 h-full justify-end">
            <div className="w-full flex gap-1 items-end justify-center h-24">
              <div
                title={`Predicted: ${b.pred}%`}
                className="w-3.5 bg-indigo-300 rounded-t"
                style={{ height: `${b.pred}%` }}
              />
              <div
                title={`Empirical: ${b.emp}%`}
                className="w-3.5 bg-indigo-600 rounded-t"
                style={{ height: `${b.emp}%` }}
              />
            </div>
            <span className="text-slate-600">p≈{b.bin}</span>
          </div>
        ))}
      </div>
      <div className="flex justify-between text-[11px] text-slate-500">
        <span className="flex items-center gap-1.5">
          <span className="w-2.5 h-2.5 rounded-xs bg-indigo-300 inline-block" /> Predicted Probability
        </span>
        <span className="flex items-center gap-1.5">
          <span className="w-2.5 h-2.5 rounded-xs bg-indigo-600 inline-block" /> Empirical Accuracy
        </span>
      </div>
    </div>
  );
}
