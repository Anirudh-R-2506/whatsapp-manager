#!usr/local/bin/python3
#importing necessary modules
from os import system
from os.path import isdir,isfile
from os import makedirs

try:
    from requests import get
except:
    system('pip install requests')
    from requests import get
try:
    from webdriver_manager.chrome import ChromeDriverManager
except:
    system('pip install webdriver-manager')
    from webdriver_manager.chrome import ChromeDriverManager
try:
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.common.action_chains import ActionChains as actions
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
except:
    system('pip install selenium')
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.common.action_chains import ActionChains as actions
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys

reorder = lambda x : [x[0]]+x[1:][::-1]#reorder the contact list

download = lambda x,y : open(x,'wb').write(get(y,allow_redirects=True).content)

class whatsapp:

    def __init__(self):#initialise driver and login to web whatsapp if not scanned before

        #system('taskkill /IM "chromedriver.exe" /F')
        self.pid = ''
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        options.add_argument('--disable-extensions')
        if not isdir(r'C:\whatsapp\data\Default'):#create user data folder if doesn't exist
            makedirs(r'C:\whatsapp\data\Default',0o777)
        if not isfile(r'C:\whatsapp\data\start.mp3'):#download specch recognition start indicator sound
            download(r'C:\whatsapp\data\start.mp3','http://cvmun2020.000webhostapp.com/start.mp3')
        if not isfile(r'C:\whatsapp\data\end.mp3'):#download specch recognition end indicator sound
            download(r'C:\whatsapp\data\end.mp3','http://cvmun2020.000webhostapp.com/end.mp3')
        if not isfile(r'C:\whatsapp\data\except.mp3'):#download specch recognition exception indicator sound
            download(r'C:\whatsapp\data\except.mp3','http://cvmun2020.000webhostapp.com/except.mp3')
        options.add_argument("user-data-dir=C:\\whatsapp\\data\\Default")#replace dir with the full path to your data dir
        options.add_experimental_option('excludeSwitches',['enable-logging'])
        self.driver=webdriver.Chrome(options=options,executable_path=ChromeDriverManager().install())      
        self.driver.get("https://web.whatsapp.com")
        MAIN = (By.CSS_SELECTOR, "._1QUKR")
        while 1:
            if WebDriverWait(self.driver, 1000).until(EC.element_to_be_clickable(MAIN)):
                self.driver.find_elements_by_class_name('_210SC')[0].click()
                break
        self.driver.execute_script("alert('DO NOT LOG OUT TO AVOID SCANNING QR EVERY TIME');")

    def check_chat(self):#check if user is in a chat window

        try:
            return 1 if self.driver.find_element_by_css_selector('#main header') else 0
        except:
            return 0

    def search_box(self):#shift focues to search box (ctrl+space)

        self.driver.find_element_by_css_selector('._2EoyP').click()

    def send_lol(self):#send lol to current contact (ctrl+l)

        if self.check_chat:
            self.driver.find_element_by_css_selector('#main footer ._3FRCZ').send_keys('LOL'+Keys.ENTER)

    def send_gg(self):#send gg to current contact (ctrl+g)

        if self.check_chat:    
            self.driver.find_element_by_css_selector('#main footer ._3FRCZ').send_keys('GG'+Keys.ENTER)

    def send_ok(self):#send ok to current contact (ctrl+k)
        
        if self.check_chat:
            self.driver.find_element_by_css_selector('#main footer ._3FRCZ').send_keys('Ok'+Keys.ENTER)

    def send_xD(self):#send yes to current contact (ctrl+x)
        
        if self.check_chat:
            self.driver.find_element_by_css_selector('#main footer ._3FRCZ').send_keys('xD'+Keys.ENTER)

    def send_yes(self):#send yes to current contact (ctrl+y)
        
        if self.check_chat:
            self.driver.find_element_by_css_selector('#main footer ._3FRCZ').send_keys('Yes'+Keys.ENTER)

    def speak_msg(self,text):#send received text to current contact (ctrl+enter)
        
        if self.check_chat:
            self.driver.find_element_by_css_selector('#main footer ._3FRCZ').send_keys(text)

    def send_smiley(self):#send 2 laughing emojis to current contact (ctrl+h)
        
        if self.check_chat:
            self.driver.find_element_by_css_selector('#main footer ._3FRCZ').send_keys(':laugh'+Keys.ENTER+':laugh'+Keys.ENTER)
            self.driver.find_element_by_css_selector('#main > footer > div._3ee1T._1LkpH.copyable-area > div:nth-child(3) > button > span').click()
       
    def latest_notification(self):#shift to most recent chat which received notification (ctrl+n)

        for person in reorder(self.driver.find_elements_by_css_selector('_210SC')):
            if person.find_element_by_css_selector("._210SC .m61XR ._31gEB"):
                person.find_element_by_css_selector('._2kHpK ._3ko75._5h6Y_').click()
                break

    def next_chat(self):#shift to next chat (ctrl+down arrow)

        if self.check_chat:            
            current_name = self.driver.find_element_by_xpath('//span[@title = "'+self.driver.find_element_by_css_selector('#main header ._3ko75').text+'"]')
            try:   
                actions(self.driver).move_to_element(current_name).move_by_offset(0,90).click().perform()
            except:
                self.driver.execute_script('document.getElementById("pane-side").scrollTop += 200;')
                try:
                    self.next_chat    
                    actions(self.driver).click().perform()
                except:
                    pass
    
    def prev_chat(self):#shift to previous chat (ctrl+up arrow)
        
        if self.check_chat:
            current_name = self.driver.find_element_by_xpath('//span[@title = "'+self.driver.find_element_by_css_selector('#main header ._3ko75').text+'"]')
            try:
                actions(self.driver).move_to_element(current_name).move_by_offset(0,-90).click().perform()
            except:
                self.driver.execute_script('document.getElementById("pane-side").scrollTop += -200;')
                try:
                    self.prev_chat
                    actions(self.driver).click().perform()
                except:
                    pass