import base64
import os
import time


def fetch_images(
    driver,
    chapter_url,
    chapter_number,
    next_chapter_selector,
    image_url_prefix,
    retries=10,
):
    start_time = time.time()
    print(
        f"\n⚡ Opening chapter {chapter_number} " f"| Time: {time.strftime('%H:%M:%S')}"
    )

    for attempt in range(1, retries + 1):
        try:
            driver.get(chapter_url)
            time.sleep(2)
            break
        except:
            print(f"⚠ Failed to load chapter page (attempt {attempt}/{retries})")
            if attempt == retries:
                print("❌ Unable to open chapter page.")
                return [], None
            time.sleep(2)

    next_chapter_url = None
    try:
        next_button = driver.find_element("css selector", next_chapter_selector)
        next_chapter_url = next_button.get_attribute("href")
    except:
        print("⚠ Next chapter button not found.")

    image_elements = driver.find_elements("css selector", "img")
    image_urls = [
        img.get_attribute("src") for img in image_elements if img.get_attribute("src")
    ]

    image_urls = [url for url in image_urls if url.startswith(image_url_prefix)]

    if not image_urls:
        print("❌ No images found — chapter may not exist.")
        return [], next_chapter_url

    print(f"🔍 Found {len(image_urls)} images")

    chapter_folder = f"chapter_{chapter_number}"
    os.makedirs(chapter_folder, exist_ok=True)

    downloaded_images = []

    for index, img_url in enumerate(image_urls, start=1):
        print(f"⬇ Downloading image {index}/{len(image_urls)}: {img_url}")

        image_data_url = None
        for attempt in range(1, retries + 1):
            try:
                driver.get(img_url)
                time.sleep(1)
                image_data_url = driver.execute_script(
                    """
                    const img = document.querySelector('img');
                    if (!img) return null;

                    const canvas = document.createElement('canvas');
                    canvas.width = img.naturalWidth;
                    canvas.height = img.naturalHeight;
                    const ctx = canvas.getContext('2d');
                    ctx.drawImage(img, 0, 0);

                    return canvas.toDataURL('image/jpeg');
                    """
                )
                if image_data_url:
                    break
            except:
                pass

            print(f"⚠ Failed to load image (attempt {attempt}/{retries}): {img_url}")

        if not image_data_url:
            print("❌ Corrupted image detected — skipping entire chapter.")
            return [], next_chapter_url

        _, encoded_data = image_data_url.split(",", 1)
        image_bytes = base64.b64decode(encoded_data)

        image_path = f"{chapter_folder}/{index}.jpg"
        with open(image_path, "wb") as file:
            file.write(image_bytes)

        downloaded_images.append(image_path)

    elapsed = int(time.time() - start_time)
    print(f"✅ Chapter {chapter_number} completed " f"| Elapsed time: {elapsed}s")

    return downloaded_images, next_chapter_url
