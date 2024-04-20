import wx
import sqlite3 as db

class NewFilm(wx.Dialog): # Dialog Box

    def __init__(self):
        wx.Dialog.__init__(self, None, title= "Dialog", size = (450,250))

        lbl = wx.StaticText(self, label="Enter A New Film", pos=(175, 10))

        self.title = wx.TextCtrl(self, -1, "", pos=(100, 39))
        wx.StaticText(self, -1, "title:", pos=(15, 40))

        self.release = wx.TextCtrl(self, -1, "", (100, 79))
        wx.StaticText(self, -1, "release_year:", (15, 80))

        self.language = wx.TextCtrl(self, -1, "", (100, 119))
        wx.StaticText(self, -1, "language:", (15, 120))

        self.rate = wx.TextCtrl(self, -1, "", pos=(305, 39))
        wx.StaticText(self, -1, "rental_rate:", pos=(220, 40))

        self.length = wx.TextCtrl(self, -1, "", (305, 79))
        wx.StaticText(self, -1, "length:", (220, 80))

        self.rating = wx.TextCtrl(self, -1, "", (305, 119))
        wx.StaticText(self, -1, "rating:", (220, 120))

        save = wx.Button(self, id=wx.ID_OK, pos=(175, 170))  

class DataList(wx.Frame): # Data frames
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(600, 400))
        panel = wx.Panel(self, -1)

        self.table_name = wx.StaticText(panel, -1, "Film Data", pos=(260, 3))
        self.list = wx.ListCtrl(panel, -1, style=wx.LC_REPORT, pos=(20, 30), size=(550, 270))

        # Columns
        self.list.InsertColumn(0, "film_id", width=55)
        self.list.InsertColumn(1, "title", width=130)
        self.list.InsertColumn(2, "release_year", width=85)
        self.list.InsertColumn(3, "language", width=70)
        self.list.InsertColumn(4, "rental_rate", width=75)
        self.list.InsertColumn(5, "length", width=55)
        self.list.InsertColumn(6, "rating", width=60)
        

        # Buttons
        display = wx.Button(panel, -1, "Display", size=(-1, 35), pos=(100, 315))
        insert = wx.Button(panel, -1, "Insert Film", size=(-1, 35), pos=(250, 315))
        close = wx.Button(panel, -1, "Close", size=(-1, 35), pos=(400, 315))

        # Binding Buttons
        display.Bind(wx.EVT_BUTTON, self.OnDisplay )
        insert.Bind(wx.EVT_BUTTON, self.OnAdd )
        close.Bind(wx.EVT_BUTTON, self.OnClose)

        self.Centre()

    def getAllData(self): # Pull Data from Database

        self.list.DeleteAllItems()
        con = db.connect("movies.db")
        cur = con.cursor()

        cur.execute("SELECT * FROM afilms")
        results = cur.fetchall()
        for row in results:
            self.list.Append(row)

        cur.close()
        con.close()


    def OnDisplay(self, event): # Display Data from Database

        try:
            self.getAllData()

        except lite.Error as error:
            error = wx.MessageDialog(self, str(error), "An Error Has Occurred.")
            error.ShowModal()


    def OnAdd(self, event): # Add Data to Database
        film = NewFilm()
        btnFilm = film.ShowModal()
        if btnFilm == wx.ID_OK:
            title = film.title.GetValue()
            release = film.release.GetValue()
            language = film.language.GetValue()
            rate = film.rate.GetValue()
            length = film.length.GetValue()
            rating = film.rating.GetValue()

        if title != "" and release != "" and language != "" and rate != "" and length != "" and rating != "":

            try:
                con = db.connect("movies.db")
                cur = con.cursor()

                sql = "INSERT INTO afilms VALUES (?, ?, ?, ?, ?, ?, ?)"

                cur.execute(sql, (None, title, release, language, rate, length, rating))
                con.commit()

                self.getAllData()

            except lite.Error as error:
                dlg = wx.MessageDialog(self, str(error), "An Error Has Occurred.")
                dlg.ShowModal()

        film.Destroy()


    def OnClose(self, event): # Close Program
        self.Close()


app = wx.App()
dl = DataList(None, -1, "Movie Archive")
dl.Show()
app.MainLoop()
