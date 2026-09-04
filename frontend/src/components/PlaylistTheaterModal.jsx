import React, { useState, useEffect, useRef } from 'react';
import { 
  X, Play, ArrowLeft, ChevronRight, ListVideo, Layers, Tv, 
  ExternalLink, Loader2, Sparkles, Bot, Send, User, RefreshCw, 
  HelpCircle, BookOpen, CheckCircle2, MessageSquareText, Maximize2, Minimize2, MoveHorizontal
} from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import remarkMath from 'remark-math';
import remarkBreaks from 'remark-breaks';
import rehypeKatex from 'rehype-katex';
import rehypeRaw from 'rehype-raw';
import Mermaid from './Mermaid';
import { preprocessMarkdownContent } from '../lib/utils';
import { getApiBaseUrl } from '../config';
import 'katex/dist/katex.min.css';

const MarkdownComponents = {
  p: ({node, ...props}) => (
    <p className="my-2.5 text-xs text-slate-200 leading-relaxed font-normal" {...props} />
  ),
  ul: ({node, ...props}) => (
    <ul className="list-disc pl-5 my-2.5 space-y-1.5 text-xs text-slate-200 leading-relaxed" {...props} />
  ),
  ol: ({node, ...props}) => (
    <ol className="list-decimal pl-5 my-2.5 space-y-1.5 text-xs text-slate-200 leading-relaxed font-medium" {...props} />
  ),
  li: ({node, ...props}) => (
    <li className="my-1 text-xs text-slate-200 leading-relaxed" {...props} />
  ),
  strong: ({node, ...props}) => (
    <strong className="font-bold text-indigo-200" {...props} />
  ),
  blockquote: ({node, ...props}) => (
    <blockquote className="border-l-2 border-indigo-500/80 pl-3 py-1 my-2.5 bg-slate-950/70 text-slate-300 italic text-xs rounded-r-lg" {...props} />
  ),
  table: ({node, ...props}) => (
    <div className="overflow-x-auto my-3 rounded-xl border border-slate-700/60 bg-slate-950/80 shadow-2xs">
      <table className="min-w-full divide-y divide-slate-700 text-xs text-left" {...props} />
    </div>
  ),
  thead: ({node, ...props}) => (
    <thead className="bg-slate-800/90 font-semibold text-slate-200 uppercase tracking-wider text-[11px]" {...props} />
  ),
  th: ({node, ...props}) => (
    <th className="px-3 py-2 font-bold border-b border-slate-700 text-indigo-300" {...props} />
  ),
  td: ({node, ...props}) => (
    <td className="px-3 py-1.5 border-b border-slate-800 text-slate-300 font-medium" {...props} />
  ),
  tr: ({node, ...props}) => (
    <tr className="hover:bg-slate-800/50 transition-colors" {...props} />
  ),
  h1: ({node, ...props}) => <h1 className="text-sm font-bold mt-4 mb-2 text-slate-100 border-b border-slate-800 pb-1" {...props} />,
  h2: ({node, ...props}) => <h2 className="text-xs font-bold mt-3.5 mb-1.5 text-indigo-200" {...props} />,
  h3: ({node, ...props}) => <h3 className="text-xs font-bold mt-3 mb-1 text-indigo-300 flex items-center gap-1.5" {...props} />,
  h4: ({node, ...props}) => <h4 className="text-[11px] font-bold uppercase tracking-wider mt-2 mb-1 text-indigo-400" {...props} />,
  hr: ({node, ...props}) => <hr className="my-3 border-slate-800/80" {...props} />,
  code({node, inline, className, children, ...props}) {
    const match = /language-(\w+)/.exec(className || '');
    if (!inline && match && match[1] === 'mermaid') {
      return <Mermaid chart={String(children).replace(/\n$/, '')} />;
    }
    return inline ? (
      <code className="bg-slate-800 text-indigo-300 px-1.5 py-0.5 rounded text-[11px] font-mono border border-slate-700/50" {...props}>
        {children}
      </code>
    ) : (
      <pre className="bg-slate-950 p-3 rounded-xl border border-slate-800 text-xs font-mono overflow-x-auto text-indigo-200 my-2.5 leading-relaxed whitespace-pre-wrap">
        <code className={className} {...props}>{children}</code>
      </pre>
    );
  }
};

