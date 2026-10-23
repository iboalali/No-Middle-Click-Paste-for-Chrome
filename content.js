// Block middle-click (button 1) primary-selection paste in editable fields only.
// Middle-clicks on links/plain content are left alone, so "open in new tab"
// and autoscroll still work.

// The paste event a middle-click triggers arrives right after mouseup, in the
// same task. The window only has to cover that gap, so Ctrl+V stays unaffected.
const PASTE_WINDOW_MS = 100;

let lastMiddleUpAt = -Infinity;

// Events from inside a shadow root are retargeted to the host element at the
// document level, so the real target is the first entry of the composed path.
function realTarget(e) {
  return e.composedPath ? e.composedPath()[0] : e.target;
}

function isEditable(el) {
  if (!el || el.nodeType !== 1) return false;
  const tag = el.tagName;
  if (tag === "INPUT" || tag === "TEXTAREA") return true;
  if (el.isContentEditable) return true;
  return false;
}

function blockMiddlePaste(e) {
  if (e.button !== 1) return;
  if (e.type === "mouseup") lastMiddleUpAt = performance.now();
  if (isEditable(realTarget(e))) {
    e.preventDefault();
    e.stopPropagation();
  }
}

function blockSelectionPaste(e) {
  if (performance.now() - lastMiddleUpAt < PASTE_WINDOW_MS) {
    e.preventDefault();
    e.stopImmediatePropagation();
  }
}

// Capture phase on window so we run before the page's own handlers and the
// default action. Chrome on Linux pastes on mouseup, not mousedown.
for (const type of ["mousedown", "mouseup", "auxclick"]) {
  window.addEventListener(type, blockMiddlePaste, true);
}
window.addEventListener("paste", blockSelectionPaste, true);
