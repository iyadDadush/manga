import pickle
import os

def save_cookies(driver, path="cookies.pkl"):
    with open(path, "wb") as file:
        pickle.dump(driver.get_cookies(), file)
    print("✅ Cookies saved successfully")


def load_cookies(driver, domain_url, path="cookies.pkl"):
    if not os.path.exists(path):
        print("⚠️ No cookies file found")
        return False

    driver.get(domain_url)  # لازم تفتح الدومين أولاً

    with open(path, "rb") as file:
        cookies = pickle.load(file)

    for cookie in cookies:
        # بعض الكوكيز تسبب مشاكل
        cookie.pop("sameSite", None)
        try:
            driver.add_cookie(cookie)
        except Exception:
            pass

    print("✅ Cookies loaded")
    return True
