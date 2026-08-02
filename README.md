# Bill Ledger

A single-page monthly bill checklist that keeps a real payment history — one entry
per bill per month, so editing this month never overwrites last month.

- Pick the date each bill was actually paid
- Tag every payment with the account it came from
- Monthly / quarterly / half-yearly / yearly / one-time schedules, so a bill only
  shows up in the months it's genuinely due
- Two currencies side by side with separate totals
- List or tile layout
- Light and dark themes

## Privacy

**This repository contains no personal data, and the site never sends any.**

There is no server, no analytics, and no network request of any kind. Everything
lives in your own browser's `localStorage`, and the only way data leaves the device
is when *you* tap **Back up**, which writes a JSON file you choose the location for.

Note that a GitHub Pages site is publicly reachable by URL even when the repository
is private — which is exactly why the app ships empty. Your bills arrive by
restoring your own backup file on your own phone.

## Use it on an iPhone

1. Open the site in Safari
2. Share → **Add to Home Screen** — it then runs full-screen like an app
3. Tap the database icon → **Restore from a file** and pick your backup

> Heads-up: a page added to the Home Screen gets its **own** storage, separate from
> Safari's. Set it up in whichever one you plan to use, or restore the same backup
> into both.

## Automatic sync (optional)

Connect a **private** GitHub repo and the ledger saves itself back to one file on
every change — no manual backups, and it follows you between devices. Each save is a
commit, so you get version history for free.

Create the token here — this link goes straight to the right page:

<https://github.com/settings/personal-access-tokens/new>

Give it an expiry, set **Repository access → Only select repositories** to your data
repo, and **Permissions → Repository permissions → Contents: Read and write**. Nothing
else. That token cannot read your other repos or act on your account, and you can
revoke it at any time.

> Looking for it by menu? **Developer settings** is at the very bottom of the sidebar
> under your *profile* settings — it does not appear under a repository's settings,
> and the GitHub **mobile app** doesn't show it at all. Use the link above in a browser.

The token is stored only in your browser, under its own key so it can never end up
inside an exported or synced file, and it is sent only to `api.github.com`.

Sync needs the GitHub Pages version — it makes a cross-origin request, which the
claude.ai artifact build blocks.

## Backups

The database icon shows an amber dot whenever there are changes you haven't backed
up yet. Tap it and choose **Back up to Files / iCloud Drive**.

To make backups land in iCloud automatically:

**Settings → Apps → Safari → Downloads → iCloud Drive**

Every backup then writes to iCloud Drive → Downloads and syncs to your other
devices. Restoring is the same picker in reverse.

## Local development

No build step, no dependencies — `index.html` is the whole application.

```bash
python3 -m http.server 8791
```

Then open <http://localhost:8791>.

## Files

| File | Purpose |
| --- | --- |
| `index.html` | The entire app — markup, styles and logic |
| `manifest.webmanifest` | Add-to-Home-Screen metadata |
| `icon.svg`, `icon.png` | App icon |
| `.nojekyll` | Serve files as-is, skipping Jekyll |
