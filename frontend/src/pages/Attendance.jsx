import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { Clock, Play, Square, Coffee, CheckCircle, AlertCircle } from 'lucide-react';

const Attendance = () => {
  const [logs, setLogs] = useState([]);
  const [statusMsg, setStatusMsg] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchMyAttendance();
  }, []);

  const fetchMyAttendance = async () => {
    try {
      const res = await api.get('/attendance/my/');
      setLogs(res.data.data || []);
    } catch (err) {
      console.error(err);
    }
  };

  const handleClockIn = async () => {
    setLoading(true);
    try {
      const res = await api.post('/attendance/clock_in/');
      setStatusMsg('Successfully Clocked In!');
      fetchMyAttendance();
    } catch (err) {
      setStatusMsg(err.response?.data?.message || 'Clock in failed');
    }
    setLoading(false);
  };

  const handleClockOut = async () => {
    setLoading(true);
    try {
      const res = await api.post('/attendance/clock_out/');
      setStatusMsg('Successfully Clocked Out!');
      fetchMyAttendance();
    } catch (err) {
      setStatusMsg(err.response?.data?.message || 'Clock out failed');
    }
    setLoading(false);
  };

  return (
    <div className="space-y-8">
      {/* Interactive Clock Punch Widget */}
      <div className="glass-panel p-8 rounded-3xl border border-blue-500/20 bg-gradient-to-r from-slate-900 via-blue-950/40 to-slate-900 flex flex-col md:flex-row items-center justify-between gap-6">
        <div>
          <span className="text-xs font-mono font-bold text-cyan-400 uppercase tracking-widest">Time & Attendance System</span>
          <h2 className="text-3xl font-extrabold text-white mt-1">Daily Punch Control</h2>
          <p className="text-xs text-slate-400 mt-1">Log your work shift hours, clock-in, clock-out, and break intervals.</p>
          {statusMsg && (
            <p className="mt-3 text-xs font-semibold text-emerald-400 bg-emerald-500/10 px-3 py-1.5 rounded-lg border border-emerald-500/20 inline-block">
              {statusMsg}
            </p>
          )}
        </div>

        <div className="flex items-center gap-4">
          <button
            onClick={handleClockIn}
            disabled={loading}
            className="px-6 py-3.5 rounded-2xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-sm flex items-center gap-2 shadow-lg shadow-emerald-600/30 transition cursor-pointer"
          >
            <Play className="w-4 h-4 fill-white" />
            <span>Clock In</span>
          </button>

          <button
            onClick={handleClockOut}
            disabled={loading}
            className="px-6 py-3.5 rounded-2xl bg-rose-600 hover:bg-rose-500 text-white font-bold text-sm flex items-center gap-2 shadow-lg shadow-rose-600/30 transition cursor-pointer"
          >
            <Square className="w-4 h-4 fill-white" />
            <span>Clock Out</span>
          </button>
        </div>
      </div>

      {/* Attendance History Table */}
      <div className="glass-panel p-6 rounded-3xl border border-slate-800">
        <h3 className="text-lg font-bold text-white mb-4">My Attendance Log</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-slate-300">
            <thead className="bg-slate-900/80 text-xs font-semibold uppercase text-slate-400 border-b border-slate-800">
              <tr>
                <th className="p-3.5">Date</th>
                <th className="p-3.5">Clock In</th>
                <th className="p-3.5">Clock Out</th>
                <th className="p-3.5">Total Hours</th>
                <th className="p-3.5">Overtime</th>
                <th className="p-3.5">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 font-mono text-xs">
              {logs.map((log) => (
                <tr key={log.id} className="hover:bg-slate-900/40">
                  <td className="p-3.5 font-sans font-medium text-white">{log.date}</td>
                  <td className="p-3.5 text-cyan-400">{log.clock_in ? new Date(log.clock_in).toLocaleTimeString() : '--'}</td>
                  <td className="p-3.5 text-cyan-400">{log.clock_out ? new Date(log.clock_out).toLocaleTimeString() : '--'}</td>
                  <td className="p-3.5 font-bold text-white">{log.total_hours} hrs</td>
                  <td className="p-3.5 text-amber-400">{log.overtime_hours} hrs</td>
                  <td className="p-3.5">
                    <span className="px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-sans text-[10px] font-bold">
                      {log.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Attendance;
