import React, { useState, useEffect } from 'react';
import { useAppStore } from '../store/appStore';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, LineChart, Line, CartesianGrid, Cell } from 'recharts';
import { Target, TrendingUp, Award, BookOpen, Clock, AlertTriangle, CheckCircle, Flame, ArrowRight } from 'lucide-react';
import { getApiBaseUrl } from '../config';

export default function Performance() {
  const { activeSubjectName, subject: storeSubject } = useAppStore();
  const searchParams = new URLSearchParams(window.location.search);
  const subjectId = searchParams.get('subject') || storeSubject;

  const [loading, setLoading] = useState(true);
  const [data, setData] = useState(null);

  useEffect(() => {
    if (!subjectId) {
      setLoading(false);
      return;
    }
    
    let isSubscribed = true;
    setLoading(true);

    fetch(`${getApiBaseUrl()}/api/subjects/${subjectId}/performance`)
      .then(res => res.json())
      .then(resData => {
        if (!isSubscribed) return;

        // Merge with local storage practice attempts if available
        const localAttemptsKey = `edumind_attempts_${subjectId}`;
        const localAttempts = JSON.parse(localStorage.getItem(localAttemptsKey) || '[]');
        
        let mergedData = { ...resData };

        if (localAttempts.length > 0 && (!resData.accuracy_trend || resData.accuracy_trend.length === 0)) {
          let totalScore = 0;
          let totalMarks = 0;
          let totalTimeSec = 0;
          const trend = localAttempts.map((att, idx) => {
            totalScore += att.score || 0;
            totalMarks += att.total || 0;
            totalTimeSec += att.time_taken_seconds || 0;
            return {
              attempt_num: idx + 1,
              score: att.score || 0,
              total: att.total || 0,
              accuracy: att.accuracy || (att.total > 0 ? (att.score / att.total * 100) : 0),
              type: att.type || 'practice'
            };
          });

          const overallAcc = totalMarks > 0 ? Math.round((totalScore / totalMarks * 100) * 10) / 10 : 0;
          const grade = overallAcc >= 85 ? 'A+' : overallAcc >= 75 ? 'A' : overallAcc >= 60 ? 'B' : overallAcc >= 45 ? 'C' : 'D';

          mergedData = {
            total_quizzes: localAttempts.length,
            overall_accuracy: overallAcc,
            grade: grade,
            total_time_minutes: Math.round((totalTimeSec / 60) * 10) / 10,
            total_questions_answered: totalMarks,
            unit_mastery: resData.unit_mastery || [
              { unit_id: 'Unit 1', accuracy: overallAcc, total_questions: totalMarks, status: overallAcc >= 75 ? 'Mastered' : 'Needs Review' }
            ],
            accuracy_trend: trend,
            weak_topics: resData.weak_topics || (overallAcc < 65 ? ['Unit 1 (Timed Practice)'] : []),
            strong_topics: resData.strong_topics || (overallAcc >= 65 ? ['Unit 1 (Timed Practice)'] : []),
            recent_activity: localAttempts.slice(-5).reverse().map((att, i) => ({
              attempt_num: localAttempts.length - i,
              score: att.score || 0,
              total: att.total || 0,
              accuracy: att.accuracy || 0,
              time_formatted: `${Math.floor((att.time_taken_seconds || 0) / 60)}m ${(att.time_taken_seconds || 0) % 60}s`,
              type: att.type === 'timed_exam' ? 'Timed Exam' : 'Practice Quiz'
            }))
          };
        }

        setData(mergedData);
        setLoading(false);
      })
      .catch(err => {
        console.error("Failed to fetch performance data", err);
        setLoading(false);
      });

    return () => { isSubscribed = false; };
  }, [subjectId]);

  if (loading) {
    return <div className="p-12 text-center text-gray-500 font-medium animate-pulse">Analyzing student performance telemetry...</div>;
  }

  if (!data || (data.total_quizzes === 0 && (!data.accuracy_trend || data.accuracy_trend.length === 0))) {
    return (
      <div className="bg-white rounded-2xl p-8 sm:p-12 border border-border-subtle shadow-sm flex flex-col min-h-[420px] items-center justify-center text-center">
        <div className="w-20 h-20 bg-blue-50 text-blue-600 rounded-2xl flex items-center justify-center mb-5 shadow-inner">
          <TrendingUp className="w-10 h-10" />
        </div>
        <h3 className="text-2xl font-bold text-gray-900 mb-2">No Performance Records Yet</h3>
        <p className="text-sm text-gray-500 max-w-md leading-relaxed mb-6">
          Complete practice quizzes or timed exam simulations for <span className="font-semibold text-blue-600">{activeSubjectName || subjectId}</span> to generate live performance analytics and topic mastery breakdown!
        </p>
        <a
          href={`/practice?subject=${subjectId}`}
          className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-bold text-sm rounded-xl shadow-md transition-all flex items-center gap-2"
        >
          <span>Start Practice Session</span>
          <ArrowRight className="w-4 h-4" />
        </a>
      </div>
    );
  }

  const {
    total_quizzes = 0,
    overall_accuracy = 0,
    grade = 'N/A',
    total_time_minutes = 0,
    total_questions_answered = 0,
    unit_mastery = [],
    accuracy_trend = [],
    weak_topics = [],
    strong_topics = [],
    recent_activity = []
  } = data;

  const CustomTooltip = ({ active, payload, label, suffix = '%' }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-slate-900 text-white p-3 border border-slate-700 shadow-xl rounded-xl text-xs space-y-1">
          <p className="font-bold text-indigo-300">{label}</p>
          <p className="text-emerald-400 font-mono font-semibold">
            {payload[0].name}: {payload[0].value.toFixed(1)}{suffix}
          </p>
          {payload[0].payload.total_questions && (
            <p className="text-[11px] text-slate-400 pt-1 border-t border-slate-800">
              Based on {payload[0].payload.total_questions} questions
            </p>
          )}
        </div>
      );
    }
    return null;
  };

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 text-white rounded-2xl p-6 sm:p-8 border border-indigo-500/30 shadow-xl flex flex-col sm:flex-row sm:items-center sm:justify-between gap-6">
        <div>
          <span className="text-xs font-bold text-indigo-400 uppercase tracking-wider">Student Telemetry Analytics</span>
          <h3 className="text-2xl sm:text-3xl font-extrabold text-white mt-1">Performance Intelligence Dashboard</h3>
          <p className="text-xs sm:text-sm text-slate-300 mt-1">
            Real-time mastery tracking &amp; predictive weak spot analysis for <span className="font-semibold text-indigo-300">{activeSubjectName || subjectId}</span>.
          </p>
        </div>

        {/* Grade Badge */}
        <div className="bg-slate-800/90 border border-slate-700 rounded-2xl p-4 flex items-center gap-4 shadow-inner flex-shrink-0 self-start sm:self-auto">
          <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-2xl font-black text-white font-mono shadow-md">
            {grade}
          </div>
          <div>
            <span className="text-[11px] text-slate-400 uppercase font-semibold">Subject Rank</span>
            <p className="text-sm font-bold text-slate-100">
              {overall_accuracy >= 75 ? 'Mastery Tier' : overall_accuracy >= 50 ? 'Proficient Tier' : 'Developing Tier'}
            </p>
          </div>
        </div>
      </div>

      {/* 4 Metric Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Overall Accuracy */}
        <div className="bg-white rounded-2xl p-5 border border-border-subtle shadow-sm flex items-center gap-4">
          <div className="w-12 h-12 bg-emerald-50 text-emerald-600 rounded-xl flex items-center justify-center flex-shrink-0">
            <Target className="w-6 h-6" />
          </div>
          <div>
            <p className="text-xs font-semibold text-text-secondary uppercase tracking-wider">Overall Accuracy</p>
            <p className="text-2xl font-extrabold text-gray-900 font-mono">{overall_accuracy}%</p>
          </div>
        </div>

        {/* Quizzes & Exams */}
        <div className="bg-white rounded-2xl p-5 border border-border-subtle shadow-sm flex items-center gap-4">
          <div className="w-12 h-12 bg-blue-50 text-blue-600 rounded-xl flex items-center justify-center flex-shrink-0">
            <BookOpen className="w-6 h-6" />
          </div>
          <div>
            <p className="text-xs font-semibold text-text-secondary uppercase tracking-wider">Completed Sessions</p>
            <p className="text-2xl font-extrabold text-gray-900 font-mono">{total_quizzes}</p>
          </div>
        </div>

        {/* Total Practice Time */}
        <div className="bg-white rounded-2xl p-5 border border-border-subtle shadow-sm flex items-center gap-4">
          <div className="w-12 h-12 bg-purple-50 text-purple-600 rounded-xl flex items-center justify-center flex-shrink-0">
            <Clock className="w-6 h-6" />
          </div>
          <div>
            <p className="text-xs font-semibold text-text-secondary uppercase tracking-wider">Practice Time</p>
            <p className="text-2xl font-extrabold text-gray-900 font-mono">{total_time_minutes}m</p>
          </div>
        </div>

        {/* Answered Questions */}
        <div className="bg-white rounded-2xl p-5 border border-border-subtle shadow-sm flex items-center gap-4">
          <div className="w-12 h-12 bg-amber-50 text-amber-600 rounded-xl flex items-center justify-center flex-shrink-0">
            <Flame className="w-6 h-6" />
          </div>
          <div>
            <p className="text-xs font-semibold text-text-secondary uppercase tracking-wider">Questions Answered</p>
            <p className="text-2xl font-extrabold text-gray-900 font-mono">{total_questions_answered}</p>
          </div>
        </div>
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* Unit Mastery Bar Chart */}
        <div className="bg-white rounded-2xl p-6 sm:p-8 border border-border-subtle shadow-sm space-y-4">
          <div className="flex items-center justify-between">
            <h4 className="text-lg font-bold text-gray-900 flex items-center gap-2">
              <Award className="w-5 h-5 text-indigo-500" /> Unit Mastery Breakdown
            </h4>
            <span className="text-xs font-semibold text-gray-400">Target: &ge; 75%</span>
          </div>

          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={unit_mastery} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E5E7EB" />
                <XAxis dataKey="unit_id" axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: '#6B7280' }} dy={10} />
                <YAxis axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: '#6B7280' }} domain={[0, 100]} />
                <Tooltip content={<CustomTooltip />} cursor={{fill: '#F3F4F6'}} />
                <Bar dataKey="accuracy" name="Accuracy" radius={[6, 6, 0, 0]}>
                  {unit_mastery.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.accuracy >= 75 ? '#10b981' : entry.accuracy >= 50 ? '#f59e0b' : '#ef4444'} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Accuracy Trend Line Chart */}
        <div className="bg-white rounded-2xl p-6 sm:p-8 border border-border-subtle shadow-sm space-y-4">
          <div className="flex items-center justify-between">
            <h4 className="text-lg font-bold text-gray-900 flex items-center gap-2">
              <TrendingUp className="w-5 h-5 text-blue-500" /> Accuracy Trend Over Time
            </h4>
            <span className="text-xs font-semibold text-gray-400">{accuracy_trend.length} Sessions</span>
          </div>

          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={accuracy_trend} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E5E7EB" />
                <XAxis dataKey="attempt_num" axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: '#6B7280' }} dy={10} tickFormatter={(val) => `#${val}`} />
                <YAxis axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: '#6B7280' }} domain={[0, 100]} />
                <Tooltip content={<CustomTooltip label="Session" />} />
                <Line type="monotone" dataKey="accuracy" name="Accuracy" stroke="#3b82f6" strokeWidth={3} dot={{ r: 4, fill: '#3b82f6', strokeWidth: 2, stroke: '#fff' }} activeDot={{ r: 6 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Focus & Weak Spots Analysis + Recent Activity Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* Strengths & Focus Areas */}
        <div className="bg-white rounded-2xl p-6 border border-border-subtle shadow-sm space-y-4">
          <h4 className="text-lg font-bold text-gray-900 flex items-center gap-2">
            <span>🎯</span> Topic Diagnostics &amp; AI Focus Plan
          </h4>

          <div className="space-y-3">
            {/* Strong Topics */}
            <div className="p-4 bg-emerald-50/70 border border-emerald-200 rounded-xl space-y-1.5">
              <div className="flex items-center gap-2 text-xs font-bold text-emerald-800 uppercase">
                <CheckCircle className="w-4 h-4 text-emerald-600" />
                <span>Strong Mastery Topics</span>
              </div>
              <p className="text-xs text-emerald-950 font-medium">
                {strong_topics.length > 0 ? strong_topics.join(', ') : 'Keep practicing to establish high-confidence strong topics!'}
              </p>
            </div>

            {/* Weak Topics */}
            <div className="p-4 bg-amber-50/70 border border-amber-200 rounded-xl space-y-1.5">
              <div className="flex items-center gap-2 text-xs font-bold text-amber-800 uppercase">
                <AlertTriangle className="w-4 h-4 text-amber-600" />
                <span>Focus Areas (Needs Practice)</span>
              </div>
              <p className="text-xs text-amber-950 font-medium">
                {weak_topics.length > 0 ? weak_topics.join(', ') : 'No critical weak spots detected. Excellent consistency!'}
              </p>
            </div>
          </div>
        </div>

        {/* Recent Activity Log */}
        <div className="bg-white rounded-2xl p-6 border border-border-subtle shadow-sm space-y-4">
          <h4 className="text-lg font-bold text-gray-900 flex items-center gap-2">
            <span>📋</span> Recent Practice &amp; Exam Sessions
          </h4>

          {recent_activity.length === 0 ? (
            <p className="text-xs text-gray-500 py-6 text-center">No recent practice submissions logged.</p>
          ) : (
            <div className="space-y-2.5 max-h-60 overflow-y-auto pr-1">
              {recent_activity.map((act, idx) => (
                <div key={idx} className="flex items-center justify-between p-3 bg-gray-50 rounded-xl border border-gray-200 text-xs">
                  <div>
                    <span className="font-bold text-gray-900">{act.type || 'Practice'}</span>
                    <p className="text-[11px] text-gray-500">Score: {act.score} / {act.total} • Time: {act.time_formatted || 'N/A'}</p>
                  </div>
                  <span className={`px-2.5 py-1 rounded-full font-bold font-mono ${act.accuracy >= 75 ? 'bg-emerald-100 text-emerald-800' : act.accuracy >= 50 ? 'bg-amber-100 text-amber-800' : 'bg-red-100 text-red-800'}`}>
                    {act.accuracy}%
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
