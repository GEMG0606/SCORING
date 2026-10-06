"""Run on the laptop that's presenting the PPT. Phone NEXT/PREV -> Right/Left arrow key.
pip install requests pyautogui
python slide-clicker.py https://xxxx.supabase.co YOUR_ANON_KEY quiz1
"""
import sys, time, requests, pyautogui
url, key, room = sys.argv[1].rstrip('/'), sys.argv[2], sys.argv[3]
H = {"apikey": key, "Authorization": f"Bearer {key}"}
last = None
print("Listening… keep the slideshow window focused. Ctrl+C to stop.")
while True:
    try:
        r = requests.get(f"{url}/rest/v1/quiz_rooms?room=eq.{room}&select=cmd,cmd_seq", headers=H, timeout=5).json()
        if r:
            seq, c = r[0]["cmd_seq"], r[0]["cmd"]
            if last is None: last = seq          # ignore old command on startup
            elif seq != last:
                last = seq
                pyautogui.press("right" if c == "next" else "left")
    except Exception as e:
        print("retry:", e)
    time.sleep(0.4)
