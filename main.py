
import pandas as pd
from playwright.sync_api import sync_playwright
import time
import re

MAX_LEADS = 200

data = []
visited = set()


# 🔢 Convert followers
def convert_followers(text):
    try:
        text = text.replace(',', '').strip()
        if 'K' in text.upper():
            return int(float(text.upper().replace('K', '')) * 1000)
        elif 'M' in text.upper():
            return int(float(text.upper().replace('M', '')) * 1000000)
        return int(text)
    except:
        return 0


# 🔥 USERNAME from HTML
def get_username_from_page(page):
    html = page.content()
    match = re.search(r"instagram\.com/([^/]+)/reel", html)
    if match:
        return match.group(1)
    match2 = re.search(r"@([a-zA-Z0-9_.]+)", html)
    if match2:
        return match2.group(1)
    return None


# 🔥 FOLLOWERS from HTML
def get_followers_from_page(page):
    html = page.content()
    match = re.search(r'([\d.,KkMm]+)\sFollowers', html)
    if match:
        return convert_followers(match.group(1))
    return 0


# 📊 PROFILE EXTRACTION
def extract_profile(page):
    try:
        url = page.url
        if url in visited:
            return None
        visited.add(url)

        page.wait_for_timeout(4000)

        name = "Unknown"
        if page.locator("h2").count() > 0:
            name = page.locator("h2").first.inner_text()

        followers = get_followers_from_page(page)

        # 🎯 NEW LOGIC: Only save if followers > 5000
        if followers > 5000:
            data.append({"Name": name, "Profile": url, "Followers": followers})
            print(f"✅ {name} | {followers} (Saved)")
        else:
            print(f"⏭ {name} | {followers} (Skipped, too few followers)")

        # data.append({"Name": name, "Profile": url, "Followers": followers})
        # print(f"✅ {name} | {followers}")

        if len(data) >= MAX_LEADS:
            print("🎯 Reached limit!")
            return "STOP"

    except Exception as e:
        print("❌ Error:", e)

    return None


# ⏭ Only used when "already visited" — waits for URL to actually change
def wait_for_reel_change(page, old_url, timeout=10):
    start = time.time()
    while time.time() - start < timeout:
        page.keyboard.press("ArrowDown")
        time.sleep(1.5)
        current_url = page.url
        if current_url != old_url and "/reel/" in current_url:
            print(f"🔄 Reel changed → {current_url}")
            time.sleep(1.5)  # Let HTML fully settle
            return True
    print("⚠ Reel URL didn't change after timeout")
    return False


# 🚀 MAIN
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://localhost:9222")
    context = browser.contexts[0]
    page = context.pages[0]

    print("🚀 Running FINAL SCRIPT")

    while len(data) < MAX_LEADS:
        try:
            page.wait_for_timeout(3000)

            current_reel_url = page.url
            username = get_username_from_page(page)

            # ❌ Username not detected
            if not username:
                print("❌ Username not found → scrolling")
                page.keyboard.press("ArrowDown")
                time.sleep(2)
                continue

            profile_url = f"https://www.instagram.com/{username}/"

            # ⏭ Already visited — use wait loop to skip to truly next reel
            if profile_url in visited:
                print(f"⏭ Already visited: {username} → next reel")
                wait_for_reel_change(page, current_reel_url)
                continue

            # ✅ New profile — open it
            print("👉 Opening:", profile_url)
            page.goto(profile_url)
            time.sleep(5)

            result = extract_profile(page)
            pd.DataFrame(data).to_excel("instagram_data.xlsx", index=False)

            if result == "STOP":
                break

            # 🔙 Go back to reels feed
            page.go_back()
            time.sleep(3)               # Wait for reels feed to settle

            # ➡ Press ONCE — move to exactly next reel
            page.keyboard.press("ArrowDown")
            time.sleep(3)               # Wait for next reel to fully load

        except Exception as e:
            print("⚠ Error:", e)
            page.keyboard.press("ArrowDown")
            time.sleep(2)

    pd.DataFrame(data).to_excel("instagram_data.xlsx", index=False)
    print("✅ DONE — Saved to instagram_data.xlsx")
