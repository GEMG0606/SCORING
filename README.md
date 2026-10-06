# Quiz Score Desk

A phone-controlled quiz scoreboard with slide remote control.

- **Control page (phone):** add/subtract points per team, switch highlight mode, send NEXT/PREV.
- **Display page (big screen):** live scoreboard with a transparent background, usable in a PowerPoint web-viewer add-in or an OBS browser source.
- **`slide-clicker.py` (presenting laptop):** turns phone NEXT/PREV into Right/Left arrow keypresses, so no physical clicker is needed.

Everything syncs through one Supabase table. No build step, no framework.

```
Phone (control) ──▶ Supabase ◀── Display page (polls every 0.6s)
                       ▲
                       └── slide-clicker.py (polls every 0.4s) ──▶ arrow keys
```

## Files

| File | Purpose |
|---|---|
| `quiz-scoreboard.html` | Control + display page (same file, `?mode=display` for display) |
| `slide-clicker.py` | Laptop script that presses arrow keys |
| `supabase-setup.sql` | Creates the `quiz_rooms` table |
| `requirements.txt` | Python dependencies |

## Setup

### 1. Supabase
1. Create a free project at [supabase.com](https://supabase.com).
2. Open the SQL editor and run `supabase-setup.sql`.
3. Go to **Project Settings → API** and copy the **Project URL** and **anon public key**.

### 2. Configure the page
The Supabase URL and anon key are already set in `quiz-scoreboard.html` (`DEF_URL` / `DEF_KEY` near the top of the script). To use a different project, replace those two values.

### 3. Host the page
Any static host works. For GitHub Pages: **Settings → Pages → Deploy from branch → `main` / root**. Your page will be at:

```
https://<user>.github.io/<repo>/quiz-scoreboard.html
```

### 4. Use it
- **Phone:** `…/quiz-scoreboard.html?room=quiz1`. Open **Setup**, enter team names (one per line), tap **Apply names**.
- **Display:** `…/quiz-scoreboard.html?mode=display&room=quiz1` (the exact link is shown under Setup).
- **Laptop (presenting the PPT):**
  ```bash
  pip install -r requirements.txt
  python slide-clicker.py https://YOUR-PROJECT.supabase.co YOUR_ANON_KEY quiz1
  ```
  Start the slideshow and keep that window focused. On macOS, grant your terminal **Accessibility** permission (System Settings → Privacy & Security).

Use the **same room code** in all three places.

## Controls

- **+10 / +5 / −5** per team.
- **Position** mode highlights 1st and 2nd; **Highest top** highlights only 1st.
- Ties share a rank (190, 170, 170 → 1st, 2nd, 2nd).
- **Undo** reverts up to the last 50 changes (per session). **Reset scores** zeroes everyone.
- Up to 12 teams.
- Status in the top-right shows `● LIVE` or `● OFFLINE`; offline usually means a wrong URL/key or a missing table.

## Security notes

- The Supabase **anon key is designed to be public**, but the SQL policy above is fully open: anyone who has your URL and key can read and edit any room. Fine for casual events; use unguessable room codes (e.g. `quiz-7f3k9x`) if it matters.
- Never commit a **service_role** key. Only the anon key belongs in this project.
- The URL and anon key are committed in `quiz-scoreboard.html`, so anyone who sees the repo can read and write the `quiz_rooms` table.

## Troubleshooting

| Problem | Fix |
|---|---|
| `● OFFLINE` | Check URL/key, that the table exists, and that RLS policy was created |
| Display doesn't update | Room code must match exactly; check the display URL |
| Slides don't advance | The slideshow window must be focused; check terminal permissions on macOS |
| Slides jump on script start | Shouldn't happen; the script ignores the command that existed at launch |

## License

Add a license of your choice (e.g. MIT) before publishing.
