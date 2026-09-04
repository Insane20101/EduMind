import React from 'react';

export default function EduMindLogo({ size = 32, showText = true, textClass = "text-xl font-bold tracking-tight text-slate-900" }) {
  return (
    <div className="flex items-center gap-2.5 select-none group">
      <div 
        className="relative flex items-center justify-center rounded-xl bg-gradient-to-br from-indigo-600 via-indigo-500 to-violet-600 shadow-md shadow-indigo-500/20 group-hover:scale-105 transition-transform duration-200"
        style={{ width: `${size}px`, height: `${size}px` }}
      >
        {/* Subtle SVG Glow effect */}
        <svg 
          viewBox="0 0 512 512" 
          fill="none" 
          xmlns="http://www.w3.org/2000/svg"
          className="w-full h-full p-1.5 text-white"
        >
          {/* Graduation Mortarboard Cap */}
          <polygon points="256,120 420,190 256,260 92,190" fill="#ffffff" />
          <polygon points="256,260 420,190 256,210 92,190" fill="#38bdf8" opacity="0.5" />
          <path d="M148 224 V275 C148 315 200 345 256 345 C312 345 364 315 364 275 V224 L256 270 Z" fill="#f8fafc" />
          <path d="M390 205 L390 295 C390 315 380 330 370 340" stroke="#fbbf24" strokeWidth="16" strokeLinecap="round" fill="none" />
          <circle cx="390" cy="205" r="12" fill="#f59e0b" />
          
          {/* AI Sparkle Star */}
          <path d="M256 360 Q256 400 235 410 Q256 420 256 460 Q256 420 277 410 Q256 400 256 360 Z" fill="#38bdf8" />
          <path d="M360 110 Q360 130 350 135 Q360 140 360 160 Q360 140 370 135 Q360 130 360 110 Z" fill="#fbbf24" />
        </svg>
      </div>

      {showText && (
        <span className={`${textClass} flex items-center`}>
          <span>Edu</span>
          <span className="text-indigo-600 font-extrabold">Mind</span>
          <span className="ml-1 px-1.5 py-0.5 text-[10px] uppercase font-bold tracking-wider rounded-md bg-indigo-50 text-indigo-700 border border-indigo-200/60 hidden sm:inline-block">
            AI
          </span>
        </span>
      )}
    </div>
  );
}
