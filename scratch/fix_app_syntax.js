const fs = require('fs');

let html = fs.readFileSync('scratch/AWS/index.html', 'utf8');

// Replace any \n string literal concatenation in JS with String.fromCharCode(10)
html = html.replace('"[WEBGPU] Initializing in-browser Llama-3.2 engine...\\n"', '"[WEBGPU] Initializing in-browser Llama-3.2 engine..." + String.fromCharCode(10)');
html = html.replace('"[WEBGPU] Initializing in-browser Llama-3.2 engine...\n"', '"[WEBGPU] Initializing in-browser Llama-3.2 engine..." + String.fromCharCode(10)');
html = html.replace('`[WEBGPU PROGRESS] ${report.text}\\n`', '`[WEBGPU PROGRESS] ${report.text}` + String.fromCharCode(10)');

// Also make sure window.addEventListener("DOMContentLoaded", ...) also runs if document is already ready
const readyCheck = `
    function initApp() {
      if (window._appInitialized) return;
      window._appInitialized = true;
      syncHeaderPasscodeUi();
      renderSidebarGitHub(CACHED_GITHUB_TELEMETRY, false);
      renderCanvas();
      renderDrawer();
      startUndoTimerLoop();
      if (ownerPasscode) {
        executeLiveAwsPipeline("Session Auto-Unlock (Live GitHub + AWS)", null, true);
      }
    }
    if (document.readyState === "loading") {
      window.addEventListener("DOMContentLoaded", initApp);
    } else {
      initApp();
    }
`;

// Replace DOMContentLoaded block
html = html.replace(
  /window\.addEventListener\("DOMContentLoaded",\s*\(\)\s*=>\s*\{[\s\S]*?\}\);/,
  readyCheck.trim()
);

fs.writeFileSync('scratch/AWS/index.html', html, 'utf8');
fs.writeFileSync('scratch/AWS/ai_factory_ambient_canvas.html', html, 'utf8');
fs.writeFileSync('ai_factory_ambient_canvas.html', html, 'utf8');
fs.writeFileSync('scratch/AWS/.nojekyll', '', 'utf8');

console.log('Sanitized index.html and added instant initApp fallback!');
