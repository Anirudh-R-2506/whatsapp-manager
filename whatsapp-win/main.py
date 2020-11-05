#!usr/local/bin/python3
#importing necessary modules
from os import system
from init import whatsapp
try:
    from playsound import playsound
except:
    system('pip install playsound')
    from playsound import playsound
try:
    import speech_recognition as speech
except:
    system('pip install SpeechRecognition')
    import speech_recognition as speech
try:
    from pynput import keyboard
except:
    system('pip install pynput')
    from pynput import keyboard
try:
    import win32gui
except:
    system('pip install win32gui')
    import win32gui
get_foreground_window = lambda : 1 if 'whatsapp' in win32gui.GetWindowText(win32gui.GetForegroundWindow()).lower() else 0#check if web whatsapp is in foreground to trigger shortcuts

def main():#main driver
    
    print('''
KEY
SEND xD ->ALT+X
SEND LOL -> ALT+L
SEND GG -> ALT+G
SEND Ok -> ALT+K
SEND Yes -> ALT+Y
GO TO NEXT CHAT -> ALT+DOWN ARROW
GO TO PREVIOUS CHAT -> ALT+UP ARROW
SEARCH FOR A CONTACT -> ALT+SPACE
DICTATE -> ALT+ENTER    

''')
    global whatsapp_obj,mic,recog
    recog = speech.Recognizer()
    mic = speech.Microphone()    
    whatsapp_obj = whatsapp()
    with keyboard.Listener(on_press=on_press,on_release=on_release) as listener:
        listener.join()

def on_release(key):#remove pressed key from current set on release
    
    try:
        current.remove(key)
    except KeyError:
        pass

def get_spoken_text(recog,mic):#recognise spoken words

    with mic as src:
        recog.adjust_for_ambient_noise(src)
        try:
            playsound(r'C:\whatsapp\data\start.mp3')
            listen = recog.listen(src)
            text = recog.recognize_google(listen)
            playsound(r'C:\whatsapp\data\end.mp3')
            return text
        except speech.UnknownValueError:
            playsound(r'C:\whatsapp\data\except.mp3')  
            return 0             

current = set()
def on_press(key):#interpret all key presses and execute specific jobs

    global whatsapp_obj,recog,mic
    comb_search = {keyboard.Key.alt, keyboard.Key.space}
    comb_speak = {keyboard.Key.alt, keyboard.Key.enter}
    comb_next = {keyboard.Key.alt, keyboard.Key.down}
    comb_prev = {keyboard.Key.alt, keyboard.Key.up}
    comb_lol = {keyboard.Key.alt, keyboard.KeyCode.from_char('l')}
    comb_ok = {keyboard.Key.alt, keyboard.KeyCode.from_char('k')}
    comb_gg = {keyboard.Key.alt, keyboard.KeyCode.from_char('g')}
    comb_yes = {keyboard.Key.alt, keyboard.KeyCode.from_char('y')}
    comb_xD = {keyboard.Key.alt, keyboard.KeyCode.from_char('x')}
    comb_smiley = {keyboard.Key.alt, keyboard.KeyCode.from_char('h')}
    comb_latest = {keyboard.Key.alt, keyboard.KeyCode.from_char('n')}
    if get_foreground_window():
        if key in comb_next:#listen for next chat key
            current.add(key)
            if all(k in current for k in comb_next):
                whatsapp_obj.next_chat()
        elif key in comb_prev:#listen for previous chat key
            current.add(key)
            if all(k in current for k in comb_prev):
                whatsapp_obj.prev_chat()
        elif key in comb_lol:#listen for lol key
            current.add(key)
            if all(k in current for k in comb_lol):
                whatsapp_obj.send_lol()
        elif key in comb_ok:#listen for ok key
            current.add(key)
            if all(k in current for k in comb_ok):
                whatsapp_obj.send_ok()
        elif key in comb_gg:#listen for gg key
            current.add(key)
            if all(k in current for k in comb_gg):
                whatsapp_obj.send_gg()
        elif key in comb_yes:#listen for yes key
            current.add(key)
            if all(k in current for k in comb_yes):
                whatsapp_obj.send_yes()
        elif key in comb_smiley:#listen for laughing emojis key
            current.add(key)
            if all(k in current for k in comb_smiley):
                whatsapp_obj.send_smiley()
        elif key in comb_latest:#listen for jump to latest notification key
            current.add(key)
            if all(k in current for k in comb_latest):
                whatsapp_obj.latest_notification()
        elif key in comb_search:#listen for focus on search box key
            current.add(key)
            if all(k in current for k in comb_search):
                whatsapp_obj.search_box()
        elif key in comb_xD:#listen for xD key
            current.add(key)
            if all(k in current for k in comb_xD):
                whatsapp_obj.send_xD()
        elif key in comb_speak:#listen for speech to text key
            current.add(key)
            if all(k in current for k in comb_speak):
                text = get_spoken_text(recog,mic)
                if text:
                    whatsapp_obj.speak_msg(text)

if __name__ == "__main__":
    main()
