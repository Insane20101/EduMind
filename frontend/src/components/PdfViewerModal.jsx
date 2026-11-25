import React, { useEffect, useState, useRef } from 'react';
import { 
  X, Lock, Eye, AlertCircle, Loader2, ExternalLink, FileText, 
  MessageSquareText, Sparkles, Send, RefreshCw, 
  ChevronRight, ChevronLeft, HelpCircle, Bot, User 
} from 'lucide-react';
import { getApiBaseUrl } from '../config';

export default function PdfViewerModal({ title, pdfUrl, resourceId, resourceType, label, onClose }) {
  const [blobUrl, setBlobUrl] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [useFallback, setUseFallback] = useState(false);
  const [isMobile, setIsMobile] = useState(() => {
    if (typeof window === 'undefined') return false;
    return window.innerWidth < 768 || /Mobi|Android|iPhone|iPad|iPod/i.test(navigator.userAgent);
  });

  // Active side panel: null | 'chat'
  const [activeSection, setActiveSection] = useState(null);

  // ── Chat State ─────────────────────────────────────────────────────────────
  const [chatMessages, setChatMessages] = useState([]);
  const [chatInput, setChatInput] = useState('');
  const [chatLoading, setChatLoading] = useState(false);
  const chatBottomRef = useRef(null);

  useEffect(() => {
    const checkMobile = () => {
      const mobile = window.innerWidth < 768 || /Mobi|Android|iPhone|iPad|iPod/i.test(navigator.userAgent);
      setIsMobile(mobile);
    };
    window.addEventListener('resize', checkMobile);
    return () => window.removeEventListener('resize', checkMobile);
  }, []);

  const handleOpenExternal = (e) => {
    if (e) e.preventDefault();
    if (!pdfUrl) return;
    window.open(pdfUrl, '_blank', 'noopener,noreferrer');
  };

  useEffect(() => {
    if (isMobile && pdfUrl) {
      try {
        window.open(pdfUrl, '_blank', 'noopener,noreferrer');
      } catch (e) {
        console.log('Mobile auto-open notice:', e);
      }
    }
  }, [isMobile, pdfUrl]);

  useEffect(() => {
    const handleKeyDown = (e) => {
      if ((e.ctrlKey || e.metaKey) && (e.key === 's' || e.key === 'S' || e.key === 'p' || e.key === 'P')) {
        e.preventDefault();
      }
    };
    window.addEventListener('keydown', handleKeyDown);

    if (!pdfUrl) return;

    setLoading(true);
    setError(null);
    setUseFallback(false);

    let active = true;
    let createdUrl = null;

    fetch(pdfUrl)
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}: Failed to fetch document.`);
        return res.blob();
      })
      .then((blob) => {
        if (!active) return;
        if (blob.size === 0) throw new Error('Document content is empty.');
        
        const pdfBlob = new Blob([blob], { type: 'application/pdf' });
        createdUrl = URL.createObjectURL(pdfBlob);
        setBlobUrl(`${createdUrl}#toolbar=0&navpanes=0&scrollbar=0`);
        setLoading(false);
      })
      .catch((err) => {
        if (!active) return;
        console.warn('PDF Blob fetch notice, attempting direct stream view:', err);
        setUseFallback(true);
        setLoading(false);
      });

    return () => {
      active = false;
      window.removeEventListener('keydown', handleKeyDown);
      if (createdUrl) {
        URL.revokeObjectURL(createdUrl);
      }
    };
  }, [pdfUrl]);

  // Scroll chat to bottom when messages update
  useEffect(() => {
    if (activeSection === 'chat' && chatBottomRef.current) {
      chatBottomRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [chatMessages, activeSection]);

  // Initial greeting when Chat is opened
  const toggleChat = () => {
    if (activeSection === 'chat') {
      setActiveSection(null);
    } else {
      setActiveSection('chat');
      if (chatMessages.length === 0) {
        setChatMessages([
          {
            role: 'assistant',
            content: `Hello! I'm your AI PDF Assistant for **${title || 'this document'}**. Ask me any question or ask me to explain any concept you don't understand!`
          }
        ]);
      }
    }
  };

  // ── Send Chat Message Handler ──────────────────────────────────────────────
  const handleSendChat = async (msgOverride = null) => {
    const messageToSend = (msgOverride || chatInput).trim();
    if (!messageToSend || chatLoading) return;

    const newHistory = [...chatMessages, { role: 'user', content: messageToSend }];
    setChatMessages(newHistory);
    if (!msgOverride) setChatInput('');
    setChatLoading(true);

    try {
      const res = await fetch(`${getApiBaseUrl()}/api/resources/pdf-chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          pdf_url: pdfUrl,
          resource_id: resourceId,
          message: messageToSend,
          history: newHistory.slice(-6)
        })
      });

      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        throw new Error(errData.detail || 'Failed to get response from AI PDF Tutor.');
      }

      const data = await res.json();
      setChatMessages([...newHistory, { role: 'assistant', content: data.reply }]);
    } catch (err) {
      setChatMessages([
        ...newHistory,
        { role: 'assistant', content: `⚠️ Sorry, I encountered an issue reading the PDF: ${err.message}` }
      ]);
    } finally {
      setChatLoading(false);
    }
  };

  if (!pdfUrl) return null;
  const targetViewerUrl = blobUrl || pdfUrl;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/85 backdrop-blur-md p-1 sm:p-3 select-none">
      <div className="bg-slate-900 border border-slate-700/80 rounded-none sm:rounded-2xl w-full h-full sm:h-[92vh] max-w-7xl flex flex-col shadow-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-200">
        
        {/* ── Top Bar Header ─────────────────────────────────────────────────── */}
        <div className="flex items-center justify-between px-3 sm:px-5 py-2.5 sm:py-3 border-b border-slate-800 bg-slate-950 gap-2 flex-wrap">
          
          {/* Document Title & Badge */}
          <div className="flex items-center gap-2.5 min-w-0">
            <div className="p-1.5 sm:p-2 bg-indigo-500/10 text-indigo-400 rounded-lg flex-shrink-0">
              <Eye size={18} />
            </div>
            <div className="min-w-0">
              <h3 className="text-xs sm:text-sm font-semibold text-slate-100 truncate max-w-[200px] sm:max-w-xs">{title || 'Course Document'}</h3>
              <p className="text-[10px] sm:text-xs text-slate-400 flex items-center gap-1 mt-0.5">
                <Lock size={11} className="text-emerald-400" />
                <span className="truncate">Protected View Mode · EduMind Cloud</span>
              </p>
            </div>
          </div>

          {/* Action Buttons: Chat with PDF & Close */}
          <div className="flex items-center gap-2 flex-wrap">
            {/* 1. Chat with PDF Button */}
            <button
              onClick={toggleChat}
              className={`flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold rounded-lg transition-all shadow-sm ${
                activeSection === 'chat'
                  ? 'bg-indigo-600 text-white border border-indigo-400 ring-2 ring-indigo-500/30'
                  : 'bg-indigo-500/10 hover:bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 hover:border-indigo-400'
              }`}
              title="Open interactive AI chat assistant to ask or explain concepts from this PDF"
            >
              <Sparkles size={14} className="text-amber-400 animate-pulse" />
              <span>Chat with PDF</span>
            </button>

            {/* External Open & Close buttons */}
            <a
              href={pdfUrl}
              target="_blank"
              rel="noopener noreferrer"
              onClick={handleOpenExternal}
              className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold text-white bg-slate-800 hover:bg-slate-700 border border-slate-700 rounded-lg transition-all shadow-sm"
              title="Open document directly in browser tab"
            >
              <ExternalLink size={14} />
              <span className="hidden sm:inline">Open in Tab ↗</span>
            </a>

            <button
              onClick={onClose}
              className="p-1.5 text-slate-400 hover:text-slate-100 hover:bg-slate-800 rounded-lg transition-colors"
              title="Close Viewer"
            >
              <X size={18} />
            </button>
          </div>
        </div>

        {/* ── Main Layout: PDF Viewer + Side Panel (Chat / Quiz) ───────────────── */}
        <div className="flex-1 relative bg-slate-950 flex flex-col md:flex-row overflow-hidden">
          
          {/* PDF Frame */}
          <div className={`flex-1 relative bg-slate-950 flex items-center justify-center overflow-hidden ${activeSection ? 'hidden md:flex md:w-3/5 lg:w-2/3 border-r border-slate-800' : 'w-full h-full'}`}>
            {loading && !isMobile && (
              <div className="flex flex-col items-center gap-3 text-slate-400 p-6 text-center">
                <Loader2 size={32} className="animate-spin text-indigo-500" />
                <p className="text-sm font-medium">Loading document securely from EduMind Cloud...</p>
              </div>
            )}

            {error && !isMobile && (
              <div className="flex flex-col items-center gap-3 text-red-400 max-w-md text-center p-6 bg-slate-900 border border-slate-800 rounded-xl">
                <AlertCircle size={36} />
                <h4 className="text-base font-semibold text-slate-200">Unable to View Document</h4>
                <p className="text-xs text-slate-400 mb-2">{error}</p>
                <button
                  onClick={handleOpenExternal}
                  className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold rounded-lg transition-all flex items-center gap-1.5 cursor-pointer"
                >
                  <ExternalLink size={14} />
                  <span>Open Document Directly</span>
                </button>
              </div>
            )}

            {isMobile ? (
              <div className="flex-1 flex flex-col items-center justify-center p-6 text-center bg-slate-950/90 text-slate-200">
                <div className="w-16 h-16 bg-indigo-500/10 border border-indigo-500/20 rounded-2xl flex items-center justify-center mb-4 text-indigo-400 shadow-inner">
                  <FileText size={36} />
                </div>
                
                <h4 className="text-base font-bold text-slate-100 mb-2 max-w-sm leading-snug">
                  {title || 'Document Preview'}
                </h4>

                <p className="text-xs text-slate-400 mb-5 max-w-xs leading-relaxed">
                  Mobile view mode active. Tap below to open the full document directly in Google Chrome / Browser tab.
                </p>

                <button
                  onClick={handleOpenExternal}
                  className="w-full max-w-xs py-3 px-5 bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-sm rounded-xl shadow-lg flex items-center justify-center gap-2 transition-all border border-indigo-400/40 cursor-pointer"
                >
                  <ExternalLink size={16} />
                  <span>Open Document Directly</span>
                </button>
              </div>
            ) : (
              !loading && !error && (
                <div className="w-full h-full relative">
                  <iframe
                    src={`${targetViewerUrl}#toolbar=0&navpanes=0&scrollbar=0`}
                    title={title || 'PDF Document Viewer'}
                    className="w-full h-full border-0 bg-white"
                    onError={() => setUseFallback(true)}
                  />
                </div>
              )
            )}
          </div>

          {/* ── Side Panel 1: IN-PLACE CHAT WITH PDF ─────────────────────────── */}
          {activeSection === 'chat' && (
            <div className="w-full md:w-2/5 lg:w-1/3 h-full bg-slate-900 flex flex-col border-l border-slate-800 shadow-2xl animate-in slide-in-from-right duration-200">
              
              {/* Chat Drawer Header */}
              <div className="p-3.5 border-b border-slate-800 bg-slate-950 flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div className="p-1.5 bg-indigo-500/10 text-indigo-400 rounded-lg">
                    <Sparkles size={16} />
                  </div>
                  <div>
                    <h4 className="text-xs font-bold text-slate-100">Chat with PDF AI</h4>
                    <p className="text-[10px] text-slate-400">Ask questions or request explanations</p>
                  </div>
                </div>
                <button 
                  onClick={() => setActiveSection(null)} 
                  className="p-1 text-slate-400 hover:text-slate-200 rounded"
                >
                  <X size={16} />
                </button>
              </div>

              {/* Chat Message List */}
              <div className="flex-1 p-3 overflow-y-auto space-y-3 text-xs">
                {chatMessages.map((msg, idx) => (
                  <div
                    key={idx}
                    className={`flex items-start gap-2 ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}
                  >
                    <div className={`p-1.5 rounded-lg flex-shrink-0 text-white ${msg.role === 'user' ? 'bg-indigo-600' : 'bg-slate-800 border border-slate-700 text-indigo-400'}`}>
                      {msg.role === 'user' ? <User size={13} /> : <Bot size={13} />}
                    </div>

                    <div className={`p-3 rounded-xl max-w-[85%] leading-relaxed ${
                      msg.role === 'user' 
                        ? 'bg-indigo-600 text-white font-medium rounded-tr-none shadow-md' 
                        : 'bg-slate-800/90 text-slate-200 border border-slate-700/70 rounded-tl-none shadow-inner whitespace-pre-wrap'
                    }`}>
                      {msg.content}
                    </div>
                  </div>
                ))}
                
                {chatLoading && (
                  <div className="flex items-center gap-2 text-indigo-400 bg-slate-800/50 p-2.5 rounded-xl border border-slate-800 w-fit">
                    <Loader2 size={14} className="animate-spin" />
                    <span className="text-[11px] font-medium">Analyzing PDF content &amp; drafting explanation...</span>
                  </div>
                )}
                <div ref={chatBottomRef} />
              </div>

              {/* Quick Prompt Chips */}
              <div className="px-3 py-2 border-t border-slate-800/80 bg-slate-950 flex items-center gap-1.5 overflow-x-auto text-[11px]">
                <button
                  onClick={() => handleSendChat("Summarize the key concepts of this PDF in 3 bullet points.")}
                  className="px-2.5 py-1 bg-slate-800 hover:bg-slate-700 text-indigo-300 rounded-full border border-slate-700 whitespace-nowrap"
                >
                  💡 Summarize Document
                </button>
                <button
                  onClick={() => handleSendChat("Explain the most complex topic in this document simply.")}
                  className="px-2.5 py-1 bg-slate-800 hover:bg-slate-700 text-indigo-300 rounded-full border border-slate-700 whitespace-nowrap"
                >
                  ❓ Explain Complex Topics
                </button>
              </div>

              {/* Chat Input Bar */}
              <div className="p-3 border-t border-slate-800 bg-slate-950">
                <form
                  onSubmit={(e) => {
                    e.preventDefault();
                    handleSendChat();
                  }}
                  className="flex items-center gap-2"
                >
                  <input
                    type="text"
                    value={chatInput}
                    onChange={(e) => setChatInput(e.target.value)}
                    placeholder="Ask AI about this PDF or ask to explain..."
                    className="flex-1 bg-slate-900 border border-slate-700 focus:border-indigo-400 text-slate-100 placeholder-slate-500 text-xs px-3 py-2 rounded-xl focus:outline-none"
                    disabled={chatLoading}
                  />
                  <button
                    type="submit"
                    disabled={chatLoading || !chatInput.trim()}
                    className="p-2 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-40 text-white rounded-xl transition-all shadow"
                  >
                    <Send size={15} />
                  </button>
                </form>
              </div>
            </div>
          )}

          
        </div>
      </div>
    </div>
  );
}
