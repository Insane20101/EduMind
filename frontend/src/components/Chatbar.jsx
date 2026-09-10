import React, { useState, useEffect, useRef } from 'react';
import { Mic, Send, Minimize2, Maximize2, X, Sparkles, Paperclip, Trash2, ChevronRight, FileText, Bot } from 'lucide-react';
import { useAppStore } from '../store/appStore';
import { cn, formatTextSpacing, preprocessMarkdownContent } from '../lib/utils';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import remarkMath from 'remark-math';
import remarkBreaks from 'remark-breaks';
import rehypeKatex from 'rehype-katex';
import rehypeRaw from 'rehype-raw';
import Mermaid from './Mermaid';
import { getApiBaseUrl } from '../config';

const MarkdownComponents = {
  p: ({node, ...props}) => {
    let textContent = '';
    React.Children.forEach(props.children, child => {
      if (typeof child === 'string') textContent += child;
    });
    const match = textContent.match(/^(Q\.?\s*\d+|Question\s*\d+|Q\d+)[.:—\-]?\s*(.*)/i);
    if (match) {
      return (
        <div className="mt-6 mb-3.5 pt-3 border-t border-slate-200/80 flex items-start gap-2.5">
          <span className="text-xs font-extrabold px-2.5 py-1 rounded-lg bg-blue-600 text-white shadow-2xs uppercase tracking-wide shrink-0 mt-0.5">
            {match[1]}
          </span>
          {match[2] && <span className="text-base sm:text-lg font-extrabold text-slate-900 leading-snug">{match[2]}</span>}
        </div>
      );
    }
    return <p className="my-3.5 text-sm text-slate-800 leading-relaxed font-normal" {...props} />;
  },
  ul: ({node, ...props}) => (
    <ul className="list-disc pl-5 my-3 space-y-2 text-sm text-slate-800 leading-relaxed" {...props} />
  ),
  ol: ({node, ...props}) => (
    <ol className="list-decimal pl-5 my-3 space-y-2 text-sm text-slate-800 leading-relaxed font-medium" {...props} />
  ),
  li: ({node, ...props}) => (
    <li className="my-1.5 text-sm text-slate-800 leading-relaxed" {...props} />
  ),
  strong: ({node, ...props}) => (
    <strong className="font-extrabold text-slate-900" {...props} />
  ),
  table: ({node, ...props}) => (
    <div className="overflow-x-auto my-4 rounded-xl border border-slate-200 shadow-2xs">
      <table className="min-w-full divide-y divide-slate-200 text-xs text-left" {...props} />
    </div>
  ),
  thead: ({node, ...props}) => (
    <thead className="bg-slate-100 font-semibold text-slate-800 uppercase tracking-wider" {...props} />
  ),
  th: ({node, ...props}) => (
    <th className="px-3.5 py-2.5 font-bold border-b border-slate-200 text-slate-900" {...props} />
  ),
  td: ({node, ...props}) => (
    <td className="px-3.5 py-2 border-b border-slate-100 text-slate-700 font-medium" {...props} />
  ),
  tr: ({node, ...props}) => (
    <tr className="hover:bg-blue-50/40 transition-colors" {...props} />
  ),
  h1: ({node, ...props}) => <h1 className="text-xl font-bold mt-5 mb-2.5 text-slate-900 border-b pb-1.5" {...props} />,
  h2: ({node, ...props}) => <h2 className="text-lg font-bold mt-5 mb-2.5 text-slate-900" {...props} />,
  h3: ({node, ...props}) => {
    let textContent = '';
    React.Children.forEach(props.children, child => {
      if (typeof child === 'string') textContent += child;
    });

    const qMatch = textContent.match(/^(Q\.?\s*\d+|Question\s*\d+|Q\d+)[.:—\-]?\s*(.*)/i);
    if (qMatch) {
      return (
        <div className="mt-6 mb-3.5 pt-3 border-t border-slate-200/80 flex items-start gap-2.5">
          <span className="text-xs font-extrabold px-2.5 py-1 rounded-lg bg-blue-600 text-white shadow-2xs uppercase tracking-wide shrink-0 mt-0.5">
            {qMatch[1]}
          </span>
          {qMatch[2] && <span className="text-base sm:text-lg font-extrabold text-slate-900 leading-snug">{qMatch[2]}</span>}
        </div>
      );
    }

    const stepMatch = textContent.match(/^(Step\s*\d+)\s*(?:—|-)?\s*(.*)/i);
    if (stepMatch) {
      return (
        <div className="mt-5 mb-2.5 flex items-center">
          <span className="text-xs font-bold px-2.5 py-1 rounded-lg bg-blue-100 text-blue-800 mr-2.5 border border-blue-200 uppercase tracking-wider">
            {stepMatch[1]}
          </span>
          {stepMatch[2] && <span className="text-sm font-bold text-slate-900 leading-none">{stepMatch[2]}</span>}
        </div>
      );
    }
    return <h3 className="text-base font-bold mt-4 mb-2 text-slate-900" {...props} />;
  },
  code({node, inline, className, children, ...props}) {
    const match = /language-(\w+)/.exec(className || '');
    if (!inline && match && match[1] === 'mermaid') {
      return <Mermaid chart={String(children).replace(/\n$/, '')} />;
    }
    return <code className={className} {...props}>{children}</code>;
  }
};

