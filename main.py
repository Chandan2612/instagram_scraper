
# # import pandas as pd
# # from playwright.sync_api import sync_playwright
# # import time
# # import re

# # MAX_LEADS = 200

# # data = []
# # visited = set()


# # # 🔢 Convert followers
# # def convert_followers(text):
# #     try:
# #         text = text.replace(',', '').strip()
# #         if 'K' in text.upper():
# #             return int(float(text.upper().replace('K', '')) * 1000)
# #         elif 'M' in text.upper():
# #             return int(float(text.upper().replace('M', '')) * 1000000)
# #         return int(text)
# #     except:
# #         return 0


# # # 🔥 USERNAME from HTML
# # def get_username_from_page(page):
# #     html = page.content()
# #     match = re.search(r"instagram\.com/([^/]+)/reel", html)
# #     if match:
# #         return match.group(1)
# #     match2 = re.search(r"@([a-zA-Z0-9_.]+)", html)
# #     if match2:
# #         return match2.group(1)
# #     return None


# # # 🔥 FOLLOWERS from HTML
# # def get_followers_from_page(page):
# #     html = page.content()
# #     match = re.search(r'([\d.,KkMm]+)\sFollowers', html)
# #     if match:
# #         return convert_followers(match.group(1))
# #     return 0


# # # 📊 PROFILE EXTRACTION
# # def extract_profile(page):
# #     try:
# #         url = page.url
# #         if url in visited:
# #             return None
# #         visited.add(url)

# #         page.wait_for_timeout(4000)

# #         name = "Unknown"
# #         if page.locator("h2").count() > 0:
# #             name = page.locator("h2").first.inner_text()

# #         followers = get_followers_from_page(page)

# #         # 🎯 NEW LOGIC: Only save if followers > 5000
# #         if followers > 5000:
# #             data.append({"Name": name, "Profile": url, "Followers": followers})
# #             print(f"✅ {name} | {followers} (Saved)")
# #         else:
# #             print(f"⏭ {name} | {followers} (Skipped, too few followers)")

# #         # data.append({"Name": name, "Profile": url, "Followers": followers})
# #         # print(f"✅ {name} | {followers}")

# #         if len(data) >= MAX_LEADS:
# #             print("🎯 Reached limit!")
# #             return "STOP"

# #     except Exception as e:
# #         print("❌ Error:", e)

# #     return None


# # # ⏭ Only used when "already visited" — waits for URL to actually change
# # def wait_for_reel_change(page, old_url, timeout=10):
# #     start = time.time()
# #     while time.time() - start < timeout:
# #         page.keyboard.press("ArrowDown")
# #         time.sleep(1.5)
# #         current_url = page.url
# #         if current_url != old_url and "/reel/" in current_url:
# #             print(f"🔄 Reel changed → {current_url}")
# #             time.sleep(1.5)  # Let HTML fully settle
# #             return True
# #     print("⚠ Reel URL didn't change after timeout")
# #     return False


# # # 🚀 MAIN
# # with sync_playwright() as p:
# #     browser = p.chromium.connect_over_cdp("http://localhost:9222")
# #     context = browser.contexts[0]
# #     page = context.pages[0]

# #     print("🚀 Running FINAL SCRIPT")

# #     while len(data) < MAX_LEADS:
# #         try:
# #             page.wait_for_timeout(3000)

# #             current_reel_url = page.url
# #             username = get_username_from_page(page)

# #             # ❌ Username not detected
# #             if not username:
# #                 print("❌ Username not found → scrolling")
# #                 page.keyboard.press("ArrowDown")
# #                 time.sleep(2)
# #                 continue

# #             profile_url = f"https://www.instagram.com/{username}/"

# #             # ⏭ Already visited — use wait loop to skip to truly next reel
# #             if profile_url in visited:
# #                 print(f"⏭ Already visited: {username} → next reel")
# #                 wait_for_reel_change(page, current_reel_url)
# #                 continue

# #             # ✅ New profile — open it
# #             print("👉 Opening:", profile_url)
# #             page.goto(profile_url)
# #             time.sleep(5)

# #             result = extract_profile(page)
# #             pd.DataFrame(data).to_excel("instagram_data.xlsx", index=False)

# #             if result == "STOP":
# #                 break

