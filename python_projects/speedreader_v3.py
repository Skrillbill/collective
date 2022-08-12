'''

Speed Reader 9000
word flashamatron thing
words go brrrr

version 1.0
'using events to pause/start/kill threads on windows:
https://stackoverflow.com/questions/3262346/pausing-a-thread-using-threading-class

TODO:
    - add a darkmode, either as an option or jsut make it the default


10/28:
changed input box to scrolled text
'''



from tkinter import *
from tkinter import ttk
import tkinter.scrolledtext as scrolledtext
from time import sleep
import threading 
from pynput import keyboard

event_Reader_Enable = threading.Event()
event_Reset = threading.Event()

class Window(Frame):
    '''Class for settig up and handling the tKinter gui, keyboard event handling, and thread start/termination '''
    def __init__(self,master=None):
        Frame.__init__(self,master)
        self.master=master
        self.master.option_add('*tearoff',False)
        self.init_window()

    def init_window(self):

        self.master.title("Speed Reader 9000")

        #create the master menu object
        menucontainer = Menu(self.master)
        root.config(menu=menucontainer)

        #File Menu
        file_MenuContainer = Menu(menucontainer)
        menucontainer.add_cascade(label="File", menu=file_MenuContainer)
        file_MenuContainer.add_command(label="Quit", command = lambda: exit())


        
        #text input box
        label_ReaderInput = Label(root,text="Reader Input",padx=10,pady=10)
        self.text_ReaderInput = scrolledtext.ScrolledText(root,height=30,width=50)
        #self.text_ReaderInput = Text(root,height=30,width=50)
        self.text_ReaderInput.grid(row=2,column=0,columnspan=1, padx=5, sticky=E+W+N+S)
        label_ReaderInput.grid(row=1,column=0,columnspan=3)

        #text output box
        label_ReaderOutput = Label(root,text="ISAMSPEED",padx=10,pady=10)
        self.text_ReaderOutput = Label(root,text="defaulttext", height=10,width=50,font=('Arial',12),relief=SUNKEN)
        self.text_ReaderOutput.grid(row=2,column=4,columnspan=1,padx=5,sticky=E+W+N+S)
        label_ReaderOutput.grid(row=1,column=4,columnspan=3)


        #speed selector/label
        frame_Speed = Frame(root)
        frame_Speed.grid(row=3, column=4)
        label_Speed = Label(frame_Speed,text="Delay:",width=4,padx=2)
        label_Speed.grid(row=0,column=0)
        self.text_Speed = Text(frame_Speed,height=1,width=8)
        self.text_Speed.insert(INSERT, "250")
        self.text_Speed.grid(row=0,column=3)
     
        #i am spedestrian button
        '''TODO: Add a label frame here; pack the start and reset buttons inside of it'''
        button_Container = Frame(root)
        button_Container.grid(row=3,column=0,columnspan=2)
        button_BeginRead = Button(button_Container, height=2,width=15, text="Begin Read", command = lambda: self.t_worker()) #self.word_Flasher_t(text_ReaderInput,text_ReaderOutput,text_Speed
        button_BeginRead.grid(row=3,column=0, columnspan = 2, padx=1,pady=3, sticky=E+W+N+S)

        button_Reset = Button(button_Container, height=2,width=15, text="Reset", command = lambda: self.reset()) #self.word_Flasher_t(text_ReaderInput,text_ReaderOutput,text_Speed
        button_Reset.grid(row=3,column=3, columnspan = 2, padx=1,pady=3, sticky=E+W+N+S)

    def word_Flasher_t(self,textBox,target_Label,speed):
        ''' This function will iterate thru all text in text_ReaderInput and display it as a label to text_ReaderOutput, one word at a time '''
        #clear the reset event each time the function is called. otherwise the function basically auto returns
        event_Reset.clear() 
        textValue = textBox.get("1.0","end-1c")
        wordlist = textValue.split(" ")
        speed= int(speed.get("1.0","end-1c"))

        lastidx = '1.0'
        for word in wordlist:
            IS_ENABLED = event_Reader_Enable.wait()
            
            highlight_Word = self.text_ReaderInput.search(word,lastidx,nocase=1,stopindex=END)
            lastidx = '%s+%dc' % (highlight_Word, len(word))
            
            self.text_ReaderInput.tag_add('high', highlight_Word, lastidx)
            self.text_ReaderInput.tag_config('high',background='yellow')
            #self.text_ReaderInput.see(lastidx)
            
            target_Label.config(text=word)
            root.update()
            sleep(speed / 1000)
            self.text_ReaderInput.tag_remove('high','1.0', END)
            
            if event_Reset.is_set(): #check if the reset trigger was pulled, and return out of the function, killing the thread

                return

    def t_worker(self):
        '''GUI button calls this, which fires off the thread for the word reader '''
        global event_Reader_Enable
        worker = threading.Thread(name='t_worker',target=self.word_Flasher_t, args=(self.text_ReaderInput,self.text_ReaderOutput,self.text_Speed))
        worker.start()
        event_Reader_Enable.set()

    def keyboard_listener(key):
        '''keyboard_listener(key): background thread for handling keyboard inputs. No parameters are required
        derived from the pynput module and this thread: https://stackoverflow.com/questions/11918999/key-listeners-in-python
        '''
        global event_Reader_Enable
        global event_Reset
        if key == keyboard.Key.esc:
            return False #stop the keyboard listener
        try:
            k = key.char
        except:
            k = key.name
        if k in ['a']:
            event_Reader_Enable.set()
        if k in ['s']:
            event_Reader_Enable.clear()
        if k in ['k']:          
            event_Reset.set()

    def reset(self):
        event_Reader_Enable.clear()
        event_Reset.set()
        self.text_ReaderInput.delete('1.0',END)


             

    kb_listener = keyboard.Listener(on_press=keyboard_listener)
    kb_listener.start()



root=Tk()
root.geometry("900x600")
app = Window(root)
root.mainloop()
