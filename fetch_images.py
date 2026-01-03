import base64
import os
import time
from math import ceil


def fetch_images(
    driver,
    chapter_url,
    chapter_number,
    next_chapter_selector,
    image_url_prefix,
    chunk_size=5,
):
    driver.set_script_timeout(60*5)
    start_time = time.time()

    print(f"\n⚡ Opening chapter {chapter_number}")
    driver.get(chapter_url)
    time.sleep(2)

    # الفصل التالي
    next_chapter_url = None
    try:
        next_button = driver.find_element("css selector", next_chapter_selector)
        next_chapter_url = next_button.get_attribute("href")
    except:
        print("⚠ Next chapter button not found.")

    # روابط الصور
    image_urls = driver.execute_script(
        """
        return Array.from(document.images)
            .map(img => img.src)
            .filter(src => src.startsWith(arguments[0]));
        """,
        image_url_prefix,
    )

    if not image_urls:
        print("❌ No images found.")
        return [], next_chapter_url

    print(f"🔍 Found {len(image_urls)} images")

    chapter_folder = f"chapter_{chapter_number}"
    os.makedirs(chapter_folder, exist_ok=True)

    downloaded_images = []

    # تقسيم إلى دفعات
    for batch in range(0, len(image_urls), chunk_size):
        urls_chunk = image_urls[batch : batch + chunk_size]
        print(
            f"⬇ Batch {batch//chunk_size + 1}/"
            f"{ceil(len(image_urls)/chunk_size)}"
        )

        images_base64 = driver.execute_async_script(
            """
            const urls = arguments[0];
            const done = arguments[1];

            Promise.all(
                urls.map(url =>
                    fetch(url)
                        .then(r => r.blob())
                        .then(blob => new Promise(res => {
                            const reader = new FileReader();
                            reader.onload = () => res(reader.result);
                            reader.readAsDataURL(blob);
                        }))
                )
            ).then(done).catch(() => done(null));
            """,
            urls_chunk,
        )

        if not images_base64:
            print("❌ Batch failed — skipping chapter")
            return [], next_chapter_url

        for data_url in images_base64:
            header, encoded = data_url.split(",", 1)
            ext = "jpg" if "jpeg" in header else "png"

            image_path = f"{chapter_folder}/{len(downloaded_images)+1:03}.{ext}"
            with open(image_path, "wb") as f:
                f.write(base64.b64decode(encoded))

            downloaded_images.append(image_path)

    elapsed = int(time.time() - start_time)
    print(f"✅ Chapter {chapter_number} done in {elapsed}s")

    return downloaded_images, next_chapter_url
