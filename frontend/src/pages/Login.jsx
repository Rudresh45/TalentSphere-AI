import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { ShieldCheck, Lock, User, ArrowRight, Sparkles } from 'lucide-react';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e?.preventDefault();
    setError('');
    setSubmitting(true);

    const res = await login(username, password);
    setSubmitting(false);

    if (res.success) {
      navigate('/dashboard');
    } else {
      setError(res.message);
    }
  };

  const fillDemoCredentials = (roleUsername) => {
    setUsername(roleUsername);
    setPassword('Password123!');
  };

  return (
    <div className="min-h-screen w-screen bg-slate-950 flex items-center justify-center p-4 relative overflow-hidden">
      {/* Dynamic Background Glows */}
      <div className="absolute -top-40 -left-40 w-96 h-96 bg-blue-600/20 rounded-full blur-3xl pointer-events-none"></div>
      <div className="absolute -bottom-40 -right-40 w-96 h-96 bg-purple-600/20 rounded-full blur-3xl pointer-events-none"></div>

      <div className="w-full max-w-md z-10">
        {/* Logo Card */}
        <div className="text-center mb-8">
          <div className="w-16 h-16 rounded-2xl bg-gradient-to-tr from-blue-600 via-indigo-600 to-cyan-400 flex items-center justify-center font-extrabold text-2xl text-white shadow-xl shadow-blue-500/30 mx-auto mb-4">
            TS
          </div>
          <h1 className="text-3xl font-extrabold text-white tracking-tight">TalentSphere</h1>
          <p className="text-sm text-cyan-400 font-medium mt-1">Enterprise HR & Activity Intelligence Platform</p>
        </div>

        {/* Login Form Panel */}
        <div className="glass-panel p-8 rounded-3xl border border-slate-800 shadow-2xl">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-bold text-white">Sign In to Platform</h2>
            <div className="flex items-center gap-1.5 text-xs text-emerald-400 font-semibold px-2.5 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20">
              <ShieldCheck className="w-3.5 h-3.5" />
              <span>JWT Auth</span>
            </div>
          </div>

          {error && (
            <div className="mb-6 p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-400 text-xs font-medium">
              {error}
            </div>
          )}

          <form onSubmit={handleLogin} className="space-y-5">
            <div>
              <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">Username</label>
              <div className="relative">
                <User className="w-5 h-5 text-slate-400 absolute left-3.5 top-3" />
                <input
                  type="text"
                  required
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  placeholder="e.g. superadmin, hradmin, manager"
                  className="w-full bg-slate-900/80 border border-slate-700/80 rounded-xl py-2.5 pl-11 pr-4 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">Password</label>
              <div className="relative">
                <Lock className="w-5 h-5 text-slate-400 absolute left-3.5 top-3" />
                <input
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••••••"
                  className="w-full bg-slate-900/80 border border-slate-700/80 rounded-xl py-2.5 pl-11 pr-4 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={submitting}
              className="w-full glass-button py-3 rounded-xl font-bold text-sm text-white flex items-center justify-center gap-2 mt-6 cursor-pointer"
            >
              {submitting ? 'Authenticating...' : 'Access Workspace'}
              <ArrowRight className="w-4 h-4" />
            </button>
          </form>

          {/* Quick Demo Fill Buttons for Interview Demonstration */}
          <div className="mt-8 pt-6 border-t border-slate-800">
            <div className="flex items-center gap-1.5 text-xs text-slate-400 font-semibold mb-3">
              <Sparkles className="w-3.5 h-3.5 text-yellow-400" />
              <span>Interview Demo Role Quick-Fill:</span>
            </div>
            <div className="grid grid-cols-2 gap-2 text-xs">
              <button
                type="button"
                onClick={() => fillDemoCredentials('superadmin')}
                className="py-2 px-3 rounded-lg bg-slate-800/60 hover:bg-slate-700/80 text-blue-300 border border-slate-700 font-medium transition text-left"
              >
                👑 Super Admin
              </button>
              <button
                type="button"
                onClick={() => fillDemoCredentials('hradmin')}
                className="py-2 px-3 rounded-lg bg-slate-800/60 hover:bg-slate-700/80 text-emerald-300 border border-slate-700 font-medium transition text-left"
              >
                💼 HR Admin
              </button>
              <button
                type="button"
                onClick={() => fillDemoCredentials('manager')}
                className="py-2 px-3 rounded-lg bg-slate-800/60 hover:bg-slate-700/80 text-cyan-300 border border-slate-700 font-medium transition text-left"
              >
                📊 Team Manager
              </button>
              <button
                type="button"
                onClick={() => fillDemoCredentials('employee')}
                className="py-2 px-3 rounded-lg bg-slate-800/60 hover:bg-slate-700/80 text-purple-300 border border-slate-700 font-medium transition text-left"
              >
                👤 Employee
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
