from pydoc import classify_class_attrs

import  requests
from bs4 import BeautifulSoup
enlisted=['tripadvisor','oyorooms','goibibo','booking','cleartrip']#yatra,makemytrip,expedia(returning wrong page)
multiplier=0

def hotel_urls(place_name):
    url_list = []
    already_in = []
    global multiplier
    while len(url_list)<=2:
        g_url = 'https://www.google.com/search?q=hotels+in+' + place_name+'&sxsrf=ACYBGNSBNAVRf3aRpOPzNEpWgVGDAZOLIA:1577611036104&ei=HG8IXtmLBsGa4-EP6Juo-Ag&start='
        g_url=g_url+str(multiplier*10)+'&sa=N&ved=2ahUKEwif077vw9rmAhVxzjgGHckHAVAQ8tMDegQIFxAt&biw=952&bih=936'
        #print(g_url)
        try:
            g_page = requests.get(g_url).text
            g_soup = BeautifulSoup(g_page, 'lxml')
        except Exception as e:
            break
        for match in g_soup.find_all('div', class_='kCrYT'):
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

        multiplier+=1
    return (url_list)

def tripadvisor(page_soup):
    c=0
    hotel_name = 0
    page_soup=page_soup.find('div',class_='bodycon_main')
    for tile in page_soup.find_all('div',class_='ui_column is-8 main_col allowEllipsis'):
        if c==5:
            break
        hotel_name=tile.find('div',class_='listing_title')
        hotel_link=str(hotel_name)
        hotel_link=hotel_link.split('href')[1].split('"')[1]
        hotel_name=hotel_name.a.text
        hotel_price=tile.find('div',class_='price autoResize')
        print('HOTEL NAME:',hotel_name.lstrip().rstrip().split(' \n ')[0])
        print('PRICE:',hotel_price.text)
        print('HOTEL LINK:', str('https://www.tripadvisor.in/' + hotel_link))
        print()
        c+=1

    return 0

def oyorooms(page_soup):
    c=0
    hotel_name = 0
    hotel_list = page_soup.find('div', class_='oyo-row oyo-row--no-spacing ListingHotelCardWrapper')
    for hotel_info in hotel_list.find_all('div', class_='hotelCardListing__descriptionWrapper'):
        if c==5:
            break
        hotel_name = hotel_info.find('div', class_='listingHotelDescription__contentWrapper--left')
        hotel_link=str(hotel_name.a)
        hotel_link=hotel_link.split('href')[1].split('"')[1]
        hotel_link='https://www.oyorooms.com'+hotel_link
        hotel_name = hotel_name.a.h3.text
        print("HOTEL NAME: ", hotel_name.lstrip().rstrip())
        '''hotel_address = hotel_info.find('div', class_='d-body-lg listingHotelDescription__hotelAddress')
        hotel_address = hotel_address.span.text
        print("HOTEL ADDRESS:", hotel_address)'''#You can just unquote this part if you ever want to use this functionality
        price_info = hotel_info.find('div', class_='listingPrice__numbers')
        try:
            offer_price = price_info.find('span', class_='listingPrice__finalPrice')
            print("PRICE:", offer_price.text)
        except Exception as e:
            print("PRICE: UNAVAILABLE (SOLD OUT)")
        print('HOTEL LINK:', hotel_link)
        print()
        c+=1

def goibibo(page_soup):
    c=0
    hotel_name = 0
    for tile in page_soup.find_all('div',class_='width100 fl htlListSeo hotel-tile-srp-container hotel-tile-srp-container-template new-htl-design-tile-main-block'):
        if c==5:
            break
        hotel_name=tile.find('div',class_='hotel-tile-srp-container-content-container')
        hotel_link = str(hotel_name.a)
        hotel_name=hotel_name.a.text
        hotel_link=hotel_link.split('href')[1].split('"')[1]
        hotel_price=tile.find('li',class_='htl-tile-discount-prc')
        hotel_price=hotel_price.text
        print('HOTEL NAME:',hotel_name.lstrip().rstrip().split(' \n ')[0])
        print('PRICE: ',hotel_price)
        print('HOTEL LINK:', hotel_link)
        print()
        c+=1

