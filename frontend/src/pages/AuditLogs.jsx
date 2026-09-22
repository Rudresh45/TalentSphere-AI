import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { ShieldAlert, Terminal, Lock, CheckCircle2 } from 'lucide-react';

const AuditLogs = () => {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get('/audit-logs/').then((res) => {
      setLogs(res.data.results || res.data || []);
      setLoading(false);
    }).catch(err => {
      console.error(err);
      setLoading(false);
    });
  }, []);

  return (
    <div className="space-y-8">
      {/* Header Banner */}
      <div className="glass-panel p-6 rounded-3xl border border-rose-500/20 bg-rose-950/10 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="p-3 rounded-2xl bg-rose-500/20 text-rose-400 border border-rose-500/30">
            <ShieldAlert className="w-6 h-6" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-white">Immutable Enterprise Security Audit Trail</h2>
            <p className="text-xs text-slate-300">Monitors sensitive mutations, role updates, authentication events, and API calls.</p>
          </div>
        </div>
      </div>

      {/* Audit Log Table */}
      <div className="glass-panel p-6 rounded-3xl border border-slate-800">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-mono text-slate-300">
            <thead className="bg-slate-900/80 uppercase text-slate-400 border-b border-slate-800 font-sans">
              <tr>
                <th className="p-3.5">Timestamp</th>
                <th className="p-3.5">User</th>
                <th className="p-3.5">Action</th>
                <th className="p-3.5">Resource</th>
                <th className="p-3.5">IP Address</th>
                <th className="p-3.5">Method</th>
                <th className="p-3.5">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {loading ? (
                <tr><td colSpan="7" className="p-6 text-center text-slate-500">Loading audit trail...</td></tr>
              ) : logs.length === 0 ? (
                <tr><td colSpan="7" className="p-6 text-center text-slate-500">No security audit logs captured yet.</td></tr>
              ) : (
                logs.map((log) => (
                  <tr key={log.id} className="hover:bg-slate-900/40">
                    <td className="p-3.5 text-slate-400">{new Date(log.timestamp).toLocaleString()}</td>
                    <td className="p-3.5 font-bold text-white">{log.username || 'Anonymous'}</td>
                    <td className="p-3.5">
                      <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                        log.action === 'LOGIN' ? 'bg-emerald-500/20 text-emerald-400' :
                        log.action === 'FAILED_LOGIN' ? 'bg-rose-500/20 text-rose-400' :
                        'bg-blue-500/20 text-blue-400'
                      }`}>
                        {log.action}
                      </span>
                    </td>
                    <td className="p-3.5 text-cyan-400">{log.resource}</td>
                    <td className="p-3.5 text-slate-400">{log.ip_address || '127.0.0.1'}</td>
                    <td className="p-3.5 font-bold">{log.request_method}</td>
                    <td className="p-3.5">
                      <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                        log.status_code === 200 || log.status_code === 201 ? 'text-emerald-400' : 'text-rose-400'
                      }`}>
                        {log.status_code}
                      </span>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default AuditLogs;
