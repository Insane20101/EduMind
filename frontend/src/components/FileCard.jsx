import React, { useState } from 'react';
import { FileText, Eye } from 'lucide-react';
import PdfViewerModal from './PdfViewerModal';

export default function FileCard({ title, label, url }) {
  const [showViewer, setShowViewer] = useState(false);
  const API_BASE = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';
  const fileUrl = url && url.startsWith('/') ? `${API_BASE}${url}` : url;

  return (
    <>
      <div className="bg-white p-4 rounded-xl border border-border-subtle shadow-sm hover:shadow-md transition-shadow flex items-center gap-4 group">
        <div className="h-10 w-10 bg-red-100 text-red-600 rounded-lg flex items-center justify-center flex-shrink-0">
          <FileText size={20} />
        </div>
        <div className="flex-1 min-w-0">
          <h4 className="font-semibold text-text-primary truncate">{title}</h4>
          {label && <p className="text-sm text-text-secondary truncate">{label}</p>}
        </div>
        {fileUrl ? (
          <div className="flex items-center gap-2">
            <button
              onClick={() => setShowViewer(true)}
              title="View Protected PDF"
              className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-indigo-600 bg-indigo-50 hover:bg-indigo-100 rounded-lg transition-colors"
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


