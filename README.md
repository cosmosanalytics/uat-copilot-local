# UAT Copilot — Local Model

The same idea as the Gemini-based `uat-helper` app, but with the AI moved fully client-side: a small
vision-language model ([SmolVLM](https://huggingface.co/blog/smolvlm)) downloads once from the Hugging
Face Hub straight into your browser and then runs every inference on your own GPU via **WebGPU** — no
API key, no server, no per-request cost, and your screenshots never leave the tab.

This is genuinely real inference (not scripted/simulated), running via
[Transformers.js](https://huggingface.co/docs/transformers.js). It is a step down in answer quality from
Gemini, and a step up in independence.

## Requirements

- **Chrome or Edge**, reasonably recent (WebGPU support).
- A GPU WebGPU can actually use — a discrete GPU or a modern integrated GPU (Apple Silicon Macs work
  well; older/weak integrated GPUs will be slow or may fail).
- On first load: enough bandwidth/patience to download the model weights once (350 MB–2.2 GB depending
  on which model you pick in the dropdown — cached by the browser afterwards).

## Run it locally

Browser module workers need a real HTTP origin, not `file://`. From this folder:

```bash
python3 -m http.server 8000
```

Then open **http://localhost:8000** in Chrome or Edge.

## Deploy to GitHub Pages (so it works from any device, no local server)

1. Create a new GitHub repo and push these two files (`index.html`, `worker.js`) to it — the `README.md`
   is optional to include.
2. In the repo settings, go to **Pages**, set the source to the branch you pushed (e.g. `main`) and the
   root folder, then save.
3. GitHub gives you a URL like `https://<username>.github.io/<repo>/` — open that in Chrome or Edge.

GitHub Pages serves over `https://`, which is a secure context, so screen sharing
(`getDisplayMedia`) works directly — no local server needed once it's deployed there.

## How to use it

1. Pick a model size (500M-Instruct is a good default balance of speed vs. quality; 256M is faster but
   noticeably weaker; the 2.2B model gives the best answers but is a much bigger download and slower per
   reply).
2. Paste your test script into the box (one step per line, numbering optional) and click **Load model**.
   Wait for the download/progress bars to finish and the button to say "Model loaded ✓".
3. Click **Share screen** and pick the window, tab, or full screen you're testing.
4. Click **What's next?** (or type your own question) — it captures a fresh frame of whatever you're
   sharing and asks the model for guidance based on your test script and the current screen.
5. Click a step in the checklist to mark it done/undone — the model is told which steps are already
   complete so its guidance stays relevant to what's left.

## Notes / limitations

- **Quality vs. Gemini.** SmolVLM is a genuinely small, open model. It's good at describing what's on
  screen, but noticeably less precise than Gemini at the specific "give me structured next-step test
  guidance" task — expect vaguer or occasionally off-base answers, especially on the 256M model.
- **Speed depends entirely on your hardware.** On a strong discrete GPU, replies stream in a couple of
  seconds. On a weak or unsupported GPU, it may fall back to being very slow or fail to load at all — the
  header pill shows whether WebGPU was detected.
- **One conversation turn at a time.** Like the original demo, this only looks at your *current* question
  plus the current screenshot — it doesn't maintain a long chat history (kept simple on purpose; SmolVLM's
  context window is small anyway).
- **Changing models re-downloads.** Switching the dropdown after the first load fetches that model's
  weights separately; they're cached independently per model by the browser.
- **To swap in a different model** (e.g. a larger or newer vision-language model as better small ones
  become available), edit `model_id` handling in `worker.js` — it uses transformers.js's standard
  `AutoProcessor` / `AutoModelForVision2Seq` pattern, so most vision2seq-compatible models on the Hub work
  as a drop-in.
