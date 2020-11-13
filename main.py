#!usr/local/bin/python3
#importing necessary modules
from os import system,name,environ,makedirs
from os.path import isdir,isfile
from object import whatsapp
from pickle import load
from requests import get
try:
    from playsound import playsound
except:
    system('pip3 install playsound')
    from playsound import playsound
try:
    import speech_recognition as speech
except:
    system('pip3 install SpeechRecognition')
    import speech_recognition as speech
try:
    from pynput import keyboard
except:
    system('pip3 install pynput')
    from pynput import keyboard

if name == "posix":
    from AppKit import NSWorkspace
    get_foreground_window = lambda : 1 if NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationProcessIdentifier'] == whatsapp_obj.return_pid() else 0

elif name == "nt":
    try:
        import win32gui
    except:
        system('pip3 install win32gui')
        import win32gui
    get_foreground_window = lambda : 1 if 'whatsapp' in win32gui.GetWindowText(win32gui.GetForegroundWindow()).lower() else 0#check if web whatsapp is in foreground to trigger shortcuts

get_keys = lambda : load(open('data/keys.keyfile','rb'))

def main():#main driver
    
    global whatsapp_obj,mic,recog
    print_keys()
    recog = speech.Recognizer()
    mic = speech.Microphone()    
    recog.adjust_for_ambient_noise(mic)
    whatsapp_obj = whatsapp()
    with keyboard.Listener(on_press=on_press,on_release=on_release) as listener:
        listener.join()

def on_release(key):#remove pressed key from current set on release
    
    try:
        current.remove(key)
    except KeyError:
        pass

def print_keys():

    key_list = get_keys()
    shortcut_keys = {
    keyboard.KeyCode.from_char('\x01'):'A',
    keyboard.KeyCode.from_char('\x02'):'B',
    keyboard.KeyCode.from_char('\x03'):'C',
    keyboard.KeyCode.from_char('\x04'):'D',
    keyboard.KeyCode.from_char('\x05'):'E',
    keyboard.KeyCode.from_char('\x06'):'F',
    keyboard.KeyCode.from_char('\x07'):'G',
    keyboard.KeyCode.from_char('\x08'):'H',
    keyboard.KeyCode.from_char('\t'):'I',
    keyboard.KeyCode.from_char('\n'):'J',
    keyboard.KeyCode.from_char('\x0b'):'K',
    keyboard.KeyCode.from_char('\x0c'):'L',
    keyboard.KeyCode.from_char('\r'):'M',
    keyboard.KeyCode.from_char('\x0e'):'N',
    keyboard.KeyCode.from_char('\x0f'):'O',
    keyboard.KeyCode.from_char('\x10'):'P',
    keyboard.KeyCode.from_char('\x11'):'Q',
    keyboard.KeyCode.from_char('\x12'):'R',
    keyboard.KeyCode.from_char('\x13'):'S',
    keyboard.KeyCode.from_char('\x14'):'T',
    keyboard.KeyCode.from_char('\x15'):'U',
    keyboard.KeyCode.from_char('\x16'):'V',
    keyboard.KeyCode.from_char('\x17'):'W',
    keyboard.KeyCode.from_char('\x18'):'X',
    keyboard.KeyCode.from_char('\x19'):'Y',
    keyboard.KeyCode.from_char('\x1a'):'Z',
    keyboard.KeyCode.from_char('\x1b'):'[',
    keyboard.KeyCode.from_char('\x1f'):'-',
    keyboard.KeyCode.from_char('\x1c'):'\ ',
    keyboard.KeyCode.from_char('\x1d'):']',
    keyboard.Key.ctrl:'CTRL',
    keyboard.Key.ctrl_r:'RIGHT CTRL',
    keyboard.Key.delete:'DELETE',
    keyboard.Key.space:'SPACE',
    keyboard.Key.enter:'ENTER',
    keyboard.Key.alt:'ALT',
    keyboard.Key.alt_r:'RIGHT ALT',
    keyboard.Key.cmd:'COMMAND/WINDOWS',
    keyboard.Key.cmd_r:'RIGHT COMMAND/WINDOWS',
    keyboard.Key.backspace:'BACKSPACE',
    keyboard.Key.tab:'TAB',
    keyboard.Key.esc:'ESC',
    keyboard.Key.shift:'SHIFT',
    keyboard.Key.shift_r:'RIGHT SHIFT',
    keyboard.Key.caps_lock:'CAPS LOCK',
    keyboard.Key.left:'LEFT',
    keyboard.Key.down:'DOWN',
    keyboard.Key.right:'RIGHT',
    keyboard.Key.up:'UP',
}
    final = "SHORTCUTS LIST\n[TO ADD MORE SHORTCUTS RUN keys.py FILE]\n"
    c = 0
    for key in key_list:
        c += 1
        final += '\n'+str(c)+') '+'+'.join([shortcut_keys[a] for a in key[0]][::-1])
        if isinstance(key[-1],str):
            final += "  -> SEND '"+key[-1]+"'"
        else:
            final += "  -> "+''.join(' '.join(str(key[-1]).split('.')[-1].split('_')).split(' at 0x')[0])
    print(final+'\n\nPRESS SPACE TO AUTOCORRECT LAST WORD AND PRESS SPACE AGAIN TO UNDO CHANGES TO THE WORD')
    return c

def get_spoken_text(recog,mic):#recognise spoken words

    with mic as src:        
        if 1:
            try:
                playsound('data/start.mp3')
                listen = recog.listen(src)
                text = recog.recognize_google(listen)
                playsound('data/end.mp3')
                return text
            except speech.UnknownValueError:
                playsound('data/except.mp3')  
                return 0

current = set()
def on_press(key):#interpret all key presses and execute specific jobs

    global whatsapp_obj,recog,mic
    comb_speak = {keyboard.Key.alt, keyboard.Key.enter}
    key_dict = get_keys()
    if get_foreground_window():
        for comb in key_dict:#check for key match for shortcuts
            if key in comb[0]:
                current.add(key)
                if all(k in current for k in comb[0]):
                    if isinstance(comb[-1],str):
                        whatsapp_obj.send_msg(comb[-1])
                    else:
                        comb[-1]()
                break
        if key in comb_speak:#listen for speech to text key
            current.add(key)
            if all(k in current for k in comb_speak):
                text = get_spoken_text(recog,mic)
                if text:
                    whatsapp_obj.speak_msg(text)

if __name__ == "__main__" and name in ("posix","nt"):
    main()
