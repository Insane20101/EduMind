import React, { useState } from 'react';
import { ChevronDown, ChevronUp } from 'lucide-react';
import { cn } from '../lib/utils';

export default function Accordion({ title, children, defaultOpen = false }) {
  const [isOpen, setIsOpen] = useState(defaultOpen);

  return (
    <div className="border border-border-subtle rounded-xl overflow-hidden mb-4 bg-white shadow-sm">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full flex items-center justify-between p-4 sm:p-5 bg-muted hover:bg-border-subtle transition-colors text-left"
      >
        <h3 className="text-lg font-semibold text-primary">{title}</h3>
        {isOpen ? <ChevronUp className="text-text-secondary" /> : <ChevronDown className="text-text-secondary" />}
      </button>
      {isOpen && (
        <div className="p-4 sm:p-5 border-t border-border-subtle bg-app/30">
          {children}
        </div>
      )}
    </div>
  );
}
