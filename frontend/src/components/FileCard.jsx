import React, { useState } from 'react';
import { FileText, Eye } from 'lucide-react';
import PdfViewerModal from './PdfViewerModal';

import { getApiBaseUrl } from '../config';

export default function FileCard({ title, label, url }) {
  const [showViewer, setShowViewer] = useState(false);
  const fileUrl = url && url.startsWith('/') ? `${getApiBaseUrl()}${url}` : url;

  const handleOpen = (e) => {
    if (e) e.stopPropagation();
    if (!fileUrl) return;

    const isMobile = typeof window !== 'undefined' && (window.innerWidth < 768 || /Mobi|Android|iPhone|iPad|iPod/i.test(navigator.userAgent));
    if (isMobile) {
      window.open(fileUrl, '_blank', 'noopener,noreferrer');
    } else {
      setShowViewer(true);
    }
  };

  return (
    <>
      <div 
        onClick={handleOpen}
        className="bg-white p-4 rounded-xl border border-border-subtle shadow-sm hover:shadow-md transition-all flex items-center gap-4 group cursor-pointer"
      >
        <div className="h-10 w-10 bg-red-100 text-red-600 rounded-lg flex items-center justify-center flex-shrink-0 group-hover:scale-105 transition-transform">
          <FileText size={20} />
        </div>
        <div className="flex-1 min-w-0">
          <h4 className="font-semibold text-text-primary truncate group-hover:text-indigo-600 transition-colors">{title}</h4>
          {label && <p className="text-sm text-text-secondary truncate">{label}</p>}
        </div>
        {fileUrl ? (
          <div className="flex items-center gap-2">
            <button
              onClick={handleOpen}
              title="View PDF Document"
              className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-indigo-600 bg-indigo-50 hover:bg-indigo-100 rounded-lg transition-colors cursor-pointer"
            >
              <Eye size={15} />
              <span>View</span>
            </button>
          </div>
        ) : (
          <span className="text-xs text-text-secondary italic">No file</span>
        )}
      </div>

      {showViewer && (
        <PdfViewerModal
          title={title}
          pdfUrl={fileUrl}
          onClose={() => setShowViewer(false)}
        />
      )}
    </>
  );
}


