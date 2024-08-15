#!/usr/bin/env python
# coding: utf-8

import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import smtplib
import time
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate


# Load environment variables from .env file
load_dotenv()

# Email configuration
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
TO_EMAIL = os.getenv("TO_EMAIL")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))


# URLs of the websites
URLS = {
    "linux-systemadministration": "https://it-fortbildung.nrw.de/seminarprogramm/linux-systemadministration-2024-bsis-linadm-000",
    "linux-netzwerkadministration": "https://it-fortbildung.nrw.de/seminarprogramm/linux-netzwerkadministration-2024-bsis-linnet-000"
}

# File names to store the previously seen seminar dates
FILES = {
    "linux-systemadministration": "systemadministration.txt",
    "linux-netzwerkadministration": "netzwerkadministration.txt"
}


def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = TO_EMAIL
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, TO_EMAIL, msg.as_string())
        print(f"Email sent successfully with subject: {subject}")
    except Exception as e:
        print(f"Failed to send email: {e}")

def check_url_validity(url, course_name):
    response = requests.get(url)
    if "Die Seite wurde nicht gefunden" in response.text:
        send_email(f"Broken Link Detected for {course_name}", f"The URL is no longer valid: {url}")
        return False
    return True

def get_seminar_dates(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all elements with the relevant class that contains the seminar dates
    date_elements = soup.find_all("div", class_="field field--name-field-event-date field--type-datetime field--label-inline")

    # Extract and clean the text from these elements
    seminar_dates = [element.get_text(strip=True).replace('Beginn', '').strip() for element in date_elements]
    return seminar_dates

def load_previous_dates(file_name):
    if os.path.exists(file_name):
        with open(file_name, "r") as file:
            return file.read().splitlines()
    return []

def save_current_dates(dates, file_name):
    with open(file_name, "w") as file:
        for date in dates:
            file.write(f"{date}\n")

def check_for_new_dates(url, file_name, course_name):
    if check_url_validity(url, course_name):
        current_dates = get_seminar_dates(url)
        previous_dates = load_previous_dates(file_name)
    
        new_dates = [date for date in current_dates if date not in previous_dates]
    
        if new_dates:
            print(f"New dates found for {course_name}: {new_dates}")
            send_email(f"{course_name} Neue Termine", f"New seminar dates found for {course_name}:\n\n{new_dates}\n\nCheck the website: {url}")
            save_current_dates(current_dates, file_name)
        else:
            print(f"No new dates found for {course_name}.")

if __name__ == "__main__":
    for course_name, url in URLS.items():
        check_for_new_dates(url, FILES[course_name], course_name)