export default function PlaylistTheaterModal({ playlists = [], initialIndex = 0, onClose }) {
  const [activePlaylistIdx, setActivePlaylistIdx] = useState(initialIndex);
  const [activeVideoIdx, setActiveVideoIdx] = useState(0);
  const [realVideos, setRealVideos] = useState([]);
  const [loadingItems, setLoadingItems] = useState(false);

  // Sidebar Tab State: 'tracklist' | 'ai'
  const [sidebarTab, setSidebarTab] = useState('tracklist');
  
  // Resizable Sidebar Panel Width state (in pixels), Full Screen Chat & Theater Full Screen states
  const [sidebarWidth, setSidebarWidth] = useState(440);
  const [isDragging, setIsDragging] = useState(false);
  const [isChatFullScreen, setIsChatFullScreen] = useState(false);
  const [isModalFullScreen, setIsModalFullScreen] = useState(false);
  const modalContainerRef = useRef(null);

  const toggleModalFullScreen = () => {
    setIsModalFullScreen((prev) => !prev);
    if (!document.fullscreenElement) {
      modalContainerRef.current?.requestFullscreen?.().catch(() => {});
    } else {
      document.exitFullscreen?.().catch(() => {});
    }
  };

  // AI Chat & Summary state
  const [chatMessages, setChatMessages] = useState([]);
  const [inputQuery, setInputQuery] = useState('');
  const [aiLoading, setAiLoading] = useState(false);
  const [summaryLoading, setSummaryLoading] = useState(false);
  const chatEndRef = useRef(null);

  const currentPlaylist = playlists[activePlaylistIdx] || playlists[0] || {};

  // Extract YouTube Playlist ID / Video ID
  const getPlaylistDetails = (url) => {
    let listId = null;
    let videoId = null;
    try {
      if (url && typeof url === 'string') {
        if (url.includes('list=')) {
          listId = new URL(url).searchParams.get('list');
        } else if (url.includes('watch?v=')) {
          videoId = new URL(url).searchParams.get('v');
        }
      }
    } catch (e) {}
    return { listId, videoId };
  };

  const { listId, videoId } = getPlaylistDetails(currentPlaylist.url);

  // Fetch 100% REAL YouTube video titles via backend RSS endpoint
  useEffect(() => {
    if (!listId) {
      setRealVideos([]);
      setLoadingItems(false);
      return;
    }

    setLoadingItems(true);
    setRealVideos([]);

    fetch(`${getApiBaseUrl()}/api/resources/playlist-items?list_id=${listId}`)
      .then((res) => res.json())
      .then((data) => {
        if (data.videos && Array.isArray(data.videos) && data.videos.length > 0) {
          setRealVideos(data.videos);
        } else {
          setRealVideos([]);
        }
      })
      .catch((err) => {
        console.warn('Playlist items fetch notice:', err);
        setRealVideos([]);
      })
      .finally(() => {
        setLoadingItems(false);
      });
  }, [listId]);

  // Reset active video index when switching playlists
  useEffect(() => {
    setActiveVideoIdx(0);
  }, [activePlaylistIdx]);

  // Auto-scroll chat to bottom
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chatMessages, aiLoading, summaryLoading]);

  // Handle panel resizing via dragging splitter
  const handleMouseDown = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  useEffect(() => {
    const handleMouseMove = (e) => {
      if (!isDragging || !modalContainerRef.current) return;
      const containerRect = modalContainerRef.current.getBoundingClientRect();
      const newWidth = containerRect.right - e.clientX;
      // Clamp sidebar width between 280px and 750px (or max 65% of viewport)
      const maxAllowed = Math.min(750, containerRect.width * 0.65);
      const clampedWidth = Math.max(280, Math.min(newWidth, maxAllowed));
      setSidebarWidth(clampedWidth);
    };

    const handleMouseUp = () => {
      if (isDragging) setIsDragging(false);
    };

    if (isDragging) {
      window.addEventListener('mousemove', handleMouseMove);
      window.addEventListener('mouseup', handleMouseUp);
    }
    return () => {
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('mouseup', handleMouseUp);
    };
  }, [isDragging]);

  if (!playlists || playlists.length === 0) return null;

  const currentVideoObj = realVideos[activeVideoIdx] || null;

  // Generate embed URL using real video ID or YouTube playlist index
  const getEmbedUrl = () => {
    if (currentVideoObj && currentVideoObj.videoId) {
      return `https://www.youtube.com/embed/${currentVideoObj.videoId}?autoplay=1`;
    }
    if (listId) {
      return `https://www.youtube.com/embed/videoseries?list=${listId}&index=${activeVideoIdx}&autoplay=1`;
    }
    if (videoId) {
      return `https://www.youtube.com/embed/${videoId}?autoplay=1`;
    }
    return null;
  };

  const embedUrl = getEmbedUrl();
  const currentVideoTitle = currentVideoObj
    ? currentVideoObj.title
    : (currentPlaylist.title || `Lecture Video #${activeVideoIdx + 1}`);

  const totalVideosCount = realVideos.length > 0 ? realVideos.length : (listId ? 20 : 1);

  // Function to generate instant Video Summary
  const handleGenerateSummary = async () => {
    if (summaryLoading) return;
    setSummaryLoading(true);
    setSidebarTab('ai');

    const promptUserMsg = {
      id: Date.now(),
      role: 'user',
      content: `✨ Generate real-time summary for: "${currentVideoTitle}"`,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setChatMessages((prev) => [...prev, promptUserMsg]);

    try {
      const res = await fetch(`${getApiBaseUrl()}/api/chat/video-summary`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          video_title: currentVideoTitle,
          subject_id: currentPlaylist.subject_id || 'BCS-401',
          unit_name: currentPlaylist.unit || 'Playlist Unit',
          playlist_title: currentPlaylist.title || ''
        })
      });

      const data = await res.json();
      if (data.summary) {
        setChatMessages((prev) => [
          ...prev,
          {
            id: Date.now() + 1,
            role: 'assistant',
            content: data.summary,
            timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            grounded: data.grounded
          }
        ]);
      } else {
        throw new Error('Failed to generate summary');
      }
    } catch (err) {
      setChatMessages((prev) => [
        ...prev,
        {
          id: Date.now() + 1,
          role: 'assistant',
          content: '⚠️ Failed to generate summary due to network or rate limit. Please try again!',
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        }
      ]);
    } finally {
      setSummaryLoading(false);
    }
  };

  // Function to send custom AI question about the video
  const handleSendQuestion = async (queryText = null) => {
    const textToSend = queryText || inputQuery;
    if (!textToSend.trim() || aiLoading) return;

    setInputQuery('');
    setSidebarTab('ai');

    const userMsg = {
      id: Date.now(),
      role: 'user',
      content: textToSend,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setChatMessages((prev) => [...prev, userMsg]);
    setAiLoading(true);

    try {
      const history = chatMessages.map((m) => ({ role: m.role, content: m.content }));
      const response = await fetch(`${getApiBaseUrl()}/api/chat/stream`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          subject_id: currentPlaylist.subject_id || 'BCS-401',
          message: textToSend,
          video_title: currentVideoTitle,
          conversation_history: history
        })
      });

      if (!response.ok) throw new Error('Streaming failed');

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let assistantText = '';

      const assistantMsgId = Date.now() + 1;
      setChatMessages((prev) => [
        ...prev,
        {
          id: assistantMsgId,
          role: 'assistant',
          content: '',
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        }
      ]);

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        const chunkStr = decoder.decode(value);
        const lines = chunkStr.split('\n');

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const rawData = line.replace('data: ', '').trim();
            if (rawData === '[DONE]') break;
            try {
              const parsed = JSON.parse(rawData);
              if (parsed.type === 'chunk' && parsed.text) {
                assistantText += parsed.text;
                setChatMessages((prev) =>
                  prev.map((msg) =>
                    msg.id === assistantMsgId ? { ...msg, content: assistantText } : msg
                  )
                );
              }
            } catch (e) {}
          }
        }
      }
    } catch (err) {
      console.warn('AI question stream error:', err);
      try {
        const res = await fetch(`${getApiBaseUrl()}/api/chat/`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            subject_id: currentPlaylist.subject_id || 'BCS-401',
            message: textToSend,
            video_title: currentVideoTitle,
            conversation_history: []
          })
        });
        const data = await res.json();
        setChatMessages((prev) => [
          ...prev,
          {
            id: Date.now() + 2,
            role: 'assistant',
            content: data.answer || 'Completed request.',
            timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
          }
        ]);
      } catch (fErr) {
        setChatMessages((prev) => [
          ...prev,
          {
            id: Date.now() + 3,
            role: 'assistant',
            content: '⚠️ Unable to connect to AI assistant. Please try again.',
            timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
          }
        ]);
      }
    } finally {
      setAiLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/95 backdrop-blur-md p-2 sm:p-4 text-slate-100 font-sans select-none">
      <div 
        ref={modalContainerRef}
        className={`bg-slate-900 flex flex-col shadow-2xl overflow-hidden transition-all duration-200 ${
          isModalFullScreen 
            ? 'w-screen h-screen fixed inset-0 z-50 rounded-none border-0' 
            : 'rounded-2xl w-full max-w-7xl h-[94vh] border border-slate-800'
        }`}
      >
        
        {/* Top Control Bar */}
        <div className="flex flex-wrap items-center justify-between px-5 py-2.5 border-b border-slate-800 bg-slate-950/90 gap-3">
          <div className="flex items-center gap-3">
            <button
              onClick={onClose}
              className="flex items-center gap-2 px-3 py-1.5 text-xs font-semibold text-slate-300 bg-slate-800/80 hover:bg-slate-700 hover:text-white rounded-lg transition-all border border-slate-700/60"
            >
              <ArrowLeft size={16} />
              <span>Back to Course</span>
            </button>

            <div className="h-5 w-[1px] bg-slate-800 hidden sm:block" />

            <div>
              <div className="flex items-center gap-2">
                <span className="px-2 py-0.5 text-[10px] uppercase font-bold tracking-wider bg-indigo-500/20 text-indigo-400 rounded border border-indigo-500/30">
                  {currentPlaylist.unit || 'Playlist'}
                </span>
                <h3 className="text-sm font-semibold text-slate-100 line-clamp-1">{currentPlaylist.title || 'Video Course'}</h3>
              </div>
            </div>
          </div>

          {/* Width Presets & YouTube External Link */}
          <div className="flex items-center gap-2">
            
            {/* Cineview Panel Width Presets */}
            <div className="hidden sm:flex items-center gap-1 bg-slate-950 p-1 rounded-xl border border-slate-800 text-[11px]">
              <span className="text-slate-400 px-2 flex items-center gap-1 font-medium">
                <MoveHorizontal size={13} className="text-indigo-400" />
                <span>View:</span>
              </span>
              <button
                onClick={() => { setIsChatFullScreen(false); setSidebarWidth(280); }}
                title="Cineview Mode (Max Video Width)"
                className={`px-2.5 py-1 rounded-lg transition-all flex items-center gap-1 ${
                  !isChatFullScreen && sidebarWidth <= 300
                    ? 'bg-indigo-600 text-white font-bold shadow-sm'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'
                }`}
              >
                🎬 <span>Cineview</span>
              </button>

              <button
                onClick={() => { setIsChatFullScreen(false); setSidebarWidth(440); }}
                title="Standard Split View"
                className={`px-2.5 py-1 rounded-lg transition-all flex items-center gap-1 ${
                  !isChatFullScreen && sidebarWidth > 300 && sidebarWidth < 550
                    ? 'bg-indigo-600 text-white font-bold shadow-sm'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'
                }`}
              >
                ⚖️ <span>Standard</span>
              </button>

              <button
                onClick={() => { setIsChatFullScreen(false); setSidebarWidth(620); }}
                title="Focus Study Mode (Wide Chat & Diagrams)"
                className={`px-2.5 py-1 rounded-lg transition-all flex items-center gap-1 ${
                  !isChatFullScreen && sidebarWidth >= 550
                    ? 'bg-indigo-600 text-white font-bold shadow-sm'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'
                }`}
              >
                💬 <span>Wide Study</span>
              </button>

              <button
                onClick={toggleModalFullScreen}
                title="Theater Full Screen (Maximize whole modal to full screen display)"
                className={`px-2.5 py-1 rounded-lg transition-all flex items-center gap-1 ${
                  isModalFullScreen
                    ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-bold shadow-sm ring-1 ring-indigo-400'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'
                }`}
              >
                {isModalFullScreen ? <Minimize2 size={13} /> : <Maximize2 size={13} />}
                <span>{isModalFullScreen ? 'Exit Full Screen' : '🖥️ Full Screen'}</span>
              </button>
            </div>

            {/* External YouTube Link Button */}
            {currentPlaylist.url && (
              <a
                href={currentPlaylist.url}
                target="_blank"
                rel="noopener noreferrer"
                title="Open directly on YouTube"
                className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold text-red-400 bg-red-500/10 hover:bg-red-500/20 border border-red-500/30 rounded-lg transition-colors"
              >
                <span>Watch on YouTube</span>
                <ExternalLink size={14} />
              </a>
            )}

            <button
              onClick={onClose}
              className="p-1.5 text-slate-400 hover:text-slate-100 hover:bg-slate-800 rounded-lg transition-colors"
              title="Close Theater Mode"
            >
              <X size={20} />
            </button>
          </div>
        </div>

        {/* Theater Content Viewport */}
        <div className="flex-1 flex flex-col lg:flex-row overflow-hidden bg-slate-950 relative">
          
          {/* Main Video Screen (Hidden in Full Screen Chat Mode) */}
          {!isChatFullScreen && (
            <div 
              className="flex-1 flex flex-col bg-black relative min-w-0"
              style={{ width: `calc(100% - ${sidebarWidth}px)` }}
            >
              <div className="flex-1 relative flex items-center justify-center">
                {embedUrl ? (
                  <iframe
                    key={`${activePlaylistIdx}-${activeVideoIdx}`}
                    src={embedUrl}
                    title={currentVideoTitle}
                    className="w-full h-full border-0"
                    style={{ pointerEvents: isDragging ? 'none' : 'auto' }}
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                    allowFullScreen
                  />
                ) : (
                  <div className="flex flex-col items-center gap-4 text-slate-400 p-8 text-center">
                    <Tv size={48} className="text-slate-600" />
                    <p className="text-sm">External video playlist link.</p>
                    <a
                      href={currentPlaylist.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold rounded-lg transition-all"
                    >
                      Open YouTube Playlist
                    </a>
                  </div>
                )}
              </div>

              {/* Video Controls Bar */}
              <div className="p-3.5 bg-slate-900 border-t border-slate-800 flex flex-wrap items-center justify-between gap-2 text-xs text-slate-300">
                <div className="flex items-center gap-3 max-w-xl min-w-0">
                  <span className="font-semibold text-slate-100 flex-shrink-0">
                    Lecture #{activeVideoIdx + 1}
                  </span>
                  <span className="text-slate-600">•</span>
                  <span className="text-slate-300 truncate font-medium">{currentVideoTitle}</span>
                </div>

                <div className="flex items-center gap-2 flex-shrink-0">
                  {/* 1-Click AI Video Summary Trigger */}
                  <button
                    onClick={handleGenerateSummary}
                    disabled={summaryLoading}
                    className="px-3 py-1.5 rounded-lg bg-gradient-to-r from-amber-500/20 via-indigo-500/20 to-purple-500/20 hover:from-amber-500/30 hover:to-purple-500/30 border border-indigo-500/40 text-indigo-300 hover:text-white font-medium text-xs flex items-center gap-1.5 transition-all shadow-sm"
                  >
                    {summaryLoading ? (
                      <Loader2 size={14} className="animate-spin text-amber-400" />
                    ) : (
                      <Sparkles size={14} className="text-amber-400" />
                    )}
                    <span>Summarize Video</span>
                  </button>

                  {listId && (
                    <>
                      <button
                        disabled={activeVideoIdx === 0}
                        onClick={() => setActiveVideoIdx((v) => Math.max(0, v - 1))}
                        className="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 disabled:opacity-40 disabled:cursor-not-allowed transition-colors font-medium"
                      >
                        Previous Video
                      </button>
                      <button
                        disabled={activeVideoIdx >= totalVideosCount - 1}
                        onClick={() => setActiveVideoIdx((v) => v + 1)}
                        className="px-3 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white font-medium disabled:opacity-40 disabled:cursor-not-allowed transition-colors flex items-center gap-1 shadow-md shadow-indigo-600/20"
                      >
                        <span>Next Video</span>
                        <ChevronRight size={14} />
                      </button>
                    </>
                  )}
                </div>
              </div>
            </div>
          )}

          {/* Draggable Vertical Splitter Resizer Handle (Hidden in Full Screen Chat Mode) */}
          {!isChatFullScreen && (
            <div
              onMouseDown={handleMouseDown}
              className={`hidden lg:flex items-center justify-center w-3 cursor-col-resize group bg-slate-950 border-x border-slate-800/80 hover:bg-indigo-600/40 transition-colors relative z-20 select-none ${
                isDragging ? 'bg-indigo-600/50 border-indigo-400' : ''
              }`}
              title="Drag left/right to resize Cineview video & chat width"
            >
              <div className={`w-1 h-8 rounded-full transition-colors ${
                isDragging ? 'bg-indigo-300' : 'bg-slate-700 group-hover:bg-indigo-400'
              }`} />
            </div>
          )}

          {/* Interactive Right Sidebar: Tracklist or Ask AI (Expands to 100% width in Full Screen Chat Mode) */}
          <div 
            className={`border-t lg:border-t-0 border-slate-800 bg-slate-900 flex flex-col ${
              isChatFullScreen ? 'w-full h-full flex-1' : 'h-80 lg:h-full flex-shrink-0'
            }`}
            style={isChatFullScreen ? {} : { width: `${sidebarWidth}px` }}
          >
            
            {/* Sidebar Tab Selector Header */}
            <div className="px-3 py-2 border-b border-slate-800 bg-slate-950 flex items-center justify-between gap-2">
              <div className="flex items-center gap-1 bg-slate-900 p-1 rounded-xl border border-slate-800 flex-1">
                <button
                  onClick={() => setSidebarTab('tracklist')}
                  className={`flex-1 py-1.5 px-3 rounded-lg text-xs font-semibold flex items-center justify-center gap-1.5 transition-all ${
                    sidebarTab === 'tracklist'
                      ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/20'
                      : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
                  }`}
                >
                  <ListVideo size={14} />
                  <span>Tracklist ({realVideos.length || 'All'})</span>
                </button>

                <button
                  onClick={() => setSidebarTab('ai')}
                  className={`flex-1 py-1.5 px-3 rounded-lg text-xs font-semibold flex items-center justify-center gap-1.5 transition-all relative ${
                    sidebarTab === 'ai'
                      ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow-md shadow-indigo-600/20'
                      : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
                  }`}
                >
                  <Sparkles size={14} className="text-amber-400" />
                  <span>Ask AI Assistant</span>
                  {chatMessages.length > 0 && sidebarTab !== 'ai' && (
                    <span className="w-2 h-2 rounded-full bg-amber-400 absolute top-1.5 right-2 animate-pulse" />
                  )}
                </button>
              </div>

              {/* Full Screen Chat Mode Toggle Button */}
              <button
                onClick={() => {
                  setSidebarTab('ai');
                  setIsChatFullScreen(!isChatFullScreen);
                }}
                className={`p-2 rounded-xl border transition-all flex items-center gap-1 text-xs font-semibold ${
                  isChatFullScreen
                    ? 'bg-amber-500/20 border-amber-500/40 text-amber-300 hover:bg-amber-500/30'
                    : 'bg-slate-800/80 border-slate-700/60 text-slate-300 hover:bg-slate-700 hover:text-white'
                }`}
                title={isChatFullScreen ? 'Exit Full Screen Chat' : 'Expand Chat to Full Screen'}
              >
                {isChatFullScreen ? <Minimize2 size={15} /> : <Maximize2 size={15} />}
                <span className="hidden sm:inline">{isChatFullScreen ? 'Exit Chat Full Screen' : 'Full Screen Chat'}</span>
              </button>
            </div>

            {/* TAB 1: TRACKLIST */}
            {sidebarTab === 'tracklist' && (
              <div className="flex-1 flex flex-col min-h-0">
                {/* Tracklist Info Header */}
                <div className="px-3.5 py-2 border-b border-slate-800/60 bg-slate-950/60 flex items-center justify-between">
                  <span className="text-[11px] font-semibold text-slate-400 flex items-center gap-1.5">
                    <Tv size={13} className="text-indigo-400" />
                    <span>Select Lecture Video</span>
                  </span>
                  {loadingItems ? (
                    <Loader2 size={13} className="animate-spin text-indigo-400" />
                  ) : (
                    <span className="text-[10px] text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-2 py-0.5 rounded font-medium">
                      {realVideos.length > 0 ? 'Live YouTube Titles' : 'YouTube Verified'}
                    </span>
                  )}
                </div>

                {/* Video List */}
                <div className="flex-1 overflow-y-auto p-2.5 space-y-2 custom-scrollbar">
                  {loadingItems ? (
                    <div className="flex flex-col items-center justify-center py-12 text-slate-500 gap-2">
                      <Loader2 size={24} className="animate-spin text-indigo-500" />
                      <p className="text-xs">Fetching real YouTube video titles...</p>
                    </div>
                  ) : realVideos.length > 0 ? (
                    realVideos.map((video, idx) => {
                      const isActive = activeVideoIdx === idx;
                      return (
                        <button
                          key={video.videoId || idx}
                          onClick={() => setActiveVideoIdx(idx)}
                          className={`w-full text-left p-3 rounded-xl transition-all flex items-start gap-3 border ${
                            isActive
                              ? 'bg-indigo-600/15 border-indigo-500/50 text-indigo-100 shadow-md shadow-indigo-500/10'
                              : 'bg-slate-950/40 border-slate-800/60 hover:bg-slate-800/80 text-slate-300 hover:text-slate-100'
                          }`}
                        >
                          <div
                            className={`h-7 w-7 rounded-lg flex items-center justify-center flex-shrink-0 text-xs font-semibold mt-0.5 ${
                              isActive
                                ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30'
                                : 'bg-slate-800 text-slate-400'
                            }`}
                          >
                            {isActive ? <Play size={12} className="fill-current" /> : idx + 1}
                          </div>
                          <div className="flex-1 min-w-0">
                            <p className={`text-xs leading-snug line-clamp-2 ${isActive ? 'text-indigo-200 font-semibold' : 'font-medium'}`}>
                              {video.title}
                            </p>
                            <p className="text-[10px] text-slate-400 mt-1 flex items-center justify-between">
                              <span>{isActive ? '▶ Playing Now' : `Video #${idx + 1}`}</span>
                              {isActive && <span className="text-emerald-400 font-semibold">Active</span>}
                            </p>
                          </div>
                        </button>
                      );
                    })
                  ) : (
                    Array.from({ length: 15 }).map((_, idx) => {
                      const isActive = activeVideoIdx === idx;
                      return (
                        <button
                          key={idx}
                          onClick={() => setActiveVideoIdx(idx)}
                          className={`w-full text-left p-3 rounded-xl transition-all flex items-center gap-3 border ${
                            isActive
                              ? 'bg-indigo-600/15 border-indigo-500/50 text-indigo-100'
                              : 'bg-slate-950/40 border-slate-800/60 hover:bg-slate-800/80 text-slate-400 hover:text-slate-200'
                          }`}
                        >
                          <div
                            className={`h-7 w-7 rounded-lg flex items-center justify-center flex-shrink-0 text-xs font-semibold ${
                              isActive
                                ? 'bg-indigo-600 text-white shadow-md'
                                : 'bg-slate-800 text-slate-400'
                            }`}
                          >
                            {isActive ? <Play size={12} className="fill-current" /> : idx + 1}
                          </div>
                          <div className="flex-1 min-w-0">
                            <p className={`text-xs font-medium truncate ${isActive ? 'text-indigo-300 font-semibold' : ''}`}>
                              Lecture Video Part {idx + 1}
                            </p>
                            <p className="text-[10px] text-slate-400 mt-0.5">
                              {isActive ? '▶ Playing Now' : 'Click to play in YouTube player'}
                            </p>
                          </div>
                        </button>
                      );
                    })
                  )}
                </div>

                {/* Footer Course Selector */}
                {playlists.length > 1 && (
                  <div className="p-3 border-t border-slate-800 bg-slate-950/80">
                    <p className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                      <Sparkles size={12} className="text-amber-400" />
                      <span>Other Playlists in Course</span>
                    </p>
                    <div className="space-y-1">
                      {playlists.map((pl, idx) => (
                        <button
                          key={idx}
                          onClick={() => setActivePlaylistIdx(idx)}
                          className={`w-full text-left px-2.5 py-1.5 rounded-lg text-xs transition-colors truncate flex items-center justify-between ${
                            activePlaylistIdx === idx
                              ? 'bg-indigo-500/10 text-indigo-400 font-semibold'
                              : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'
                          }`}
                        >
                          <span className="truncate">{pl.title || `Playlist ${idx + 1}`}</span>
                          {activePlaylistIdx === idx && <span className="text-[10px] text-indigo-400">Active</span>}
                        </button>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* TAB 2: ASK AI / VIDEO SUMMARY */}
            {sidebarTab === 'ai' && (
              <div className="flex-1 flex flex-col min-h-0 bg-slate-950/50">
                
                {/* Active Video AI Header */}
                <div className="p-3 border-b border-slate-800 bg-slate-900/90 flex items-center justify-between gap-2">
                  <div className="flex items-center gap-2 min-w-0">
                    <div className="w-7 h-7 rounded-lg bg-indigo-600/20 border border-indigo-500/40 flex items-center justify-center text-indigo-400 flex-shrink-0">
                      <Bot size={16} />
                    </div>
                    <div className="min-w-0">
                      <div className="flex items-center gap-2">
                        <p className="text-xs font-bold text-slate-200 truncate">Video AI Assistant</p>
                        {isChatFullScreen && (
                          <span className="px-2 py-0.5 text-[10px] font-bold bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 rounded flex items-center gap-1">
                            🖥️ Full Screen Concept Mode
                          </span>
                        )}
                      </div>
                      <p className="text-[10px] text-slate-400 truncate">Watching: {currentVideoTitle}</p>
                    </div>
                  </div>

                  <div className="flex items-center gap-2">
                    {isChatFullScreen && (
                      <button
                        onClick={() => setIsChatFullScreen(false)}
                        className="px-2.5 py-1 text-[11px] font-semibold bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg border border-slate-700 transition-all flex items-center gap-1"
                      >
                        <Minimize2 size={12} />
                        <span>Exit Full Screen</span>
                      </button>
                    )}

                    <button
                      onClick={handleGenerateSummary}
                      disabled={summaryLoading}
                      className="px-2.5 py-1 text-[11px] font-semibold bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg transition-all flex items-center gap-1 shadow-sm flex-shrink-0 disabled:opacity-50"
                    >
                      {summaryLoading ? (
                        <Loader2 size={12} className="animate-spin" />
                      ) : (
                        <Sparkles size={12} className="text-amber-300" />
                      )}
                      <span>Summarize</span>
                    </button>
                  </div>
                </div>

                {/* Messages & Chat History */}
                <div className="flex-1 overflow-y-auto p-3 space-y-3 custom-scrollbar">
                  {chatMessages.length === 0 ? (
                    <div className="py-6 px-3 text-center flex flex-col items-center gap-3">
                      <div className="w-12 h-12 rounded-2xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-400 shadow-inner">
                        <Sparkles size={24} className="text-amber-400 animate-pulse" />
                      </div>
                      <div>
                        <h4 className="text-xs font-bold text-slate-200">Ask Anything About This Video</h4>
                        <p className="text-[11px] text-slate-400 mt-1 leading-relaxed max-w-xs">
                          EduMind AI generates Mermaid flowcharts & answers questions using syllabus notes.
                        </p>
                      </div>

                      {/* Quick Prompt Chips */}
                      <div className="w-full space-y-1.5 mt-2">
                        <button
                          onClick={handleGenerateSummary}
                          className="w-full p-2.5 rounded-xl bg-slate-900 border border-slate-800 hover:border-indigo-500/40 text-left text-xs text-indigo-300 hover:text-white transition-all flex items-center gap-2 group"
                        >
                          <Sparkles size={14} className="text-amber-400 group-hover:scale-110 transition-transform" />
                          <span>✨ Generate 1-Click Executive Summary</span>
                        </button>
                        <button
                          onClick={() => handleSendQuestion('Explain the core concept covered in this lecture video with a Mermaid flowchart diagram.')}
                          className="w-full p-2 rounded-xl bg-slate-900/80 border border-slate-800 hover:border-indigo-500/30 text-left text-xs text-slate-300 hover:text-indigo-200 transition-all flex items-center gap-2"
                        >
                          <BookOpen size={14} className="text-indigo-400" />
                          <span>📊 Generate flowchart diagram & concepts</span>
                        </button>
                        <button
                          onClick={() => handleSendQuestion('Give me 3 potential exam questions based on this video topic.')}
                          className="w-full p-2 rounded-xl bg-slate-900/80 border border-slate-800 hover:border-indigo-500/30 text-left text-xs text-slate-300 hover:text-indigo-200 transition-all flex items-center gap-2"
                        >
                          <HelpCircle size={14} className="text-purple-400" />
                          <span>📝 Give 3 high-yield exam questions</span>
                        </button>
                      </div>
                    </div>
                  ) : (
                    chatMessages.map((msg) => (
                      <div
                        key={msg.id}
                        className={`flex gap-2.5 text-xs ${
                          msg.role === 'user' ? 'justify-end' : 'justify-start'
                        }`}
                      >
                        {msg.role === 'assistant' && (
                          <div className="w-6 h-6 rounded-lg bg-indigo-600/30 border border-indigo-500/40 flex items-center justify-center text-indigo-300 flex-shrink-0 mt-0.5">
                            <Bot size={13} />
                          </div>
                        )}

                        <div
                          className={`max-w-[90%] rounded-2xl p-3 shadow-md ${
                            msg.role === 'user'
                              ? 'bg-indigo-600 text-white rounded-tr-none'
                              : 'bg-slate-900 border border-slate-800 text-slate-200 rounded-tl-none'
                          }`}
                        >
                          {msg.role === 'assistant' ? (
                            <div className="text-xs text-slate-200 leading-relaxed space-y-1 select-text">
                              <ReactMarkdown
                                remarkPlugins={[remarkGfm, remarkMath]}
                                rehypePlugins={[rehypeKatex, rehypeRaw]}
                                components={MarkdownComponents}
                              >
                                {preprocessMarkdownContent(msg.content)}
                              </ReactMarkdown>

                              {msg.grounded && (
                                <div className="mt-2 pt-1.5 border-t border-slate-800 text-[10px] text-emerald-400 flex items-center gap-1 font-medium">
                                  <CheckCircle2 size={11} />
                                  <span>Grounded in Subject RAG Notes</span>
                                </div>
                              )}
                            </div>
                          ) : (
                            <p className="leading-relaxed font-medium">{msg.content}</p>
                          )}
                          <span className="text-[9px] text-slate-400 block text-right mt-1 opacity-70">
                            {msg.timestamp}
                          </span>
                        </div>

                        {msg.role === 'user' && (
                          <div className="w-6 h-6 rounded-lg bg-slate-800 border border-slate-700 flex items-center justify-center text-slate-300 flex-shrink-0 mt-0.5">
                            <User size={13} />
                          </div>
                        )}
                      </div>
                    ))
                  )}

                  {(aiLoading || summaryLoading) && (
                    <div className="flex items-center gap-2 text-xs text-indigo-400 bg-indigo-500/10 border border-indigo-500/20 p-2.5 rounded-xl w-max animate-pulse">
                      <Loader2 size={14} className="animate-spin" />
                      <span>{summaryLoading ? 'Generating lecture video summary...' : 'AI is thinking & rendering diagram...'}</span>
                    </div>
                  )}

                  <div ref={chatEndRef} />
                </div>

                {/* Question Input Footer */}
                <div className="p-2.5 border-t border-slate-800 bg-slate-950">
                  <form
                    onSubmit={(e) => {
                      e.preventDefault();
                      handleSendQuestion();
                    }}
                    className="flex items-center gap-2"
                  >
                    <input
                      type="text"
                      value={inputQuery}
                      onChange={(e) => setInputQuery(e.target.value)}
                      placeholder="Ask AI or request a flowchart..."
                      disabled={aiLoading || summaryLoading}
                      className="flex-1 bg-slate-900 border border-slate-800 hover:border-slate-700 focus:border-indigo-500 text-slate-100 text-xs rounded-xl px-3 py-2 outline-none transition-colors placeholder:text-slate-500 disabled:opacity-50"
                    />
                    <button
                      type="submit"
                      disabled={!inputQuery.trim() || aiLoading || summaryLoading}
                      className="p-2 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-40 disabled:cursor-not-allowed text-white rounded-xl transition-all shadow-md shadow-indigo-600/30 flex-shrink-0"
                      title="Send Question"
                    >
                      <Send size={14} />
                    </button>
                  </form>
                </div>
              </div>
            )}

          </div>
        </div>
      </div>
    </div>
  );
}

