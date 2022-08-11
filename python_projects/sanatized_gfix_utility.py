'''
sources used:
 https://www.endpoint.com/blog/2015/01/28/getting-realtime-output-using-python
 https://stackoverflow.com/questions/11284147/how-to-do-multiple-arguments-with-python-popen/11309864
'''

'''
+=========+
CHANGELOG

prior to april 2021: no changelog existed

04/23/21
Window.get_masterkey // Watchdog.w_chksumvld :: 
    changed the workflow of encrypting the masterkey user input. Now, it simply byte-encodes the input and runs that thru a base64 hash nbefore it checksums it.
    Unless the base64 aspect gets used for other purposes thruout, it maybe removed entirely and the masterkey will simply be encoded and then checksummed


+=========+
'''
VERSION_INFO = '1.5.3 Alpha'
VERSION_DATE = '4/23/2021'


import base64
import os
import hashlib
import subprocess
import logging
import time
import inspect
from tkinter import Frame, Button , Tk , messagebox, Menu,scrolledtext,filedialog,simpledialog
from tkinter import *
from subprocess import Popen,PIPE
from pathlib import Path # this is to get the file name from the path returned by tk-askopenfilename



# a91e55eeeba96c33feb82425b61ab0be43101fa9dcea45fdc05d4740cbea2fea -- this is the SYSDBA masterkey hash. md5

masterkeyhash = None #currently unused
activedb = None
#base64, because reasons
help_msg = 'UFJPR1JJTV9OQU1FIAoKCkZpcnN0IHlvdSBtdXN0IHNwZWNpZnkgdGhlIFNZU0RCQSBtYXN0ZXJrZXkuIApEYXRhYmFzZSAtPiBNYXN0ZXIgS2V5IAogCk5leHQsIHNlbGVjdCBhIGRhdGFiYXNlOiAgCkRhdGFiYXNlIC0+IE9wZW4gIA=='
gbak_running = False
#Replace this checksum with the password for you firebirds sysdba account. 
chksum = "3e8f9e2333ea510b3920cc4ad3319481" #default password

