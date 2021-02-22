import os
from selenium import webdriver
from time import sleep
import argparse

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

MAX_WAIT_TIMEOUT = 120


def get_arguments():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-v", "--version", help="Windows version or build number", required=True)
    arg_parser.add_argument("-l", "--language", help="Windows Language", default="English International")
    arg_parser.add_argument("-a", "--arch", help="x64 or x32", default="x64")
    return arg_parser.parse_args()


def wait_for_page_to_load(driver):
    wait = WebDriverWait(driver, MAX_WAIT_TIMEOUT, 1)
    wait.until(lambda _driver: _driver.execute_script("return document.readyState") == "complete")


def wait_for_list_to_load(select: WebElement):
    wait = 0
    while len(Select(select).options) < 2:
        sleep(1)
        wait += 1
        if wait == MAX_WAIT_TIMEOUT:
            break


def create_web_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.headless = True

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(MAX_WAIT_TIMEOUT)
    return driver


def select_windows_architecture(driver, required_arch):
    select_file = driver.find_element_by_id("arch_id")
    wait_for_list_to_load(select_file)
    files = Select(select_file)
    for i, file in enumerate(files.options):
        if file.text.find(required_arch) != -1:
            files.select_by_index(i)
            print("Selected File: " + file.text)
            break


def select_windows_language(driver, required_language):
    select_language = driver.find_element_by_id("language_id")
    wait_for_list_to_load(select_language)
    languages = Select(select_language)
    for i, language in enumerate(languages.options):
        if language.text == required_language:
            languages.select_by_index(i)
            print("Selected Language: " + language.text)
            break


def select_normal_windows_10_edition(driver):
    select_edition = driver.find_element_by_id("edition_id")
    wait_for_list_to_load(select_edition)
    editions = Select(select_edition)
    for i, edition in enumerate(editions.options):
        if edition.text == "Windows 10":
            editions.select_by_index(i)
            print("Selected Edition: " + edition.text)
            break


def select_windows_version(driver, required_version):
    select_version = driver.find_element_by_id("version_id")
    wait_for_list_to_load(select_version)
    versions = Select(select_version)
    for i, version in enumerate(versions.options):
        if version.text.find(required_version) != -1:
            versions.select_by_index(i)
            print("Selected Version: " + version.text)
            break


def select_download_type(driver, required_type):
    types = Select(driver.find_element_by_id("type_id"))
    for i, type in enumerate(types.options):
        if type.text == required_type:
            types.select_by_index(i)
            print("Selected Type:" + type.text)
            break


def main(required_type, required_version, required_language, required_arch):
    driver = create_web_driver()
    driver.get("https://tb.rg-adguard.net/public.php")

    wait_for_page_to_load(driver)

    select_download_type(driver, required_type)
    select_windows_version(driver, required_version)
    select_normal_windows_10_edition(driver)
    select_windows_language(driver, required_language)
    select_windows_architecture(driver, required_arch)

    download_button = driver.find_element_by_css_selector(".buttond a")
    download_link = download_button.get_attribute("href")
    print(download_link)
    os.system(f"wget -O win.iso '{download_link}'")
    driver.quit()


if __name__ == "__main__":
    args = get_arguments()
    main("Windows (Final)", args.version, args.language, args.arch)