def booking(page_soup):
    c=0
    hotel_name = 0
    for tile in page_soup.find_all('div',class_='sr__card'):
        if c==5:
            break
        hotel_name=tile.find('header',class_='bui-spacer--medium').h3.text.lstrip().rstrip()
        hotel_link=str(tile.find('header',class_='bui-spacer--medium').a)
        hotel_link = hotel_link.split('href')[1].split('"')[1]
        try:
            hotel_price=tile.find('div',class_='sr__card_price bui-spacer--large').span.text
        except Exception as e:
            hotel_price='UNAVAILABLE'
        print('HOTEL NAME:',hotel_name.lstrip().rstrip().split('\n')[0])
        print('PRICE:',hotel_price)
        print('HOTEL LINK', str('https://www.booking.com' + hotel_link))
        print()
        c+=1

def cleartrip(page_soup):
    c=0
    hotel_name = 0
    page_soup=page_soup.find('div',class_='col-sm-9 pad-lzero m-5')
    for tile in page_soup.find_all('div',class_='hotels-card-cnt'):
        if c==5:
            break
        hotel_name=tile.a
        hotel_link = 'https://www.cleartrip.com'+str(hotel_name).split('href')[1].split('"')[1].split('&')[0]
        try:
            hotel_price=tile.find('div',class_='text-right book-now').a.text
        except Exception as e:
            hotel_price='UNAVAILABLE'
        hotel_name=hotel_name.text
        print('HOTEL NAME: ',hotel_name.lstrip().rstrip())
        print('PRICE:',hotel_price.split('/')[0])
        print('HOTEL LINK: ',hotel_link)
        print()
        c+=1

place_name=input('ENTER YOUR DESTINATOIN:').lstrip().rstrip()
print()
#place_name='hyderabad'
l1=place_name.split()
place_name=l1[0]
for i in range(1,len(l1)):
    place_name=place_name+'+'+l1[i]
#print(place_name)
url_list=hotel_urls(place_name)
#print(url_list)
c = 0
for urls in url_list:
    if c==3:
        break
    site_name=urls.split('.')[1]
    #print(site_name,urls)
    site_page=requests.get(urls.lstrip().rstrip()).text
    #print(1)
    page_soup=BeautifulSoup(site_page,'lxml')
    #print('2')
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

    elif site_name=='cleartrip':
        cleartrip(page_soup)
    c+=1
print('DONE')



'''
def makemytrip(page_soup):
    page_soup=page_soup.find('div',class_='container makeFlex spaceBetween')
    #print(page_soup.prettify())
    for tile in page_soup.find_all('div',class_='listingRowOuter'):
        hotel_name=tile.find('div',class_='makeFlex spaceBetween')
        hotel_name=hotel_name.p.text
        print('HOTEL NAME:',hotel_name.lstrip().rstrip().split(' \n ')[0])

def yatra(page_soup):
    c=0
    hotel_name=0
    print(c)
    #page_soup=page_soup.find('div',class_='result-holder')
    for tile in page_soup.find_all('div',class_='col-sm-9 right-section prel'):
        if c==2:
            break
        hotel_name=tile

        print('HOTEL NAME: ',hotel_name.lstrip().rstrip())
        c+=1
    print('whatever')


def trivago(page_soup):
    c=0
    hotel_name=0
    for tile in page_soup.find_all('div',class_=''):
        if c==5:
            break


def expedia(page_soup):
    c=0
    hotel_name=0
    print(c)
    print(page_soup.prettify())
    for tile in page_soup.find_all('div',class_='uitk-card uitk-grid all-t-margin-three imagelayout-left-fullbleed'):
        print(tile)
        if c==5:
            break
        hotel_name=tile.find('div',class_='truncate uitk-type-600 uitk-type-bold')
        hotel_link=str(hotel_name.a).split('href')[1].split('"')[1]
        hotel_name=hotel_name.a.text
        print('hotel name ',hotel_name.lstrip().rstrip())
        print('link ',hotel_link)


        c+=1

'''