class Window(Frame):
    masterkey = None


    def __init__(self,master=None):
        Frame.__init__(self,master)
        self.master = master
        self.master.option_add('*tearOff',False)
        self.init_window()

        self.version="Alpha 1.0.0"

    def init_window(self):
        
            
        self.master.title("Database Maintenance Utility")

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
        
    #File
        filemenu = Menu(mastermenu)
        mastermenu.add_cascade(label="File",menu=filemenu)
        filemenu.add_command(label="Quit",command = lambda: root.destroy())
        filemenu.add_command(label="Test Function",command= lambda: self.test_func(txtbox))
        
        
    #Database
        dbmenu = Menu(mastermenu)
        mastermenu.add_cascade(label="Database",underline=0,menu=dbmenu)
        dbmenu.add_command(label="Masterkey..",command=self.get_masterkey)
            #Database -> Open
        subopen = Menu(filemenu)
        subopen.add_command(label="Database",command= self.menu_db_select)
        subopen.add_command(label="SQL Editor",command=lambda: self.gen_error(None,"function not defined"))       
        dbmenu.add_cascade(label="Open",menu=subopen)
            #Database -> Restore
        dbmenu.add_command(label="Restore", command=lambda: self.cb_restore())

    #Repair
        repairmenu = Menu(mastermenu)
        mastermenu.add_cascade(label="Repair",menu=repairmenu,underline=0)
        repairmenu.add_command(label="Validate",command= lambda: self.gen_error(None,"function not defined"))
        repairmenu.add_command(label="Mend",command=lambda: self.gen_error(None,"function not defined"))
        
    #Repair -> backup
        subrep = Menu(repairmenu)
        subrep.add_command(label="Collect Garbage",command=lambda: self.gen_error(None,"function not defined"))
        subrep.add_command(label="Skip Garbage Route",command= lambda: self.cb_bak())
        repairmenu.add_cascade(label="Backup",menu=subrep)
        
    #Helpmenu
        helpmenu = Menu(mastermenu)
        mastermenu.add_cascade(label="Help",menu=helpmenu)
        helpmenu.add_command(label="About",command=self.show_about)
        helpmenu.add_command(label="Show Help",command=self.show_help)

    def get_masterkey(self): #get the masterkey
        key = simpledialog.askstring("Firebird","Enter the SYSDBA Masterkey",parent=self.master,show="*")
        try:
            self.masterkey = base64.b64encode(key.encode()) #this converts to b64
        except:
            self.gen_error("MASTERKEY","Masterkey was not captured")
            wd.w_debug(" MASTERKEY not captured! ")
        
    def cb_bak(self):
        utils.bak_no_garbage(self,["none"])

    def cb_restore(self):
        utils.restore(self,activedb,txtbox)
       

    def menu_db_select(self):
        global activedb #use global here to set the activedb OUTSIDE of the function.
        global activepath
        fdb = filedialog.askopenfilename(initialdir="C:\/", title="Select Database", filetypes= (("Firebird Database (*.fdb)","*.fdb"),("Firebird Backup (*.fbk)","*.fbk"),("all files","*.*")))
        try:
            with open(fdb,'r') as usedb:
                activedb =  Path(usedb.name).name[:-4]
                activepath = fdb[:-len(activedb)-4]
                wd.w_debug("DEBUG: Currently selected DB %s" % (activedb))
                wd.w_console(None,activedb)
                wd.w_console(None,activepath)
                return
        except:
            self.gen_error("Invalid Selection","You select wrong or no file name.")
            wd.w_console(None,sys.exc_info()[0])
            
    def show_about(self):
        messagebox.showinfo("Information"," Firebird GFIX GUI. \n Build: %s" % (VERSION_INFO))

    def show_help(self):
        messagebox.showinfo("HELP!",base64.b64decode(help_msg).decode())

    def gen_error(self,title,msg): # gen_error(string title,string msg)
        if title == None:
            title="Generic Error"
        messagebox.showerror(title="%s" % title,message="%s" % msg)
        wd.w_debug("%s :: %s " % (inspect.stack()[1][3],msg ))

    def test_func(self,arg1):
        wd.w_debug("DEBUG: testion function activated")
        wd.w_debug("DEBUG: test_func arg1: %s " % type(arg1))

class utils: #this class has all of the heavy lifting code
    def __init__(self, func, *args, **kwargs): #am told this makes this class callable or something? can't source
        self.func = func
        self.args = args
        self.kwargs = kwargs
    def __call__(self):
        self.func(*self.args, **self.kwargs)


##BACKUP - SKIP GARBAGE COLLECTION
    def bak_no_garbage(self,cmd):
        
        if self.masterkey is None:
            self.gen_error("Undefined Masterkey","Masterkey is not defined. Database -> Masterkey")
            wd.w_debug(" MASTERKEY= %s. Exiting" % self.masterkey)
            return
        if wd.w_chksumvld(chksum,self.masterkey) == 0:
            wd.w_console(None,"Masterkey is wrong. Please retry")
            wd.w_debug("user supplied incorrect masterkey")
            return
        if activedb is None:
            self.gen_error("Database Error","There is no database selected. Database -> Open")
            wd.w_debug("No databse selected. Exiting")
            return
        
        command = ("gbak.exe -v -nt -e -g -user SYSDBA -pas %s C:\Sitewatch\DB\%s.fdb C:\Sitewatch\Backup\%s.fbk" % (base64.b64decode(self.masterkey).decode(), activedb, activedb))
        process = subprocess.Popen(command, stdout=subprocess.PIPE,shell=True)
        
        while True:
            output = process.stdout.readline().decode() #output is a byte array instad of a string. decode() to string to prevent hanging
            if output == '' and process.poll() is not None:
                #objTxtBox.config(state=DISABLED)
                txtbox.insert(END,"PROGRIM COMPLETE \n")
                txtbox.update()
                txtbox.yview(END)
                gbak_running = False
                break
            if output:
                txtbox.insert(END,(output))   
                txtbox.update()
                txtbox.yview(END)
                gbak_running = True
        rc = process.poll()
        return rc
    
