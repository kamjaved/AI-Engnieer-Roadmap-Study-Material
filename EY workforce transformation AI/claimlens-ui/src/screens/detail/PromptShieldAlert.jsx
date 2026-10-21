import { ShieldAlert } from 'lucide-react';
import { useClaimLens } from '../../context/useClaimLens';

/** Shown only when Prompt Shields flagged an indirect attack inside the encounter note. */
export default function PromptShieldAlert() {
  const { selectedClaim } = useClaimLens();

  if (selectedClaim.note_meta?.prompt_shield !== 'INDIRECT_ATTACK_DETECTED') return null;

  return (
    <div className="bg-rose-50 border border-rose-300 rounded-2xl p-4 flex flex-wrap items-center justify-between gap-4 text-xs shadow-2xs">
      <div className="flex items-start gap-3">
        <div className="p-2 rounded-xl bg-rose-100 text-rose-700">
          <ShieldAlert className="w-5 h-5 shrink-0" />
        </div>
        <div>
          <div className="font-bold text-rose-950 text-sm">
            Azure Prompt Shields Guardrail Triggered — Indirect Prompt Attack Isolated
          </div>
          <div className="text-rose-800 mt-0.5 leading-relaxed">
            The encounter note contains adversarial instructions attempting to override claim status. Isolated
            strictly as untrusted data; AI models have zero write tools (§10).
          </div>
        </div>
      </div>
      <span className="px-3 py-1 bg-rose-700 text-white text-[11px] font-bold rounded-full shrink-0">
        STATE CHANGE BLOCKED
      </span>
    </div>
  );
}
