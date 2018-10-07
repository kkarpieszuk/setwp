#!/usr/bin/python

import os, re
import xml.etree.ElementTree as ET

sites_directory = "/var/www/html"
issue_link = "https://onthegosystems.myjetbrains.com/youtrack/rest/issue/"
replaces = {
    "ai": "wpmlai",
    "bridge": "wpmlbridge",
    "supp": "compsupp"
}

jsessionid = "leo93qxqshqo1ilkfyyrq5v6n"


def clean_projects():
    xml = os.popen("curl 'https://onthegosystems.myjetbrains.com/youtrack/rest/issue/wpmlai-77' -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' -H 'Accept-Language: pl,en-US;q=0.7,en;q=0.3' --compressed -H 'Cookie: JSESSIONID="+jsessionid+"' -H 'DNT: 1' -H 'Connection: keep-alive' -H 'Upgrade-Insecure-Requests: 1' -H 'Cache-Control: max-age=0' -H 'TE: Trailers'").read()

    root = ET.fromstring(xml)

    if root.tag == "issue":
        for field in root.iter("field"):
            if field.attrib['name'] == 'resolved':
                print "resolved"



if __name__ == "__main__":
    clean_projects()