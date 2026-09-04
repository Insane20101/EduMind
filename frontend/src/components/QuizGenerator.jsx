import React, { useState, useEffect } from 'react';
import { cn, formatTextSpacing } from '../lib/utils';
import { useAppStore } from '../store/appStore';
import { ChevronDown, ChevronUp, AlertCircle, CheckCircle2, XCircle, ArrowLeft, Loader2 } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import remarkMath from 'remark-math';
import remarkBreaks from 'remark-breaks';
import rehypeKatex from 'rehype-katex';
import rehypeRaw from 'rehype-raw';
import Mermaid from './Mermaid';
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
  },
  code({node, inline, className, children, ...props}) {
    const match = /language-(\w+)/.exec(className || '');
    if (!inline && match && match[1] === 'mermaid') {
      return <Mermaid chart={String(children).replace(/\n$/, '')} />;
    }
    return <code className={className} {...props}>{children}</code>;
  }
};

export default function QuizGenerator({ onBack }) {
  const { subject: storeSubject, activeSubjectName } = useAppStore();
  const searchParams = new URLSearchParams(window.location.search);
  const subjectId = searchParams.get('subject') || storeSubject;

  const [availableUnits, setAvailableUnits] = useState([]);
  const [loadingUnits, setLoadingUnits] = useState(true);

  // Form state
  const [selectedUnits, setSelectedUnits] = useState([]);
  const [difficulty, setDifficulty] = useState('Basic');
  const [count, setCount] = useState(5);

  // Generation state
  const [generating, setGenerating] = useState(false);
  const [errorMsg, setErrorMsg] = useState(null);

  // Quiz state
  const [quizData, setQuizData] = useState(null);
  const [answers, setAnswers] = useState({}); // user's selected answers
  const [submitted, setSubmitted] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [score, setScore] = useState(0);

  const STANDARD_FALLBACK_UNITS = [
    { unit_id: "Unit I", count: 5 },
    { unit_id: "Unit II", count: 5 },
    { unit_id: "Unit III", count: 5 },
    { unit_id: "Unit IV", count: 5 }
  ];

  useEffect(() => {
    if (!subjectId) return;
    
    // Fetch available units from practice endpoint
    fetch(`${getApiBaseUrl()}/api/subjects/${subjectId}/practice`)
      .then(res => res.json())
      .then(data => {
        if (data && data.units && data.units.length > 0) {
          setAvailableUnits(data.units);
          setSelectedUnits([data.units[0].unit_id]);
        } else {
          setAvailableUnits(STANDARD_FALLBACK_UNITS);
          setSelectedUnits(["Unit I"]);
        }
        setLoadingUnits(false);
      })
      .catch(err => {
        console.error("Failed to load units", err);
        setAvailableUnits(STANDARD_FALLBACK_UNITS);
        setSelectedUnits(["Unit I"]);
        setLoadingUnits(false);
      });
  }, [subjectId]);

  const handleUnitToggle = (unitId) => {
    setSelectedUnits(prev => 
      prev.includes(unitId) 
        ? prev.filter(u => u !== unitId) 
        : [...prev, unitId]
    );
  };

  const handleGenerate = async () => {
    if (selectedUnits.length === 0) {
      setErrorMsg("Please select at least one unit.");
      return;
    }
    
    setGenerating(true);
    setErrorMsg(null);
    setQuizData(null);
    setAnswers({});
    setSubmitted(false);
    setIsSubmitting(false);

    try {
      const response = await fetch(`${getApiBaseUrl()}/api/subjects/${subjectId}/quiz/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          unit_ids: selectedUnits,
          difficulty: difficulty,
          count: parseInt(count, 10),
          user_id: "test_user"
        })
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.detail || "Failed to generate quiz.");
      }
      
      setQuizData(data);
    } catch (err) {
      console.error(err);
      setErrorMsg(err.message);
    } finally {
      setGenerating(false);
    }
  };

  const handleAnswerSelect = (questionIndex, optionIndex) => {
    if (submitted) return;
    setAnswers(prev => ({ ...prev, [questionIndex]: optionIndex }));
  };

  const handleSubmitQuiz = async () => {
    if (isSubmitting) return;
    setIsSubmitting(true);
    
    try {
      const response = await fetch(`${getApiBaseUrl()}/api/quiz/${quizData.quiz.quiz_id}/submit`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ answers })
      });
      if (!response.ok) throw new Error("Failed to submit quiz");
      const data = await response.json();
      setScore(data.score);
      setSubmitted(true);
      setIsSubmitting(false);
    } catch (err) {
      console.error("Submission error:", err);
      setErrorMsg("Failed to submit quiz. Please try again.");
      setIsSubmitting(false);
    }
  };

  if (loadingUnits) {
    return <div className="p-8 text-center text-text-secondary">Loading units...</div>;
  }

  // View 1: Show Quiz (if generated)
  if (quizData) {
    const { requested_count, delivered_count, quiz } = quizData;
    const questions = quiz.questions;
    
    return (
      <div className="bg-white rounded-2xl p-6 sm:p-8 border border-border-subtle shadow-sm flex flex-col min-h-[400px]">
        <div className="mb-6 flex items-center justify-between">
          <div>
            <h3 className="text-2xl font-bold text-primary mb-2">Custom Quiz</h3>
            <p className="text-text-secondary">
              {delivered_count} questions • {difficulty}
            </p>
          </div>
          <button 
            onClick={() => { setQuizData(null); setSubmitted(false); setAnswers({}); }}
            className="flex items-center text-sm font-medium text-text-secondary hover:text-primary transition-colors"
          >
            <ArrowLeft size={16} className="mr-1" /> New Quiz
          </button>
        </div>
        
        {delivered_count < requested_count && (
          <div className="mb-6 bg-yellow-50 border border-yellow-200 text-yellow-800 p-4 rounded-xl flex items-start">
            <AlertCircle className="w-5 h-5 mr-3 mt-0.5 flex-shrink-0" />
            <div>
              <p className="font-semibold text-sm">Questions removed during grounding check</p>
              <p className="text-sm mt-1">
                {delivered_count} of {requested_count} questions generated — {requested_count - delivered_count} were removed for not being strictly grounded in your materials.
              </p>
            </div>
          </div>
        )}
        
        {questions.length === 0 ? (
          <div className="text-center p-8 text-text-secondary bg-gray-50 rounded-xl">
            No valid questions could be generated. Please try a different configuration or more units.
          </div>
        ) : (
          <div className="space-y-8 flex-1">
            {questions.map((q, qIdx) => {
              const isCorrect = answers[qIdx] === q.correct_option_index;
              const hasAnswered = answers[qIdx] !== undefined;
              
              return (
                <div key={qIdx} className="border border-border-subtle rounded-xl p-6 bg-gray-50/50">
                  <div className="flex justify-between items-start mb-4">
                    <h4 className="text-lg font-semibold text-text-primary flex items-start gap-2">
                      <span className="mt-0.5">{qIdx + 1}.</span> 
                      <div className="prose prose-sm max-w-none prose-p:my-0">
                        <ReactMarkdown components={MarkdownComponents} remarkPlugins={[remarkMath, remarkBreaks]} rehypePlugins={[rehypeKatex, rehypeRaw]}>{formatTextSpacing(q.question_text)}</ReactMarkdown>
                      </div>
                    </h4>
                    <span className="text-xs font-medium px-2 py-1 rounded bg-blue-100 text-blue-700 ml-4 whitespace-nowrap">
                      {q.unit}
                    </span>
                  </div>
                  
                  <div className="space-y-3">
                    {q.options.map((opt, optIdx) => {
                      let bgColor = "bg-white hover:bg-gray-50";
                      let borderColor = "border-border-subtle";
                      let icon = null;
                      
                      if (submitted) {
                        if (optIdx === q.correct_option_index) {
                          bgColor = "bg-green-50";
                          borderColor = "border-green-300";
                          icon = <CheckCircle2 className="w-5 h-5 text-green-600 ml-auto" />;
                        } else if (answers[qIdx] === optIdx) {
                          bgColor = "bg-red-50";
                          borderColor = "border-red-300";
                          icon = <XCircle className="w-5 h-5 text-red-600 ml-auto" />;
                        } else {
                          bgColor = "bg-gray-50 opacity-60";
                        }
                      } else if (answers[qIdx] === optIdx) {
                        bgColor = "bg-blue-50";
                        borderColor = "border-blue-300";
                      }
                      
                      return (
                        <label 
                          key={optIdx}
                          className={`flex items-center p-4 border rounded-xl cursor-pointer transition-colors ${bgColor} ${borderColor}`}
                        >
                          <input 
                            type="radio" 
                            name={`question-${qIdx}`} 
                            className="w-4 h-4 text-blue-600 border-gray-300 focus:ring-blue-500 mr-4"
                            checked={answers[qIdx] === optIdx}
                            onChange={() => handleAnswerSelect(qIdx, optIdx)}
                            disabled={submitted}
                          />
                          <span className={`text-sm flex-1 ${submitted && optIdx === q.correct_option_index ? 'font-semibold text-green-900' : 'text-text-primary'}`}>
                            <div className="prose prose-sm max-w-none prose-p:my-0 inline-block">
                              <ReactMarkdown components={MarkdownComponents} remarkPlugins={[remarkMath, remarkBreaks]} rehypePlugins={[rehypeKatex, rehypeRaw]}>{opt}</ReactMarkdown>
                            </div>
                          </span>
                          {icon}
                        </label>
                      );
                    })}
                  </div>
                  
                  {submitted && (
                    <div className={`mt-6 p-4 rounded-xl text-sm ${isCorrect ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                      <p className="font-bold mb-1">{isCorrect ? 'Correct!' : 'Incorrect.'}</p>
                      <div className="prose prose-sm max-w-none prose-p:my-1 mt-2 text-inherit">
                        <ReactMarkdown components={MarkdownComponents} remarkPlugins={[remarkMath, remarkBreaks]} rehypePlugins={[rehypeKatex, rehypeRaw]}>{formatTextSpacing(q.explanation)}</ReactMarkdown>
                      </div>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        )}
        
        {questions.length > 0 && !submitted && (
          <div className="mt-8 pt-6 border-t border-border-subtle flex justify-end">
            <button 
              onClick={handleSubmitQuiz}
              disabled={Object.keys(answers).length < questions.length || isSubmitting}
              className="px-6 py-3 bg-primary text-white rounded-xl font-semibold hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
            >
              {isSubmitting ? (
                <><Loader2 className="w-5 h-5 mr-2 animate-spin" /> Submitting...</>
              ) : (
                'Submit Quiz'
              )}
            </button>
          </div>
        )}
        
        {submitted && (
          <div className="mt-8 pt-6 border-t border-border-subtle text-center">
            <h4 className="text-2xl font-bold text-primary mb-2">
              You scored {score} out of {questions.length}
            </h4>
            <p className="text-text-secondary mb-6">
              {score === questions.length ? 'Perfect score! Great job!' : 'Keep practicing to master these units.'}
            </p>
            <button 
              onClick={() => { setQuizData(null); setSubmitted(false); setAnswers({}); }}
              className="px-6 py-3 bg-gray-100 text-gray-800 rounded-xl font-semibold hover:bg-gray-200 transition-colors"
            >
              Generate Another Quiz
            </button>
          </div>
        )}
      </div>
    );
  }

  // View 2: Configuration Form
  return (
    <div className="bg-white rounded-2xl p-6 sm:p-8 border border-border-subtle shadow-sm flex flex-col min-h-[400px]">
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h3 className="text-2xl font-bold text-primary mb-2">Quiz Generator</h3>
          <p className="text-text-secondary">Configure a custom quiz for <span className="font-semibold">{activeSubjectName}</span>.</p>
        </div>
      </div>
      
      {errorMsg && (
        <div className="mb-6 bg-red-50 border border-red-200 text-red-800 p-4 rounded-xl flex items-start">
          <AlertCircle className="w-5 h-5 mr-3 mt-0.5 flex-shrink-0" />
          <p className="text-sm">{errorMsg}</p>
        </div>
      )}
      
      <div className="space-y-8 flex-1">
        {/* Units Selection */}
        <div>
          <label className="block text-sm font-semibold text-text-primary mb-3">Select Units</label>
          {availableUnits.length === 0 ? (
            <p className="text-sm text-text-secondary italic">No units available for this subject.</p>
          ) : (
            <div className="flex flex-wrap gap-2">
              {availableUnits.map((u) => (
                <button
                  key={u.unit_id}
                  onClick={() => handleUnitToggle(u.unit_id)}
                  className={`px-4 py-2 rounded-full font-medium text-sm transition-colors ${
                    selectedUnits.includes(u.unit_id)
                      ? "bg-blue-600 text-white shadow-md border border-blue-600" 
                      : "bg-blue-50 text-blue-700 hover:bg-blue-100 border border-blue-200"
                  }`}
                >
                  {u.unit_id}
                </button>
              ))}
            </div>
          )}
        </div>
        
        {/* Difficulty & Count */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-semibold text-text-primary mb-3">Difficulty</label>
            <div className="flex rounded-xl overflow-hidden border border-border-subtle p-1 bg-gray-50">
              {['Basic', 'Intermediate', 'Advanced'].map(diff => (
                <button
                  key={diff}
                  onClick={() => setDifficulty(diff)}
                  className={`flex-1 py-2 text-sm font-medium rounded-lg transition-colors ${
                    difficulty === diff ? 'bg-white shadow text-primary' : 'text-text-secondary hover:text-primary'
                  }`}
                >
                  {diff}
                </button>
              ))}
            </div>
          </div>
          
          <div>
            <label className="block text-sm font-semibold text-text-primary mb-3">Number of Questions</label>
            <div className="flex items-center">
              <input 
                type="range" 
                min="3" 
                max="20" 
                value={count} 
                onChange={(e) => setCount(e.target.value)}
                className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-blue-600"
              />
              <span className="ml-4 font-bold text-lg text-primary w-8 text-center">{count}</span>
            </div>
          </div>
        </div>
      </div>
      
      <div className="mt-8 pt-6 border-t border-border-subtle flex justify-end">
        <button 
          onClick={handleGenerate}
          disabled={generating || availableUnits.length === 0}
          className="px-6 py-3 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-xl font-semibold hover:shadow-lg transition-all flex items-center disabled:opacity-70 disabled:cursor-not-allowed"
        >
          {generating ? (
            <><Loader2 className="w-5 h-5 mr-2 animate-spin" /> Generating Quiz...</>
          ) : (
            'Generate Quiz'
          )}
        </button>
      </div>
    </div>
  );
}
