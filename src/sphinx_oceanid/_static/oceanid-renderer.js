/**
 * sphinx-oceanid: Main entry point for client-side Mermaid rendering.
 *
 * Loads config from #oceanid-config, dynamically imports beautiful-mermaid,
 * resolves theme colors, partitions diagrams by visibility, and delegates
 * rendering to oceanid-observer.js.
 */

/**
 * Load configuration from the #oceanid-config JSON script element.
 *
 * @returns {object} Parsed config object
 * @throws {Error} If #oceanid-config element is not found
 */
const loadConfig = () => {
  const el = document.getElementById("oceanid-config");
  if (!el || !el.textContent) {
    throw new Error("oceanid-config element not found");
  }
  return JSON.parse(el.textContent);
};

/**
 * Partition diagram elements into visible and hidden groups.
 *
 * Uses offsetParent and getClientRects() to determine visibility.
 * Hidden elements will be lazily rendered via IntersectionObserver.
 *
 * @param {NodeList|Element[]} elements - .oceanid-diagram elements
 * @returns {{visible: Element[], hidden: Element[]}}
 */
const partitionByVisibility = (elements) => {
  const visible = [];
  const hidden = [];

  elements.forEach((el) => {
    if (el.offsetParent === null || el.getClientRects().length === 0) {
      hidden.push(el);
    } else {
      visible.push(el);
    }
  });

  return { visible, hidden };
};

/**
 * Main entry point. Runs on window load.
 */
const main = async () => {
  try {
    const config = loadConfig();

    const beautifulMermaid = await import(config.beautifulMermaidUrl);
    const renderFn = beautifulMermaid.renderMermaidSVG;
    const THEMES = beautifulMermaid.THEMES;

    const { resolveThemeColors, observeThemeChanges } = await import(
      "./oceanid-theme.js"
    );

    const themeColors = resolveThemeColors(config, THEMES);

    const { renderVisibleDiagrams, setupLazyRendering, renderSingleDiagram } =
      await import("./oceanid-observer.js");

    const diagrams = document.querySelectorAll(".oceanid-diagram");
    if (diagrams.length === 0) {
      return;
    }

    const { visible, hidden } = partitionByVisibility(diagrams);

    renderVisibleDiagrams(visible, renderFn, themeColors);
    setupLazyRendering(hidden, renderFn, themeColors);

    if (config.zoom || config.zoomSelectors.length > 0) {
      const { setupZoom } = await import("./oceanid-zoom.js");
      setupZoom(config.zoomSelectors);
    }

    if (config.fullscreen) {
      const { setupFullscreen } = await import("./oceanid-fullscreen.js");
      setupFullscreen(config);
    }

    if (config.revealjs || typeof Reveal !== "undefined") {
      Reveal.addEventListener?.("slidechanged", () => {
        document
          .querySelectorAll(
            '.oceanid-diagram:not([data-oceanid-rendered="true"])'
          )
          .forEach((el) => {
            if (el.offsetParent !== null) {
              renderSingleDiagram(el, renderFn, themeColors);
            }
          });
      });
    }

    observeThemeChanges(config, THEMES, renderFn);
  } catch (err) {
    console.error("sphinx-oceanid: Failed to initialize:", err);
  }
};

window.addEventListener("load", main);
