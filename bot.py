import requests
import os
import mmap
import hashlib
import cloudscraper
from Extractor.modules.jupiter import json_to_html
from Extractor import app
from pyrogram import filters

scraper = cloudscraper.create_scraper()

# 🔥 LOG CHANNEL
LOG_CHANNEL = -1003703688225

# ---------------- Filename Sanitization ---------------- #
def sanitize_filename_unique(name, max_length=80):
    safe_name = "".join(c for c in name if c.isalnum() or c in (" ", "_", "-")).rstrip()
    if len(safe_name) > max_length:
        safe_name = safe_name[:max_length].rstrip()
    hash_str = hashlib.md5(name.encode()).hexdigest()[:6]
    return f"{safe_name}_{hash_str}"

# ---------------- API Functions ---------------- #
async def fetch_courses(api_url):
    headers = {
        "Client-Service": "Appx",
        "Auth-Key": "appxapi",
        "source": "website",
        "User-ID": "82093",
        "Content-Type": "application/json"
    }
    payload = {"search_term": "TEST SERIES", "user_id": "-1", "screen_name": "Dashboard"}
    resp = scraper.post(f"{api_url}/get/search", headers=headers, json=payload).json()
    return [(c["id"], c["course_name"]) for c in resp.get("courses_with_folder", [])]

async def explore_folder(api_url, course_id, parent_id):
    headers = {
        "Client-Service": "Appx",
        "Auth-Key": "appxapi",
        "source": "website",
        "User-ID": "82093",
    }
    url = f"{api_url}/get/folder_contentsv3?course_id={course_id}&parent_id={parent_id}&start=0"
    data = scraper.get(url, headers=headers).json().get("data", [])

    tests = []
    for item in data:
        if item.get("material_type") == "TEST":
            tid = item.get("quiz_title_id")
            if tid and tid != "-1":
                d = scraper.get(f"{api_url}/get/test_title_by_id?id={tid}&userid=82093", headers=headers).json().get("data", {})
                if d.get("test_questions_url"):
                    tests.append((d["title"], d["test_questions_url"]))
        elif item.get("material_type") == "FOLDER":
            tests.extend(await explore_folder(api_url, course_id, item.get("id")))
    return tests

# ---------------- PDF ---------------- #
async def download_and_decrypt_pdf(url, name, key):
    file_path = await download_file(url, name)
    try:
        with open(file_path, "r+b") as f:
            mm = mmap.mmap(f.fileno(), length=min(28, os.path.getsize(file_path)))
            for i in range(len(mm)):
                mm[i] ^= ord(key[i]) if i < len(key) else i
        return file_path
    except:
        return False

async def download_file(url, name):
    file_path = f"{name}.pdf"
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(file_path, "wb") as f:
            for chunk in r.iter_content(8192):
                f.write(chunk)
        return file_path
    return None

# ---------------- 🔥 MAIN COMMAND ---------------- #
@app.on_message(filters.command("extractall"))
async def extract_all_handler(app, message):
    chat_id = message.chat.id

    await message.reply_text("Send API URL:")
    api_msg = await app.listen(chat_id)
    api = api_msg.text.strip()
    if not api.startswith("http"):
        api = f"https://{api}"

    created_by = (await app.ask(chat_id, "SEND CREATOR NAME")).text

    # -------- COURSE --------
    courses = await fetch_courses(api)

    for cid, cname in courses:
        await message.reply_text(f"📚 {cname}")
        tests = await explore_folder(api, cid, -1)

        for title, link in tests:
            try:
                html = json_to_html(link, title, created_by)
                file = f"{sanitize_filename_unique(title)}.html"

                with open(file, "w", encoding="utf-8") as f:
                    f.write(html)

                await message.reply_document(file, caption=f"HTML: {title}")
                await app.send_document(LOG_CHANNEL, file, caption=title)

                os.remove(file)
            except:
                continue

    # -------- TEST SERIES --------
    headers = {
        'User-Agent': "Mozilla/5.0",
        'user-id': "86333",
        'auth-key': "appxapi",
        'client-service': "Appx",
        'source': "website",
    }

    series = requests.get(f"{api}/get/test_series", params={'start': "-1"}, headers=headers).json().get("data", [])

    for ts in series:
        tid = ts["id"]

        subj = requests.get(f"{api}/get/testseries_subjects",
                            params={'testseries_id': tid},
                            headers=headers).json()

        for s in subj.get("data", []):
            t_data = requests.get(f"{api}/get/test_titlev2",
                                  params={
                                      'testseriesid': tid,
                                      'subject_id': s["subjectid"],
                                      'userid': "-1",
                                      'start': "-1"
                                  },
                                  headers=headers).json()

            # HTML
            for t in t_data.get("test_titles", []):
                if t.get("test_questions_url"):
                    try:
                        html = json_to_html(t["test_questions_url"], t["title"], created_by)
                        file = f"{sanitize_filename_unique(t['title'])}.html"

                        with open(file, "w", encoding="utf-8") as f:
                            f.write(html)

                        await message.reply_document(file, caption=t["title"])
                        await app.send_document(LOG_CHANNEL, file, caption=t["title"])

                        os.remove(file)
                    except:
                        continue

            # PDF
            for t in t_data.get("test_pdf", []):
                url = t.get("pdf_url")
                title = t.get("title")

                if url:
                    try:
                        if "*" in url:
                            url, key = url.split("*", 1)
                            file = await download_and_decrypt_pdf(url, title, key)
                        else:
                            file = await download_file(url, title)

                        if file:
                            await message.reply_document(file, caption=title)
                            await app.send_document(LOG_CHANNEL, file, caption=title)
                            os.remove(file)
                    except:
                        continue

    await message.reply_text("✅ DONE ALL (HTML + PDF + CHANNEL)")
