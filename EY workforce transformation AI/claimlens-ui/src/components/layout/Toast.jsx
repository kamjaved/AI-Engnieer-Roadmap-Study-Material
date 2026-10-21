import { Terminal, X } from 'lucide-react';
import { useClaimLens } from '../../context/useClaimLens';

export default function Toast() {
  const { toastMessage, setToastMessage } = useClaimLens();

  if (!toastMessage) return null;

  return (
    <div className="bg-slate-900 text-white text-xs px-5 py-3 border-b border-indigo-500/40 shadow-md flex items-center justify-between">
      <div className="max-w-7xl mx-auto w-full flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <span className="p-1 rounded-md bg-indigo-500/20 text-indigo-300">
            <Terminal className="w-4 h-4 shrink-0" />
          </span>
          <span className="font-medium">{toastMessage}</span>
        </div>
        <button onClick={() => setToastMessage(null)} className="text-slate-400 hover:text-white">
          <X className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
}
