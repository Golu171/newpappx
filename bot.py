import requests
import os
import mmap
import hashlib
import cloudscraper
from Extractor.modules.jupiter import json_to_html
from Extractor import app
from pyrogram import filters
scraper = cloudscraper.create_scraper()

# ---------------- Filename Sanitization ---------------- #
def sanitize_filename_unique(name, max_length=80):
    """Sanitize filename, truncate, and append short hash for uniqueness"""
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
        "Authorization": "",
        "User-ID": "82093",
        "Content-Type": "application/json"
    }
    payload = {"search_term": "TEST SERIES", "user_id": "-1", "screen_name": "Dashboard"}
    resp = scraper.post(f"{api_url}/get/search", headers=headers, json=payload).json()
    return [(c["id"], c["course_name"]) for c in resp.get("courses_with_folder", [])]

async def fetch_folder_contents(api_url, course_id, parent_id):
    headers = {
        "Client-Service": "Appx",
        "Auth-Key": "appxapi",
        "source": "website",
        "Authorization": "",
        "User-ID": "82093",
    }
    url = f"{api_url}/get/folder_contentsv3?course_id={course_id}&parent_id={parent_id}&start=0"
    resp = scraper.get(url, headers=headers).json()
    return resp.get("data", [])

async def fetch_test_details(api_url, quiz_title_id):
    headers = {
        "Client-Service": "Appx",
        "Auth-Key": "appxapi",
        "source": "website",
        "Authorization": "",
        "User-ID": "82093",
    }
    url = f"{api_url}/get/test_title_by_id?id={quiz_title_id}&userid=82093"
    resp = scraper.get(url, headers=headers).json()
    return resp.get("data", {})

async def explore_folder(api_url, course_id, parent_id):
    """Recursively explore folders and return list of (title, url)"""
    tests = []
    items = await fetch_folder_contents(api_url, course_id, parent_id)
    for item in items:
        material_type = item.get("material_type")
        quiz_title_id = item.get("quiz_title_id")

        if material_type == "TEST" and quiz_title_id and quiz_title_id != "-1":
            details = await fetch_test_details(api_url, quiz_title_id)
            title = details.get("title")
            url = details.get("test_questions_url")
            if title and url:
                tests.append((title, url))

        elif material_type == "FOLDER":
            folder_id = item.get("id")
            tests.extend(await explore_folder(api_url, course_id, folder_id))
    return tests

# ---------------- /coursehtml Command ---------------- #
@app.on_message(filters.command("coursehtml"))
async def coursehtml_handler(app, message):
    chat_id = message.chat.id

    # Step 1: Ask for API URL
    await message.reply_text("Send the API URL (e.g., `https://mahiyapathshalaapi.classx.co.in`):")
    api_msg = await app.listen(chat_id)
    api_url = api_msg.text.strip()
    if not api_url.startswith("http"):
        api_url = f"https://{api_url}"

    # Step 2: Ask for creator name
    created_by_msg = await app.ask(chat_id, "SEND CREATOR NAME")
    created_by = created_by_msg.text

    # Step 3: Fetch courses/batches
    try:
        courses = await fetch_courses(api_url)
    except Exception as e:
        await message.reply_text(f"âŒ Failed to fetch courses: {e}")
        return

    if not courses:
        await message.reply_text("No courses found.")
        return

    # Step 4: Send list to user
    course_list = "\n".join([f"{idx+1}. {c[1]}" for idx, c in enumerate(courses)])
    await message.reply_text(f"Available Courses:\n\n{course_list}\n\nSend the course index (e.g., 1, 2...) to process that course:")

    course_msg = await app.listen(chat_id)
    try:
        selected_index = int(course_msg.text.strip())
        if not 1 <= selected_index <= len(courses):
            await message.reply_text("âŒ Invalid index. Exiting.")
            return
        selected_course_id, selected_course_name = courses[selected_index - 1]
    except Exception:
        await message.reply_text("âŒ Invalid input. Exiting.")
        return

    # Step 5: Explore folder and fetch tests
    await message.reply_text(f"Fetching tests for course: {selected_course_name}...")
    tests = await explore_folder(api_url, selected_course_id, -1)

    if not tests:
        await message.reply_text("No tests found in this course.")
        return

    # Step 6: Convert each test URL â†’ HTML and send
    for title, url in tests:
        try:
            html_content = json_to_html(url, title, created_by)
            html_file = f"{sanitize_filename_unique(title)}.html"
            with open(html_file, "w", encoding="utf-8") as f:
                f.write(html_content)
            await message.reply_document(html_file, caption=f"HTML: {title}")
            os.remove(html_file)
        except Exception as e:
            await message.reply_text(f"âŒ Failed for {title}: {e}")

    await message.reply_text("âœ… Done processing the course!")

