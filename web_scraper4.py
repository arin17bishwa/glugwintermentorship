import requests
from bs4 import BeautifulSoup

for i in range(1,23):
	#print(" "*8,"PAGE--",i)
	url="https://www.oyorooms.com/hotels-in-mumbai/?page="+str(i)
	src_site=requests.get(url).text
	soup=BeautifulSoup(src_site,'lxml')

	hotel_list=soup.find('div',class_='oyo-row oyo-row--no-spacing ListingHotelCardWrapper')
	for hotel_info in hotel_list.find_all('div',class_='hotelCardListing__descriptionWrapper'):
		hotel_name=hotel_info.find('div',class_='listingHotelDescription__contentWrapper--left')
		hotel_name=hotel_name.a.h3.text
		print("HOTEL NAME:  ",hotel_name)
		hotel_address=hotel_info.find('div',class_='d-body-lg listingHotelDescription__hotelAddress')
		hotel_address=hotel_address.span.text
		print("HOTEL ADDRESS:",hotel_address)
		price_info=hotel_info.find('div',class_='listingPrice__numbers')
		try:
			offer_price=price_info.find('span',class_='listingPrice__finalPrice')
			print("PRICE: ",offer_price.text)
		except Exception as e:
			print("PRICE : UNAVAILABLE (SOLD OUT)")
		
		print()


