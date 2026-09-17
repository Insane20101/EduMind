import React, { useState, useEffect } from 'react';
import { cn, formatTextSpacing, preprocessMarkdownContent } from '../lib/utils';
import { useAppStore } from '../store/appStore';
import { ChevronDown, ChevronUp, Download, Sparkles, BookOpen, Clock, Bookmark, AlertTriangle, Lightbulb, FlipHorizontal, RefreshCw, X, Send, HelpCircle, CheckCircle2, XCircle, Target, Layers, Sliders } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import remarkMath from 'remark-math';
import remarkBreaks from 'remark-breaks';
import rehypeKatex from 'rehype-katex';
import rehypeRaw from 'rehype-raw';
import MermaidViewer from './MermaidViewer';
import { exportPracticeSheetPdf } from '../utils/PdfExportService';
import { getApiBaseUrl } from '../config';

const MarkdownComponents = {
  h3: ({node, ...props}) => {
    let textContent = '';
    React.Children.forEach(props.children, child => {
      if (typeof child === 'string') textContent += child;
    });
    const match = textContent.match(/^(Step\s*\d+)\s*(?:—|-)?\s*(.*)/i);
    if (match) {
      return (
        <div className="mt-6 mb-3 flex items-center">
          <span className="text-xs font-bold px-2 py-1 rounded bg-blue-100 text-blue-800 mr-3 border border-blue-200 shadow-sm uppercase tracking-wider">
            {match[1]}
          </span>
          {match[2] && <span className="text-sm font-semibold text-gray-800 leading-none">{match[2]}</span>}
        </div>
      );
    }
    return <h3 className="text-lg font-semibold mt-4 mb-2 text-gray-800" {...props} />;
  }
};

