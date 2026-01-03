import time
from fetch_images import fetch_images
from images_to_pdf import images_to_pdf
from start_driver import start_driver
from cookies_utils import save_cookies, load_cookies
import os
from dotenv import load_dotenv

from wait_for_real_page import wait_for_real_page

load_dotenv()
# ----------------------------------------------------------
# MAIN
# ----------------------------------------------------------


if __name__ == "__main__":
    try:
        while True:
            # create cookies folder if not exists
            os.makedirs("cookies", exist_ok=True)
            # create chapters folder if not exists
            os.makedirs("chapters", exist_ok=True)
            
            chapter_url = input(
                f"Enter starting chapter URL(default:{ os.environ.get("manga")}):"
            ).strip() or os.environ.get("manga", "")
            chapters_to_download = int(
                input("Enter number of chapters to download (default: 5): ") or 5
            )

            next_chapter_selector = (
                input(
                    "Enter CSS selector for Next Chapter button "
                    "(default: a#next-chapter): "
                ).strip()
                or "a#next-chapter"
            )

            image_url_prefix = input(
                f"Enter image URL prefix(default:{ os.environ.get("image_URL_prefix")}): "
            ).strip() or os.environ.get("image_URL_prefix", "")

            driver = start_driver()

            # استخراج الدومين فقط
            domain = chapter_url.split("/")[0] + "//" + chapter_url.split("/")[2]

            # محاولة تحميل cookies
            cookies_loaded = load_cookies(
                driver, domain, path=f"cookies/{domain.split('/')[-1]}.pkl"
            )

            driver.get(chapter_url)

            while not wait_for_real_page(driver, image_url_prefix):
                ready = driver.execute_script("return document.readyState")
                print("status:", ready)  # complete / interactive / loading
                print("🔐 Please bypass Cloudflare manually...")
                time.sleep(2)

            save_cookies(driver, path=f"cookies/{domain.split('/')[-1]}.pkl")
            while chapters_to_download > 0:

                chapter_number = chapter_url.rstrip("/").split("/")[-1]
                output_pdf_name = f"chapters/chapter_{chapter_number}.pdf"

                images, chapter_url = fetch_images(
                    driver,
                    chapter_url,
                    chapter_number,
                    next_chapter_selector,
                    image_url_prefix,
                )

                if not chapter_url:
                    print("🛑 Stopping: next chapter URL not found.")
                    break

                if images:
                    images_to_pdf(images, output_pdf_name)

                chapters_to_download -= 1
                save_cookies(driver, path=f"cookies/{domain.split('/')[-1]}.pkl")

            driver.quit()
            print("🎉 All chapters downloaded successfully")
            

            input("Press Enter to continue or Ctrl+C to exit...")
    except KeyboardInterrupt:
        print("\n👋 Exiting program")
