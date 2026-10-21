import { Sparkles, X, Lock } from 'lucide-react';
import { useClaimLens } from '../../context/useClaimLens';
import { COPILOT_QUICK_PROMPTS } from '../../data/copilotPrompts';

/** "Ask ClaimLens" side drawer (§3.5 #8, §8.4, F14). Read-only tools only: it cannot change claim state. */
export default function CopilotDrawer() {
  const {
    copilotOpen,
    setCopilotOpen,
    selectedClaim,
    currentUser,
    chatMessages,
    chatInput,
    setChatInput,
    handleSendCopilot,
  } = useClaimLens();

  if (!copilotOpen) return null;

  return (
    <aside className="w-96 bg-white border-l border-slate-200 shadow-xl flex flex-col justify-between shrink-0">
      <div className="p-4 bg-gradient-to-r from-indigo-600 to-blue-600 text-white flex items-center justify-between">
        <div>
          <div className="text-xs font-bold flex items-center gap-1.5">
            <Sparkles className="w-4 h-4 text-amber-300" /> Ask ClaimLens Copilot ({selectedClaim.id})
          </div>
          <div className="text-[11px] text-indigo-100 mt-0.5">
            Foundry Agent Service • Toolbox MCP • Foundry IQ
          </div>
        </div>
        <button
          onClick={() => setCopilotOpen(false)}
          className="text-indigo-100 hover:text-white cursor-pointer"
        >
          <X className="w-4 h-4" />
        </button>
      </div>

      {/* Quick Scripted Questions (§8.4, §13 B21) */}
      <div className="p-3 bg-slate-50 border-b border-slate-200 space-y-2">
        <div className="text-[10px] font-bold uppercase tracking-wider text-slate-400">
          Quick Examiner Prompts (Read-Only MCP Tools)
        </div>
        <div className="flex flex-wrap gap-1.5">
          {COPILOT_QUICK_PROMPTS.map((q) => (
            <button
              key={q.prompt}
              onClick={() => handleSendCopilot(q.prompt)}
              className="text-[11px] font-medium px-2.5 py-1 bg-white border border-slate-200 rounded-lg hover:border-indigo-300 hover:text-indigo-700 text-left transition cursor-pointer"
            >
              {q.label}
            </button>
          ))}
        </div>
      </div>

      {/* Chat Message History */}
      <div className="flex-1 overflow-y-auto p-4 space-y-3 text-xs">
        {chatMessages.map((m, idx) => (
          <div
            key={idx}
            className={`p-3.5 rounded-2xl space-y-2 ${
              m.role === 'user'
                ? 'bg-indigo-600 text-white ml-6 shadow-xs'
                : 'bg-slate-100 text-slate-800 border border-slate-200/80 mr-4'
            }`}
          >
            <div className="text-[10px] font-semibold uppercase opacity-75">
              {m.role === 'user'
                ? `${currentUser.name} (${currentUser.role})`
                : 'Foundry Agent (Responses API)'}
            </div>
            <div className="leading-relaxed">{m.text}</div>
            {m.toolCall && (
              <div className="p-2 bg-white border border-slate-200 rounded-xl font-mono text-[10px] text-indigo-900">
                🔧 <strong>MCP Tool:</strong> <code>{m.toolCall}</code>
              </div>
            )}
            {m.citation && (
              <div className="p-2 bg-white border border-slate-200 rounded-xl text-[11px] text-slate-600">
                📚 <strong>Foundry IQ:</strong> {m.citation}
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Chat Input */}
      <div className="p-3.5 border-t border-slate-200 bg-slate-50 space-y-2">
        <div className="text-[11px] text-slate-500 flex items-center gap-1">
          <Lock className="w-3 h-3 text-slate-400" />
          Read-only MCP tools only. Copilot cannot mutate claim state.
        </div>
        <div className="flex gap-2">
          <input
            type="text"
            value={chatInput}
            onChange={(e) => setChatInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSendCopilot()}
            placeholder="Ask about PTP pairs, MUEs, or policy..."
            className="flex-1 border border-slate-300 rounded-xl px-3 py-2 text-xs bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500/20"
          />
          <button
            onClick={() => handleSendCopilot()}
            className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold rounded-xl transition cursor-pointer"
          >
            Send
          </button>
        </div>
      </div>
    </aside>
  );
}
