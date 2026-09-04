import React, { useState, useEffect } from 'react';
import Accordion from './Accordion';
import FileCard from './FileCard';
import VideoCard from './VideoCard';
import PlaylistTheaterModal from './PlaylistTheaterModal';
import { useAppStore } from '../store/appStore';
import { useAuth } from '../store/useAuth';
import toast from 'react-hot-toast';

const API = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';


// ── Loading / empty placeholders ───────────────────────────────────────────────

const ComingSoon = ({ title }) => (
  <div className="py-8 text-center bg-white rounded-xl border border-border-subtle shadow-sm flex flex-col items-center justify-center">
    <div className="w-12 h-12 bg-blue-50 text-blue-500 rounded-full flex items-center justify-center mb-3">
      <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
      </svg>
    </div>
    <h3 className="text-lg font-bold text-primary mb-1">{title} Material Coming Soon</h3>
    <p className="text-text-secondary max-w-sm text-sm">
      We're still gathering and processing the {title.toLowerCase()} for this subject. Check back later!
    </p>
  </div>
);

const LoadingPlaceholder = () => (
  <div className="p-4 text-center text-text-secondary">Checking availability...</div>
);

// ── Suggest a Resource form ────────────────────────────────────────────────────

function SuggestForm({ subjectId }) {
  const { token } = useAuth();
  const [open, setOpen]       = useState(false);
  const [resType, setResType] = useState('note');
  const [title, setTitle]     = useState('');
  const [url, setUrl]         = useState('');
  const [file, setFile]       = useState(null);
  const [loading, setLoading] = useState(false);
  const fileRef               = React.useRef();

  const reset = () => { setResType('note'); setTitle(''); setUrl(''); setFile(null); if (fileRef.current) fileRef.current.value = ''; };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!title.trim()) { toast.error('Title is required.'); return; }
    if (!file && !url.trim()) { toast.error('Provide at least a file or a URL.'); return; }
    if (file && file.size > 10 * 1024 * 1024) { toast.error('File must be under 10 MB.'); return; }

    setLoading(true);
    try {
      const fd = new FormData();
      fd.append('subject_id',    subjectId);
      fd.append('resource_type', resType);
      fd.append('title',         title.trim());
      if (url.trim()) fd.append('url', url.trim());
      if (file)       fd.append('file', file);

      const res = await fetch(`${API}/api/resources/suggest`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${token}` },
        // No Content-Type header — browser sets it with the correct boundary
        body: fd,
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail ?? 'Submission failed.');
      toast.success('Thanks! Your submission is under admin review.');
      reset();
      setOpen(false);
    } catch (err) {
      toast.error(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mt-4">
      {!open ? (
        <button
          onClick={() => setOpen(true)}
          className="inline-flex items-center gap-2 text-sm text-primary border border-primary/30 hover:border-primary hover:bg-primary/5 px-4 py-2 rounded-lg transition-colors"
        >
          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
          </svg>
          Suggest a resource
        </button>
      ) : (
        <div className="bg-blue-50 border border-blue-200 rounded-xl p-4 space-y-3">
          <h4 className="font-semibold text-sm text-blue-900">Suggest a resource for this subject</h4>
          <form onSubmit={handleSubmit} className="space-y-3">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-medium text-blue-800 mb-1">Type</label>
                <select
                  className="w-full border border-blue-200 bg-white rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-blue-500"
                  value={resType} onChange={e => setResType(e.target.value)}
                >
                  <option value="note">Note / Study Material</option>
                  <option value="pyq">Previous Year Question</option>
                  <option value="other">Other</option>
                </select>
              </div>
              <div>
                <label className="block text-xs font-medium text-blue-800 mb-1">Title *</label>
                <input
                  required
                  className="w-full border border-blue-200 bg-white rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-blue-500"
                  placeholder="Unit 2 Notes"
                  value={title} onChange={e => setTitle(e.target.value)}
                />
              </div>
            </div>

            {/* File upload */}
            <div>
              <label className="block text-xs font-medium text-blue-800 mb-1">
                Upload file <span className="font-normal text-blue-600">(PDF / JPG / PNG, max 10 MB)</span>
              </label>
              <div
                className="flex items-center gap-2 border border-dashed border-blue-300 bg-white rounded-lg px-3 py-2 cursor-pointer hover:border-blue-500 text-sm text-blue-700"
                onClick={() => fileRef.current?.click()}
              >
                <svg className="w-4 h-4 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a2 2 0 002 2h12a2 2 0 002-2v-1M12 12V4m0 0l-3 3m3-3l3 3" />
                </svg>
                <span className="truncate">{file ? `${file.name} (${(file.size/1024/1024).toFixed(2)} MB)` : 'Choose file…'}</span>
              </div>
              <input ref={fileRef} type="file" accept=".pdf,.jpg,.jpeg,.png,.webp" className="hidden"
                onChange={e => setFile(e.target.files[0] ?? null)} />
            </div>

            {/* OR divider */}
            <div className="flex items-center gap-2 text-xs text-blue-400">
              <div className="flex-1 h-px bg-blue-200" />
              <span>or provide a link</span>
              <div className="flex-1 h-px bg-blue-200" />
            </div>

            {/* URL field */}
            <div>
              <label className="block text-xs font-medium text-blue-800 mb-1">External URL (Google Drive, etc.)</label>
              <input
                type="url"
                className="w-full border border-blue-200 bg-white rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-blue-500"
                placeholder="https://drive.google.com/…"
                value={url} onChange={e => setUrl(e.target.value)}
              />
            </div>

            <div className="flex items-center gap-3">
              <button
                type="submit" disabled={loading}
                className="bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium px-4 py-2 rounded-lg transition-colors disabled:opacity-50"
              >
                {loading ? 'Submitting…' : 'Submit for review'}
              </button>
              <button
                type="button"
                onClick={() => { setOpen(false); reset(); }}
                className="text-sm text-blue-700 hover:underline"
              >
                Cancel
              </button>
            </div>
          </form>
          <p className="text-xs text-blue-600">Submissions are reviewed by an admin before being published. Limit: 5 per minute.</p>
        </div>
      )}
    </div>
  );
}

// ── Main component ─────────────────────────────────────────────────────────────

export default function LearnTab() {
  const { subject, sem, subjectsData } = useAppStore();

  let currentSubjectData = (subjectsData[sem] || []).find(s => s.code?.toUpperCase() === subject?.toUpperCase());
  if (!currentSubjectData && subjectsData) {
    for (const semList of Object.values(subjectsData)) {
      if (Array.isArray(semList)) {
        const found = semList.find(s => s.code?.toUpperCase() === subject?.toUpperCase());
        if (found) {
          currentSubjectData = found;
          break;
        }
      }
    }
  }
  let staticPlaylists = currentSubjectData?.playlists || [];
  if (!Array.isArray(staticPlaylists)) {
    staticPlaylists = [];
  } else {
    staticPlaylists = staticPlaylists.filter(p => p && typeof p === 'object' && typeof p.url === 'string');
  }

  // null = loading, [] = none, [...] = has resources
  const [notes, setNotes] = useState(null);
  const [pyqs,  setPyqs]  = useState(null);
  const [dbPlaylists, setDbPlaylists] = useState([]);
  const [activeTheaterIdx, setActiveTheaterIdx] = useState(null);

  useEffect(() => {
    if (!subject) return;
    setNotes(null);
    setPyqs(null);
    setDbPlaylists([]);
    setActiveTheaterIdx(null);

    // Use unified /api/resources endpoint for notes and pyqs
    fetch(`${API}/api/resources?subject_id=${subject}&resource_type=note`)
      .then(res => res.json())
      .then(data => setNotes(Array.isArray(data) ? data : []))
      .catch(() => setNotes([]));

    fetch(`${API}/api/resources?subject_id=${subject}&resource_type=pyq`)
      .then(res => res.json())
      .then(data => setPyqs(Array.isArray(data) ? data : []))
      .catch(() => setPyqs([]));

    // Fetch dynamic playlists added via Admin Dashboard
    fetch(`${API}/api/resources/playlists?subject_id=${subject}`)
      .then(res => res.json())
      .then(data => setDbPlaylists(Array.isArray(data) ? data : []))
      .catch(() => setDbPlaylists([]));
  }, [subject]);

  const playlists = [...staticPlaylists, ...dbPlaylists];


  return (
    <div className="w-full space-y-4">
      <Accordion title="Notes" defaultOpen={true}>
        {notes === null ? (
          <LoadingPlaceholder />
        ) : notes.length === 0 ? (
          <ComingSoon title="Notes" />
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {notes.map((resource) => (
              <FileCard
                key={resource.resource_id}
                title={resource.title}
                label="PDF Note"
                url={resource.file_url || resource.url}
              />
            ))}
          </div>
        )}
      </Accordion>

      <Accordion title="Previous Year Questions (PYQs)">
        {pyqs === null ? (
          <LoadingPlaceholder />
        ) : pyqs.length === 0 ? (
          <ComingSoon title="PYQ" />
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {pyqs.map((resource) => (
              <FileCard
                key={resource.resource_id}
                title={resource.title}
                label="Previous Year Questions"
                url={resource.file_url || resource.url}
              />
            ))}
          </div>
        )}

      </Accordion>

      <Accordion title="Lectures">
        {playlists.length > 0 ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {playlists.map((playlist, idx) => (
              <VideoCard
                key={idx}
                item={playlist}
                onClick={() => setActiveTheaterIdx(idx)}
              />
            ))}
          </div>
        ) : (
          <div className="py-8 text-center bg-white rounded-xl border border-border-subtle shadow-sm">
            <p className="text-text-secondary text-lg">No recommended lectures available for this subject.</p>
            {currentSubjectData?.note && (
              <p className="text-sm text-text-secondary mt-2 px-6 max-w-2xl mx-auto">
                Note: {currentSubjectData.note}
              </p>
            )}
          </div>
        )}
      </Accordion>

      {/* Interactive Lecture Playlist Theater View Modal */}
      {activeTheaterIdx !== null && (
        <PlaylistTheaterModal
          playlists={playlists}
          initialIndex={activeTheaterIdx}
          onClose={() => setActiveTheaterIdx(null)}
        />
      )}

      {/* Suggest a Resource — always shown once subject is selected */}
      {subject && <SuggestForm subjectId={subject} />}
    </div>
  );

}
