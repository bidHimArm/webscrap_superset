import codecs
from progress.bar import Bar 
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
import time

username = input('Enter username: ')
pswd = input("Password:")
dashboard=input("Input dashboard name:") # for exemple "Degrilleur - rapport"


Url="https://3-1457-superset.public.a4.saagie.io/login/"


def superset_login(url,Username,Password,DashboardName):
	options=Options()
	options.set_headless(True)
	FFprofile = webdriver.FirefoxProfile()
	FFprofile.set_preference('print.always_print_silent',True)
	driver = webdriver.Firefox(FFprofile,options=options)

	driver.get(url)
	driver.find_element_by_id("username").send_keys(Username)
	driver.find_element_by_id("password").send_keys(Password)
	driver.find_element_by_xpath("//input[@type='submit']").click()
	print('Connexion to superset succeded...')
	delay=10
	# WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'fa fa-fw fa-dashboard')))
	driver.find_element_by_link_text("Dashboards").click()
	driver.find_element_by_link_text(DashboardName).click()
	WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID,'GRID_ID')))
	# driver.save_screenshot("rapport_journalier.png")
	print('Start printing...')
	driver.execute_script("window.print()")
	bar = Bar('Processing', max=20)
	for i in range(20):
		time.sleep(0.9)
		bar.next()
	bar.finish()
	
	print('The dashboard has been printed')
	
	driver.quit()

html_sortie = superset_login(url=Url,Username=username,Password=pswd,DashboardName=dashboard)
