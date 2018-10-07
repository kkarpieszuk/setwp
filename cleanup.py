#!/usr/bin/python

import os, re, sys
import xml.etree.ElementTree as ET
import config

sites_directory = "/var/www/html"
issue_link = "https://onthegosystems.myjetbrains.com/youtrack/rest/issue/"
replaces = {
    "ai": "wpmlai",
    "bridge": "wpmlbridge",
    "supp": "compsupp"
}


def clean_projects(argv):
    jsessionid = "xbgzff09qkr91oq2m7jf8vi3b"
    for arg in argv:
        jsessionid = arg

    print jsessionid
    regex = r"(\D+)(\d+)\D*"


    for project_directory_name in next(os.walk(sites_directory))[1]:
        print "###### Investigating directory", project_directory_name
        matchgroups = re.match(regex, project_directory_name)
        if matchgroups:
            project_part = matchgroups.group(1)
            id_part = matchgroups.group(2)
            if project_part in replaces:
                project_part = replaces[project_part]
            full_ticket_id = project_part + "-" + id_part
            print "###### Looks like it is project", full_ticket_id
            
            xml = os.popen("curl 'https://onthegosystems.myjetbrains.com/youtrack/rest/issue/"+full_ticket_id+"' -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' -H 'Accept-Language: pl,en-US;q=0.7,en;q=0.3' --compressed -H 'Cookie: JSESSIONID="+jsessionid+"' -H 'DNT: 1' -H 'Connection: keep-alive' -H 'Upgrade-Insecure-Requests: 1' -H 'Cache-Control: max-age=0' -H 'TE: Trailers'").read()
            root = ET.fromstring(xml)
            if root.tag == "error" and root.text == "You are not logged in.":
                print "Please log in and pass correct jsessionid"
                break;
            if root.tag == "issue":
                for field in root.iter("field"):
                    if field.attrib['name'] == 'resolved':
                        print "###### This ticket looks like resolved"
                        print "###### Dropping database", project_directory_name
                        os.system("echo 'drop database " + project_directory_name + "' | mysql -u" + config.dbuser + " -p" + config.dbpass)
                        print "###### Deleting files from", sites_directory+"/"+project_directory_name
                        os.system("rm -rf " + sites_directory+"/"+project_directory_name)




if __name__ == "__main__":
    clean_projects(sys.argv[1:])