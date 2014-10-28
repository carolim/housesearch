import requests
from bs4 import BeautifulSoup, NavigableString
import sqlite3


# grabs all titles of houses on page
def get_house_titles(soup):
	page_titles = soup.find_all('a', class_="hdrlnk")
	titles = []
	for title in page_titles:
		string = title.contents[0]
		titles.append(unicode(string))
	return titles

# grabs all prices of houses on page
def get_house_prices(soup):
	page_prices = soup.find_all(class_="price")
	prices = []
	for price in page_prices:
		string = price.contents[0]
		prices.append(unicode(string))
	return prices

# grabs all locations of houses on page
def get_house_locations(soup):
	page_locations = soup.find_all(class_="pnr")
	locations = []
	for location in page_locations:
		string = location.contents[1].contents[0].strip(" ()")
		locations.append(unicode(string))
	return locations


# grabs date of all listings on page
# TODO: convert to date object!!!
def get_house_listingdate(soup):
	page_listdate = soup.find_all(class_="pl")
	listdate = []
	for date in page_listdate:
		string = date.contents[1].contents[0]
		listdate.append(unicode(string))
	return listdate


def main():
	url = 'http://philadelphia.craigslist.org/search/apa?bedrooms=6'
	req = requests.get(url)
	soup = BeautifulSoup(req.text)
	print get_house_titles(soup)


if __name__ == '__main__':
	main()
