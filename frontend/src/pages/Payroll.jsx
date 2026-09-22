import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { DollarSign, ShieldAlert, Download, FileCheck } from 'lucide-react';

const Payroll = () => {
  const [payslips, setPayslips] = useState([]);

  useEffect(() => {
    api.get('/payroll/payslips/my/').then((res) => {
      if (res.data.success) {
        setPayslips(res.data.data || []);
      }
    }).catch(err => console.error(err));
  }, []);

  return (
    <div className="space-y-8">
      {/* Security Banner */}
      <div className="glass-panel p-6 rounded-3xl border border-purple-500/30 bg-purple-950/20 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="p-3 rounded-2xl bg-purple-500/20 text-purple-400 border border-purple-500/30">
            <DollarSign className="w-6 h-6" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-white">Confidential Employee Compensation Hub</h2>
            <p className="text-xs text-slate-300">Protected with strict object-level authorization (Employees see only their own payslips).</p>
          </div>
        </div>
      </div>

      {/* Payslips List */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {payslips.length === 0 ? (
          <div className="glass-panel p-8 rounded-3xl border border-slate-800 col-span-2 text-center text-slate-400">
            No processed payslips found for current employee profile.
          </div>
        ) : (
          payslips.map((slip) => (
            <div key={slip.id} className="glass-panel p-6 rounded-3xl border border-slate-800 space-y-4">
              <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                <div>
                  <h3 className="font-bold text-white text-lg">Pay Period: {slip.pay_period_month}/{slip.pay_period_year}</h3>
                  <p className="text-xs text-slate-400">{slip.employee_name} ({slip.employee_code})</p>
                </div>
                <span className="px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-xs font-bold">
                  {slip.status}
                </span>
              </div>

              <div className="grid grid-cols-2 gap-3 text-xs font-mono">
                <div className="bg-slate-900/60 p-3 rounded-xl">
                  <span className="text-slate-400 block mb-1">Basic Salary:</span>
                  <strong className="text-white text-sm">${slip.basic}</strong>
                </div>
                <div className="bg-slate-900/60 p-3 rounded-xl">
                  <span className="text-slate-400 block mb-1">Allowances:</span>
                  <strong className="text-cyan-400 text-sm">${slip.allowances}</strong>
                </div>
                <div className="bg-slate-900/60 p-3 rounded-xl">
                  <span className="text-slate-400 block mb-1">Deductions (Tax/PF):</span>
                  <strong className="text-rose-400 text-sm">-${slip.deductions}</strong>
                </div>
                <div className="bg-slate-900/60 p-3 rounded-xl border border-emerald-500/30">
                  <span className="text-emerald-400 block mb-1 font-sans font-bold">NET SALARY:</span>
                  <strong className="text-emerald-300 text-base font-extrabold">${slip.net_salary}</strong>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default Payroll;
