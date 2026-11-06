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
3. Tap **More** → **Restore from a file** and pick your backup

> Heads-up: a page added to the Home Screen gets its **own** storage, separate from
> Safari's. Set it up in whichever one you plan to use, or restore the same backup
> into both.

## Logging a spend

Tap the big **+** at the bottom. The keypad is already up: type the amount, and
your last-used card is already picked — tap a different one if needed, tap what
it was for (Groceries, Dining, Fuel…), optionally type where, and **Save**. A
place you've used before fills in its category by itself.

Opening `…/bill-ledger/#add` goes straight to that screen.

Updating a card or account balance no longer deletes the spends logged before
it: they're marked settled, so they stop counting toward the live balance but
stay in **Activity** with their categories.

## Log from anywhere on your iPhone (Back Tap)

Double-tap the back of the phone and a Shortcut asks *which card*, *how much*
and *what for* — no need to open the app. Needs **Automatic sync** (below).

1. On the iPhone open **More → Get the "Log Spend" shortcut** (or open
   `Log Spend.shortcut` from this site) and tap **Add Shortcut**. When it asks,
   paste a GitHub token with **Contents: Read and write** on your data repo —
   the same kind of token sync uses.
2. **Settings → Accessibility → Touch → Back Tap → Double Tap → Log Spend**.
3. Open the ledger once after updating, so it publishes your card list for the
   shortcut.

How it works: the shortcut reads your card list from the `quick` block the app
writes into `bill-ledger.json`, then drops one small file per spend into
`inbox/` in the data repo. The next time the app opens (or comes back to the
foreground) it files those as spends, saves the ledger, and only then deletes
the inbox files. Each entry's id comes from its file name, so a retry never
counts a spend twice. An entry naming a card that doesn't exist is left in the
inbox and flagged under **More**.

The token lives inside the shortcut on your phone. `tools/build_shortcut.py`
regenerates the shortcut (then sign it with
`shortcuts sign --mode anyone --input unsigned.shortcut --output "Log Spend.shortcut"`).

## Log Apple Pay taps automatically

`Log Apple Pay.shortcut` runs from a Wallet **Transaction** automation, so every
Apple Pay tap is logged with its card, amount and merchant — no typing. Setup is
under **More → Log Apple Pay taps automatically**: add the shortcut (paste the
token from **Copy my sync token**), then in Shortcuts create an Automation →
Transaction → your cards → Run Immediately → Run Shortcut *Log Apple Pay* with
*Shortcut Input* as its input.

Taps land in the same `inbox/` as the Back Tap shortcut. A merchant you've used
before gets its category automatically. If Wallet calls a card something the
ledger doesn't recognise ("Gold Card"), the tap waits under **More → Waiting for
a card**; pick the card once and that name is remembered (`cardAlias` in the
ledger file). Zero-amount taps such as transit are discarded.

## Updating a balance shows what was missed

**Update balance** (on a card or account) and **Update all balances** show what
the app expected next to what you type. A higher card balance than expected —
or a lower account balance — is spending you didn't log; tick-on by default, it
is filed as an *unlogged* spend (already settled, since the new reading includes
it), optionally with a category. Activity tags those entries, and each card shows
how much went unlogged over the last 90 days — a measure of how far the app
drifts. In **Update all balances**, a card left blank keeps its current reading.

## Reminders

The data panel can add every bill to your calendar as a repeating event with an
alert — 9am on the due date, or 1, 3 or 7 days before. Recurring bills repeat on
their own, so you only redo this when you add or change a bill.

Tick **Also remind me to update each card's balance** and each card with a
statement day also gets a monthly 9am reminder the morning after its statement
closes — when the card app's figure is freshest — pointing you at
**Update balance**, which then shows anything you forgot to log.

It generates a standard `.ics` file, so the OS does the reminding: no notification
permissions, no service worker, and it rides iCloud to your other devices. Events
carry stable UIDs, so re-adding them updates the existing entries rather than
duplicating, provided you keep them in the same calendar.

## Automatic sync (optional)

Connect a **private** GitHub repo and the ledger saves itself back to one file on
every change — no manual backups, and it follows you between devices. Each save is a
commit, so you get version history for free.

Create the token here — this link goes straight to the right page:

<https://github.com/settings/personal-access-tokens/new>

Give it an expiry and set **Repository access → Only select repositories** to your
data repo. Then under **Permissions**, click **Repository permissions** to *expand
it* — it starts collapsed, which makes the setting look missing. The list is
alphabetical: scroll to **Contents** and change the dropdown on its right from *No
access* to **Read and write**. Leave every other row alone.

When two devices (say the Home Screen app and Safari, or phone and Mac) both
change things before syncing, the copies are **merged record by record**, not
replaced. Each device keeps a private fingerprint of every record as of its last
sync, so it can tell something you added from something the other device
deleted, and an edit on one side from an edit on both; only a record edited on
both sides falls back to the newer copy. A save that finds GitHub changed
underneath it merges and retries instead of overwriting.

That token cannot read your other repos or act on your account, and you can revoke it
at any time.

> Seeing tick-boxes (`repo`, `workflow`, `gist`) instead of dropdowns? That's the
> *classic* token page. Use the link above for the fine-grained one. A classic token
> with `repo` ticked also works, but it grants access to **all** your repositories.

> Looking for it by menu? **Developer settings** is at the very bottom of the sidebar
> under your *profile* settings — it does not appear under a repository's settings,
> and the GitHub **mobile app** doesn't show it at all. Use the link above in a browser.

The token is stored only in your browser, under its own key so it can never end up
inside an exported or synced file, and it is sent only to `api.github.com`.

Sync needs the GitHub Pages version — it makes a cross-origin request, which the
claude.ai artifact build blocks.

## Backups

**More** shows an amber dot whenever there are changes you haven't backed
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
| `Log Spend.shortcut` | Signed iPhone Shortcut for Back Tap logging |
| `Log Apple Pay.shortcut` | Signed Shortcut for the Wallet transaction automation |
| `tools/build_shortcut.py` | Regenerates either shortcut (`applepay` as 2nd argument) |
| `.nojekyll` | Serve files as-is, skipping Jekyll |
