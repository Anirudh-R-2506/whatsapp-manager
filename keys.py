#!usr/local/bin/python3
#importing necessary modules
from os import system,name,environ
from pickle import load,dump
from threading import Thread
global shortcut_keys
from object import whatsapp as whatsapp_obj
try:
    from pynput import keyboard
except:
    system('pip3 install pynput')
    from pynput import keyboard
global msg,goOn
msg = ''
goOn = 1
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
home_dir = 'data/'
key_dict_read = lambda : load(open(home_dir+'keys.keyfile','rb'))
key_dict_write = lambda x : dump(x,open(home_dir+'keys.keyfile','wb'))

def get_keys(key_set):

    final = ''
    for a in key_set:
        if isinstance(a,str):
            final += a.upper()
        else:
            final += shortcut_keys[a]
        final += '+'
    return '+'.join(final.split('+'))

def del_shortcut(key_count):
    
    key_list = key_dict_read()
    c = 0
    update = []
    for key in key_list:
        c+=1
        if c == key_count:
            continue
        update.append(key)
    key_dict_write(update)


def edit_shortcut(key_count):

    global msg
    key_list = key_dict_read()
    c = 0
    for key in key_list:
        c+=1
        if c == key_count:
            if isinstance(key[-1],str):
                msg = input('[-] ENTER MESSAGE TO MAP TO SHORTCUT KEY ')
                print('[-] PRESS YOUR DESIRED SHORTCUT KEYS (MAKE SURE THEY DIFFER FROM GLOBAL SHORTCUTS)')
            else:
                msg = key[-1]
                print('[-] PRESS YOUR DESIRED SHORTCUT KEYS (MAKE SURE THEY DIFFER FROM GLOBAL SHORTCUTS)')

def print_keys():

    key_list = key_dict_read()
    final = "\nSHORTCUTS LIST\n"
    c = 0
    for key in key_list:
        c += 1
        final += '\n'+str(c)+') '+'+'.join([shortcut_keys[a] for a in key[0]][::-1])
        if isinstance(key[-1],str):
            final += "  -> SEND '"+key[-1]+"'"
        else:
            final += "  -> "+''.join(' '.join(str(key[-1]).split('.')[-1].split('_')).split(' at 0x')[0])
    print(final)
    return c

current = set()
def on_press(key):#interpret all key presses
    current.add(key)

def on_release(key):#remove pressed key from current set on release
    global msg,goOn
    if msg:
        while 1:
            try:
                go_on = input('\n[-] DO YOU WANT TO USE '+get_keys(current)+' FOR '+msg+'(Y/N)? ') if isinstance(msg,str) else input('\n[-] DO YOU WANT TO USE '+get_keys(current)+' FOR '+str(msg).split('.')[-1]+'(Y/N)? ')
                if go_on.lower() in 'yn':
                    break
                else:
                    print('\n[-] INVALID CHOICE')
                    continue
            except:
                print('\n[-] INVALID CHOICE')
                continue
        if go_on.lower() == 'y':
            key_dict_write(key_dict_read().append([current,msg]))
            goOn = 0
        else:
            print('[-] PRESS YOUR DESIRED SHORTCUT KEYS (MAKE SURE THEY DIFFER FROM GLOBAL SHORTCUTS)')
            goOn = 1

def listen():
    with keyboard.Listener(on_press=on_press,on_release=on_release) as listener:
        listener.join()

def main():
    global msg,goOn
    t = Thread(target=listen)
    t.setDaemon = True
    t.start()
    menu = '''
\n[-] SELECT YOUR CHOICE
1) ADD A SHORTCUT
2) LIST ALL SHORTCUTS
3) DELETE A SHORTCUT
4) EDIT A SHORTCUT
5) QUIT

'''
    while 1:
        print('\r'*100)
        choice = int(input(menu))
        if choice not in (1,2,3,4,5):
            print('[-] INVALID')
            continue
        elif choice == 5:
            break
        elif choice == 2:
            print_keys()
        elif choice == 4:
            tot = print_keys()
            selected_key = int(input('[-] SELECT KEY TO EDIT '))
            if selected_key > tot:
                print('[-] INVALID')
                continue
            else:
                edit_shortcut(selected_key)
            while 1:
                if not goOn:
                    goOn = 1
                    break
        elif choice == 3:
            tot = print_keys()
            selected_key = int(input('[-] SELECT KEY TO DELETE '))
            if selected_key > tot:
                print('[-] INVALID')
                continue
            else:
                del_shortcut(selected_key)
        elif choice == 1:
            msg = input('[-] ENTER MESSAGE TO MAP TO SHORTCUT(COPY AND PASTE YOUR DESIRED EMOJI TO SEND EMOJIS) ')
            print('[-] PRESS YOUR DESIRED SHORTCUT KEYS (MAKE SURE THEY DIFFER FROM GLOBAL SHORTCUTS)')
            while 1:
                if not goOn:
                    goOn = 1
                    break

if __name__ == "__main__" and name in ("nt","posix"):
    main()
    if name != 'nt':#scrap all threads
        system('killall Python > /dev/null 2>&1')
    else:#scrap all threads
        system('taskkill /F /IM python.exe /T')