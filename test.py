import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from methods import *
import os

# TO REPLACE WITH mail and pwd of unipd account
if not os.path.exists("credentials.txt"):
    USERNAME = input("Insert your email: ")
    PASSWORD = input("Insert your pwd: ")
    with open(os.getcwd() + '/credentials.txt', 'w') as f:
        f.write(USERNAME)
        f.write(',')
        f.write(PASSWORD)
        f.close

else:
    with open(os.getcwd() + '/credentials.txt', 'r') as f:
        print(f.readline())
        f.close()


if __name__ == '__main__':
    
    # Loading the driver
    driver = webdriver.Firefox()

    # logging in
    login(USERNAME, PASSWORD, driver)
    # returns the grades and the cfus (a.k.a the weights of the exams)
    g, w = grade_scraping(driver)
    # calculating the weighted mean and the base degree grade
    curr_mean = weighted_mean(g,w)
    b_grade = np.round(base_degree_grade(curr_mean), decimals=2)

    print()
    print(f"Your mean is: {curr_mean} and the expected base grade is: {b_grade}")
    print()
    print(f"Max expected grade if brilliant: {b_grade + incremental_points(b_grade, 'e') + 1}")
    print(f"Max expected grade if very good: {b_grade + incremental_points(b_grade, 'o') + 1}")
    print(f"Max expected grade if good: {b_grade + incremental_points(b_grade, 'b') + 1}")
    print(f"Max expected grade if mediocre: {b_grade + incremental_points(b_grade, 'd') + 1}")
