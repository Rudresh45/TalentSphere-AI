import React, { useState } from 'react';
import { UserPlus, Briefcase, CheckCircle2, Clock, Calendar } from 'lucide-react';

const pipelineStages = [
  { id: 'APPLIED', title: 'Applied', color: 'border-blue-500/30 bg-blue-500/5 text-blue-400' },
  { id: 'SCREENING', title: 'Screening', color: 'border-purple-500/30 bg-purple-500/5 text-purple-400' },
  { id: 'INTERVIEW', title: 'Interview', color: 'border-cyan-500/30 bg-cyan-500/5 text-cyan-400' },
  { id: 'SELECTED', title: 'Selected / Hired', color: 'border-emerald-500/30 bg-emerald-500/5 text-emerald-400' },
];

const mockCandidates = [
  { id: 1, name: 'Sophia Miller', role: 'Senior Python Engineer', stage: 'INTERVIEW', score: '9/10' },
  { id: 2, name: 'Liam Johnson', role: 'Full Stack Architect', stage: 'SCREENING', score: '8/10' },
  { id: 3, name: 'Emma Davis', role: 'DevOps & AWS Specialist', stage: 'APPLIED', score: 'Pending' },
  { id: 4, name: 'Noah Wilson', role: 'React UI Lead', stage: 'SELECTED', score: '9.5/10' },
];

const Recruitment = () => {
  return (
    <div className="space-y-8">
      {/* Top Banner */}
      <div className="glass-panel p-6 rounded-3xl border border-slate-800 flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-white">Talent Acquisition & Hiring Pipeline</h2>
          <p className="text-xs text-slate-400 mt-1">Manage open requisitions, candidate screening, interview scheduling, and hiring workflow.</p>
        </div>
        <button className="glass-button px-4 py-2 rounded-xl text-xs font-semibold text-white flex items-center gap-2">
          <UserPlus className="w-4 h-4" />
          <span>Post New Job Requisition</span>
        </button>
      </div>

      {/* Hiring Kanban Board */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        {pipelineStages.map((stage) => (
          <div key={stage.id} className="glass-panel p-4 rounded-2xl border border-slate-800 flex flex-col min-h-[420px]">
            <div className={`p-3 rounded-xl border font-bold text-xs flex items-center justify-between mb-4 ${stage.color}`}>
              <span>{stage.title}</span>
              <span className="w-5 h-5 rounded-full bg-slate-900 flex items-center justify-center text-[10px]">
                {mockCandidates.filter(c => c.stage === stage.id).length}
              </span>
            </div>

            <div className="space-y-3 flex-1">
              {mockCandidates
                .filter((candidate) => candidate.stage === stage.id)
                .map((candidate) => (
                  <div key={candidate.id} className="p-4 rounded-xl bg-slate-900/80 border border-slate-800 hover:border-blue-500/40 transition-all cursor-pointer">
                    <h4 className="font-bold text-sm text-white mb-1">{candidate.name}</h4>
                    <p className="text-xs text-slate-400 mb-3">{candidate.role}</p>
                    <div className="flex items-center justify-between text-[10px] text-slate-400 pt-2 border-t border-slate-800">
                      <span>Score: <strong className="text-cyan-400">{candidate.score}</strong></span>
                      <Calendar className="w-3.5 h-3.5 text-slate-500" />
                    </div>
                  </div>
                ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Recruitment;
