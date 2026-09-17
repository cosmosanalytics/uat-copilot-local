// Runs the vision-language model entirely in this worker thread, on the GPU via WebGPU.
// No network calls happen here except the one-time model weight download from the
// Hugging Face Hub (cached by the browser after the first load).
 
import {
  AutoProcessor,
  AutoModelForVision2Seq,
  TextStreamer,
  InterruptableStoppingCriteria,
  load_image,
} from "https://cdn.jsdelivr.net/npm/@huggingface/transformers@3.7.1/+esm";
 
const MAX_NEW_TOKENS = 512;
 
async function checkWebGPU() {
  try {
    if (!("gpu" in navigator)) {
      throw new Error("WebGPU is not available in this browser.");
    }
    const adapter = await navigator.gpu.requestAdapter();
    if (!adapter) {
      throw new Error("WebGPU is not supported (no GPU adapter found).");
    }
  } catch (e) {
    self.postMessage({ status: "error", data: e.toString() });
    return false;
  }
  return true;
}
 
// Lazy-loaded singleton so the model is only ever fetched/instantiated once.
class VisionModel {
  static model_id = null;
  static processor = null;
  static model = null;
 
  static async getInstance(model_id, progress_callback) {
    if (this.model_id !== model_id) {
      // Model choice changed — drop the old instance and load the new one.
      this.model_id = model_id;
      this.processor = AutoProcessor.from_pretrained(model_id, { progress_callback });
      this.model = AutoModelForVision2Seq.from_pretrained(model_id, {
        dtype: "fp32",
        device: "webgpu",
        progress_callback,
      });
    }
    return Promise.all([this.processor, this.model]);
  }
}
 
const stopping_criteria = new InterruptableStoppingCriteria();
 
async function generate(model_id, systemText, userText, imageDataUrl) {
  const [processor, model] = await VisionModel.getInstance(model_id, (x) => {
    self.postMessage(x);
  });
 
  const image = await load_image(imageDataUrl);
 
  const messages = [
    { role: "system", content: [{ type: "text", text: systemText }] },
    {
      role: "user",
      content: [
        { type: "image", image },
        { type: "text", text: userText },
      ],
    },
  ];
 
  const text = processor.apply_chat_template(messages, { add_generation_prompt: true });
  const inputs = await processor(text, [image]);
 
  let startTime;
  let numTokens = 0;
  let tps = 0;
  const token_callback_function = () => {
    startTime ??= performance.now();
    if (numTokens++ > 0) tps = (numTokens / (performance.now() - startTime)) * 1000;
  };
  const callback_function = (output) => {
    self.postMessage({ status: "update", output, tps, numTokens });
  };
 
  const streamer = new TextStreamer(processor.tokenizer, {
    skip_prompt: true,
    skip_special_tokens: true,
    callback_function,
    token_callback_function,
  });
 
  self.postMessage({ status: "start" });
 
  stopping_criteria.reset();
  try {
    const { sequences } = await model.generate({
      ...inputs,
      do_sample: false,
      repetition_penalty: 1.15,
      max_new_tokens: MAX_NEW_TOKENS,
      streamer,
      stopping_criteria,
      return_dict_in_generate: true,
    });
 
    const decoded = processor.batch_decode(sequences, { skip_special_tokens: true });
    self.postMessage({ status: "complete", output: decoded });
  } catch (e) {
    self.postMessage({ status: "error", data: e.toString() });
  }
}
 
self.addEventListener("message", async (e) => {
  const { type, data } = e.data;
  switch (type) {
    case "check": {
      const ok = await checkWebGPU();
      if (ok) self.postMessage({ status: "webgpu-ok" });
      break;
    }
    case "load":
      self.postMessage({ status: "loading", data: "Loading model…" });
      try {
        await VisionModel.getInstance(data.model_id, (x) => self.postMessage(x));
        self.postMessage({ status: "ready" });
      } catch (e) {
        self.postMessage({ status: "error", data: e.toString() });
      }
      break;
    case "generate":
      generate(data.model_id, data.systemText, data.userText, data.image);
      break;
    case "interrupt":
      stopping_criteria.interrupt();
      break;
  }
});
