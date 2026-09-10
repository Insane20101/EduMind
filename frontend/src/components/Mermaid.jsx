import React, { useEffect, useRef, useState } from 'react';
import mermaid from 'mermaid';
import { 
  ZoomIn, 
  ZoomOut, 
  RotateCcw, 
  Maximize2, 
  X, 
  RefreshCw, 
  Code, 
  Move,
  AlertCircle
} from 'lucide-react';
import toast from 'react-hot-toast';

mermaid.initialize({
  startOnLoad: false,
  theme: 'neutral',
  themeVariables: {
    fontFamily: 'Inter, system-ui, sans-serif',
    darkMode: false,
    background: '#ffffff',
    primaryColor: '#ffffff',
    primaryTextColor: '#0f172a',
    primaryBorderColor: '#334155',
    lineColor: '#334155',
    secondaryColor: '#f8fafc',
    tertiaryColor: '#ffffff',
    nodeTextColor: '#0f172a',
    mainBkg: '#ffffff',
    clusterBkg: '#f8fafc',
    clusterBorder: '#cbd5e1',
    titleColor: '#0f172a',
    edgeLabelBackground: '#ffffff',
  },
  flowchart: {
    htmlLabels: false,
    curve: 'basis',
    useMaxWidth: true,
    padding: 25
  },
  securityLevel: 'loose',
});

