import React from 'react';
import { Bell, ShieldCheck, User } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

const Navbar = ({ title }) => {
  const { user } = useAuth();

  return (
    <header className="h-16 glass-panel border-b border-slate-800 flex items-center justify-between px-8 sticky top-0 z-20">
      <div>
        <h2 className="text-xl font-bold text-white tracking-tight">{title}</h2>
      </div>

      <div className="flex items-center gap-4">
        {/* Security Badge */}
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-semibold">
          <ShieldCheck className="w-4 h-4" />
          <span>JWT + RBAC Protected</span>
        </div>

        {/* Notification Bell */}
        <button className="p-2 text-slate-400 hover:text-slate-200 hover:bg-slate-800/50 rounded-lg transition-all relative">
          <Bell className="w-5 h-5" />
          <span className="w-2 h-2 rounded-full bg-blue-500 absolute top-2 right-2 animate-pulse"></span>
        </button>

        {/* User Avatar */}
        <div className="flex items-center gap-3 border-l border-slate-800 pl-4">
          <div className="w-9 h-9 rounded-full bg-gradient-to-tr from-cyan-500 to-blue-600 flex items-center justify-center font-semibold text-white shadow-md">
            {user?.username?.[0]?.toUpperCase() || 'U'}
          </div>
        </div>
      </div>
    </header>
  );
};

export default Navbar;
