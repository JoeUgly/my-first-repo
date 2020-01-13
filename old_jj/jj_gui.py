# Description: GUI for Jorbs

# To do:
# help button
# context menu
# make functional
# make pretty -
# fully abs +
# back and shift return bug +
# delay next button +


import datetime, os, queue, re, socket, time, urllib.parse, urllib.request, webbrowser
from multiprocessing import active_children, Lock, Manager, Process, Queue, Value
from math import sin, cos, sqrt, atan2, radians
from http.cookiejar import CookieJar
import tkinter as tk
from tkinter import *


LARGE_FONT = ("Courier bold", 14)
SMALL_FONT = ("Courier bold", 12)
title_y = 40
desc_y = 100
entry_y = 160
err_y = 200


class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title('Joe\'s Jorbs')

        # Set geometry and postion
        w = 600
        h = 450
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = (ws/2) - (w/2)
        y = (hs/4) - (h/4)
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
         
        # This container contains all the pages
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)   # make the cell in grid cover the entire window
        container.grid_columnconfigure(0,weight=1) # make the cell in grid cover the entire window
        self.frames = {} # these are pages we want to navigate to
 
        # Each page
        for F in (StartPage, job_page, zip_page, dist_page, adv_page, search_page):
            frame = F(container, self) # create the page
            self.frames[F] = frame  # store into frames
            frame.grid(row=0, column=0, sticky="nsew") # grid it to container

        # Show first page
        self.show_frame(StartPage)
 
    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()


# Start page
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        #self.config(bg='gray25')

        # Page label and desc
        title_label = tk.Label(self, text='Joe\'s Jorbs')
        title_label.config(font=("Courier bold", 24))
        title_label.place(relx=0.5, y=30, anchor=CENTER)
        desc_label = tk.Label(self, text='Find jobs in New York State', font=LARGE_FONT)
        desc_label.place(relx=0.5, y=70, anchor=CENTER)

        # Message
        cb_pos = 150
        messageVar = Message(self, text = 'Select at least one to search', font=(LARGE_FONT), width=380) 
        messageVar.place(relx=0.5, y=cb_pos, anchor=CENTER)

        # Set checkbutton type
        c1=tk.BooleanVar()
        c2=tk.BooleanVar()
        c3=tk.BooleanVar()

        # Create and place left checkbuttons
        tk.Checkbutton(self,text='Civil Service', font=LARGE_FONT, variable=c1).place(relx=0.5, y=cb_pos+30, anchor=CENTER)
        tk.Checkbutton(self,text='Schools       ', font=LARGE_FONT, variable=c2).place(relx=0.5, y=cb_pos+60, anchor=CENTER)
        tk.Checkbutton(self,text='Universities ', font=LARGE_FONT, variable=c3).place(relx=0.5, y=cb_pos+90, anchor=CENTER)

        # Advanced options page button
        nextButton = Button(self, text="Advanced options", command=lambda : controller.show_frame(adv_page), font=SMALL_FONT)
        nextButton.place(x=50,y=320)

        # Next button
        def next():
                
            # Show next page if mandatory arg is met
            if c1.get() or c2.get() or c3.get():
                controller.show_frame(job_page)
                controller.bind('<Return>', enter2)
                controller.bind('<Shift-Return>', enter22)
                job_entry.focus()
                
                # Append checkbutton values to list
                for c in (c1,c2,c3):
                    checks.append(c.get())

                # Clear error message
                err_label = Message(self, text = '\t\t\t\t\t\t\t\t\t', width=180) 
                err_label.place(x=200, y=260)

            # Display error if missing mandatory arg
            else:
                err_label = Message(self, text = 'Error. You must select at least one option.', font=SMALL_FONT, width=180) 
                err_label.config(bg='pink') 
                err_label.place(x=200, y=260)

        # Bind enter key to Next
        global enter1
        def enter1(event=None):
            next()
        controller.bind('<Return>', enter1)
            
        nextButton = Button(self, text="Next", command=next, font=SMALL_FONT)
        nextButton.place(x=440, y=320)


