/**
 * Render Mermaid codes via beautiful-mermaid and report results as JSON.
 *
 * Input (stdin): JSON array of strings (Mermaid diagram codes)
 * Output (stdout): JSON array of objects { code, success, error?, svgLength?, hasValidSvg? }
 *
 * Mermaid YAML frontmatter (---...---) is stripped before rendering because
 * beautiful-mermaid does not support it. See: https://github.com/drillan/sphinx-oceanid/issues/45
 */

import { renderMermaidSVG } from "beautiful-mermaid";
import { readFileSync } from "node:fs";

/**
 * Strip Mermaid YAML frontmatter (---...---) from diagram code.
 *
 * @param {string} code - Mermaid diagram code potentially with frontmatter
 * @returns {string} Code with frontmatter removed
 */
const stripFrontmatter = (code) => {
  if (!code.startsWith("---\n")) {
    return code;
  }
  const endIndex = code.indexOf("\n---\n", 4);
  if (endIndex === -1) {
    return code;
  }
  return code.slice(endIndex + 5);
};

const input = readFileSync("/dev/stdin", "utf-8");
const codes = JSON.parse(input);

const results = codes.map((code) => {
  try {
    const renderableCode = stripFrontmatter(code);
    const svg = renderMermaidSVG(renderableCode);
    return {
      code,
      success: true,
      svgLength: svg.length,
      hasValidSvg: svg.startsWith("<svg"),
    };
  } catch (e) {
    return {
      code,
      success: false,
      error: e.message,
    };
  }
});

process.stdout.write(JSON.stringify(results));
