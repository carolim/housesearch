import requests
import sqlite3
from bs4 import BeautifulSoup, NavigableString

# creates & populates table to hold info within a given database
def create_houses_table(dbname, houselist):
	try:
		db = sqlite3.connect(dbname)
		print "Successfully connected to database..."
		cursor = db.cursor()
		# create table for houses
		cursor.execute('''
			CREATE TABLE houses(title TEXT, price INTEGER,
				location TEXT, listingdate TEXT)
			''')
		print "Finished creating table..."
		db.commit()

		# insert list of tuples passed in
		cursor.executemany('''INSERT INTO houses(title, price, location, listingdate)
							VALUES(?,?,?,?)''', houselist)
		print "Finished inserting into table..."
		db.commit()
	except Exception as e:
		db.rollback()
		raise e
	finally:
		db.close()


# queries first 5 pages of craigslist
def get_all_houses(url):
	req = requests.get(url) # make a request
	soup = BeautifulSoup(req.text)
	houses = [] # list of tuples to be returned
	for i in range(5):
		params = {'s': str(i*100)}
		req = requests.get(url, params=params)
		soup = BeautifulSoup(req.text)
		titles = get_house_titles(soup)
		prices = get_house_prices(soup)
		locations = get_house_locations(soup)
		listingdate = get_house_listingdate(soup)

		#zip into tuple
		l = zip(titles, prices, locations, listingdate)
		houses.extend(l)
	return houses


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
		string = price.contents[0].lstrip("$")
		prices.append(int(string))
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
# TODO: convert to date object?
def get_house_listingdate(soup):
	page_listdate = soup.find_all(class_="pl")
	listdate = []
	for date in page_listdate:
		string = date.contents[1].contents[0]
		listdate.append(unicode(string))
	return listdate


def main():
	url = 'http://philadelphia.craigslist.org/search/apa?bedrooms=6'
	houselist = get_all_houses(url)
	create_houses_table('houseinfo.db', houselist)


if __name__ == '__main__':
	main()
