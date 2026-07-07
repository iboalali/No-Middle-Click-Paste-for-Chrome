// Block middle-click (button 1) primary-selection paste in editable fields only.
// Middle-clicks on links/plain content are left alone, so "open in new tab"
// and autoscroll still work.

function isEditable(el) {
  if (!el || el.nodeType !== 1) return false;
  const tag = el.tagName;
  if (tag === "INPUT" || tag === "TEXTAREA") return true;
  if (el.isContentEditable) return true;
  return false;
}

function blockMiddlePaste(e) {
  if (e.button === 1 && isEditable(e.target)) {
    e.preventDefault();
    e.stopPropagation();
  }
}

// Capture phase so we run before the page's own handlers and the default action.
document.addEventListener("mousedown", blockMiddlePaste, true);
document.addEventListener("auxclick", blockMiddlePaste, true);
