from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
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



# Initial Opening of website
s = Service(r"chromedriver_win32/chromedriver.exe")
driver = webdriver.Chrome(service=s)
driver.get("https://gaana.com/songs")


# Gets all the songs 
container = driver.find_elements(By.CSS_SELECTOR, '.song-list > .list_data > ._wrap > ._grp > a.t_over > .t_over')

# Stores the textContent in a list
songsList = [ item.text for item in container ]
print(songsList)




login(driver = driver, username = username, password = password)

# # Opens Login Page
# driver.get('https://accounts.spotify.com/en/login')
# userID = WebDriverWait(driver,20).until(EC.element_to_be_clickable( (By.ID, 'login-username') ))
# userID.send_keys(username)

# password = WebDriverWait(driver,20).until(EC.element_to_be_clickable( (By.ID, 'login-password') ))
# password.send_keys(password)

# login_button = WebDriverWait(driver,20).until(EC.element_to_be_clickable( (By.ID, 'login-button') ))
# login_button.click()

# sleep(2)

# # web_player_button = WebDriverWait(driver,20).until(EC.element_to_be_clickable( (By.CSS_SELECTOR, '[data-testid="web-player-link"]') ))

# # web_player_button.click()









# Opens Spotify to add to liked songs
driver.get('https://open.spotify.com/search')

song = songsList[0]
search_box = WebDriverWait(driver,20).until(EC.element_to_be_clickable( (By.CSS_SELECTOR, 'form[role="search"] > input') ))
search_box.send_keys(song)
search_box.submit()

# row1 = WebDriverWait(driver,20).until(EC.element_to_be_clickable( (By.CSS_SELECTOR, '[role="row"]') ))
row1 = WebDriverWait(driver,20).until(EC.element_to_be_clickable( (By.XPATH, f"//*[text()='{song}']" )))
hover = ActionChains(driver).move_to_element(row1)
hover.perform()

more_button = WebDriverWait(driver,20).until(EC.element_to_be_clickable( (By.CSS_SELECTOR, '[data-testid="more-button"]') ))

# more_button = driver.find_element(By.CSS_SELECTOR, '[data-testid="more-button"]')
more_button.click()

# save_to_liked = WebDriverWait(driver,20).until(EC.element_to_be_clickable( (By.XPATH, "//*[text()='Save to your Liked Songs']") ))
# save_to_liked.click()


add_to_playlist = WebDriverWait(driver,20).until(EC.element_to_be_clickable( (By.XPATH, "//*[text()='Add to playlist']") ))
add_to_playlist.click()


testing = WebDriverWait(driver,20).until(EC.element_to_be_clickable( (By.XPATH, "//button/span[text()='Testing']") ))
testing.click()

# sleep(30)
# driver.close()