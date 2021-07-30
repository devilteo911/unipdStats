import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

USERNAME = "YOUR EMAIL"
PASSWORD = "YOUR PWD"


driver = webdriver.Firefox()

def login(username, password):
    driver.get("https://uniweb.unipd.it/Home.do")
    time.sleep(0.1)
    driver.find_element_by_id("hamburger").click()
    time.sleep(0.1)
    driver.find_element_by_id("menu_link-navbox_account_auth/Logon").click()
    time.sleep(3)
    driver.find_element_by_id("j_username_js").send_keys(username)
    driver.find_element_by_id("password").send_keys(password)
    driver.find_element_by_id("login_button_js").click()
    time.sleep(2)
    driver.find_element_by_id("gu_link_sceltacarriera_2293915").click()
    time.sleep(0.1)
    

def grade_scraping():
    driver.find_element_by_id("hamburger").click()
    time.sleep(0.1)
    driver.find_element_by_id("menu_link-navbox_studenti_Home").click()
    time.sleep(0.1)
    driver.find_element_by_id("menu_link-navbox_studenti_auth/studente/Libretto/LibrettoHome").click()
    time.sleep(0.1)
    cfus, grades = np.array([]), np.array([])
    table =  driver.find_element_by_class_name("table-1-body")

    for row in table.find_elements_by_xpath(".//tr"):
        cfus_elem = row.find_elements_by_xpath(".//td[@class='cell-alignC libretto-verticalAlign'][2]")
        grades_elem = row.find_elements_by_xpath(".//td[@class='cell-alignC libretto-verticalAlign'][5]")
        for cfu, grade in zip(cfus_elem, grades_elem):
            trimmed_grade = grade.text.split(' -')[0]
            # If 30L
            trimmed_grade = trimmed_grade.split('L')[0]
            if trimmed_grade == '':
                continue
            try:
                trimmed_grade = int(trimmed_grade)
                grades = np.append(grades, trimmed_grade)
                trimmed_cfu = int(cfu.text)
                cfus = np.append(cfus, trimmed_cfu)
            except Exception:
                continue
        #print([(cfu.text,  grade.text.split(' -')[0]) for cfu, grade in zip(cfus, grades_elem)])

    return grades.T, cfus.T

def weighted_mean(grades, weights):
    return np.dot(grades, weights)/np.sum(w)

def base_degree_grade(mean, rate=3.666666667):
    return mean * rate

def incremental_points(b_grade, flag):
    if flag == 'e':
        return np.round((b_grade*8)/100, decimals=3)
    if flag == 'o':
        return np.round((b_grade*6)/100, decimals=3)
    if flag == 'b':
        return np.round((b_grade*4)/100, decimals=3)
    if flag == 'd':
        return np.round((b_grade*2)/100, decimals=3)
    else:
        return 0


if __name__ == '__main__':
    
    # logging in
    login(USERNAME, PASSWORD)
    g, w = grade_scraping()

    print(g,w)
    curr_mean = weighted_mean(g,w)
    b_grade = np.round(base_degree_grade(curr_mean), decimals=2)

    print()
    print(f"Your mean is: {curr_mean} and the expected base grade is: {b_grade}")
    print()
    print(f"Max expected grade if brilliant: {b_grade + incremental_points(b_grade, 'e') + 1}")
    print(f"Max expected grade if very good: {b_grade + incremental_points(b_grade, 'o') + 1}")
    print(f"Max expected grade if good: {b_grade + incremental_points(b_grade, 'b') + 1}")
    print(f"Max expected grade if mediocre: {b_grade + incremental_points(b_grade, 'd') + 1}")
