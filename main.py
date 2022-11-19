from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
from time import sleep
import os
from dotenv import load_dotenv

load_dotenv('.env')
username = os.environ["SPOTIFYUSER"]
password = os.environ["SPOTIFYPASSWORD"]


def login(driver, username , password , link = 'https://accounts.spotify.com/en/login'):
	# Opens Login Page
	driver.get(link)
	userID = WebDriverWait(driver,20).until(EC.element_to_be_clickable( (By.ID, 'login-username') ))
	userID.send_keys(username)

	userPassword = WebDriverWait(driver,20).until(EC.element_to_be_clickable( (By.ID, 'login-password') ))
	userPassword.send_keys(password)

	login_button = WebDriverWait(driver,20).until(EC.element_to_be_clickable( (By.ID, 'login-button') ))
	login_button.click()

	sleep(2)

def fetch_songs(driver):
	# Gets all the songs (just the song name)
	# container = driver.find_elements(By.CSS_SELECTOR, '.song-list > .list_data > ._wrap > ._grp > a.t_over > .t_over')

	# Gets all the songs (with artist)
	container = driver.find_elements(By.CSS_SELECTOR, '.song-list > .list_data > ._wrap > ._grp')

	# Stores the textContent in a list
	songsList = [ item.text.replace("\n"," ") for item in container ]

	print(songsList)
	return songsList

def search(driver, song):
	search_box = WebDriverWait(driver,20).until(EC.element_to_be_clickable( (By.CSS_SELECTOR, 'form[role="search"] > input') ))
	search_box.clear()
	search_box.send_keys(song)
	search_box.submit()

def addFirstSong(driver , song , to_playlist = False , playlist_name = ""):

	# Hover on the Song
	# row1 = WebDriverWait(driver,20).until(EC.element_to_be_clickable( (By.XPATH, f"//*[text()='{song}']" )))
	row1 = WebDriverWait(driver,20).until(EC.element_to_be_clickable( (By.CSS_SELECTOR, '[role="row"]') ))
	hover = ActionChains(driver).move_to_element(row1)
	hover.perform()

	# Adds song to liked songs
	if not to_playlist:
		save_to_liked = WebDriverWait(driver,20).until(EC.element_to_be_clickable( (By.CSS_SELECTOR, '[aria-label="Save to Your Library"]') ))
		save_to_liked.click()
		return


	# Click on More button
	more_button = WebDriverWait(driver,20).until(EC.element_to_be_clickable( (By.CSS_SELECTOR, '[data-testid="more-button"]') ))
	more_button.click()

	add_to_playlist = WebDriverWait(driver,20).until(EC.element_to_be_clickable( (By.XPATH, "//*[text()='Add to playlist']") ))
	add_to_playlist.click()

	testing = WebDriverWait(driver,20).until(EC.element_to_be_clickable( (By.XPATH, f"//button/span[text()='{playlist_name}']") ))
	testing.click()

	try:
		ignored_exceptions = (StaleElementReferenceException)
		if button := WebDriverWait(driver,5, ignored_exceptions=ignored_exceptions).until(EC.element_to_be_clickable( (By.XPATH, '//button/span[text()="Don\'t add"]') )):
			button.click()
	except Exception as e:
		print("Exception is \n", e)





def main():
	# Initial Opening of website
	s = Service(r"chromedriver_win32/chromedriver.exe")
	driver = webdriver.Chrome(service=s)
	driver.get("https://gaana.com/songs")


	songsList = fetch_songs(driver = driver)
	login(driver = driver, username = username, password = password)

	driver.get('https://open.spotify.com/search')
	# song = songsList[0]

	for song in songsList:
		sleep(2)
		search(driver, song)
		sleep(2)
		addFirstSong(driver, song, to_playlist = True, playlist_name = "Trending")

	sleep(30)
	driver.close()


if __name__ == '__main__':
	main()

