import React, { useState, useEffect } from 'react';
import { cn, formatTextSpacing, preprocessMarkdownContent } from '../lib/utils';
import { useAppStore } from '../store/appStore';
import { ChevronDown, ChevronUp } from 'lucide-react';
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

const ComingSoon = () => (
  <div className="bg-white rounded-2xl p-8 border border-border-subtle shadow-sm flex flex-col min-h-[400px] items-center justify-center text-center">
    <div className="w-16 h-16 bg-blue-50 text-blue-500 rounded-full flex items-center justify-center mb-4">
      <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
      </svg>
    </div>
    <h3 className="text-xl font-bold text-primary mb-2">Practice Material Coming Soon</h3>
    <p className="text-text-secondary max-w-md">
      We're still generating the question bank and detailed solutions for this subject. Check back later!
    </p>
  </div>
);

export default function Practice() {
  const { activeSubjectName } = useAppStore();
  const searchParams = new URLSearchParams(window.location.search);
  const subjectId = searchParams.get('subject');

  const [available, setAvailable] = useState(null);
  const [units, setUnits] = useState([]);
  const [selectedUnit, setSelectedUnit] = useState(null);
  
  const [questions, setQuestions] = useState([]);
  const [loadingQuestions, setLoadingQuestions] = useState(false);
  
  const [solutions, setSolutions] = useState({});
  const [loadingSolutions, setLoadingSolutions] = useState({});
  const [expandedQuestions, setExpandedQuestions] = useState({});

  useEffect(() => {
    if (!subjectId) return;
    
    // Fetch available units
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
    setQuestions([]); // Clear stale questions immediately
    setSolutions({}); // Clear solutions state
    setExpandedQuestions({});
    
    fetch(`${getApiBaseUrl()}/api/subjects/${subjectId}/practice/${selectedUnit}`)
      .then(res => {
        if (!res.ok) throw new Error("Failed");
        return res.json();
      })
      .then(data => {
        setQuestions(data.questions);
        setLoadingQuestions(false);
      })
      .catch(err => {
        console.error("Failed to load questions", err);
        setLoadingQuestions(false);
      });
  }, [subjectId, selectedUnit]);

  const toggleSolution = (questionId) => {
    const isExpanded = expandedQuestions[questionId];
    
    // Toggle expand state
    setExpandedQuestions(prev => ({ ...prev, [questionId]: !isExpanded }));
    
    // Fetch if not already loaded and we're expanding it
    if (!isExpanded && !solutions[questionId] && !loadingSolutions[questionId]) {
      setLoadingSolutions(prev => ({ ...prev, [questionId]: true }));
      
      fetch(`${getApiBaseUrl()}/api/subjects/${subjectId}/practice/${selectedUnit}/${questionId}/solution`)
        .then(async res => {
          if (!res.ok) {
            if (res.status === 404) throw new Error("404");
            throw new Error("Failed");
          }
          const data = await res.json();
          setSolutions(prev => ({ ...prev, [questionId]: data.solution_text }));
          setLoadingSolutions(prev => ({ ...prev, [questionId]: false }));
        })
        .catch(err => {
          console.error("Failed to load solution", err);
          let errorMsg = "Solution could not be loaded.";
          if (err.message === "404") {
             errorMsg = "Solution missing for this question.";
          }
          setSolutions(prev => ({ ...prev, [questionId]: errorMsg }));
          setLoadingSolutions(prev => ({ ...prev, [questionId]: false }));
        });
    }
  };

  if (available === null) {
    return <div className="p-8 text-center text-text-secondary">Loading practice materials...</div>;
  }

  if (available === false) {
    return <ComingSoon />;
  }

  return (
    <div className="bg-white rounded-2xl p-6 sm:p-8 border border-border-subtle shadow-sm flex flex-col min-h-[400px]">
      <div className="mb-6">
        <h3 className="text-2xl font-bold text-primary mb-2">Manual Practice</h3>
        <p className="text-text-secondary">Master <span className="font-semibold text-primary">{activeSubjectName}</span> unit by unit.</p>
      </div>
      
      {/* Unit Selector */}
      <div className="flex overflow-x-auto hide-scrollbar gap-2 mb-8 pb-2">
        {units.map((u) => (
          <button
            key={u.unit_id}
            onClick={() => setSelectedUnit(u.unit_id)}
            className={`px-4 py-2 rounded-full font-medium text-sm whitespace-nowrap transition-colors ${
              selectedUnit === u.unit_id 
                ? "bg-blue-600 text-white shadow-md" 
                : "bg-blue-50 text-blue-700 hover:bg-blue-100 border border-blue-200"
            }`}
          >
            {u.unit_id} <span className="ml-1 opacity-75 text-xs">({u.count})</span>
          </button>
        ))}
      </div>
      
      {/* Question List */}
      <div className="flex-1 space-y-4">
        {loadingQuestions ? (
          <div className="text-center p-8 text-text-secondary">Loading questions...</div>
        ) : (
          questions.map((q) => {
            const isExpanded = expandedQuestions[q.question_id];
            
            return (
              <div key={q.question_id} className="border border-border-subtle rounded-xl overflow-hidden bg-gray-50/50">
                <div className="p-4 sm:p-6">
                  {/* Metadata Badges */}
                  <div className="flex flex-wrap gap-2 mb-3">
                    <span className="text-xs font-semibold px-2 py-1 rounded bg-gray-200 text-gray-700">
                      Q {q.question_id}
                    </span>
                    {q.metadata.topic !== 'unassigned' && (
                      <span className="text-xs font-medium px-2 py-1 rounded bg-blue-100 text-blue-700">
                        {q.metadata.topic}
                      </span>
                    )}
                    {q.metadata.difficulty !== 'unassigned' && (
                      <span className={`text-xs font-medium px-2 py-1 rounded ${
                        q.metadata.difficulty.toLowerCase() === 'basic' ? 'bg-green-100 text-green-700' :
                        q.metadata.difficulty.toLowerCase() === 'intermediate' ? 'bg-yellow-100 text-yellow-700' :
                        'bg-red-100 text-red-700'
                      }`}>
                        {q.metadata.difficulty}
                      </span>
                    )}
                    {q.metadata.type !== 'unassigned' && (
                      <span className="text-xs font-medium px-2 py-1 rounded bg-purple-100 text-purple-700">
                        {q.metadata.type}
                      </span>
                    )}
                  </div>
                  
                  {/* Question Text */}
                  <div className="prose prose-sm max-w-none text-text-primary mb-4">
                    <div className="prose-p:my-2 prose-p:first:mt-0 prose-p:last:mb-0">
                      <ReactMarkdown 
                        remarkPlugins={[remarkMath, remarkBreaks]} 
                        rehypePlugins={[rehypeKatex, rehypeRaw]}
                        components={MarkdownComponents}
                      >
                        {formatTextSpacing(q.question_text)}
                      </ReactMarkdown>
                    </div>
                  </div>
                  
                  {/* Show Solution Toggle */}
                  <button 
                    onClick={() => toggleSolution(q.question_id)}
                    className="flex items-center text-sm font-semibold text-blue-600 hover:text-blue-800 transition-colors"
                  >
                    {isExpanded ? (
                      <><ChevronUp className="w-4 h-4 mr-1" /> Hide Solution</>
                    ) : (
                      <><ChevronDown className="w-4 h-4 mr-1" /> Show Solution</>
                    )}
                  </button>
                </div>
                
                {/* Lazy-loaded Solution Content */}
                {isExpanded && (
                  <div className="border-t border-border-subtle bg-white p-4 sm:p-6">
                    {loadingSolutions[q.question_id] ? (
                      <div className="text-sm text-text-secondary italic">Loading solution...</div>
                    ) : (
                      <div className="prose prose-sm max-w-none text-text-primary">
                        <div className="prose-p:my-2 prose-p:first:mt-0 prose-p:last:mb-0">
                          <ReactMarkdown 
                            remarkPlugins={[remarkMath, remarkBreaks]} 
                            rehypePlugins={[rehypeKatex, rehypeRaw]}
                            components={MarkdownComponents}
                          >
                            {preprocessMarkdownContent(formatTextSpacing(solutions[q.question_id])) || "Solution not available."}
                          </ReactMarkdown>
                        </div>
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
  );
}
