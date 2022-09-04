#!/usr/bin/python
# -*- coding: utf8 -*-

"""
Author: psjs97 (https://github.com/psjs97)
"""

# Libraries
import os
import argparse
from googlesearch import search
from urllib.parse import urlparse
from datetime import datetime


# Arguments
parser = argparse.ArgumentParser(description='Google enum script: subdomain enumeration using Google dorks.',formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-d", "--domain", type=str, help="Domain to get subdomains.", required=True)
parser.add_argument("-o", "--output", type=str, help="Write subdomains to output file.", required=False)
args = parser.parse_args()


# Functions
def get_current_datetime():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("Script execution datetime: ", dt_string)
    print()


def banner():
    # Script banner
    os.system('color')
    print('\033[92m' + '\033[01m' + """
       _____                   _        ______                       
      / ____|                 | |      |  ____|                      
     | |  __  ___   ___   __ _| | ___  | |__   _ __  _   _ _ __ ___  
     | | |_ |/ _ \ / _ \ / _` | |/ _ \ |  __| | '_ \| | | | '_ ` _ \ 
     | |__| | (_) | (_) | (_| | |  __/ | |____| | | | |_| | | | | | |
      \_____|\___/ \___/ \__, |_|\___| |______|_| |_|\__,_|_| |_| |_|
                          __/ |                                      
                         |___/ 
    """ + '\033[0m')
    print('\033[93m' + '\033[01m' +"[ Author: psjs97 ] | https://github.com/psjs97\n" + '\033[0m')


def get_domain_variations(domain):
    # Domain variations for Google query
    domain_variations_list = []
    domain_variations_list.append(domain + '.*') # query: site.com.*
    domain_variations_list.append('*.' + domain) # query: *.site.com
    domain_variations_list.append('*.*.' + domain) # query: *.*.site.com
    domain_variations_list.append('*.*.*.' + domain) # query: *.*.*.site.com
    domain_variations_list.append('*.*.*.*.' + domain) # query: *.*.*.*.site.com
    return domain_variations_list
    
    
def get_subdomains_from_google(domain):
    domain_variations_list = get_domain_variations(domain)
    total_urls_list = []
    for variation in domain_variations_list:
        google_query = "site:DOMAIN"
        google_query = google_query.replace('DOMAIN', variation)
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0'
        urls_list = list(search(google_query, tld="co.in", num=10, stop=None, pause=30.0, user_agent=user_agent))
        total_urls_list.extend(urls_list)

    subdomains_result = []
    for url in total_urls_list:
        subdomains_result.append(urlparse(url).netloc)

    subdomains_result = list(set(subdomains_result)) # Remove duplicated subdomains
    return subdomains_result    

def write_output_file(output_file, subdomains_result):
    with open(output_file, "w") as f:
        f.write("\n".join(str(subdomain) for subdomain in subdomains_result))


def main():
    banner()
    get_current_datetime()
    subdomains_result = get_subdomains_from_google(args.domain)
    
    if args.output is not None:
        write_output_file(args.output, subdomains_result)
    else:
        for subdomain in subdomains_result:
            print(subdomain)
    
if __name__=='__main__':
    main()