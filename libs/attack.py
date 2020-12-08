# coding=utf-8
#!/usr/bin/env python3

from requests import Session
from sys import exit
import string
import random

import pprint

from libs.utils import print_success
from libs.utils import print_error
from libs.utils import ask_question
from libs.utils import print_status
from libs.utils import parse_proxy_file
from libs.user_agents import get_user_agent

page_headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "DNT": "1",
}

report_headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded",
    "DNT": "1",
    "Host": "help.instagram.com",
    "Origin": "help.instagram.com",
    "Pragma": "no-cache",
    "Referer": "https://help.instagram.com/contact/497253480400030",
    "TE": "Trailers",
}

def random_str(length):
    letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return ''.join(random.choice(letters) for i in range(length))

def report_profile_attack(username, proxy):
    ses = Session()

    if (proxy != None):
        ses.proxies = {
            "https": "https://" + proxy,
            "http": "https://" + proxy
        }
    
    user_agent = get_user_agent()

    page_headers["User-Agent"] = user_agent
    report_headers["User-Agent"] = user_agent

    try:
        res = ses.get("https://www.facebook.com/", timeout=10)
    except:
        print_error("Connection error has occurred! (FacebookRequestsError)")
        return

    if (res.status_code != 200):
        print_error("Connection error has occurred! (STATUS CODE:", res.status_code, ")")
        return

    if ('["_js_datr","' not in res.text):
        print_error("Connection error has occurred! (CookieErrorJSDatr)")
        return
    
    try:
        js_datr = res.text.split('["_js_datr","')[1].split('",')[0]
    except:
        print_error("Connection error has occurred! (CookieParsingError)")
        return

    page_cookies = {
        "_js_datr": js_datr
    }

    try:
        res = ses.get("https://help.instagram.com/contact/497253480400030", cookies=page_cookies, headers=page_headers, timeout=10)
    except:
        print_error("Connection error has occurred! (InstagramRequestsError)")
        return

    if (res.status_code != 200):
        print_error("Connection error has occurred! (STATUS CODE:", res.status_code, ")")
        return
    
    if ("datr" not in res.cookies.get_dict()):
        print_error("Connection error has occurred! (CookieErrorDatr)")
        return
    
    if ('["LSD",[],{"token":"' not in res.text):
        print_error("Connection error has occurred! (CookieErrorLSD)")
        return

    if ('"__spin_r":' not in res.text):
        print_error("Connection error has occurred! (CookieErrorSpinR)")
        return

    if ('"__spin_b":' not in res.text):
        print_error("Connection error has occurred! (CookieErrorSpinB)")
        return

    if ('"__spin_t":' not in res.text):
        print_error("Connection error has occurred! (CookieErrorSpinT)")
        return

    if ('"server_revision":' not in res.text):
        print_error("Connection error has occurred! (CookieErrorRev)")
        return

    if ('"hsi":' not in res.text):
        print_error("Connection error has occurred! (CookieErrorHsi)")
        return

    try:
        lsd = res.text.split('["LSD",[],{"token":"')[1].split('"},')[0]
        spin_r = res.text.split('"__spin_r":')[1].split(',')[0]
        spin_b = res.text.split('"__spin_b":')[1].split(',')[0].replace('"',"")
        spin_t = res.text.split('"__spin_t":')[1].split(',')[0]
        hsi = res.text.split('"hsi":')[1].split(',')[0].replace('"',"")
        rev = res.text.split('"server_revision":')[1].split(',')[0].replace('"',"")
        datr = res.cookies.get_dict()["datr"]
    except:
        print_error("Connection error has occurred! (CookieParsingError)")
        return

    report_cookies = {
        "datr": datr
    }

    report_form = {
        "jazoest": "2723",
        "lsd": lsd,
        "instagram_username": username,
        "Field241164302734019_iso2_country_code": "IN",
        "Field241164302734019": "India",
        "support_form_id": "497253480400030",
        "support_form_hidden_fields": "{}",
        "support_form_fact_false_fields": "[]",
        "__user": "0",
        "__a": "1",
        "__dyn": "7xe6Fo4SQ1PyUhxOnFwn84a2i5U4e1Fx-ey8kxx0LxW0DUeUhw5cx60Vo1upE4W0OE2WxO0SobEa81Vrzo5-0jx0Fwww6DwtU6e",
        "__csr": "",
        "__req": "d",
        "__beoa": "0",
        "__pc": "PHASED:DEFAULT",
        "dpr": "1",
        "__rev": rev,
        "__s": "5gbxno:2obi73:56i3vc",
        "__hsi": hsi,
        "__comet_req": "0",
        "__spin_r": spin_r,
        "__spin_b": spin_b,
        "__spin_t": spin_t
    }

    try:
        res = ses.post(
            "https://help.instagram.com/ajax/help/contact/submit/page",
            data=report_form,
            headers=report_headers,
            cookies=report_cookies,
            timeout=10
        )
    except:
        print_error("Connection error has occurred! (FormRequestsError)")
        return
    
    if (res.status_code != 200):
        print_error("Connection error has occurred! (STATUS CODE:", res.status_code, ")")
        return
    
    print_success("Connection error has occurred!")

