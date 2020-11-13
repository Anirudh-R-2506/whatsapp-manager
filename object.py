#!usr/local/bin/python3
#importing necessary modules
from os import system,name,environ
from time import sleep
if name == "posix":
    from contextlib import suppress
    try:
        import psutil
    except:
        system('pip3 install psutil')
        import psutil

try:
    from webdriver_manager.chrome import ChromeDriverManager
except:
    system('pip3 install webdriver-manager')
    from webdriver_manager.chrome import ChromeDriverManager

try:
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.common.action_chains import ActionChains as actions
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
except:
    system('pip3 install selenium')
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.common.action_chains import ActionChains as actions
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys

reorder = lambda x : [x[0]]+x[1:][::-1]#reorder the contact list
updatedict = lambda x : open('main2.js','w').write(open('main2.js').read().split('];')[0]+",'"+x+"'];") if x not in "10" else 0
if name == "posix":    
    home_dir = 'Users/'+environ['USER']+'/Library/Application Support/Google/Chrome/Default'
elif name == "nt":
    home_dir = environ['USERPROFILE']+'\\AppData\\Local\\Google\\Chrome\\User Data\\Default'
else:
    home_dir = '/home/'+environ['USER']+'/.config/google-chrome/default'
home_dir = 'data/user'

class whatsapp:

    def __init__(self):#initialise driver and login to web whatsapp if not scanned before

        self.pid = ''
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)          
        options.add_argument("user-data-dir="+home_dir)
        options.add_extension('data/auto_correct.crx')
        options.add_experimental_option('excludeSwitches',['enable-logging'])
        self.driver=webdriver.Chrome(options=options,executable_path=ChromeDriverManager().install())      
        self.driver.get("https://web.whatsapp.com")
        MAIN = (By.CSS_SELECTOR, "._1QUKR")
        while 1:
            if WebDriverWait(self.driver, 1000).until(EC.element_to_be_clickable(MAIN)):
                self.driver.find_elements_by_class_name('_210SC')[0].click()
                break
        if name == "posix":            
            for process in psutil.process_iter():
                try:
                    if process.name() == 'Google Chrome' and '--test-type=webdriver' in process.cmdline():
                        with suppress(psutil.NoSuchProcess):
                            self.pid = process.pid
                except:
                    continue
        self.driver.execute_script(open('main.js').read()+"alert('DO NOT LOG OUT TO AVOID SCANNING QR EVERY TIME');")

    def return_pid(self):#returns pid of spawned chrome window

        return self.pid

    def check_chat(self):#check if user is in a chat window

        try:
            return 1 if self.driver.find_element_by_css_selector('#main footer ._3FRCZ') else 0
        except:
            return 0

    def search_box(self):#shift focues to search box (ctrl+space)

        self.driver.find_element_by_css_selector('._2EoyP').click()

    def send_msg(self,text):#send received text to current contact 
        
        if self.check_chat:
            self.driver.find_element_by_css_selector('#main footer ._3FRCZ').send_keys(text)
            self.driver.find_element_by_css_selector('#main > footer > div._3ee1T._1LkpH.copyable-area > div:nth-child(3) > button > span').click()

    def speak_msg(self,text):#send received text to current contact (ctrl+enter)
        
        if self.check_chat:
            self.driver.find_element_by_css_selector('#main footer ._3FRCZ').send_keys(text)

    def jump_to_latest_notification(self):#shift to most recent chat which received notification (ctrl+n)

        for person in self.driver.find_elements_by_css_selector('_210SC'):
            try:
                if person.find_element_by_css_selector("._210SC .m61XR ._31gEB"):
                    person.find_element_by_css_selector('._2kHpK ._3ko75._5h6Y_').click()
                    break
            except:
                pass

    def auto_correct(self,x):#toggle autocorrect on or off

        self.driver.execute_script("console.log(goAhead);")
        if x == '1':
            self.driver.execute_script("goAhead = 0;")
        else:
            self.driver.execute_script("goAhead = 1;")

    def next_chat(self):#shift to next chat (ctrl+down arrow)

        if self.check_chat:            
            current_name = self.driver.find_element_by_xpath('//span[@title = "'+self.driver.find_element_by_css_selector('#main header ._3ko75').text+'"]')
            try:   
                actions(self.driver).move_to_element(current_name).move_by_offset(0,90).click().perform()
            except:
                self.driver.execute_script('document.getElementById("pane-side").scrollTop += 120;')
                sleep(1.2)
                try:
                    self.next_chat    
                    actions(self.driver).click().perform()
                except:
                    pass
    
    def previous_chat(self):#shift to previous chat (ctrl+up arrow)
        
        if self.check_chat:
            current_name = self.driver.find_element_by_xpath('//span[@title = "'+self.driver.find_element_by_css_selector('#main header ._3ko75').text+'"]')
            try:
                actions(self.driver).move_to_element(current_name).move_by_offset(0,-90).click().perform()
            except:
                self.driver.execute_script('document.getElementById("pane-side").scrollTop += -120;')
                sleep(1.2)
                try:
                    self.previous_chat
                    actions(self.driver).click().perform()
                except:
                    pass

    def get_console(self):#to be run in infinite loop as a seperate thread

        x = self.driver.get_log('browser');open('main2.js','w').write(open('main2.js').read().split('];')[0]+",'"+x+"'];") if x not in "10" else self.auto_correct(x)