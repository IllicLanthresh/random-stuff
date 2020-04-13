from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from itertools import product
from string import ascii_uppercase
from difflib import SequenceMatcher
import json

base_url = "https://www.oscaro.es/"

browser = webdriver.Chrome(ChromeDriverManager().install())

run = bool()

start = "BFJ"
end = "HBP"

browser.get(base_url)
sleep(5)


def longestSubstringFinder(string1, string2):  # TODO
    seqMatch = SequenceMatcher(None, string1, string2)
    match = seqMatch.find_longest_match(0, len(string1), 0, len(string2))
    answer = string1[match.a: match.a + match.size]
    return answer


def waitForCaptcha():
    while True:
        sleep(2)
        if len(browser.find_elements_by_id("recaptcha_widget")) == 0:
            break


def getCommon(carList):
    longest = carList[0]
    for car in carList[1:]:
        longest = longestSubstringFinder(longest, car)
    return longest


def reload():
    browser.get(base_url)
    waitForCaptcha()


old_coches = None

database = dict()
try:
    for e in product(ascii_uppercase, repeat=3):
        matricula = "2860" + "".join(e)

        if not run and matricula[-3:] == start:
            run = True
        if run:
            print(matricula[:4] + " " + matricula[-3:], " ----> ", end="")
            while True:
                good = False
                waitForCaptcha()

                if len(browser.find_elements_by_class_name("vehicle-selected")) > 0:
                    change = browser.find_element_by_class_name(
                        "vehicle-selected").find_element_by_xpath("./div/a")
                    change.click()
                    sleep(5)
                    waitForCaptcha()

                if len(browser.find_elements_by_id("vehicle-input-plate")) > 0:
                    box = browser.find_element_by_id("vehicle-input-plate")
                    box.clear()
                    box.send_keys(matricula)

                    button = box.find_element_by_xpath("../../../button")
                    button.click()
                    sleep(5)
                    waitForCaptcha()

                    coches = None
                    if len(browser.find_elements_by_class_name("plate")) > 0:
                        if len(browser.find_elements_by_class_name("form-message")) > 0:
                            coches = ["No Info"]
                            good = True
                        elif len(browser.find_element_by_class_name("plate").find_elements_by_tag_name("select")) > 0:
                            coches = [e.get_attribute("innerHTML") for e in browser.find_element_by_class_name(
                                "plate").find_elements_by_tag_name("option")[1:]]
                            if coches == old_coches or coches == []:
                                reload()
                                continue
                            good = True
                            old_coches = coches
                        else:
                            reload()
                            continue
                    elif len(browser.find_elements_by_class_name("vehicle-selected")) > 0:
                        coches = [browser.find_element_by_class_name(
                            "vehicle-selected").find_elements_by_xpath("./div/span")[0].get_attribute("innerHTML")]
                        good = True
                    else:
                        reload()
                        continue
                if good:
                    print(coches)
                    database[matricula] = coches
                    break
        if run and matricula[-3:] == end:
            run = False
finally:
    #with open()

    print("\n"*4, "dumping database:\n\n", json.dumps(database, indent=4))
