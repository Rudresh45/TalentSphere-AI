import React from 'react';
import { NavLink } from 'react-router-dom';
import { 
  LayoutDashboard, Users, UserPlus, Clock, 
  DollarSign, Briefcase, BrainCircuit, FileText, ShieldAlert, LogOut 
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';

const Sidebar = () => {
  const { user, logout } = useAuth();

  const navItems = [
    { label: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
    { label: 'Employees', path: '/employees', icon: Users },
    { label: 'Recruitment', path: '/recruitment', icon: UserPlus },
    { label: 'Attendance', path: '/attendance', icon: Clock },
    { label: 'Payroll', path: '/payroll', icon: DollarSign },
    { label: 'Engineering', path: '/projects', icon: Briefcase },
    { label: 'AI Intelligence', path: '/ai-intelligence', icon: BrainCircuit },
    { label: 'Quotations', path: '/quotations', icon: FileText },
    { label: 'Audit Logs', path: '/audit-logs', icon: ShieldAlert, roles: ['SUPER_ADMIN', 'HR_ADMIN'] },
  ];

  return (
    <aside className="w-64 glass-panel h-screen flex flex-col fixed left-0 top-0 z-30 border-r border-slate-800">
      {/* Brand Header */}
      <div className="p-6 border-b border-slate-800 flex items-center gap-3">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-600 via-indigo-600 to-cyan-400 flex items-center justify-center font-bold text-white shadow-lg shadow-blue-500/25">
          TS
        </div>
        <div>
          <h1 className="font-bold text-lg text-white tracking-wide">TalentSphere</h1>
          <p className="text-xs text-cyan-400 font-medium">Enterprise HR & AI Intelligence</p>
        </div>
      </div>

      {/* Navigation Links */}
      <nav className="flex-1 p-4 space-y-1.5 overflow-y-auto">
        {navItems.map((item) => {
          if (item.roles && !item.roles.includes(user?.role)) {
            return null;
          }
          const Icon = item.icon;
          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center gap-3.5 px-4 py-3 rounded-xl font-medium text-sm transition-all duration-200 ${
                  isActive
                    ? 'bg-blue-600/20 text-blue-400 border border-blue-500/30 shadow-md shadow-blue-500/10'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/40'
                }`
              }
            >
              <Icon className="w-5 h-5" />
              <span>{item.label}</span>
            </NavLink>
          );
        })}
      </nav>

      {/* Logged in User Badge & Logout */}
      <div className="p-4 border-t border-slate-800 bg-slate-900/40">
        <div className="flex items-center justify-between mb-3 px-2">
          <div>
            <p className="text-sm font-semibold text-slate-200">{user?.username}</p>
            <span className="inline-block px-2 py-0.5 text-[10px] font-bold rounded-full bg-blue-500/20 text-blue-400 border border-blue-500/30">
              {user?.role_display || user?.role}
            </span>
          </div>
        </div>
        <button
          onClick={logout}
          className="w-full flex items-center justify-center gap-2 px-3 py-2 text-xs font-semibold text-rose-400 bg-rose-500/10 hover:bg-rose-500/20 border border-rose-500/20 rounded-lg transition-all"
        >
          <LogOut className="w-4 h-4" />
          <span>Sign Out</span>
        </button>
      </div>
    </aside>
  );
};

export default Sidebar;
