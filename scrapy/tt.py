from selenium import webdriver
from bs4 import BeautifulSoup


driver = webdriver.Chrome(executable_path="C:/Users/costa\chromedriver.exe")
driver.get('https://www.i-traffic.co.za/traffic/time_speed.aspx')
next = driver.find_elements_by_xpath('//td[@class="listPagerCell"]/a')[-1]
next.click()

info = driver.find_elements_by_xpath('//table[@class="listGridView"]//tr')[2]
soup = BeautifulSoup(info.get_attribute('innerHTML'), 'lxml')
data = []
for item in soup.find_all('span'):
    data += [item.get_text()]