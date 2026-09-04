import React, { useState, useEffect } from 'react';
import { useAppStore } from '../store/appStore';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, LineChart, Line, CartesianGrid, Cell } from 'recharts';
import { Target, TrendingUp, Award, BookOpen } from 'lucide-react';
import { getApiBaseUrl } from '../config';

export default function Performance() {
  const { activeSubjectName } = useAppStore();
  const searchParams = new URLSearchParams(window.location.search);
  const subjectId = searchParams.get('subject');

  const [loading, setLoading] = useState(true);
  const [data, setData] = useState(null);

  useEffect(() => {
    if (!subjectId) return;
    
    fetch(`${getApiBaseUrl()}/api/subjects/${subjectId}/performance`)
      .then(res => res.json())
      .then(resData => {
        setData(resData);
        setLoading(false);
      })
      .catch(err => {
        console.error("Failed to fetch performance data", err);
        setLoading(false);
      });
  }, [subjectId]);

  if (loading) {
    return <div className="p-8 text-center text-text-secondary">Loading performance metrics...</div>;
  }

  if (!data || data.total_quizzes === 0) {
    return (
      <div className="bg-white rounded-2xl p-8 border border-border-subtle shadow-sm flex flex-col min-h-[400px] items-center justify-center text-center">
        <div className="w-16 h-16 bg-blue-50 text-blue-500 rounded-full flex items-center justify-center mb-4">
          <TrendingUp className="w-8 h-8" />
        </div>
        <h3 className="text-xl font-bold text-primary mb-2">No Data Yet</h3>
        <p className="text-text-secondary max-w-md">
          You haven't completed any quizzes for this subject. Head over to the Practice tab, generate a quiz, and your performance will appear here!
        </p>
      </div>
    );
  }

  const { total_quizzes, overall_accuracy, unit_mastery, accuracy_trend } = data;

  const CustomTooltip = ({ active, payload, label, suffix = '%' }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-3 border border-border-subtle shadow-md rounded-xl">
          <p className="text-sm font-semibold text-primary">{label}</p>
          <p className="text-sm text-blue-600">
            {payload[0].name}: <span className="font-bold">{payload[0].value.toFixed(1)}{suffix}</span>
          </p>
          {payload[0].payload.total_questions && (
            <p className="text-xs text-text-secondary mt-1">
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
      {/* Header */}
      <div className="bg-white rounded-2xl p-6 sm:p-8 border border-border-subtle shadow-sm">
        <h3 className="text-2xl font-bold text-primary mb-2">Performance Analytics</h3>
        <p className="text-text-secondary">Track your mastery and progress for <span className="font-semibold text-primary">{activeSubjectName}</span>.</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white rounded-2xl p-6 border border-border-subtle shadow-sm flex items-center">
          <div className="w-12 h-12 bg-blue-50 rounded-full flex items-center justify-center mr-4">
            <BookOpen className="w-6 h-6 text-blue-600" />
          </div>
          <div>
            <p className="text-sm font-semibold text-text-secondary">Total Quizzes</p>
            <p className="text-2xl font-bold text-primary">{total_quizzes}</p>
          </div>
        </div>
        
        <div className="bg-white rounded-2xl p-6 border border-border-subtle shadow-sm flex items-center">
          <div className="w-12 h-12 bg-green-50 rounded-full flex items-center justify-center mr-4">
            <Target className="w-6 h-6 text-green-600" />
          </div>
          <div>
            <p className="text-sm font-semibold text-text-secondary">Overall Accuracy</p>
            <p className="text-2xl font-bold text-primary">{overall_accuracy}%</p>
          </div>
        </div>
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* Unit Mastery Bar Chart */}
        <div className="bg-white rounded-2xl p-6 sm:p-8 border border-border-subtle shadow-sm">
          <h4 className="text-lg font-bold text-primary mb-6 flex items-center">
            <Award className="w-5 h-5 mr-2 text-indigo-500" /> Unit Mastery
          </h4>
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={unit_mastery} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E5E7EB" />
                <XAxis dataKey="unit_id" axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: '#6B7280' }} dy={10} />
                <YAxis axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: '#6B7280' }} domain={[0, 100]} />
                <Tooltip content={<CustomTooltip />} cursor={{fill: '#F3F4F6'}} />
                <Bar dataKey="accuracy" name="Accuracy" radius={[4, 4, 0, 0]}>
                  {unit_mastery.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.accuracy >= 75 ? '#4ade80' : entry.accuracy >= 50 ? '#facc15' : '#f87171'} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Accuracy Trend Line Chart */}
        <div className="bg-white rounded-2xl p-6 sm:p-8 border border-border-subtle shadow-sm">
          <h4 className="text-lg font-bold text-primary mb-6 flex items-center">
            <TrendingUp className="w-5 h-5 mr-2 text-blue-500" /> Progress Over Time
          </h4>
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={accuracy_trend} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E5E7EB" />
                <XAxis dataKey="attempt_num" axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: '#6B7280' }} dy={10} tickFormatter={(val) => `Quiz ${val}`} />
                <YAxis axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: '#6B7280' }} domain={[0, 100]} />
                <Tooltip content={<CustomTooltip label="Attempt" />} />
                <Line type="monotone" dataKey="accuracy" name="Accuracy" stroke="#3b82f6" strokeWidth={3} dot={{ r: 4, fill: '#3b82f6', strokeWidth: 2, stroke: '#fff' }} activeDot={{ r: 6 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
}