##RESTORE
    def restore(self,bak_db,objTxtBox):

        if self.masterkey is None:
            self.gen_error("Undefined Masterkey","Masterkey is not defined. Database -> Masterkey")
            wd.w_debug(" MASTERKEY= %s. Exiting" % self.masterkey)
            return
        if wd.w_chksumvld(chksum,self.masterkey) == 0:
            wd.w_console(None,"Masterkey is wrong. Please retry")
            wd.w_debug("user supplied incorrect masterkey")
            return
        if activedb is None:
            self.gen_error("Database Error","There is no database selected. Database -> Open")
            wd.w_debug("No databse selected. Exiting")
            return
        
        command = ("gbak.exe -v -c -user SYSDBA -pas %s C:\Sitewatch\Backup\%s.fbk C:\Sitewatch\DB\%s_restore.fdb" % (base64.b64decode(self.masterkey).decode(),activedb,activedb))
        wd.w_console(None,command)
        process = subprocess.Popen(command, stdout=subprocess.PIPE,shell=True)
        
        while True:
            output = process.stdout.readline().decode() 
            if output == '' and process.poll() is not None:
                objTxtBox.insert(END,"RESTORE COMPLETE")
                objTxtBox.update()
                objTxtBox.config(state=DISABLED)
                break
            if output:
                objTxtBox.insert(END,(output))   
                objTxtBox.update()
                objTxtBox.yview(END)
        rc = process.poll()
        return rc
    
##VALIDATE                
    def validate(self,options,objTxtBox):
        command = ("gbak.exe -user SYSDBA -pas %s" % self.masterkey )
        process = subprocess.Popen(command, stdout=subprocess.PIPE,shell=True)
        if self.masterkey is None:
            self.gen_error("Undefined Masterkey","Masterkey is not defined. Database -> Masterkey")
            return
        while True:
            output = process.stdout.readline().decode() 
            if output == '' and process.poll() is not None:
                objTxtBox.insert(END,"BACKUP COMPLETE")
                objTxtBox.update()
                objTxtBox.config(state=DISABLED)
                break
            if output:
                objTxtBox.insert(END,(output))   
                objTxtBox.update()
                objTxtBox.yview(END)
        rc = process.poll()
        return rc  


class Watchdog:
    wd_message_types = {
            1: "Debug",
            2: "Info",
            3: "Warning"
            }
    def __init__(self):
        #logging configuration
        fname="debug_.log"
        logging.basicConfig(filename=fname,level=logging.DEBUG)
        logging.info('LOG INITIALIZED')
        logging.info('%s' % time.asctime())
  
    def w_debug(self,msg):        
        dbg_last_call = hex(id(inspect.stack()[1][3])) #this only prints the memory address of whatever called w_debug, not very useful but it looks cool
        buf = " CALL_STACK(%s) %s :: %s" % (dbg_last_call,inspect.stack()[1][3],msg)
        logging.debug(buf)

    def w_console(self,w_type,w_msg):
        txtbox.insert(END,(w_msg))
        txtbox.insert(END,("\n"))
        txtbox.update()
        txtbox.yview(END)
        #print(w_msg)

    def w_chksumvld(self,w_chksum,w_masterkey):
        md5 = hashlib.md5()
        #md5.update(w_masterkey)
        try:
            md5.update(w_masterkey) #decode base64 string has to be unicoded for the md5 digest to work. 
        except:
            wd.w_console(None,sys.exc_info()[0])              
        if w_chksum == md5.hexdigest():
            return 1
        else:
            return 0
        

root = Tk() #initialize the progrim
root.geometry("900x300")
wd = Watchdog()
app = Window(root)
root.mainloop()

