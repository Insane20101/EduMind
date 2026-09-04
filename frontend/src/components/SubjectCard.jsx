import React from 'react';
import { Book, Network, Cpu, Database, ChevronRight } from 'lucide-react';
import { Link } from 'react-router-dom';
import { useAppStore } from '../store/appStore';

const getIcon = (code) => {
  if (code.includes('BSM')) return <Network className="text-accent" size={24} />;
  if (code.includes('BEE') || code.includes('BEC')) return <Cpu className="text-accent" size={24} />;
  if (code.includes('BCS')) {
    if (code.includes('251') || code.includes('Data')) return <Database className="text-accent" size={24} />;
    return <Book className="text-accent" size={24} />;
  }
  return <Book className="text-accent" size={24} />;
};

export default function SubjectCard({ subject }) {
  const setSubject = useAppStore(state => state.setSubject);
  const branch = useAppStore(state => state.branch);
  const sem = useAppStore(state => state.sem);
  
  const handleClick = (e) => {
    setSubject(subject.code, subject.name);
  };

  return (
    <div className="bg-card p-6 rounded-xl border border-border-subtle shadow-sm hover:shadow-md transition-shadow flex flex-col h-full">
      <div className="h-12 w-12 rounded-lg bg-muted flex items-center justify-center mb-4">
        {getIcon(subject.code)}
      </div>
      <h3 className="text-lg font-semibold text-text-primary mb-2 flex-grow">
        {subject.name}
      </h3>
      <p className="text-sm text-text-secondary mb-6 font-medium">
        {subject.code}
      </p>
      
      <Link 
        to={`/chat?branch=${branch}&sem=${sem}&subject=${subject.code}`}
        onClick={handleClick}
        className="w-full flex items-center justify-center gap-2 bg-primary hover:bg-primary-hover text-white py-2.5 rounded-lg font-medium transition-colors mt-auto"
      >
        Start Learning
        <ChevronRight size={18} />
      </Link>
    </div>
  );
}
