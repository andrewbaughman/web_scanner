import sys
import requests
from bs4 import BeautifulSoup
import webbrowser
import time
from urllib.parse import parse_qsl, urljoin, urlparse
import os

file_links = open("thelinks.txt", "w")
all_links = []
done_links = []

def get_em_all(url):
	#print(str(level) + " levels deep")
	#level = level + 1
	print("Now entering :  " + url)
	#webbrowser.open(url, new=2)
	start = time.time()
	page = requests.get(url)
	end = time.time()
	if ((end - start) > 5):
		print('Timeout')
		return
	done_links.append(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	links = soup.findAll('a')
	for link in links:
		if link.get('href') == None:
			continue
		else:
			if ((link.get('href')[0:8] == 'https://') and (link.get('href')[0:20] != 'https://www.facebook')):
				if link.get('href') in all_links:
					continue#print('already done')
				else:
					all_links.append(link.get('href'))
	for found_link in all_links:
		if found_link in done_links:
			continue
		else:
			#if (level % 1 == 0):
			organize_links(all_links)
			get_em_all(found_link)
			#if (level % 20 == 0):
			#	file_links.close() #to change file access modes 
			#	file_links = open("thelinks.txt", "w")

def organize_links(link_list):
	link_tree = {}
	for link in link_list:
		domain = extract_domain(link)
		#print("Original: ", link)
		#print("Extracted: ", domain)
		website = []
		if domain in link_tree:
			#print('Found domain')
			link_tree[domain].append(link)
		else:
			website.append(link)
			link_tree[domain] = website
	display_links(link_tree)
	
def extract_domain(url, remove_http=True):
    uri = urlparse(url)
    if remove_http:
        domain_name = f"{uri.netloc}"
    else:
        domain_name = f"{uri.netloc}://{uri.netloc}"
    return domain_name

def display_links(link_tree):
	os.system("clear")
	for key, value in link_tree.items():
		print('><><><><><><><><> ' + key + ' :')
		file_links.writelines('\n' + '><><><><><><><><> ' + key + ' :') 
		for item in value:
			print('		-' + item)
			file_links.writelines('		-' + item) 
		print('--------------------------')
		file_links.writelines('--------------------------')
	program_time = time.time()
	seconds = (program_time - program_start)
	minutes = (program_time - program_start) / 60
	hours = (program_time - program_start) / 3600
	print("Elapsed Time: " + str(round(minutes)) + ":" + str(round(minutes)) + ":" + str(round(seconds)))
	print(str(len(all_links)) + " locations detected")
	print(str(len(done_links)) + " webpages visited")
	

program_start = time.time()
get_em_all(str(sys.argv[1]))