# Job title page
class job_page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Page label
        label = tk.Label(self, text='\nEnter jobs to search for\n', font=LARGE_FONT)
        label.place(relx=0.5, y=title_y, anchor=CENTER)
        
        # Append job titles to list
        def comp():
            global j_count
            try: j_count += 1
            except: j_count = 1
            if len(job_entry.get()) > 0:
                keyword_list.append(job_entry.get())
                job_entry.delete(0, 'end')

                # Clear error message
                err_label = Label(self, text="\t\t\t\t\t\t\t", font=SMALL_FONT)
                err_label.place(relx=0.5, y=200, anchor=CENTER)

                # Display list
                job_label = Label(self, text="Using job titles: " + str(keyword_list[:j_count])[1:-1], font=SMALL_FONT)
                job_label.place(relx=0.5, y=200, anchor=CENTER)

        # Bind enter key to Comp
        global enter2
        def enter2(event=None):
            comp()

        global enter22
        def enter22(event=None):
            next()

        jjob_label = Label(self, text='Type a job title and click Accept.\nYou can enter multiple job titles.\n', font=SMALL_FONT)
        jjob_label.place(relx=0.5, y=desc_y, anchor=CENTER)

        # Accept and next
        def next():
            comp()

            # Display empty keyword error
            if len(keyword_list) < 1:
                err_label = Label(self, text="Error. You must enter at least one job title.", font=SMALL_FONT)
                err_label.config(bg='pink')
                err_label.place(relx=0.5, y=200, anchor=CENTER)

            # Clear error
            else:
                err_label = Label(self, text="\t\t\t\t\t\t\t", font=SMALL_FONT)
                err_label.place(relx=0.5, y=200, anchor=CENTER)

                # Next page
                job_label = Label(self, text="Using job titles: " + str(keyword_list[:j_count])[1:-1], font=SMALL_FONT)
                job_label.place(relx=0.5, y=200, anchor=CENTER)
                controller.show_frame(zip_page)
                controller.bind('<Return>', enter3)
                #controller.bind('<Shift-Return>', enter3)                
                zip_entry.focus()
                global startTime1
                startTime1 = datetime.datetime.now()                

        # Job title entries       
        L1 = Label(self, text="Job title: ", font=SMALL_FONT)
        L1.place(relx=0.28, y=160, anchor=CENTER)
        L_ex = Label(self, text=" Example: librarian", font=SMALL_FONT)
        L_ex.place(relx=0.78, y=160, anchor=CENTER)
        global job_entry
        job_entry = Entry(self, bd =4, font=SMALL_FONT)
        job_entry.place(relx=0.5, y=160, anchor=CENTER)
                
        # Filler for list
        job_label = Label(self, text='')
        job_label.place(relx=0.5, y=200, anchor=CENTER)

        # Back button
        def back_page():
            
            checks.clear() # Clear list to prevent too many values
            controller.show_frame(StartPage) # Show previous page
            controller.bind('<Return>', enter1)
            controller.bind('<Shift-Return>', enter1)

        # Create back button and place ## can be one line
        backButton = Button(self, text="Back", command=back_page, font=SMALL_FONT)
        backButton.place(x=80, y=240)

        # Next button
        nextButton = Button(self, text="Next", command=next, font=SMALL_FONT)
        nextButton.place(x=440, y=240)

        # Accept button
        acc_Button = Button(self, text="Accept", command=comp, font=SMALL_FONT)
        acc_Button.place(x=310, y=240)


