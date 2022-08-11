from fdb import services
import fdb
import os
from pathlib import Path
from tkinter import Frame, Button , Tk , messagebox, Menu,scrolledtext,filedialog,simpledialog
from tkinter import *
import time
import threading
import random
import queue as Queue


class tkgui:
    def __init__(self,master,queue,endCommand):
        self.queue = queue
        self.db_tools = db_tools()
        #initiate the tk() gui
        self.master = master
        self.master.title("Database Maintenance Utility")
        self.master.geometry("600x600")
        #Create the master menu object
        mastermenu = Menu(self.master) 
        root.config(menu=mastermenu)
        
        #runtime output box
        consoleFrame = LabelFrame(self.master,text="Console Output",padx=5,pady=5)
        consoleFrame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky=E+W+N+S)
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(1, weight=1)
        consoleFrame.rowconfigure(0, weight=1)
        consoleFrame.columnconfigure(0, weight=1)
        global txtbox
        txtbox = scrolledtext.ScrolledText(consoleFrame, width=40, height=10,bg="Black",fg="Yellow")
        txtbox.grid(row=0, column=0, sticky=E+W+N+S)
        global progVar
        progVar = StringVar()
        progVar.set("No Task")
        progressLabel = Label(self.master,textvariable=progVar)
        progressLabel.grid(row=2,sticky=W)

#File
        filemenu = Menu(mastermenu)
        mastermenu.add_cascade(label="File",menu=filemenu)
        filemenu.add_command(label="Quit",command = lambda: root.destroy())
        filemenu.add_command(label="Test Function")
        
        
#Database
        dbmenu = Menu(mastermenu)
        mastermenu.add_cascade(label="Database",underline=0,menu=dbmenu)
        dbmenu.add_command(label="Masterkey..",command= lambda: print("Masterkey undef"))
            #Database -> Open
        subopen = Menu(filemenu)
        subopen.add_command(label="Database",command=print("undef"))
        subopen.add_command(label="SQL Editor",command=print("undef"))       
        dbmenu.add_cascade(label="Open",menu=subopen)
        dbmenu.add_cascade(label="Backup",command= lambda: self.db_tools.bakup())
        dbmenu.add_cascade(label="Repair/Validate",command= lambda: self.db_tools.gfix())
        dbmenu.add_cascade(label="It's a Me, Marito",command= lambda: self.bakupOptions())
            #Database -> Restore
        dbmenu.add_command(label="Restore", command=lambda: self.db_tools.restore())

    def bakupOptions(self):
        self.bakOpts = Toplevel(self.master)
        self.bakOpts.title("")
        self.bakOpts.geometry("300x150")
        self.optsLabel = Label(self.bakOpts,text="Backup options")
        self.optsLabel.grid()

        global c_sgbcValue
        c_sgbcValue = BooleanVar()
        self.c_sgbc = Checkbutton(self.bakOpts,text="Skip Garbage Collection",var=c_sgbcValue)
        self.c_sgbc.grid(row=1,sticky='w')

        c_cmprsValue = BooleanVar()
        c_cmprs = Checkbutton(self.bakOpts,text="Compressed",var=c_cmprsValue)
        c_cmprs.grid(row=2,sticky='w')


        c_ichksmValue = BooleanVar()
        c_ichksm = Checkbutton(self.bakOpts,text="Ignore Checksums",var=c_ichksmValue)
        c_ichksm.grid(row=3,sticky='w')

        b_stbak = Button(self.bakOpts,text="Go",command= lambda: self.db_tools.threaded_bak())
        b_stbak.grid(row=5,column=2)


    def processIncoming(self):
        #this will handle the 'message' queue.
        while self.queue.qsize():
            try:
                msg = self.queue.get(0)
                #Check contents of message and do whatever.
                #for testing, we'll just print
                print(msg)
            except Queue.Empty:
                #only added for necessity, i don't expect this to happen
                pass


class ThreadedClient:
    #I think this is the main thread of the gui.

    def __init__(self,master):
        self.master = master

        #we create a new async thread in this, the main thread, for the gui
        #as well as the worker

        #create the queue
        self.queue = Queue.Queue()
        self.gui = tkgui(master,self.queue,self.endApplication)

        #setup thread to do async io
        self.running = 1
        self.thread1 = threading.Thread(target=self.WorkerThread1)
        self.thread1.start()
    
        self.periodicCall()

    def periodicCall(self):
        #check queue every 200ms for new messages
        self.gui.processIncoming()
        if not self.running:
            sys.exit(1)
        self.master.after(200,self.periodicCall)


    def WorkerThread1(self):
        #this is where we handle the async i/o.
        while self.running:
            time.sleep(rand.random()*1.5)
            msg = rand.random()
            self.queue.put(msg)

    def endApplication(self):
        self.running = 0


class db_tools:
    fb_db_source = 'C:\\Daterbases\\test\\test.fdb'
    fb_db_bak = 'C:\\Daterbases\\test\\test.fbk'
    fb_db_rest = 'C:\\Daterbases\\test\\test_rest.fdb'

    def progressBar(self):
        z = self.t1.is_alive()
        if(z):
            progVar.set("Task is active...")
            
    def threaded_bak(self):
        self.t1 = threading.Thread(target=self.bakup,args=())
        self.progressBar()
        self.t1.start()
        

    def bakup(self):
        print("this was called")
        try:
            con.backup(self.fb_db_source,self.fb_db_bak, collect_garbage=c_sgbcValue.get())
            for line in con:
                txtbox.insert(END,(line))
                txtbox.insert(END,("\n"))
                txtbox.update()
                txtbox.yview(END)
        except:
            e = sys.exc_info()[0]
            txtbox.insert(END,e)
            txtbox.insert(END,("\n"))
            txtbox.update()
            txtbox.yview(END)
            print("!ERROR! # %s" % e)


    def gfix(self):
        con.repair(self.fb_db_source,ignore_checksums=True,read_onely_validation=True)
        con.wait()
        print(con.isrunning())
        print(report)

    def restore(self):
        try:
            con.restore(self.fb_db_bak, self.fb_db_rest, commit_after_each_table=True)
            for line in con:
                txtbox.insert(END,(line))
                txtbox.insert(END,("\n"))
                txtbox.update()
                txtbox.yview(END)
        except:
            e = sys.exc_info()[1]
            txtbox.insert(END,e)
            txtbox.insert(END,("\n"))
            txtbox.update()
            txtbox.yview(END)
            print("!ERROR! # %s" % e)

    def gfix(self):
        con.repair(self.fb_db_source,ignore_checksums=True,read_only_validation=True)
        con.wait()
        print(con.isrunning())
        print(report)

#services.connect() - from the fdb module
#con = services.connect(host='localhost',user='sysdba',password="masterkey")
con = fdb.connect(dsn='C:\path\to\db\fdb.fdb',user='sysdba',password='masterkey')
rand = random.Random()
root = Tk()

testvar = con.db_info(fdb.isc_info_db_id)
print(testvar)
fdb.isc_dpb_garbage_collect

client = ThreadedClient(root)
root.mainloop()
#con.__del__ #closes con
#print(con.closed)










        
