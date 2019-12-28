from pydoc import classify_class_attrs

import  requests
from bs4 import BeautifulSoup
enlisted=['tripadvisor','oyorooms','goibibo','booking']
def hotel_urls(place_name):
    g_url = 'https://www.google.com/search?q=hotels+in+' + place_name
    ##print(g_url)
    g_page = requests.get(g_url).text
    g_soup = BeautifulSoup(g_page, 'lxml')
    url_list=[]
    already_in=[]
    for match in g_soup.find_all('div', class_='kCrYT'):
        if len(url_list) > 2:
            break
        try:
            match = str(match.a)
            match = match.split('=')[2]
            match=match.split('&')[0]
            name=match.split('.')[1]
            if (name in enlisted) and (name not in already_in):
                url_list.append(match)
                already_in.append(name)

        except Exception as e:
            pass
    return (url_list)

def tripadvisor(page_soup):
    c=0
    page_soup=page_soup.find('div',class_='bodycon_main')
    for tile in page_soup.find_all('div',class_='ui_column is-8 main_col allowEllipsis'):
        if c==5:
            break
        hotel_name=tile.find('div',class_='listing_title')
        hotel_link=str(hotel_name)
        hotel_link=hotel_link.split('href')[1].split('"')[1]
        hotel_name=hotel_name.a.text
        hotel_price=tile.find('div',class_='price autoResize')
        print('HOTEL NAME:',hotel_name)
        print('PRICE:',hotel_price.text)
        print('HOTEL LINK:', str('https://www.tripadvisor.in/' + hotel_link))
        print()
        c+=1
    return 0

def oyorooms(page_soup):
    c=0
    hotel_list = page_soup.find('div', class_='oyo-row oyo-row--no-spacing ListingHotelCardWrapper')
    for hotel_info in hotel_list.find_all('div', class_='hotelCardListing__descriptionWrapper'):
        if c==5:
            break
        hotel_name = hotel_info.find('div', class_='listingHotelDescription__contentWrapper--left')
        hotel_link=str(hotel_name.a)
        hotel_link=hotel_link.split('href')[1].split('"')[1]
        hotel_link='https://www.oyorooms.com'+hotel_link
        hotel_name = hotel_name.a.h3.text
        print("HOTEL NAME: ", hotel_name)
        '''hotel_address = hotel_info.find('div', class_='d-body-lg listingHotelDescription__hotelAddress')
        hotel_address = hotel_address.span.text
        print("HOTEL ADDRESS:", hotel_address)'''#You can just unquote this part if you ever want to use this functionality
        price_info = hotel_info.find('div', class_='listingPrice__numbers')
        print('HOTEL LINK:', hotel_link)
        try:
            offer_price = price_info.find('span', class_='listingPrice__finalPrice')
            print("PRICE:", offer_price.text)
        except Exception as e:
            print("PRICE: UNAVAILABLE (SOLD OUT)")
        print()
        c+=1

'''
def makemytrip(page_soup):
    page_soup=page_soup.find('div',class_='container makeFlex spaceBetween')
    #print(page_soup.prettify())
    for tile in page_soup.find_all('div',class_='listingRowOuter'):
        hotel_name=tile.find('div',class_='makeFlex spaceBetween')
        hotel_name=hotel_name.p.text
        print('hotel name:',hotel_name)
'''

def goibibo(page_soup):
    c=0
    for tile in page_soup.find_all('div',class_='width100 fl htlListSeo hotel-tile-srp-container hotel-tile-srp-container-template new-htl-design-tile-main-block'):
        if c==5:
            break
        hotel_name=tile.find('div',class_='hotel-tile-srp-container-content-container')
        hotel_link = str(hotel_name.a)
        hotel_name=hotel_name.a.text
        hotel_link=hotel_link.split('href')[1].split('"')[1]
        hotel_price=tile.find('li',class_='htl-tile-discount-prc')
        hotel_price=hotel_price.text
        print('HOTEL NAME:',hotel_name)
        print('PRICE: ',hotel_price)
        print('HOTEL LINK:', hotel_link)
        print()
        c+=1

def booking(page_soup):
    c=0
    for tile in page_soup.find_all('div',class_='sr__card'):
        if c==5:
            break
        hotel_name=tile.find('header',class_='bui-spacer--medium').h3.text.lstrip().rstrip()
        hotel_link=str(tile.find('header',class_='bui-spacer--medium').a)
        hotel_link = hotel_link.split('href')[1].split('"')[1]
        hotel_price=tile.find('div',class_='sr__card_price bui-spacer--large').span.text
        print('HOTEL NAME:',hotel_name)
        print('PRICE:',hotel_price)
        print('HOTEL LINK', str('https://www.booking.com' + hotel_link))
        print()
        c+=1


place_name=input('Enter your destination: ').lstrip().rstrip()
#place_name='chennai'
#print(place_name)
url_list=hotel_urls(place_name)
#print(url_list)
for urls in url_list:
    site_name=urls.split('.')[1]
    #print(site_name,urls)
    site_page=requests.get(urls).text
    page_soup=BeautifulSoup(site_page,'lxml')
    if site_name=='tripadvisor':
        tripadvisor(page_soup)
    elif site_name=='oyorooms':
        oyorooms(page_soup)
    elif site_name=='makemytrip':
        makemytrip(page_soup)
    elif site_name=='goibibo':
        goibibo(page_soup)
    elif site_name=='booking':
        booking(page_soup)

#print('done')
