import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import rsa
import time
from methods import *
import os


# save and load the public and private keys
# it is suggested to keep the keys in a secure
# folder so to not expose them
if not os.path.exists("keys/public.pem"):
    store_keys(num=256)
pub_key, priv_key = load_keys()

# TO REPLACE WITH mail and pwd of unipd account
if not os.path.exists("credentials.txt"):
    USERNAME = input("Insert your email: ")
    PASSWORD = input("Insert your pwd: ")

    # encrypting the credentials
    USERNAME = rsa.encrypt(USERNAME.encode(), pub_key)
    PASSWORD = rsa.encrypt(PASSWORD.encode(), pub_key)

    with open(os.getcwd() + '/credentials.txt', 'wb') as f:
        f.write(USERNAME)
        f.write('\n'.encode())
        print('\n'.encode())
        f.write(PASSWORD)
        f.close

else:
    with open(os.getcwd() + '/credentials.txt', 'rb') as f:
        USERNAME, PASSWORD = f.read().split(b'\n')
        USERNAME = rsa.decrypt(USERNAME, priv_key).decode() + '@studenti.unipd.it'
        PASSWORD = rsa.decrypt(PASSWORD, priv_key).decode()
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
