import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
from scrapeItems import CoupangScraper
from threading import Thread, Event
import pandas as pd
import time

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.thread = None
        self.stop_thread = Event()
        self.output = tk.StringVar()
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

        self.output_label = tk.Label(self, text="결과 파일명:")
        self.output_label.grid(row=1, column=0)

        self.delay_time_label = tk.Label(self, text="딜레이 (초)")
        self.delay_time_label.grid(row=2, column=0)

        self.range_label = tk.Label(self, text="페이지 범위")
        self.range_label.grid(row=3, column=0)

        self.progress_label = tk.Label(self, text="")
        self.progress_label.grid(row=4, column=0)

        #Entry
        self.output_entry = tk.Entry(self, width=7, textvariable=self.output)
        self.output_entry.grid(row=1, column=1)

        self.delay_time_entry = tk.Entry(self, width=7, textvariable=self.delay_time)
        self.delay_time_entry.grid(row=2, column=1)

        self.min_entry = tk.Entry(self, width=3, textvariable=self.min)
        self.min_entry.grid(row=3, column=1, sticky=tk.W)

        self.max_entry = tk.Entry(self, width=3, textvariable=self.max)
        self.max_entry.grid(row=3, column=1, sticky=tk.E)

        #ProgressBar
        self.progress = Progressbar(self,orient=tk.HORIZONTAL, length=100)
        self.progress.grid(row=4,column=1,columnspan=2, pady=5)
        
        #Button
        self.search_btn = tk.Button(self, text='파일 탐색', command=self.add_file)
        self.search_btn.grid(row=5, column=0, pady=5)

        self.start_btn = tk.Button(self, text="시작", command=self.start)
        self.start_btn.grid(row=5, column=1, pady=5, sticky=tk.E)

        # self.end_btn = tk.Button(self, text="중지", command=self.stop)
        # self.end_btn.grid(row=5, column=1, pady=5, sticky=tk.E)
    
    def add_file(self):
        filename = filedialog.askopenfilename(initialdir='./list', title='파일 탐색', filetypes=[("text files", "*.txt")])
        self.filename_label.config(text=f"{filename.split('/')[-1]}")
        self.FILENAME = filename
    
    def start(self):
        self.stop_thread.clear()
        self.thread = Thread(target=self.scraping)
        self.thread.start()

    # def stop(self):
    #     self.stop_thread.set()
    #     self.thread.join()
    #     self.thread = None
    #     messagebox.showinfo("info", message="프로그램을 종료하였습니다.")
    #     self.progress["value"] = 0
    #     self.master.update_idletasks()
    
    def scraping(self):
        app = CoupangScraper()
        with open(self.FILENAME, 'r') as f:
            request_list = f.readlines()
        for q in request_list:
            if self.stop_thread.is_set():
                break
            self.progress["value"] = 0
            self.progress_label.config(text=f"{request_list.index(q)+1}/{len(request_list)}")
            q = q.replace('\n','')
            for p in range(self.min.get(), self.max.get()+1):
                links=app.query(q, p)
                if links==None:
                    break
                for l in links:
                    self.seller_scrape(app, q, l)
                self.progress["value"] += 100/(self.max.get()-self.min.get()+1)
                self.master.update_idletasks()
                time.sleep(self.delay_time.get())
            # self.progress["value"] += 100/len(request_list)
            # self.master.update_idletasks()
        self.progress["value"] = 0
        messagebox.showinfo("Info", message="크롤링 완료!")
        return
    
    def seller_scrape(self, app, q, link):
        c1 = link.split('?')[0].split('/')[-1]
        c2 = link.split('itemId=')[-1].split('&')[0]
        c3 = link.split('vendorItemId=')[-1].split('&')[0]
        df = app.scrape_seller(q, c1, c2, c3)
        df.to_csv(f"{self.output.get()}.csv", mode="a", index=False, encoding='utf-8-sig', header=False)
        return
    

root = tk.Tk()
root.title('쿠팡 크롤러')
root.geometry('250x200')
app = Application(master=root)
app.mainloop()
