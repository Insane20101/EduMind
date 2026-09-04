import re

def split_large_text(text: str, max_chars: int = 2000, overlap: int = 200) -> list[str]:
    chunks = []
    start = 0
    text_len = len(text)
    
    while start < text_len:
        end = start + max_chars
        if end >= text_len:
            chunks.append(text[start:text_len].strip())
            break
            
        # Find the last period or space within the window to avoid cutting mid-sentence
        last_period = text.rfind('.', start, end)
        if last_period != -1 and last_period > start + (max_chars * 0.5):
            end = last_period + 1
        else:
            last_space = text.rfind(' ', start, end)
            if last_space != -1:
                end = last_space + 1
                
        chunk_text = text[start:end].strip()
        if chunk_text:
            chunks.append(chunk_text)
            
        # Move start forward, but backtrack for overlap
        start = end - overlap
        if start < 0:
            start = 0
            
    return chunks

def chunk_transcript(text: str, source_file: str, subject_id: str, semester: str) -> list[dict]:
    """
    Chunks transcript text by ~500 tokens (~2000 chars) with ~50 tokens (~200 chars) overlap.
    """
    raw_chunks = split_large_text(text, max_chars=2000, overlap=200)
    
    final_chunks = []
    for i, c_text in enumerate(raw_chunks):
        if not c_text:
            continue
        final_chunks.append({
            "text": c_text,
            "metadata": {
                "subject_id": subject_id,
                "semester": semester,
                "unit": "unassigned",
                "source_type": "transcript",
                "source_file": source_file,
                "chunk_index": i
            }
        })
        
    return final_chunks

def chunk_markdown(text: str, source_file: str, subject_id: str, semester: str, source_type: str) -> list[dict]:
    """
    Chunks Question Bank and Solution Markdown files by question boundaries.
    Falls back to character-based chunking if a block is too large.
    """
    final_chunks = []
    
    # Strip Coverage Summary from the end to prevent it from bleeding into the last question
    coverage_idx = text.find("## Coverage Summary")
    if coverage_idx != -1:
        text = text[:coverage_idx].strip()
        
    # Split by Question Bank format: "\n1. **[Unit" OR Solutions format: "\n**1. " OR "\n**Q1. "
    pattern = r'\n(?=\d+\.\s\*\*\[Unit\s|\*\*\d+\.\s|\*\*Q\d+\.\s)'
    raw_blocks = re.split(pattern, text)
    
    chunk_idx = 0
    current_unit = "unassigned"
    global_question_id = 1
    
    for block in raw_blocks:
        block = block.strip()
        if not block:
            continue
            
        # Try to update current_unit from header if present
        # e.g., '## UNIT II — Linear Algebra' or '## Detailed Step-Wise Solutions — UNIT I:'
        unit_header_match = re.search(r'(?:#+.*?)?(UNIT\s+[IVX]+)', block, re.IGNORECASE)
        if unit_header_match:
            current_unit = "Unit " + unit_header_match.group(1).split()[-1].upper()

        question_id = None
        qb_match = re.match(r'^(\d+)\.\s\*\*\[Unit', block)
        sol_match = re.match(r'^\*\*(\d+)\.\s', block)
        sol_q_match = re.match(r'^\*\*Q(\d+)\.\s', block)
        if qb_match:
            question_id = qb_match.group(1)
        elif sol_match:
            question_id = sol_match.group(1)
        elif sol_q_match:
            question_id = sol_q_match.group(1)

        # Extract metadata from tag line: **[Unit X | Topic: Y | Type: Z | Difficulty: W]**
        tag_match = re.search(r'\*\*\[(.*?)\]\*\*', block)
        
        metadata = {
            "subject_id": subject_id,
            "semester": semester,
            "unit": current_unit, # Default to the section's unit
            "topic": "unassigned",
            "type": "unassigned",
            "difficulty": "unassigned",
            "source_type": source_type,
            "source_file": source_file,
            "chunk_index": chunk_idx
        }
        
        if question_id:
            metadata["question_id"] = str(global_question_id)
            global_question_id += 1
        
        if tag_match:
            parts = [p.strip() for p in tag_match.group(1).split('|')]
            for part in parts:
                if part.lower().startswith('unit'):
                    metadata["unit"] = part.strip()
                    # Also update current_unit for future fallback just in case
                    current_unit = part.strip()
                elif part.lower().startswith('topic:'):
                    metadata["topic"] = part.split(':', 1)[1].strip()
                elif part.lower().startswith('type:'):
                    metadata["type"] = part.split(':', 1)[1].strip()
                elif part.lower().startswith('difficulty:'):
                    metadata["difficulty"] = part.split(':', 1)[1].strip()
                    
            if len(block) > 8000:
                sub_blocks = split_large_text(block, 4000, 200)
                for sb in sub_blocks:
                    m = metadata.copy()
                    m["chunk_index"] = chunk_idx
                    final_chunks.append({"text": sb, "metadata": m})
                    chunk_idx += 1
            else:
                final_chunks.append({"text": block, "metadata": metadata})
                chunk_idx += 1
        else:
            if len(block) > 100:
                if len(block) > 4000:
                    sub_blocks = split_large_text(block, 2000, 200)
                    for sb in sub_blocks:
                        m = metadata.copy()
                        m["chunk_index"] = chunk_idx
                        final_chunks.append({"text": sb, "metadata": m})
                        chunk_idx += 1
                else:
                    final_chunks.append({"text": block, "metadata": metadata})
                    chunk_idx += 1
                
    return final_chunks