function sanitizeMermaidChart(rawChart) {
  if (!rawChart) return '';
  let chart = String(rawChart).trim();

  chart = chart.replace(/^```(?:mermaid)?/i, '').replace(/```$/, '').trim();

  chart = chart
    .replace(/&gt;/g, '>')
    .replace(/&lt;/g, '<')
    .replace(/&amp;/g, '&')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'");

  const lines = chart.split('\n');
  const processedLines = [];

  for (let line of lines) {
    let trimmed = line.trim();
    if (!trimmed) continue;

    const quoteCount = (trimmed.match(/"/g) || []).length;
    if (quoteCount % 2 !== 0) {
      trimmed += '"';
    }

    processedLines.push(trimmed);
  }

  let result = processedLines.join('\n').trim();

  const headerKeywords = [
    'flowchart', 'graph', 'sequenceDiagram', 'classDiagram', 
    'stateDiagram', 'erDiagram', 'gantt', 'pie', 'gitGraph', 
    'mindmap', 'quadrantChart', 'timeline', 'sankey', 'kanban', 'architecture'
  ];
  const firstWord = result.split(/\s+/)[0];
  if (!headerKeywords.some(kw => firstWord && firstWord.toLowerCase().startsWith(kw.toLowerCase()))) {
    result = `flowchart TD\n${result}`;
  }

  return result;
}

export default function Mermaid({ chart }) {
  const containerRef = useRef(null);
  const modalContainerRef = useRef(null);
  const lastValidSvgRef = useRef('');

  const [hasError, setHasError] = useState(false);
  const [isRendered, setIsRendered] = useState(false);
  const [isRendering, setIsRendering] = useState(true);
  const [renderKey, setRenderKey] = useState(0);
  const [showCode, setShowCode] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);

  // Zoom & Pan state for Fullscreen Modal
  const [zoom, setZoom] = useState(1);
  const [pan, setPan] = useState({ x: 0, y: 0 });
  const [isDragging, setIsDragging] = useState(false);
  const [dragStart, setDragStart] = useState({ x: 0, y: 0 });

  const applyUnfilledLightStyles = (container) => {
    if (!container) return;
    const svgEl = container.querySelector('svg');
    if (!svgEl) return;

    svgEl.style.maxWidth = '100%';
    svgEl.style.height = 'auto';
    svgEl.style.margin = '0 auto';
    svgEl.style.padding = '16px';
    svgEl.style.background = '#ffffff';
    svgEl.style.overflow = 'visible';

    // Expand viewBox padding so top & side nodes are NEVER clipped
    const currentViewBox = svgEl.getAttribute('viewBox');
    if (currentViewBox) {
      const parts = currentViewBox.split(/[\s,]+/).map(Number);
      if (parts.length === 4 && !parts.some(isNaN)) {
        const [x, y, w, h] = parts;
        svgEl.setAttribute('viewBox', `${x - 18} ${y - 18} ${w + 36} ${h + 36}`);
      }
    }

    // Node rect width adjustments & styling
    const nodeGroups = svgEl.querySelectorAll('.node');
    nodeGroups.forEach((nodeG) => {
      const rect = nodeG.querySelector('rect');
      if (rect) {
        const w = parseFloat(rect.getAttribute('width'));
        const x = parseFloat(rect.getAttribute('x'));
        if (!isNaN(w) && !isNaN(x) && w > 0) {
          rect.setAttribute('width', (w + 28).toString());
          rect.setAttribute('x', (x - 14).toString());
        }
      }
    });

    const nodeShapes = svgEl.querySelectorAll('.node rect, .node circle, .node polygon, .node ellipse, .node path, rect.basic, .label-container');
    nodeShapes.forEach((shape) => {
      shape.style.setProperty('fill', '#ffffff', 'important');
      shape.style.setProperty('fill-opacity', '1', 'important');
      shape.style.setProperty('stroke', '#1e293b', 'important');
      shape.style.setProperty('stroke-width', '2px', 'important');
      shape.setAttribute('fill', '#ffffff');
      shape.setAttribute('stroke', '#1e293b');
    });

    const nodeTexts = svgEl.querySelectorAll('.node text, .node tspan, .node span, .node div, .label text, .label tspan');
    nodeTexts.forEach((txt) => {
      txt.style.setProperty('fill', '#0f172a', 'important');
      txt.style.setProperty('color', '#0f172a', 'important');
      txt.style.setProperty('font-weight', '600', 'important');
      txt.style.setProperty('font-size', '13px', 'important');
      txt.style.setProperty('letter-spacing', '0.01em', 'important');
      txt.setAttribute('fill', '#0f172a');
    });

    const edgeLabelRects = svgEl.querySelectorAll('.edgeLabel rect, .edgeLabel polygon, rect.bg');
    edgeLabelRects.forEach((rect) => {
      rect.style.setProperty('fill', '#ffffff', 'important');
      rect.style.setProperty('fill-opacity', '0.95', 'important');
      rect.style.setProperty('stroke', '#cbd5e1', 'important');
      rect.style.setProperty('stroke-width', '1px', 'important');
      rect.setAttribute('fill', '#ffffff');
      rect.setAttribute('stroke', '#cbd5e1');
    });

    const edgeLabelTexts = svgEl.querySelectorAll('.edgeLabel text, .edgeLabel tspan, .edgeLabel span, .edgeLabel div');
    edgeLabelTexts.forEach((txt) => {
      txt.style.setProperty('fill', '#0f172a', 'important');
      txt.style.setProperty('color', '#0f172a', 'important');
      txt.style.setProperty('font-weight', '600', 'important');
      txt.style.setProperty('font-size', '11px', 'important');
      txt.setAttribute('fill', '#0f172a');
    });

    const edgePaths = svgEl.querySelectorAll('.edgePath path, .edgePath line, path.path');
    edgePaths.forEach((path) => {
      path.style.setProperty('stroke', '#334155', 'important');
      path.style.setProperty('stroke-width', '2px', 'important');
    });

    const markers = svgEl.querySelectorAll('.marker path, marker path, .marker');
    markers.forEach((m) => {
      m.style.setProperty('fill', '#334155', 'important');
      m.style.setProperty('stroke', '#334155', 'important');
      m.setAttribute('fill', '#334155');
    });
  };

  const renderDiagram = () => {
    if (!chart) return;
    setIsRendering(true);
    const cleaned = sanitizeMermaidChart(chart);

    const id = `mermaid-svg-${Math.floor(Math.random() * 10000000)}`;

    mermaid.render(id, cleaned)
      .then((res) => {
        lastValidSvgRef.current = res.svg;
        setHasError(false);
        setIsRendered(true);
        setIsRendering(false);
        if (containerRef.current) {
          containerRef.current.innerHTML = res.svg;
          applyUnfilledLightStyles(containerRef.current);
        }
      })
      .catch(() => {
        const errEl = document.getElementById(`d${id}`) || document.getElementById(id);
        if (errEl) errEl.remove();

        const fallbackCode = cleaned.replace(/\["([^"]*)"\]/g, (m, txt) => `["${txt.replace(/[:;,{}()]/g, ' ')}"]`);
        const fallbackId = `mermaid-fallback-${Math.floor(Math.random() * 10000000)}`;

        mermaid.render(fallbackId, fallbackCode)
          .then((res2) => {
            lastValidSvgRef.current = res2.svg;
            setHasError(false);
            setIsRendered(true);
            setIsRendering(false);
            if (containerRef.current) {
              containerRef.current.innerHTML = res2.svg;
              applyUnfilledLightStyles(containerRef.current);
            }
          })
          .catch(() => {
            const errEl2 = document.getElementById(`d${fallbackId}`) || document.getElementById(fallbackId);
            if (errEl2) errEl2.remove();

            setIsRendering(false);
            if (!lastValidSvgRef.current) {
              setHasError(true);
              setIsRendered(false);
            }
          });
      });
  };

  useEffect(() => {
    renderDiagram();
  }, [chart, renderKey]);

  // Re-render trigger
  const handleRetry = (e) => {
    e?.stopPropagation();
    setHasError(false);
    setIsRendered(false);
    setIsRendering(true);
    setRenderKey(k => k + 1);
    toast.success("Re-rendering diagram...", { id: "mermaid-retry" });
  };

  // Open Fullscreen Modal
  const openModal = (e) => {
    e?.stopPropagation();
    if (!lastValidSvgRef.current && !containerRef.current?.innerHTML) return;
    setIsModalOpen(true);
    setZoom(1);
    setPan({ x: 0, y: 0 });
  };

  // Populate Modal SVG when opened
  useEffect(() => {
    if (isModalOpen && modalContainerRef.current) {
      modalContainerRef.current.innerHTML = lastValidSvgRef.current || containerRef.current?.innerHTML || '';
      applyUnfilledLightStyles(modalContainerRef.current);
    }
  }, [isModalOpen]);

  // Handle ESC key to close modal
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape') setIsModalOpen(false);
    };
    if (isModalOpen) window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isModalOpen]);

  // Zoom & Pan Handlers for Modal
  const handleZoomIn = () => setZoom(z => Math.min(4.0, z + 0.25));
  const handleZoomOut = () => setZoom(z => Math.max(0.3, z - 0.25));
  const handleResetZoom = () => { setZoom(1); setPan({ x: 0, y: 0 }); };

  const handleWheel = (e) => {
    e.preventDefault();
    const zoomFactor = e.deltaY < 0 ? 1.15 : 0.87;
    setZoom(z => Math.min(4.0, Math.max(0.3, z * zoomFactor)));
  };

  const handleMouseDown = (e) => {
    setIsDragging(true);
    setDragStart({ x: e.clientX - pan.x, y: e.clientY - pan.y });
  };

  const handleMouseMove = (e) => {
    if (!isDragging) return;
    setPan({ x: e.clientX - dragStart.x, y: e.clientY - dragStart.y });
  };

  const handleMouseUp = () => setIsDragging(false);

  return (
    <>
      <div className="my-3 rounded-2xl border border-slate-200 bg-white shadow-sm hover:shadow-md transition-all overflow-hidden text-slate-900 group">
        {/* Header Bar */}
        <div className="px-3.5 py-2 bg-slate-50 border-b border-slate-200 flex items-center justify-between flex-wrap gap-2">
          <div className="flex items-center gap-2 text-indigo-700 font-bold text-[11px] uppercase tracking-wider">
            <span className="w-2 h-2 rounded-full bg-indigo-600 animate-pulse" />
            <span>📊 Flowchart / Process Diagram</span>
          </div>

          <div className="flex items-center gap-1.5">
            {/* Retry / Re-render Button */}
            <button
              type="button"
              onClick={handleRetry}
              className="flex items-center gap-1 px-2.5 py-1 text-xs font-semibold text-slate-600 hover:text-indigo-600 bg-white hover:bg-indigo-50 border border-slate-200 rounded-lg transition-all shadow-xs"
              title="Re-render Diagram"
            >
              <RefreshCw size={13} className={isRendering ? "animate-spin text-indigo-600" : ""} />
              <span>{isRendering ? "Rendering..." : "Re-render"}</span>
            </button>

            {/* View Fullscreen Modal */}
            {(isRendered || lastValidSvgRef.current) && (
              <button
                type="button"
                onClick={openModal}
                className="flex items-center gap-1 px-2.5 py-1 text-xs font-semibold text-indigo-700 hover:text-indigo-800 bg-indigo-50 hover:bg-indigo-100 border border-indigo-200 rounded-lg transition-all shadow-xs"
                title="Expand & Zoom Diagram"
              >
                <Maximize2 size={13} />
                <span>Fullscreen</span>
              </button>
            )}

            {/* View Raw Code Toggle */}
            <button
              type="button"
              onClick={() => setShowCode(!showCode)}
              className="p-1 text-slate-400 hover:text-slate-700 rounded-md transition-colors"
              title={showCode ? "Hide Code" : "View Code"}
            >
              <Code size={14} />
            </button>
          </div>
        </div>

        {/* Crisp White Render Area */}
        <div 
          className="p-4 flex flex-col items-center justify-center w-full bg-white relative min-h-[100px] cursor-zoom-in group/canvas"
          onClick={openModal}
        >
          {/* SVG Diagram Canvas */}
          <div 
            ref={containerRef} 
            className="mermaid-render-area w-full flex justify-center text-slate-900 [&_svg]:max-w-full [&_svg]:h-auto [&_svg]:bg-white" 
          />

          {/* Click to expand hover overlay badge */}
          {(isRendered || lastValidSvgRef.current) && (
            <div className="absolute top-3 right-3 opacity-0 group-hover/canvas:opacity-100 transition-opacity bg-slate-900/80 text-white text-[11px] font-medium px-2.5 py-1 rounded-full backdrop-blur-xs shadow-md pointer-events-none flex items-center gap-1.5">
              <Maximize2 size={12} />
              <span>Click to view large &amp; zoom</span>
            </div>
          )}

          {/* Rendering or Failed State Handling */}
          {!isRendered && (
            <div className="py-6 px-4 flex flex-col items-center justify-center text-center space-y-3">
              {isRendering ? (
                <div className="flex items-center gap-2 text-xs font-semibold text-indigo-600">
                  <RefreshCw size={14} className="animate-spin" />
                  <span>Rendering diagram...</span>
                </div>
              ) : hasError ? (
                <div className="bg-amber-50 border border-amber-200 rounded-xl p-4 max-w-md text-amber-900 space-y-2">
                  <div className="flex items-center justify-center gap-2 text-amber-700 font-bold text-xs">
                    <AlertCircle size={15} />
                    <span>Diagram Rendering Notice</span>
                  </div>
                  <p className="text-xs text-amber-800">
                    The diagram formatting was interrupted or incomplete. Click below to re-render.
                  </p>
                  <button
                    type="button"
                    onClick={handleRetry}
                    className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold text-white bg-indigo-600 hover:bg-indigo-700 rounded-lg shadow-sm transition-all"
                  >
                    <RefreshCw size={13} />
                    <span>Re-render Diagram</span>
                  </button>
                </div>
              ) : null}
            </div>
          )}

          {/* Raw Mermaid Syntax Collapsible View */}
          {showCode && (
            <div className="w-full mt-3 p-3 bg-slate-900 rounded-xl text-slate-200 font-mono text-xs overflow-x-auto border border-slate-800">
              <pre>{chart}</pre>
            </div>
          )}
        </div>
      </div>

      {/* ── Interactive Fullscreen / Large Screen Modal ───────────────────────── */}
      {isModalOpen && (
        <div 
          className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-md flex flex-col animate-in fade-in duration-200"
          onClick={() => setIsModalOpen(false)}
        >
          {/* Modal Top Control Bar */}
          <div 
            className="flex items-center justify-between px-6 py-4 bg-slate-900/90 border-b border-slate-800 text-white z-10"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-center gap-3">
              <span className="w-2.5 h-2.5 rounded-full bg-indigo-500 animate-pulse" />
              <div>
                <h4 className="text-sm font-bold text-slate-100">Flowchart &amp; Diagram Inspector</h4>
                <p className="text-xs text-slate-400">Use mouse wheel to zoom • Click &amp; drag to pan across screen</p>
              </div>
            </div>

            {/* Controls Bar */}
            <div className="flex items-center gap-2">
              <span className="text-xs font-mono font-bold text-indigo-300 bg-indigo-950/80 border border-indigo-800 px-3 py-1 rounded-lg">
                {Math.round(zoom * 100)}%
              </span>

              <button
                type="button"
                onClick={handleZoomIn}
                className="p-2 text-slate-300 hover:text-white bg-slate-800 hover:bg-slate-700 rounded-lg transition-colors border border-slate-700"
                title="Zoom In (+25%)"
              >
                <ZoomIn size={16} />
              </button>

              <button
                type="button"
                onClick={handleZoomOut}
                className="p-2 text-slate-300 hover:text-white bg-slate-800 hover:bg-slate-700 rounded-lg transition-colors border border-slate-700"
                title="Zoom Out (-25%)"
              >
                <ZoomOut size={16} />
              </button>

              <button
                type="button"
                onClick={handleResetZoom}
                className="p-2 text-slate-300 hover:text-white bg-slate-800 hover:bg-slate-700 rounded-lg transition-colors border border-slate-700"
                title="Reset Zoom & Position"
              >
                <RotateCcw size={16} />
              </button>

              <div className="h-5 w-px bg-slate-800 mx-1" />

              <button
                type="button"
                onClick={() => setIsModalOpen(false)}
                className="p-2 text-slate-400 hover:text-white hover:bg-rose-500/20 hover:border-rose-500/40 rounded-lg transition-colors border border-slate-700"
                title="Close Fullscreen (Esc)"
              >
                <X size={18} />
              </button>
            </div>
          </div>

          {/* Interactive Zoomable & Pannable Canvas Container */}
          <div 
            className="flex-1 w-full h-full overflow-hidden flex items-center justify-center p-8 select-none relative cursor-grab active:cursor-grabbing bg-slate-900/50"
            onClick={(e) => e.stopPropagation()}
            onWheel={handleWheel}
            onMouseDown={handleMouseDown}
            onMouseMove={handleMouseMove}
            onMouseUp={handleMouseUp}
            onMouseLeave={handleMouseUp}
          >
            <div 
              className="transition-transform duration-75 ease-out flex items-center justify-center"
              style={{
                transform: `translate(${pan.x}px, ${pan.y}px) scale(${zoom})`,
                transformOrigin: 'center center'
              }}
            >
              <div 
                ref={modalContainerRef} 
                className="bg-white p-8 rounded-2xl shadow-2xl border border-slate-200 max-w-none [&_svg]:max-w-none [&_svg]:bg-white"
              />
            </div>

            {/* Floating Navigation Hint */}
            <div className="absolute bottom-4 left-1/2 -translate-x-1/2 bg-slate-950/80 border border-slate-800 text-slate-400 text-xs px-4 py-1.5 rounded-full backdrop-blur-md flex items-center gap-2 pointer-events-none shadow-lg">
              <Move size={14} className="text-indigo-400" />
              <span>Drag to Pan • Mouse Wheel to Zoom</span>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
