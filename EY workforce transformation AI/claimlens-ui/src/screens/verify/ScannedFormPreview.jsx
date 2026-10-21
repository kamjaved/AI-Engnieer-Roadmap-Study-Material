import { Eye } from 'lucide-react';

/** Left pane: stylised CMS-1500 with the low-confidence box highlighted (§3.4 F17). */
export default function ScannedFormPreview() {
  return (
    <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-2xs space-y-4">
      <div className="flex items-center justify-between border-b border-slate-100 pb-3">
        <div className="flex items-center gap-2">
          <Eye className="w-4 h-4 text-indigo-600" />
          <span className="text-xs font-bold text-slate-800">
            Scanned CMS-1500 Document (bills/bill_00042_noisy.pdf)
          </span>
        </div>
        <span className="text-[11px] font-medium px-2.5 py-0.5 bg-emerald-50 text-emerald-700 border border-emerald-200 rounded-full">
          Bounding Boxes Active
        </span>
      </div>

      {/* Stylized CMS-1500 Form Preview */}
      <div className="bg-stone-50 border border-stone-200/90 rounded-xl p-5 font-mono text-xs space-y-4 shadow-inner">
        <div className="flex justify-between items-center border-b border-stone-300 pb-2.5">
          <div>
            <div className="font-bold text-sm text-stone-900">HEALTH INSURANCE CLAIM FORM (CMS-1500)</div>
            <div className="text-[10px] text-stone-500">
              SYNTHETIC RENDERED BILL — REPORTLAB + SCAN NOISE (±1.8° ROTATION)
            </div>
          </div>
          <span className="px-2 py-0.5 bg-rose-100 text-rose-800 border border-rose-200 font-bold text-[10px] rounded">
            CARRIER / PART B
          </span>
        </div>

        {/* Box 1-21 Header */}
        <div className="grid grid-cols-2 gap-3 bg-white p-3 rounded-lg border border-stone-200">
          <div className="border border-emerald-400 bg-emerald-50/40 p-2 rounded-md">
            <div className="text-[10px] text-emerald-700 font-semibold">2. PATIENT TOKEN [conf: 0.99]</div>
            <div className="font-bold text-slate-900 mt-0.5">SYN-PT-90412 (68M)</div>
          </div>
          <div className="border border-emerald-400 bg-emerald-50/40 p-2 rounded-md">
            <div className="text-[10px] text-emerald-700 font-semibold">
              21. DIAGNOSIS ICD-10 [conf: 0.94]
            </div>
            <div className="font-bold text-slate-900 mt-0.5">A. M54.50 (Low back pain)</div>
          </div>
        </div>

        {/* Box 24 Service Lines with Highlighted Bounding Box on Line 2 Box 24G */}
        <div className="border border-stone-200 bg-white p-3 rounded-lg space-y-2.5">
          <div className="text-[10px] font-bold text-stone-500 border-b border-stone-200 pb-1.5">
            24. SERVICE LINES (A. DOS | B. POS | D. CPT/HCPCS | E. DX | F. CHARGES | G. UNITS | J. NPI)
          </div>

          {/* Line 1 */}
          <div className="grid grid-cols-7 gap-1 items-center text-[11px] p-2 border border-emerald-400 bg-emerald-50/30 rounded-md">
            <span>2026-10-11</span>
            <span>11</span>
            <span className="font-bold text-slate-900">97110</span>
            <span>A</span>
            <span>$160.00</span>
            <span className="font-bold text-emerald-800">2</span>
            <span className="text-[10px]">1982654328</span>
          </div>

          {/* Line 2 (Highlighted Low Confidence Box 24G) */}
          <div className="grid grid-cols-7 gap-1 items-center text-[11px] p-2 border border-stone-200 bg-stone-50/70 rounded-md">
            <span>2026-10-11</span>
            <span>11</span>
            <span className="font-bold text-slate-900">97140</span>
            <span>A</span>
            <span>$520.00</span>
            <div className="border-2 border-rose-600 bg-amber-100 px-1.5 py-1 font-bold text-rose-950 rounded-md shadow-xs">
              <span className="line-through opacity-50 mr-1">2</span>8?
              <span className="block text-[9px] bg-rose-600 text-white px-1 mt-0.5 rounded">0.64</span>
            </div>
            <span className="text-[10px]">1982654328</span>
          </div>
        </div>

        {/* Box 28-33 Footer */}
        <div className="grid grid-cols-2 gap-3 border border-stone-200 bg-white p-3 rounded-lg">
          <div>
            <div className="text-[10px] text-stone-500">28. TOTAL CHARGE</div>
            <div className="font-bold text-slate-900 mt-0.5">$680.00</div>
          </div>
          <div className="border border-emerald-400 bg-emerald-50/40 p-2 rounded-md">
            <div className="text-[10px] text-emerald-700 font-semibold">33. BILLING NPI [conf: 0.97]</div>
            <div className="font-bold text-slate-900 mt-0.5">1245319599</div>
          </div>
        </div>

        <div className="p-3 bg-white border border-stone-200 rounded-lg text-xs font-sans text-slate-700 leading-relaxed">
          <strong className="text-slate-900">Attached Encounter Note Snippet:</strong> "...Performed 30
          minutes (2 units) of supervised therapeutic lumbar stabilization exercises and{' '}
          <strong className="bg-amber-100 px-1 rounded text-amber-950">
            30 minutes (2 units) of myofascial manual therapy (97140)
          </strong>
          ..."
        </div>
      </div>
    </div>
  );
}
