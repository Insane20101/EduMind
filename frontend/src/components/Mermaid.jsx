import React, { useEffect, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
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
    padding: 20
  },
  securityLevel: 'loose',
});

function sanitizeMermaidChart(rawChart) {
  if (!rawChart) return '';
  let chart = String(rawChart).trim();

  // Strip markdown fences
  chart = chart.replace(/^```(?:mermaid)?/i, '').replace(/```$/, '').trim();

  // HTML entities
  chart = chart
    .replace(/&gt;/g, '>')
    .replace(/&lt;/g, '<')
    .replace(/&amp;/g, '&')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'");

  // Ensure unquoted brackets are safely quoted: Node[Label (e.g. text)] -> Node["Label (e.g. text)"]
  chart = chart.replace(/([A-Za-z0-9_]+)\[([^"\]\n]+)\]/g, (m, id, label) => {
    const cleanLabel = label.replace(/"/g, "'").trim();
    return `${id}["${cleanLabel}"]`;
  });

  // Ensure unquoted parentheses are safely quoted: Node(Label text) -> Node(["Label text"])
  chart = chart.replace(/([A-Za-z0-9_]+)\(([^"\)\n]+)\)/g, (m, id, label) => {
    const cleanLabel = label.replace(/"/g, "'").trim();
    return `${id}(["${cleanLabel}"])`;
  });

  // Strip markdown bold/italics inside node labels
  chart = chart.replace(/\["([^"]*)"\]/g, (m, txt) => {
    return `["${txt.replace(/\*\*/g, '').replace(/\*/g, '')}"]`;
  });

  const lines = chart.split('\n');
  const processedLines = [];

  for (let line of lines) {
    let trimmed = line.trim();
    if (!trimmed) continue;

    // Balance odd quotes on individual lines
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

function repairMermaidSyntax(rawCode) {
  if (!rawCode) return 'flowchart TD\n  Start["Select Course Subject"] --> Explore["Explore Syllabus & Notes"] --> Ask["Ask AI Academic Questions"]';
  
  const lines = String(rawCode).split('\n');
  const edgeLines = [];
  const extractedNodes = new Map();
  let nodeCounter = 1;

  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed) continue;
    if (trimmed.startsWith('flowchart') || trimmed.startsWith('graph') || trimmed.startsWith('subgraph') || trimmed === 'end') continue;

    if (trimmed.includes('-->') || trimmed.includes('---') || trimmed.includes('==>')) {
      const parts = trimmed.split(/\s*-->\s*|\s*---\s*|\s*==>\s*/);
      if (parts.length >= 2) {
        const stepIds = [];
        for (const p of parts) {
          const nodeMatch = p.match(/([A-Za-z0-9_]+)(?:\["?([^"\]]*)"?\]|\("?([^"\)]*)"?\)|\(\["?([^"\]]*)"?\]\))?/);
          if (nodeMatch) {
            const rawId = nodeMatch[1] || `Node${nodeCounter++}`;
            const cleanId = rawId.replace(/[^A-Za-z0-9_]/g, '') || `N${nodeCounter++}`;
            const label = (nodeMatch[2] || nodeMatch[3] || nodeMatch[4] || cleanId).replace(/["`]/g, '').trim();
            extractedNodes.set(cleanId, label.slice(0, 45) || cleanId);
            stepIds.push(cleanId);
          }
        }
        if (stepIds.length >= 2) {
          for (let i = 0; i < stepIds.length - 1; i++) {
            edgeLines.push(`  ${stepIds[i]} --> ${stepIds[i + 1]}`);
          }
        }
      }
    }
  }

  if (edgeLines.length > 0 && extractedNodes.size > 0) {
    let repaired = 'flowchart TD\n';
    extractedNodes.forEach((label, id) => {
      repaired += `  ${id}["${label}"]\n`;
    });
    repaired += edgeLines.join('\n');
    return repaired;
  }

  const phrases = lines
    .map(l => l.replace(/[^A-Za-z0-9\s]/g, ' ').trim())
    .filter(l => l.length > 3 && l.length < 50 && !l.toLowerCase().startsWith('flowchart') && !l.toLowerCase().startsWith('graph'))
    .slice(0, 4);

  if (phrases.length >= 2) {
    let repaired = 'flowchart TD\n';
    phrases.forEach((phrase, idx) => {
      repaired += `  Step${idx + 1}["${phrase}"]\n`;
      if (idx > 0) {
        repaired += `  Step${idx} --> Step${idx + 1}\n`;
      }
    });
    return repaired;
  }

  return 'flowchart TD\n  Start["Select Course Subject"] --> Explore["Explore Syllabus & Notes"] --> Ask["Ask AI Academic Questions"]';
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

  const applyUnfilledLightStyles = (container, isModal = false) => {
    if (!container) return;
    const svgEl = container.querySelector('svg');
    if (!svgEl) return;

    svgEl.style.maxWidth = '100%';
    svgEl.style.margin = '0 auto';
    svgEl.style.padding = '8px';
    svgEl.style.background = '#ffffff';
    svgEl.style.overflow = 'visible';
    svgEl.style.boxSizing = 'border-box';
    svgEl.setAttribute('preserveAspectRatio', 'xMidYMid meet');

    if (isModal) {
      svgEl.style.maxHeight = '65vh';
      svgEl.style.maxWidth = '80vw';
      svgEl.style.width = 'auto';
      svgEl.style.height = 'auto';
    } else {
      svgEl.style.maxHeight = '340px';
      svgEl.style.width = '100%';
      svgEl.style.height = 'auto';
    }

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
          rect.setAttribute('width', (w + 24).toString());
          rect.setAttribute('x', (x - 12).toString());
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

  const renderDiagram = (isRetry = false) => {
    if (!chart) return;
    setIsRendering(true);
    setHasError(false);

    // If retry is explicitly requested, attempt auto-repaired syntax directly
    const cleaned = isRetry ? repairMermaidSyntax(chart) : sanitizeMermaidChart(chart);
    const id = `mermaid-svg-${Math.floor(Math.random() * 10000000)}`;

    mermaid.render(id, cleaned)
      .then((res) => {
        lastValidSvgRef.current = res.svg;
        setHasError(false);
        setIsRendered(true);
        setIsRendering(false);
        if (containerRef.current) {
          containerRef.current.innerHTML = res.svg;
          applyUnfilledLightStyles(containerRef.current, false);
        }
      })
      .catch(() => {
        const errEl = document.getElementById(`d${id}`) || document.getElementById(id);
        if (errEl) errEl.remove();

        // Stage 2: Relaxed character replacement fallback
        const fallbackCode = cleaned
          .replace(/\["([^"]*)"\]/g, (m, txt) => `["${txt.replace(/[:;,{}()&/\\]/g, ' ').trim()}"]`)
          .replace(/\(([^)]*)\)/g, (m, txt) => `(["${txt.replace(/[:;,{}()&/\\]/g, ' ').trim()}"])`);
        const fallbackId = `mermaid-fallback-${Math.floor(Math.random() * 10000000)}`;

        mermaid.render(fallbackId, fallbackCode)
          .then((res2) => {
            lastValidSvgRef.current = res2.svg;
            setHasError(false);
            setIsRendered(true);
            setIsRendering(false);
            if (containerRef.current) {
              containerRef.current.innerHTML = res2.svg;
              applyUnfilledLightStyles(containerRef.current, false);
            }
          })
          .catch(() => {
            const errEl2 = document.getElementById(`d${fallbackId}`) || document.getElementById(fallbackId);
            if (errEl2) errEl2.remove();

            // Stage 3: Guaranteed Synthesizer Repair
            const repairedCode = repairMermaidSyntax(chart);
            const repairId = `mermaid-repair-${Math.floor(Math.random() * 10000000)}`;

            mermaid.render(repairId, repairedCode)
              .then((res3) => {
                lastValidSvgRef.current = res3.svg;
                setHasError(false);
                setIsRendered(true);
                setIsRendering(false);
                if (containerRef.current) {
                  containerRef.current.innerHTML = res3.svg;
                  applyUnfilledLightStyles(containerRef.current, false);
                }
              })
              .catch(() => {
                const errEl3 = document.getElementById(`d${repairId}`) || document.getElementById(repairId);
                if (errEl3) errEl3.remove();

                setIsRendering(false);
                if (!lastValidSvgRef.current) {
                  setHasError(true);
                  setIsRendered(false);
                }
              });
          });
      });
  };

  useEffect(() => {
    renderDiagram(renderKey > 0);
  }, [chart, renderKey]);

  // Re-render trigger
  const handleRetry = (e) => {
    e?.stopPropagation();
    setHasError(false);
    setIsRendered(false);
    setIsRendering(true);
    setRenderKey(k => k + 1);
    toast.success("Repairing and re-rendering diagram...", { id: "mermaid-retry" });
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
      applyUnfilledLightStyles(modalContainerRef.current, true);
    }
  }, [isModalOpen]);

  // Handle ESC key & keyboard zoom shortcuts
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (!isModalOpen) return;
      if (e.key === 'Escape') setIsModalOpen(false);
      if (e.key === '+' || e.key === '=') setZoom(z => Math.min(4.0, z + 0.15));
      if (e.key === '-') setZoom(z => Math.max(0.3, z - 0.15));
      if (e.key === '0' || e.key === 'r') { setZoom(1); setPan({ x: 0, y: 0 }); }
    };
    if (isModalOpen) window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isModalOpen]);

  // Zoom & Pan Handlers for Modal - Relaxed smooth wheel sensitivity (1.06 factor)
  const handleZoomIn = () => setZoom(z => Math.min(4.0, z + 0.20));
  const handleZoomOut = () => setZoom(z => Math.max(0.3, z - 0.20));
  const handleResetZoom = () => { setZoom(1); setPan({ x: 0, y: 0 }); };

  const handleWheel = (e) => {
    e.preventDefault();
    const zoomFactor = e.deltaY < 0 ? 1.06 : 0.94;
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
      <div className="my-2.5 w-full max-w-full rounded-xl sm:rounded-2xl border border-slate-200 bg-white shadow-xs hover:shadow-sm transition-all overflow-hidden text-slate-900 group box-border">
        {/* Responsive Header Bar */}
        <div className="px-2.5 sm:px-3.5 py-1.5 sm:py-2 bg-slate-50 border-b border-slate-200 flex items-center justify-between gap-1.5 w-full min-w-0 box-border">
          <div className="flex items-center gap-1.5 text-indigo-700 font-bold text-[10px] sm:text-[11px] uppercase tracking-wider min-w-0 truncate">
            <span className="w-1.5 h-1.5 sm:w-2 sm:h-2 rounded-full bg-indigo-600 animate-pulse shrink-0" />
            <span className="truncate">📊 Flowchart</span>
          </div>

          <div className="flex items-center gap-1 shrink-0">
            {/* Retry / Re-render Button */}
            <button
              type="button"
              onClick={handleRetry}
              className="flex items-center gap-1 px-2 py-0.5 sm:px-2.5 sm:py-1 text-[11px] sm:text-xs font-semibold text-slate-600 hover:text-indigo-600 bg-white hover:bg-indigo-50 border border-slate-200 rounded-lg transition-all shadow-2xs"
              title="Re-render Diagram"
            >
              <RefreshCw size={12} className={isRendering ? "animate-spin text-indigo-600" : ""} />
              <span className="hidden xs:inline">{isRendering ? "Rendering..." : "Re-render"}</span>
            </button>

            {/* View Fullscreen Modal */}
            {(isRendered || lastValidSvgRef.current) && (
              <button
                type="button"
                onClick={openModal}
                className="flex items-center gap-1 px-2 py-0.5 sm:px-2.5 sm:py-1 text-[11px] sm:text-xs font-semibold text-indigo-700 hover:text-indigo-800 bg-indigo-50 hover:bg-indigo-100 border border-indigo-200 rounded-lg transition-all shadow-2xs"
                title="Expand & Zoom Diagram"
              >
                <Maximize2 size={12} />
                <span className="hidden xs:inline">Fullscreen</span>
              </button>
            )}

            {/* View Raw Code Toggle */}
            <button
              type="button"
              onClick={() => setShowCode(!showCode)}
              className="p-1 text-slate-400 hover:text-slate-700 rounded-md transition-colors"
              title={showCode ? "Hide Code" : "View Code"}
            >
              <Code size={13} />
            </button>
          </div>
        </div>

        {/* Crisp White Render Area */}
        <div 
          className="p-2 sm:p-3 flex flex-col items-center justify-center w-full max-w-full bg-white relative min-h-[90px] max-h-[380px] overflow-hidden cursor-zoom-in group/canvas box-border"
          onClick={openModal}
        >
          {/* SVG Diagram Canvas */}
          <div 
            ref={containerRef} 
            className="mermaid-render-area w-full max-w-full overflow-x-auto overflow-y-hidden flex justify-center text-slate-900 [&_svg]:max-h-[340px] [&_svg]:max-w-full [&_svg]:w-full [&_svg]:h-auto [&_svg]:bg-white" 
          />

          {/* Click to expand hover overlay badge */}
          {(isRendered || lastValidSvgRef.current) && (
            <div className="absolute top-2.5 right-2.5 opacity-0 group-hover/canvas:opacity-100 transition-opacity bg-slate-900/80 text-white text-[10px] sm:text-[11px] font-medium px-2 py-0.5 sm:px-2.5 sm:py-1 rounded-full backdrop-blur-xs shadow-md pointer-events-none flex items-center gap-1">
              <Maximize2 size={11} />
              <span>Click to zoom</span>
            </div>
          )}

          {/* Rendering or Failed State Handling - Guaranteed 100% Responsive */}
          {!isRendered && (
            <div className="py-4 px-2 sm:px-4 flex flex-col items-center justify-center text-center space-y-2.5 w-full max-w-full min-w-0 box-border">
              {isRendering ? (
                <div className="flex items-center justify-center gap-2 text-xs font-semibold text-indigo-600 py-3">
                  <RefreshCw size={14} className="animate-spin" />
                  <span>Rendering diagram...</span>
                </div>
              ) : hasError ? (
                <div className="w-full max-w-full box-border bg-amber-50/90 border border-amber-200/90 rounded-xl p-3 sm:p-4 text-amber-900 space-y-2 text-center">
                  <div className="flex items-center justify-center gap-1.5 text-amber-700 font-bold text-xs">
                    <AlertCircle size={14} className="shrink-0" />
                    <span>Diagram Rendering Notice</span>
                  </div>
                  <p className="text-[11px] sm:text-xs text-amber-800 leading-relaxed break-words max-w-xs mx-auto">
                    The diagram formatting was interrupted or incomplete. Click below to repair.
                  </p>
                  <button
                    type="button"
                    onClick={handleRetry}
                    className="inline-flex items-center justify-center gap-1.5 px-3 py-1.5 text-xs font-semibold text-white bg-indigo-600 hover:bg-indigo-700 rounded-lg shadow-xs transition-all mx-auto active:scale-95"
                  >
                    <RefreshCw size={12} className={isRendering ? "animate-spin" : ""} />
                    <span>{isRendering ? "Repairing..." : "Re-render Diagram"}</span>
                  </button>
                </div>
              ) : null}
            </div>
          )}

          {/* Raw Mermaid Syntax Collapsible View */}
          {showCode && (
            <div className="w-full max-w-full mt-2.5 p-2.5 sm:p-3 bg-slate-900 rounded-xl text-slate-200 font-mono text-[11px] sm:text-xs overflow-x-auto border border-slate-800 box-border">
              <pre className="whitespace-pre-wrap break-words">{chart}</pre>
            </div>
          )}
        </div>
      </div>

      {/* ── Interactive Fullscreen / Large Screen Modal (Portal to body for guaranteed full screen visibility) ── */}
      {isModalOpen && createPortal(
        <div 
          className="fixed inset-0 z-[99999] bg-slate-950/90 backdrop-blur-md flex flex-col animate-in fade-in duration-200"
          onClick={() => setIsModalOpen(false)}
        >
          {/* Modal Top Control Bar - Guaranteed 100% visible on all viewports */}
          <div 
            className="flex items-center justify-between px-4 sm:px-6 py-3 bg-slate-900/95 border-b border-slate-800 text-white z-50 shrink-0 gap-2 flex-wrap sm:flex-nowrap"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-center gap-2.5 min-w-0 flex-1">
              <span className="w-2.5 h-2.5 rounded-full bg-indigo-500 animate-pulse shrink-0" />
              <div className="min-w-0">
                <h4 className="text-xs sm:text-sm font-bold text-slate-100 truncate">Flowchart &amp; Diagram Inspector</h4>
                <p className="text-[10px] sm:text-xs text-slate-400 truncate hidden sm:block">
                  Use mouse wheel to zoom • Click &amp; drag to pan across screen
                </p>
              </div>
            </div>

            {/* Controls Bar - Always visible, never cut off */}
            <div className="flex items-center gap-1.5 sm:gap-2 shrink-0">
              <span className="text-[11px] sm:text-xs font-mono font-bold text-indigo-300 bg-indigo-950/80 border border-indigo-800/80 px-2 py-0.5 sm:px-2.5 sm:py-1 rounded-lg">
                {Math.round(zoom * 100)}%
              </span>

              <button
                type="button"
                onClick={handleZoomIn}
                className="p-1.5 sm:p-2 text-slate-300 hover:text-white bg-slate-800 hover:bg-slate-700 rounded-lg transition-colors border border-slate-700"
                title="Zoom In (+20%)"
              >
                <ZoomIn size={15} />
              </button>

              <button
                type="button"
                onClick={handleZoomOut}
                className="p-1.5 sm:p-2 text-slate-300 hover:text-white bg-slate-800 hover:bg-slate-700 rounded-lg transition-colors border border-slate-700"
                title="Zoom Out (-20%)"
              >
                <ZoomOut size={15} />
              </button>

              <button
                type="button"
                onClick={handleResetZoom}
                className="p-1.5 sm:p-2 text-slate-300 hover:text-white bg-slate-800 hover:bg-slate-700 rounded-lg transition-colors border border-slate-700"
                title="Reset Zoom & Position"
              >
                <RotateCcw size={15} />
              </button>

              <div className="h-4 w-px bg-slate-800 mx-0.5" />

              <button
                type="button"
                onClick={() => setIsModalOpen(false)}
                className="p-1.5 sm:p-2 text-slate-300 hover:text-white bg-rose-500/20 hover:bg-rose-500/30 text-rose-300 border border-rose-500/40 rounded-lg transition-colors"
                title="Close Fullscreen (Esc)"
              >
                <X size={17} />
              </button>
            </div>
          </div>

          {/* Interactive Zoomable & Pannable Canvas Container */}
          <div 
            className="flex-1 w-full h-full overflow-hidden flex items-center justify-center p-4 sm:p-8 select-none relative cursor-grab active:cursor-grabbing bg-slate-900/60"
            onClick={(e) => e.stopPropagation()}
            onWheel={handleWheel}
            onMouseDown={handleMouseDown}
            onMouseMove={handleMouseMove}
            onMouseUp={handleMouseUp}
            onMouseLeave={handleMouseUp}
          >
            <div 
              className="transition-transform duration-75 ease-out flex items-center justify-center max-w-full max-h-full"
              style={{
                transform: `translate(${pan.x}px, ${pan.y}px) scale(${zoom})`,
                transformOrigin: 'center center'
              }}
            >
              <div 
                ref={modalContainerRef} 
                className="bg-white p-4 sm:p-6 rounded-2xl shadow-2xl border border-slate-200 max-w-[85vw] max-h-[70vh] flex items-center justify-center overflow-hidden [&_svg]:max-h-[65vh] [&_svg]:max-w-[80vw] [&_svg]:w-auto [&_svg]:h-auto [&_svg]:bg-white"
              />
            </div>

            {/* Floating Navigation Hint */}
            <div className="absolute bottom-4 left-1/2 -translate-x-1/2 bg-slate-950/90 border border-slate-800 text-slate-300 text-xs px-4 py-1.5 rounded-full backdrop-blur-md flex items-center gap-2 pointer-events-none shadow-xl">
              <Move size={14} className="text-indigo-400" />
              <span>Drag to Pan • Mouse Wheel to Zoom • Press Esc to Close</span>
            </div>
          </div>
        </div>,
        document.body
      )}
    </>
  );
}

