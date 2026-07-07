# No Middle-Click Paste

A tiny Chrome/Chromium extension that disables **middle-click (primary selection) paste**
inside editable fields on web pages, while leaving other middle-click behaviors —
like *open link in new tab* and autoscroll — untouched.

## Why this exists

On Linux, clicking the middle mouse button pastes the current X11/Wayland *primary
selection* (the last text you highlighted) into whatever is under the cursor. This is a
frequent source of accidental pastes.

GTK apps expose a setting to turn this off:

```ini
# ~/.config/gtk-3.0/settings.ini  (and gtk-4.0/settings.ini)
[Settings]
gtk-enable-primary-paste=false
```

**Chrome/Chromium ignore that setting** and have no built-in toggle of their own, so this
extension fills the gap for web page content.

## Install (unpacked)

1. Open `chrome://extensions`.
2. Enable **Developer mode** (top-right).
3. Click **Load unpacked** and select this folder.

The extension takes effect on newly loaded pages — no browser restart needed.

## How it works

`content.js` runs at `document_start` in every frame and, in the capture phase, cancels
the middle button (`button === 1`) on `mousedown`/`auxclick` **only when the target is an
editable element** (`<input>`, `<textarea>`, or `contenteditable`). Non-editable targets
are left alone, so middle-clicking a link still opens it in a new tab.

## Limitations

- **The address bar (omnibox) is not covered.** It is native Chrome UI, not a web page, so
  no extension API can reach it. The only way to stop paste there is to neutralize the
  middle mouse button at the OS input layer, which disables middle-click everywhere.
- Covers Chrome/Chromium only. For GTK apps use the `gtk-enable-primary-paste` setting
  above; Firefox has `middlemouse.paste` in `about:config`.

## License

MIT — see [LICENSE](LICENSE).
