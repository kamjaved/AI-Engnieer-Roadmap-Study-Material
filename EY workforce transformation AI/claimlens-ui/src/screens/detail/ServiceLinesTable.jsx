import { CheckCircle2 } from 'lucide-react';
import { useClaimLens } from '../../context/useClaimLens';

/** Service lines (CMS-1500 Box 24A-24J) with flags per line. */
export default function ServiceLinesTable() {
  const { selectedClaim } = useClaimLens();

  return (
    <div className="bg-white border border-slate-200 rounded-2xl shadow-2xs overflow-hidden">
      <div className="bg-slate-50/80 border-b border-slate-200 px-5 py-3 flex flex-wrap items-center justify-between gap-2">
        <span className="text-xs font-bold uppercase tracking-wider text-slate-700">
          Service Lines (CMS-1500 Box 24A–24J)
        </span>
        <span className="text-xs text-slate-500">
          Fee Benchmark:{' '}
          <span className="font-mono font-medium text-slate-700">PFREV26D-nonQP (Oct 2026)</span> & Peer
          Charge p99
        </span>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse text-xs">
          <thead>
            <tr className="border-b border-slate-200 text-[11px] font-semibold uppercase tracking-wider text-slate-500 bg-slate-50/40">
              <th className="py-3 px-4">Line</th>
              <th className="py-3 px-4">DOS / POS</th>
              <th className="py-3 px-4">CPT / HCPCS & Description</th>
              <th className="py-3 px-4">Modifiers</th>
              <th className="py-3 px-4">Diagnosis (ICD-10-CM)</th>
              <th className="py-3 px-4 text-right">Units</th>
              <th className="py-3 px-4 text-right">Billed Charge</th>
              <th className="py-3 px-4 text-right">PFS / Peer p99</th>
              <th className="py-3 px-4">Active Flags</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {selectedClaim.lines.map((line) => (
              <tr key={line.line_no} className={line.flags.length > 0 ? 'bg-rose-50/30' : 'bg-white'}>
                <td className="py-3 px-4 font-mono font-bold text-slate-700">#{line.line_no}</td>
                <td className="py-3 px-4 font-mono">
                  <div className="text-slate-800">{line.dos}</div>
                  <div className="text-[11px] text-slate-400">POS: {line.pos}</div>
                </td>
                <td className="py-3 px-4">
                  <span className="font-mono font-bold text-indigo-700 text-sm">{line.code}</span>
                  <div className="text-xs text-slate-600 mt-0.5">{line.code_desc}</div>
                </td>
                <td className="py-3 px-4 font-mono">
                  {line.modifiers.length > 0 ? (
                    line.modifiers.map((m) => (
                      <span
                        key={m}
                        className="px-2 py-0.5 bg-slate-100 border border-slate-300 rounded-md text-slate-800 font-bold mr-1"
                      >
                        {m}
                      </span>
                    ))
                  ) : (
                    <span className="text-slate-300">—</span>
                  )}
                </td>
                <td className="py-3 px-4">
                  <div className="font-mono font-bold text-slate-800">{line.dx_codes.join(', ')}</div>
                  <div className="text-[11px] text-slate-500">{line.dx_desc?.[0]}</div>
                </td>
                <td className="py-3 px-4 font-mono text-right font-bold text-slate-900">{line.units}</td>
                <td className="py-3 px-4 font-mono text-right font-bold text-slate-900">
                  ${line.charge.toFixed(2)}
                </td>
                <td className="py-3 px-4 font-mono text-right text-[11px] text-slate-500">
                  <div>PFS: ${line.pfs_rate.toFixed(2)}</div>
                  <div>p99: ${line.peer_p99.toFixed(2)}</div>
                </td>
                <td className="py-3 px-4">
                  {line.flags.length > 0 ? (
                    <div className="flex flex-wrap gap-1">
                      {line.flags.map((flg) => (
                        <span
                          key={flg}
                          className="px-2 py-0.5 bg-rose-100 border border-rose-300 rounded-md text-rose-800 font-mono text-[11px] font-bold"
                        >
                          ⚑ {flg}
                        </span>
                      ))}
                    </div>
                  ) : (
                    <span className="inline-flex items-center gap-1 text-emerald-600 font-semibold text-xs">
                      <CheckCircle2 className="w-3.5 h-3.5" /> Clean
                    </span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
