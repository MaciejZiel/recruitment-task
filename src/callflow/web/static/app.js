/* callflow web app shell: routing, new-analysis form, progress polling and history.
   The result view itself is rendered by results.js (window.CallflowResults).
   All API text goes into the DOM through textContent / createElement, never innerHTML. */
"use strict";

const POLL_MS = 2000;
const STEPS = ["Wczytanie transkrypcji", "Analiza AI", "Weryfikacja cytatów", "Raport"];
const STATUS_LABELS = { queued: "w kolejce", running: "w toku", done: "gotowe", error: "błąd" };
const DEFAULT_SOURCE = "wklejona-transkrypcja.md";

const state = {
  examples: [],
  exampleId: null,
  exampleText: null,
  sourceName: null,
  routeToken: 0,
  pollTimer: null,
  tickTimer: null,
};

const $ = (id) => document.getElementById(id);

/* ---------- DOM helpers ---------- */

function el(tag, attrs = {}, ...children) {
  const node = document.createElement(tag);
  for (const [key, value] of Object.entries(attrs)) {
    if (value === null || value === undefined || value === false) continue;
    if (key === "class") node.className = value;
    else if (key === "text") node.textContent = value;
    else if (key.startsWith("on")) node.addEventListener(key.slice(2), value);
    else node.setAttribute(key, value === true ? "" : String(value));
  }
  for (const child of children.flat()) {
    if (child === null || child === undefined || child === false) continue;
    node.append(child instanceof Node ? child : document.createTextNode(String(child)));
  }
  return node;
}

function showMessage(node, text) {
  node.textContent = text || "";
  node.hidden = !text;
}

function toast(text) {
  const node = $("toast");
  node.textContent = text;
  node.classList.add("show");
  clearTimeout(toast.timer);
  toast.timer = setTimeout(() => node.classList.remove("show"), 3000);
}

function formatDuration(seconds) {
  const total = Math.max(0, Math.floor(Number(seconds) || 0));
  const minutes = Math.floor(total / 60);
  return `${minutes}:${String(total % 60).padStart(2, "0")}`;
}

function formatTime(value) {
  if (!value) return "";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return String(value);
  return date.toLocaleString("pl-PL", { dateStyle: "short", timeStyle: "short" });
}

/* ---------- API ---------- */

class ApiError extends Error {}

async function api(path, options = {}) {
  let response;
  try {
    response = await fetch(path, {
      ...options,
      headers: { Accept: "application/json", ...(options.body ? { "Content-Type": "application/json" } : {}) },
    });
  } catch {
    throw new ApiError("Brak połączenia z serwerem callflow. Sprawdź, czy callflow-web działa.");
  }
  let data = null;
  try {
    data = await response.json();
  } catch {
    data = null;
  }
  if (!response.ok) {
    const detail = data && typeof data.error === "string" ? data.error : `HTTP ${response.status}`;
    throw new ApiError(detail);
  }
  return data;
}

/* ---------- Routing ---------- */

function stopTimers() {
  clearTimeout(state.pollTimer);
  clearInterval(state.tickTimer);
  state.pollTimer = null;
  state.tickTimer = null;
}

function showView(name) {
  for (const view of document.querySelectorAll(".view")) view.hidden = view.id !== `view-${name}`;
  const nav = name === "history" ? "history" : name === "new" ? "new" : null;
  for (const link of document.querySelectorAll("[data-nav]")) {
    if (link.dataset.nav === nav) link.setAttribute("aria-current", "page");
    else link.removeAttribute("aria-current");
  }
  showMessage($("global-error"), "");
}

function focusHeading(view) {
  const heading = document.querySelector(`#view-${view} h1`);
  if (heading) {
    if (!heading.hasAttribute("tabindex")) heading.setAttribute("tabindex", "-1");
    heading.focus({ preventScroll: true });
  }
  window.scrollTo(0, 0);
}

