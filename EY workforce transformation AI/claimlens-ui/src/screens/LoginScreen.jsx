import { ShieldAlert, ShieldCheck, CheckCircle2, Lock } from 'lucide-react';
import { useClaimLens } from '../context/useClaimLens';
import { USERS } from '../data/users';

/** Entra ID persona picker (§3.5 #1, F1). */
export default function LoginScreen() {
  const { currentRole, setCurrentRole, setIsLoggedIn, setActiveScreen } = useClaimLens();

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-indigo-950 text-slate-900 flex flex-col justify-between font-sans">
      <div className="bg-slate-950/80 backdrop-blur-md text-slate-200 text-xs py-2.5 px-6 flex flex-wrap items-center justify-between border-b border-slate-800">
        <div className="flex items-center gap-2.5">
          <span className="px-2 py-0.5 bg-amber-500/20 text-amber-300 border border-amber-400/30 font-semibold rounded-full text-[11px] flex items-center gap-1">
            <ShieldAlert className="w-3.5 h-3.5 text-amber-400" />
            SYNTHETIC DATA ONLY
          </span>
          <span className="text-slate-300">
            CMS DE-SynPUF + Synthetic NPIs — Human-in-the-Loop Pre-Payment Copilot. Never auto-denies.
          </span>
        </div>
        <span className="text-indigo-300 font-medium text-[11px] tracking-wide uppercase">
          ClaimLens Enterprise v1.0
        </span>
      </div>

      <div className="max-w-lg w-full mx-auto px-4 my-10">
        <div className="bg-white rounded-2xl border border-slate-200/80 p-8 shadow-2xl space-y-6">
          <div className="flex items-center gap-3.5 border-b border-slate-100 pb-5">
            <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-indigo-600 to-blue-600 text-white font-bold flex items-center justify-center text-lg shadow-md shadow-indigo-500/20">
              <ShieldCheck className="w-6 h-6" />
            </div>
            <div>
              <div className="text-[11px] font-semibold uppercase tracking-wider text-indigo-600">
                Microsoft Entra ID (MSAL Single Sign-On)
              </div>
              <h1 className="text-2xl font-bold tracking-tight text-slate-900">ClaimLens Intelligence</h1>
              <p className="text-xs text-slate-500 mt-0.5">
                Select an Entra ID App Role persona to preview RBAC and four-eyes controls.
              </p>
            </div>
          </div>

          <div className="space-y-3">
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-500">
              Select Active Persona
            </label>
            {Object.values(USERS).map((u) => {
              const isSelected = currentRole === u.role;
              return (
                <button
                  key={u.role}
                  onClick={() => setCurrentRole(u.role)}
                  className={`w-full text-left p-4 rounded-xl border transition-all flex items-center justify-between ${
                    isSelected
                      ? 'border-indigo-600 bg-indigo-50/50 ring-2 ring-indigo-600/20 shadow-xs'
                      : 'border-slate-200 hover:border-slate-300 hover:bg-slate-50'
                  }`}
                >
                  <div className="space-y-0.5">
                    <div className="text-sm font-bold text-slate-900 flex items-center gap-2">
                      {u.name}
                      {isSelected && <CheckCircle2 className="w-4 h-4 text-indigo-600" />}
                    </div>
                    <div className="text-xs text-slate-600 font-medium">{u.badge}</div>
                    <div className="text-[11px] font-mono text-slate-400 pt-0.5">OID: {u.oid}</div>
                  </div>
                  <span
                    className={`px-2.5 py-1 text-xs font-semibold rounded-full border ${
                      isSelected
                        ? 'bg-indigo-600 text-white border-indigo-600'
                        : 'bg-slate-100 text-slate-700 border-slate-200'
                    }`}
                  >
                    {u.role}
                  </span>
                </button>
              );
            })}
          </div>

          <button
            onClick={() => {
              setIsLoggedIn(true);
              setActiveScreen('queue');
            }}
            className="w-full py-3 px-5 bg-gradient-to-r from-indigo-600 to-blue-600 hover:from-indigo-500 hover:to-blue-500 text-white text-sm font-semibold rounded-xl shadow-md shadow-indigo-600/20 transition flex items-center justify-center gap-2 cursor-pointer"
          >
            <Lock className="w-4 h-4" />
            Sign In with Entra ID Token
          </button>
        </div>
      </div>

      <div className="text-center text-xs text-slate-400 py-4 border-t border-slate-800/80 bg-slate-950/60">
        Powered by FastAPI • Azure PostgreSQL • Azure Content Understanding • Microsoft-Decision-1 • Foundry
        IQ
      </div>
    </div>
  );
}
