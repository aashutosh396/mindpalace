// Tiny safe markdown for agent text: HTML is escaped FIRST, then a small set
// of markdown becomes tags we generate ourselves — no raw HTML ever passes
// through. Containers use white-space: pre-wrap, so newlines survive as-is.

function esc(s: string): string {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
}

export function md(src: string): string {
  if (!src) return ''
  let s = esc(src)
  // fenced code blocks (drop an optional language tag on the fence)
  s = s.replace(/```[a-z]*\n?([\s\S]*?)```/g,
    (_m, code) => `<pre class="md-pre">${code.replace(/\n$/, '')}</pre>`)
  s = s.replace(/`([^`\n]+)`/g, '<code class="md-code">$1</code>')
  s = s.replace(/\*\*([^*\n]+)\*\*/g, '<strong>$1</strong>')
  s = s.replace(/(^|[\s(])\*([^*\n]+)\*(?=[\s).,!?:;]|$)/g, '$1<em>$2</em>')
  s = s.replace(/^#{1,4} (.+)$/gm, '<strong class="md-h">$1</strong>')
  s = s.replace(/^[-*] (.+)$/gm, '<span class="md-li">•</span> $1')
  s = s.replace(/\[([^\]\n]+)\]\((https?:\/\/[^)\s]+)\)/g,
    '<a class="md-link" href="$2" target="_blank" rel="noopener noreferrer">$1</a>')
  return s
}

// one-line contexts (ellipsized excerpts): remove the markers instead
export function stripMd(src: string): string {
  return (src || '')
    .replace(/```[a-z]*\n?/g, '').replace(/[`*_#]/g, '')
    .replace(/\[([^\]\n]+)\]\((?:https?:\/\/)[^)\s]+\)/g, '$1')
}
