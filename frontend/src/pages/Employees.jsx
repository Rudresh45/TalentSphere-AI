import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { Search, UserPlus, Filter, Mail, Phone, Building, Briefcase } from 'lucide-react';

const Employees = () => {
  const [employees, setEmployees] = useState([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchEmployees();
  }, [search]);

  const fetchEmployees = async () => {
    try {
      const res = await api.get(`/employees/?search=${search}`);
      setEmployees(res.data.results || res.data);
      setLoading(false);
    } catch (err) {
      console.error(err);
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Search & Actions Bar */}
      <div className="flex flex-col md:flex-row gap-4 justify-between items-center glass-panel p-4 rounded-2xl border border-slate-800">
        <div className="relative w-full md:w-96">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search by name, email, employee ID or skills..."
            className="w-full bg-slate-900 border border-slate-700/70 rounded-xl py-2 pl-10 pr-4 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-blue-500"
          />
        </div>

        <div className="flex items-center gap-3">
          <button className="glass-button px-4 py-2 rounded-xl text-xs font-semibold text-white flex items-center gap-2">
            <UserPlus className="w-4 h-4" />
            <span>Onboard Employee</span>
          </button>
        </div>
      </div>

      {/* Employee Cards Grid */}
      {loading ? (
        <div className="text-center py-12 text-slate-400">Loading TalentSphere Directory...</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {employees.map((emp) => (
            <div key={emp.id} className="glass-panel p-6 rounded-2xl border border-slate-800 hover:border-blue-500/40 transition-all group">
              <div className="flex items-center justify-between mb-4">
                <span className="text-xs font-mono px-2.5 py-1 rounded-md bg-slate-800 text-cyan-400 border border-slate-700 font-bold">
                  {emp.employee_id}
                </span>
                <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                  emp.status === 'ACTIVE' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 'bg-amber-500/10 text-amber-400 border border-amber-500/20'
                }`}>
                  {emp.status}
                </span>
              </div>

              <h3 className="text-lg font-bold text-white group-hover:text-blue-400 transition">{emp.full_name}</h3>
              <p className="text-xs text-slate-400 mb-4">{emp.designation_title || 'Software Engineer'}</p>

              <div className="space-y-2 text-xs text-slate-300 mb-4 border-t border-slate-800/80 pt-3">
                <div className="flex items-center gap-2">
                  <Mail className="w-3.5 h-3.5 text-blue-400" />
                  <span className="truncate">{emp.email}</span>
                </div>
                <div className="flex items-center gap-2">
                  <Building className="w-3.5 h-3.5 text-cyan-400" />
                  <span>{emp.department_name || 'Engineering'}</span>
                </div>
              </div>

              <div className="flex flex-wrap gap-1.5 pt-2 border-t border-slate-800/50">
                <span className="text-[10px] px-2 py-0.5 rounded bg-blue-500/10 text-blue-300 font-medium">Python</span>
                <span className="text-[10px] px-2 py-0.5 rounded bg-purple-500/10 text-purple-300 font-medium">Django</span>
                <span className="text-[10px] px-2 py-0.5 rounded bg-cyan-500/10 text-cyan-300 font-medium">React</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Employees;
