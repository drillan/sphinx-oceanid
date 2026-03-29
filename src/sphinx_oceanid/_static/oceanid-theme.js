/**
 * sphinx-oceanid: Theme management — dark/light detection and CSS variable theming.
 *
 * Exports:
 *   resolveThemeColors(config, THEMES) → DiagramColors
 *   observeThemeChanges(config, THEMES) → void
 */

/** CSS variable keys used by beautiful-mermaid SVGs. */
const CSS_VAR_KEYS = ["bg", "fg", "line", "accent", "muted", "surface", "border"];

/**
 * Detect the page's current color scheme.
 *
 * Detection priority:
 * 1. data-theme attribute on <html> or <body>
 * 2. class attribute containing "dark" or "light"
 * 3. prefers-color-scheme media query
 * 4. Background color luminance (YIQ formula)
 *
 * @returns {"dark" | "light"}
 */
const detectColorScheme = () => {
  // 1. data-theme attribute
  const dataTheme =
    document.documentElement.getAttribute("data-theme") ||
    document.body.getAttribute("data-theme");
  if (dataTheme) {
    const normalized = dataTheme.toLowerCase();
    if (normalized.includes("dark")) return "dark";
    if (normalized.includes("light")) return "light";
  }

  // 2. class attribute
  const classes = [
    ...document.documentElement.classList,
    ...document.body.classList,
  ];
  for (const cls of classes) {
    const lower = cls.toLowerCase();
    if (lower === "dark" || lower.includes("dark-mode") || lower.includes("dark-theme")) return "dark";
    if (lower === "light" || lower.includes("light-mode") || lower.includes("light-theme")) return "light";
  }

  // 3. prefers-color-scheme media query
  if (window.matchMedia("(prefers-color-scheme: dark)").matches) return "dark";
  if (window.matchMedia("(prefers-color-scheme: light)").matches) return "light";

  // 4. Background luminance (YIQ)
  const bgColor = getComputedStyle(document.body).backgroundColor;
  const rgb = parseRgb(bgColor);
  if (rgb) {
    const yiq = (rgb.r * 299 + rgb.g * 587 + rgb.b * 114) / 1000;
    return yiq < 128 ? "dark" : "light";
  }

  return "light";
};

/**
 * Parse an rgb/rgba CSS color string into {r, g, b} components.
 *
 * @param {string} color - CSS color string (e.g., "rgb(255, 255, 255)")
 * @returns {{r: number, g: number, b: number} | null}
 */
const parseRgb = (color) => {
  const match = color.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)/);
  if (!match) return null;
  return { r: Number(match[1]), g: Number(match[2]), b: Number(match[3]) };
};

/**
 * Resolve theme colors from config and beautiful-mermaid THEMES.
 *
 * When theme is "auto", uses detectColorScheme() to pick dark or light theme.
 * When theme is a specific name, uses that theme directly.
 *
 * @param {object} config - Oceanid config object
 * @param {Record<string, object>} THEMES - beautiful-mermaid THEMES map
 * @returns {object} DiagramColors object for renderMermaidSVG
 * @throws {Error} If the specified theme name is not found in THEMES
 */
export const resolveThemeColors = (config, THEMES) => {
  let themeName;
  if (config.theme === "auto") {
    const scheme = detectColorScheme();
    themeName = scheme === "dark" ? config.themeDark : config.themeLight;
  } else {
    themeName = config.theme;
  }

  const colors = THEMES[themeName];
  if (!colors) {
    throw new Error(
      `sphinx-oceanid: Theme "${themeName}" not found in THEMES. ` +
        `Available: ${Object.keys(THEMES).join(", ")}`
    );
  }
  return colors;
};

/**
 * Apply CSS variables from DiagramColors to all rendered SVG elements.
 *
 * @param {object} colors - DiagramColors object
 */
const applyCssVariables = (colors) => {
  const svgs = document.querySelectorAll(
    '.oceanid-diagram[data-oceanid-rendered="true"] .oceanid-svg-container svg'
  );
  svgs.forEach((svg) => {
    for (const key of CSS_VAR_KEYS) {
      if (colors[key] !== undefined) {
        svg.style.setProperty(`--${key}`, colors[key]);
      }
    }
  });
};

/**
 * Observe theme changes via MutationObserver and prefers-color-scheme listener.
 *
 * On theme change detection:
 * - Resolves new theme colors from config + THEMES
 * - Applies CSS variables to all rendered SVGs (no re-render)
 *
 * @param {object} config - Oceanid config object
 * @param {Record<string, object>} THEMES - beautiful-mermaid THEMES map
 */
export const observeThemeChanges = (config, THEMES) => {
  if (config.theme !== "auto") return;

  const updateTheme = () => {
    try {
      const colors = resolveThemeColors(config, THEMES);
      applyCssVariables(colors);
    } catch (err) {
      console.error("sphinx-oceanid: Theme update failed:", err);
    }
  };

  // MutationObserver: watch data-theme and class on <html> and <body>
  const observer = new MutationObserver(updateTheme);
  const observerConfig = {
    attributes: true,
    attributeFilter: ["data-theme", "class"],
  };
  observer.observe(document.documentElement, observerConfig);
  observer.observe(document.body, observerConfig);

  // MediaQueryList: watch prefers-color-scheme changes
  const mediaQuery = window.matchMedia("(prefers-color-scheme: dark)");
  mediaQuery.addEventListener("change", updateTheme);
};
