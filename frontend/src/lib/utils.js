import { clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs) {
  return twMerge(clsx(inputs));
}

export function formatTextSpacing(text) {
  if (!text) return "";
  return text;
}

/**
 * Preprocesses markdown content to ensure Mermaid diagrams are properly fenced,
 * auto-detects raw unfenced Mermaid blocks, and synthesizes fallback diagrams
 * if the text promises a diagram but lacks a ```mermaid code block.
 */
export function preprocessMarkdownContent(content, isStreaming = false) {
  if (!content || typeof content !== 'string') return content || '';

  let processed = content;

  // 1. Fix code blocks with missing 'mermaid' language identifier (e.g. ``` \n flowchart TD ...)
  processed = processed.replace(/```(?:\w*)\n\s*(flowchart\s+[A-Z]{2}|graph\s+[A-Z]{2}|sequenceDiagram|erDiagram|classDiagram|stateDiagram-v2)[\s\S]*?```/gi, (match) => {
    if (!match.startsWith('```mermaid')) {
      return match.replace(/^```(?:\w*)/, '```mermaid');
    }
    return match;
  });

  // 2. Auto-wrap raw un-fenced Mermaid diagrams
  if (!processed.includes('```mermaid')) {
    const rawMermaidRegex = /(?:^|\n)(flowchart\s+(?:TD|LR|TB|BT|RL)|graph\s+(?:TD|LR|TB|BT|RL)|sequenceDiagram|classDiagram|erDiagram|stateDiagram-v2)[\s\S]*?(?=\n\s*\n[A-Z0-9#\*]|\n\s*\n?$|$)/gi;
    processed = processed.replace(rawMermaidRegex, (match) => {
      const trimmed = match.trim();
      if (trimmed.startsWith('```')) return match;
      return `\n\n\`\`\`mermaid\n${trimmed}\n\`\`\`\n\n`;
    });
  }

  // 3. Fallback Auto-Diagram Synthesizer:
  // ONLY run when isStreaming is FALSE. While response text is actively streaming,
  // speculative synthesis causes layout shifts, diagram popping, and height oscillations.
  if (!isStreaming && !processed.includes('```mermaid')) {
    const claimsDiagramRegex = /(?:here's|here is|below is|represented in|block diagram of|flowchart of|diagram of)(?:[^\n]*?)(?:flowchart|diagram|block diagram)/i;
    
    if (claimsDiagramRegex.test(processed)) {
      // Extract bullet points / bold headers to construct a clean flowchart automatically
      const bulletLines = [];
      const lineRegex = /(?:^\s*[-*•\d\.]+\s+|\*\*)([A-Za-z0-9\s_\-\(\)]+?)(?:\*\*|:|\s*[-–—]|\n)/g;
      let match;
      while ((match = lineRegex.exec(processed)) !== null) {
        const cleanTerm = match[1].trim();
        if (cleanTerm.length > 2 && cleanTerm.length < 45 && !bulletLines.includes(cleanTerm)) {
          bulletLines.push(cleanTerm);
        }
      }

      if (bulletLines.length >= 2) {
        const mainTitleMatch = processed.match(/(?:flowchart|diagram|block diagram)\s+(?:of|for)?\s*([A-Za-z0-9\s]+?)(?=\n|\.|:|$)/i);
        const mainTitle = mainTitleMatch ? mainTitleMatch[1].trim() : 'System Flowchart';

        let autoMermaid = `\n\n\`\`\`mermaid\nflowchart TD\n    Root["${mainTitle.slice(0, 32)}"]\n`;
        bulletLines.slice(0, 6).forEach((item, idx) => {
          autoMermaid += `    Root --> Node${idx + 1}["${item}"]\n`;
        });
        autoMermaid += `\`\`\`\n\n`;

        processed += autoMermaid;
      }
    }
  }

  return processed;
}
