import csv
from getpass import getpass
from selenium import webdriver
from time import sleep
from random import randrange
from selenium.webdriver.common.keys import Keys
from parsel import Selector
'''
---------------------------------------------------------
This function writes to csv excel file 
---------------------------------------------------------
'''
def write_to_csv(filename,dict_array):
    myFile = open(filename, "w")
    with myFile:
        fieldnames = ['name', 'job description','location']
        writer = csv.DictWriter(myFile, fieldnames=fieldnames)
        writer.writeheader()
        for row in dict_array:
            writer.writerow(row)
'''
---------------------------------------------------------
This function validates field 
---------------------------------------------------------
'''
def validate_field(field):
    if field:
        pass
    else:
        field = ''
    return field
def validate_button(button):
    if button is None:
        return -1
    else:
        return button
'''
------------------------------------------------------------------------
           ASK FOR EMAIL AND PASSWORD
------------------------------------------------------------------------
'''
user_email =input("Enter Email:")
password =getpass()
print("Google Chrome Starting...")
sleep(randrange(5,7))
'''
------------------------------------------------------------------------
            SELENIUM DRIVER STARTS
------------------------------------------------------------------------
'''
driver = webdriver.Chrome()
driver.get("https://www.linkedin.com")
'''
------------------------------------------------------------------------
            SIGN IN
------------------------------------------------------------------------
'''
email_button = driver.find_element_by_xpath('//input[@id="login-email"]')
email_button.send_keys(user_email)
sleep(randrange(3,5))
pass_button = driver.find_element_by_xpath('//input[@id="login-password"]')
pass_button.send_keys(password)
sleep(randrange(3,5))
submit_button = driver.find_element_by_xpath('//input[@id="login-submit"]')
submit_button.click()
print("Log in...")
'''
------------------------------------------------------------------------
            Go to google
------------------------------------------------------------------------
'''
driver.get("https://www.google.com")
search_inp = driver.find_element_by_xpath("//input[@name='q']")
job_title = input("Enter Job Title:")
location = input("Enter Location:")
query_string = 'site:linkedin.com/in/ and "'+job_title+'" and "'+location+'"'
search_inp.send_keys(query_string)
search_inp.send_keys(Keys.RETURN)
urls = driver.find_elements_by_xpath("//h3[@class='r']/a")
linkedin_urls = [url.get_attribute('href') for url in urls]
sleep(10)
next_page = driver.find_element_by_xpath("//a[@id='pnnext']")
next_page.click()
sleep(10)
next_page_urls = driver.find_elements_by_xpath("//h3[@class='r']/a")
next_page_linkedin_urls=[url.get_attribute('href') for url in next_page_urls]
sleep(10)
driver.back()
sleep(10)
'''
---------------------------------------------------------
LinkedIn Profiles Scraping 
---------------------------------------------------------
'''
dict_array=[]
for url in next_page_linkedin_urls:
    print("NEXT PAGE:"+url)
sleep(10)
linkedin_urls.extend(next_page_linkedin_urls)
for linkedin_url in linkedin_urls:
    try:
        driver.get(linkedin_url)
    except Exception:
        continue
    sleep(3)
    sel = Selector(text=driver.page_source)
    try:
        menu_button = driver.find_element_by_xpath("//button[starts-with(@class,'pv-s-profile-actions__overflow-toggle')]")
        menu_button = validate_button(menu_button)
        if menu_button != -1:
            menu_button.click()
    except Exception:
        pass
    sleep(3)
    try:
        follow_button = driver.find_element_by_xpath("//button[@class='pv-s-profile-actions pv-s-profile-actions--follow pv-s-profile-actions__overflow-button full-width text-align-left']")
        follow_button = validate_button(follow_button)
        if follow_button != -1:
            follow_button.click()
    except Exception:
        pass
    sleep(3)
    try:
        save_to_pdf_button =driver.find_element_by_xpath("//button[@class='pv-s-profile-actions pv-s-profile-actions--save-to-pdf pv-s-profile-actions__overflow-button full-width text-align-left']")
        save_to_pdf_button=validate_button(save_to_pdf_button)
        if save_to_pdf_button != -1:
            save_to_pdf_button.click()
    except Exception:
        pass
    sleep(randrange(5, 10))
    name = sel.xpath("//h1[starts-with(@class,'pv-top-card-section__name')]/text()").extract_first()
    name = validate_field(name)
    job_description=sel.xpath("//h2[starts-with(@class,'pv-top-card-section__headline')]/text()").extract_first()
    job_description=validate_field(job_description)
    location = sel.xpath("//h3[starts-with(@class,'pv-top-card-section__location')]/text()").extract_first()
    location  =validate_field(location)
    dict_row={'name':name,'job description':job_description,'location':location}
    dict_array.append(dict_row)
    sleep(randrange(5, 10))
write_to_csv("results.csv",dict_array)
dict_array.clear()
'''
------------------------------------------------------------------------
            Log out
------------------------------------------------------------------------
'''
driver.get('https://www.linkedin.com')
sleep(randrange(5,7))
try:
    nav_menu_button = driver.find_element_by_xpath("//*[@id='nav-settings__dropdown-trigger']")
    nav_menu_button.click()
except Exception:
    pass
sleep(randrange(5,7))
try:
    sign_out_button = driver.find_element_by_xpath("//a[@href='/m/logout/']")
    sign_out_button.click()
except Exception:
    pass
print("Log out...")
sleep(randrange(5,7))

print("Done...")
driver.close()
exit()