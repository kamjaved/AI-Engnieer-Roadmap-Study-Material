import { CheckCircle2 } from 'lucide-react';
import KpiStrip from './KpiStrip';
import GoldSetBreakdown from './GoldSetBreakdown';
import CalibrationPlot from './CalibrationPlot';
import ThresholdConfig from './ThresholdConfig';

/** Metrics, evaluation harness and thresholds (§3.5 #7, §11, F12, F15, F16). */
export default function DashboardScreen() {
  return (
    <div className="max-w-7xl mx-auto space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900">
            Evaluation Harness, Calibration & Routing Thresholds
          </h1>
          <p className="text-sm text-slate-500 mt-0.5">
            Evaluation by Construction (§5.4-D, §11): Measured on frozen{' '}
            <code className="font-mono text-xs bg-slate-100 px-1.5 py-0.5 rounded">gold_test.jsonl</code>{' '}
            (1,000 synthetic claims with planted ground-truth labels).
          </p>
        </div>
        <span className="px-3.5 py-1.5 bg-emerald-50 text-emerald-700 border border-emerald-200 text-xs font-bold rounded-full flex items-center gap-1.5">
          <CheckCircle2 className="w-4 h-4 text-emerald-600" />
          CI Gate (eval-smoke 100 claims): PASSING
        </span>
      </div>

      {/* Business KPI Cards (§11.2) */}
      <KpiStrip />

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        <GoldSetBreakdown />

        {/* Right column: calibration plot + threshold config */}
        <div className="lg:col-span-5 space-y-5">
          <CalibrationPlot />
          <ThresholdConfig />
        </div>
      </div>
    </div>
  );
}
