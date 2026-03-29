/**
 * sphinx-oceanid: Native SVG zoom without d3.js (FR-017, ADR-004).
 *
 * Implements wheel zoom, drag pan, double-click reset, and pinch zoom
 * using Pointer Events + SVG viewBox manipulation.
 */

const MIN_SCALE = 0.1;
const MAX_SCALE = 10;
const WHEEL_ZOOM_FACTOR = 0.1;

/**
 * Enable zoom/pan on a single SVG element.
 *
 * @param {SVGSVGElement} svg - Target SVG element
 */
const enableSvgZoom = (svg) => {
  const baseViewBox = svg.viewBox.baseVal;
  if (!baseViewBox || baseViewBox.width === 0) {
    return;
  }

  const initial = {
    x: baseViewBox.x,
    y: baseViewBox.y,
    width: baseViewBox.width,
    height: baseViewBox.height,
  };

  let state = { x: initial.x, y: initial.y, scale: 1 };
  let isPanning = false;
  let startPoint = { x: 0, y: 0 };
  let startViewBox = { x: 0, y: 0 };

  const applyViewBox = () => {
    const w = initial.width / state.scale;
    const h = initial.height / state.scale;
    svg.setAttribute("viewBox", `${state.x} ${state.y} ${w} ${h}`);
  };

  const svgPoint = (clientX, clientY) => {
    const ctm = svg.getScreenCTM();
    if (!ctm) {
      return { x: clientX, y: clientY };
    }
    const inv = ctm.inverse();
    return {
      x: clientX * inv.a + clientY * inv.c + inv.e,
      y: clientX * inv.b + clientY * inv.d + inv.f,
    };
  };

  // Wheel zoom
  svg.addEventListener(
    "wheel",
    (e) => {
      e.preventDefault();
      const direction = e.deltaY > 0 ? -1 : 1;
      const factor = 1 + direction * WHEEL_ZOOM_FACTOR;
      const newScale = Math.max(MIN_SCALE, Math.min(MAX_SCALE, state.scale * factor));

      const pt = svgPoint(e.clientX, e.clientY);
      const ratio = 1 - state.scale / newScale;

      state.x += (pt.x - state.x) * ratio;
      state.y += (pt.y - state.y) * ratio;
      state.scale = newScale;

      applyViewBox();
    },
    { passive: false }
  );

  // Drag pan
  svg.addEventListener("pointerdown", (e) => {
    if (e.button !== 0) {
      return;
    }
    isPanning = true;
    startPoint = svgPoint(e.clientX, e.clientY);
    startViewBox = { x: state.x, y: state.y };
    svg.setPointerCapture(e.pointerId);
  });

  svg.addEventListener("pointermove", (e) => {
    if (!isPanning) {
      return;
    }
    const current = svgPoint(e.clientX, e.clientY);
    state.x = startViewBox.x - (current.x - startPoint.x);
    state.y = startViewBox.y - (current.y - startPoint.y);
    applyViewBox();
  });

  const endPan = (e) => {
    if (isPanning) {
      isPanning = false;
      svg.releasePointerCapture(e.pointerId);
    }
  };
  svg.addEventListener("pointerup", endPan);
  svg.addEventListener("pointercancel", endPan);

  // Double-click reset
  svg.addEventListener("dblclick", (e) => {
    e.preventDefault();
    state = { x: initial.x, y: initial.y, scale: 1 };
    applyViewBox();
  });

  // Pinch zoom (touch)
  let pinchStartDist = 0;
  let pinchStartScale = 1;

  svg.addEventListener(
    "touchstart",
    (e) => {
      if (e.touches.length === 2) {
        e.preventDefault();
        const dx = e.touches[0].clientX - e.touches[1].clientX;
        const dy = e.touches[0].clientY - e.touches[1].clientY;
        pinchStartDist = Math.hypot(dx, dy);
        pinchStartScale = state.scale;
      }
    },
    { passive: false }
  );

  svg.addEventListener(
    "touchmove",
    (e) => {
      if (e.touches.length === 2) {
        e.preventDefault();
        const dx = e.touches[0].clientX - e.touches[1].clientX;
        const dy = e.touches[0].clientY - e.touches[1].clientY;
        const dist = Math.hypot(dx, dy);
        const factor = dist / pinchStartDist;
        state.scale = Math.max(
          MIN_SCALE,
          Math.min(MAX_SCALE, pinchStartScale * factor)
        );
        applyViewBox();
      }
    },
    { passive: false }
  );

  svg.style.touchAction = "none";
};

/**
 * Set up zoom on diagram elements matching the given selectors.
 *
 * If selectors is empty, zoom is applied to all .oceanid-diagram[data-oceanid-zoom] elements.
 *
 * @param {string[]} selectors - CSS selectors for zoom targets (e.g. ["#diagram-1"])
 */
export const setupZoom = (selectors) => {
  const selector =
    selectors.length > 0
      ? selectors.join(", ")
      : ".oceanid-diagram[data-oceanid-zoom]";

  const attachZoom = (el) => {
    const svg = el.querySelector("svg");
    if (svg && !svg.dataset.oceanidZoomEnabled) {
      enableSvgZoom(svg);
      svg.dataset.oceanidZoomEnabled = "true";
    }
  };

  document.querySelectorAll(selector).forEach(attachZoom);

  // Watch for lazily rendered diagrams
  const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      if (
        mutation.type === "attributes" &&
        mutation.attributeName === "data-oceanid-rendered" &&
        mutation.target.getAttribute("data-oceanid-rendered") === "true" &&
        mutation.target.matches(selector)
      ) {
        attachZoom(mutation.target);
      }
    });
  });

  document.querySelectorAll(".oceanid-diagram").forEach((el) => {
    observer.observe(el, { attributes: true });
  });
};
