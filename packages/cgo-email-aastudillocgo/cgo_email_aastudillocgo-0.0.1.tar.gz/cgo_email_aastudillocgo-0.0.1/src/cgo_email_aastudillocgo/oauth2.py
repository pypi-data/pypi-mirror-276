"""
Adapted from:
https://github.com/google/gmail-oauth2-tools/blob/master/python/oauth2.py
https://developers.google.com/identity/protocols/OAuth2

1. Generate and authorize an OAuth2 (generate_oauth2_token)
2. Generate a new access tokens using a refresh token(refresh_token)
3. Generate an OAuth2 string to use for login (access_token)
"""

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import base64
import json
import datetime
import smtplib
import urllib.parse
import urllib.request
import lxml.html


GOOGLE_ACCOUNTS_BASE_URL = 'https://accounts.google.com'

def generate_oauth2_string(username, access_token, as_base64=False):
    auth_string = 'user=%s\1auth=Bearer %s\1\1' % (username, access_token)
    if as_base64:
        auth_string = base64.b64encode(auth_string.encode('ascii')).decode('ascii')
    return auth_string

def add_time(current_time, expires_in):
    dummy_date = datetime.datetime.today().strftime('%Y-%m-%d')
    current_datetime = datetime.datetime.strptime(dummy_date + ' ' + str(current_time), '%Y-%m-%d %H:%M:%S.%f')

    return current_datetime + datetime.timedelta(seconds=expires_in)

def command_to_url(command):
    return '%s/%s' % (GOOGLE_ACCOUNTS_BASE_URL, command)

def call_refresh_token(client_id, client_secret, refresh_token):
    params = {}
    params['client_id'] = client_id
    params['client_secret'] = client_secret
    params['refresh_token'] = refresh_token
    params['grant_type'] = 'refresh_token'
    request_url = command_to_url('o/oauth2/token')
    response = urllib.request.urlopen(request_url, urllib.parse.urlencode(params).encode('UTF-8')).read().decode('UTF-8')
    return json.loads(response)

def refresh_authorization(google_client_id, google_client_secret, refresh_token):
    response = call_refresh_token(google_client_id, google_client_secret, refresh_token)
    return response['access_token'], response['expires_in']

def send_mail(fromaddr, toaddr, subject, message, credentials):
    GOOGLE_CLIENT_ID = credentials['client_id']
    GOOGLE_CLIENT_SECRET = credentials['client_secret']
    GOOGLE_REFRESH_TOKEN = credentials['refresh_token']
    expires_in = credentials['expires_in']
    current_time = datetime.datetime.now().time()

    access_token, expires_in = refresh_authorization(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REFRESH_TOKEN)
    expires_in = add_time(current_time, expires_in)

    auth_string = generate_oauth2_string(fromaddr, access_token, as_base64=True)

    msg = MIMEMultipart('related')
    msg['Subject'] = subject
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg.preamble = 'This is a multi-part message in MIME format.'
    msg_alternative = MIMEMultipart('alternative')
    msg.attach(msg_alternative)
    part_text = MIMEText(lxml.html.fromstring(message).text_content().encode('utf-8'), 'plain', _charset='utf-8')
    part_html = MIMEText(message.encode('utf-8'), 'html', _charset='utf-8')
    msg_alternative.attach(part_text)
    msg_alternative.attach(part_html)
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo(GOOGLE_CLIENT_ID)
    server.starttls()
    server.docmd('AUTH', 'XOAUTH2 ' + auth_string)
    server.sendmail(fromaddr, toaddr, msg.as_string())
    server.quit()

    return GOOGLE_REFRESH_TOKEN, access_token, str(expires_in)

def send_email(config, subject, message):
    return send_mail(config['sender'], config['destination_email'], subject, message, config)
