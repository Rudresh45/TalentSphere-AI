import React, { useState } from 'react';
import { Plus, CheckSquare, Clock, AlertOctagon, CheckCircle2 } from 'lucide-react';

const kanbanColumns = [
  { id: 'TODO', title: 'To Do', color: 'border-slate-700 bg-slate-900/50 text-slate-300' },
  { id: 'IN_PROGRESS', title: 'In Progress', color: 'border-blue-500/40 bg-blue-500/10 text-blue-400' },
  { id: 'REVIEW', title: 'Code Review', color: 'border-purple-500/40 bg-purple-500/10 text-purple-400' },
  { id: 'COMPLETED', title: 'Completed', color: 'border-emerald-500/40 bg-emerald-500/10 text-emerald-400' },
];

const mockTasks = [
  { id: 1, title: 'Implement JWT Auth & Token Blacklisting', project: 'ENG-01', priority: 'URGENT', assignee: 'Alex', status: 'COMPLETED' },
  { id: 2, title: 'Build spaCy NLP Skill Gap Analysis Engine', project: 'AI-02', priority: 'HIGH', assignee: 'Sophia', status: 'IN_PROGRESS' },
  { id: 3, title: 'Configure DRF Scoped Rate Throttling', project: 'SEC-03', priority: 'HIGH', assignee: 'Marcus', status: 'REVIEW' },
  { id: 4, title: 'Design Enterprise Glassmorphic React UI', project: 'UI-04', priority: 'MEDIUM', assignee: 'Elena', status: 'TODO' },
];

const ProjectsTasks = () => {
  return (
    <div className="space-y-8">
      {/* Engineering Header */}
      <div className="glass-panel p-6 rounded-3xl border border-slate-800 flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-white">Sprint & Kanban Task Management</h2>
          <p className="text-xs text-slate-400 mt-1">Track sprint velocity, backlog tasks, code reviews, and project milestones.</p>
        </div>
        <button className="glass-button px-4 py-2 rounded-xl text-xs font-semibold text-white flex items-center gap-2">
          <Plus className="w-4 h-4" />
          <span>Create Task</span>
        </button>
      </div>

      {/* Kanban Board */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        {kanbanColumns.map((col) => (
          <div key={col.id} className="glass-panel p-4 rounded-2xl border border-slate-800 flex flex-col min-h-[460px]">
            <div className={`p-3 rounded-xl border font-bold text-xs flex items-center justify-between mb-4 ${col.color}`}>
              <span>{col.title}</span>
              <span className="w-5 h-5 rounded-full bg-slate-950 flex items-center justify-center text-[10px]">
                {mockTasks.filter(t => t.status === col.id).length}
              </span>
            </div>

            <div className="space-y-3 flex-1">
              {mockTasks
                .filter(t => t.status === col.id)
                .map((task) => (
                  <div key={task.id} className="p-4 rounded-xl bg-slate-900/90 border border-slate-800 hover:border-blue-500/40 transition-all cursor-pointer">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-cyan-400 font-bold">
                        {task.project}
                      </span>
                      <span className={`text-[9px] font-bold px-1.5 py-0.5 rounded ${
                        task.priority === 'URGENT' ? 'bg-rose-500/20 text-rose-400' : 'bg-blue-500/20 text-blue-400'
                      }`}>
                        {task.priority}
                      </span>
                    </div>

                    <h4 className="font-semibold text-xs text-white mb-3">{task.title}</h4>

                    <div className="flex items-center justify-between text-[10px] text-slate-400 pt-2 border-t border-slate-800/80">
                      <span>Assignee: <strong className="text-slate-200">{task.assignee}</strong></span>
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

export default ProjectsTasks;
