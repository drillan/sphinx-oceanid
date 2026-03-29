/**
 * sphinx-oceanid: Fullscreen modal for Mermaid diagrams (FR-018).
 *
 * Creates a modal overlay, injects fullscreen buttons on rendered diagrams,
 * and watches for newly rendered diagrams via MutationObserver.
 */

/**
 * Create the fullscreen modal DOM element and append to document body.
 *
 * @param {object} config - Oceanid config with fullscreenButton and fullscreenButtonOpacity
 * @returns {{modal: HTMLElement, container: HTMLElement, close: Function}}
 */
const createModal = (config) => {
  const modal = document.createElement("div");
  modal.className = "oceanid-fullscreen-modal";

  const closeBtn = document.createElement("button");
  closeBtn.className = "oceanid-fullscreen-close";
  closeBtn.textContent = "\u00d7";
  closeBtn.setAttribute("aria-label", "Close fullscreen");

  const container = document.createElement("div");
  container.className = "oceanid-container-fullscreen";

  modal.appendChild(closeBtn);
  modal.appendChild(container);
  document.body.appendChild(modal);

  const close = () => {
    modal.classList.remove("active");
    container.innerHTML = "";
  };

  closeBtn.addEventListener("click", close);

  modal.addEventListener("click", (e) => {
    if (e.target === modal) {
      close();
    }
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && modal.classList.contains("active")) {
      close();
    }
  });

  return { modal, container, close };
};

/**
 * Inject a fullscreen button on a rendered diagram element.
 *
 * @param {Element} el - .oceanid-diagram element with data-oceanid-rendered="true"
 * @param {object} config - Oceanid config
 * @param {{modal: HTMLElement, container: HTMLElement}} modalCtx - Modal context
 */
const addFullscreenButton = (el, config, modalCtx) => {
  if (el.querySelector(".oceanid-fullscreen-btn")) {
    return;
  }

  const wrapper = el.querySelector(".oceanid-svg-container");
  if (!wrapper) {
    return;
  }

  el.style.position = el.style.position || "relative";

  const btn = document.createElement("button");
  btn.className = "oceanid-fullscreen-btn";
  btn.textContent = config.fullscreenButton;
  btn.setAttribute("aria-label", "Open fullscreen");
  btn.style.opacity = String(config.fullscreenButtonOpacity / 100);

  btn.addEventListener("click", () => {
    const svg = wrapper.querySelector("svg");
    if (!svg) {
      return;
    }
    modalCtx.container.innerHTML = "";
    const clone = svg.cloneNode(true);
    clone.removeAttribute("width");
    clone.removeAttribute("height");
    clone.style.width = "100%";
    clone.style.height = "100%";
    modalCtx.container.appendChild(clone);
    modalCtx.modal.classList.add("active");
  });

  el.appendChild(btn);
};

/**
 * Set up fullscreen modal functionality.
 *
 * - Creates modal DOM and appends to body
 * - Adds fullscreen button to already-rendered diagrams
 * - Uses MutationObserver to add button to diagrams rendered later (lazy)
 *
 * @param {object} config - Oceanid config
 */
export const setupFullscreen = (config) => {
  const modalCtx = createModal(config);

  document
    .querySelectorAll('.oceanid-diagram[data-oceanid-rendered="true"]')
    .forEach((el) => {
      addFullscreenButton(el, config, modalCtx);
    });

  const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      if (
        mutation.type === "attributes" &&
        mutation.attributeName === "data-oceanid-rendered" &&
        mutation.target.getAttribute("data-oceanid-rendered") === "true"
      ) {
        addFullscreenButton(mutation.target, config, modalCtx);
      }
    });
  });

  document.querySelectorAll(".oceanid-diagram").forEach((el) => {
    observer.observe(el, { attributes: true });
  });
};
