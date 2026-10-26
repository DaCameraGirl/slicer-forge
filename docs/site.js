(() => {
  const simulator = document.querySelector("[data-simulator]");
  if (!simulator) return;

  const startButton = simulator.querySelector("[data-sim-start]");
  const resetButton = simulator.querySelector("[data-sim-reset]");
  const status = simulator.querySelector("[data-sim-status]");
  const indicator = simulator.querySelector("[data-sim-indicator]");
  const log = simulator.querySelector("[data-sim-log]");
  const steps = [...simulator.querySelectorAll("[data-sim-step]")];
  const timers = [];
  const stageMessages = [
    "Grouped synthetic CT and MR files into two series.",
    "Applied a simulated moderate de-identification policy.",
    "Recorded geometry checks with no simulated QC errors.",
    "Marked both synthetic series for NRRD output.",
    "Marked two simulated volumes as available to load into a Slicer scene.",
  ];

  function clearTimers() {
    while (timers.length) window.clearTimeout(timers.pop());
  }

  function addLog(message, kind = "") {
    const entry = document.createElement("p");
    entry.className = kind;
    const prompt = document.createElement("span");
    prompt.className = "log-prompt";
    prompt.textContent = kind === "complete" ? "✓" : "›";
    entry.append(prompt, document.createTextNode(` ${message}`));
    log.append(entry);
    log.scrollTop = log.scrollHeight;
  }

  function reset() {
    clearTimers();
    steps.forEach((step) => step.classList.remove("is-active", "is-complete"));
    log.replaceChildren();
    addLog("Awaiting a simulated batch run.");
    indicator.textContent = "Idle";
    status.textContent = "Ready to trace five workflow stages.";
    startButton.disabled = false;
    resetButton.disabled = true;
  }

  function run() {
    reset();
    startButton.disabled = true;
    resetButton.disabled = false;
    indicator.textContent = "Running illustration";
    status.textContent = "Tracing the synthetic workflow. No DICOM data is being processed.";

    stageMessages.forEach((message, index) => {
      timers.push(
        window.setTimeout(() => {
          if (index > 0) steps[index - 1].classList.replace("is-active", "is-complete");
          steps[index].classList.add("is-active");
          addLog(message);

          if (index === stageMessages.length - 1) {
            timers.push(
              window.setTimeout(() => {
                steps[index].classList.replace("is-active", "is-complete");
                indicator.textContent = "Illustration complete";
                status.textContent = "Walkthrough complete. The display is illustrative only.";
                addLog("Synthetic walkthrough complete — no files were changed.", "complete");
                startButton.disabled = false;
              }, 650),
            );
          }
        }, index * 800),
      );
    });
  }

  startButton.addEventListener("click", run);
  resetButton.addEventListener("click", reset);
})();
