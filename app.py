import os
import wget
import time
import getpass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


USERNAME = input("Enter your Insta username: ")
PASSWORD = getpass.getpass()
KEYWORD = "#python"


driver = webdriver.Firefox()

driver.get("http://www.instagram.com")

# Default wait of 15 for every find element
driver.implicitly_wait(15)


def login():
    username = driver.find_element(By.CSS_SELECTOR, "input[name='username']")
    password = driver.find_element(By.CSS_SELECTOR, "input[name='password']")

    username.clear()
    username.send_keys(USERNAME)
    password.clear()
    password.send_keys(PASSWORD)

    button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

    # Click "NOT NOW" when asked for "Save login"
    save_login_or_not_popup = driver.find_element(By.XPATH, '//button[contains(text(), "Not Now")]').click()

    # Click "NOT NOW" when asked for "Desktop notification"
    get_notification_or_not_popup = driver.find_element(By.XPATH, '//button[contains(text(), "Not Now")]').click()


def search_and_download():
    # Searching for a hashtag
    searchbox = driver.find_element(By.XPATH, "//input[@placeholder='Search']")
    searchbox.clear()
    searchbox.send_keys(KEYWORD)
    time.sleep(5)
    my_link = driver.find_element(By.XPATH, "//a[contains(@href, '/" + KEYWORD[1:] + "/')]")
    time.sleep(3)
    my_link.click()
    time.sleep(3)
    # Scroll down 2 times
    n_scrolls = 2
    for j in range(0, n_scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)

    anchors = driver.find_elements(By.TAG_NAME, 'a')
    anchors = [a.get_attribute('href') for a in anchors]
    anchors = [a for a in anchors if str(a).startswith("https://www.instagram.com/p/")]
    print('Found ' + str(len(anchors)) + ' links to images')

    images = []
    for a in anchors:
        driver.get(a)
        time.sleep(5)
        img = driver.find_elements(By.TAG_NAME, 'img')
        img = [i.get_attribute('src') for i in img]
        images.append(img[1])

    time.sleep(2)
    path = os.getcwd()
    path = os.path.join(path, KEYWORD[1:] + "s")
    os.mkdir(path)

    # Download images
    counter = 0
    for image in images:
        print(image)
        save_as = os.path.join(path, KEYWORD[1:] + str(counter) + '.jpg')
        try:
            wget.download(image, save_as)
        except Exception as exc:
            print(f"\nUnable to download the image from link above\n ")
        counter += 1
        print("\n")


if __name__ == "__main__":
    login()
    time.sleep(2)
    search_and_download()
