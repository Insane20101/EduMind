import React, { useEffect, useState } from 'react';
import { X, Lock, Eye, AlertCircle, Loader2 } from 'lucide-react';

export default function PdfViewerModal({ title, pdfUrl, onClose }) {
  const [blobUrl, setBlobUrl] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

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

    // Fetch PDF binary directly and convert to browser blob URL to bypass cross-origin / iframe blocks
    let active = true;
    let createdUrl = null;

    fetch(pdfUrl)
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}: Failed to fetch document.`);
        return res.blob();
      })
      .then((blob) => {
        if (!active) return;
        // Verify blob is non-empty PDF
        if (blob.size === 0) throw new Error('Document content is empty.');
        
        const pdfBlob = new Blob([blob], { type: 'application/pdf' });
        createdUrl = URL.createObjectURL(pdfBlob);
        setBlobUrl(`${createdUrl}#toolbar=0&navpanes=0&scrollbar=0`);
        setLoading(false);
      })
      .catch((err) => {
        if (!active) return;
        console.error('PDF Viewer Fetch Error:', err);
        setError(err.message || 'Failed to load PDF document.');
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

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-2 sm:p-4 select-none">
      <div className="bg-slate-900 border border-slate-700/80 rounded-2xl w-full max-w-5xl h-[90vh] flex flex-col shadow-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-200">
        
        {/* Header */}
        <div className="flex items-center justify-between px-5 py-3 border-b border-slate-800 bg-slate-950">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-indigo-500/10 text-indigo-400 rounded-lg">
              <Eye size={18} />
            </div>
            <div>
              <h3 className="text-sm font-semibold text-slate-100 line-clamp-1">{title || 'Course Document'}</h3>
              <p className="text-xs text-slate-400 flex items-center gap-1 mt-0.5">
                <Lock size={12} className="text-emerald-400" />
                <span>Protected View Mode · Direct Downloading Disabled</span>
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 text-slate-400 hover:text-slate-100 hover:bg-slate-800 rounded-lg transition-colors"
            title="Close Viewer"
          >
            <X size={20} />
          </button>
        </div>

        {/* Protected Viewer Container */}
        <div
          className="flex-1 relative bg-slate-950 flex items-center justify-center overflow-hidden"
          onContextMenu={(e) => e.preventDefault()}
        >
          {loading && (
            <div className="flex flex-col items-center gap-3 text-slate-400">
              <Loader2 size={32} className="animate-spin text-indigo-500" />
              <p className="text-sm font-medium">Loading document securely from MongoDB Cloud...</p>
            </div>
          )}

          {error && (
            <div className="flex flex-col items-center gap-3 text-red-400 max-w-md text-center p-6 bg-slate-900 border border-slate-800 rounded-xl">
              <AlertCircle size={36} />
              <h4 className="text-base font-semibold text-slate-200">Unable to View Document</h4>
              <p className="text-xs text-slate-400">{error}</p>
            </div>
          )}

          {!loading && !error && blobUrl && (
            <object
              data={blobUrl}
              type="application/pdf"
              className="w-full h-full border-0"
            >
              <iframe
                src={blobUrl}
                title={title || 'PDF Viewer'}
                className="w-full h-full border-0"
              />
            </object>
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
