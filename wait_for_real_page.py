import time


def wait_for_real_page(driver, image_url_prefix, timeout=60):

    html = driver.page_source.lower()

    if "just a moment..." in html:
        time.sleep(2)


    if image_url_prefix in html:
        return True

    return False
