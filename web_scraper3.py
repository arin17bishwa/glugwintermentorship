import requests
from bs4 import BeautifulSoup
#lname=[]
#lprice=[]

src_site=requests.get('https://www.trivago.in/mumbai-84780/hotel').text
soup=BeautifulSoup(src_site,'lxml')
#print(soup.prettify())

hotel_list=soup.find('div',class_='clearfix trvsc_toplist')
#print(hotel_list.prettify())

for hotel_info in hotel_list.find_all('div',class_='trvsc_path_info'):
	#print(hotel_info.prettify())
	hotel_name=hotel_info.find('strong',class_='trvsc_path_name').text
	hotel_price=hotel_info.find('strong',class_='trvsc_path_price').text
	print("NAME:  ",hotel_name)
	print("PRICE: ",hotel_price)
	#lname.append(hotel_name)
	#lprice.append(hotel_price)
	print()
	print()

