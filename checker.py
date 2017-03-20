from bs4 import BeautifulSoup
import requests
import time
import sys
import smtplib
import string

mail_server = smtplib.SMTP('localhost', 25)
DEFAULT_RECEIPIENT = 'tigger@applet.ifttt.com'
YOUR_EMAIL= ''
def send_email(receipient, subject, text):
    SMTPserver = "smtp.com"
    # To is a comma-separated list
    From = YOUR_EMAIL
    To = receipient
    Subj = subject
    Text = text
    Body = string.join((
    "From: %s" % From,
    "To: %s" % To,
    "Subject: %s" % Subj,
    "",
    Text,
    ), "\r\n")
    mail_server.sendmail(From,[To],Body)

mail_server.sendmail('song.macbook','lsupperx@gmail.com','title\nxxxx')
headers_list = [
    {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'},
    {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.24 (KHTML, like Gecko) Chrome/56.0.2924.82 Safari/537.32'},
]
product_skuids = {
        '5621780': 'dji-mavic-pro-quadcopter-with-remote-controller-gray', # DJI - Mavic Pro Quadcopter with Remote Controller - Gray
        '5659900': 'dji-mavic-pro-quadcopter-fly-more-combo-gray', # DJI - Mavic Pro Quadcopter Fly More Combo - Gray
        '5683310': 'dji-lithium-polymer-battery-for-mavic-pro-gray', # battery
    }
base_url = 'http://www.bestbuy.com/site/{name}/{skuid}.p?skuid={skuid}'
url_dict = {}
skuids = ['5621780', '5659900', '5683310']
for skuid in skuids:
    url_dict[skuid] = base_url.format(name=product_skuids[skuid], skuid=skuid)

DEFAULT_SECS = 10
sleep_secs = DEFAULT_SECS
headers_index = 0
while True:
    for skuid in skuids:
        url = url_dict[skuid]
        print url
        print headers_list[headers_index]
        resp = requests.get(url, headers=headers_list[headers_index])
        try:
            resp.raise_for_status()
        except:
            e = sys.exc_info()[0]
            print e
            sleep_secs = DEFAULT_SECS * 10 if sleep_secs * 2 > DEFAULT_SECS * 10 else sleep_secs * 2
            if sleep_secs >= DEFAULT_SECS * 10:
                # notify me
                pass
        else:
            sleep_secs = sleep_secs/2 if sleep_secs/2 > DEFAULT_SECS else DEFAULT_SECS
            
        headers_index = (headers_index + 1) % 2
        html = resp.text
        soup = BeautifulSoup(html, 'html.parser')
        result = soup.find_all(attrs = {'data-button-state-id':'ADD_TO_CART'})
        if result:
            print 'BUY %s NOW!'%product_skuids[skuid]
            print url
            send_email(DEFAULT_RECEIPIENT, '#bestbuyBUY!', url)
            skuids.remove(skuid)
    time.sleep(sleep_secs) 
