/**
 * sphinx-oceanid: Diagram rendering and lazy loading via IntersectionObserver.
 *
 * Exports:
 *   renderVisibleDiagrams(elements, renderFn, themeColors)
 *   setupLazyRendering(elements, renderFn, themeColors)
 */

/**
 * Render a single diagram element.
 *
 * On success: inserts SVG in .oceanid-svg-container, sets data-oceanid-rendered="true".
 * On failure (FR-023): sets data-oceanid-render-failed="true", shows error message + source code.
 *
 * @param {Element} el - .oceanid-diagram element
 * @param {Function} renderFn - beautiful-mermaid renderMermaidSVG function
 * @param {object} themeColors - DiagramColors object
 */
const renderSingleDiagram = (el, renderFn, themeColors) => {
  try {
    const code = el.getAttribute("data-oceanid-code");
    if (!code) {
      throw new Error("data-oceanid-code attribute is missing");
    }

    const svg = renderFn(code, { ...themeColors });

    const container = document.createElement("div");
    container.className = "oceanid-svg-container";
    container.innerHTML = svg;

    el.appendChild(container);
    el.setAttribute("data-oceanid-rendered", "true");
  } catch (error) {
    el.setAttribute("data-oceanid-render-failed", "true");

    const code = el.getAttribute("data-oceanid-code") || "";

    const errorDiv = document.createElement("div");
    errorDiv.className = "oceanid-render-error";
    errorDiv.textContent = `Rendering failed: ${error.message}`;

    const sourcePre = document.createElement("pre");
    sourcePre.className = "oceanid-render-error-source";
    sourcePre.textContent = code;

    el.appendChild(errorDiv);
    el.appendChild(sourcePre);

    console.error("sphinx-oceanid: Diagram rendering failed:", error);
  }
};

/**
 * Render all visible diagram elements immediately.
 *
 * @param {Element[]} elements - Visible .oceanid-diagram elements
 * @param {Function} renderFn - beautiful-mermaid renderMermaidSVG function
 * @param {object} themeColors - DiagramColors object
 */
export const renderVisibleDiagrams = (elements, renderFn, themeColors) => {
  elements.forEach((el) => {
    renderSingleDiagram(el, renderFn, themeColors);
  });
};

/**
 * Set up IntersectionObserver for lazy rendering of hidden diagram elements.
 *
 * Each element gets data-oceanid-deferred="true" while waiting.
 * Once visible (threshold 0.01), it is rendered and unobserved.
 *
 * @param {Element[]} elements - Hidden .oceanid-diagram elements
 * @param {Function} renderFn - beautiful-mermaid renderMermaidSVG function
 * @param {object} themeColors - DiagramColors object
 */
export const setupLazyRendering = (elements, renderFn, themeColors) => {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (
          entry.isIntersecting &&
          !entry.target.hasAttribute("data-oceanid-rendered")
        ) {
          renderSingleDiagram(entry.target, renderFn, themeColors);
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.01 }
  );

  elements.forEach((el) => {
    el.setAttribute("data-oceanid-deferred", "true");
    observer.observe(el);
  });
};
