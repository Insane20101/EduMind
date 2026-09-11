import React, { useEffect, useRef, useState } from 'react';
import mermaid from 'mermaid';
import { Maximize2, Minimize2, ZoomIn, ZoomOut, RotateCcw } from 'lucide-react';

mermaid.initialize({
  startOnLoad: false,
  theme: 'dark',
  securityLevel: 'loose',
  fontFamily: 'Inter, sans-serif'
});

export default function MermaidViewer({ chartCode, title = "Diagram View" }) {
  const containerRef = useRef(null);
  const [svgContent, setSvgContent] = useState('');
  const [isFullScreen, setIsFullScreen] = useState(false);
  const [zoomScale, setZoomScale] = useState(1.0);
  const [parseError, setParseError] = useState(null);

  useEffect(() => {
    if (!chartCode) return;
    let isMounted = true;
    const renderDiagram = async () => {
      try {
        setParseError(null);
        const uniqueId = `mermaid-${Math.random().toString(36).substring(2, 9)}`;
        const { svg } = await mermaid.render(uniqueId, chartCode.strip ? chartCode.strip() : chartCode);
        if (isMounted) {
          setSvgContent(svg);
        }
      } catch (err) {
        if (isMounted) {
          console.warn("Mermaid render error:", err);
          setParseError("Unable to render visual diagram for this step.");
        }
      }
    };

    renderDiagram();
    return () => { isMounted = false; };
  }, [chartCode]);

  const handleZoomIn = (e) => {
    e.stopPropagation();
    setZoomScale(prev => Math.min(prev * 1.15, 2.5));
  };

  const handleZoomOut = (e) => {
    e.stopPropagation();
    setZoomScale(prev => Math.max(prev / 1.15, 0.5));
  };

  const handleResetZoom = (e) => {
    e.stopPropagation();
    setZoomScale(1.0);
  };

  const toggleFullScreen = () => {
    setIsFullScreen(!isFullScreen);
    setZoomScale(1.0);
  };

  return (
    <div className={`relative my-4 rounded-xl border border-slate-700/60 bg-slate-950/80 p-4 shadow-xl transition-all ${isFullScreen ? 'fixed inset-4 z-50 flex flex-col bg-slate-950 p-6' : 'max-h-[420px] overflow-hidden'}`}>
      
      {/* Header Toolbar */}
      <div className="mb-3 flex items-center justify-between border-b border-slate-800 pb-2">
        <span className="text-xs font-semibold uppercase tracking-wider text-cyan-400 flex items-center gap-2">
          <span className="h-2 w-2 rounded-full bg-cyan-400 animate-pulse" />
          {title}
        </span>
        <div className="flex items-center gap-1.5 bg-slate-900/90 rounded-lg p-1 border border-slate-800">
          <button
            onClick={handleZoomIn}
            title="Zoom In"
            className="p-1 text-slate-400 hover:text-white hover:bg-slate-800 rounded transition"
          >
            <ZoomIn className="w-4 h-4" />
          </button>
          <button
            onClick={handleZoomOut}
            title="Zoom Out"
            className="p-1 text-slate-400 hover:text-white hover:bg-slate-800 rounded transition"
          >
            <ZoomOut className="w-4 h-4" />
          </button>
          <button
            onClick={handleResetZoom}
            title="Reset Scale"
            className="p-1 text-slate-400 hover:text-white hover:bg-slate-800 rounded transition"
          >
            <RotateCcw className="w-3.5 h-3.5" />
          </button>
          <div className="h-4 w-px bg-slate-800 mx-0.5" />
          <button
            onClick={toggleFullScreen}
            title={isFullScreen ? "Exit Fullscreen" : "Full Screen View"}
            className="p-1 text-cyan-400 hover:bg-cyan-950/50 rounded transition flex items-center gap-1 text-xs font-medium px-2"
          >
            {isFullScreen ? <Minimize2 className="w-4 h-4" /> : <Maximize2 className="w-4 h-4" />}
            <span className="hidden sm:inline">{isFullScreen ? "Close" : "Expand"}</span>
          </button>
        </div>
      </div>

      {/* Render Canvas */}
      <div className={`overflow-auto flex-1 flex items-center justify-center p-2 transition-transform duration-150 ${isFullScreen ? 'min-h-[80vh]' : 'min-h-[220px]'}`}>
        {parseError ? (
          <div className="text-xs text-amber-400/80 bg-amber-950/20 border border-amber-800/40 rounded-lg p-3 text-center">
            {parseError}
          </div>
        ) : (
          <div
            ref={containerRef}
            style={{ transform: `scale(${zoomScale})`, transformOrigin: 'center center' }}
            className="transition-transform duration-200 ease-out"
            dangerouslySetInnerHTML={{ __html: svgContent }}
          />
        )}
      </div>

    </div>
  );
}
