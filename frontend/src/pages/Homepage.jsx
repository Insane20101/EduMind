import React, { useEffect, useState, useRef } from 'react';
import { useAppStore } from '../store/appStore';
import { useAuth } from '../store/useAuth';
import SubjectCard from '../components/SubjectCard';
import { Sparkles, Paperclip, Send, FileText, X } from 'lucide-react';

export default function Homepage() {
  const { 
    branch, 
    sem, 
    clearSubject, 
    setSemester, 
    setBranch, 
    subjectsData, 
    fetchSubjects, 
    isLoadingSubjects,
    tempFile,
    setTempFile,
    clearTempFile,
    sendPrompt
  } = useAppStore();

  const { user } = useAuth();
  const [homeInput, setHomeInput] = useState('');
  const fileInputRef = useRef(null);

  useEffect(() => {
    fetchSubjects();
  }, [fetchSubjects]);
  
  useEffect(() => {
    clearSubject();
    if (user) {
      if (user.branch) setBranch(user.branch);
      if (user.semester) setSemester(user.semester);
    }
  }, [clearSubject, user, setSemester, setBranch]);

  const handleFileAttach = (e) => {
    const file = e.target.files?.[0];
    if (file) {
      setTempFile(file);
    }
  };

  const handleAskAI = (e) => {
    e.preventDefault();
    if (!homeInput.trim() && !tempFile) return;
    
    // Automatically dispatch prompt to chat drawer & start AI response
    sendPrompt(homeInput.trim());
    setHomeInput('');
  };

  const userName = user ? `${user.first_name}${user.middle_name ? ' ' + user.middle_name : ''} ${user.last_name}` : "Student";
  const displayBranch = user?.branch || branch;
  const rawSem = user?.semester || sem || "Semester-3";
  const displaySem = rawSem;
  const semKeyHyphen = rawSem.includes('-') ? rawSem : rawSem.replace(' ', '-');
  
  // Robust subject lookup matching both "Semester-7" and "Semester 7"
  const currentSubjects = subjectsData[semKeyHyphen] || 
    subjectsData[rawSem] || 
    Object.entries(subjectsData).find(([k]) => k.replace(/[\s-]/g, '').toLowerCase() === semKeyHyphen.replace(/[\s-]/g, '').toLowerCase())?.[1] || 
    subjectsData["Semester-3"] || 
    [];

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8 pb-32">
      {/* ── Welcome Header & Hero Section ────────────────────────────── */}
      <div className="mb-10 text-center sm:text-left">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
          <div>
            <h1 className="text-3xl sm:text-4xl font-bold text-slate-800 tracking-tight">
              Welcome Back, <span className="text-primary">{userName}</span>! 👋
            </h1>
            <p className="text-text-secondary text-base font-medium mt-1">
              {rawSem.replace('-', ' ')} • Branch: <span className="font-semibold text-slate-700">{displayBranch}</span>
            </p>
          </div>
        </div>

        {/* ── Homepage Hero Chat & Google AI Attachment Input Bar ───────────── */}
        <div className="bg-gradient-to-r from-blue-900/90 via-indigo-900 to-slate-900 p-6 sm:p-8 rounded-3xl shadow-xl text-white relative overflow-hidden">
          <div className="absolute top-0 right-0 -mt-8 -mr-8 w-48 h-48 bg-blue-500/20 rounded-full blur-3xl pointer-events-none" />
          
          <div className="relative z-10 max-w-3xl">
            <div className="flex items-center gap-2 mb-3">
              <span className="bg-blue-500/30 text-blue-200 text-xs font-semibold px-3 py-1 rounded-full border border-blue-400/30 flex items-center gap-1.5">
                <Sparkles size={14} className="text-yellow-300 animate-spin" /> Google AI OCR Document Chat
              </span>
            </div>
            
            <h2 className="text-xl sm:text-2xl font-bold mb-2">
              What do you want to learn or analyze today?
            </h2>
            <p className="text-blue-100/80 text-sm mb-6 max-w-xl leading-relaxed">
              Ask any question across your subjects or attach a PDF/Image for instant AI text extraction and detailed analysis.
            </p>

            {/* File Attachment Chip */}
            {tempFile && (
              <div className="mb-3 px-3 py-2 bg-white/10 border border-white/20 rounded-xl flex items-center justify-between text-xs text-white max-w-md backdrop-blur-md">
                <div className="flex items-center gap-2 truncate">
                  <FileText size={16} className="text-blue-300 shrink-0" />
                  <span className="font-medium truncate">{tempFile.name}</span>
                  <span className="text-[10px] bg-blue-500/40 text-blue-100 px-2 py-0.5 rounded font-mono shrink-0">
                    Google AI Ready
                  </span>
                </div>
                <button 
                  type="button" 
                  onClick={clearTempFile}
                  className="text-blue-200 hover:text-white transition-colors p-1"
                >
                  <X size={14} />
                </button>
              </div>
            )}

            <form onSubmit={handleAskAI} className="flex items-center gap-2 max-w-2xl bg-white/15 backdrop-blur-md p-2 rounded-2xl border border-white/20 shadow-inner">
              <input 
                type="file" 
                ref={fileInputRef} 
                onChange={handleFileAttach}
                accept=".pdf,.png,.jpg,.jpeg,.webp" 
                className="hidden" 
              />

              <button
                type="button"
                onClick={() => fileInputRef.current?.click()}
                className="p-3 rounded-xl bg-white/20 hover:bg-white/30 text-white transition-colors flex items-center justify-center shrink-0"
                title="Attach PDF or Image for Google AI OCR"
              >
                <Paperclip size={20} />
              </button>

              <input 
                type="text"
                value={homeInput}
                onChange={(e) => setHomeInput(e.target.value)}
                placeholder={tempFile ? "Ask about attached document..." : "Ask EduMind AI anything or attach a PDF..."}
                className="flex-1 bg-transparent border-none outline-none px-3 text-white placeholder-blue-200/70 text-sm sm:text-base min-w-0"
              />

              <button
                type="submit"
                className="px-5 py-3 rounded-xl bg-gradient-to-r from-blue-500 to-indigo-500 hover:from-blue-600 hover:to-indigo-600 text-white font-semibold text-sm flex items-center gap-2 shadow-md transition-all shrink-0"
              >
                <span>Ask AI</span>
                <Send size={16} />
              </button>
            </form>
          </div>
        </div>
      </div>

      {/* ── My Subjects Grid ────────────────────────────────────────── */}
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-slate-800">My Subjects</h2>
        <p className="text-text-secondary text-sm font-medium">Select a subject to explore units, notes, practice &amp; RAG context</p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {isLoadingSubjects ? (
          <p className="text-text-secondary">Loading subjects...</p>
        ) : currentSubjects.length > 0 ? (
          currentSubjects.map((subject, idx) => (
            <SubjectCard key={idx} subject={subject} />
          ))
        ) : (
          <p className="text-text-secondary">No subjects found for {displaySem}.</p>
        )}
      </div>
    </div>
  );
}
