window.CUSDIS = {};
const makeIframeContent = (target) => {
  const host = target.dataset.host || "https://cusdis.com";
  const iframeJsPath = target.dataset.iframe || `${host}/js/iframe.umd.js`;
  const cssPath = `${host}/js/style.css`;
  return `<!DOCTYPE html>
<html>
  <head>
    <link rel="stylesheet" href="${cssPath}">
    <base target="_parent" />
    <link>
    <script>
      window.CUSDIS_LOCALE = ${JSON.stringify(window.CUSDIS_LOCALE)}
      window.__DATA__ = ${JSON.stringify(target.dataset)}
    <\/script>
    <style>
      :root {
        color-scheme: inherit;
        font-family: "Source Sans Pro", "Microsoft Yahei", sans-serif;
      }
      body {
        background: transparent !important;
      }
      label {
        font-weight: 400 !important;
        font-size: 0.85rem !important;
      }
      /* Force everything to be visible in dark mode */
      .dark, .dark * {
        color: #d1d5db !important;
      }
      .dark .font-medium, .dark .my-2 {
        color: #ffffff !important;
      }
      /* Ensure inputs are visible */
      input, textarea {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid #444 !important;
        color: inherit !important;
      }
    </style>
  </head>
  <body>
    <div id="root"></div>
    <script src="${iframeJsPath}" type="module"><\/script>
  </body>
</html>`;
};

let singleTonIframe;
function createIframe(target) {
  if (!singleTonIframe) {
    singleTonIframe = document.createElement("iframe");
    listenEvent(singleTonIframe, target);
  }
  singleTonIframe.srcdoc = makeIframeContent(target);
  singleTonIframe.style.width = "100%";
  singleTonIframe.style.border = "0";
  singleTonIframe.style.background = "transparent";
  singleTonIframe.style.minHeight = "800px"; // Massive min-height to avoid clipping
  singleTonIframe.setAttribute("allowtransparency", "true");
  return singleTonIframe;
}

function postMessage(event, data) {
  if (singleTonIframe && singleTonIframe.contentWindow) {
    singleTonIframe.contentWindow.postMessage(
      JSON.stringify({ from: "cusdis", event, data }), "*"
    );
  }
}

function listenEvent(iframe, target) {
  const onMessage = (e) => {
    try {
      const msg = typeof e.data === 'string' ? JSON.parse(e.data) : e.data;
      if (msg.from === "cusdis") {
        if (msg.event === "onload") {
          const isDark = document.documentElement.getAttribute('data-mode') === 'dark' || 
                         (!document.documentElement.hasAttribute('data-mode') && window.matchMedia('(prefers-color-scheme: dark)').matches);
          postMessage("setTheme", isDark ? "dark" : "light");
        } else if (msg.event === "resize") {
          // Add 200px buffer to ensure everything fits
          iframe.style.height = (msg.data + 200) + "px";
        }
      }
    } catch (e2) {}
  };
  window.addEventListener("message", onMessage);
}

function render(target) {
  if (target) {
    target.innerHTML = "";
    target.appendChild(createIframe(target));
  }
}

window.CUSDIS = {
  renderTo: render,
  setTheme: (theme) => postMessage("setTheme", theme),
  initial: () => {
    const target = document.querySelector("#cusdis_thread") || document.querySelector("#cusdis");
    if (target && window.CUSDIS_PREVENT_INITIAL_RENDER !== true) {
      render(target);
    }
  }
};

window.CUSDIS.initial();
