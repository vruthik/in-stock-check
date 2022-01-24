import time
import requests
from bs4 import BeautifulSoup
import numpy as np
from notif import *


def check_sale(url, size, email_login_args, recipient_emails, percent_threshold):
    type_assertions(url, size, email_login_args, recipient_emails, percent_threshold)
    overall_data = {}

    while True:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        prices = soup.find_all('span',  attrs={'class': 'price'})
        original_prices = soup.find_all('span',  attrs={'class': 'list_price'})
        sizes = soup.find_all('span', attrs={'class': 'size'})
        avail_spans = soup.find_all('span', attrs={'class': 'availability'})

        int_data = {}
        size_lst = [size_.getText() for size_ in sizes]
        if size in size_lst:
            idx = size_lst.index(size)
            int_data[size] = {'Availability': [avail_span.getText() for avail_span in avail_spans][idx],
                        'Price': [price.getText() for price in prices][idx],
                        'original_price': [original_price.getText() for original_price in original_prices][idx]}
        else:
            print("Given size doesn't exist on website")

        sale_percent = (1 - (float(int_data[size]['Price']) / float(int_data[size]['original_price']))) * 100
        sale_percent = round(np.abs(sale_percent), 0)

        if int_data[size]['Availability'] != "OutOfStock" and sale_percent >= percent_threshold:
            subject = "Tracked item is on sale!"
            body = "Your tracked item at " + url + " is on sale!\nIt is currently in stock in your desired size " \
                                                   "of " + str(size) + " for " + str(int(sale_percent)) + "% off!"

            # If item is in stock and on sale for more than percent_threshold, send a notifcation to specified users
            send_email_notif(email_login_args, recipient_emails, subject, body)

        # Store data with timestamp as key in case
        overall_data[time.time()] = int_data

        # If more than a month of data exists, delete the oldest datapoint
        if len(overall_data) > 30:
            overall_data.pop(min([k for k in overall_data.keys()]))

        # print(overall_data)
        time.sleep(86400)


def type_assertions(url, size, email_login_args, recipient_emails, percent_threshold):
    assert(type(url) == str)
    assert(type(size) == str)
    assert(type(email_login_args) == dict)
    assert('username' in email_login_args)
    assert('password' in email_login_args)
    assert(type(recipient_emails) == list)
    assert(len(recipient_emails) > 0)
    assert(type(percent_threshold) == float)

