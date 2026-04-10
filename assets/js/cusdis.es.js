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
      label {
        font-weight: 400 !important;
        font-size: 0.85rem !important;
      }
      .dark label, .dark div {
        color: #b3b3b3 !important;
      }
      }
    </style>
  </head>
  <body>
    <div id="root"></div>
    <script src="${iframeJsPath}" type="module">
      
    <\/script>
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
  singleTonIframe.style.colorScheme = "normal";
  singleTonIframe.scrolling = "no";
  singleTonIframe.style.minHeight = "350px";


  return singleTonIframe;
}
function postMessage(event, data) {
  if (singleTonIframe) {
    singleTonIframe.contentWindow.postMessage(
      JSON.stringify({
        from: "cusdis",
        event,
        data
      }), "*"
    );
  }
}
function listenEvent(iframe, target) {
  const darkModeQuery = window.matchMedia("(prefers-color-scheme: dark)");
  const onMessage = (e) => {
    try {
      const msg = JSON.parse(e.data);
      if (msg.from === "cusdis") {
        switch (msg.event) {
          case "onload":
            {
              if (target.dataset.theme === "auto") {
                postMessage(
                  "setTheme",
                  darkModeQuery.matches ? "dark" : "light"
                );
              }
            }
            break;
          case "resize":
            {
              iframe.style.height = (msg.data + 20) + "px"; iframe.style.overflow = "hidden";
            }
            break;
        }
      }
    } catch (e2) {
    }
  };
  window.addEventListener("message", onMessage);
  function onChangeColorScheme(e) {
    const isDarkMode = e.matches;
    if (target.dataset.theme === "auto") {
      postMessage("setTheme", isDarkMode ? "dark" : "light");
    }
  }
  darkModeQuery.addEventListener("change", onChangeColorScheme);
  return () => {
    darkModeQuery.removeEventListener("change", onChangeColorScheme);
    window.removeEventListener("message", onMessage);
  };
}
function render(target) {
  if (target) {
    target.innerHTML = "";
    const iframe = createIframe(target);
    target.appendChild(iframe);
  }
}
window.renderCusdis = render;
window.CUSDIS.renderTo = render;
window.CUSDIS.setTheme = function(theme) {
  postMessage("setTheme", theme);
};
function initial() {
  let target;
  if (window.cusdisElementId) {
    target = document.querySelector(`#${window.cusdisElementId}`);
  } else if (document.querySelector("#cusdis_thread")) {
    target = document.querySelector("#cusdis_thread");
  } else if (document.querySelector("#cusdis")) {
    console.warn(
      "id `cusdis` is deprecated. Please use `cusdis_thread` instead"
    );
    target = document.querySelector("#cusdis");
  }
  if (window.CUSDIS_PREVENT_INITIAL_RENDER === true)
    ;
  else {
    if (target) {
      render(target);
    }
  }
}
window.CUSDIS.initial = initial;
initial();
