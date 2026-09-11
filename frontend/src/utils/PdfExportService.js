/**
 * Utility for generating printable PDF practice sheets for offline study.
 */

export const exportPracticeSheetPdf = (subjectId, questions, title = "EduMind Practice Sheet") => {
  const printWindow = window.open('', '_blank');
  if (!printWindow) {
    alert("Please allow popups to download the PDF practice sheet.");
    return;
  }

  const dateStr = new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });

  const htmlContent = `
    <!DOCTYPE html>
    <html>
      <head>
        <title>${title} - ${subjectId}</title>
        <style>
          body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 40px; color: #1e293b; }
          .header { border-bottom: 2px solid #0284c7; padding-bottom: 15px; margin-bottom: 25px; }
          .title { font-size: 24px; font-weight: bold; color: #0f172a; }
          .meta { font-size: 13px; color: #64748b; margin-top: 5px; }
          .question-card { margin-bottom: 25px; padding: 15px; border: 1px solid #e2e8f0; border-radius: 8px; page-break-inside: avoid; }
          .q-header { font-size: 15px; font-weight: 600; color: #0369a1; margin-bottom: 10px; }
          .q-text { font-size: 14px; margin-bottom: 12px; line-height: 1.5; }
          .options-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; font-size: 13px; }
          .option-item { background: #f8fafc; padding: 6px 12px; border-radius: 4px; border: 1px solid #cbd5e1; }
          .footer { margin-top: 40px; text-align: center; font-size: 12px; color: #94a3b8; border-top: 1px solid #e2e8f0; padding-top: 15px; }
          @media print {
            body { margin: 20px; }
            .question-card { border-color: #cbd5e1; }
          }
        </style>
      </head>
      <body>
        <div class="header">
          <div class="title">EduMind AI — ${title}</div>
          <div class="meta">Subject: <strong>${subjectId}</strong> | Generated on: ${dateStr} | Total Questions: ${questions.length}</div>
        </div>

        <div class="content">
          ${questions.map((q, idx) => `
            <div class="question-card">
              <div class="q-header">Q${idx + 1}. [${q.marks || 2} Marks]</div>
              <div class="q-text">${q.question || q.question_text || "Practice Question"}</div>
              ${q.options && q.options.length ? `
                <div class="options-grid">
                  ${q.options.map(opt => `<div class="option-item">${opt}</div>`).join('')}
                </div>
              ` : ''}
            </div>
          `).join('')}
        </div>

        <div class="footer">
          Grounded Course Materials Practice Sheet • EduMind Intelligence Engine
        </div>

        <script>
          window.onload = function() {
            window.print();
          };
        </script>
      </body>
    </html>
  `;

  printWindow.document.write(htmlContent);
  printWindow.document.close();
};
