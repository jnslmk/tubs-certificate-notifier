# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import requests
import re
import configparser

URL = 'https://www.tu-braunschweig.de/fmb/aktuellestermine/termine#Zeugnisausgabe'
    
def send_notification(text, email, recepient, api_key):
    p = requests.post(
        "https://api.mailgun.net/v3/sandboxf9f20535651b426ab55ebc05468cd3f1.mailgun.org/messages",
        auth=("api", api_key),
        data={"from": "Mailgun Sandbox <postmaster@sandboxf9f20535651b426ab55ebc05468cd3f1.mailgun.org>",
              "to": recepient + ' <' + email + '>',
              "subject": "Zeugnisausgabe: Statusänderung",
              "text": text}
        )
    if p.status_code == 200:
        print('Sent email successfully')
    else:
        print('Email sending not successful')

config = configparser.ConfigParser()
config.read('credentials.ini')

matriculation = config['student account']['matriculation-number']
email = config['email account']['email']
recepient = config['email account']['recepient']
api_key = config['email account']['api-key']

website = requests.get(URL).text
number_of_entries = len(re.findall(matriculation, website))
print('Anzahl der Einträge ' + str(number_of_entries))
with open('history.log', 'r') as f:
    last_number_of_entries = int(f.read())
with open('history.log', 'w') as f:
    f.write(str(number_of_entries))
if number_of_entries and number_of_entries != last_number_of_entries:
    print('There have been changes since last execution')
    if number_of_entries == 1:
        mailtext = 'Das Zeugnis wurde erstellt und liegt zur Abholung bereit'
        print('Certificate prepared')
    else:
        mailtext = 'Das Zeugnis wurde korrigiert und liegt zur Abholung bereit'
        print('Certificate corrected')
    send_notification(mailtext, email, recepient, api_key)
else:
    print('No changes since last execution')