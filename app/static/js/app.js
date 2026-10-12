(function () {
  const t = JSON.parse(document.getElementById("ui-strings").textContent);
  const examples = JSON.parse(document.getElementById("examples").textContent);
  const lang = document.body.dataset.lang;

  const form = document.getElementById("check-form");
  const textarea = document.getElementById("message");
  const imageInput = document.getElementById("image");
  const submit = document.getElementById("submit");
  const errorBox = document.getElementById("error");
  const result = document.getElementById("result");
  let lastCheckId = null;

  const el = (tag, attrs = {}, ...children) => {
    const node = document.createElement(tag);
    Object.entries(attrs).forEach(([k, v]) => (k === "class" ? (node.className = v) : node.setAttribute(k, v)));
    children.flat().forEach((c) => node.append(c instanceof Node ? c : document.createTextNode(c)));
    return node;
  };

  function showError(message) {
    errorBox.textContent = message;
    errorBox.hidden = false;
  }

  function busy(on) {
    submit.disabled = on;
    submit.textContent = on ? submit.dataset.busy : submit.dataset.idle;
  }

  // Message text with every flagged span wrapped in <mark>
  function renderBubble(text, flags) {
    const spans = flags.flatMap((f) => f.spans).sort((a, b) => a[0] - b[0]);
    const merged = [];
    spans.forEach(([s, e]) => {
      const last = merged[merged.length - 1];
      if (last && s <= last[1]) last[1] = Math.max(last[1], e);
      else merged.push([s, e]);
    });
    const bubble = document.getElementById("bubble");
    bubble.replaceChildren();
    let pos = 0;
    merged.forEach(([s, e]) => {
      if (s > pos) bubble.append(text.slice(pos, s));
      bubble.append(el("mark", {}, text.slice(s, e)));
      pos = e;
    });
    if (pos < text.length) bubble.append(text.slice(pos));
    return merged.length > 0;
  }

  function renderLink(link) {
    const i = link.url.toLowerCase().lastIndexOf(link.domain.toLowerCase());
    const url = el("span", { class: "url" });
    if (link.domain && i >= 0) {
      url.append(link.url.slice(0, i), el("b", {}, link.url.slice(i, i + link.domain.length)), link.url.slice(i + link.domain.length));
    } else {
      url.append(link.url);
    }
    const verdict = link.official
      ? el("span", { class: "verdict is-official" }, `${t.goes_to} ${link.domain}: ${t.official}`)
      : el("span", { class: "verdict not-official" }, `${t.goes_to} ${link.domain}: ${t.not_official}`);
    return el("li", {}, url, verdict);
  }

  function render(report) {
    lastCheckId = report.check_id || null;
    result.className = `result v-${report.verdict}`;

    const hasMarks = renderBubble(report.text, report.flags);
    document.getElementById("hint").hidden = !hasMarks;

    const stamp = document.getElementById("stamp");
    stamp.textContent = report.label;
    stamp.classList.remove("press");
    void stamp.offsetWidth; // restart the press animation
    stamp.classList.add("press");

    const headline = document.getElementById("headline");
    headline.textContent = report.headline;

    const flags = document.getElementById("flags");
    flags.replaceChildren(...report.flags.map((f) =>
      el("li", { class: f.weight >= 0.7 ? "w-high" : f.weight >= 0.4 ? "w-mid" : "w-low" }, el("strong", {}, f.title), el("p", {}, f.detail))
    ));
    document.getElementById("flags-block").hidden = report.flags.length === 0;

    const links = document.getElementById("links");
    links.replaceChildren(...report.links.map(renderLink));
    document.getElementById("links-block").hidden = report.links.length === 0;

    document.getElementById("actions").replaceChildren(...report.actions.map((a) => el("li", {}, a)));

    const feedback = document.getElementById("feedback");
    feedback.hidden = !lastCheckId;
    feedback.querySelectorAll("button").forEach((b) => (b.hidden = false, b.disabled = false));
    document.getElementById("thanks").hidden = true;

    result.hidden = false;
    headline.focus({ preventScroll: true });
    result.scrollIntoView({ behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth", block: "start" });
  }

  async function send() {
    errorBox.hidden = true;
    const file = imageInput && imageInput.files[0];
    const text = textarea.value.trim();
    if (!file && !text) {
      showError(t.empty);
      textarea.focus();
      return;
    }
    busy(true);
    try {
      let res;
      if (file && !text) {
        const body = new FormData();
        body.append("image", file);
        body.append("lang", lang);
        res = await fetch("/api/check-image", { method: "POST", body });
      } else {
        res = await fetch("/api/check", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ text, lang }),
        });
      }
      const data = await res.json().catch(() => ({}));
      if (!res.ok) {
        showError(res.status === 429 ? t.too_many : data.error && typeof data.error === "string" ? data.error : t.error);
        return;
      }
      render(data);
    } catch (e) {
      showError(t.error);
    } finally {
      busy(false);
    }
  }

  form.addEventListener("submit", (e) => { e.preventDefault(); send(); });

  document.querySelectorAll("[data-example]").forEach((b) =>
    b.addEventListener("click", () => {
      textarea.value = examples[b.dataset.example];
      if (imageInput) { imageInput.value = ""; imageInput.closest(".upload").classList.remove("has-file"); }
      send();
    })
  );

  if (imageInput) {
    const label = document.querySelector("[data-upload-label]");
    const original = label.textContent;
    imageInput.addEventListener("change", () => {
      const f = imageInput.files[0];
      label.textContent = f ? f.name : original;
      imageInput.closest(".upload").classList.toggle("has-file", Boolean(f));
      if (f) textarea.value = "";
    });
  }

  document.querySelectorAll("[data-correct]").forEach((b) =>
    b.addEventListener("click", async () => {
      if (!lastCheckId) return;
      document.querySelectorAll("[data-correct]").forEach((x) => (x.disabled = true));
      try {
        await fetch("/api/feedback", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ check_id: lastCheckId, correct: b.dataset.correct === "true" }),
        });
        document.querySelectorAll("[data-correct]").forEach((x) => (x.hidden = true));
        document.getElementById("thanks").hidden = false;
      } catch (e) {
        document.querySelectorAll("[data-correct]").forEach((x) => (x.disabled = false));
      }
    })
  );
})();
