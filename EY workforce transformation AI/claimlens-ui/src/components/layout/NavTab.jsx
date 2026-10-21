export default function NavTab({ active, onClick, children }) {
  return (
    <button
      onClick={onClick}
      className={`px-3 py-1.5 text-xs font-semibold rounded-lg transition flex items-center gap-1.5 cursor-pointer ${
        active
          ? 'bg-white text-indigo-700 shadow-2xs border border-slate-200/80'
          : 'text-slate-600 hover:text-slate-900 hover:bg-white/50'
      }`}
    >
      {children}
    </button>
  );
}