def report_video_attack(video_url, proxy):
    ses = Session()
    if (proxy != None):
        ses.proxies = {
            "https": "https://" + proxy,
            "http": "https://" + proxy
        }
    
    user_agent = get_user_agent()

    page_headers["User-Agent"] = user_agent
    report_headers["User-Agent"] = user_agent

    try:
        res = ses.get("https://www.facebook.com/", timeout=10)
    except Exception as e:
        print_error("Connection error has occurred! (FacebookRequestsError)", e)
        return

    if (res.status_code != 200):
        print_error("Connection error has occurred! (STATUS CODE:", res.status_code, ")")
        return

    if ('["_js_datr","' not in res.text):
        print_error("Connection error has occurred! (CookieErrorJSDatr)")
        return
    
    try:
        js_datr = res.text.split('["_js_datr","')[1].split('",')[0]
    except:
        print_error("Connection error has occurred! (CookieParsingError)")
        return

    page_cookies = {
        "_js_datr": js_datr
    }

    try:
        res = ses.get("https://help.instagram.com/contact/497253480400030", cookies=page_cookies, headers=page_headers, timeout=10)
    except:
        print_error("Connection error has occurred! (InstagramRequestsError)")
        return

    if (res.status_code != 200):
        print_error("Connection error has occurred! (STATUS CODE:", res.status_code, ")")
        return
    
    if ("datr" not in res.cookies.get_dict()):
        print_error("Connection error has occurred! (CookieErrorDatr)")
        return
    
    if ('["LSD",[],{"token":"' not in res.text):
        print_error("Connection error has occurred! (CookieErrorLSD)")
        return

    if ('"__spin_r":' not in res.text):
        print_error("Connection error has occurred! (CookieErrorSpinR)")
        return

    if ('"__spin_b":' not in res.text):
        print_error("Connection error has occurred! (CookieErrorSpinB)")
        return

    if ('"__spin_t":' not in res.text):
        print_error("Connection error has occurred! (CookieErrorSpinT)")
        return

    if ('"server_revision":' not in res.text):
        print_error("Connection error has occurred! (CookieErrorRev)")
        return

    if ('"hsi":' not in res.text):
        print_error("Connection error has occurred! (CookieErrorHsi)")
        return

    try:
        lsd = res.text.split('["LSD",[],{"token":"')[1].split('"},')[0]
        spin_r = res.text.split('"__spin_r":')[1].split(',')[0]
        spin_b = res.text.split('"__spin_b":')[1].split(',')[0].replace('"',"")
        spin_t = res.text.split('"__spin_t":')[1].split(',')[0]
        hsi = res.text.split('"hsi":')[1].split(',')[0].replace('"',"")
        rev = res.text.split('"server_revision":')[1].split(',')[0].replace('"',"")
        datr = res.cookies.get_dict()["datr"]
    except:
        print_error("Connection error has occurred! (CookieParsingError)")
        return

    report_cookies = {
        "datr": datr
    }

    report_form = {
        "jazoest": "2723",
        "lsd": lsd,
        "sneakyhidden": "",
        "Field419623844841592": video_url,
        "Field1476905342523314_iso2_country_code": "IN",
        "Field1476905342523314": "India",
        "support_form_id": "440963189380968",
        "support_form_hidden_fields": '{"423417021136459":false,"419623844841592":false,"754839691215928":false,"1476905342523314":false,"284770995012493":true,"237926093076239":false}',
        "support_form_fact_false_fields": "[]",
        "__user": "0",
        "__a": "1",
        "__dyn": "7xe6Fo4SQ1PyUhxOnFwn84a2i5U4e1Fx-ey8kxx0LxW0DUeUhw5cx60Vo1upE4W0OE2WxO0SobEa81Vrzo5-0jx0Fwww6DwtU6e",
        "__csr": "",
        "__req": "d",
        "__beoa": "0",
        "__pc": "PHASED:DEFAULT",
        "dpr": "1",
        "__rev": rev,
        "__s": "5gbxno:2obi73:56i3vc",
        "__hsi": hsi,
        "__comet_req": "0",
        "__spin_r": spin_r,
        "__spin_b": spin_b,
        "__spin_t": spin_t
    }

    try:
        res = ses.post(
            "https://help.instagram.com/ajax/help/contact/submit/page",
            data=report_form,
            headers=report_headers,
            cookies=report_cookies,
            timeout=10
        )
    except:
        print_error("Connection error has occurred! (FormRequestsError)")
        return
    
    if (res.status_code != 200):
        print_error("Connection error has occurred! (STATUS CODE:", res.status_code, ")")
        return
    
    print_success("Successfully reported!")





