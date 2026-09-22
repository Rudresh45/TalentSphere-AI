import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { 
  Users, CheckCircle2, Clock, AlertTriangle, TrendingUp, BrainCircuit, ShieldCheck 
} from 'lucide-react';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area 
} from 'recharts';

const chartData = [
  { name: 'Sprint 1', velocity: 32, completed: 28 },
  { name: 'Sprint 2', velocity: 40, completed: 38 },
  { name: 'Sprint 3', velocity: 35, completed: 34 },
  { name: 'Sprint 4', velocity: 48, completed: 45 },
  { name: 'Sprint 5', velocity: 52, completed: 50 },
];

const attendanceData = [
  { day: 'Mon', present: 98, late: 2 },
  { day: 'Tue', present: 96, late: 4 },
  { day: 'Wed', present: 100, late: 0 },
  { day: 'Thu', present: 95, late: 5 },
  { day: 'Fri', present: 94, late: 6 },
];

const Dashboard = () => {
  const [metrics, setMetrics] = useState(null);

  useEffect(() => {
    api.get('/performance/dashboard/').then((res) => {
      if (res.data.success) {
        setMetrics(res.data.data);
      }
    }).catch(err => console.error(err));
  }, []);

  return (
    <div className="space-y-8">
      {/* Top Banner */}
      <div className="glass-panel p-6 rounded-3xl border border-blue-500/20 bg-gradient-to-r from-blue-900/30 via-slate-900 to-indigo-900/30 flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-extrabold text-white">Executive Intelligence Overview</h2>
          <p className="text-sm text-slate-300 mt-1">Real-time enterprise HR metrics, task velocity, and AI talent insight.</p>
        </div>
        <div className="flex items-center gap-2 px-4 py-2 rounded-xl bg-blue-500/20 text-blue-300 border border-blue-500/30 text-xs font-semibold">
          <TrendingUp className="w-4 h-4 text-cyan-400" />
          <span>Platform Health: 99.8%</span>
        </div>
      </div>

      {/* Stats Cards Row */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="glass-panel p-6 rounded-2xl border border-slate-800 flex items-center gap-4">
          <div className="p-3.5 rounded-xl bg-blue-500/10 text-blue-400 border border-blue-500/20">
            <CheckCircle2 className="w-6 h-6" />
          </div>
          <div>
            <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Completed Tasks</p>
            <h3 className="text-2xl font-bold text-white mt-1">{metrics?.completed_tasks ?? 45}</h3>
          </div>
        </div>

        <div className="glass-panel p-6 rounded-2xl border border-slate-800 flex items-center gap-4">
          <div className="p-3.5 rounded-xl bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
            <TrendingUp className="w-6 h-6" />
          </div>
          <div>
            <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Completion Rate</p>
            <h3 className="text-2xl font-bold text-white mt-1">{metrics?.task_completion_rate ?? 92.5}%</h3>
          </div>
        </div>

        <div className="glass-panel p-6 rounded-2xl border border-slate-800 flex items-center gap-4">
          <div className="p-3.5 rounded-xl bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
            <Clock className="w-6 h-6" />
          </div>
          <div>
            <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Attendance %</p>
            <h3 className="text-2xl font-bold text-white mt-1">{metrics?.attendance_percentage ?? 96.4}%</h3>
          </div>
        </div>

        <div className="glass-panel p-6 rounded-2xl border border-slate-800 flex items-center gap-4">
          <div className="p-3.5 rounded-xl bg-purple-500/10 text-purple-400 border border-purple-500/20">
            <BrainCircuit className="w-6 h-6" />
          </div>
          <div>
            <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Avg Perf Score</p>
            <h3 className="text-2xl font-bold text-white mt-1">{metrics?.average_performance_score ?? 4.8} / 5</h3>
          </div>
        </div>
      </div>

      {/* Analytics Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="glass-panel p-6 rounded-3xl border border-slate-800">
          <h3 className="text-lg font-bold text-white mb-4">Sprint Engineering Velocity</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="name" stroke="#64748b" />
                <YAxis stroke="#64748b" />
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', color: '#f8fafc' }} />
                <Bar dataKey="velocity" fill="#3b82f6" radius={[6, 6, 0, 0]} />
                <Bar dataKey="completed" fill="#10b981" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="glass-panel p-6 rounded-3xl border border-slate-800">
          <h3 className="text-lg font-bold text-white mb-4">Weekly Attendance Trend (%)</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={attendanceData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="day" stroke="#64748b" />
                <YAxis stroke="#64748b" />
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', color: '#f8fafc' }} />
                <Area type="monotone" dataKey="present" stroke="#06b6d4" fill="rgba(6, 182, 212, 0.2)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
