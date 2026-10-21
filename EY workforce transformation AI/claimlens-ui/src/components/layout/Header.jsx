import {
  ShieldCheck,
  Layers,
  Upload,
  Edit3,
  FileText,
  UserCheck,
  BarChart3,
  Sparkles,
  LogOut,
} from 'lucide-react';
import { useClaimLens } from '../../context/useClaimLens';
import { USERS } from '../../data/users';
import NavTab from './NavTab';

export default function Header() {
  const {
    claims,
    supervisorQueue,
    activeScreen,
    setActiveScreen,
    setSelectedClaimId,
    copilotOpen,
    setCopilotOpen,
    currentRole,
    setCurrentRole,
    triggerToast,
  } = useClaimLens();

  return (
    <header className="bg-white border-b border-slate-200 px-5 py-3 sticky top-0 z-30 shadow-2xs">
      <div className="max-w-7xl mx-auto flex flex-wrap items-center justify-between gap-4">
        <div className="flex flex-wrap items-center gap-6">
          <div
            onClick={() => setActiveScreen('queue')}
            className="cursor-pointer flex items-center gap-2.5 group"
          >
            <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-indigo-600 to-blue-600 text-white font-bold flex items-center justify-center text-sm shadow-sm shadow-indigo-500/20 group-hover:scale-105 transition">
              <ShieldCheck className="w-5 h-5" />
            </div>
            <div>
              <div className="font-bold text-base leading-none tracking-tight text-slate-900">ClaimLens</div>
              <div className="text-[11px] text-slate-500 font-medium mt-0.5">
                Pre-Payment Integrity Copilot
              </div>
            </div>
          </div>

          {/* Primary Screen Tabs (§3.5) */}
          <nav className="flex flex-wrap items-center gap-1 bg-slate-100/80 p-1 rounded-xl border border-slate-200/60">
            <NavTab active={activeScreen === 'queue'} onClick={() => setActiveScreen('queue')}>
              <Layers className="w-3.5 h-3.5" />
              Work Queue
              <span className="px-1.5 py-0.2 text-[10px] rounded-full bg-slate-200/80 text-slate-700 font-mono">
                {claims.length}
              </span>
            </NavTab>
            <NavTab active={activeScreen === 'submit'} onClick={() => setActiveScreen('submit')}>
              <Upload className="w-3.5 h-3.5" /> Submit Claim
            </NavTab>
            <NavTab
              active={activeScreen === 'verify'}
              onClick={() => {
                setSelectedClaimId('CLM-2026-00042');
                setActiveScreen('verify');
              }}
            >
              <Edit3 className="w-3.5 h-3.5" /> OCR Verify
              <span className="px-1.5 py-0.2 text-[10px] rounded-full bg-amber-100 text-amber-800 font-semibold">
                HITL #1
              </span>
            </NavTab>
            <NavTab active={activeScreen === 'detail'} onClick={() => setActiveScreen('detail')}>
              <FileText className="w-3.5 h-3.5" /> Claim Review
              <span className="px-1.5 py-0.2 text-[10px] rounded-full bg-indigo-100 text-indigo-700 font-semibold">
                HITL #2
              </span>
            </NavTab>
            <NavTab active={activeScreen === 'supervisor'} onClick={() => setActiveScreen('supervisor')}>
              <UserCheck className="w-3.5 h-3.5" /> Supervisor
              <span className="px-1.5 py-0.2 text-[10px] rounded-full bg-purple-100 text-purple-800 font-semibold">
                {supervisorQueue.length}
              </span>
            </NavTab>
            <NavTab active={activeScreen === 'dashboard'} onClick={() => setActiveScreen('dashboard')}>
              <BarChart3 className="w-3.5 h-3.5" /> Eval & KPIs
            </NavTab>
          </nav>
        </div>

        {/* Right Controls: Copilot Toggle + Entra Role Switcher */}
        <div className="flex items-center gap-2.5">
          <button
            onClick={() => setCopilotOpen(!copilotOpen)}
            className={`px-3.5 py-2 text-xs font-semibold rounded-xl transition flex items-center gap-1.5 cursor-pointer shadow-2xs ${
              copilotOpen
                ? 'bg-indigo-600 text-white shadow-indigo-500/20'
                : 'bg-indigo-50 text-indigo-700 border border-indigo-200 hover:bg-indigo-100'
            }`}
          >
            <Sparkles className="w-3.5 h-3.5" />
            Ask ClaimLens AI
          </button>

          <div className="flex items-center border border-slate-200 rounded-xl bg-slate-50 px-3 py-1.5 text-xs">
            <span className="text-[11px] font-medium text-slate-400 mr-1.5">Role:</span>
            <select
              value={currentRole}
              onChange={(e) => {
                setCurrentRole(e.target.value);
                triggerToast(
                  `Switched Entra ID token role to ${e.target.value} (${USERS[e.target.value].name})`
                );
              }}
              className="bg-transparent font-semibold text-slate-800 focus:outline-none cursor-pointer"
            >
              <option value="Examiner">Examiner (Alex Rivera)</option>
              <option value="Supervisor">Supervisor (Dana Sterling)</option>
              <option value="Admin">Admin / Analyst (Priya Nair)</option>
            </select>
          </div>

          <button
            onClick={() => setActiveScreen('login')}
            title="Switch Entra Persona / Sign Out"
            className="p-2 border border-slate-200 rounded-xl hover:bg-slate-100 text-slate-500 hover:text-slate-800 transition cursor-pointer"
          >
            <LogOut className="w-4 h-4" />
          </button>
        </div>
      </div>
    </header>
  );
}