export default function Chatbar() {
  const { 
    chatContext, 
    subject, 
    isChatDrawerOpen, 
    toggleChatDrawer, 
    setChatDrawerOpen,
    tempFile,
    setTempFile,
    clearTempFile,
    pendingPrompt,
    clearPendingPrompt
  } = useAppStore();

  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isFullScreen, setIsFullScreen] = useState(false);
  
  const messagesEndRef = useRef(null);
  const fileInputRef = useRef(null);
  const chatContainerRef = useRef(null);

  const autoScrollToBottom = (force = false) => {
    const container = chatContainerRef.current;
    if (!container) return;
    const isNearBottom = container.scrollHeight - container.scrollTop - container.clientHeight < 120;
    if (force || isNearBottom) {
      container.scrollTop = container.scrollHeight;
    }
  };

  useEffect(() => {
    if (isChatDrawerOpen) {
      autoScrollToBottom(true);
    }
  }, [isChatDrawerOpen]);
  
  const isLocked = !subject && chatContext !== 'All Subjects';

  const handleFileChange = (e) => {
    const file = e.target.files?.[0];
    if (file) {
      setTempFile(file);
      // Auto-open drawer if file attached
      setChatDrawerOpen(true);
    }
  };

  const handleClearHistory = () => {
    setMessages([]);
  };

  const executeSend = async (overridePrompt) => {
    const textToSend = typeof overridePrompt === 'string' ? overridePrompt : input;
    const trimmedInput = textToSend.trim();
    if ((!trimmedInput && !tempFile) || isLocked) return;
    
    const userContent = trimmedInput || (tempFile ? `Analyze attached document: ${tempFile.name}` : '');
    const attachedFileName = tempFile ? tempFile.name : null;
    
    const userMessage = { 
      role: 'user', 
      content: userContent,
      attachedFile: attachedFileName
    };

    setMessages(prev => [...prev, userMessage]);
    setChatDrawerOpen(true);
    
    const currentInput = trimmedInput;
    const currentTempFile = tempFile;
    
    setInput('');
    clearTempFile();
    if (fileInputRef.current) fileInputRef.current.value = '';
    
    setIsLoading(true);
    
    try {
      const history = messages.map(m => ({ role: m.role, content: m.content }));
      const apiBaseUrl = getApiBaseUrl();
      
      if (currentTempFile) {
        // Temp Document Endpoint with Google AI OCR
        const formData = new FormData();
        formData.append('file', currentTempFile);
        formData.append('message', currentInput || 'Explain and summarize this document in detail.');
        formData.append('subject_id', subject || 'global');

        const res = await fetch(`${apiBaseUrl}/api/chat/temp-document`, {
          method: 'POST',
          body: formData
        });
        const data = await res.json();
        if (res.ok) {
          setMessages(prev => [...prev, {
            role: 'ai',
            content: data.answer || data.response || "Analysis complete.",
            grounded: data.grounded,
            sources: data.sources,
            ocrProcessed: true,
            isStreaming: false
          }]);
          autoScrollToBottom(true);
        } else {
          console.error("Error from chat API:", data);
          setMessages(prev => [...prev, { role: 'ai', content: data.detail || "Sorry, I encountered an error.", isStreaming: false }]);
          autoScrollToBottom(true);
        }
      } else {
        // Streaming RAG Chat Endpoint with fallback
        let streamSuccess = false;
        try {
          const res = await fetch(`${apiBaseUrl}/api/chat/stream`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              subject_id: subject || "global",
              unit_id: null,
              message: currentInput,
              conversation_history: history
            })
          });

          if (res.ok && res.body) {
            streamSuccess = true;
            const reader = res.body.getReader();
            const decoder = new TextDecoder('utf-8');
            let networkContent = '';
            let displayedContent = '';
            let grounded = false;
            let sources = [];
            let buffer = '';
            let isDone = false;

            // Add initial empty AI message container with isStreaming: true
            setMessages(prev => [...prev, {
              role: 'ai',
              content: '',
              grounded: false,
              sources: [],
              ocrProcessed: false,
              isStreaming: true
            }]);

            // Micro-ticker dispenser interval (~22ms tick = 45fps) for relaxed line-by-line streaming
            const ticker = setInterval(() => {
              if (displayedContent.length < networkContent.length) {
                const diff = networkContent.length - displayedContent.length;
                const step = Math.max(2, Math.min(Math.ceil(diff / 3), 12));
                displayedContent = networkContent.slice(0, displayedContent.length + step);

                setMessages(prev => {
                  const next = [...prev];
                  const lastIdx = next.length - 1;
                  if (lastIdx >= 0 && next[lastIdx].role === 'ai') {
                    next[lastIdx] = {
                      ...next[lastIdx],
                      content: displayedContent,
                      grounded,
                      sources,
                      isStreaming: true
                    };
                  }
                  return next;
                });
                autoScrollToBottom(false);
              } else if (isDone) {
                clearInterval(ticker);
                setMessages(prev => {
                  const next = [...prev];
                  const lastIdx = next.length - 1;
                  if (lastIdx >= 0 && next[lastIdx].role === 'ai') {
                    next[lastIdx] = {
                      ...next[lastIdx],
                      content: networkContent,
                      grounded,
                      sources,
                      isStreaming: false
                    };
                  }
                  return next;
                });
                autoScrollToBottom(true);
              }
            }, 22);

            try {
              while (true) {
                const { done, value } = await reader.read();
                if (done) {
                  isDone = true;
                  break;
                }
                buffer += decoder.decode(value, { stream: true });

                const parts = buffer.split('\n\n');
                buffer = parts.pop() || '';

                for (const part of parts) {
                  const trimmed = part.trim();
                  if (!trimmed.startsWith('data: ')) continue;
                  const dataStr = trimmed.slice(6);
                  if (dataStr === '[DONE]') {
                    isDone = true;
                    break;
                  }

                  try {
                    const parsed = JSON.parse(dataStr);
                    if (parsed.type === 'metadata') {
                      grounded = parsed.grounded;
                      sources = parsed.sources || [];
                    } else if (parsed.type === 'chunk' && parsed.text) {
                      networkContent += parsed.text;
                    }
                  } catch (e) {
                    console.error("Error parsing stream chunk:", e);
                  }
                }
              }
            } catch (err) {
              console.error("Stream reader error:", err);
            } finally {
              isDone = true;
            }
          }
        } catch (e) {
          console.warn("Streaming fetch failed, trying standard endpoint...", e);
        }

        // Fallback to standard non-streaming chat endpoint if stream failed
        if (!streamSuccess) {
          const res = await fetch(`${apiBaseUrl}/api/chat/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              subject_id: subject || "global",
              unit_id: null,
              message: currentInput,
              conversation_history: history
            })
          });
          const data = await res.json();
          if (res.ok) {
            setMessages(prev => [...prev, {
              role: 'ai',
              content: data.answer || data.response || "Analysis complete.",
              grounded: data.grounded,
              sources: data.sources,
              ocrProcessed: false
            }]);
          } else {
            console.error("Error from chat API:", data);
            setMessages(prev => [...prev, { role: 'ai', content: data.detail || "Sorry, I encountered an error." }]);
          }
        }
      }
    } catch (err) {
      console.error("Failed to send message:", err);
      setMessages(prev => [...prev, { role: 'ai', content: "Network error. Please try again." }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSend = (e) => {
    e.preventDefault();
    executeSend();
  };

  useEffect(() => {
    if (pendingPrompt) {
      const promptToRun = pendingPrompt;
      clearPendingPrompt();
      executeSend(promptToRun);
    }
  }, [pendingPrompt]);

  return (
    <>
      {/* ── Floating Toggle Button (Right Side) ────────────────────────────── */}
      <button 
        onClick={toggleChatDrawer}
        className={cn(
          "fixed bottom-6 right-6 z-40 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-medium px-4 py-3 rounded-full shadow-2xl flex items-center gap-2.5 transition-all duration-300 transform hover:scale-105 active:scale-95 border border-white/20",
          isChatDrawerOpen && "opacity-0 pointer-events-none scale-90"
        )}
        title="Open EduMind AI Chat"
      >
        <div className="relative flex items-center justify-center">
          <Sparkles size={20} className="text-yellow-300 animate-pulse" />
        </div>
        <span className="text-sm font-semibold tracking-wide">Ask EduMind AI</span>
        {messages.length > 0 && (
          <span className="w-2.5 h-2.5 bg-emerald-400 rounded-full animate-ping" />
        )}
      </button>

      {/* ── Backdrop for Mobile ────────────────────────────────────────────── */}
      {isChatDrawerOpen && (
        <div 
          className="fixed inset-0 bg-slate-900/30 backdrop-blur-xs z-40 sm:hidden transition-opacity"
          onClick={() => setChatDrawerOpen(false)}
        />
      )}

      {/* ── Right-Side Chat Drawer Panel ─────────────────────────────────── */}
      <div 
        className={cn(
          "fixed top-0 right-0 bottom-0 z-50 bg-white border-l border-border-subtle shadow-2xl flex flex-col transition-transform duration-300 ease-in-out",
          isFullScreen ? "w-full" : "w-full sm:w-[440px] md:w-[480px]",
          isChatDrawerOpen ? "translate-x-0" : "translate-x-full"
        )}
      >
        {/* Drawer Header */}
        <div className="flex items-center justify-between px-5 py-3.5 border-b border-border-subtle bg-slate-50/90 backdrop-blur-md">
          <div className="flex items-center gap-3">
            <div className="h-9 w-9 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-600 flex items-center justify-center text-white shadow-md">
              <Bot size={20} />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="font-bold text-slate-800 text-base leading-tight">EduMind AI</h3>
                <span className="text-[10px] font-semibold uppercase px-2 py-0.5 rounded-full bg-blue-100 text-blue-700 border border-blue-200">
                  Assistant
                </span>
              </div>
              <p className="text-xs text-text-secondary font-medium truncate max-w-[200px]">
                Context: <span className="text-primary font-semibold">{chatContext}</span>
              </p>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex items-center gap-1.5">
            {messages.length > 0 && (
              <button 
                type="button"
                onClick={handleClearHistory} 
                className="p-2 text-text-secondary hover:text-rose-600 hover:bg-rose-50 rounded-lg transition-colors"
                title="Clear Chat History"
              >
                <Trash2 size={16} />
              </button>
            )}
            <button 
              type="button"
              onClick={() => setIsFullScreen(!isFullScreen)} 
              className="p-2 text-text-secondary hover:text-primary hover:bg-slate-100 rounded-lg transition-colors hidden sm:block"
              title={isFullScreen ? "Exit Fullscreen" : "Fullscreen"}
            >
              {isFullScreen ? <Minimize2 size={16} /> : <Maximize2 size={16} />}
            </button>
            <button 
              type="button"
              onClick={() => setChatDrawerOpen(false)} 
              className="p-2 text-text-secondary hover:text-slate-800 hover:bg-slate-100 rounded-lg transition-colors"
              title="Close Drawer"
            >
              <ChevronRight size={20} />
            </button>
          </div>
        </div>

        {/* Drawer Body - Messages */}
        <div ref={chatContainerRef} className="flex-1 overflow-y-auto p-4 custom-scrollbar flex flex-col gap-4 bg-slate-50/40">
          {messages.length === 0 ? (
            <div className="flex-1 flex flex-col items-center justify-center text-center p-6 my-auto">
              <div className="h-14 w-14 rounded-2xl bg-blue-50 text-blue-600 flex items-center justify-center mb-3 shadow-inner">
                <Sparkles size={28} />
              </div>
              <h4 className="font-bold text-slate-800 text-lg mb-1">How can I help you today?</h4>
              <p className="text-xs text-text-secondary max-w-xs leading-relaxed mb-4">
                Ask questions about your subjects, practice topics, or attach a document for instant AI extraction & Q&A.
              </p>
              <div className="w-full flex flex-col gap-2 max-w-xs">
                <button 
                  onClick={() => setInput("Explain the key concepts for this subject.")}
                  className="text-xs text-left p-2.5 rounded-xl bg-white border border-border-subtle hover:border-primary/40 hover:bg-blue-50/50 text-slate-700 font-medium transition-all shadow-2xs"
                >
                  💡 "Explain key concepts for this subject"
                </button>
                <button 
                  onClick={() => setInput("Summarize the main formulas and definitions.")}
                  className="text-xs text-left p-2.5 rounded-xl bg-white border border-border-subtle hover:border-primary/40 hover:bg-blue-50/50 text-slate-700 font-medium transition-all shadow-2xs"
                >
                  📑 "Summarize formulas & definitions"
                </button>
              </div>
            </div>
          ) : (
            messages.map((msg, idx) => (
              <div 
                key={idx} 
                className={cn(
                  "flex flex-col max-w-[88%]", 
                  msg.role === 'user' ? "self-end items-end" : "self-start items-start"
                )}
              >
                {msg.role === 'ai' && (
                  <div className="mb-1 flex items-center gap-1.5 flex-wrap">
                    <span className="text-[11px] font-semibold text-text-secondary">EduMind AI</span>
                    {msg.grounded === true && (
                      <span className="bg-emerald-100 text-emerald-800 text-[10px] px-2 py-0.5 rounded-full font-medium border border-emerald-200">
                        From Course Materials
                      </span>
                    )}
                    {msg.grounded === false && (
                      <span className="bg-amber-100 text-amber-800 text-[10px] px-2 py-0.5 rounded-full font-medium border border-amber-200">
                        General Knowledge
                      </span>
                    )}
                    {msg.ocrProcessed && (
                      <span className="bg-blue-100 text-blue-800 text-[10px] px-2 py-0.5 rounded-full font-medium border border-blue-200 flex items-center gap-1">
                        <Sparkles size={10} /> Google AI OCR
                      </span>
                    )}
                  </div>
                )}

                <div 
                  className={cn(
                    "px-4 py-3 rounded-2xl text-sm leading-relaxed shadow-xs", 
                    msg.role === 'user' 
                      ? "bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-br-none" 
                      : "bg-white text-slate-800 rounded-bl-none border border-slate-200/80 shadow-sm"
                  )}
                >
                  {msg.attachedFile && (
                    <div className="mb-2 p-2 rounded-lg bg-white/20 border border-white/30 text-xs flex items-center gap-2">
                      <FileText size={14} />
                      <span className="font-semibold truncate">{msg.attachedFile}</span>
                    </div>
                  )}

                  <div className={msg.role === 'user' ? "prose-invert prose-p:my-0" : "prose prose-sm max-w-none prose-p:my-1.5 prose-p:first:mt-0 prose-p:last:mb-0"}>
                    <ReactMarkdown 
                      components={MarkdownComponents}
                      remarkPlugins={[remarkGfm, remarkMath, remarkBreaks]} 
                      rehypePlugins={[rehypeKatex, rehypeRaw]}
                    >
                      {preprocessMarkdownContent(formatTextSpacing(msg.content), msg.isStreaming)}
                    </ReactMarkdown>
                  </div>
                </div>

                {msg.role === 'ai' && msg.sources?.length > 0 && (
                  <div className="mt-1.5 flex flex-wrap gap-1">
                    {msg.sources.map((src, i) => (
                      <span key={i} className="text-[10px] bg-slate-200/60 text-slate-600 px-2 py-0.5 rounded-md font-mono">
                        📄 {src.filename || src.title || `Source ${i+1}`}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            ))
          )}

          {isLoading && (
            <div className="self-start flex items-center gap-2 text-xs font-medium text-blue-600 bg-blue-50 border border-blue-200 px-3.5 py-2 rounded-xl animate-pulse">
              <Sparkles size={14} className="animate-spin" />
              <span>EduMind AI is thinking &amp; scanning...</span>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Drawer Footer - Input & Document Attachment */}
        <div className="p-3.5 border-t border-border-subtle bg-white">
          {/* File Attachment Chip */}
          {tempFile && (
            <div className="mb-2.5 px-3 py-1.5 bg-blue-50 border border-blue-200 rounded-xl flex items-center justify-between text-xs text-blue-900 shadow-2xs">
              <div className="flex items-center gap-2 truncate">
                <FileText size={16} className="text-blue-600 shrink-0" />
                <span className="font-semibold truncate">{tempFile.name}</span>
                <span className="text-[10px] bg-blue-200 text-blue-800 px-1.5 py-0.5 rounded font-mono shrink-0">
                  Google AI OCR
                </span>
              </div>
              <button 
                type="button" 
                onClick={clearTempFile}
                className="text-slate-400 hover:text-rose-600 transition-colors p-1"
                title="Remove Attached File"
              >
                <X size={14} />
              </button>
            </div>
          )}

          <form onSubmit={handleSend} className="flex items-center gap-2">
            {/* Hidden File Input */}
            <input 
              type="file" 
              ref={fileInputRef} 
              onChange={handleFileChange}
              accept=".pdf,.png,.jpg,.jpeg,.webp" 
              className="hidden" 
            />

            {/* Paperclip Button */}
            <button
              type="button"
              onClick={() => fileInputRef.current?.click()}
              disabled={isLoading}
              className={cn(
                "p-2.5 rounded-xl text-slate-500 hover:text-blue-600 hover:bg-blue-50 transition-colors border border-slate-200 shrink-0",
                tempFile && "text-blue-600 bg-blue-50 border-blue-300"
              )}
              title="Attach PDF or Image for Google AI OCR Analysis"
            >
              <Paperclip size={18} />
            </button>

            {/* Input Field */}
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              disabled={isLocked || isLoading}
              placeholder={tempFile ? "Ask about attached document..." : "Ask EduMind AI..."}
              className="flex-1 bg-slate-50 border border-slate-200 rounded-xl px-3.5 py-2.5 text-sm text-slate-800 placeholder-slate-400 focus:outline-none focus:border-blue-500 focus:bg-white transition-all"
            />

            {/* Send Button */}
            <button 
              type="submit"
              disabled={isLocked || (!input.trim() && !tempFile) || isLoading}
              className="p-2.5 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white disabled:opacity-40 disabled:bg-slate-300 transition-all shadow-md shrink-0"
            >
              <Send size={18} />
            </button>
          </form>
        </div>
      </div>
    </>
  );
}
