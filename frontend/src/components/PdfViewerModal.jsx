import React, { useEffect, useState } from 'react';
import { X, Lock, Eye, AlertCircle, Loader2, ExternalLink, FileText } from 'lucide-react';

export default function PdfViewerModal({ title, pdfUrl, onClose }) {
  const [blobUrl, setBlobUrl] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [useFallback, setUseFallback] = useState(false);

  useEffect(() => {
    // Anti-save / anti-print key listeners
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
        // On cross-origin or fetch error, fallback to direct pdfUrl stream view
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

  if (!pdfUrl) return null;

  const targetViewerUrl = blobUrl || pdfUrl;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-1 sm:p-4 select-none">
      <div className="bg-slate-900 border border-slate-700/80 rounded-none sm:rounded-2xl w-full h-full sm:h-[90vh] max-w-5xl flex flex-col shadow-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-200">
        
        {/* Header */}
        <div className="flex items-center justify-between px-3 sm:px-5 py-2.5 sm:py-3 border-b border-slate-800 bg-slate-950 gap-2">
          <div className="flex items-center gap-2.5 min-w-0">
            <div className="p-1.5 sm:p-2 bg-indigo-500/10 text-indigo-400 rounded-lg flex-shrink-0">
              <Eye size={18} />
            </div>
            <div className="min-w-0">
              <h3 className="text-xs sm:text-sm font-semibold text-slate-100 truncate">{title || 'Course Document'}</h3>
              <p className="text-[10px] sm:text-xs text-slate-400 flex items-center gap-1 mt-0.5">
                <Lock size={11} className="text-emerald-400" />
                <span className="truncate">Protected View Mode · EduMind Cloud</span>
              </p>
            </div>
          </div>

          <div className="flex items-center gap-1.5 flex-shrink-0">
            {/* Open in tab button for mobile / web fallback */}
            <a
              href={pdfUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-1 px-2.5 py-1.5 text-xs font-semibold text-indigo-300 hover:text-white bg-indigo-600/20 hover:bg-indigo-600/40 border border-indigo-500/30 rounded-lg transition-all"
              title="Open document directly in browser tab"
            >
              <ExternalLink size={13} />
              <span className="hidden sm:inline">Open in Tab</span>
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

        {/* Protected Viewer Container */}
        <div
          className="flex-1 relative bg-slate-950 flex items-center justify-center overflow-hidden"
          onContextMenu={(e) => e.preventDefault()}
        >
          {loading && (
            <div className="flex flex-col items-center gap-3 text-slate-400 p-6 text-center">
              <Loader2 size={32} className="animate-spin text-indigo-500" />
              <p className="text-sm font-medium">Loading document securely from EduMind Cloud...</p>
            </div>
          )}

          {error && (
            <div className="flex flex-col items-center gap-3 text-red-400 max-w-md text-center p-6 bg-slate-900 border border-slate-800 rounded-xl">
              <AlertCircle size={36} />
              <h4 className="text-base font-semibold text-slate-200">Unable to View Document</h4>
              <p className="text-xs text-slate-400 mb-2">{error}</p>
              <a
                href={pdfUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold rounded-lg transition-all flex items-center gap-1.5"
              >
                <ExternalLink size={14} />
                <span>Open Document Directly</span>
              </a>
            </div>
          )}

          {!loading && !error && (
            <div className="w-full h-full relative">
              <iframe
                src={`${targetViewerUrl}#toolbar=0&navpanes=0&scrollbar=0`}
                title={title || 'PDF Document Viewer'}
                className="w-full h-full border-0 bg-white"
                onError={() => setUseFallback(true)}
              />
            </div>
          )}

          {/* Security Overlay */}
          <div
            className="absolute inset-0 bg-transparent pointer-events-none"
            onContextMenu={(e) => e.preventDefault()}
          />
        </div>
      </div>
    </div>
  );
}