# #             # 🔙 Go back to reels feed
# #             page.go_back()
# #             time.sleep(3)               # Wait for reels feed to settle

# #             # ➡ Press ONCE — move to exactly next reel
# #             page.keyboard.press("ArrowDown")
# #             time.sleep(3)               # Wait for next reel to fully load

# #         except Exception as e:
# #             print("⚠ Error:", e)
# #             page.keyboard.press("ArrowDown")
# #             time.sleep(2)

# #     pd.DataFrame(data).to_excel("instagram_data.xlsx", index=False)
# #     print("✅ DONE — Saved to instagram_data.xlsx")
# import pandas as pd
# from playwright.sync_api import sync_playwright
# import time
# import re

# # --- CONFIGURATION ---
# MAX_LEADS = 200
# EXCEL_FILE = "instagram_data.xlsx"

# data = []
# visited = set()

# def convert_followers(text):
#     try:
#         text = text.replace(',', '').strip().upper()
#         if 'K' in text:
#             return int(float(text.replace('K', '')) * 1000)
#         elif 'M' in text:
#             return int(float(text.replace('M', '')) * 1000000)
#         return int(''.join(filter(str.isdigit, text)))
#     except:
#         return 0

# def get_username_from_page(page):
#     """Searches the full page HTML for the creator username."""
#     html = page.content()
#     # Pattern 1: /username/reel/
#     match = re.search(r"instagram\.com/([^/]+)/reel", html)
#     if match:
#         return match.group(1)
#     # Pattern 2: @username text
#     match2 = re.search(r"@([a-zA-Z0-9_.]+)", html)
#     if match2:
#         return match2.group(1)
#     return None

# def extract_profile(page):
#     """Scrapes the profile tab."""
#     try:
#         url = page.url
#         if url in visited:
#             return "SKIP"
#         visited.add(url)

#         # Wait for profile to load
#         page.wait_for_timeout(5000)

#         name = "Unknown"
#         if page.locator("h2").count() > 0:
#             name = page.locator("h2").first.inner_text()

#         # Follower count extraction
#         followers = 0
#         html = page.content()
#         match = re.search(r'([\d.,KkMm]+)\sFollowers', html)
#         if match:
#             followers = convert_followers(match.group(1))

#         if followers > 10000:
#             data.append({"Name": name, "Profile": url, "Followers": followers})
#             print(f"✅ {name} | {followers} (Saved)")
#             return "SAVED"
#         else:
#             print(f"⏭ {name} | {followers} (Skipped, <10k)")
#             return "LOW_FOLLOWERS"

#     except Exception as e:
#         print("❌ Scrape Error:", e)
#         return "ERROR"

# # --- MAIN EXECUTION ---
# with sync_playwright() as p:
#     browser = p.chromium.connect_over_cdp("http://localhost:9222")
#     context = browser.contexts[0]
#     page = context.pages[0]

#     print("🚀 SCRAPER STARTING (Wait-on-Feed Mode)")

#     while len(data) < MAX_LEADS:
#         try:
#             # --- STEP 1: FIND USERNAME ---
#             username = get_username_from_page(page)

#             if not username:
#                 print("❌ No username found. Scrolling...")
#                 page.keyboard.press("ArrowDown")
#                 time.sleep(3)
#                 continue

#             profile_url = f"https://www.instagram.com/{username}/"

#             # --- STEP 2: NAVIGATE TO PROFILE ---
#             print(f"👉 Opening Profile: {username}")
#             page.goto(profile_url)

#             # --- STEP 3: COLLECT DATA ---
#             extract_profile(page)
#             pd.DataFrame(data).to_excel(EXCEL_FILE, index=False)

#             # --- STEP 4: COME BACK TO REELS ---
#             page.go_back()
#             print("🔙 Returned to feed. Waiting for reload...")
#             page.wait_for_timeout(4000) # Wait for feed to stabilize

#             # --- STEP 5: SCROLL TO NEXT REEL ---
#             print("🖱 Scrolling to NEXT Reel...")
#             page.keyboard.press("ArrowDown")

#             # --- STEP 6: WAIT 10 SECONDS (CRITICAL SYNC) ---
#             print("⏳ Sitting on Reel for 10 seconds to ensure ID change...")
#             time.sleep(10)

