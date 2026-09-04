import React, { useEffect, useRef, useState } from 'react';
import mermaid from 'mermaid';

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
  const [hasError, setHasError] = useState(false);

  useEffect(() => {
    if (!chart || !containerRef.current) return;

    const cleaned = sanitizeMermaidChart(chart);
    setHasError(false);

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

      // 0. Expand viewBox padding so top & side nodes are NEVER clipped by SVG canvas boundary
      const currentViewBox = svgEl.getAttribute('viewBox');
      if (currentViewBox) {
        const parts = currentViewBox.split(/[\s,]+/).map(Number);
        if (parts.length === 4 && !parts.some(isNaN)) {
          const [x, y, w, h] = parts;
          // Add 18px padding buffer to viewBox top/left/width/height to ensure no top borders or text edges cut off
          svgEl.setAttribute('viewBox', `${x - 18} ${y - 18} ${w + 36} ${h + 36}`);
        }
      }

      // 1. Expand Node Rect Widths (add extra padding buffer inside every node box so text never touches border)
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

      // 2. Force all Node Boxes to be UNFILLED (White background + Sharp 2px Dark Slate border)
      const nodeShapes = svgEl.querySelectorAll('.node rect, .node circle, .node polygon, .node ellipse, .node path, rect.basic, .label-container');
      nodeShapes.forEach((shape) => {
        shape.style.setProperty('fill', '#ffffff', 'important');
        shape.style.setProperty('fill-opacity', '1', 'important');
        shape.style.setProperty('stroke', '#1e293b', 'important');
        shape.style.setProperty('stroke-width', '2px', 'important');
        shape.setAttribute('fill', '#ffffff');
        shape.setAttribute('stroke', '#1e293b');
      });

      // 3. Force all Node Text to be crisp black, properly sized and spaced
      const nodeTexts = svgEl.querySelectorAll('.node text, .node tspan, .node span, .node div, .label text, .label tspan');
      nodeTexts.forEach((txt) => {
        txt.style.setProperty('fill', '#0f172a', 'important');
        txt.style.setProperty('color', '#0f172a', 'important');
        txt.style.setProperty('font-weight', '600', 'important');
        txt.style.setProperty('font-size', '13px', 'important');
        txt.style.setProperty('letter-spacing', '0.01em', 'important');
        txt.setAttribute('fill', '#0f172a');
      });

      // 3. Force Edge Labels to have white background and crisp black text (NO dark navy blocks)
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

      // 4. Force Edge Paths and Arrow Markers to be dark slate
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

    const id = `mermaid-svg-${Math.floor(Math.random() * 10000000)}`;
    containerRef.current.innerHTML = '';

    mermaid.render(id, cleaned)
      .then((res) => {
        if (containerRef.current) {
          containerRef.current.innerHTML = res.svg;
          applyUnfilledLightStyles(containerRef.current);
        }
      })
      .catch((err) => {
        console.warn('Mermaid initial render notice:', err);
        const errEl = document.getElementById(`d${id}`) || document.getElementById(id);
        if (errEl) errEl.remove();

        const fallbackCode = cleaned.replace(/\["([^"]*)"\]/g, (m, txt) => `["${txt.replace(/[:;,{}()]/g, ' ')}"]`);
        const fallbackId = `mermaid-fallback-${Math.floor(Math.random() * 10000000)}`;

        mermaid.render(fallbackId, fallbackCode)
          .then((res2) => {
            if (containerRef.current) {
              containerRef.current.innerHTML = res2.svg;
              applyUnfilledLightStyles(containerRef.current);
            }
          })
          .catch((e2) => {
            console.error('Mermaid render final notice:', e2);
            const errEl2 = document.getElementById(`d${fallbackId}`) || document.getElementById(fallbackId);
            if (errEl2) errEl2.remove();
            setHasError(true);
          });
      });
  }, [chart]);

  if (hasError) return null;

  return (
    <div className="my-3 rounded-2xl border border-slate-200 bg-white shadow-md overflow-hidden text-slate-900">
      {/* Light Header bar */}
      <div className="px-3.5 py-2 bg-slate-100 border-b border-slate-200 flex items-center justify-between">
        <div className="flex items-center gap-2 text-indigo-700 font-bold text-[11px] uppercase tracking-wider">
          <span className="w-2 h-2 rounded-full bg-indigo-600 animate-pulse" />
          <span>📊 Flowchart / Process Diagram</span>
        </div>
      </div>

      {/* Crisp White Render Area */}
      <div className="p-4 flex justify-center w-full overflow-x-auto bg-white custom-scrollbar">
        <div 
          ref={containerRef} 
          className="mermaid-render-area w-full flex justify-center text-slate-900 [&_svg]:max-w-full [&_svg]:h-auto [&_svg]:bg-white" 
        />
      </div>
    </div>
  );
}
