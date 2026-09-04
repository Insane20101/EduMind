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
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const { setSubject, activeSubjectName, subjectsData, fetchSubjects } = useAppStore();
  
  const semParam = searchParams.get('sem');
  const subjectParam = searchParams.get('subject');
  
  const [activeTab, setActiveTab] = useState('Learn');
  const [practiceMode, setPracticeMode] = useState('menu'); // 'menu', 'manual', 'quiz'
  const tabs = ['Learn', 'Practice', 'Performance'];

  useEffect(() => {
    if (Object.keys(subjectsData).length === 0) {
      fetchSubjects();
    }
  }, [fetchSubjects, subjectsData]);

  useEffect(() => {
    if (semParam && subjectParam && Object.keys(subjectsData).length > 0) {
      const semSubjects = subjectsData[semParam] || [];
      const sub = semSubjects.find(s => s.code === subjectParam);
      setSubject(subjectParam, sub ? sub.name : subjectParam);
    }
  }, [semParam, subjectParam, setSubject, subjectsData]);

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
        {activeTab === 'Practice' && practiceMode === 'menu' && (
          <div className="bg-white rounded-2xl p-8 border border-border-subtle shadow-sm flex flex-col min-h-[400px]">
            <div className="mb-8 text-center sm:text-left">
              <h3 className="text-2xl font-bold text-primary mb-2">Practice Modes</h3>
              <p className="text-text-secondary text-lg">Master <span className="font-semibold text-primary">{activeSubjectName}</span> with tailored practice sessions.</p>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 lg:gap-8 flex-1">
              
              {/* Option 1 */}
              <div 
                onClick={() => setPracticeMode('manual')}
                className="relative group overflow-hidden bg-white border border-border-subtle rounded-2xl p-6 sm:p-8 hover:border-transparent hover:shadow-xl transition-all duration-300 flex flex-col cursor-pointer transform hover:-translate-y-1"
              >
                <div className="absolute inset-0 bg-gradient-to-br from-blue-50/50 via-indigo-50/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none" />
                <div className="absolute inset-0 bg-gradient-to-br from-blue-500 to-indigo-600 opacity-0 group-hover:opacity-5 transition-opacity duration-300 rounded-2xl pointer-events-none" />
                <div className="absolute inset-0 rounded-2xl border-2 border-transparent group-hover:border-indigo-500/20 transition-colors duration-300 pointer-events-none" />
                
                <div className="relative z-10">
                  <h4 className="text-xl font-bold text-primary mb-3">Manual Practice</h4>
                  <p className="text-text-secondary mb-8 leading-relaxed flex-1">Access comprehensive question banks unit by unit. Dive deep into specific topics at your own pace with detailed solutions.</p>
                  
                  <div className="mt-auto flex items-center text-sm font-semibold text-blue-600 group-hover:text-indigo-600">
                    Select Unit 
                    <svg className="ml-2 w-4 h-4 transform group-hover:translate-x-1 transition-transform" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
                  </div>
                </div>
              </div>

              {/* Option 2 */}
              <div 
                onClick={() => setPracticeMode('quiz')}
                className="relative group overflow-hidden bg-white border border-border-subtle rounded-2xl p-6 sm:p-8 hover:border-transparent hover:shadow-xl transition-all duration-300 flex flex-col cursor-pointer transform hover:-translate-y-1"
              >
                <div className="absolute inset-0 bg-gradient-to-br from-purple-50/50 via-pink-50/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none" />
                <div className="absolute inset-0 bg-gradient-to-br from-purple-500 to-pink-600 opacity-0 group-hover:opacity-5 transition-opacity duration-300 rounded-2xl pointer-events-none" />
                <div className="absolute inset-0 rounded-2xl border-2 border-transparent group-hover:border-purple-500/20 transition-colors duration-300 pointer-events-none" />
                
                <div className="relative z-10">
                  <h4 className="text-xl font-bold text-primary mb-3">Generate Custom Quiz</h4>
                  <p className="text-text-secondary mb-8 leading-relaxed flex-1">Configure a personalized test. Choose specific units (1-4 or combined), set your difficulty, and pick the number of questions.</p>
                  
                  <div className="mt-auto flex items-center text-sm font-semibold text-purple-600 group-hover:text-pink-600">
                    Configure Quiz 
                    <svg className="ml-2 w-4 h-4 transform group-hover:translate-x-1 transition-transform" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
                  </div>
                </div>
              </div>

            </div>
          </div>
        )}
        {activeTab === 'Practice' && practiceMode === 'manual' && (
          <div>
            <button 
              onClick={() => setPracticeMode('menu')}
              className="flex items-center text-sm font-medium text-text-secondary hover:text-primary mb-4 transition-colors"
            >
              <ArrowLeft size={16} className="mr-1" /> Back to Practice Menu
            </button>
            <Practice />
          </div>
        )}
        {activeTab === 'Practice' && practiceMode === 'quiz' && (
          <div>
            <button 
              onClick={() => setPracticeMode('menu')}
              className="flex items-center text-sm font-medium text-text-secondary hover:text-primary mb-4 transition-colors"
            >
              <ArrowLeft size={16} className="mr-1" /> Back to Practice Menu
            </button>
            <QuizGenerator />
          </div>
        )}
        {activeTab === 'Performance' && (
          <Performance />
        )}
      </div>
    </div>
  );
}
