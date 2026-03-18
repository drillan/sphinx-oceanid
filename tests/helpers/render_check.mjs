/**
 * Render Mermaid codes via beautiful-mermaid and report results as JSON.
 *
 * Input (stdin): JSON array of strings (Mermaid diagram codes)
 * Output (stdout): JSON array of objects { code, success, error?, svgLength?, hasValidSvg? }
 */

import { renderMermaidSVG } from "beautiful-mermaid";
import { readFileSync } from "node:fs";

const input = readFileSync("/dev/stdin", "utf-8");
const codes = JSON.parse(input);

const results = codes.map((code) => {
  try {
    const svg = renderMermaidSVG(code);
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
