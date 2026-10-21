import { FileText } from 'lucide-react';
import { useClaimLens } from '../../context/useClaimLens';

/** Encounter note, treated as untrusted input. */
export default function EncounterNotePanel() {
  const { selectedClaim } = useClaimLens();

  return (
    <div className="lg:col-span-4 bg-white border border-slate-200 rounded-2xl p-5 shadow-2xs flex flex-col justify-between space-y-4">
      <div className="space-y-3">
        <div className="flex items-center justify-between border-b border-slate-100 pb-3">
          <span className="text-xs font-bold uppercase tracking-wider text-slate-700 flex items-center gap-1.5">
            <FileText className="w-4 h-4 text-indigo-600" />
            Outpatient Encounter Note
          </span>
          <span className="text-[10px] font-semibold px-2 py-0.5 bg-slate-100 text-slate-600 border border-slate-200 rounded-full">
            Untrusted Input
          </span>
        </div>

        <div className="p-4 bg-amber-50/30 border border-slate-200/90 rounded-xl text-sm leading-relaxed text-slate-800">
          "{selectedClaim.encounter_note}"
        </div>
      </div>

      <div className="border-t border-slate-100 pt-3 text-xs text-slate-500 space-y-1.5">
        <div className="flex justify-between">
          <span>Generator Model:</span>
          <strong className="font-mono text-slate-700">{selectedClaim.note_meta?.generator_model}</strong>
        </div>
        <div className="flex justify-between">
          <span>Prompt Version:</span>
          <strong className="font-mono text-slate-700">
            {selectedClaim.note_meta?.prompt_version} (seed {selectedClaim.note_meta?.seed})
          </strong>
        </div>
        <div className="flex justify-between">
          <span>Prompt Shields Status:</span>
          <strong
            className={`font-mono ${
              selectedClaim.note_meta?.prompt_shield === 'CLEAN' ? 'text-emerald-600' : 'text-rose-600'
            }`}
          >
            {selectedClaim.note_meta?.prompt_shield}
          </strong>
        </div>
      </div>
    </div>
  );
}
