import React, { useState, useEffect } from 'react';
import { cn, formatTextSpacing, preprocessMarkdownContent } from '../lib/utils';
import { useAppStore } from '../store/appStore';
import { ChevronDown, ChevronUp, Download, Sparkles, BookOpen, Clock, Bookmark, AlertTriangle, Lightbulb, FlipHorizontal, RefreshCw, X, Send } from 'lucide-react';
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

  const [activeSubMode, setActiveSubMode] = useState('adaptive'); // 'adaptive', 'exam', 'mistakes', 'diagrams', 'cram'
  
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
  const [examActive, setExamActive] = useState(false);
  const [examTimeLeft, setExamTimeLeft] = useState(1800);
  const [examQuestions, setExamQuestions] = useState([]);
  const [examAnswers, setExamAnswers] = useState({});
  const [examFinished, setExamFinished] = useState(false);

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
          setExamFinished(true);
          setExamActive(false);
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
    return () => clearInterval(timer);
  }, [examActive, examTimeLeft]);

  const startExamSession = () => {
    setExamActive(true);
    setExamFinished(false);
    setExamTimeLeft(examDuration * 60);
    setExamAnswers({});
    
    fetch(`${getApiBaseUrl()}/api/practice/exam-session`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ subject_id: subjectId, duration_minutes: examDuration })
    })
      .then(r => r.json())
      .then(data => {
        setExamQuestions(data.questions || []);
      })
      .catch(console.error);
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
          className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium text-xs sm:text-sm whitespace-nowrap transition-all ${
            activeSubMode === 'adaptive'
              ? "bg-blue-600 text-white shadow-md"
              : "bg-gray-100 text-gray-700 hover:bg-gray-200"
          }`}
        >
          <BookOpen className="w-4 h-4" /> Standard & Adaptive
        </button>

        <button
          onClick={() => setActiveSubMode('exam')}
          className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium text-xs sm:text-sm whitespace-nowrap transition-all ${
            activeSubMode === 'exam'
              ? "bg-blue-600 text-white shadow-md"
              : "bg-gray-100 text-gray-700 hover:bg-gray-200"
          }`}
        >
          <Clock className="w-4 h-4" /> Timed Exam Simulation
        </button>

        <button
          onClick={() => setActiveSubMode('mistakes')}
          className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium text-xs sm:text-sm whitespace-nowrap transition-all ${
            activeSubMode === 'mistakes'
              ? "bg-blue-600 text-white shadow-md"
              : "bg-gray-100 text-gray-700 hover:bg-gray-200"
          }`}
        >
          <Bookmark className="w-4 h-4" /> Mistake Notebook & Saved
        </button>

        <button
          onClick={() => setActiveSubMode('cram')}
          className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium text-xs sm:text-sm whitespace-nowrap transition-all ${
            activeSubMode === 'cram'
              ? "bg-blue-600 text-white shadow-md"
              : "bg-gray-100 text-gray-700 hover:bg-gray-200"
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
                          <span className="text-xs font-bold px-2 py-1 rounded bg-gray-100 text-gray-800 border border-gray-200">
                            Q{idx + 1}
                          </span>
                          <span className="text-xs font-semibold px-2 py-1 rounded bg-blue-100 text-blue-800">
                            {q.marks || 2} Marks
                          </span>
                          {q.metadata?.topic && q.metadata.topic !== 'unassigned' && (
                            <span className="text-xs font-medium px-2 py-1 rounded bg-gray-100 text-gray-700">
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

      {/* ── MODE 2: Timed Exam Simulation ────────────────────────────────────── */}
      {activeSubMode === 'exam' && (
        <div className="space-y-6">
          {!examActive && !examFinished ? (
            <div className="max-w-xl mx-auto text-center py-8 space-y-6">
              <div className="w-16 h-16 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center mx-auto">
                <Clock className="w-8 h-8" />
              </div>
              <div>
                <h4 className="text-xl font-bold text-gray-900">Timed Exam Simulation</h4>
                <p className="text-sm text-gray-500 mt-1">Simulate real university exam conditions with restricted 2, 3, and 5 mark questions.</p>
              </div>

              <div className="flex justify-center gap-3">
                {[15, 30, 60].map(mins => (
                  <button
                    key={mins}
                    onClick={() => setExamDuration(mins)}
                    className={`px-4 py-2 rounded-lg font-semibold text-sm border ${
                      examDuration === mins
                        ? "bg-blue-600 text-white border-blue-600"
                        : "bg-white text-gray-700 border-gray-300 hover:bg-gray-50"
                    }`}
                  >
                    {mins} Minutes
                  </button>
                ))}
              </div>

              <button
                onClick={startExamSession}
                className="w-full py-3 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-xl shadow-md transition-all"
              >
                Start Exam Session Now
              </button>
            </div>
          ) : (
            <div>
              <div className="flex items-center justify-between bg-gray-900 text-white px-5 py-3 rounded-xl mb-6 shadow">
                <span className="font-semibold text-sm">Exam in Progress</span>
                <span className="text-lg font-mono font-bold text-amber-400">{formatTime(examTimeLeft)}</span>
                <button
                  onClick={() => { setExamFinished(true); setExamActive(false); }}
                  className="text-xs bg-red-600 hover:bg-red-700 px-3 py-1.5 rounded font-semibold"
                >
                  Submit Exam
                </button>
              </div>

              <div className="space-y-6">
                {examQuestions.map((q, idx) => (
                  <div key={q.question_id || idx} className="p-5 border border-gray-200 rounded-xl bg-white">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-xs font-bold text-blue-600 uppercase">Question {idx + 1}</span>
                      <span className="text-xs font-semibold bg-gray-100 px-2 py-0.5 rounded">{q.marks || 2} Marks</span>
                    </div>
                    <p className="text-sm font-medium text-gray-900 mb-4">{q.question_text || q.question}</p>
                    <textarea
                      placeholder="Type your structured solution here..."
                      rows={3}
                      value={examAnswers[q.question_id] || ''}
                      onChange={(e) => setExamAnswers({ ...examAnswers, [q.question_id]: e.target.value })}
                      className="w-full text-sm p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none"
                    />
                  </div>
                ))}
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