#         except Exception as e:
#             print("⚠ Loop Error:", e)
#             page.keyboard.press("ArrowDown")
#             time.sleep(5)

#     print(f"✅ FINISHED. Check {EXCEL_FILE}")


import pandas as pd
from playwright.sync_api import sync_playwright
import time
import re
import datetime

# --- CONFIGURATION ---
MAX_LEADS = 200
EXCEL_FILE = "instagram_10k_leads.xlsx"
LOG_FILE = "scraped_log.txt"
FOLLOWER_THRESHOLD = 10000

data = []
visited = set()

def write_to_log(message):
    """Saves a timestamped entry to the text file."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")

def convert_followers(text):
    try:
        text = text.replace(',', '').strip().upper()
        if 'K' in text:
            return int(float(text.replace('K', '')) * 1000)
        elif 'M' in text:
            return int(float(text.replace('M', '')) * 1000000)
        return int(''.join(filter(str.isdigit, text)))
    except:
        return 0

def get_username_from_page(page):
    """Searches the full page HTML for the creator username."""
    try:
        html = page.content()
        match = re.search(r"instagram\.com/([^/]+)/reel", html)
        if match:
            return match.group(1)
        match2 = re.search(r"@([a-zA-Z0-9_.]+)", html)
        if match2:
            return match2.group(1)
    except:
        pass
    return None

def extract_profile(page):
    """Scrapes the profile and logs to TXT."""
    try:
        url = page.url
        if url in visited:
            return "SKIP"
        visited.add(url)

        # Wait for profile to load
        page.wait_for_timeout(5000)

        username = url.split('/')[-2]
        name = "Unknown"
        if page.locator("h2").count() > 0:
            name = page.locator("h2").first.inner_text()

        # Follower count extraction
        followers = 0
        html = page.content()
        match = re.search(r'([\d.,KkMm]+)\sFollowers', html)
        if match:
            followers = convert_followers(match.group(1))

        if followers > FOLLOWER_THRESHOLD:
            entry = {"Name": name, "Profile": url, "Followers": followers}
            data.append(entry)
            log_msg = f"✅ SAVED: {username} | {followers} followers | Name: {name}"
            print(log_msg)
            write_to_log(log_msg)
            return "SAVED"
        else:
            log_msg = f"⏭ SKIPPED: {username} | {followers} (Below 10k)"
            print(log_msg)
            write_to_log(log_msg)
            return "LOW_FOLLOWERS"

    except Exception as e:
        err_msg = f"❌ Scrape Error on {page.url}: {e}"
        print(err_msg)
        write_to_log(err_msg)
        return "ERROR"

# --- MAIN EXECUTION ---
with sync_playwright() as p:
    try:
        # Connecting to your open Chrome browser
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = context.pages[0]
    except:
        print("❌ Error: Ensure Chrome is open with: --remote-debugging-port=9222")
        exit()

    print(f"🚀 SCRAPER STARTING (Filter: > {FOLLOWER_THRESHOLD} followers)")
    write_to_log("--- NEW SESSION STARTED ---")

    while len(data) < MAX_LEADS:
        try:
            # 1. Look for username
            username = get_username_from_page(page)

            if not username:
                print("❌ No username found. Scrolling...")
                page.keyboard.press("ArrowDown")
                time.sleep(3)
                continue

            profile_url = f"https://www.instagram.com/{username}/"

            # 2. Open Profile
            print(f"👉 Investigating: {username}")
            page.goto(profile_url)

            # 3. Extract and Save to Excel/TXT
            extract_profile(page)
            if data:
                pd.DataFrame(data).to_excel(EXCEL_FILE, index=False)

            # 4. Return to feed
            page.go_back()
            print("🔙 Returned to feed. Waiting for reload...")
            page.wait_for_timeout(4000)

            # 5. Move to next reel
            print("🖱 Scrolling to NEXT Reel...")
            page.keyboard.press("ArrowDown")

            # 6. Wait for Sync
            print("⏳ Buffer Wait: 10 seconds for UI stability...")
            time.sleep(10)

        except Exception as e:
            write_to_log(f"⚠ Main Loop Error: {e}")
            page.keyboard.press("ArrowDown")
            time.sleep(5)

    print(f"✅ FINISHED. Leads: {EXCEL_FILE} | Logs: {LOG_FILE}")
