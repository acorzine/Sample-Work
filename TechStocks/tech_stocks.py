# William Corzine
# tech_stocks.py

import wx
import sqlite3 as db
import requests
import datetime

x = datetime.datetime.now() # date and time
date = x.strftime("%A %B %d, %Y : %H:%M") # Formatted date and time

class DataList(wx.Frame): # Data Frames
    def __init__ (self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(600, 450))
        panel = wx.Panel(self, -1)

        self.table_name = wx.StaticText(panel, -1, "Stock Difference Analyzer", pos=(235, 2))
        self.date = wx.StaticText(panel, -1, "Today's Date", pos=(235, 20))
        self.gain_loss = wx.StaticText(panel, -1, "Total", pos=(235, 40))
        self.list = wx.ListCtrl(panel, -1, style = wx.LC_REPORT, pos=(20, 70), size=(550, 220))

        # Columns
        self.list.InsertColumn(0, "Company Name", width=120)
        self.list.InsertColumn(1, "Symbol", width=70)
        self.list.InsertColumn(2, "Purchase Price", width=100)
        self.list.InsertColumn(3, "Current Price", width=100)
        self.list.InsertColumn(4, "Shares", width=70)
        self.list.InsertColumn(5, "Gain/Loss", width=70)
        

        # Buttons
        display = wx.Button(panel, -1, "Display", size=(-1, 35), pos=(180, 310))
        cancel = wx.Button(panel, -1, "Cancel", size=(-1, 35), pos=(320, 310))

        # Binding Buttons
        display.Bind(wx.EVT_BUTTON, self.OnDisplay )
        cancel.Bind(wx.EVT_BUTTON, self.OnCancel)

        self.Centre()

    def getAllData(self): # Pull Data from Database

        self.list.DeleteAllItems()
        con = db.connect("tech_stocks.db")
        cur = con.cursor()

        cur.execute("SELECT * FROM dow_stocks")
        rows = cur.fetchall()
        overallGainLoss = float()
        for r in rows:
            tok = "cnuusb1r01qub9j02ul0cnuusb1r01qub9j02ulg"
            url = 'https://finnhub.io/api/v1/quote?symbol='+ r[3] +'&token=' + tok
            response = requests.get(url)
            apiData = response.json()
            stockGainLoss = (apiData["c"] -  r[5]) * r[4]
            overallGainLoss += stockGainLoss
            stockGainLoss = (f"{stockGainLoss:.2f}")
            self.list.Append((r[1], r[3], r[5], apiData["c"], r[4], stockGainLoss))
        
        self.gain_loss.SetLabel(f"Net gain/loss: ${overallGainLoss:.2f}") # Displays Total Gains/Loss at top
    
        cur.close()
        con.close()

    def OnDisplay(self, event): # Display Data from Database
        self.getAllData()
        self.date.SetLabel(date) # Changes Date
        
    def OnCancel(self, event): # Close Program
        self.Close()

app = wx.App()
dl = DataList(None, -1, "Stock Difference")
dl.Show()
app.MainLoop()
