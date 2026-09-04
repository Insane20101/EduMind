import { create } from 'zustand';

export const useAppStore = create((set) => ({
  branch: 'CSE', 
  sem: 'Semester-3', 
  subject: null, 
  activeSubjectName: null, 
  chatContext: 'All Subjects', 
  subjectsData: {},
  isLoadingSubjects: false,
  
  // Chat Drawer & Attachment State
  isChatDrawerOpen: false,
  toggleChatDrawer: () => set((state) => ({ isChatDrawerOpen: !state.isChatDrawerOpen })),
  setChatDrawerOpen: (isOpen) => set({ isChatDrawerOpen: isOpen }),
  
  pendingPrompt: null,
  sendPrompt: (promptText) => set({ pendingPrompt: promptText, isChatDrawerOpen: true }),
  clearPendingPrompt: () => set({ pendingPrompt: null }),
  
  tempFile: null,
  setTempFile: (file) => set({ tempFile: file }),
  clearTempFile: () => set({ tempFile: null }),
  
  // Admin Ingestion Lock & Progress State
  ingestionState: { status: 'idle', progress: 0, message: '', locked: false, filename: '' },
  setIngestionState: (newState) => set((state) => ({
    ingestionState: { ...state.ingestionState, ...newState }
  })),

  fetchSubjects: async () => {
    set({ isLoadingSubjects: true });
    try {
      const baseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
      const res = await fetch(`${baseUrl}/api/subjects/`);
      if (res.ok) {
        const data = await res.json();
        set({ subjectsData: data, isLoadingSubjects: false });
      } else {
        set({ isLoadingSubjects: false });
      }
    } catch (error) {
      console.error("Failed to fetch subjects:", error);
      set({ isLoadingSubjects: false });
    }
  },

  setSubject: (subjectCode, subjectName) => set({ 
    subject: subjectCode, 
    activeSubjectName: subjectName,
    chatContext: subjectName || 'All Subjects'
  }),
  
  setSemester: (sem) => set({ sem }),
  
  setBranch: (branch) => set({ branch }),
  
  clearSubject: () => set({ 
    subject: null, 
    activeSubjectName: null, 
    chatContext: 'All Subjects' 
  }),
}));