export default function Practice() {
  const { subject: storeSubject, activeSubjectName } = useAppStore();
  const searchParams = new URLSearchParams(window.location.search);
  const subjectId = searchParams.get('subject') || storeSubject;

  const [activeSubMode, setActiveSubMode] = useState('adaptive'); // 'adaptive', 'mcq', 'exam', 'mistakes', 'cram'
  
  // Standard / Adaptive State
  const [available, setAvailable] = useState(null);
  const [units, setUnits] = useState([]);
  const [selectedUnit, setSelectedUnit] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [loadingQuestions, setLoadingQuestions] = useState(false);
  const [solutions, setSolutions] = useState({});
  const [loadingSolutions, setLoadingSolutions] = useState({});
  const [expandedQuestions, setExpandedQuestions] = useState({});
  
  // Hints State
  const [activeHintQuestionId, setActiveHintQuestionId] = useState(null);
  const [hintsData, setHintsData] = useState({});
  const [loadingHints, setLoadingHints] = useState({});
  const [currentHintStep, setCurrentHintStep] = useState({});

  // AI Tutor Side Drawer State
  const [tutorOpen, setTutorOpen] = useState(false);
  const [tutorQuery, setTutorQuery] = useState('');
  const [tutorResponse, setTutorResponse] = useState(null);
  const [tutorLoading, setTutorLoading] = useState(false);

  // Timed Exam State
  const [examDuration, setExamDuration] = useState(30);
  const [examSelectedUnits, setExamSelectedUnits] = useState(['All Units']);
  const [examDifficulty, setExamDifficulty] = useState('Medium');
  const [examActive, setExamActive] = useState(false);
  const [examTimeLeft, setExamTimeLeft] = useState(1800);
  const [examQuestions, setExamQuestions] = useState([]);
  const [examAnswers, setExamAnswers] = useState({});
  const [examFinished, setExamFinished] = useState(false);
  const [evaluatingExam, setEvaluatingExam] = useState(false);
  const [examResult, setExamResult] = useState(null);
  const [loadingExam, setLoadingExam] = useState(false);

  // MCQs Practice State
  const [mcqSelectedUnits, setMcqSelectedUnits] = useState(['All Units']);
  const [mcqDifficulty, setMcqDifficulty] = useState('Medium');
  const [mcqCount, setMcqCount] = useState(20); // Min 15, Max 60
  const [mcqActive, setMcqActive] = useState(false);
  const [mcqQuestions, setMcqQuestions] = useState([]);
  const [mcqAnswers, setMcqAnswers] = useState({});
  const [mcqQuestionTimes, setMcqQuestionTimes] = useState({});
  const [mcqOverallTime, setMcqOverallTime] = useState(0);
  const [mcqFinished, setMcqFinished] = useState(false);
  const [evaluatingMcq, setEvaluatingMcq] = useState(false);
  const [mcqResult, setMcqResult] = useState(null);
  const [loadingMcqs, setLoadingMcqs] = useState(false);

  // Mistakes & Bookmarks State
  const [bookmarks, setBookmarks] = useState([]);
  const [mistakes, setMistakes] = useState([]);
  const [savedTab, setSavedTab] = useState('bookmarks');

  // Cram Protocol State
  const [cramCards, setCramCards] = useState([]);
  const [cramIndex, setCramIndex] = useState(0);
  const [isFlipped, setIsFlipped] = useState(false);
  const [cramLoading, setCramLoading] = useState(false);

  // Diagram Mode State
  const [diagramAssets, setDiagramAssets] = useState([]);
  const [diagramLoading, setDiagramLoading] = useState(false);

  useEffect(() => {
    if (!subjectId) return;
    
    // Fetch units for manual/adaptive practice
    fetch(`${getApiBaseUrl()}/api/subjects/${subjectId}/practice`)
      .then(res => res.json())
      .then(data => {
        if (data.available) {
          setAvailable(true);
          setUnits(data.units);
          if (data.units.length > 0) {
            setSelectedUnit(data.units[0].unit_id);
          }
        } else {
          setAvailable(false);
        }
      })
      .catch(err => {
        console.error("Failed to load practice info", err);
        setAvailable(false);
      });
  }, [subjectId]);

  useEffect(() => {
    if (!subjectId || !selectedUnit) return;
    
    setLoadingQuestions(true);
    setQuestions([]);
    setSolutions({});
    setExpandedQuestions({});
    
    fetch(`${getApiBaseUrl()}/api/subjects/${subjectId}/practice/${selectedUnit}`)
      .then(res => res.json())
      .then(data => {
        setQuestions(data.questions || []);
        setLoadingQuestions(false);
      })
      .catch(err => {
        console.error("Failed to load questions", err);
        setLoadingQuestions(false);
      });
  }, [subjectId, selectedUnit]);

  // Load Bookmarks & Mistakes
  useEffect(() => {
    if (activeSubMode === 'mistakes') {
      const token = localStorage.getItem('token');
      if (!token) return;
      
      fetch(`${getApiBaseUrl()}/api/practice/bookmarks`, {
        headers: { 'Authorization': `Bearer ${token}` }
      })
        .then(r => r.ok ? r.json() : [])
        .then(data => setBookmarks(Array.isArray(data) ? data : []))
        .catch(console.error);

      fetch(`${getApiBaseUrl()}/api/practice/mistakes`, {
        headers: { 'Authorization': `Bearer ${token}` }
      })
        .then(r => r.ok ? r.json() : [])
        .then(data => setMistakes(Array.isArray(data) ? data : []))
        .catch(console.error);
    }
  }, [activeSubMode]);

  // Load Cram Cards
  useEffect(() => {
    if (activeSubMode === 'cram' && subjectId) {
      setCramLoading(true);
      fetch(`${getApiBaseUrl()}/api/practice/cram/${subjectId}`)
        .then(r => r.json())
        .then(data => {
          setCramCards(data.cards || []);
          setCramLoading(false);
        })
        .catch(() => setCramLoading(false));
    }
  }, [activeSubMode, subjectId]);

  // Exam Countdown Timer
  useEffect(() => {
    if (!examActive || examTimeLeft <= 0) return;
    const timer = setInterval(() => {
      setExamTimeLeft(prev => {
        if (prev <= 1) {
          clearInterval(timer);
          handleExamSubmit();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
    return () => clearInterval(timer);
  }, [examActive, examTimeLeft]);

  // MCQ Practice Timer Effect (Self-Paced Overall Timer)
  useEffect(() => {
    if (!mcqActive || mcqFinished) return;
    const timer = setInterval(() => {
      setMcqOverallTime(prev => prev + 1);
    }, 1000);
    return () => clearInterval(timer);
  }, [mcqActive, mcqFinished]);

  const toggleUnitSelection = (unitName, currentList, setList) => {
    if (unitName === 'All Units') {
      setList(['All Units']);
      return;
    }
    let updated = currentList.filter(u => u !== 'All Units');
    if (updated.includes(unitName)) {
      updated = updated.filter(u => u !== unitName);
    } else {
      updated.push(unitName);
    }
    if (updated.length === 0) updated = ['All Units'];
    setList(updated);
  };

  const startExamSession = () => {
    setLoadingExam(true);
    setExamActive(false);
    setExamFinished(false);
    setExamResult(null);
    setExamTimeLeft(examDuration * 60);
    setExamAnswers({});
    
    fetch(`${getApiBaseUrl()}/api/practice/exam-session`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        subject_id: subjectId, 
        duration_minutes: examDuration,
        unit_ids: examSelectedUnits,
        difficulty: examDifficulty
      })
    })
      .then(r => r.json())
      .then(data => {
        const mapped = (data.questions || []).map((q, idx) => ({
          ...q,
          question_id: q.question_id || q.id || `exam_q_${idx + 1}`
        }));
        setExamQuestions(mapped);
        setExamActive(true);
        setLoadingExam(false);
      })
      .catch((err) => {
        console.error(err);
        setLoadingExam(false);
      });
  };

  const startMcqSession = () => {
    setLoadingMcqs(true);
    setMcqActive(false);
    setMcqFinished(false);
    setMcqResult(null);
    setMcqAnswers({});
    setMcqQuestionTimes({});
    setMcqOverallTime(0);

    fetch(`${getApiBaseUrl()}/api/practice/mcq-session`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        subject_id: subjectId,
        unit_ids: mcqSelectedUnits,
        difficulty: mcqDifficulty,
        count: mcqCount
      })
    })
      .then(r => r.json())
      .then(data => {
        setMcqQuestions(data.questions || []);
        setMcqActive(true);
        setLoadingMcqs(false);
      })
      .catch((err) => {
        console.error(err);
        setLoadingMcqs(false);
      });
  };

  const handleSelectMcqOption = (qId, optionIdx) => {
    setMcqAnswers(prev => ({ ...prev, [qId]: optionIdx }));
    setMcqQuestionTimes(prev => ({
      ...prev,
      [qId]: (prev[qId] || 0) + 5
    }));
  };

  const handleMcqSubmit = () => {
    setEvaluatingMcq(true);
    setMcqActive(false);

    const token = localStorage.getItem('token');
    const headers = { 'Content-Type': 'application/json' };
    if (token) headers['Authorization'] = `Bearer ${token}`;

    fetch(`${getApiBaseUrl()}/api/practice/submit-mcq`, {
      method: 'POST',
      headers,
      body: JSON.stringify({
        subject_id: subjectId,
        total_time_seconds: mcqOverallTime,
        question_times: mcqQuestionTimes,
        answers: mcqAnswers,
        questions: mcqQuestions
      })
    })
      .then(r => r.json())
      .then(data => {
        setMcqResult(data);
        setMcqFinished(true);
        setEvaluatingMcq(false);
      })
      .catch((err) => {
        console.error(err);
        setEvaluatingMcq(false);
        setMcqFinished(true);
      });
  };

  const handleExamSubmit = async () => {
    setExamActive(false);
    setExamFinished(true);
    setEvaluatingExam(true);

    const timeSpentSeconds = (examDuration * 60) - examTimeLeft;

    try {
      const token = localStorage.getItem('token');
      const headers = { 'Content-Type': 'application/json' };
      if (token) headers['Authorization'] = `Bearer ${token}`;

      const res = await fetch(`${getApiBaseUrl()}/api/practice/submit-exam`, {
        method: 'POST',
        headers,
        body: JSON.stringify({
          subject_id: subjectId,
          duration_minutes: examDuration,
          time_taken_seconds: timeSpentSeconds,
          answers: examAnswers,
          questions: examQuestions
        })
      });

      if (res.ok) {
        const evalData = await res.json();
        setExamResult(evalData);
        saveLocalAttempt(evalData);
      } else {
        generateFallbackEvaluation(timeSpentSeconds);
      }
    } catch (e) {
      console.error(e);
      generateFallbackEvaluation(timeSpentSeconds);
    } finally {
      setEvaluatingExam(false);
    }
  };

  const saveLocalAttempt = (evalData) => {
    try {
      const storageKey = `edumind_attempts_${subjectId || 'GENERAL'}`;
      const existing = JSON.parse(localStorage.getItem(storageKey) || '[]');
      const newAttempt = {
        quiz_id: evalData.session_id || `exam_${Date.now()}`,
        score: evalData.score,
        total: evalData.total_marks,
        accuracy: evalData.accuracy,
        time_taken_seconds: evalData.time_taken_seconds,
        submitted_at: Date.now() / 1000,
        type: 'timed_exam'
      };
      existing.push(newAttempt);
      localStorage.setItem(storageKey, JSON.stringify(existing));
    } catch (e) {
      console.error(e);
    }
  };

  const generateFallbackEvaluation = (timeSpentSeconds) => {
    let totalMarks = 0;
    let score = 0;
    let answeredCount = 0;
    const evals = examQuestions.map((q, idx) => {
      const qKey = q.question_id || q.id || `exam_q_${idx + 1}`;
      const m = q.marks || 2;
      totalMarks += m;
      const userAns = (examAnswers[qKey] || '').trim();
      const isAns = userAns.length > 0;
      if (isAns) {
        answeredCount++;
        score += userAns.length >= 15 ? m : 1;
      }
      return {
        question_id: qKey,
        question_text: q.question_text || q.question,
        marks: m,
        score: isAns ? (userAns.length >= 15 ? m : 1) : 0,
        user_answer: userAns || '(No answer provided)',
        solution: q.solution || q.answer || 'Refer to standard course notes for step-by-step derivation.'
      };
    });

    const acc = totalMarks > 0 ? Math.round((score / totalMarks * 100) * 10) / 10 : 0;
    const resultObj = {
      score,
      total_marks: totalMarks,
      accuracy: acc,
      time_taken_seconds: timeSpentSeconds,
      time_formatted: `${Math.floor(timeSpentSeconds / 60)}m ${timeSpentSeconds % 60}s`,
      answered_count: answeredCount,
      total_questions: examQuestions.length,
      evaluations: evals
    };
    setExamResult(resultObj);
    saveLocalAttempt(resultObj);
  };

  const toggleSolution = (questionId) => {
    const isExpanded = expandedQuestions[questionId];
    setExpandedQuestions(prev => ({ ...prev, [questionId]: !isExpanded }));
    
    if (!isExpanded && !solutions[questionId] && !loadingSolutions[questionId]) {
      setLoadingSolutions(prev => ({ ...prev, [questionId]: true }));
      fetch(`${getApiBaseUrl()}/api/subjects/${subjectId}/practice/${selectedUnit}/${questionId}/solution`)
        .then(async res => {
          if (!res.ok) throw new Error("404");
          const data = await res.json();
          setSolutions(prev => ({ ...prev, [questionId]: data.solution_text }));
          setLoadingSolutions(prev => ({ ...prev, [questionId]: false }));
        })
        .catch(() => {
          setSolutions(prev => ({ ...prev, [questionId]: "Solution missing for this question." }));
          setLoadingSolutions(prev => ({ ...prev, [questionId]: false }));
        });
    }
  };

  const fetchHints = (questionId) => {
    if (hintsData[questionId]) {
      setActiveHintQuestionId(activeHintQuestionId === questionId ? null : questionId);
      return;
    }
    setLoadingHints(prev => ({ ...prev, [questionId]: true }));
    fetch(`${getApiBaseUrl()}/api/practice/hints/${questionId}`)
      .then(r => r.json())
      .then(data => {
        setHintsData(prev => ({ ...prev, [questionId]: data.hints || [] }));
        setCurrentHintStep(prev => ({ ...prev, [questionId]: 0 }));
        setActiveHintQuestionId(questionId);
        setLoadingHints(prev => ({ ...prev, [questionId]: false }));
      })
      .catch(() => {
        setLoadingHints(prev => ({ ...prev, [questionId]: false }));
      });
  };

  const handleTutorSubmit = (e) => {
    e.preventDefault();
    if (!tutorQuery.trim()) return;
    setTutorLoading(true);
    setTutorResponse(null);

    fetch(`${getApiBaseUrl()}/api/practice/tutor-explain`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: tutorQuery, subject_id: subjectId, unit: selectedUnit })
    })
      .then(r => r.json())
      .then(data => {
        setTutorResponse(data);
        setTutorLoading(false);
      })
      .catch(() => setTutorLoading(false));
  };

  const bookmarkQuestion = async (q) => {
    const token = localStorage.getItem('token');
    if (!token) {
      alert("Please log in to save bookmarks.");
      return;
    }
    try {
      await fetch(`${getApiBaseUrl()}/api/practice/bookmark`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
        body: JSON.stringify({ subject_id: subjectId, question: q })
      });
      alert("Question saved to Bookmarks!");
    } catch (e) {
      console.error(e);
    }
  };

  const formatTime = (seconds) => {
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
  };

  return (
    <div className="bg-white rounded-2xl p-4 sm:p-8 border border-border-subtle shadow-sm flex flex-col min-h-[500px]">
      
      {/* Top Header & Sub-Mode Navigation */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between border-b border-gray-100 pb-6 mb-6 gap-4">
        <div>
          <h3 className="text-2xl font-bold text-gray-900">Intelligence Practice Studio</h3>
          <p className="text-sm text-gray-500">Master <span className="font-semibold text-blue-600">{activeSubjectName || subjectId}</span> with adaptive AI modes.</p>
        </div>
        
        <div className="flex items-center gap-2">
          {activeSubMode === 'adaptive' && questions.length > 0 && (
            <button
              onClick={() => exportPracticeSheetPdf(subjectId, questions, `${activeSubjectName || subjectId} Practice Sheet`)}
              className="flex items-center gap-2 px-3 py-2 text-xs font-semibold text-blue-700 bg-blue-50 hover:bg-blue-100 border border-blue-200 rounded-lg transition-colors shadow-sm"
            >
              <Download className="w-4 h-4" /> Export PDF Sheet
            </button>
          )}
          <button
            onClick={() => setTutorOpen(!tutorOpen)}
            className="flex items-center gap-2 px-3 py-2 text-xs font-semibold text-purple-700 bg-purple-50 hover:bg-purple-100 border border-purple-200 rounded-lg transition-colors shadow-sm"
          >
            <Sparkles className="w-4 h-4 text-purple-600" /> Ask AI Tutor
          </button>
        </div>
      </div>

      {/* Sub-Mode Tabs */}
      <div className="flex overflow-x-auto hide-scrollbar gap-2 mb-6 border-b border-gray-200 pb-2">
        <button
          onClick={() => setActiveSubMode('adaptive')}
          className={`flex items-center gap-2 px-4 py-2 rounded-lg font-semibold text-xs sm:text-sm whitespace-nowrap transition-all ${
            activeSubMode === 'adaptive'
              ? "bg-blue-600 text-white shadow-md font-bold"
              : "bg-slate-200/90 dark:bg-slate-800 text-slate-900 dark:text-slate-100 hover:bg-slate-300 dark:hover:bg-slate-700 border border-slate-300 dark:border-slate-700"
          }`}
        >
          <BookOpen className="w-4 h-4" /> Standard &amp; Adaptive
        </button>

        <button
          onClick={() => setActiveSubMode('mcq')}
          className={`flex items-center gap-2 px-4 py-2 rounded-lg font-semibold text-xs sm:text-sm whitespace-nowrap transition-all ${
            activeSubMode === 'mcq'
              ? "bg-blue-600 text-white shadow-md font-bold"
              : "bg-slate-200/90 dark:bg-slate-800 text-slate-900 dark:text-slate-100 hover:bg-slate-300 dark:hover:bg-slate-700 border border-slate-300 dark:border-slate-700"
          }`}
        >
          <HelpCircle className="w-4 h-4" /> MCQs Practice &amp; Quiz
        </button>

        <button
          onClick={() => setActiveSubMode('exam')}
          className={`flex items-center gap-2 px-4 py-2 rounded-lg font-semibold text-xs sm:text-sm whitespace-nowrap transition-all ${
            activeSubMode === 'exam'
              ? "bg-blue-600 text-white shadow-md font-bold"
              : "bg-slate-200/90 dark:bg-slate-800 text-slate-900 dark:text-slate-100 hover:bg-slate-300 dark:hover:bg-slate-700 border border-slate-300 dark:border-slate-700"
          }`}
        >
          <Clock className="w-4 h-4" /> Timed Exam Simulation
        </button>

        <button
          onClick={() => setActiveSubMode('mistakes')}
          className={`flex items-center gap-2 px-4 py-2 rounded-lg font-semibold text-xs sm:text-sm whitespace-nowrap transition-all ${
            activeSubMode === 'mistakes'
              ? "bg-blue-600 text-white shadow-md font-bold"
              : "bg-slate-200/90 dark:bg-slate-800 text-slate-900 dark:text-slate-100 hover:bg-slate-300 dark:hover:bg-slate-700 border border-slate-300 dark:border-slate-700"
          }`}
        >
          <Bookmark className="w-4 h-4" /> Mistake Notebook &amp; Saved
        </button>

        <button
          onClick={() => setActiveSubMode('cram')}
          className={`flex items-center gap-2 px-4 py-2 rounded-lg font-semibold text-xs sm:text-sm whitespace-nowrap transition-all ${
            activeSubMode === 'cram'
              ? "bg-blue-600 text-white shadow-md font-bold"
              : "bg-slate-200/90 dark:bg-slate-800 text-slate-900 dark:text-slate-100 hover:bg-slate-300 dark:hover:bg-slate-700 border border-slate-300 dark:border-slate-700"
          }`}
        >
          <AlertTriangle className="w-4 h-4" /> 5-Min Cram Protocol
        </button>
      </div>

      {/* ── MODE 1: Standard & Adaptive ────────────────────────────────────── */}
      {activeSubMode === 'adaptive' && (
        <div className="space-y-6">
          {/* Unit Selector */}
          <div className="flex overflow-x-auto hide-scrollbar gap-2 pb-2">
            {units.map((u) => (
              <button
                key={u.unit_id}
                onClick={() => setSelectedUnit(u.unit_id)}
                className={`px-4 py-2 rounded-full font-medium text-xs sm:text-sm whitespace-nowrap transition-colors ${
                  selectedUnit === u.unit_id 
                    ? "bg-blue-600 text-white shadow" 
                    : "bg-blue-50 text-blue-700 hover:bg-blue-100 border border-blue-200"
                }`}
              >
                {u.unit_id} <span className="ml-1 opacity-75 text-xs">({u.count})</span>
              </button>
            ))}
          </div>

          {/* Question List */}
          <div className="space-y-4">
            {loadingQuestions ? (
              <div className="text-center py-12 text-gray-500">Loading questions...</div>
            ) : questions.length === 0 ? (
              <div className="text-center py-12 text-gray-500">No practice questions available for this unit yet.</div>
            ) : (
              questions.map((q, idx) => {
                const isExpanded = expandedQuestions[q.question_id];
                const hints = hintsData[q.question_id] || [];
                const hintStep = currentHintStep[q.question_id] || 0;

                return (
                  <div key={q.question_id || idx} className="border border-gray-200 rounded-xl overflow-hidden bg-white shadow-xs">
                    <div className="p-5">
                      <div className="flex items-center justify-between gap-2 mb-3">
                        <div className="flex flex-wrap items-center gap-2">
                          <span className="text-xs font-bold px-2.5 py-1 rounded-lg bg-blue-100 dark:bg-blue-900/40 text-blue-800 dark:text-blue-200 border border-blue-200 dark:border-blue-800/60">
                            Q{idx + 1}
                          </span>
                          <span className="text-xs font-semibold px-2.5 py-1 rounded-lg bg-blue-100 dark:bg-blue-900/40 text-blue-800 dark:text-blue-200 border border-blue-200 dark:border-blue-800/60">
                            {q.marks || 2} Marks
                          </span>
                          {q.metadata?.topic && q.metadata.topic !== 'unassigned' && (
                            <span className="text-xs font-semibold px-2.5 py-1 rounded-lg bg-blue-100 dark:bg-blue-900/40 text-blue-800 dark:text-blue-200 border border-blue-200 dark:border-blue-800/60">
                              {q.metadata.topic}
                            </span>
                          )}
                        </div>
                        <button
                          onClick={() => bookmarkQuestion(q)}
                          className="text-gray-400 hover:text-blue-600 p-1 transition-colors"
                          title="Bookmark Question"
                        >
                          <Bookmark className="w-4 h-4" />
                        </button>
                      </div>

                      <div className="prose prose-sm max-w-none text-gray-800 mb-4">
                        <ReactMarkdown 
                          remarkPlugins={[remarkMath, remarkBreaks]} 
                          rehypePlugins={[rehypeKatex, rehypeRaw]}
                          components={MarkdownComponents}
                        >
                          {formatTextSpacing(q.question_text || q.question)}
                        </ReactMarkdown>
                      </div>

                      {/* Progressive AI Hints */}
                      {activeHintQuestionId === q.question_id && (
                        <div className="mb-4 p-4 bg-amber-50/80 border border-amber-200 rounded-lg">
                          <div className="flex items-center justify-between mb-2">
                            <span className="text-xs font-bold text-amber-800 flex items-center gap-1">
                              <Lightbulb className="w-4 h-4" /> Progressive Hint ({hintStep + 1} / {hints.length || 3})
                            </span>
                            {hints.length > 0 && hintStep < hints.length - 1 && (
                              <button
                                onClick={() => setCurrentHintStep(prev => ({ ...prev, [q.question_id]: hintStep + 1 }))}
                                className="text-xs font-semibold text-amber-700 hover:underline"
                              >
                                Next Hint →
                              </button>
                            )}
                          </div>
                          <p className="text-xs sm:text-sm text-amber-900">
                            {hints[hintStep] || "Review the key formulas and input parameters given in your course notes."}
                          </p>
                        </div>
                      )}

                      <div className="flex items-center gap-4 border-t border-gray-100 pt-3">
                        <button 
                          onClick={() => toggleSolution(q.question_id)}
                          className="flex items-center text-xs font-semibold text-blue-600 hover:text-blue-800 transition-colors"
                        >
                          {isExpanded ? (
                            <><ChevronUp className="w-4 h-4 mr-1" /> Hide Solution</>
                          ) : (
                            <><ChevronDown className="w-4 h-4 mr-1" /> Show Solution</>
                          )}
                        </button>

                        <button 
                          onClick={() => fetchHints(q.question_id)}
                          className="flex items-center text-xs font-semibold text-amber-600 hover:text-amber-800 transition-colors"
                        >
                          <Lightbulb className="w-3.5 h-3.5 mr-1" /> 
                          {loadingHints[q.question_id] ? "Loading Hint..." : "AI Hint"}
                        </button>
                      </div>
                    </div>

                    {isExpanded && (
                      <div className="border-t border-gray-200 bg-gray-50/50 p-5">
                        {loadingSolutions[q.question_id] ? (
                          <div className="text-xs text-gray-500 italic">Loading full solution...</div>
                        ) : (
                          <div className="prose prose-sm max-w-none text-gray-800">
                            <ReactMarkdown 
                              remarkPlugins={[remarkMath, remarkBreaks]} 
                              rehypePlugins={[rehypeKatex, rehypeRaw]}
                              components={MarkdownComponents}
                            >
                              {preprocessMarkdownContent(formatTextSpacing(solutions[q.question_id])) || "Solution unavailable."}
                            </ReactMarkdown>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                );
              })
            )}
          </div>
        </div>
      )}

      {/* ── MODE 1B: MCQs Practice & Quiz (New Section) ─────────────────────────── */}
      {activeSubMode === 'mcq' && (
        <div className="space-y-6">
          {!mcqActive && !mcqFinished ? (
            <div className="max-w-2xl mx-auto p-6 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl space-y-6 shadow-sm">
              <div className="text-center space-y-2">
                <div className="w-14 h-14 bg-blue-100 dark:bg-blue-900/50 text-blue-600 dark:text-blue-400 rounded-2xl flex items-center justify-center mx-auto shadow-inner">
                  <HelpCircle className="w-7 h-7" />
                </div>
                <h4 className="text-xl font-bold text-gray-900 dark:text-white">MCQs Practice &amp; Revision Engine</h4>
                <p className="text-xs sm:text-sm text-gray-600 dark:text-slate-300 max-w-lg mx-auto">
                  Extensive conceptual &amp; numerical multiple choice questions designed for fast clarity, syllabus mastery, and exam revision.
                </p>
              </div>

              {/* Unit Selection */}
              <div className="space-y-2">
                <label className="text-xs font-bold text-gray-700 dark:text-slate-300 flex items-center gap-1.5 uppercase tracking-wider">
                  <Layers size={14} className="text-blue-500" /> Select Unit(s) (1 to 4)
                </label>
                <div className="flex flex-wrap gap-2">
                  {['All Units', 'Unit 1', 'Unit 2', 'Unit 3', 'Unit 4'].map(u => {
                    const isSelected = mcqSelectedUnits.includes(u);
                    return (
                      <button
                        key={u}
                        type="button"
                        onClick={() => toggleUnitSelection(u, mcqSelectedUnits, setMcqSelectedUnits)}
                        className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all border ${
                          isSelected
                            ? "bg-blue-600 text-white border-blue-600 shadow-xs font-bold"
                            : "bg-white dark:bg-slate-800 text-gray-700 dark:text-slate-300 border-gray-300 dark:border-slate-700 hover:bg-gray-100 dark:hover:bg-slate-700"
                        }`}
                      >
                        {u}
                      </button>
                    );
                  })}
                </div>
              </div>

              {/* Difficulty Selection */}
              <div className="space-y-2">
                <label className="text-xs font-bold text-gray-700 dark:text-slate-300 flex items-center gap-1.5 uppercase tracking-wider">
                  <Target size={14} className="text-blue-500" /> Question Difficulty
                </label>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
                  {['Easy', 'Medium', 'Hard', 'Exam Level'].map(diff => (
                    <button
                      key={diff}
                      type="button"
                      onClick={() => setMcqDifficulty(diff)}
                      className={`px-3 py-2 rounded-xl text-xs font-bold transition-all border text-center ${
                        mcqDifficulty === diff
                          ? "bg-indigo-600 text-white border-indigo-600 shadow-xs"
                          : "bg-white dark:bg-slate-800 text-gray-700 dark:text-slate-300 border-gray-300 dark:border-slate-700 hover:bg-gray-100 dark:hover:bg-slate-700"
                      }`}
                    >
                      {diff}
                    </button>
                  ))}
                </div>
              </div>

              {/* Number of Questions (Min 15, Max 60) */}
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <label className="text-xs font-bold text-gray-700 dark:text-slate-300 flex items-center gap-1.5 uppercase tracking-wider">
                    <Sliders size={14} className="text-blue-500" /> Number of Questions (15 to 60)
                  </label>
                  <span className="text-sm font-black text-blue-600 dark:text-blue-400 bg-blue-50 dark:bg-blue-900/40 px-2.5 py-0.5 rounded-lg border border-blue-200 dark:border-blue-800">
                    {mcqCount} Questions
                  </span>
                </div>

                <input
                  type="range"
                  min="15"
                  max="60"
                  step="1"
                  value={mcqCount}
                  onChange={(e) => setMcqCount(parseInt(e.target.value))}
                  className="w-full accent-blue-600 cursor-pointer"
                />

                <div className="flex justify-between gap-2 pt-1">
                  {[15, 25, 40, 60].map(val => (
                    <button
                      key={val}
                      type="button"
                      onClick={() => setMcqCount(val)}
                      className={`px-3 py-1 rounded-md text-xs font-semibold border ${
                        mcqCount === val
                          ? "bg-blue-100 dark:bg-blue-900/60 text-blue-800 dark:text-blue-200 border-blue-300"
                          : "bg-white dark:bg-slate-800 text-gray-600 dark:text-slate-400 border-gray-200 dark:border-slate-700"
                      }`}
                    >
                      {val} Qs
                    </button>
                  ))}
                </div>
                <p className="text-[11px] text-gray-500 dark:text-slate-400 italic">
                  Note: MCQs mode is extensive (15 to 60 questions) to cover every concept line and numerical variation without a strict timer cutoff.
                </p>
              </div>

              <button
                type="button"
                disabled={loadingMcqs}
                onClick={startMcqSession}
                className="w-full py-3.5 bg-blue-600 hover:bg-blue-700 text-white font-extrabold text-sm rounded-xl shadow-md transition-all flex items-center justify-center gap-2 cursor-pointer disabled:opacity-50"
              >
                {loadingMcqs ? (
                  <><RefreshCw className="w-4 h-4 animate-spin" /> Generating MCQ Practice Set...</>
                ) : (
                  <><Sparkles className="w-4 h-4" /> Generate MCQ Practice Set ({mcqCount} Qs)</>
                )}
              </button>
            </div>
          ) : mcqFinished ? (
            <div className="space-y-6">
              {evaluatingMcq ? (
                <div className="text-center py-16 space-y-3">
                  <RefreshCw className="w-8 h-8 text-blue-600 animate-spin mx-auto" />
                  <p className="text-base font-bold text-gray-800 dark:text-white">Evaluating your MCQ Practice Session...</p>
                  <p className="text-xs text-gray-500">Calculating score, analyzing time spent per question, and logging performance.</p>
                </div>
              ) : (
                <div className="space-y-6 animate-in fade-in duration-300">
                  {/* Results Summary Card */}
                  <div className="bg-gradient-to-r from-slate-900 via-blue-950 to-slate-900 text-white rounded-2xl p-6 shadow-xl border border-blue-500/30">
                    <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-slate-800 pb-4">
                      <div>
                        <span className="text-xs font-bold text-blue-400 uppercase tracking-wider">MCQ Practice Results</span>
                        <h4 className="text-2xl font-extrabold text-white mt-0.5">Session Overview</h4>
                      </div>
                      <button
                        onClick={startMcqSession}
                        className="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs rounded-xl shadow transition-all cursor-pointer"
                      >
                        New MCQ Practice Session 🔄
                      </button>
                    </div>

                    <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mt-5 text-center">
                      <div className="bg-slate-800/80 p-3 rounded-xl border border-slate-700/60">
                        <span className="text-[11px] text-slate-400 font-semibold uppercase">Score</span>
                        <div className="text-2xl font-black text-amber-400 font-mono mt-1">
                          {mcqResult?.score ?? 0} / {mcqResult?.total_questions ?? 0}
                        </div>
                      </div>

                      <div className="bg-slate-800/80 p-3 rounded-xl border border-slate-700/60">
                        <span className="text-[11px] text-slate-400 font-semibold uppercase">Accuracy</span>
                        <div className="text-2xl font-black text-emerald-400 font-mono mt-1">
                          {mcqResult?.accuracy ?? 0}%
                        </div>
                      </div>

                      <div className="bg-slate-800/80 p-3 rounded-xl border border-slate-700/60">
                        <span className="text-[11px] text-slate-400 font-semibold uppercase">Total Time</span>
                        <div className="text-2xl font-black text-blue-400 font-mono mt-1">
                          {formatTime(mcqOverallTime)}
                        </div>
                      </div>

                      <div className="bg-slate-800/80 p-3 rounded-xl border border-slate-700/60">
                        <span className="text-[11px] text-slate-400 font-semibold uppercase">Avg Time / Q</span>
                        <div className="text-2xl font-black text-indigo-400 font-mono mt-1">
                          {mcqResult?.total_questions ? `${Math.round(mcqOverallTime / mcqResult.total_questions)}s` : '0s'}
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Detailed MCQ Evaluation List */}
                  <div className="space-y-4">
                    <h4 className="text-base font-bold text-gray-900 dark:text-white flex items-center gap-2">
                      <span>🎯</span> Detailed Question Breakdown &amp; Solutions
                    </h4>

                    {(mcqResult?.evaluations || []).map((ev, idx) => (
                      <div key={ev.question_id || idx} className="p-5 border border-gray-200 dark:border-slate-800 rounded-xl bg-white dark:bg-slate-900 shadow-xs space-y-3">
                        <div className="flex flex-wrap items-center justify-between gap-2 border-b border-gray-100 dark:border-slate-800 pb-2.5">
                          <div className="flex items-center gap-2">
                            <span className="text-xs font-bold text-blue-600 dark:text-blue-400 uppercase">
                              Q{idx + 1} ({ev.unit || 'Unit 1'})
                            </span>
                            <span className="text-xs font-medium px-2 py-0.5 rounded bg-blue-50 dark:bg-blue-900/40 text-blue-700 dark:text-blue-300 border border-blue-200 dark:border-blue-800">
                              ⏱️ Time spent: {ev.time_spent_seconds || 0}s
                            </span>
                          </div>
                          
                          <span className={`text-xs font-bold px-2.5 py-0.5 rounded-full flex items-center gap-1 ${
                            ev.is_correct ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300' : 'bg-red-100 text-red-800 dark:bg-red-950 dark:text-red-300'
                          }`}>
                            {ev.is_correct ? <><CheckCircle2 size={14} /> Correct</> : <><XCircle size={14} /> Incorrect</>}
                          </span>
                        </div>

                        <p className="text-sm font-semibold text-gray-900 dark:text-slate-100">{ev.question_text}</p>

                        {/* Options List */}
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 pt-1">
                          {(ev.options || []).map((opt, oIdx) => {
                            const isUserPick = ev.user_selected_index === oIdx;
                            const isCorrectOpt = ev.correct_option_index === oIdx;
                            let styleClass = "bg-gray-50 dark:bg-slate-800 border-gray-200 dark:border-slate-700 text-gray-700 dark:text-slate-300";
                            
                            if (isCorrectOpt) {
                              styleClass = "bg-emerald-50 dark:bg-emerald-950/60 border-emerald-300 text-emerald-900 dark:text-emerald-200 font-bold";
                            } else if (isUserPick && !isCorrectOpt) {
                              styleClass = "bg-red-50 dark:bg-red-950/60 border-red-300 text-red-900 dark:text-red-200 font-bold";
                            }

                            return (
                              <div key={oIdx} className={`p-2.5 rounded-lg border text-xs flex items-center justify-between ${styleClass}`}>
                                <span>{opt}</span>
                                {isCorrectOpt && <span className="text-[10px] bg-emerald-200 text-emerald-900 px-1.5 py-0.5 rounded font-bold">Correct</span>}
                                {isUserPick && !isCorrectOpt && <span className="text-[10px] bg-red-200 text-red-900 px-1.5 py-0.5 rounded font-bold">Your Choice</span>}
                              </div>
                            );
                          })}
                        </div>

                        {/* Explanation Box */}
                        <div className="p-3.5 bg-blue-50/70 dark:bg-blue-950/40 border border-blue-200 dark:border-blue-900/60 rounded-lg text-xs text-slate-800 dark:text-slate-200">
                          <strong className="text-blue-900 dark:text-blue-300 block mb-1">Concept &amp; Solution Explanation:</strong>
                          <p className="whitespace-pre-wrap leading-relaxed">{ev.explanation}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div className="space-y-6">
              {/* MCQ Active Quiz Header Bar */}
              <div className="flex items-center justify-between bg-slate-900 text-white px-5 py-3.5 rounded-xl shadow">
                <div className="flex items-center gap-3">
                  <span className="font-bold text-sm text-blue-400">MCQs Revision Session</span>
                  <span className="text-xs bg-slate-800 px-2.5 py-1 rounded font-mono text-slate-300">
                    Answered: {Object.keys(mcqAnswers).length} / {mcqQuestions.length}
                  </span>
                </div>
                <div className="flex items-center gap-4">
                  <span className="text-sm font-mono font-bold text-emerald-400">⏱️ {formatTime(mcqOverallTime)}</span>
                  <button
                    onClick={handleMcqSubmit}
                    className="text-xs bg-blue-600 hover:bg-blue-700 text-white px-3.5 py-1.5 rounded-lg font-bold transition-all cursor-pointer shadow"
                  >
                    Submit Quiz
                  </button>
                </div>
              </div>

              {/* MCQ Active Question List */}
              <div className="space-y-6">
                {mcqQuestions.map((q, idx) => {
                  const qKey = q.question_id || `mcq_q_${idx + 1}`;
                  const selectedOpt = mcqAnswers[qKey];
                  return (
                    <div key={qKey} className="p-5 border border-gray-200 dark:border-slate-800 rounded-xl bg-white dark:bg-slate-900 shadow-xs space-y-4">
                      <div className="flex items-center justify-between border-b border-gray-100 dark:border-slate-800 pb-2">
                        <span className="text-xs font-bold text-blue-600 dark:text-blue-400 uppercase">Question {idx + 1} of {mcqQuestions.length} ({q.unit || 'Unit 1'})</span>
                        <span className="text-xs font-semibold bg-blue-100 dark:bg-blue-900/40 text-blue-800 dark:text-blue-200 px-2 py-0.5 rounded border border-blue-200 dark:border-blue-800">{q.difficulty || 'Medium'}</span>
                      </div>

                      <p className="text-sm sm:text-base font-semibold text-gray-900 dark:text-slate-100 leading-relaxed">{q.question_text}</p>

                      {/* Options Grid */}
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-1">
                        {(q.options || []).map((opt, oIdx) => {
                          const isPicked = selectedOpt === oIdx;
                          return (
                            <button
                              key={oIdx}
                              type="button"
                              onClick={() => handleSelectMcqOption(qKey, oIdx)}
                              className={`p-3 rounded-xl border text-left text-xs sm:text-sm font-medium transition-all flex items-center justify-between ${
                                isPicked
                                  ? "bg-blue-600 text-white border-blue-600 shadow-sm font-bold"
                                  : "bg-slate-50 dark:bg-slate-800 text-gray-800 dark:text-slate-200 border-gray-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-700"
                              }`}
                            >
                              <span>{opt}</span>
                              {isPicked && <CheckCircle2 size={16} className="shrink-0 text-white" />}
                            </button>
                          );
                        })}
                      </div>
                    </div>
                  );
                })}

                <button
                  type="button"
                  onClick={handleMcqSubmit}
                  className="w-full py-4 bg-blue-600 hover:bg-blue-700 text-white font-extrabold text-base rounded-xl shadow-lg transition-all cursor-pointer"
                >
                  Submit &amp; Evaluate MCQ Practice Set
                </button>
              </div>
            </div>
          )}
        </div>
      )}

      {/* ── MODE 2: Timed Exam Simulation ────────────────────────────────────── */}
      {activeSubMode === 'exam' && (
        <div className="space-y-6">
          {!examActive && !examFinished ? (
            <div className="max-w-2xl mx-auto p-6 bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl space-y-6 shadow-sm">
              <div className="text-center space-y-2">
                <div className="w-14 h-14 bg-blue-100 dark:bg-blue-900/50 text-blue-600 dark:text-blue-400 rounded-2xl flex items-center justify-center mx-auto shadow-inner">
                  <Clock className="w-7 h-7" />
                </div>
                <h4 className="text-xl font-bold text-gray-900 dark:text-white">Timed Exam Simulation</h4>
                <p className="text-xs sm:text-sm text-gray-600 dark:text-slate-300 max-w-lg mx-auto">
                  Simulate real university exam conditions with restricted 2, 3, and 5 mark questions under strict countdown conditions.
                </p>
              </div>

              {/* Unit Selection (Units 1 to 4) */}
              <div className="space-y-2">
                <label className="text-xs font-bold text-gray-700 dark:text-slate-300 flex items-center gap-1.5 uppercase tracking-wider">
                  <Layers size={14} className="text-blue-500" /> Select Unit(s) (1 to 4)
                </label>
                <div className="flex flex-wrap gap-2">
                  {['All Units', 'Unit 1', 'Unit 2', 'Unit 3', 'Unit 4'].map(u => {
                    const isSelected = examSelectedUnits.includes(u);
                    return (
                      <button
                        key={u}
                        type="button"
                        onClick={() => toggleUnitSelection(u, examSelectedUnits, setExamSelectedUnits)}
                        className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all border ${
                          isSelected
                            ? "bg-blue-600 text-white border-blue-600 shadow-xs font-bold"
                            : "bg-white dark:bg-slate-800 text-gray-700 dark:text-slate-300 border-gray-300 dark:border-slate-700 hover:bg-gray-100 dark:hover:bg-slate-700"
                        }`}
                      >
                        {u}
                      </button>
                    );
                  })}
                </div>
              </div>

              {/* Difficulty Selection */}
              <div className="space-y-2">
                <label className="text-xs font-bold text-gray-700 dark:text-slate-300 flex items-center gap-1.5 uppercase tracking-wider">
                  <Target size={14} className="text-blue-500" /> Exam Question Difficulty
                </label>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
                  {['Easy', 'Medium', 'Hard', 'Exam Level'].map(diff => (
                    <button
                      key={diff}
                      type="button"
                      onClick={() => setExamDifficulty(diff)}
                      className={`px-3 py-2 rounded-xl text-xs font-bold transition-all border text-center ${
                        examDifficulty === diff
                          ? "bg-indigo-600 text-white border-indigo-600 shadow-xs"
                          : "bg-white dark:bg-slate-800 text-gray-700 dark:text-slate-300 border-gray-300 dark:border-slate-700 hover:bg-gray-100 dark:hover:bg-slate-700"
                      }`}
                    >
                      {diff}
                    </button>
                  ))}
                </div>
              </div>

              {/* Duration Selection */}
              <div className="space-y-2">
                <label className="text-xs font-bold text-gray-700 dark:text-slate-300 flex items-center gap-1.5 uppercase tracking-wider">
                  <Clock size={14} className="text-blue-500" /> Exam Duration
                </label>
                <div className="flex justify-center gap-2">
                  {[15, 30, 45, 60].map(mins => (
                    <button
                      key={mins}
                      type="button"
                      onClick={() => setExamDuration(mins)}
                      className={`flex-1 py-2 rounded-xl font-semibold text-xs sm:text-sm border transition-all text-center ${
                        examDuration === mins
                          ? "bg-blue-600 text-white border-blue-600 font-bold shadow-xs"
                          : "bg-white dark:bg-slate-800 text-gray-700 dark:text-slate-300 border-gray-300 dark:border-slate-700 hover:bg-gray-100 dark:hover:bg-slate-700"
                      }`}
                    >
                      {mins} Mins
                    </button>
                  ))}
                </div>
              </div>

              <button
                type="button"
                disabled={loadingExam}
                onClick={startExamSession}
                className="w-full py-3.5 bg-blue-600 hover:bg-blue-700 text-white font-extrabold text-sm rounded-xl shadow-md transition-all flex items-center justify-center gap-2 cursor-pointer disabled:opacity-50"
              >
                {loadingExam ? (
                  <><RefreshCw className="w-4 h-4 animate-spin" /> Preparing Exam Session...</>
                ) : (
                  <><Sparkles className="w-4 h-4" /> Start Timed Exam Session Now</>
                )}
              </button>
            </div>
          ) : examFinished ? (
            <div className="space-y-6">
              {evaluatingExam ? (
                <div className="text-center py-16 space-y-3">
                  <RefreshCw className="w-8 h-8 text-blue-600 animate-spin mx-auto" />
                  <p className="text-base font-bold text-gray-800">Evaluating your Exam Answers...</p>
                  <p className="text-xs text-gray-500">Scoring answers, calculating accuracy, and syncing performance analytics.</p>
                </div>
              ) : (
                <div className="space-y-6 animate-in fade-in duration-300">
                  {/* Results Header Card */}
                  <div className="bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 text-white rounded-2xl p-6 shadow-xl border border-indigo-500/30">
                    <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-slate-800 pb-4">
                      <div>
                        <span className="text-xs font-bold text-indigo-400 uppercase tracking-wider">Exam Submission Results</span>
                        <h4 className="text-2xl font-extrabold text-white mt-0.5">Session Overview</h4>
                      </div>
                      <button
                        onClick={startExamSession}
                        className="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs rounded-xl shadow transition-all self-start sm:self-auto cursor-pointer"
                      >
                        Retake Exam Session 🔄
                      </button>
                    </div>

                    <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mt-5 text-center">
                      <div className="bg-slate-800/80 p-3 rounded-xl border border-slate-700/60">
                        <span className="text-[11px] text-slate-400 font-semibold uppercase">Total Score</span>
                        <div className="text-2xl font-black text-amber-400 font-mono mt-1">
                          {examResult?.score ?? 0} / {examResult?.total_marks ?? 0}
                        </div>
                      </div>

                      <div className="bg-slate-800/80 p-3 rounded-xl border border-slate-700/60">
                        <span className="text-[11px] text-slate-400 font-semibold uppercase">Accuracy</span>
                        <div className="text-2xl font-black text-emerald-400 font-mono mt-1">
                          {examResult?.accuracy ?? 0}%
                        </div>
                      </div>

                      <div className="bg-slate-800/80 p-3 rounded-xl border border-slate-700/60">
                        <span className="text-[11px] text-slate-400 font-semibold uppercase">Questions Answered</span>
                        <div className="text-2xl font-black text-blue-400 font-mono mt-1">
                          {examResult?.answered_count ?? 0} / {examResult?.total_questions ?? 0}
                        </div>
                      </div>

                      <div className="bg-slate-800/80 p-3 rounded-xl border border-slate-700/60">
                        <span className="text-[11px] text-slate-400 font-semibold uppercase">Time Spent</span>
                        <div className="text-2xl font-black text-purple-300 font-mono mt-1">
                          {examResult?.time_formatted || '0m 0s'}
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Question Evaluation & Model Answer Breakdown */}
                  <div className="space-y-4">
                    <h4 className="text-base font-bold text-gray-900 flex items-center gap-2">
                      <span>📝</span> Question-by-Question Evaluation &amp; Model Solutions
                    </h4>

                    {(examResult?.evaluations || []).map((ev, idx) => (
                      <div key={ev.question_id || idx} className="p-5 border border-gray-200 rounded-xl bg-white shadow-xs space-y-3">
                        <div className="flex items-center justify-between gap-2 border-b border-gray-100 pb-2.5">
                          <span className="text-xs font-bold text-blue-600 uppercase">Question {idx + 1} ({ev.marks} Marks)</span>
                          <span className={`text-xs font-bold px-2.5 py-0.5 rounded-full ${ev.score === ev.marks ? 'bg-emerald-100 text-emerald-800' : ev.score > 0 ? 'bg-amber-100 text-amber-800' : 'bg-red-100 text-red-800'}`}>
                            Earned: {ev.score} / {ev.marks} Marks
                          </span>
                        </div>

                        <p className="text-sm font-semibold text-gray-900">{ev.question_text}</p>

                        <div className="p-3 bg-gray-50 border border-gray-200 rounded-lg text-xs text-gray-800">
                          <strong className="text-gray-900 block mb-1">Your Submitted Answer:</strong>
                          <p className="whitespace-pre-wrap">{ev.user_answer}</p>
                        </div>

                        <div className="p-3.5 bg-blue-50/70 border border-blue-200 rounded-lg text-xs text-blue-950">
                          <strong className="text-blue-900 block mb-1">Model Solution &amp; Key Rubric Steps:</strong>
                          <ReactMarkdown 
                            remarkPlugins={[remarkMath, remarkBreaks]} 
                            rehypePlugins={[rehypeKatex, rehypeRaw]}
                            components={MarkdownComponents}
                          >
                            {preprocessMarkdownContent(formatTextSpacing(ev.solution))}
                          </ReactMarkdown>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div>
              <div className="flex items-center justify-between bg-gray-900 text-white px-5 py-3 rounded-xl mb-6 shadow">
                <span className="font-semibold text-sm">Exam in Progress</span>
                <span className="text-lg font-mono font-bold text-amber-400">{formatTime(examTimeLeft)}</span>
                <button
                  onClick={handleExamSubmit}
                  className="text-xs bg-red-600 hover:bg-red-700 px-3 py-1.5 rounded font-semibold transition-colors cursor-pointer"
                >
                  Submit Exam
                </button>
              </div>

              <div className="space-y-6">
                {examQuestions.map((q, idx) => {
                  const qKey = q.question_id || q.id || `exam_q_${idx + 1}`;
                  return (
                    <div key={qKey} className="p-5 border border-gray-200 rounded-xl bg-white shadow-xs">
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-xs font-bold text-blue-600 uppercase">Question {idx + 1}</span>
                        <span className="text-xs font-semibold bg-gray-100 text-gray-700 px-2 py-0.5 rounded">{q.marks || 2} Marks</span>
                      </div>
                      <p className="text-sm font-semibold text-gray-900 mb-4">{q.question_text || q.question}</p>
                      <textarea
                        placeholder="Type your structured solution here..."
                        rows={3}
                        value={examAnswers[qKey] || ''}
                        onChange={(e) => {
                          const val = e.target.value;
                          setExamAnswers(prev => ({ ...prev, [qKey]: val }));
                        }}
                        className="w-full text-sm p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none transition-all"
                      />
                    </div>
                  );
                })}
              </div>
            </div>
          )}
        </div>
      )}

      {/* ── MODE 3: Mistake Notebook & Bookmarks ────────────────────────────── */}
      {activeSubMode === 'mistakes' && (
        <div className="space-y-6">
          <div className="flex gap-4 border-b border-gray-200 pb-2">
            <button
              onClick={() => setSavedTab('bookmarks')}
              className={`font-bold text-sm pb-2 border-b-2 ${savedTab === 'bookmarks' ? 'border-blue-600 text-blue-600' : 'border-transparent text-gray-500'}`}
            >
              Saved Bookmarks ({bookmarks.length})
            </button>
            <button
              onClick={() => setSavedTab('mistakes')}
              className={`font-bold text-sm pb-2 border-b-2 ${savedTab === 'mistakes' ? 'border-blue-600 text-blue-600' : 'border-transparent text-gray-500'}`}
            >
              Mistake Notebook ({mistakes.length})
            </button>
          </div>

          {savedTab === 'bookmarks' ? (
            <div className="space-y-4">
              {bookmarks.length === 0 ? (
                <div className="text-center py-12 text-gray-400">No bookmarked questions yet. Click the bookmark icon on any question to save it!</div>
              ) : (
                bookmarks.map((b, i) => (
                  <div key={i} className="p-4 border border-gray-200 rounded-xl bg-white">
                    <span className="text-xs font-bold text-blue-600">{b.subject_id}</span>
                    <p className="text-sm font-medium text-gray-800 mt-1">{b.question?.question_text || b.question?.question || "Bookmarked item"}</p>
                  </div>
                ))
              )}
            </div>
          ) : (
            <div className="space-y-4">
              {mistakes.length === 0 ? (
                <div className="text-center py-12 text-gray-400">No logged mistakes found.</div>
              ) : (
                mistakes.map((m, i) => (
                  <div key={i} className="p-4 border border-red-200 rounded-xl bg-red-50/50">
                    <span className="text-xs font-bold text-red-600">{m.subject_id}</span>
                    <p className="text-sm font-medium text-gray-900 mt-1">{m.question}</p>
                    <div className="mt-2 text-xs text-red-700"><strong>Your Answer:</strong> {m.user_answer}</div>
                    <div className="text-xs text-green-700"><strong>Correct Answer:</strong> {m.correct_answer}</div>
                  </div>
                ))
              )}
            </div>
          )}
        </div>
      )}

      {/* ── MODE 4: 5-Minute Cram Protocol ───────────────────────────────────── */}
      {activeSubMode === 'cram' && (
        <div className="space-y-6 max-w-2xl mx-auto py-4">
          {cramLoading ? (
            <div className="text-center py-12 text-gray-500">Loading approved cram memory hooks...</div>
          ) : cramCards.length === 0 ? (
            <div className="text-center py-12 bg-amber-50 rounded-2xl border border-amber-200 p-8">
              <AlertTriangle className="w-10 h-10 text-amber-500 mx-auto mb-3" />
              <h4 className="text-lg font-bold text-amber-900">No Approved Cram Cards Yet</h4>
              <p className="text-sm text-amber-800 mt-1">Cram memory hooks for this subject are queued for teacher approval in the Admin Review Queue.</p>
            </div>
          ) : (
            <div className="space-y-6">
              {/* Flashcard Flip Component */}
              <div
                onClick={() => setIsFlipped(!isFlipped)}
                className="cursor-pointer min-h-[260px] p-8 rounded-2xl border-2 border-blue-200 bg-gradient-to-br from-blue-50 via-indigo-50 to-white shadow-lg flex flex-col justify-between transition-all transform hover:scale-[1.01]"
              >
                <div className="flex items-center justify-between text-xs font-bold text-blue-600">
                  <span>CARD {cramIndex + 1} OF {cramCards.length}</span>
                  <span className="flex items-center gap-1 text-gray-400"><FlipHorizontal className="w-4 h-4" /> Click to Flip</span>
                </div>

                <div className="py-6 text-center">
                  {!isFlipped ? (
                    <div>
                      <span className="text-xs font-bold text-indigo-700 bg-indigo-100 px-3 py-1 rounded-full uppercase tracking-wider">Concept</span>
                      <h4 className="text-2xl font-black text-gray-900 mt-3">{cramCards[cramIndex]?.topic || cramCards[cramIndex]?.content?.mnemonic || "Memory Hook"}</h4>
                    </div>
                  ) : (
                    <div className="text-left space-y-3">
                      <span className="text-xs font-bold text-emerald-700 bg-emerald-100 px-3 py-1 rounded-full uppercase tracking-wider">Recall Answer</span>
                      <p className="text-sm text-gray-800 font-medium">{cramCards[cramIndex]?.content?.quick_summary || cramCards[cramIndex]?.content?.explanation}</p>
                      {cramCards[cramIndex]?.content?.mnemonic && (
                        <div className="p-3 bg-amber-100/70 text-amber-900 rounded-lg text-xs font-semibold">
                          💡 Mnemonic: {cramCards[cramIndex]?.content?.mnemonic}
                        </div>
                      )}
                    </div>
                  )}
                </div>

                <div className="text-center text-xs text-gray-400">
                  {isFlipped ? "Showing Recall Answer" : "Showing Prompt Concept"}
                </div>
              </div>

              {/* Navigation Controls */}
              <div className="flex justify-between items-center">
                <button
                  disabled={cramIndex === 0}
                  onClick={() => { setCramIndex(prev => prev - 1); setIsFlipped(false); }}
                  className="px-4 py-2 text-sm font-semibold bg-gray-100 disabled:opacity-40 rounded-lg"
                >
                  ← Previous Card
                </button>
                <button
                  disabled={cramIndex === cramCards.length - 1}
                  onClick={() => { setCramIndex(prev => prev + 1); setIsFlipped(false); }}
                  className="px-4 py-2 text-sm font-semibold bg-blue-600 text-white disabled:opacity-40 rounded-lg"
                >
                  Next Card →
                </button>
              </div>
            </div>
          )}
        </div>
      )}

      {/* ── AI TUTOR SIDE DRAWER ────────────────────────────────────────────── */}
      {tutorOpen && (
        <div className="fixed inset-y-0 right-0 w-full sm:w-96 bg-white shadow-2xl z-50 border-l border-gray-200 p-6 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between border-b pb-4 mb-4">
              <div className="flex items-center gap-2">
                <Sparkles className="w-5 h-5 text-purple-600" />
                <h4 className="font-bold text-gray-900">AI Tutor Explainer</h4>
              </div>
              <button onClick={() => setTutorOpen(false)} className="text-gray-400 hover:text-gray-600">
                <X className="w-5 h-5" />
              </button>
            </div>

            <p className="text-xs text-gray-500 mb-4">Ask any concept question grounded strictly in your subject notes.</p>

            <form onSubmit={handleTutorSubmit} className="flex gap-2 mb-6">
              <input
                type="text"
                placeholder="Ask e.g. What is Master Theorem?"
                value={tutorQuery}
                onChange={e => setTutorQuery(e.target.value)}
                className="flex-1 text-xs sm:text-sm p-2.5 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
              />
              <button type="submit" disabled={tutorLoading} className="bg-purple-600 text-white px-3 py-2.5 rounded-lg text-xs font-semibold hover:bg-purple-700">
                <Send className="w-4 h-4" />
              </button>
            </form>

            {tutorLoading && <div className="text-xs text-purple-600 italic text-center">Searching course materials & synthesizing answer...</div>}

            {tutorResponse && (
              <div className="p-4 bg-purple-50 border border-purple-200 rounded-xl text-xs text-purple-950 space-y-2 max-h-[400px] overflow-y-auto">
                <p className="font-medium whitespace-pre-wrap">{tutorResponse.explanation}</p>
                {tutorResponse.citations && tutorResponse.citations.length > 0 && (
                  <div className="pt-2 border-t border-purple-200 text-[10px] text-purple-700">
                    <strong>Grounded Citations:</strong> {tutorResponse.citations.join(', ')}
                  </div>
                )}
              </div>
            )}
          </div>

          <div className="text-[11px] text-gray-400 text-center">
            EduMind AI Tutor • Grounded RAG Response
          </div>
        </div>
      )}

    </div>
  );
}
