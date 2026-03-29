/**
 * sphinx-oceanid: Diagram rendering and lazy loading via IntersectionObserver.
 *
 * Exports:
 *   renderSingleDiagram(el, renderFn, themeColors)
 *   renderVisibleDiagrams(elements, renderFn, themeColors)
 *   setupLazyRendering(elements, renderFn, themeColors)
 */

/** Keys from data-oceanid-config that map to beautiful-mermaid RenderOptions. */
const RENDER_OPTION_KEYS = [
  "bg", "fg", "line", "accent", "muted", "surface", "border",
  "font", "padding", "nodeSpacing", "layerSpacing", "componentSpacing",
  "transparent", "interactive",
];

/**
 * Build per-diagram render options by merging page-level theme colors
 * with diagram-level config (data-oceanid-config).
 *
 * Only keys that match beautiful-mermaid RenderOptions are applied;
 * unknown keys (e.g. Mermaid.js "theme", "look") are silently ignored.
 *
 * @param {Element} el - .oceanid-diagram element
 * @param {object} themeColors - Page-level DiagramColors object
 * @returns {object} Merged render options
 */
const buildDiagramOptions = (el, themeColors) => {
  const configAttr = el.getAttribute("data-oceanid-config");
  if (!configAttr) {
    return { ...themeColors };
  }
  try {
    const config = JSON.parse(configAttr);
    const overrides = {};
    for (const key of RENDER_OPTION_KEYS) {
      if (key in config) {
        overrides[key] = config[key];
      }
    }
    return { ...themeColors, ...overrides };
  } catch {
    return { ...themeColors };
  }
};

/**
 * Insert a title element before the SVG container if data-oceanid-title is set.
 *
 * @param {Element} el - .oceanid-diagram element
 */
const insertTitle = (el) => {
  const title = el.getAttribute("data-oceanid-title");
  if (!title) return;
  const titleEl = document.createElement("p");
  titleEl.className = "oceanid-diagram-title";
  titleEl.textContent = title;
  el.prepend(titleEl);
};

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
export const renderSingleDiagram = (el, renderFn, themeColors) => {
  try {
    const code = el.getAttribute("data-oceanid-code");
    if (!code) {
      throw new Error("data-oceanid-code attribute is missing");
    }

    const options = buildDiagramOptions(el, themeColors);
    const svg = renderFn(code, options);

    insertTitle(el);

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
