# coding: UTF-8
import requests
from bs4 import BeautifulSoup
import json
import version
import urllib2
import pandas as pd

def scrape_page(ver) :
    url = 'https://lucene.apache.org/solr/4_5_0/changes/Changes.html'
    try:
        r = requests.get(url)
    except :
        throw_error('cannot open: ' + url)
        return
    r.encoding = r.apparent_encoding
    html_src = r.text.encode('utf-8')
    soup = BeautifulSoup(html_src, 'html.parser')
    result_table = soup.find(id='v'+ver+'.bug_fixes.list')
    list = []
    for li in result_table.findAll('li',''):
        if li.a:
            list.append( li.a.string )
    return list

def get_patch_file(url):
    # print url
    DOMAIN = 'https://issues.apache.org'
    try:
        r = requests.get(url)
    except :
        throw_error('cannot open: ' + url)
        return
    r.encoding = r.apparent_encoding
    html_src = r.text.encode('utf-8')
    soup = BeautifulSoup(html_src, 'html.parser')
    for dt in soup.findAll('dt',''):
        # print dt
        if dt.a:
            patch_url = dt.a.get('href')
            url_prefix = patch_url.split('.')[-1]
            if url_prefix == 'patch' or url_prefix == 'txt':
                return DOMAIN + patch_url
    return


def get_bug_modules(list) :
    bug_modules = []
    for bugNo in list:
        print bugNo
        url = 'https://issues.apache.org/jira/browse/' + bugNo
        # url = 'https://issues.apache.org/jira/secure/attachment/12537918/' + bugNo + '.patch'
        patch_file = get_patch_file(url)
        # open patch_file
        # print patch_file
        if patch_file:
            response = urllib2.urlopen(patch_file)
            html = response.read()
            lines = str.splitlines(html)

            for line in lines:
                index_line = []
                if 'Index: ' in line:
                    index_line = line.split(' ')
                    module_name = index_line[1]
                    if module_name.split('.')[-1] == 'java':
                        print module_name
                        bug_modules.append(module_name)

                elif 'diff --git' in line:
                    index_line = line.split(' ')
                    module_name = index_line[2]
                    if module_name.split('.')[-1] == 'java':
                        print module_name
                        bug_modules.append(module_name)

        else:
            print bugNo + 'does not have patch file'
    return bug_modules

def throw_error(error_message):
    f = open("./not_found.txt","a")
    f.write(error_message)

dict = {}
vers = version.get_version_list()
for ver in vers :
    print ver
    list = scrape_page(ver)
    bug_modules = get_bug_modules(list)

    # remove duplicates
    bug_modules = pd.DataFrame(bug_modules)
    bug_modules = bug_modules.drop_duplicates()

    # save bug modules
    bug_modules.to_csv( './../metrics/numBug/slr_'+ver+'_bgmd.csv', index=False, cols=None )


f = open('./../slr_bug_list.json','w')
json.dump(dict,f)

# count the number of bug
for ver in vers :
    filename = './../metrics/numBug/slr_'+ver+'_bgmd.csv'
    df = pd.read_csv(filename, header=0)
    length = df.size
    print (ver, length)