# ------------------ PDF Download & Decrypt ------------------ #
async def download_and_decrypt_pdf(url, name, key):
    file_path = await downloadnew_file(url, name)
    if not os.path.exists(file_path):
        print(f"The file {file_path} does not exist.")
        return False
    try:
        with open(file_path, "r+b") as f:
            num_bytes = min(28, os.path.getsize(file_path))
            with mmap.mmap(f.fileno(), length=num_bytes, access=mmap.ACCESS_WRITE) as mmapped_file:
                for i in range(num_bytes):
                    mmapped_file[i] ^= ord(key[i]) if i < len(key) else i
        print(f"Decryption completed for {file_path}.")
        return file_path
    except Exception as e:
        print(f"Error during decryption: {e}")
        return False
async def downloadnew_file(url, name):
    file_path = f"{name}.pdf" if ".pdf" in url else name
    headers = {
        'User-Agent': "Mozilla/5.0",
        'origin': "https://sciencemagnet.classx.co.in",
        'referer': "https://sciencemagnet.classx.co.in/",
    }
    try:
        response = requests.get(url, headers=headers, stream=True, timeout=60)
        if response.status_code == 200:
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            return file_path if os.path.exists(file_path) else None
        else:
            print(f"[ERROR] Failed to download file. Status: {response.status_code}")
            return None
    except Exception as e:
        print(f"[ERROR] Exception during download: {e}")
        return None

# ------------------ JSON â†’ HTML Converter ------------------ #


# ------------------ /jsontxt Command ------------------ #
@app.on_message(filters.command("jsontxt"))
async def jsontxt_handler(app, message):
    chat_id = message.chat.id
    await message.reply_text("Send a `.txt` with format: Title:JSON_LINK (one per line)")
    txt_msg = await app.listen(chat_id)
    created_by_message = await app.ask(message.chat.id, "SEND CREATOR NAME")
    created_by = created_by_message.text
    if not txt_msg.document or not txt_msg.document.file_name.endswith(".txt"):
        await message.reply_text("âŒ Please send a valid `.txt` file.")
        return
    txt_path = await txt_msg.download()
    try:
        with open(txt_path, "r", encoding="utf-8") as f:
            lines=[line.strip() for line in f if line.strip()]
        for idx,line in enumerate(lines,1):
            try:
                if ":" not in line:
                    await message.reply_text(f"âš ï¸ Invalid line {idx}: {line}")
                    continue
                title, link=line.split(":",1)
                title, link=title.strip(), link.strip()
                data=requests.get(link).json()
                html= json_to_html(link, title, created_by)
                html_path=f"{title.replace(' ','_')}.html"
                with open(html_path,"w",encoding="utf-8") as f_html:
                    f_html.write(html)
                await message.reply_document(html_path, caption=f"âœ… HTML: {title}")
                os.remove(html_path)
            except Exception as e:
                await message.reply_text(f"âš ï¸ Error line {idx}: {e}")
    finally:
        if os.path.exists(txt_path):
            os.remove(txt_path)