# ZIP code page
class zip_page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Page label
        label1 = tk.Label(self, text='\nEnter your ZIP code\n', font=LARGE_FONT)
        label1.place(relx=0.5, y=title_y, anchor=CENTER)
        label2 = tk.Label(self, text='This will be used to search only the job postings near you. \n Leave blank to search all of NYS.\n', font=SMALL_FONT)
        label2.place(relx=0.5, y=desc_y, anchor=CENTER)           
        
        # Next page
        def next():

            # Ignore if less than .5 seconds to prevent accidental double clicks
            duration = datetime.datetime.now() - startTime1
            if duration.seconds < 1:
                if duration.microseconds < 500000: return

            # Declare ZIP
            global home_resp
            home_resp = zip_entry.get()

            # Test ZIP
            if len(home_resp) > 0:
                try:
                    home_resp_i = int(home_resp)

                    '''
                    # Catch ZIP not found
                    if not home_resp_i in zip_dict:
                        err_label = Label(self, text="Error. Your input is not a known NYS ZIP code.", font=SMALL_FONT)
                        err_label.config(bg='pink')
                        err_label.place(relx=0.5, y=err_y, anchor=CENTER)
                    '''
                    # Clear error message
                    err_label = Label(self, text="\t\t\t\t\t\t\t", font=SMALL_FONT)
                    err_label.place(relx=0.5, y=err_y, anchor=CENTER)
                    
                    # Set ZIP and go to next page
                    z_label = Label(self, text="Using ZIP code: " + home_resp, font=SMALL_FONT)
                    z_label.place(relx=0.5, y=err_y, anchor=CENTER)
                    controller.show_frame(dist_page)
                    controller.bind('<Return>', enter4)
                    dist_entry.focus()
                    global startTime2
                    startTime2 = datetime.datetime.now()                

                # Catch non number input
                except:
                    err_label = Label(self, text="Error. Your input was not a number.", font=SMALL_FONT)
                    err_label.config(bg='pink')
                    err_label.place(relx=0.5, y=err_y, anchor=CENTER)
                    
            # Exit if ZIP is blank
            else:
                controller.destroy()
            
        # ZIP code entry      
        L1 = Label(self, text="ZIP code: ", font=SMALL_FONT)
        L1.place(relx=0.28, y=entry_y, anchor=CENTER)
        L_ex = Label(self, text=" Example: 14020", font=SMALL_FONT)
        L_ex.place(relx=0.77, y=entry_y, anchor=CENTER)
        global zip_entry
        zip_entry = Entry(self, bd =4, font=SMALL_FONT)
        zip_entry.place(relx=0.5, y=entry_y, anchor=CENTER)

        # Back button
        def back_page():
            controller.show_frame(job_page)
            controller.bind('<Return>', enter2)
            job_entry.focus()
            
        backButton = Button(self, text="Back", command=back_page, font=SMALL_FONT)
        backButton.place(x=80, y=240)

        # Bind enter key to Next
        global enter3
        def enter3(event=None):
            next()

        # Next button
        nextButton = Button(self, text="Accept and next", command=next, font=SMALL_FONT)
        nextButton.place(x=370, y=240)

        
# Distance page
class dist_page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Page label
        label = tk.Label(self, text='\nEnter the maximum distance (in miles) to search\n', font=LARGE_FONT)
        label.place(relx=0.5, y=title_y, anchor=CENTER)
        label2 = tk.Label(self, text='Leave blank to search all of NYS.\n\n', font=SMALL_FONT)
        label2.place(relx=0.5, y=desc_y, anchor=CENTER)            

        # Next page
        def next():

            # Ignore if less than .5 seconds to prevent accidental double clicks
            duration = datetime.datetime.now() - startTime2
            if duration.seconds < 1:
                if duration.microseconds < 500000: return

            # Declare max distance
            global max_dist
            max_dist = dist_entry.get()

            # Skip if blank
            if len(max_dist) > 0:

                # Test distance input
                try:
                    max_dist_i = int(max_dist)
                    controller.destroy()

                # Catch non number input
                except:
                    err_label = Label(self, text="Error. Your input was not a number.", font=SMALL_FONT)
                    err_label.config(bg='pink')
                    err_label.place(relx=0.5, y=err_y, anchor=CENTER)
            else:
                controller.destroy()
            
        # Distance entry      
        L1 = Label(self, text="Max distance: ", font=SMALL_FONT)
        L1.place(relx=0.25, y=entry_y, anchor=CENTER)
        L_ex = Label(self, text=" Example: 125", font=SMALL_FONT)
        L_ex.place(relx=0.75, y=entry_y, anchor=CENTER)
        global dist_entry        
        dist_entry = Entry(self, bd =4, font=SMALL_FONT)
        dist_entry.place(relx=0.5, y=entry_y, anchor=CENTER)

        # Back button
        def back_page():
            controller.show_frame(zip_page)
            controller.bind('<Return>', enter3)
            zip_entry.focus()

        backButton = Button(self, text="Back", command=back_page, font=SMALL_FONT)
        backButton.place(x=80, y=240)

        # Bind enter key to Next
        global enter4
        def enter4(event=None):
            next()

        # Next button
        nextButton = Button(self, text="Accept and Start", command=next, font=SMALL_FONT)
        nextButton.place(x=370, y=240)
        

