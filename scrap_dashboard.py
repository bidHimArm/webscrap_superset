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
from hdfs import InsecureClient

Username = os.environ.get('SUPERSET_USER')
Password = os.environ.get('SUPERSET_PASSWORD')


username = input('Enter username: ')
pswd = input("Password:")
dashboard=input("Input dashboard name:") # for exemple "Degrilleur - rapport"
url="https://3-1457-superset.public.a4.saagie.io/login/"

"""
Install firefox
"""
# from subprocess import call
# curdir=os.getcwd()
# call(['sudo', 'apt-get', 'update'])
# call(['sudo', 'apt-get', 'install', 'firefox'])


options=Options()
options.set_headless(True)
FFprofile = webdriver.FirefoxProfile()
FFprofile.set_preference('print.always_print_silent',True)
FFprofile.set_preference('print.printer', "Microsoft Print to PDF")
driver = webdriver.Firefox(firefox_profile=FFprofile, options=options)
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
for i in range(3):
	time.sleep(1)
	bar.next()
bar.finish()

driver.execute_script("(document.getElementsByClassName('navbar'))[0].style.display = 'none';")
driver.execute_script("(document.getElementsByClassName('dashboard-header'))[0].style.display = 'none';")
driver.get_screenshot_as_file('/tmp/google.png')
date_v  = datetime.datetime.today().strftime('%Y-%m-%d')
driver.save_screenshot("rapport_journalier "+ date_v +".png")
print('Start printing...')
driver.execute_script("window.print()")
print('The dashboard has been printed')

client_hdfs = InsecureClient('http://' + os.environ['IP_HDFS'] + ':50070', user='projet.degrilleur')
path_result = '/user/projet.degrilleur/Output/Reports'

buf = io.BytesIO()
plt.savefig(buf, format='png')
buf.seek(0)
with client_hdfs.write('/user/hdfs/data/figure.png', overwrite=True) as writer:
    writer.write(buf.getvalue())
buf.close()

driver.quit()