@app.on_message(filters.command("test"))
async def test_handler(app, message):
    chat_id = message.chat.id

    # Ask for API URL
    await message.reply_text("Send me the API URL (e.g., `boosteracademyapi.classx.co.in`)")
    api_msg = await app.listen(chat_id)
    api = api_msg.text.strip()
    if not api.startswith("http"):
        api = f"https://{api}"

    # Ask for creator name
    created_by_msg = await app.ask(chat_id, "SEND CREATOR NAME")
    created_by = created_by_msg.text

    headers = {
        'User-Agent': "Mozilla/5.0",
        'user-id': "86333",
        'auth-key': "appxapi",
        'client-service': "Appx",
        'source': "website",
        'authorization': "token",
    }

    await message.reply_text("Fetching test series...")
    try:
        response = requests.get(f"{api}/get/test_series", params={'start': "-1"}, headers=headers).json()
    except Exception as e:
        await message.reply_text(f"âŒ Failed to fetch test series: {e}")
        return

    if "data" not in response or not response["data"]:
        await message.reply_text("No test series found.")
        return

    test_series = response["data"]
    test_list_text = "\n".join([f"{ts['id']} - {ts['title']}" for ts in test_series])
    await message.reply_text(f"Available Test Series:\n\n{test_list_text}\n\nSend the Test IDs (separated by `&`).")

    # Listen for selected test IDs
    test_msg = await app.listen(chat_id)
    test_ids = [tid.strip() for tid in test_msg.text.strip().split("&")]

    for test_id in test_ids:
        # Fetch subjects for each test
        subject_resp = requests.get(f"{api}/get/testseries_subjects", params={'testseries_id': test_id}, headers=headers).json()
        if "data" not in subject_resp or not subject_resp["data"]:
            continue

        for subject in subject_resp["data"]:
            subject_id = subject.get("subjectid")
            params2 = {
                'testseriesid': test_id,
                'subject_id': subject_id,
                'userid': "-1",
                'start': "-1",
                'search': ""
            }
            test_titles_resp = requests.get(f"{api}/get/test_titlev2", params=params2, headers=headers).json()

            # ---------------- Objective Tests (JSON â†’ HTML) ---------------- #
            if "test_titles" in test_titles_resp:
                for test in test_titles_resp["test_titles"]:
                    title = test.get("title", "Unknown Title")
                    json_link = test.get("test_questions_url")
                    if json_link:
                        try:
                            html_content = json_to_html(json_link, title, created_by)
                            html_file = f"{title.replace(' ', '_')}.html"
                            with open(html_file, "w", encoding="utf-8") as f:
                                f.write(html_content)
                            await message.reply_document(html_file, caption=f"HTML file: **{title}**")
                            os.remove(html_file)
                        except Exception as e:
                            await message.reply_text(f"âŒ Failed to generate HTML for {title}: {e}")

            # ---------------- PDF Tests ---------------- #
            if "test_pdf" in test_titles_resp:
                for test in test_titles_resp["test_pdf"]:
                    title = test.get("title", "Unknown Title")
                    url = test.get("pdf_url")
                    if url:
                        try:
                            if "*" in url:
                                url, key = url.split("*", 1)
                                file_path = await download_and_decrypt_pdf(url, title, key)
                            else:
                                file_path = await downloadnew_file(url, title)
                            if file_path:
                                await message.reply_document(file_path, caption=f"ðŸ“„ PDF: **{title}**")
                                os.remove(file_path)
                        except Exception as e:
                            await message.reply_text(f"âŒ Failed to download PDF {title}: {e}")

            # ---------------- Subjective Tests (PDF + Solution) ---------------- #
            if "test_subjective" in test_titles_resp:
                for test in test_titles_resp["test_subjective"]:
                    title = test.get("title", "Unknown Title")
                    pdf_url = test.get("pdf_url")
                    solution_url = test.get("solutions_pdf")

                    # Main PDF
                    if pdf_url:
                        try:
                            if "*" in pdf_url:
                                pdf_url, key = pdf_url.split("*", 1)
                                file_path = await download_and_decrypt_pdf(pdf_url, f"{title}_main", key)
                            else:
                                file_path = await downloadnew_file(pdf_url, f"{title}_main")
                            if file_path:
                                await message.reply_document(file_path, caption=f"ðŸ“„ PDF: **{title}**")
                                os.remove(file_path)
                        except Exception as e:
                            await message.reply_text(f"âŒ Failed to download main PDF {title}: {e}")

                    # Solution PDF
                    if solution_url:
                        try:
                            if "*" in solution_url:
                                solution_url, key = solution_url.split("*", 1)
                                file_path = await download_and_decrypt_pdf(solution_url, f"{title}_solution", key)
                            else:
                                file_path = await downloadnew_file(solution_url, f"{title}_solution")
                            if file_path:
                                await message.reply_document(file_path, caption=f"ðŸ“„ Solution: **{title}**")
                                os.remove(file_path)
                        except Exception as e:
                            await message.reply_text(f"âŒ Failed to download solution PDF {title}: {e}")
                    
