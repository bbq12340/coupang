import tkinter as tk
from tkinter import filedialog
from tkinter.ttk import Progressbar
from scrapeItems import ItemScraper
import time

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.delay_time = tk.DoubleVar()
        self.min = tk.IntVar()
        self.max = tk.IntVar()
        self.create_widgets()
        

    def create_widgets(self):
        #Label
        self.filename_label = tk.Label(self, text="")
        self.filename_label.grid(row=0, column=1)

        self.request_label = tk.Label(self, text='요청 파일명:')
        self.request_label.grid(row=0, column=0)

        self.delay_time_label = tk.Label(self, text="딜레이 (초)")
        self.delay_time_label.grid(row=1, column=0)

        self.range_label = tk.Label(self, text="페이지 범위")
        self.range_label.grid(row=2, column=0)

        #Entry
        self.delay_time_entry = tk.Entry(self, width=7, textvariable=self.delay_time)
        self.delay_time_entry.grid(row=1, column=1)

        self.min_entry = tk.Entry(self, width=3, textvariable=self.min)
        self.min_entry.grid(row=2, column=1, sticky=tk.W)

        self.max_entry = tk.Entry(self, width=3, textvariable=self.max)
        self.max_entry.grid(row=2, column=1, sticky=tk.E)

        #ProgressBar
        self.progress = Progressbar(self,orient=tk.HORIZONTAL,length=150)
        self.progress.grid(row=3,column=0,columnspan=2,pady=5)
        
        #Button
        self.search_btn = tk.Button(self, text='파일 탐색', command=self.add_file)
        self.search_btn.grid(row=4, column=0, pady=5)

        self.start_btn = tk.Button(self, text="시작", command=self.start)
        self.start_btn.grid(row=4, column=1, pady=5)
    
    def add_file(self):
        filename = filedialog.askopenfilename(initialdir='./list', title='파일 탐색', filetypes=[("text files", "*.txt")])
        self.filename_label.config(text=f"{filename.split('/')[-1]}")
        self.FILENAME = filename

    def start(self):
        app = ItemScraper()
        with open(self.FILENAME, 'r') as f:
            request_list = f.readlines()
        for q in request_list:
            q = q.replace('\n','')
            for p in range(self.min.get(), self.max.get()+1):
                links=app.query(q, p)
                time.sleep(self.delay_time.get())
                print(links)
        return
    

root = tk.Tk()
root.title('쿠팡 크롤러')
root.geometry('250x150')
app = Application(master=root)
app.mainloop()