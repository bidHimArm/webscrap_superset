"""
Install packages
"""


"""
Import packages
"""

import codecs
from progress.bar import Bar
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
import time
import datetime
import os
import getpass 


username = input('Enter username: ')
pswd =getpass.getpass('Password: ')
# pswd = input("Password:")
dashboard=input("Input dashboard name:") # for exemple "Degrilleur - rapport"
Url="https://3-1457-superset.public.a4.saagie.io/login/"

"""
Install phantomjs
"""
# from subprocess import call
# curdir=os.getcwd()

# call(['sudo','apt-get','update'])
# call(['sudo','apt-get','install','build-essential chrpath libssl-dev libxft-dev'])
# call(['sudo','apt-get','install','libfreetype6 libfreetype6-dev'])
# call(['sudo','apt-get','install','libfontconfig1 libfontconfig1-dev'])
# os.chdir(os.path.expanduser("~"))
# call(['export', 'PHANTOM_JS = "phantomjs-2.1.1-linux-x86_64"'])
# call(['wget', 'https://bitbucket.org/ariya/phantomjs/downloads/$PHANTOM_JS.tar.bz2'])
# call(['sudo','tar','xvjf','$PHANTOM_JS.tar.bz2'])
# call(['sudo','mv','$PHANTOM_JS','/usr/local/share'])
# call(['sudo','ln','-sf','/usr/local/share','/$PHANTOM_JS/bin/phantomjs','/usr/local/bin'])
# print("PhantomJs version is: ", str(os.system('phantomjs --version')))
# os.chdir(curdir)

"""
Do the job :-
"""

def superset_login(url,Username,Password,DashboardName):
	driver = webdriver.PhantomJS()
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
	bar = Bar('Processing', max=3)
	for tt in range(3):
		time.sleep(1)
		bar.next()
	bar.finish()
	
	driver.execute_script("(document.getElementsByClassName('navbar'))[0].style.display = 'none';")
	driver.execute_script("(document.getElementsByClassName('dashboard-header'))[0].style.display = 'none';")
	date_v  = datetime.datetime.today().strftime('%Y-%m-%d')
	driver.save_screenshot("rapport_journalier "+ date_v +".png")
	print('Start printing...')
	driver.execute_script("window.print()")
	print('The dashboard has been printed')
	
	driver.quit()

html_sortie = superset_login(url=Url,Username=username,Password=pswd,DashboardName=dashboard)


