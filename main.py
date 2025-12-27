import time

from fetch_images import fetch_images
from images_to_pdf import images_to_pdf
from start_driver import start_driver


# ----------------------------------------------------------
# MAIN
# ----------------------------------------------------------

if __name__ == "__main__":
    try:
        while True:
            chapter_url = input("Enter starting chapter URL: ").strip()
            chapters_to_download = int(input("Enter number of chapters to download: "))

            next_chapter_selector = (
                input(
                    "Enter CSS selector for Next Chapter button "
                    "(default: a#next-chapter): "
                ).strip()
                or "a#next-chapter"
            )

            image_url_prefix = input(
                "Enter image URL prefix (example: https://site.com/uploads): "
            ).strip()

            driver = start_driver()
            if not driver:
                exit()

            print("\n\nOpen the chapter in the browser and manually bypass Cloudflare.")
            driver.get(chapter_url)

            while "Just a moment..." in driver.title:
                time.sleep(3)

            while chapters_to_download > 0:
                chapter_number = chapter_url.rstrip("/").split("/")[-1]
                output_pdf_name = f"chapter_{chapter_number}.pdf"

                images, chapter_url = fetch_images(
                    driver,
                    chapter_url,
                    chapter_number,
                    next_chapter_selector,
                    image_url_prefix,
                )

                if images:
                    images_to_pdf(images, output_pdf_name)

                chapters_to_download -= 1

            driver.quit()
            print("🎉 All chapters downloaded successfully.")

            input("Press Enter to download more chapters or Ctrl+C to exit...")
    except KeyboardInterrupt:
        print("\nExiting program. Goodbye!")