function route() {
  stopTimers();
  const token = ++state.routeToken;
  const hash = location.hash || "#/new";
  const runMatch = hash.match(/^#\/run\/([^/]+)$/);
  if (runMatch) openRun(decodeURIComponent(runMatch[1]), token);
  else if (hash === "#/history") openHistory(token);
  else {
    showView("new");
    document.title = "Po rozmowie z klientem · callflow";
  }
}

/* ---------- 1. New analysis ---------- */

async function loadExamples() {
  const box = $("examples");
  try {
    state.examples = (await api("/api/examples")) || [];
  } catch (error) {
    box.replaceChildren(el("span", { class: "muted", text: `Nie udało się wczytać przykładów: ${error.message}` }));
    return;
  }
  if (!state.examples.length) {
    box.replaceChildren(el("span", { class: "muted", text: "Brak przykładów na serwerze." }));
    return;
  }
  box.replaceChildren(
    ...state.examples.map((example) =>
      el("button", {
        type: "button",
        class: "btn btn-ghost btn-sm example-btn",
        "aria-pressed": "false",
        "data-id": example.id,
        text: example.title || example.transcript_name || example.id,
        onclick: () => useExample(example),
      }),
    ),
  );
}

function useExample(example) {
  $("transcript").value = example.transcript || "";
  state.exampleId = example.id;
  state.exampleText = $("transcript").value;
  state.sourceName = example.transcript_name || `${example.id}.md`;
  showMessage($("new-error"), "");
  updateFormState();
}

function readFile(event) {
  const file = event.target.files && event.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.addEventListener("load", () => {
    $("transcript").value = String(reader.result || "");
    state.exampleId = null;
    state.exampleText = null;
    state.sourceName = file.name;
    showMessage($("new-error"), "");
    updateFormState();
  });
  reader.addEventListener("error", () => showMessage($("new-error"), `Nie udało się odczytać pliku ${file.name}.`));
  reader.readAsText(file, "UTF-8");
  event.target.value = "";
}

function onTranscriptInput() {
  // An edited example is no longer the example: its saved result would not match the text.
  if (state.exampleId && $("transcript").value !== state.exampleText) {
    state.exampleId = null;
    state.exampleText = null;
    state.sourceName = null;
  }
  updateFormState();
}

function updateFormState() {
  const text = $("transcript").value;
  const lines = text.split("\n").filter((line) => line.trim()).length;
  for (const button of document.querySelectorAll(".example-btn")) {
    button.setAttribute("aria-pressed", String(button.dataset.id === state.exampleId));
  }
  $("run-example").disabled = !state.exampleId;
  const source = state.sourceName || (text.trim() ? DEFAULT_SOURCE : "");
  $("source-info").textContent = source ? `Źródło: ${source} · niepustych linii: ${lines}` : "";
}

function formPayload(mode) {
  const payload = {
    transcript: $("transcript").value,
    source_name: state.sourceName || DEFAULT_SOURCE,
    meeting_date: $("meeting-date").value || null,
    vendor: $("vendor").value.trim(),
    effort: $("effort").value,
    mode,
  };
  if (mode === "example") payload.example_id = state.exampleId;
  return payload;
}

function validate(payload) {
  if (!payload.transcript.trim()) return "Wklej transkrypcję, wczytaj plik albo wybierz przykład.";
  if (!payload.vendor) return "Podaj nazwę firmy.";
  return null;
}

async function submitRun(mode) {
  const errorBox = $("new-error");
  const payload = formPayload(mode);
  const problem = validate(payload);
  if (problem) {
    showMessage(errorBox, problem);
    (payload.transcript.trim() ? $("vendor") : $("transcript")).focus();
    return;
  }
  showMessage(errorBox, "");
  const buttons = [$("run-live"), $("run-example")];
  for (const button of buttons) button.setAttribute("aria-busy", "true");
  $("run-live").disabled = true;
  $("run-example").disabled = true;
  try {
    const created = await api("/api/runs", { method: "POST", body: JSON.stringify(payload) });
    location.hash = `#/run/${encodeURIComponent(created.id)}`;
  } catch (error) {
    showMessage(errorBox, error.message);
  } finally {
    for (const button of buttons) button.removeAttribute("aria-busy");
    $("run-live").disabled = false;
    updateFormState();
  }
}

/* ---------- 2. Progress ---------- */

async function openRun(id, token) {
  let run;
  try {
    run = await api(`/api/runs/${encodeURIComponent(id)}`);
  } catch (error) {
    if (token !== state.routeToken) return;
    showView("progress");
    renderProgressError(id, error.message);
    return;
  }
  if (token !== state.routeToken) return;
  if (run.status === "done") {
    await openResult(run, token);
    return;
  }
  showView("progress");
  focusHeading("progress");
  renderProgress(run);
  if (run.status === "queued" || run.status === "running") startPolling(run, token);
}

function startPolling(run, token) {
  state.lastRun = run;
  state.lastPollAt = Date.now();
  state.tickTimer = setInterval(tickElapsed, 1000);
  const poll = async () => {
    let next;
    try {
      next = await api(`/api/runs/${encodeURIComponent(run.id)}`);
    } catch (error) {
      if (token !== state.routeToken) return;
      $("progress-status").textContent = `${error.message} Ponawiam…`;
      state.pollTimer = setTimeout(poll, POLL_MS);
      return;
    }
    if (token !== state.routeToken) return;
    state.lastRun = next;
    state.lastPollAt = Date.now();
    renderProgress(next);
    if (next.status === "done") {
      stopTimers();
      await openResult(next, token);
    } else if (next.status === "error") {
      stopTimers();
    } else {
      state.pollTimer = setTimeout(poll, POLL_MS);
    }
  };
  state.pollTimer = setTimeout(poll, POLL_MS);
}

function tickElapsed() {
  const run = state.lastRun;
  if (!run || (run.status !== "running" && run.status !== "queued")) return;
  const base = Number(run.elapsed_s) || 0;
  $("elapsed").textContent = formatDuration(base + (Date.now() - state.lastPollAt) / 1000);
}

// The API reports only queued/running/done/error, so the current step is inferred:
// queued = loading, running = AI analysis (verification and report follow within seconds).
function currentStep(run) {
  if (run.status === "queued") return 0;
  if (run.status === "running") return 1;
  if (run.status === "error") return run.started_at ? 1 : 0;
  return STEPS.length;
}

const STEP_STATES = {
  done: ["step done", "zakończono"],
  active: ["step active", "w toku"],
  failed: ["step failed", "przerwano"],
  pending: ["step", "oczekuje"],
};

function renderSteps(run) {
  const current = currentStep(run);
  return STEPS.map((label, index) => {
    let key = "pending";
    if (index < current) key = "done";
    else if (index === current) key = run.status === "error" ? "failed" : "active";
    const [cls, spoken] = STEP_STATES[key];
    const note = key === "active" && index === 1 && run.mode !== "example" ? " (zwykle 1–5 min)" : "";
    return el(
      "li",
      { class: cls, "aria-current": key === "active" ? "step" : null },
      el("span", {}, label, el("span", { class: "step-note", text: note })),
      el("span", { class: "visually-hidden", text: `: ${spoken}` }),
    );
  });
}

function renderProgress(run) {
  const failed = run.status === "error";
  $("progress-title").textContent = failed ? "Analiza nie powiodła się" : "Analiza w toku";
  document.title = `${$("progress-title").textContent} · callflow`;
  const mode = run.mode === "example" ? "zapisany wynik przykładu" : "analiza Claude";
  $("progress-source").textContent = `Źródło: ${run.source_name || "—"} · ${mode} · start: ${formatTime(run.created_at)}`;
  $("steps").replaceChildren(...renderSteps(run));
  $("elapsed").textContent = formatDuration(run.elapsed_s);
  $("progress-status").textContent = `Status: ${STATUS_LABELS[run.status] || run.status}`;
  const warnings = Array.isArray(run.warnings) ? run.warnings : [];
  $("progress-warnings").replaceChildren(...warnings.map((text) => el("li", { text: String(text) })));
  $("progress-warnings").hidden = !warnings.length;
  showMessage($("progress-error"), failed ? run.error || "Nieznany błąd." : "");
  $("progress-actions").hidden = !failed;
}

function renderProgressError(id, message) {
  $("progress-title").textContent = "Nie znaleziono analizy";
  $("progress-source").textContent = `Identyfikator: ${id}`;
  $("steps").replaceChildren();
  $("elapsed").textContent = "0:00";
  $("progress-status").textContent = "";
  $("progress-warnings").hidden = true;
  showMessage($("progress-error"), message);
  $("progress-actions").hidden = false;
  focusHeading("progress");
}

/* ---------- 3. Result (rendered by results.js) ---------- */

async function openResult(run, token) {
  let result;
  try {
    result = await api(`/api/runs/${encodeURIComponent(run.id)}/result`);
  } catch (error) {
    if (token !== state.routeToken) return;
    showView("progress");
    renderProgress(run);
    showMessage($("progress-error"), `Nie udało się pobrać wyniku: ${error.message}`);
    $("progress-actions").hidden = false;
    return;
  }
  if (token !== state.routeToken) return;
  const container = $("result-container");
  container.replaceChildren();
  showView("result");
  const client = (run.summary && run.summary.client) || (result.outbox && result.outbox.client) || "";
  document.title = `Po rozmowie${client ? `: ${client}` : ""} · callflow`;
  if (window.CallflowResults && typeof window.CallflowResults.render === "function") {
    try {
      window.CallflowResults.render(container, run, result);
    } catch (error) {
      console.error(error);
      container.replaceChildren(resultFallback(run, "Nie udało się wyświetlić wyniku w aplikacji."));
    }
  } else {
    container.replaceChildren(resultFallback(run, "Widok wyniku nie jest dostępny w tej wersji aplikacji."));
  }
  focusHeading("result");
}

function resultFallback(run, message) {
  const files = run.files || {};
  return el(
    "div",
    {},
    el("div", { class: "hero" }, el("div", { class: "wrap" }, el("h1", { tabindex: "-1", text: "Wynik analizy" }))),
    el(
      "div",
      { class: "wrap" },
      el(
        "div",
        { class: "panel" },
        el("p", { class: "alert", text: message }),
        files.report_html
          ? el("a", { class: "btn btn-primary", href: files.report_html, target: "_blank", rel: "noopener", text: "Otwórz report.html" })
          : el("p", { text: "Raport HTML nie jest dostępny." }),
      ),
    ),
  );
}

/* ---------- 4. History ---------- */

async function openHistory(token) {
  showView("history");
  document.title = "Historia analiz · callflow";
  focusHeading("history");
  const status = $("history-status");
  const list = $("history-list");
  status.textContent = "Ładowanie…";
  let runs;
  try {
    runs = (await api("/api/runs")) || [];
  } catch (error) {
    if (token !== state.routeToken) return;
    status.textContent = "";
    showMessage($("global-error"), `Nie udało się wczytać historii: ${error.message}`);
    list.replaceChildren();
    return;
  }
  if (token !== state.routeToken) return;
  runs.sort((a, b) => String(b.created_at || "").localeCompare(String(a.created_at || "")));
  status.textContent = runs.length ? `Analiz: ${runs.length}` : "Brak analiz. Zacznij od zakładki „Nowa analiza”.";
  list.replaceChildren(...runs.map(historyRow));
}

function summaryLine(run) {
  const s = run.summary;
  if (run.status === "error") return run.error ? `Błąd: ${run.error}` : "Błąd analizy.";
  if (!s) return run.status === "done" ? "" : "Analiza jeszcze trwa.";
  const parts = [
    s.client,
    s.meeting_date || "data nieznana",
    `pozycji: ${s.items}`,
    `zabezpieczeń: ${s.guardrails}`,
    `szkiców: ${s.drafts}`,
    `cytaty: ${s.quotes_verified}/${s.quotes_total}`,
  ];
  if (s.issues) parts.push(`ostrzeżeń: ${s.issues}`);
  return parts.filter((part) => part !== null && part !== undefined && part !== "").join(" · ");
}

function historyRow(run) {
  const href = `#/run/${encodeURIComponent(run.id)}`;
  const mode = run.mode === "example" ? "zapisany przykład" : "analiza Claude";
  const time = run.elapsed_s !== null && run.elapsed_s !== undefined ? ` · czas ${formatDuration(run.elapsed_s)}` : "";
  const action = run.status === "done" ? "Otwórz wynik" : run.status === "error" ? "Szczegóły" : "Pokaż przebieg";
  return el(
    "li",
    { class: "history-row" },
    el(
      "div",
      {},
      el("h2", { text: run.source_name || run.id }),
      el(
        "div",
        { class: "badges" },
        el("span", { class: `badge status-${run.status}`, text: STATUS_LABELS[run.status] || run.status }),
      ),
      el("p", { text: `${formatTime(run.created_at)} · ${mode}${time}` }),
      el("p", { text: summaryLine(run) }),
    ),
    el("a", { class: "btn btn-secondary btn-sm", href, text: action, "aria-label": `${action}: ${run.source_name || run.id}` }),
  );
}

/* ---------- Init ---------- */

function init() {
  $("new-form").addEventListener("submit", (event) => {
    event.preventDefault();
    submitRun("live");
  });
  $("run-example").addEventListener("click", () => submitRun("example"));
  $("file").addEventListener("change", readFile);
  $("transcript").addEventListener("input", onTranscriptInput);
  window.addEventListener("hashchange", route);
  updateFormState();
  loadExamples();
  route();
}

init();
