import React, { useState } from 'react';
import api from '../services/api';
import { BrainCircuit, Sparkles, CheckCircle2, AlertTriangle, BookOpen, ArrowRight } from 'lucide-react';

const AIIntelligence = () => {
  const [targetRole, setTargetRole] = useState('Full Stack Cloud Architect');
  const [requiredSkillsInput, setRequiredSkillsInput] = useState('Python, Django, FastAPI, PostgreSQL, Docker, AWS, Kubernetes');
  const [analysis, setAnalysis] = useState(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [error, setError] = useState('');

  const runAnalysis = async () => {
    setAnalyzing(true);
    setError('');
    const skillsList = requiredSkillsInput.split(',').map(s => s.strip ? s.strip() : s.trim()).filter(Boolean);

    try {
      const res = await api.post('/ai/skill-gap/analyze/', {
        target_role: targetRole,
        required_skills: skillsList
      });
      if (res.data.success) {
        setAnalysis(res.data.data);
      }
    } catch (err) {
      setError(err.response?.data?.message || 'AI Skill Gap analysis failed.');
    }
    setAnalyzing(false);
  };

  return (
    <div className="space-y-8">
      {/* Top AI Header */}
      <div className="glass-panel p-8 rounded-3xl border border-purple-500/30 bg-gradient-to-r from-purple-950/40 via-slate-900 to-indigo-950/40 flex items-center justify-between">
        <div>
          <div className="flex items-center gap-2 text-xs font-mono font-bold text-purple-400 uppercase tracking-widest mb-1">
            <BrainCircuit className="w-4 h-4 text-cyan-400" />
            <span>spaCy NLP & Scikit-Learn Match Engine</span>
          </div>
          <h2 className="text-3xl font-extrabold text-white">AI Skill Gap & Learning Portal</h2>
          <p className="text-xs text-slate-300 mt-1">Analyze candidate/employee skills against target job profiles to calculate match score and generate personalized course recommendations.</p>
        </div>
      </div>

      {/* Input Analyzer Form */}
      <div className="glass-panel p-6 rounded-3xl border border-slate-800 space-y-4">
        <h3 className="text-base font-bold text-white flex items-center gap-2">
          <Sparkles className="w-4 h-4 text-yellow-400" />
          <span>Configure Target Role Skill Matrix</span>
        </h3>

        {error && (
          <div className="p-3 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-400 text-xs font-semibold">
            {error}
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-xs font-semibold text-slate-400 mb-1">Target Position / Role</label>
            <input
              type="text"
              value={targetRole}
              onChange={(e) => setTargetRole(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700/80 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:border-purple-500"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-400 mb-1">Required Skills (Comma Separated)</label>
            <input
              type="text"
              value={requiredSkillsInput}
              onChange={(e) => setRequiredSkillsInput(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700/80 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:border-purple-500"
            />
          </div>
        </div>

        <button
          onClick={runAnalysis}
          disabled={analyzing}
          className="glass-button px-6 py-3 rounded-xl font-bold text-sm text-white flex items-center gap-2 cursor-pointer"
        >
          {analyzing ? 'Computing TF-IDF Vectors...' : 'Execute AI Skill Gap Analysis'}
          <ArrowRight className="w-4 h-4" />
        </button>
      </div>

      {/* Analysis Results */}
      {analysis && (
        <div className="space-y-6">
          <div className="glass-panel p-6 rounded-3xl border border-blue-500/30 bg-blue-950/10 flex items-center justify-between">
            <div>
              <span className="text-xs font-semibold text-slate-400">Skill Match Score</span>
              <h3 className="text-4xl font-extrabold text-cyan-400 mt-1">{analysis.match_percentage}%</h3>
              <p className="text-xs text-slate-300 mt-1">Target Role: <strong className="text-white">{analysis.target_role}</strong></p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="glass-panel p-6 rounded-3xl border border-emerald-500/20 bg-emerald-950/10">
              <h4 className="text-sm font-bold text-emerald-400 mb-3 flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4" />
                <span>Matched Skills ({analysis.matched_skills.length})</span>
              </h4>
              <div className="flex flex-wrap gap-2">
                {analysis.matched_skills.map((skill, idx) => (
                  <span key={idx} className="px-3 py-1.5 rounded-lg bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 text-xs font-semibold">
                    {skill}
                  </span>
                ))}
              </div>
            </div>

            <div className="glass-panel p-6 rounded-3xl border border-rose-500/20 bg-rose-950/10">
              <h4 className="text-sm font-bold text-rose-400 mb-3 flex items-center gap-2">
                <AlertTriangle className="w-4 h-4" />
                <span>Identified Skill Gaps ({analysis.missing_skills.length})</span>
              </h4>
              <div className="flex flex-wrap gap-2">
                {analysis.missing_skills.map((skill, idx) => (
                  <span key={idx} className="px-3 py-1.5 rounded-lg bg-rose-500/20 text-rose-300 border border-rose-500/30 text-xs font-semibold">
                    {skill}
                  </span>
                ))}
              </div>
            </div>
          </div>

          {/* Recommended Learning Courses */}
          <div className="glass-panel p-6 rounded-3xl border border-slate-800">
            <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
              <BookOpen className="w-5 h-5 text-blue-400" />
              <span>Personalized AI Learning Recommendations</span>
            </h3>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {analysis.recommendations.map((rec) => (
                <div key={rec.id} className="p-4 rounded-2xl bg-slate-900/80 border border-slate-800 hover:border-purple-500/40 transition">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-purple-500/20 text-purple-300 border border-purple-500/30">
                      GAP: {rec.skill_gap}
                    </span>
                    <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-rose-500/20 text-rose-400 border border-rose-500/30 uppercase">
                      {rec.priority}
                    </span>
                  </div>
                  <h4 className="font-bold text-sm text-white mb-1">{rec.course_title}</h4>
                  <p className="text-xs text-slate-400 mb-3">{rec.description}</p>
                  <a
                    href={rec.recommended_url}
                    target="_blank"
                    rel="noreferrer"
                    className="inline-flex items-center gap-1.5 text-xs font-semibold text-blue-400 hover:text-blue-300"
                  >
                    <span>Start Learning Course</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </a>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AIIntelligence;
