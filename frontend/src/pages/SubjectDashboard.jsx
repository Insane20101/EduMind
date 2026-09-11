import React, { useEffect, useState } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { ArrowLeft } from 'lucide-react';
import { useAppStore } from '../store/appStore';
import LearnTab from '../components/LearnTab';
import Practice from '../components/Practice';
import QuizGenerator from '../components/QuizGenerator';
import Performance from '../components/Performance';
import { cn } from '../lib/utils';

export default function SubjectDashboard() {
  const tabs = ['Learn', 'Practice', 'Performance'];
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const { setSubject, setSemester, activeSubjectName, subjectsData, fetchSubjects } = useAppStore();
  
  const semParam = searchParams.get('sem');
  const subjectParam = searchParams.get('subject');
  
  const [activeTab, setActiveTab] = useState('Learn');
  const [practiceMode, setPracticeMode] = useState('menu'); // 'menu', 'manual', 'quiz'
  useEffect(() => {
    if (activeSubjectName) {
      document.title = `EduMind — ${activeSubjectName}`;
    } else {
      document.title = "EduMind — AI Study Assistant";
    }
  }, [activeSubjectName]);

  useEffect(() => {
    if (Object.keys(subjectsData).length === 0) {
      fetchSubjects();
    }
  }, [fetchSubjects, subjectsData]);

  useEffect(() => {
    if (semParam) {
      setSemester(semParam);
    }
    if (subjectParam && Object.keys(subjectsData).length > 0) {
      const semSubjects = subjectsData[semParam] || [];
      let sub = semSubjects.find(s => s.code === subjectParam);
      if (!sub) {
        // Fallback search across all semesters
        for (const list of Object.values(subjectsData)) {
          sub = list.find(s => s.code === subjectParam);
          if (sub) break;
        }
      }
      setSubject(subjectParam, sub ? sub.name : subjectParam);
    }
  }, [semParam, subjectParam, setSubject, setSemester, subjectsData]);

  return (
    <div className="flex flex-col min-h-screen">
      <div className="bg-white border-b border-border-subtle sticky top-16 z-40 shadow-sm">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center gap-4 mb-4">
            <button 
              onClick={() => navigate('/')}
              className="h-10 w-10 flex flex-shrink-0 items-center justify-center rounded-lg border border-border-subtle hover:bg-muted text-text-secondary transition-colors"
            >
              <ArrowLeft size={20} />
            </button>
            <h1 className="text-xl sm:text-2xl font-bold text-primary truncate">
              {activeSubjectName || subjectParam}
            </h1>
          </div>
          
          <div className="flex overflow-x-auto hide-scrollbar border-b border-border-subtle/50">
            {tabs.map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={cn(
                  "px-6 py-3 font-medium text-sm whitespace-nowrap border-b-2 transition-colors",
                  activeTab === tab 
                    ? "border-primary text-primary" 
                    : "border-transparent text-text-secondary hover:text-text-primary hover:border-border-subtle"
                )}
              >
                {tab}
              </button>
            ))}
          </div>
        </div>
      </div>
      
      <div className="flex-1 max-w-6xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-8 pb-32">
        {activeTab === 'Learn' && <LearnTab />}
        {activeTab === 'Practice' && (
          <Practice />
        )}
        {activeTab === 'Performance' && (
          <Performance />
        )}
      </div>
    </div>
  );
}
