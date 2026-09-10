import React, { useState, useEffect, useRef } from 'react';
import { useAdminAuth } from '../store/useAdminAuth';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { api } from '../services/api';
import { useAppStore } from '../store/appStore';
import EduMindLogo from '../components/EduMindLogo';
import PdfViewerModal from '../components/PdfViewerModal';
import { getApiBaseUrl } from '../config';

// ── Icons ──────────────────────────────────────────────────────────────────────
const Icon = ({ path, size = 20 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d={path} />
  </svg>
);
const UploadIcon    = () => <Icon path="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M17 8l-5-5-5 5M12 3v12" />;
const CheckIcon     = () => <Icon path="M20 6L9 17l-5-5" />;
const XIcon         = () => <Icon path="M18 6L6 18M6 6l12 12" />;
const TrashIcon     = () => <Icon path="M3 6h18M8 6V4h8v2M19 6l-1 14H6L5 6" />;
const KeyIcon       = () => <Icon path="M21 2l-2 2m-7.61 7.61a5.5 5.5 0 1 1-7.778 7.778 5.5 5.5 0 0 1 7.777-7.777zm0 0L15.5 7.5m0 0l3 3L22 7l-3-3m-3.5 3.5L19 4" />;
const InboxIcon     = () => <Icon path="M22 12h-6l-2 3h-4l-2-3H2M5.45 5.11L2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z" />;
const FilesIcon     = () => <Icon path="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8zM14 2v6h6M16 13H8M16 17H8M10 9H8" />;
const LogoutIcon    = () => <Icon path="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4M16 17l5-5-5-5M21 12H9" />;
const ChartIcon     = () => <Icon path="M18 20V10M12 20V4M6 20v-6" />;
const ClockIcon     = () => <Icon path="M12 8v4l3 3m6-3a9 9 0 1 1-18 0 9 9 0 0 1 18 0z" />;

// ── Shared helpers & Constants ──────────────────────────────────────────────────
const SUBJECT_OPTIONS = [
  { id: '', name: 'All Subjects' },
  { id: 'CS301', name: 'Operating Systems (CS301)' },
  { id: 'CS302', name: 'Database Management Systems (CS302)' },
  { id: 'CS303', name: 'Computer Networks (CS303)' },
  { id: 'BCS-401', name: 'Operating System (BCS-401)' },
  { id: 'BCS-402', name: 'Cryptography and Information Security (BCS-402)' },
  { id: 'BSM-104', name: 'Linear Algebra & Calculus (BSM-104)' },
  { id: 'KCS-501', name: 'Database Management System (KCS-501)' },
  { id: 'KCS-502', name: 'Compiler Design (KCS-502)' },
  { id: 'KCS-503', name: 'Design and Analysis of Algorithms (KCS-503)' },
];

const formatDate = (isoStr) => {
  if (!isoStr) return null;
  try {
    const d = new Date(isoStr);
    if (isNaN(d.getTime())) return isoStr;
    return d.toLocaleString('en-US', {
      day: '2-digit',
      month: 'short',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      hour12: true
    });
  } catch {
    return isoStr;
  }
};

const Badge = ({ status }) => {
  const map = {
    approved: 'bg-emerald-500/15 text-emerald-400 border-emerald-500/30',
    pending:  'bg-amber-500/15  text-amber-400  border-amber-500/30',
    rejected: 'bg-rose-500/15   text-rose-400   border-rose-500/30',
  };
  return (
    <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-semibold border ${map[status] ?? 'bg-gray-500/15 text-gray-400 border-gray-500/30'}`}>
      {status}
    </span>
  );
};

const Spinner = () => (
  <div className="adm-spinner" />
);

// ── Tab: Live Analytics & Overview ──────────────────────────────────────────────
function OverviewTab() {
  const [stats, setStats]     = useState(null);
  const [loading, setLoading] = useState(true);

  const loadStats = async () => {
    setLoading(true);
    try {
      const res = await api.get('/admin/resources/stats');
      setStats(res.data);
    } catch {
      toast.error('Failed to fetch live analytics.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { loadStats(); }, []);

  if (loading) {
    return <div className="adm-card flex items-center justify-center p-12"><Spinner /></div>;
  }

  const s = stats || {};

  return (
    <div className="space-y-6">
      <div className="adm-card">
        <div className="flex items-center justify-between mb-6 flex-wrap gap-4">
          <div>
            <h2 className="adm-section-title text-xl font-bold flex items-center gap-2">
              <span className="text-indigo-400">📊</span> Live Tracking &amp; Analytics
            </h2>
            <p className="adm-section-sub">Real-time breakdown of users, study resources, vector database items &amp; pending reviews.</p>
          </div>
          <button className="adm-btn-ghost flex items-center gap-2" onClick={loadStats}>
            <span>Refresh Analytics</span>
          </button>
        </div>

        {/* Live Metrics Grid */}
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
          {/* Total Users */}
          <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-4 flex flex-col justify-between shadow-sm hover:border-indigo-500/40 transition-all">
            <div className="flex items-center justify-between text-slate-400 text-xs font-semibold uppercase tracking-wider mb-2">
              <span>Total Users</span>
              <span className="text-indigo-400 text-base">👥</span>
            </div>
            <div className="text-3xl font-extrabold text-white font-mono">{s.total_users ?? 0}</div>
            <div className="text-[11px] text-slate-500 mt-2">Registered student accounts</div>
          </div>

          {/* Active Users */}
          <div className="bg-emerald-500/5 border border-emerald-500/30 rounded-xl p-4 flex flex-col justify-between shadow-sm hover:border-emerald-500/60 transition-all">
            <div className="flex items-center justify-between text-emerald-400 text-xs font-semibold uppercase tracking-wider mb-2">
              <span>Active Users</span>
              <span className="flex h-2.5 w-2.5 relative">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
              </span>
            </div>
            <div className="text-3xl font-extrabold text-emerald-300 font-mono">{s.active_users ?? 0}</div>
            <div className="text-[11px] text-emerald-400/70 mt-2">Verified &amp; active logins</div>
          </div>

          {/* Total Notes / PDFs */}
          <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-4 flex flex-col justify-between shadow-sm hover:border-blue-500/40 transition-all">
            <div className="flex items-center justify-between text-slate-400 text-xs font-semibold uppercase tracking-wider mb-2">
              <span>Total PDFs / Notes</span>
              <span className="text-blue-400 text-base">📄</span>
            </div>
            <div className="text-3xl font-extrabold text-blue-400 font-mono">{s.total_notes ?? 0}</div>
            <div className="text-[11px] text-slate-500 mt-2">Approved study notes</div>
          </div>

          {/* Total PYQs */}
          <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-4 flex flex-col justify-between shadow-sm hover:border-purple-500/40 transition-all">
            <div className="flex items-center justify-between text-slate-400 text-xs font-semibold uppercase tracking-wider mb-2">
              <span>Total PYQs</span>
              <span className="text-purple-400 text-base">📝</span>
            </div>
            <div className="text-3xl font-extrabold text-purple-400 font-mono">{s.total_pyqs ?? 0}</div>
            <div className="text-[11px] text-slate-500 mt-2">Previous year question papers</div>
          </div>

          {/* Total Playlists */}
          <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-4 flex flex-col justify-between shadow-sm hover:border-pink-500/40 transition-all">
            <div className="flex items-center justify-between text-slate-400 text-xs font-semibold uppercase tracking-wider mb-2">
              <span>Total Playlists</span>
              <span className="text-pink-400 text-base">🎬</span>
            </div>
            <div className="text-3xl font-extrabold text-pink-400 font-mono">{s.total_playlists ?? 0}</div>
            <div className="text-[11px] text-slate-500 mt-2">YouTube course playlists</div>
          </div>

          {/* Total Video Lectures */}
          <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-4 flex flex-col justify-between shadow-sm hover:border-red-500/40 transition-all">
            <div className="flex items-center justify-between text-slate-400 text-xs font-semibold uppercase tracking-wider mb-2">
              <span>Total Lectures</span>
              <span className="text-red-400 text-base">🎥</span>
            </div>
            <div className="text-3xl font-extrabold text-red-400 font-mono">{s.total_lectures ?? 0}</div>
            <div className="text-[11px] text-slate-500 mt-2">Playlists + Video links</div>
          </div>

          {/* Pending Reviews */}
          <div className="bg-amber-500/5 border border-amber-500/30 rounded-xl p-4 flex flex-col justify-between shadow-sm hover:border-amber-500/60 transition-all">
            <div className="flex items-center justify-between text-amber-400 text-xs font-semibold uppercase tracking-wider mb-2">
              <span>Pending Approvals</span>
              <span className="text-amber-400 text-base">⏳</span>
            </div>
            <div className="text-3xl font-extrabold text-amber-300 font-mono">{s.pending_reviews ?? 0}</div>
            <div className="text-[11px] text-amber-400/70 mt-2">Awaiting admin review</div>
          </div>

          {/* Approved Resources Total */}
          <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-4 flex flex-col justify-between shadow-sm hover:border-emerald-500/40 transition-all">
            <div className="flex items-center justify-between text-slate-400 text-xs font-semibold uppercase tracking-wider mb-2">
              <span>Approved Resources</span>
              <span className="text-emerald-400 text-base">✅</span>
            </div>
            <div className="text-3xl font-extrabold text-emerald-400 font-mono">{s.total_resources ?? 0}</div>
            <div className="text-[11px] text-slate-500 mt-2">Total published resources</div>
          </div>
        </div>
      </div>
    </div>
  );
}

// ── Tab: Upload Resource ────────────────────────────────────────────────────────
function UploadTab() {
  const [form, setForm]       = useState({ subject_id: '', resource_type: 'note', title: '' });
  const [file, setFile]       = useState(null);
  const [loading, setLoading] = useState(false);
  const fileRef               = useRef();
  const { ingestionState, setIngestionState } = useAppStore();

  const set = (k, v) => setForm(f => ({ ...f, [k]: v }));

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (ingestionState.locked) {
      return toast.error('An ingestion is already in progress! Please wait until it completes.');
    }
    if (!file) return toast.error('Please select a file.');
    
    setLoading(true);
    setIngestionState({ 
      status: 'processing', 
      progress: 15, 
      message: 'Uploading document & starting Google AI OCR parsing...', 
      locked: true,
      filename: file.name
    });

    try {
      const fd = new FormData();
      fd.append('subject_id',   form.subject_id.trim().toUpperCase());
      fd.append('resource_type', form.resource_type);
      fd.append('title',        form.title);
      fd.append('file',         file);
      
      setIngestionState({ progress: 50, message: 'Extracting text and equations with Google AI OCR...' });
      
      await api.post('/admin/resources/upload', fd, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      
      setIngestionState({ progress: 90, message: 'Ingesting vector chunks into Qdrant Vector Database...' });
      
      setTimeout(() => {
        setIngestionState({ 
          status: 'idle', 
          progress: 100, 
          message: 'Ingestion completed successfully!', 
          locked: false,
          filename: ''
        });
        toast.success('Resource uploaded, processed with Google AI OCR, and approved!');
        setForm({ subject_id: '', resource_type: 'note', title: '' });
        setFile(null);
        if (fileRef.current) fileRef.current.value = '';
      }, 1000);

    } catch (err) {
      setIngestionState({ 
        status: 'failed', 
        progress: 0, 
        message: 'Ingestion failed.', 
        locked: false 
      });
      toast.error(err.response?.data?.detail ?? 'Upload failed.');
    } finally {
      setLoading(false);
    }
  };

  const isIngestingActive = ingestionState.locked || loading;

  return (
    <div className="adm-card">
      <h2 className="adm-section-title">Upload Resource &amp; Ingest to RAG</h2>
      <p className="adm-section-sub">Uploaded files are auto-processed with Google AI OCR, vector-embedded into Qdrant Vector Database, and published to students.</p>

      {/* ── Active Ingestion & Locking Banner Alert ───────────────────── */}
      {isIngestingActive && (
        <div className="mb-6 p-4 rounded-xl bg-amber-500/10 border border-amber-500/30 text-amber-300 space-y-3 shadow-lg">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2 font-semibold text-sm text-amber-200">
              <span className="animate-pulse">🔒</span>
              <span>Ingestion in Progress: Do not upload any other document right now.</span>
            </div>
            <span className="text-xs font-mono font-bold bg-amber-500/20 px-2.5 py-1 rounded-full border border-amber-500/30">
              {ingestionState.progress || 25}%
            </span>
          </div>

          {/* Progress Bar */}
          <div className="w-full bg-slate-800 rounded-full h-2.5 overflow-hidden border border-amber-500/20">
            <div 
              className="bg-gradient-to-r from-amber-500 to-yellow-400 h-2.5 rounded-full transition-all duration-500 ease-out shadow-sm"
              style={{ width: `${ingestionState.progress || 25}%` }}
            />
          </div>

          <p className="text-xs text-amber-300/80 font-mono">
            Status: {ingestionState.message || 'Current ingestion and updation is happening...'}
          </p>
        </div>
      )}

      <form onSubmit={handleSubmit} className="adm-form">
        <div className="adm-grid-2">
          <div className="adm-field">
            <label className="adm-label">Subject ID *</label>
            <select className="adm-input" required value={form.subject_id} disabled={isIngestingActive} onChange={e => set('subject_id', e.target.value)}>
              <option value="">Select Subject</option>
              {SUBJECT_OPTIONS.filter(s => s.id).map(s => (
                <option key={s.id} value={s.id}>{s.name}</option>
              ))}
            </select>
          </div>
          <div className="adm-field">
            <label className="adm-label">Resource Type *</label>
            <select className="adm-input" value={form.resource_type} disabled={isIngestingActive} onChange={e => set('resource_type', e.target.value)}>
              <option value="note">Note (PDF)</option>
              <option value="pyq">Previous Year Question (PYQ)</option>
              <option value="other">Other Study Material</option>
            </select>
          </div>
        </div>
        <div className="adm-field">
          <label className="adm-label">Title *</label>
          <input className="adm-input" required placeholder="Unit 1 – Introduction to OS" value={form.title}
            disabled={isIngestingActive}
            onChange={e => set('title', e.target.value)} />
        </div>
        <div className="adm-field">
          <label className="adm-label">File * (PDF, JPG, PNG — Google AI OCR Enabled)</label>
          <div 
            className={`adm-file-drop ${isIngestingActive ? 'opacity-50 cursor-not-allowed' : ''}`} 
            onClick={() => !isIngestingActive && fileRef.current.click()}
          >
            <UploadIcon />
            <span>{file ? file.name : 'Click to choose file'}</span>
            {file && <span className="adm-file-size">({(file.size / 1024 / 1024).toFixed(2)} MB)</span>}
          </div>
          <input ref={fileRef} type="file" accept=".pdf,.jpg,.jpeg,.png,.webp" className="hidden"
            disabled={isIngestingActive}
            onChange={e => setFile(e.target.files[0] ?? null)} />
        </div>
        <button type="submit" className="adm-btn-primary" disabled={isIngestingActive}>
          {isIngestingActive ? <Spinner /> : <><UploadIcon /><span>Upload, Process &amp; Ingest</span></>}
        </button>
      </form>
    </div>
  );
}

// ── Tab: Review Pending ────────────────────────────────────────────────────────
function ReviewTab() {
  const [resources, setResources]           = useState([]);
  const [loading, setLoading]               = useState(true);
  const [selectedSubject, setSelectedSubject] = useState('');
  const [busy, setBusy]                     = useState({});    // resource_id → true
  const [rejectForm, setRejectForm]         = useState(null); // resource_id
  const [rejectReason, setRejectReason]     = useState('');
  const [previewDoc, setPreviewDoc]         = useState(null);

  const load = async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams({ status: 'pending' });
      if (selectedSubject) params.append('subject_id', selectedSubject);
      const res = await api.get(`/admin/resources/?${params.toString()}`);
      setResources(res.data);
    } catch {
      toast.error('Failed to load pending resources.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, [selectedSubject]);

  const approve = async (id) => {
    setBusy(b => ({ ...b, [id]: true }));
    try {
      await api.post(`/admin/resources/${id}/approve`);
      toast.success('Approved & Ingested!');
      setResources(r => r.filter(x => x.resource_id !== id));
    } catch (err) {
      toast.error(err.response?.data?.detail ?? 'Failed to approve.');
    } finally {
      setBusy(b => ({ ...b, [id]: false }));
    }
  };

  const reject = async (id) => {
    setBusy(b => ({ ...b, [id]: true }));
    try {
      const fd = new FormData();
      fd.append('reason', rejectReason);
      await api.post(`/admin/resources/${id}/reject`, fd);
      toast.success('Rejected.');
      setResources(r => r.filter(x => x.resource_id !== id));
      setRejectForm(null);
      setRejectReason('');
    } catch (err) {
      toast.error(err.response?.data?.detail ?? 'Failed to reject.');
    } finally {
      setBusy(b => ({ ...b, [id]: false }));
    }
  };

  const handleView = (r) => {
    if (r.resource_type === 'playlist' || (r.url && r.url.includes('youtube'))) {
      window.open(r.url, '_blank');
    } else {
      const targetUrl = r.resource_id ? `${getApiBaseUrl()}/api/resources/file/${r.resource_id}` : r.url;
      setPreviewDoc({ title: r.title, url: targetUrl });
    }
  };

  return (
    <div className="adm-card space-y-6">
      <div className="adm-row-between">
        <div>
          <h2 className="adm-section-title">Pending Suggestions Review</h2>
          <p className="adm-section-sub">Student-submitted resources awaiting your review and approval for ingestion.</p>
        </div>
        <div className="flex items-center gap-3">
          <select 
            className="adm-input adm-input-sm max-w-xs" 
            value={selectedSubject} 
            onChange={e => setSelectedSubject(e.target.value)}
          >
            {SUBJECT_OPTIONS.map(s => (
              <option key={s.id} value={s.id}>{s.name}</option>
            ))}
          </select>
          <button className="adm-btn-ghost" onClick={load}>Refresh</button>
        </div>
      </div>

      {loading ? (
        <div className="adm-empty"><Spinner /></div>
      ) : resources.length === 0 ? (
        <div className="adm-empty">
          <InboxIcon />
          <p>No pending submissions for this filter — you're all caught up!</p>
        </div>
      ) : (
        <div className="adm-list">
          {resources.map(r => {
            const timeStr = formatDate(r.uploaded_at) || r.uploaded_at_formatted;
            const fullSubjectName = r.subject_name ? `${r.subject_name} (${r.subject_id})` : r.subject_id;
            return (
              <div key={r.resource_id} className="adm-list-item">
                <div className="adm-list-meta space-y-1">
                  <div className="flex items-center gap-2 flex-wrap">
                    <span className="adm-list-title">{r.title}</span>
                    <span className="px-2 py-0.5 rounded text-[11px] font-medium bg-slate-800 text-slate-300 border border-slate-700 uppercase">
                      {r.resource_type === 'note' ? 'PDF Note' : r.resource_type === 'pyq' ? 'PYQ' : r.resource_type}
                    </span>
                  </div>

                  <div className="adm-list-sub flex items-center gap-3 flex-wrap text-xs text-slate-400">
                    <span className="font-semibold text-indigo-300">{fullSubjectName}</span>
                    <span>•</span>
                    <span>by <strong>{r.submitter_enrollment || 'Student'}</strong></span>
                    {timeStr && (
                      <>
                        <span>•</span>
                        <span className="flex items-center gap-1 text-slate-400">
                          <ClockIcon size={13} /> Uploaded: {timeStr}
                        </span>
                      </>
                    )}
                  </div>

                  <button onClick={() => handleView(r)} className="adm-link text-left pt-1 inline-block">
                    Preview Document ↗
                  </button>
                </div>

                <div className="adm-list-actions">
                  {rejectForm === r.resource_id ? (
                    <div className="adm-reject-inline">
                      <input className="adm-input adm-input-sm" placeholder="Reason (optional)"
                        value={rejectReason} onChange={e => setRejectReason(e.target.value)} />
                      <button className="adm-btn-danger-sm" onClick={() => reject(r.resource_id)} disabled={busy[r.resource_id]}>
                        {busy[r.resource_id] ? <Spinner /> : 'Confirm'}
                      </button>
                      <button className="adm-btn-ghost-sm" onClick={() => { setRejectForm(null); setRejectReason(''); }}>Cancel</button>
                    </div>
                  ) : (
                    <>
                      <button className="adm-btn-approve" onClick={() => approve(r.resource_id)} disabled={busy[r.resource_id]}>
                        {busy[r.resource_id] ? <Spinner /> : <><CheckIcon /><span>Approve &amp; Ingest</span></>}
                      </button>
                      <button className="adm-btn-reject" onClick={() => setRejectForm(r.resource_id)} disabled={busy[r.resource_id]}>
                        <XIcon /><span>Reject</span>
                      </button>
                    </>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      )}

      {previewDoc && (
        <PdfViewerModal
          title={previewDoc.title}
          pdfUrl={previewDoc.url}
          onClose={() => setPreviewDoc(null)}
        />
      )}
    </div>
  );
}

// ── Tab: All Resources ──────────────────────────────────────────────────────────
function AllResourcesTab() {
  const [resources, setResources]           = useState([]);
  const [loading, setLoading]               = useState(true);
  const [filterStatus, setFilterStatus]     = useState('all');
  const [selectedSubject, setSelectedSubject] = useState('');
  const [selectedType, setSelectedType]     = useState('all');
  const [busy, setBusy]                     = useState({});
  const [previewDoc, setPreviewDoc]         = useState(null);

  const load = async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (filterStatus !== 'all') params.append('status', filterStatus);
      if (selectedSubject) params.append('subject_id', selectedSubject);
      if (selectedType !== 'all') params.append('resource_type', selectedType);
      
      const res = await api.get(`/admin/resources/?${params.toString()}`);
      setResources(res.data);
    } catch {
      toast.error('Failed to load resources.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, [filterStatus, selectedSubject, selectedType]);

  const remove = async (id) => {
    if (!window.confirm('Permanently delete this resource?')) return;
    setBusy(b => ({ ...b, [id]: true }));
    try {
      await api.delete(`/admin/resources/${id}`);
      toast.success('Deleted.');
      setResources(r => r.filter(x => x.resource_id !== id));
    } catch (err) {
      toast.error(err.response?.data?.detail ?? 'Delete failed.');
    } finally {
      setBusy(b => ({ ...b, [id]: false }));
    }
  };

  const handleView = (r) => {
    if (r.resource_type === 'playlist' || (r.url && r.url.includes('youtube'))) {
      window.open(r.url, '_blank');
    } else {
      const targetUrl = r.resource_id ? `${getApiBaseUrl()}/api/resources/file/${r.resource_id}` : r.url;
      setPreviewDoc({ title: r.title, url: targetUrl });
    }
  };

  const STATUS_PILLS = ['all', 'approved', 'pending', 'rejected'];
  const TYPE_OPTIONS = [
    { id: 'all', label: 'All Resource Types' },
    { id: 'note', label: 'PDF Notes' },
    { id: 'pyq', label: 'PYQs' },
    { id: 'playlist', label: 'Playlists' },
    { id: 'other', label: 'Other Study Material' }
  ];

  return (
    <div className="adm-card space-y-6">
      <div>
        <h2 className="adm-section-title">All Resources &amp; Material Directory</h2>
        <p className="adm-section-sub">Browse, filter by subject, resource type, or status, and manage every resource in the system.</p>
      </div>

      {/* Filters bar */}
      <div className="flex flex-wrap items-center justify-between gap-4 p-3 bg-slate-900/60 rounded-xl border border-slate-800">
        <div className="flex flex-wrap items-center gap-3">
          {/* Subject selector */}
          <div className="flex items-center gap-2">
            <span className="text-xs font-semibold text-slate-400 uppercase">Subject:</span>
            <select 
              className="adm-input adm-input-sm max-w-xs" 
              value={selectedSubject} 
              onChange={e => setSelectedSubject(e.target.value)}
            >
              {SUBJECT_OPTIONS.map(s => (
                <option key={s.id} value={s.id}>{s.name}</option>
              ))}
            </select>
          </div>

          {/* Resource type selector */}
          <div className="flex items-center gap-2">
            <span className="text-xs font-semibold text-slate-400 uppercase">Type:</span>
            <select 
              className="adm-input adm-input-sm" 
              value={selectedType} 
              onChange={e => setSelectedType(e.target.value)}
            >
              {TYPE_OPTIONS.map(t => (
                <option key={t.id} value={t.id}>{t.label}</option>
              ))}
            </select>
          </div>
        </div>

        {/* Status Pills */}
        <div className="adm-filter-pills">
          {STATUS_PILLS.map(f => (
            <button key={f} className={`adm-pill ${filterStatus === f ? 'adm-pill-active' : ''}`} onClick={() => setFilterStatus(f)}>
              {f.charAt(0).toUpperCase() + f.slice(1)}
            </button>
          ))}
        </div>
      </div>

      {loading ? (
        <div className="adm-empty"><Spinner /></div>
      ) : resources.length === 0 ? (
        <div className="adm-empty">
          <FilesIcon />
          <p>No resources found for this filter combination.</p>
        </div>
      ) : (
        <div className="adm-list">
          {resources.map(r => {
            const timeStr = formatDate(r.uploaded_at) || r.uploaded_at_formatted;
            const reviewedStr = formatDate(r.reviewed_at) || r.reviewed_at_formatted;
            const fullSubjectName = r.subject_name ? `${r.subject_name} (${r.subject_id})` : r.subject_id;
            return (
              <div key={r.resource_id} className="adm-list-item">
                <div className="adm-list-meta space-y-1">
                  <div className="adm-list-title-row">
                    <span className="adm-list-title">{r.title}</span>
                    <Badge status={r.status} />
                    <span className="px-2 py-0.5 rounded text-[11px] font-medium bg-slate-800 text-slate-300 border border-slate-700 uppercase">
                      {r.resource_type === 'note' ? 'PDF Note' : r.resource_type === 'pyq' ? 'PYQ' : r.resource_type}
                    </span>
                  </div>

                  <div className="adm-list-sub flex items-center gap-3 flex-wrap text-xs text-slate-400">
                    <span className="font-semibold text-indigo-300">{fullSubjectName}</span>
                    <span>•</span>
                    <span>{r.source === 'student' ? `by Student (${r.submitter_enrollment || 'Unknown'})` : 'by Admin'}</span>
                    {timeStr && (
                      <>
                        <span>•</span>
                        <span className="flex items-center gap-1 text-slate-400">
                          <ClockIcon size={13} /> {timeStr}
                        </span>
                      </>
                    )}
                    {reviewedStr && r.status === 'approved' && (
                      <>
                        <span>•</span>
                        <span className="text-emerald-400/80">Approved: {reviewedStr}</span>
                      </>
                    )}
                  </div>

                  <button onClick={() => handleView(r)} className="adm-link text-left pt-1 inline-block">
                    View / Preview ↗
                  </button>
                </div>
                <div className="adm-list-actions">
                  <button className="adm-btn-danger-sm" onClick={() => remove(r.resource_id)} disabled={busy[r.resource_id]}>
                    {busy[r.resource_id] ? <Spinner /> : <><TrashIcon /><span>Delete</span></>}
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {previewDoc && (
        <PdfViewerModal
          title={previewDoc.title}
          pdfUrl={previewDoc.url}
          onClose={() => setPreviewDoc(null)}
        />
      )}
    </div>
  );
}

// ── Tab: Active Playlists Control ──────────────────────────────────────────────
function PlaylistsTab() {
  const [playlists, setPlaylists]           = useState([]);
  const [loading, setLoading]               = useState(true);
  const [selectedSubject, setSelectedSubject] = useState('');
  const [form, setForm]                     = useState({ subject_id: '', title: '', playlist_url: '', unit: 'Unit 1' });
  const [saving, setSaving]                 = useState(false);

  const load = async () => {
    setLoading(true);
    try {
      const params = selectedSubject ? `?subject_id=${selectedSubject}` : '';
      const res = await api.get(`/admin/resources/playlists${params}`);
      setPlaylists(res.data);
    } catch {
      toast.error('Failed to load playlists.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, [selectedSubject]);

  const handleAdd = async (e) => {
    e.preventDefault();
    setSaving(true);
    try {
      const fd = new FormData();
      fd.append('subject_id', form.subject_id.trim().toUpperCase());
      fd.append('title', form.title);
      fd.append('playlist_url', form.playlist_url);
      fd.append('unit', form.unit);
      await api.post('/admin/resources/playlists', fd);
      toast.success('Playlist added!');
      setForm({ subject_id: '', title: '', playlist_url: '', unit: 'Unit 1' });
      load();
    } catch (err) {
      toast.error(err.response?.data?.detail ?? 'Failed to add playlist.');
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Delete this playlist?')) return;
    try {
      await api.delete(`/admin/resources/playlists/${id}`);
      toast.success('Playlist deleted.');
      setPlaylists(p => p.filter(x => x.playlist_id !== id));
    } catch (err) {
      toast.error('Delete failed.');
    }
  };

  return (
    <div className="adm-card space-y-6">
      <div>
        <h2 className="adm-section-title">Active Playlists &amp; Video Courses Manager</h2>
        <p className="adm-section-sub">Add and manage active YouTube video course playlists per subject in MongoDB.</p>
      </div>

      <form onSubmit={handleAdd} className="adm-form p-4 bg-slate-900/60 rounded-xl border border-slate-800">
        <h3 className="text-sm font-bold text-slate-200 mb-1">Add New YouTube Playlist</h3>
        <div className="adm-grid-2">
          <div className="adm-field">
            <label className="adm-label">Subject ID *</label>
            <select 
              className="adm-input" 
              required 
              value={form.subject_id} 
              onChange={e => setForm(f => ({...f, subject_id: e.target.value}))}
            >
              <option value="">Select Subject</option>
              {SUBJECT_OPTIONS.filter(s => s.id).map(s => (
                <option key={s.id} value={s.id}>{s.name}</option>
              ))}
            </select>
          </div>
          <div className="adm-field">
            <label className="adm-label">Unit Tag</label>
            <input className="adm-input" placeholder="Unit 1" value={form.unit} onChange={e => setForm(f => ({...f, unit: e.target.value}))} />
          </div>
        </div>
        <div className="adm-grid-2">
          <div className="adm-field">
            <label className="adm-label">Playlist Title *</label>
            <input className="adm-input" required placeholder="Complete Video Course" value={form.title} onChange={e => setForm(f => ({...f, title: e.target.value}))} />
          </div>
          <div className="adm-field">
            <label className="adm-label">YouTube Playlist URL *</label>
            <input className="adm-input" required placeholder="https://youtube.com/playlist?list=..." value={form.playlist_url} onChange={e => setForm(f => ({...f, playlist_url: e.target.value}))} />
          </div>
        </div>
        <button type="submit" className="adm-btn-primary" disabled={saving}>
          {saving ? <Spinner /> : <span>Add Subject Playlist</span>}
        </button>
      </form>

      <div className="border-t border-slate-800 pt-6 space-y-4">
        <div className="flex items-center justify-between flex-wrap gap-4">
          <h3 className="text-base font-bold text-slate-200">Active Playlists List</h3>

          {/* Subject Filter */}
          <div className="flex items-center gap-2">
            <span className="text-xs font-semibold text-slate-400 uppercase">Filter Subject:</span>
            <select 
              className="adm-input adm-input-sm max-w-xs" 
              value={selectedSubject} 
              onChange={e => setSelectedSubject(e.target.value)}
            >
              {SUBJECT_OPTIONS.map(s => (
                <option key={s.id} value={s.id}>{s.name}</option>
              ))}
            </select>
          </div>
        </div>

        {loading ? <Spinner /> : playlists.length === 0 ? <p className="text-xs text-slate-500">No playlists found for this filter.</p> : (
          <div className="adm-list">
            {playlists.map(p => {
              const timeStr = formatDate(p.created_at) || p.created_at_formatted;
              const fullSubjectName = p.subject_name ? `${p.subject_name} (${p.subject_id})` : p.subject_id;
              return (
                <div key={p.playlist_id} className="adm-list-item">
                  <div className="adm-list-meta space-y-1">
                    <span className="adm-list-title">{p.title}</span>
                    <div className="adm-list-sub flex items-center gap-3 flex-wrap text-xs text-slate-400">
                      <span className="font-semibold text-indigo-300">{fullSubjectName}</span>
                      <span>•</span>
                      <span className="bg-slate-800 px-2 py-0.5 rounded text-slate-300 border border-slate-700">{p.unit || 'General'}</span>
                      {timeStr && (
                        <>
                          <span>•</span>
                          <span className="flex items-center gap-1 text-slate-400">
                            <ClockIcon size={13} /> Added: {timeStr}
                          </span>
                        </>
                      )}
                    </div>
                    <a href={p.url} target="_blank" rel="noopener noreferrer" className="adm-link inline-block pt-1">{p.url} ↗</a>
                  </div>
                  <button className="adm-btn-danger-sm" onClick={() => handleDelete(p.playlist_id)}>Delete</button>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}

// ── Tab: Vector Knowledge Base Curator ──────────────────────────────────────
function VectorCuratorTab() {
  const [subjectId, setSubjectId] = useState('BCS-401');
  const [chunksData, setChunksData] = useState(null);
  const [loading, setLoading]     = useState(false);
  const [mdTitle, setMdTitle]     = useState('');
  const [mdFile, setMdFile]       = useState(null);
  const [ingesting, setIngesting] = useState(false);
  const fileRef = useRef();

  const loadChunks = async (targetSubj = subjectId) => {
    const cleanSubj = (targetSubj || '').trim().toUpperCase();
    if (!cleanSubj || cleanSubj.length < 3) return;
    setLoading(true);
    try {
      const res = await api.get(`/admin/vector/chunks?subject_id=${cleanSubj}`);
      setChunksData(res.data);
    } catch (err) {
      console.warn('Vector inspection notice:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { 
    loadChunks('BCS-401'); 
  }, []);

  const handleInspectSubmit = (e) => {
    e.preventDefault();
    loadChunks(subjectId);
  };

  const handleIngestMarkdown = async (e) => {
    e.preventDefault();
    if (!mdFile) return toast.error('Please select a Markdown (.md / .txt) file.');
    setIngesting(true);
    try {
      const fd = new FormData();
      fd.append('subject_id', subjectId.trim().toUpperCase());
      fd.append('title', mdTitle || mdFile.name);
      fd.append('file', mdFile);
      await api.post('/admin/vector/ingest-md', fd);
      toast.success('Curated Markdown file ingested into vector database!');
      setMdTitle('');
      setMdFile(null);
      if (fileRef.current) fileRef.current.value = '';
      loadChunks();
    } catch (err) {
      toast.error(err.response?.data?.detail ?? 'Ingestion failed.');
    } finally {
      setIngesting(false);
    }
  };

  const handleScopedDelete = async (filename) => {
    const cleanSubj = subjectId.trim().toUpperCase();
    if (!window.confirm(`Purge all vector chunks for '${filename}' in subject '${cleanSubj}'?`)) return;
    try {
      await api.delete(`/admin/vector/chunks/${cleanSubj}/${encodeURIComponent(filename)}`);
      toast.success(`Purged chunks for ${filename}!`);
      loadChunks();
    } catch (err) {
      toast.error(err.response?.data?.detail ?? 'Delete failed.');
    }
  };

  return (
    <div className="adm-card space-y-6">
      <div>
        <h2 className="adm-section-title">Vector Knowledge Base Curator</h2>
        <p className="adm-section-sub">Inspect, refine, add, and purge Qdrant Cloud vector chunks per subject to curate high accuracy.</p>
      </div>

      <form onSubmit={handleInspectSubmit} className="adm-grid-2">
        <div className="adm-field">
          <label className="adm-label">Subject Collection ID *</label>
          <select 
            className="adm-input" 
            value={subjectId} 
            onChange={e => setSubjectId(e.target.value.toUpperCase())}
          >
            {SUBJECT_OPTIONS.filter(s => s.id).map(s => (
              <option key={s.id} value={s.id}>{s.name}</option>
            ))}
          </select>
        </div>
        <div className="flex items-end">
          <button type="submit" className="adm-btn-ghost w-full">Inspect Collection Chunks</button>
        </div>
      </form>

      {/* Add Custom Markdown Form */}
      <form onSubmit={handleIngestMarkdown} className="p-4 border border-blue-500/20 bg-blue-500/5 rounded-xl space-y-3">
        <h4 className="text-sm font-semibold text-blue-300">Curate &amp; Add Standalone Markdown / Text File</h4>
        <div className="adm-grid-2">
          <input className="adm-input" placeholder="Title (e.g. Unit 3 Extra Formula Sheet)" value={mdTitle} onChange={e => setMdTitle(e.target.value)} />
          <input ref={fileRef} type="file" accept=".md,.txt" className="adm-input" onChange={e => setMdFile(e.target.files[0] ?? null)} />
        </div>
        <button type="submit" className="adm-btn-primary" disabled={ingesting}>
          {ingesting ? <Spinner /> : <span>Ingest Markdown to {subjectId} Vector Collection</span>}
        </button>
      </form>

      {/* Inspection & Chunks Table */}
      <div>
        <h3 className="text-sm font-semibold text-slate-300 mb-2">
          Qdrant Collection: <span className="font-mono text-indigo-400">{chunksData?.collection_name}</span> ({chunksData?.total_chunks || 0} total chunks)
        </h3>
        {loading ? <Spinner /> : !chunksData || chunksData.chunks.length === 0 ? (
          <p className="text-xs text-slate-500">No vector chunks in this collection.</p>
        ) : (
          <div className="adm-list max-h-96 overflow-y-auto pr-2">
            {chunksData.chunks.map(c => (
              <div key={c.chunk_id} className="adm-list-item">
                <div className="adm-list-meta">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-mono bg-slate-800 px-2 py-0.5 rounded text-slate-300">{c.chunk_id}</span>
                    <span className="text-xs text-indigo-300 font-semibold">{c.metadata?.unit || 'unassigned'}</span>
                  </div>
                  <span className="text-xs text-slate-400 line-clamp-2 mt-1">{c.snippet}</span>
                </div>
                {c.metadata?.source_filename && (
                  <button className="adm-btn-danger-sm" onClick={() => handleScopedDelete(c.metadata.source_filename)}>
                    Purge File
                  </button>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

// ── Tab: Settings ──────────────────────────────────────────────────────────────
function SettingsTab() {
  const { updateCredentials } = useAdminAuth();
  const [creds, setCreds] = useState({ current_password: '', new_admin_id: '', new_password: '' });
  const [loading, setLoading] = useState(false);

  const set = (k, v) => setCreds(c => ({ ...c, [k]: v }));

  const handleUpdate = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await updateCredentials(creds);
      toast.success('Credentials updated!');
      setCreds({ current_password: '', new_admin_id: '', new_password: '' });
    } catch (err) {
      toast.error(err.response?.data?.detail ?? 'Update failed.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="adm-card">
      <h2 className="adm-section-title">Change Admin Credentials</h2>
      <p className="adm-section-sub">Update your admin ID or password. Current password is required.</p>
      <form onSubmit={handleUpdate} className="adm-form">
        <div className="adm-field">
          <label className="adm-label">Current Password *</label>
          <input type="password" required className="adm-input" placeholder="••••••••"
            value={creds.current_password} onChange={e => set('current_password', e.target.value)} />
        </div>
        <div className="adm-grid-2">
          <div className="adm-field">
            <label className="adm-label">New Admin ID <span className="adm-optional">(optional)</span></label>
            <input type="text" className="adm-input" placeholder="Leave blank to keep current"
              value={creds.new_admin_id} onChange={e => set('new_admin_id', e.target.value)} />
          </div>
          <div className="adm-field">
            <label className="adm-label">New Password <span className="adm-optional">(optional, min 8 chars)</span></label>
            <input type="password" className="adm-input" placeholder="Leave blank to keep current"
              value={creds.new_password} onChange={e => set('new_password', e.target.value)} />
          </div>
        </div>
        <button type="submit" className="adm-btn-primary" disabled={loading}>
          {loading ? <Spinner /> : <><KeyIcon /><span>Update Credentials</span></>}
        </button>
      </form>
    </div>
  );
}

// ── Main Dashboard ─────────────────────────────────────────────────────────────
const TABS = [
  { id: 'overview',  label: 'Analytics', icon: <ChartIcon />,   component: OverviewTab },
  { id: 'upload',    label: 'Upload',    icon: <UploadIcon />,  component: UploadTab },
  { id: 'playlists', label: 'Playlists', icon: <FilesIcon />,   component: PlaylistsTab },
  { id: 'vector',    label: 'Curator',   icon: <KeyIcon />,     component: VectorCuratorTab },
  { id: 'review',    label: 'Review',    icon: <InboxIcon />,   component: ReviewTab },
  { id: 'all',       label: 'Resources', icon: <FilesIcon />,   component: AllResourcesTab },
  { id: 'settings',  label: 'Settings',  icon: <KeyIcon />,     component: SettingsTab },
];

export default function AdminDashboard() {
  const { logout } = useAdminAuth();
  const navigate   = useNavigate();
  const [active, setActive] = useState('overview');

  useEffect(() => {
    document.title = "EduMind Admin — Analytics & Management Portal";
  }, []);

  const ActiveTab = TABS.find(t => t.id === active)?.component ?? OverviewTab;

  const handleLogout = () => { logout(); navigate('/admin/login'); };

  return (
    <>
      <style>{`
        /* ── Reset & base ── */
        .adm-root { min-height:100vh; background:#0f1117; color:#e2e8f0; font-family:'Inter',system-ui,sans-serif; padding:0; }
        
        /* ── Header ── */
        .adm-header { display:flex; align-items:center; justify-content:space-between; padding:18px 32px; background:#161b27; border-bottom:1px solid #1e2536; }
        .adm-logo { font-size:1.25rem; font-weight:700; background:linear-gradient(135deg,#6366f1,#8b5cf6); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
        .adm-header-right { display:flex; align-items:center; gap:12px; }
        .adm-badge-admin { background:#6366f1/20; color:#818cf8; border:1px solid #6366f1/30; border-radius:20px; padding:3px 12px; font-size:0.75rem; font-weight:600; }
        .adm-logout { display:flex; align-items:center; gap:6px; background:transparent; border:1px solid #2d3748; color:#94a3b8; padding:7px 14px; border-radius:8px; cursor:pointer; font-size:0.85rem; transition:all .15s; }
        .adm-logout:hover { background:#1e2536; color:#e2e8f0; border-color:#4a5568; }

        /* ── Layout ── */
        .adm-body { display:flex; gap:0; max-width:1200px; margin:0 auto; padding:32px 24px; }
        @media(max-width:768px){ .adm-body{flex-direction:column;padding:16px;} }

        /* ── Sidebar nav ── */
        .adm-nav { width:200px; flex-shrink:0; margin-right:28px; }
        @media(max-width:768px){ .adm-nav{width:100%;margin-right:0;margin-bottom:20px;display:flex;flex-wrap:wrap;gap:8px;} }
        .adm-nav-btn { display:flex; align-items:center; gap:10px; width:100%; padding:11px 14px; border-radius:10px; border:none; background:transparent; color:#94a3b8; cursor:pointer; font-size:0.9rem; transition:all .15s; margin-bottom:4px; }
        .adm-nav-btn:hover { background:#1e2536; color:#e2e8f0; }
        .adm-nav-btn.active { background:linear-gradient(135deg,#6366f1,#8b5cf6); color:#fff; box-shadow:0 4px 20px #6366f140; }
        @media(max-width:768px){ .adm-nav-btn{width:auto;flex:1;min-width:100px;justify-content:center;} }

        /* ── Content card ── */
        .adm-main { flex:1; min-width:0; }
        .adm-card { background:#161b27; border:1px solid #1e2536; border-radius:16px; padding:28px; }

        /* ── Section header ── */
        .adm-section-title { font-size:1.15rem; font-weight:700; color:#f1f5f9; margin:0 0 4px; }
        .adm-section-sub { font-size:0.85rem; color:#64748b; margin:0 0 24px; }
        .adm-row-between { display:flex; align-items:flex-start; justify-content:space-between; flex-wrap:wrap; gap:12px; margin-bottom:20px; }

        /* ── Form ── */
        .adm-form { display:flex; flex-direction:column; gap:18px; }
        .adm-grid-2 { display:grid; grid-template-columns:1fr 1fr; gap:16px; }
        @media(max-width:600px){ .adm-grid-2{grid-template-columns:1fr;} }
        .adm-field { display:flex; flex-direction:column; gap:6px; }
        .adm-label { font-size:0.8rem; font-weight:600; color:#94a3b8; letter-spacing:.03em; text-transform:uppercase; }
        .adm-optional { font-weight:400; text-transform:none; }
        .adm-input { background:#0f1117; border:1px solid #2d3748; color:#e2e8f0; padding:10px 14px; border-radius:8px; font-size:0.9rem; width:100%; box-sizing:border-box; transition:border-color .15s; outline:none; }
        .adm-input:focus { border-color:#6366f1; }
        .adm-input-sm { padding:7px 10px; font-size:0.85rem; }
        .adm-file-drop { display:flex; align-items:center; gap:12px; background:#0f1117; border:2px dashed #2d3748; border-radius:10px; padding:18px 20px; cursor:pointer; color:#64748b; transition:border-color .15s; }
        .adm-file-drop:hover { border-color:#6366f1; color:#818cf8; }
        .adm-file-size { color:#64748b; font-size:0.8rem; }
        .hidden { display:none; }

        /* ── Buttons ── */
        .adm-btn-primary { display:inline-flex; align-items:center; gap:8px; background:linear-gradient(135deg,#6366f1,#8b5cf6); color:#fff; border:none; padding:11px 22px; border-radius:10px; font-size:0.9rem; font-weight:600; cursor:pointer; transition:opacity .15s; }
        .adm-btn-primary:hover:not(:disabled) { opacity:.9; }
        .adm-btn-primary:disabled { opacity:.5; cursor:not-allowed; }
        .adm-btn-ghost { background:transparent; border:1px solid #2d3748; color:#94a3b8; padding:8px 16px; border-radius:8px; font-size:0.85rem; cursor:pointer; transition:all .15s; }
        .adm-btn-ghost:hover { background:#1e2536; color:#e2e8f0; }
        .adm-btn-approve { display:inline-flex; align-items:center; gap:6px; background:#10b98120; color:#34d399; border:1px solid #10b98140; padding:7px 14px; border-radius:8px; font-size:0.82rem; font-weight:600; cursor:pointer; transition:all .15s; white-space:nowrap; }
        .adm-btn-approve:hover:not(:disabled) { background:#10b98130; }
        .adm-btn-approve:disabled { opacity:.5; cursor:not-allowed; }
        .adm-btn-reject { display:inline-flex; align-items:center; gap:6px; background:#f4373720; color:#f87171; border:1px solid #f4373740; padding:7px 14px; border-radius:8px; font-size:0.82rem; font-weight:600; cursor:pointer; transition:all .15s; white-space:nowrap; }
        .adm-btn-reject:hover:not(:disabled) { background:#f4373730; }
        .adm-btn-danger-sm { display:inline-flex; align-items:center; gap:6px; background:#f4373710; color:#f87171; border:1px solid #f4373730; padding:6px 12px; border-radius:7px; font-size:0.8rem; font-weight:600; cursor:pointer; transition:all .15s; white-space:nowrap; }
        .adm-btn-danger-sm:hover:not(:disabled) { background:#f4373720; }
        .adm-btn-danger-sm:disabled { opacity:.5; cursor:not-allowed; }
        .adm-btn-ghost-sm { background:transparent; border:1px solid #2d3748; color:#94a3b8; padding:6px 12px; border-radius:7px; font-size:0.8rem; cursor:pointer; }

        /* ── Filter pills ── */
        .adm-filter-pills { display:flex; gap:6px; flex-wrap:wrap; }
        .adm-pill { background:transparent; border:1px solid #2d3748; color:#64748b; padding:5px 14px; border-radius:20px; font-size:0.8rem; cursor:pointer; transition:all .15s; }
        .adm-pill:hover { border-color:#6366f1; color:#818cf8; }
        .adm-pill-active { background:#6366f120; border-color:#6366f150; color:#818cf8; }

        /* ── List ── */
        .adm-list { display:flex; flex-direction:column; gap:10px; }
        .adm-list-item { display:flex; align-items:flex-start; justify-content:space-between; gap:16px; background:#0f1117; border:1px solid #1e2536; border-radius:10px; padding:14px 16px; flex-wrap:wrap; }
        .adm-list-meta { flex:1; min-width:0; display:flex; flex-direction:column; gap:4px; }
        .adm-list-title-row { display:flex; align-items:center; gap:8px; flex-wrap:wrap; }
        .adm-list-title { font-size:0.9rem; font-weight:600; color:#e2e8f0; }
        .adm-list-sub { font-size:0.78rem; color:#64748b; }
        .adm-list-actions { display:flex; align-items:center; gap:8px; flex-shrink:0; flex-wrap:wrap; }
        .adm-reject-inline { display:flex; align-items:center; gap:8px; flex-wrap:wrap; }
        .adm-link { font-size:0.78rem; color:#818cf8; text-decoration:none; }
        .adm-link:hover { text-decoration:underline; }

        /* ── Empty state ── */
        .adm-empty { display:flex; flex-direction:column; align-items:center; justify-content:center; gap:12px; padding:48px 20px; color:#475569; font-size:0.9rem; }

        /* ── Spinner ── */
        .adm-spinner { width:18px; height:18px; border:2px solid currentColor; border-top-color:transparent; border-radius:50%; animation:spin .6s linear infinite; display:inline-block; }
        @keyframes spin { to{ transform:rotate(360deg); } }
      `}</style>

      <div className="adm-root">
        {/* Header */}
        <header className="adm-header">
          <EduMindLogo size={32} textClass="text-xl font-bold tracking-tight text-white" />
          <div className="adm-header-right">
            <span className="adm-badge-admin">Administrator</span>
            <button className="adm-logout" onClick={handleLogout}>
              <LogoutIcon /> Logout
            </button>
          </div>
        </header>

        {/* Body */}
        <div className="adm-body">
          {/* Sidebar */}
          <nav className="adm-nav">
            {TABS.map(t => (
              <button key={t.id} className={`adm-nav-btn ${active === t.id ? 'active' : ''}`}
                onClick={() => setActive(t.id)}>
                {t.icon} {t.label}
              </button>
            ))}
          </nav>

          {/* Content */}
          <main className="adm-main">
            <ActiveTab />
          </main>
        </div>
      </div>
    </>
  );
}
