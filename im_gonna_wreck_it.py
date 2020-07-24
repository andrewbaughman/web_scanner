import sys
import requests
from bs4 import BeautifulSoup
import webbrowser
import time
from urllib.parse import parse_qsl, urljoin, urlparse

file_links = open("thelinks.txt", "w")
all_links = []

def get_em_all(url, level):
	level = level + 1
	print("Now entering " + url)
	#webbrowser.open(url, new=2)
	start = time.time()
	page = requests.get(url)
	end = time.time()
	if ((end - start) > 5):
		print('Timeout')
		return
	soup = BeautifulSoup(page.content, 'html.parser')
	links = soup.findAll('a')
	for link in links:
		if link.get('href') == None:
			continue
		else:
			if ((link.get('href')[0:8] == 'https://') and (link.get('href')[0:20] != 'https://www.facebook')):
				file_links.writelines(link.get('href') + "\n") 
				if link.get('href') in all_links:
					continue#print('already done')
				else:
					all_links.append(link.get('href'))
					print(str(level) + " levels deep")
					if (level % 5 == 0):
						organize_links(all_links)
					get_em_all(link.get('href'), level)
		
def organize_links(link_list):
	link_tree = {}
	for link in link_list:
		domain = extract_domain(link)
		print("Original: ", link)
		print("Extracted: ", domain)
		website = []
		if domain in link_list:
			print('here')
			website.append(link)
		website.append('yolo')
		website.append('hello')
		website.append('hello')
		#website = ['hello','how', 'are', 'you']
		link_tree[link] = website
	display_links(link_tree)
	
def extract_domain(url, remove_http=True):
    uri = urlparse(url)
    if remove_http:
        domain_name = f"{uri.netloc}"
    else:
        domain_name = f"{uri.netloc}://{uri.netloc}"
    return domain_name

def display_links(link_tree):
	for key, value in link_tree.items():
		print('--------------------------')
		print(key, ' : ', value)
		print('--------------------------')



get_em_all(str(sys.argv[1]), 0)

file_links.close() #to change file access modes 