# Advanced options page
class adv_page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Page label
        label = tk.Label(self, text='Advanced options', font=LARGE_FONT)
        label.place(relx=0.5, y=title_y, anchor=CENTER)

        # Entry labels
        procs_lab = Label(self, text="Number of processes:", font=SMALL_FONT)
        procs_lab.place(relx=0.2, y=250, anchor=CENTER)
        crawl_lab = Label(self, text="Max crawl depth:  ", font=SMALL_FONT)
        crawl_lab.place(relx=0.24, y=280, anchor=CENTER)

        # Vars for checkbuttons
        c4=tk.BooleanVar()
        c5=tk.BooleanVar()
        c6=tk.BooleanVar()

        # Declare checkbuttons, processes, and crawl level 
        def back():
            global num_procs
            global max_crawl_depth
            num_procs = procs_entry.get()
            max_crawl_depth = crawl_entry.get()
            global aa
            global ww
            global vv
            aa = c4.get()
            ww = c5.get()
            vv = c6.get()
            controller.show_frame(StartPage)

        # Create and place checkbuttons
        tk.Checkbutton(self,text='All links      ', font=LARGE_FONT, variable=c4).place(relx=0.5, y=120, anchor=CENTER)
        tk.Checkbutton(self,text='Write to file', font=LARGE_FONT, variable=c5).place(relx=0.5, y=155, anchor=CENTER)
        tk.Checkbutton(self,text='Verbose     ', font=LARGE_FONT, variable=c6).place(relx=0.5, y=190, anchor=CENTER)
        
        # Number of processes
        global procs_entry
        procs_entry = Entry(self, bd=4, font=SMALL_FONT)
        procs_entry.place(relx=0.5, y=250, anchor=CENTER)
        Label(self, text="Default: 32", font=SMALL_FONT).place(relx=0.75, y=250, anchor=CENTER)

        # Max crawl depth
        global crawl_entry
        crawl_entry = Entry(self, bd=4, font=SMALL_FONT)
        crawl_entry.place(relx=0.5, y=280, anchor=CENTER)
        Label(self, text="Default: 2 ", font=SMALL_FONT).place(relx=0.75, y=280, anchor=CENTER)

        # Back button
        backButton = Button(self, text="Back", command=back, font=SMALL_FONT)
        backButton.place(x=70,y=320)
        
        
# Searching page
class search_page(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Page label
        label = tk.Label(self, text='Now searching', font=LARGE_FONT)
        label.place(relx=0.5, y=title_y, anchor=CENTER)
        
        
        try:
            textt = str(prog_count.value, 'of')
        except:
            textt = 0
        tk.Label(self, text=textt, font=LARGE_FONT).place(relx=0.5, y=desc_y, anchor=CENTER)
        time.sleep(3)

        def des():
            controller.destroy()

        #  button
        backButton = Button(self, text="done", command=des, font=SMALL_FONT)
        backButton.place(x=70,y=320)

        

        
# Get objects
checks = [] 
keyword_list = []


if __name__ == '__main__':
    app = MainWindow()
    app.mainloop()


# Set default values
try: aa
except: aa = False
try: ww
except: ww = False
try: vv
except: vv = False
try: num_procs
except: num_procs = 32
try: max_crawl_depth
except: max_crawl_depth = 2
try: home_resp
except: home_resp = False
try: max_dist
except: max_dist = False


print('Civil Service = ', checks[0], '\nSchools =', checks[1], '\nUni =', checks[2], '\nLinks =', aa, '\nWrite =', ww, '\nVerbose =', vv)
print('keyword_list =', keyword_list, '\nhome_resp =', home_resp, '\nmax_dist =', max_dist, '\nnum_procs =', num_procs, '\nmax_crawl_depth =', max_crawl_depth)




















