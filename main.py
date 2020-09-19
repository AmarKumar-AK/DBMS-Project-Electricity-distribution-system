#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from functools import partial
import wx
import string
from random import*
import wx.lib.scrolledpanel as scrolled
import MySQLdb as mdb

con = mdb.connect('localhost', 'admin', 'admin', 'eds')
cur=con.cursor()
# with con:
#     cur=con.cursor()

class HeadNewPanel(wx.Panel):

    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent,size=(w,100),pos=(0,0))
        l1=wx.StaticText(self, -1,"Electricity Distribution System",pos=(350,30),size=(300,30),style = wx.ALIGN_CENTER)
        l1.SetFont(wx.Font(30,wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD))
        l1.SetForegroundColour("white")
class NewPanel(wx.Panel):

    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent,size=(w,h-100),pos=(0,100))
        self.Bind(wx.EVT_PAINT, self.OnPaintN)
    def OnPaintN(self,e) :
        dc = wx.PaintDC(self)
        dc.SetBrush(wx.Brush(wx.Colour(255,255,255)))
        dc.DrawRectangle(10, 10, 1346, 500)

class upperNewPanel(wx.Panel):

    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent,size=(w,165),pos=(0,100))
class lowerNewPanel(wx.Panel):

    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent,size=(w,h-265),pos=(0,220))

class MainWindow(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent=None,style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        self.SetIcon(wx.Icon("display1.ico"))
        global w,h
        w,h=wx.GetDisplaySize()
        self.InitUI()


    def InitUI(self):

        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        fileItem = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)

        self.Bind(wx.EVT_MENU, self.OnClose, fileItem)

        self.headpnl=HeadNewPanel(self)
        imr = 'logor1.png'
        bmp1 = wx.Image(imr, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.bitmap1 = wx.StaticBitmap(self.headpnl, -1, bmp1, (20,10))
        self.headpnl.SetBackgroundColour("grey16")

        self.homepnl = NewPanel(self)

        imr = '4r.jpg'

        bmp1 = wx.Image(imr, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.bitmap1 = wx.StaticBitmap(self.homepnl, -1, bmp1, (0,0))

        pcButton = wx.Button(self.homepnl, label='Power Company', pos=(40, 150),size=(200,40))
        dcButton = wx.Button(self.homepnl, label='Distribution Company', pos=(40, 200),size=(200,40))
        tcButton = wx.Button(self.homepnl, label='Transmission Company', pos=(40, 250),size=(200,40))
        ebButton = wx.Button(self.homepnl, label='Electricity Board', pos=(40, 300),size=(200,40))


        pcButton.Bind(wx.EVT_BUTTON, self.pc)
        dcButton.Bind(wx.EVT_BUTTON, self.dc)
        tcButton.Bind(wx.EVT_BUTTON, self.tc)
        ebButton.Bind(wx.EVT_BUTTON, self.eb)

        l0 = wx.StaticText(self.homepnl, -1, "Customer Login ",pos=(600,170),size=(500,500))
        l0.SetFont(wx.Font(16,wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        #l0.SetForegroundColour("white")
        errormsg = wx.StaticText(self.homepnl, -1, " ",pos=(610,340))
        l1 = wx.StaticText(self.homepnl, -1, "Customer ID : ",pos=(510,240))
        l1.SetForegroundColour("white")
        t1 = wx.TextCtrl(self.homepnl,style= wx.TE_PROCESS_ENTER,pos=(610,230),size=(200,40))
        l2 = wx.StaticText(self.homepnl, -1, "Password    : ",pos=(510,290))
        l2.SetForegroundColour("white")
        t2 = wx.TextCtrl(self.homepnl,style = wx.TE_PASSWORD|wx.TE_PROCESS_ENTER,pos=(610,280),size=(200,40))
        t1.Bind(wx.EVT_TEXT_ENTER,partial(self.Login,t1=t1,t2=t2,errormsg=errormsg))
        t2.Bind(wx.EVT_TEXT_ENTER,partial(self.Login,t1=t1,t2=t2,errormsg=errormsg))

        loginButton = wx.Button(self.homepnl, label='Log In', pos=(715, 370))
        loginButton.Bind(wx.EVT_BUTTON, partial(self.Login,t1=t1,t2=t2,errormsg=errormsg))
        NacButton = wx.Button(self.homepnl, label='Not a Consumer', pos=(515, 370))
        NacButton.Bind(wx.EVT_BUTTON, partial(self.EmpLoginForm,pt1=t1,pt2=t2,perrormsg=errormsg))
        newConButton = wx.Button(self.homepnl, label='Apply New Connection', pos=(1000,20),size=(200,40))
        newConButton.Bind(wx.EVT_BUTTON,self.newConnection)
        statBtn = wx.Button(self.homepnl, label='Know Your Conn. status', pos=(1000,80),size=(200,40))
        statBtn.Bind(wx.EVT_BUTTON,self.ncStat)
        #w,h=wx.GetDisplaySize()
        self.SetSize((w,h))
        self.SetMaxSize((w,h))
        self.SetMinSize((w,h))
        self.SetTitle('Power Distribution System')
        self.Centre()
        self.homepnl.Bind(wx.EVT_PAINT, partial(self.OnPaint,op=self.homepnl))
        #self.Centre()
        #self.Show(True)


    def OnPaint(self,e,op):
        dc = wx.PaintDC(op)
        dc.SetBrush(wx.Brush(wx.Colour(255,255,255)))
        dc.DrawRectangle(10, 10, 1346, 500)
        dc.SetBrush(wx.Brush(wx.Colour(220,217,217)))
        dc.DrawRectangle(450, 160, 480, 290)

    def ncStat(self,e):
        self.homepnl.Hide()
        self.previousTitle=self.GetTitle()
        self.SetTitle("Application Status form New Connection")
        self.ncstatpnl=NewPanel(self)
        msg=wx.StaticText(self.ncstatpnl, -1, "",pos=(600,250),size=(300,300))
        l1=wx.StaticText(self.ncstatpnl, -1, "Provide your ref_id :",pos=(400,250),size=(500,500))
        self.t222 = wx.TextCtrl(self.ncstatpnl,style= wx.TE_PROCESS_ENTER,pos=(600,250),size=(200,40))
        knowstatButton = wx.Button(self.ncstatpnl, label='submit', pos=(650, 310))
        knowstatButton.Bind(wx.EVT_BUTTON, partial(self.ncstatsubmit,msg=msg))
        backButton = wx.Button(self.ncstatpnl, label='Back', pos=(1000, 15))
        backButton.Bind(wx.EVT_BUTTON, partial(self.back,p1=self.ncstatpnl,p2=self.homepnl,title="Power Distribution System"))
        #self.ncstatpnl.Bind(wx.EVT_PAINT, partial(self.OnPaint2,op=self.ncstatpnl))


    def ncstatsubmit(self,e,msg):
        if(self.t222.GetValue()):
            cur.execute("select status from ncstatus where refid=%s",(self.t222.GetValue(),))
            rows=cur.fetchall()
            print(len(rows))
            if(len(rows)!=0):
                self.ncstatpnl.Hide()
                self.previousTitle=self.GetTitle()
                self.SetTitle("Status for New Connection")
                self.statpnl=NewPanel(self)
                backButton = wx.Button(self.statpnl, label='Back', pos=(1000, 15))
                backButton.Bind(wx.EVT_BUTTON, partial(self.back,p1=self.statpnl,p2=self.ncstatpnl,title="Application Status form New Connection"))
                if rows[0][0]=='Aproved' :
                    msg='Hi Your Application has been succesfuly Aproved !!'
                    wx.MessageBox(message=msg,caption='Info',style=wx.OK | wx.ICON_INFORMATION)
                    l1=wx.StaticText(self.statpnl, -1,'Status  : ',              pos=(980,350),size=(500,500))
                    l1.SetFont(wx.Font(15,wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
                    l2=wx.StaticText(self.statpnl, -1, rows[0][0] ,  pos=(1100,350),size=(500,500))
                    l2.SetFont(wx.Font(15,wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

                    l3=wx.StaticText(self.statpnl, -1,'Reference no. : ',              pos=(900,150),size=(500,500))
                    l3.SetFont(wx.Font(15,wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
                    l4=wx.StaticText(self.statpnl, -1, self.t222.GetValue() ,  pos=(1100,150),size=(500,500))
                    l4.SetFont(wx.Font(15,wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

                    h1=wx.StaticText(self.statpnl, -1,'Applicant Name     :',          pos=(100,100),size=(500,20))
                    h2=wx.StaticText(self.statpnl, -1,'Consumer id        :',          pos=(100,130),size=(500,20))
                    h3=wx.StaticText(self.statpnl, -1,'Phone no           :',          pos=(100,160),size=(500,20))
                    h4=wx.StaticText(self.statpnl, -1,'Boardname          :',          pos=(100,190),size=(500,20))
                    h5=wx.StaticText(self.statpnl, -1,'State              :',          pos=(100,220),size=(500,20))
                    h6=wx.StaticText(self.statpnl, -1,'Subdivision        :',          pos=(100,250),size=(500,20))
                    h7=wx.StaticText(self.statpnl, -1,'Division           :',          pos=(100,280),size=(500,20))
                    h8=wx.StaticText(self.statpnl, -1,'City               :',          pos=(100,310),size=(500,20))
                    h9=wx.StaticText(self.statpnl, -1,'Meter no.          :',          pos=(100,340),size=(500,20))
                    h10=wx.StaticText(self.statpnl, -1,'Email id          :',          pos=(100,370),size=(500,20))
                    h11=wx.StaticText(self.statpnl, -1,'Insta.. add       :',          pos=(100,400),size=(500,20))
                    h1.SetBackgroundColour('light gray')
                    h2.SetBackgroundColour('light gray')
                    h3.SetBackgroundColour('light gray')
                    h4.SetBackgroundColour('light gray')
                    h5.SetBackgroundColour('light gray')
                    h6.SetBackgroundColour('light gray')
                    h7.SetBackgroundColour('light gray')
                    h8.SetBackgroundColour('light gray')
                    h9.SetBackgroundColour('light gray')
                    h10.SetBackgroundColour('light gray')
                    h11.SetBackgroundColour('light gray')


                    cur.execute("select * from consumer c,ncstatus n where c.cid=n.cid and refid=%s",(self.t222.GetValue(),))
                    d=cur.fetchall()
                    self.t222.Clear()
                    wx.StaticText(self.statpnl, -1, d[0][1]  ,  pos=(260,100),size=(500,500))
                    wx.StaticText(self.statpnl, -1, str(d[0][0]) ,  pos=(260,130),size=(500,500))
                    wx.StaticText(self.statpnl, -1, str(d[0][2])  ,  pos=(260,160),size=(500,500))
                    wx.StaticText(self.statpnl, -1, d[0][3] ,  pos=(260,190),size=(500,500))
                    wx.StaticText(self.statpnl, -1, d[0][4] ,  pos=(260,220),size=(500,500))
                    wx.StaticText(self.statpnl, -1, d[0][5] ,  pos=(260,250),size=(500,500))
                    wx.StaticText(self.statpnl, -1, d[0][6]  ,  pos=(260,280),size=(500,500))
                    wx.StaticText(self.statpnl, -1, d[0][7] ,  pos=(260,310),size=(500,500))
                    wx.StaticText(self.statpnl, -1, str(d[0][8]) ,  pos=(260,340),size=(500,500))
                    wx.StaticText(self.statpnl, -1, d[0][10] ,  pos=(260,370),size=(500,500))
                    wx.StaticText(self.statpnl, -1, d[0][11] ,  pos=(260,400),size=(500,500))


                    l2.SetForegroundColour((0,255,0))
                    #self.statpnl.Bind(wx.EVT_PAINT, partial(self.OnPaint2,op=self.statpnl))
                else:
                    if rows[0][0]=='pending' :
                        h12=wx.StaticText(self.statpnl, -1,'Applicant Name :',          pos=(100,100),size=(500,20))
                        h13=wx.StaticText(self.statpnl, -1,'Phone no       :',          pos=(100,130),size=(500,20))
                        h14=wx.StaticText(self.statpnl, -1,'Boardname      :',          pos=(100,160),size=(500,20))
                        h15=wx.StaticText(self.statpnl, -1,'State          :',          pos=(100,190),size=(500,20))
                        h16=wx.StaticText(self.statpnl, -1,'Subdivision    :',          pos=(100,220),size=(500,20))
                        h17=wx.StaticText(self.statpnl, -1,'Division       :',          pos=(100,250),size=(500,20))
                        h18=wx.StaticText(self.statpnl, -1,'City           :',          pos=(100,280),size=(500,20))
                        h19=wx.StaticText(self.statpnl, -1,'Email id       :',          pos=(100,310),size=(500,20))
                        h20=wx.StaticText(self.statpnl, -1,'Insta.. add    :',          pos=(100,340),size=(500,20))
                        h12.SetBackgroundColour('light gray')
                        h13.SetBackgroundColour('light gray')
                        h14.SetBackgroundColour('light gray')
                        h15.SetBackgroundColour('light gray')
                        h16.SetBackgroundColour('light gray')
                        h17.SetBackgroundColour('light gray')
                        h18.SetBackgroundColour('light gray')
                        h19.SetBackgroundColour('light gray')
                        h20.SetBackgroundColour('light gray')
                        cur.execute("select * from newconnection where refid=%s",(self.t222.GetValue(),))
                        dt=cur.fetchall()
                        print(dt)
                        wx.StaticText(self.statpnl, -1, dt[0][0]  ,      pos=(260,100),size=(500,500))
                        wx.StaticText(self.statpnl, -1, str(dt[0][1]) ,  pos=(260,130),size=(500,500))
                        wx.StaticText(self.statpnl, -1, dt[0][2]  ,      pos=(260,160),size=(500,500))
                        wx.StaticText(self.statpnl, -1, dt[0][3] ,       pos=(260,190),size=(500,500))
                        wx.StaticText(self.statpnl, -1, dt[0][4] ,       pos=(260,220),size=(500,500))
                        wx.StaticText(self.statpnl, -1, dt[0][5] ,       pos=(260,250),size=(500,500))
                        wx.StaticText(self.statpnl, -1, dt[0][6]  ,      pos=(260,280),size=(500,500))
                        wx.StaticText(self.statpnl, -1, dt[0][7] ,       pos=(260,310),size=(500,500))
                        wx.StaticText(self.statpnl, -1, dt[0][8] ,       pos=(260,340),size=(500,500))
                        msg='Hi Your Application is Pending \n \n and is under verification process'
                        l1=wx.StaticText(self.statpnl, -1,'Status  : ',              pos=(980,350),size=(500,500))
                        l1.SetFont(wx.Font(15,wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
                        l2=wx.StaticText(self.statpnl, -1, rows[0][0] ,  pos=(1100,350),size=(500,500))
                        l2.SetFont(wx.Font(15,wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

                        l3=wx.StaticText(self.statpnl, -1,'Reference no. : ',              pos=(900,150),size=(500,500))
                        l3.SetFont(wx.Font(15,wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
                        l4=wx.StaticText(self.statpnl, -1, self.t222.GetValue() ,  pos=(1100,150),size=(500,500))
                        l4.SetFont(wx.Font(15,wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
                        l2.SetForegroundColour((0,0,255))
                        #self.statpnl.Bind(wx.EVT_PAINT, partial(self.OnPaint2,op=self.statpnl))
                    else:
                        msg='Hi Your Application has been rejected'
                        l1=wx.StaticText(self.statpnl, -1,'Status  : ',              pos=(980,350),size=(500,500))
                        l1.SetFont(wx.Font(15,wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
                        l2=wx.StaticText(self.statpnl, -1, rows[0][0] ,  pos=(1100,350),size=(500,500))
                        l2.SetFont(wx.Font(15,wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

                        l3=wx.StaticText(self.statpnl, -1,'Reference no. : ',              pos=(900,150),size=(500,500))
                        l3.SetFont(wx.Font(15,wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
                        l4=wx.StaticText(self.statpnl, -1, self.t222.GetValue() ,  pos=(1100,150),size=(500,500))
                        l4.SetFont(wx.Font(15,wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
                        l2.SetForegroundColour((255,0,0))
                        #self.statpnl.Bind(wx.EVT_PAINT, partial(self.OnPaint2,op=self.statpnl))
                    wx.MessageBox(message=msg,caption='Info',style=wx.OK | wx.ICON_INFORMATION)

                    self.t222.Clear()
            else:
                """msg.Hide()
                msg.Show()
                msg.SetLabel("Invalid reference id")
                msg.SetForegroundColour((255,0,0))"""
                msg="Invalid reference id"
                wx.MessageBox(message=msg,caption='Info',style=wx.OK | wx.ICON_INFORMATION)
        else:
            """msg.Hide()
            msg.Show()
            msg.SetLabel("Enter reference id pleas!!!!")
            msg.SetForegroundColour((255,0,0))"""
            msg="Enter reference id pleas!!!!"
            wx.MessageBox(message=msg,caption='Info',style=wx.OK | wx.ICON_INFORMATION)


    def newConnection(self,e):
        self.homepnl.Hide()

        self.SetTitle("Application for New Connection")
        self.ncpnl=NewPanel(self)
        #self.ncpnl.SetBackgroundColour((232,232,232))
        ebButton = wx.Button(self.ncpnl, label='Back', pos=(1000, 10))
        ebButton.Bind(wx.EVT_BUTTON, partial(self.back,p1=self.ncpnl,p2=self.homepnl,title="Power Distribution System"))

        l1=wx.StaticText(self.ncpnl, -1, "State/UT :",pos=(w/2-230,180),size=(500,500))
        l2=wx.StaticText(self.ncpnl, -1, "Distribution Company :",pos=(w/2-230,230),size=(500,500))
        l3=wx.StaticText(self.ncpnl, -1, "Division :",pos=(w/2-230,280),size=(500,500))
        l4=wx.StaticText(self.ncpnl, -1, "Sub Division :",pos=(w/2-230,330),size=(500,500))
        l1.SetFont(wx.Font(12,wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        l2.SetFont(wx.Font(12,wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        l3.SetFont(wx.Font(12,wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        l4.SetFont(wx.Font(12,wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute("select state from distributioncompany")
        rows=cur.fetchall()
        #desc = cur.description()
        stateList=list()
        for row in rows:
            stateList.append(row["state"])
        print (stateList)
        self.cbState=wx.ComboBox(self.ncpnl,pos=(w/2,180),size=(300,30),choices=stateList)
        self.cbState.Bind(wx.EVT_COMBOBOX, self.ncDcSelect)
        #self.ncpnl.Bind(wx.EVT_PAINT, partial(self.OnPaint1,op=self.ncpnl))

    def OnPaint1(self,e,op):
        dc = wx.PaintDC(op)
        dc.SetBrush(wx.Brush(wx.Colour(255,255,255)))
        dc.DrawRectangle(10, 10, 1346, 500)
        dc.SetBrush(wx.Brush(wx.Colour(220,217,217)))
        dc.DrawRectangle(400, 140, 600, 320)

    def ncDcSelect(self,e):
        self.state=e.GetString()
        print (self.state)
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute("select dname from distributioncompany where state = %s",(self.state,))
        rows=cur.fetchall()
        dcList=list()
        for row in rows:
            dcList.append(row["dname"])
        print (dcList)
        self.cbDc=wx.ComboBox(self.ncpnl,pos=(w/2,230),size=(300,30),choices=dcList)
        self.cbDc.Bind(wx.EVT_COMBOBOX, self.ncDivSelect)

    def ncDivSelect(self,e):
        self.Dc=e.GetString()
        print (self.Dc)
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute("select divname from division as d1,distributioncompany as d2 where d1.did=d2.did and d2.dname=%s and d2.state=%s ",(self.Dc,self.state))
        rows=cur.fetchall()
        divList=list()
        for row in rows:
            divList.append(row["divname"])
        print (divList)
        self.cbDc=wx.ComboBox(self.ncpnl,pos=(w/2,280),size=(300,30),choices=divList)
        self.cbDc.Bind(wx.EVT_COMBOBOX, self.ncSubdivSelect)
    def ncSubdivSelect(self,e):
        self.Div=e.GetString()
        print (self.Div)
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute("select sdivname from subdivision as d1,division as d2 where d1.divid=d2.divid and d1.state=%s and d2.divname=%s",(self.state,self.Div))
        rows=cur.fetchall()
        sdivList=list()
        for row in rows:
            sdivList.append(row["sdivname"])
        print (sdivList)
        self.cbDc=wx.ComboBox(self.ncpnl,pos=(w/2,330),size=(300,30),choices=sdivList)
        self.cbDc.Bind(wx.EVT_COMBOBOX, self.submit_form1)

    def submit_form1(self,e):
        self.Subdiv=e.GetString()
        print (self.Subdiv)
        submitForm=wx.Button(self.ncpnl, label='Submit', pos=(w/2, 400))
        submitForm.Bind(wx.EVT_BUTTON,self.NewconForm)

    def eb(self,e):
        #self.lpnl.SetBackgroundColour("blue")
        self.homepnl.Hide()
        self.SetTitle("Electricity Board")
        self.upnl= upperNewPanel(self)
        self.lpnl=lowerNewPanel(self)
        ebButton = wx.Button(self.upnl, label='Back', pos=(1000, 10))
        ebButton.Bind(wx.EVT_BUTTON, partial(self.back_tc_pc_dc_eb,p1=self.upnl,p2=self.homepnl,title="Power Distribution System"))
        #l1 = wx.StaticText(self.ebpnl, -1,"hello",pos=(10,10))

        self.ebNameSearch=wx.SearchCtrl(self.upnl,pos=(120,50),size=(200,40))
        self.ebNameSearch.SetDescriptiveText("Search by B.name")
        self.ebNameSearch.Bind(wx.EVT_TEXT,self.ebNameS)


        ebAll = wx.Button(self.upnl, label='Show all', pos=(10, 50),size=(100,40))
        ebAll.Bind(wx.EVT_BUTTON, self.ebAll)
        wx.StaticText(self.upnl, -1,"State/UT:",pos=(500,60))
        t1 = wx.SearchCtrl(self.upnl,pos=(570,50),size=(200,40))
        t1.SetDescriptiveText("Search by State/UT")
        self.ebStateSB=t1
        t1.Bind(wx.EVT_TEXT,partial(self.ebStateSearch,t1=t1))
        if(t1.GetValue()==""):
            cur = con.cursor(mdb.cursors.DictCursor)
            cur.execute("SELECT * FROM electricityboard ")
            rows = cur.fetchall()
            desc = cur.description

            l0=wx.StaticText(self.upnl, -1,"Board Name",pos=(70,100),size=(500,500))
            l0.SetFont(wx.Font(10,wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
            l1=wx.StaticText(self.upnl, -1,"No. of Consumer",pos=(270,100),size=(500,500))
            l1.SetFont(wx.Font(10,wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
            l2=wx.StaticText(self.upnl, -1,"State/UT",pos=(470,100),size=(500,500))
            l2.SetFont(wx.Font(10,wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
            l3=wx.StaticText(self.upnl, -1,"Power Consumed",pos=(600,100),size=(500,500))
            l3.SetFont(wx.Font(10,wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

            #print "%s %s %s %s %s" % (desc[0][0], desc[1][0],desc[2][0],desc[3][0],desc[4][0])
            i=20
            for row in rows:
                #txt = row[desc[0][0]], row[desc[1][0]], row[desc[2][0]],row[desc[3][0]],row[desc[4][0]]
                wx.StaticText(self.lpnl, -1,row[desc[0][0]],pos=(80,i))
                wx.StaticText(self.lpnl, -1,str(row[desc[1][0]]),pos=(270,i))
                wx.StaticText(self.lpnl, -1,row[desc[2][0]],pos=(470,i))
                wx.StaticText(self.lpnl, -1,str(row[desc[4][0]]),pos=(600,i))

                i=i+30
        #self.lpnl.Show()


    def ebNameS(self,e):
        if(self.ebStateSB.IsEmpty()==0):
            self.ebStateSB.Clear()        #searching by boardname(dynamically)
        self.lpnl.Hide()
        name=e.GetString()
        self.lpnl=lowerNewPanel(self)
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute("select * FROM electricityboard where boardname like '{}%'".format(name))
        rows=cur.fetchall()
        desc = cur.description
        if(len(rows)==0):
            msg=wx.StaticText(self.lpnl, -1,"Not available !!",pos=(300,30))
            msg.SetForegroundColour((255,0,0))
        i=20
        for row in rows:
            wx.StaticText(self.lpnl, -1,row[desc[0][0]],pos=(80,i))
            wx.StaticText(self.lpnl, -1,str(row[desc[1][0]]),pos=(270,i))
            wx.StaticText(self.lpnl, -1,row[desc[2][0]],pos=(470,i))
            wx.StaticText(self.lpnl, -1,str(row[desc[4][0]]),pos=(600,i))
            i=i+30


    def ebAll(self,e):
        if(self.ebNameSearch.IsEmpty()==0):
            self.ebNameSearch.Clear()
        if(self.ebStateSB.IsEmpty()==0):
            self.ebStateSB.Clear()

        self.lpnl.Hide()
        self.lpnl=lowerNewPanel(self)
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute("SELECT * FROM electricityboard ")
        rows = cur.fetchall()
        desc = cur.description
        #print "%s %s %s %s %s" % (desc[0][0], desc[1][0],desc[2][0],desc[3][0],desc[4][0])
        i=20
        for row in rows:
            #txt = row[desc[0][0]], row[desc[1][0]], row[desc[2][0]],row[desc[3][0]],row[desc[4][0]]
            wx.StaticText(self.lpnl, -1,row[desc[0][0]],pos=(80,i))
            wx.StaticText(self.lpnl, -1,str(row[desc[1][0]]),pos=(270,i))
            wx.StaticText(self.lpnl, -1,row[desc[2][0]],pos=(470,i))
            wx.StaticText(self.lpnl, -1,str(row[desc[4][0]]),pos=(600,i))
            i=i+30
    def ebStateSearch(self,e,t1):
        if(self.ebNameSearch.IsEmpty()==0):
            self.ebNameSearch.Clear()
        if(t1.GetValue()):
            self.lpnl.Hide()

            self.lpnl=lowerNewPanel(self)

            #lpnl.SetBackgroundColour("grey")
            print ("hello")
            self.lpnl.Show()
            print (t1.GetValue())
            cur = con.cursor(mdb.cursors.DictCursor)
            cur.execute("SELECT * FROM electricityboard where state like '{}%'".format(t1.GetValue()))
            rows = cur.fetchall()
            desc = cur.description
            if(len(rows)==0):
                msg=wx.StaticText(self.lpnl, -1,"Not available !!",pos=(300,30))
                msg.SetForegroundColour((255,0,0))
            #wx.StaticText(lpnl, -1,"Board Name",pos=(70,100))
            #wx.StaticText(lpnl, -1,"No. of Consumer",pos=(270,100))
            #wx.StaticText(lpnl, -1,"State",pos=(470,100))
            #wx.StaticText(lpnl, -1,"Power Consumed",pos=(600,100))
            dc = wx.ClientDC(self)
            dc.DrawLine(50, 60, 190, 60)
            #print "%s %s %s %s %s" % (desc[0][0], desc[1][0],desc[2][0],desc[3][0],desc[4][0])
            i=20
            for row in rows:
                #txt = row[desc[0][0]], row[desc[1][0]], row[desc[2][0]],row[desc[3][0]],row[desc[4][0]]
                wx.StaticText(self.lpnl, -1,row[desc[0][0]],pos=(80,i))
                wx.StaticText(self.lpnl, -1,str(row[desc[1][0]]),pos=(270,i))
                wx.StaticText(self.lpnl, -1,row[desc[2][0]],pos=(470,i))
                wx.StaticText(self.lpnl, -1,str(row[desc[4][0]]),pos=(600,i))

                i=i+30
        if(t1.GetValue()==""):
            self.lpnl.Hide()
            self.lpnl=lowerNewPanel(self)
            cur = con.cursor(mdb.cursors.DictCursor)
            cur.execute("SELECT * FROM electricityboard ")
            rows = cur.fetchall()
            desc = cur.description
            #print "%s %s %s %s %s" % (desc[0][0], desc[1][0],desc[2][0],desc[3][0],desc[4][0])
            i=20
            for row in rows:
                #txt = row[desc[0][0]], row[desc[1][0]], row[desc[2][0]],row[desc[3][0]],row[desc[4][0]]
                wx.StaticText(self.lpnl, -1,row[desc[0][0]],pos=(80,i))
                wx.StaticText(self.lpnl, -1,str(row[desc[1][0]]),pos=(270,i))
                wx.StaticText(self.lpnl, -1,row[desc[2][0]],pos=(470,i))
                wx.StaticText(self.lpnl, -1,str(row[desc[4][0]]),pos=(600,i))

                i=i+30

    def tcStateSearch(self,e,t1):
        if(t1.GetValue()):
            self.lpnl.Hide()
            self.lpnl=lowerNewPanel(self)
            self.lpnl.Show()

            #self.currentpnl.SetBackgroundColour("pink")
            cur = con.cursor(mdb.cursors.DictCursor)
            cur.execute("SELECT * FROM transmissioncompany where state like '{}%'".format(t1.GetValue()))
            rows = cur.fetchall()
            desc = cur.description
            if(len(rows)==0):
                msg=wx.StaticText(self.lpnl, -1,"Not available !!",pos=(300,30))
                msg.SetForegroundColour((255,0,0))
            i=20
            for row in rows:
                #txt = row[desc[0][0]], row[desc[1][0]], row[desc[2][0]],row[desc[3][0]],row[desc[4][0]]
                wx.StaticText(self.lpnl, -1,row[desc[1][0]],pos=(100,i))
                wx.StaticText(self.lpnl, -1,row[desc[4][0]],pos=(300,i))
                wx.StaticText(self.lpnl, -1,str(row[desc[3][0]]),pos=(500,i))
                wx.StaticText(self.lpnl, -1,str(row[desc[5][0]]),pos=(700,i))
                i=i+30

    def tcNameS(self,e):
        if(self.tcNameSearch.GetValue()):
            self.lpnl.Hide()
            self.lpnl=lowerNewPanel(self)
            self.lpnl.Show()

            #self.currentpnl.SetBackgroundColour("pink")
            cur = con.cursor(mdb.cursors.DictCursor)
            cur.execute("SELECT * FROM transmissioncompany where tname like '{}%'".format(self.tcNameSearch.GetValue()))
            rows = cur.fetchall()
            desc = cur.description
            if(len(rows)==0):
                msg=wx.StaticText(self.lpnl, -1,"Not available !!",pos=(300,30))
                msg.SetForegroundColour((255,0,0))
            i=20
            for row in rows:
                #txt = row[desc[0][0]], row[desc[1][0]], row[desc[2][0]],row[desc[3][0]],row[desc[4][0]]
                wx.StaticText(self.lpnl, -1,row[desc[1][0]],pos=(100,i))
                wx.StaticText(self.lpnl, -1,row[desc[4][0]],pos=(300,i))
                wx.StaticText(self.lpnl, -1,str(row[desc[3][0]]),pos=(500,i))
                wx.StaticText(self.lpnl, -1,str(row[desc[5][0]]),pos=(700,i))
                i=i+30

    def pcStateSearch(self,e,t1):
        if(t1.GetValue()):
            self.lpnl.Hide()
            self.lpnl=lowerNewPanel(self)
            self.lpnl.Show()

            #self.currentpnl.SetBackgroundColour("pink")
            cur = con.cursor(mdb.cursors.DictCursor)
            cur.execute("SELECT * FROM powercompany where state like '{}%'".format(t1.GetValue()))
            rows = cur.fetchall()
            desc = cur.description
            if(len(rows)==0):
                msg=wx.StaticText(self.lpnl, -1,"Not available !!",pos=(300,30))
                msg.SetForegroundColour((255,0,0))
            i=20
            for row in rows:
                #txt = row[desc[0][0]], row[desc[1][0]], row[desc[2][0]],row[desc[3][0]],row[desc[4][0]]
                wx.StaticText(self.lpnl, -1,row[desc[1][0]],pos=(100,i))
                wx.StaticText(self.lpnl, -1,row[desc[4][0]],pos=(300,i))
                wx.StaticText(self.lpnl, -1,row[desc[2][0]],pos=(500,i))
                wx.StaticText(self.lpnl, -1,str(row[desc[3][0]]),pos=(700,i))
                i=i+30

    def pcNameS(self,e):
        if(self.pcNameSearch.GetValue()):
            self.lpnl.Hide()
            self.lpnl=lowerNewPanel(self)
            self.lpnl.Show()

            #self.currentpnl.SetBackgroundColour("pink")
            cur = con.cursor(mdb.cursors.DictCursor)
            cur.execute("SELECT * FROM powercompany where pname like '{}%'".format(self.pcNameSearch.GetValue()))
            rows = cur.fetchall()
            desc = cur.description
            if(len(rows)==0):
                msg=wx.StaticText(self.lpnl, -1,"Not available !!",pos=(300,30))
                msg.SetForegroundColour((255,0,0))
            i=20
            for row in rows:
                #txt = row[desc[0][0]], row[desc[1][0]], row[desc[2][0]],row[desc[3][0]],row[desc[4][0]]
                wx.StaticText(self.lpnl, -1,row[desc[1][0]],pos=(100,i))
                wx.StaticText(self.lpnl, -1,row[desc[4][0]],pos=(300,i))
                wx.StaticText(self.lpnl, -1,row[desc[2][0]],pos=(500,i))
                wx.StaticText(self.lpnl, -1,str(row[desc[3][0]]),pos=(700,i))
                i=i+30

    def dcStateSearch(self,e,t1):
        if(t1.GetValue()):
            self.lpnl.Hide()
            self.lpnl=lowerNewPanel(self)
            self.lpnl.Show()

            #self.currentpnl.SetBackgroundColour("pink")
            cur = con.cursor(mdb.cursors.DictCursor)
            cur.execute("SELECT * FROM distributioncompany where state like '{}%'".format(t1.GetValue()))
            rows = cur.fetchall()
            desc = cur.description
            if(len(rows)==0):
                msg=wx.StaticText(self.lpnl, -1,"Not available !!",pos=(300,30))
                msg.SetForegroundColour((255,0,0))
            i=20
            for row in rows:
                #txt = row[desc[0][0]], row[desc[1][0]], row[desc[2][0]],row[desc[3][0]],row[desc[4][0]]
                wx.StaticText(self.lpnl, -1,row[desc[1][0]],pos=(100,i))
                wx.StaticText(self.lpnl, -1,row[desc[3][0]],pos=(500,i))
                wx.StaticText(self.lpnl, -1,str(row[desc[2][0]]),pos=(700,i))
                i=i+30

    def dcNameS(self,e):
        if(self.dcNameSearch.GetValue()):
            self.lpnl.Hide()
            self.lpnl=lowerNewPanel(self)
            self.lpnl.Show()

            #self.currentpnl.SetBackgroundColour("pink")
            cur = con.cursor(mdb.cursors.DictCursor)
            cur.execute("SELECT * FROM distributioncompany where dname like '{}%'".format(self.dcNameSearch.GetValue()))
            rows = cur.fetchall()
            desc = cur.description
            if(len(rows)==0):
                msg=wx.StaticText(self.lpnl, -1,"Not available !!",pos=(300,30))
                msg.SetForegroundColour((255,0,0))
            i=20
            for row in rows:
                #txt = row[desc[0][0]], row[desc[1][0]], row[desc[2][0]],row[desc[3][0]],row[desc[4][0]]
                wx.StaticText(self.lpnl, -1,row[desc[1][0]],pos=(100,i))
                wx.StaticText(self.lpnl, -1,row[desc[3][0]],pos=(500,i))
                wx.StaticText(self.lpnl, -1,str(row[desc[2][0]]),pos=(700,i))
                i=i+30

    def tcAll(self,e):
        self.lpnl.Hide()
        self.upnl.Hide()
        self.tc(self)


    def pcAll(self,e):
        self.lpnl.Hide()
        self.upnl.Hide()
        self.pc(self)

    def dcAll(self,e):
        self.lpnl.Hide()
        self.upnl.Hide()
        self.dc(self)






        #self.ebpnl.Show()

    def back(self,e,p1,p2,title):
    	p1.Hide()
    	p2.Show()
    	self.SetTitle(title)


    def back_tc_pc_dc_eb(self,e,p1,p2,title):
        p1.Hide()
        p2.Show()
        self.lpnl.Hide()
        self.SetTitle(title)


    def pc(self,e):
        self.homepnl.Hide()
        self.SetTitle("Power Company")
        self.upnl=upperNewPanel(self)
        self.lpnl=lowerNewPanel(self)
        BackButton = wx.Button(self.upnl, label='Back', pos=(1000, 15),size=(100,40))
        ShowAllButton = wx.Button(self.upnl, label='Show All', pos=(10, 50),size=(100,40))
        BackButton.Bind(wx.EVT_BUTTON,partial(self.back_tc_pc_dc_eb,p1=self.upnl,p2=self.homepnl,title="Power Distribution System"))
        ShowAllButton.Bind(wx.EVT_BUTTON,self.pcAll)
        self.pcNameSearch=wx.SearchCtrl(self.upnl,pos=(120,50),size=(200,40))
        self.pcNameSearch.SetDescriptiveText("Search by P.Name")
        self.pcNameSearch.Bind(wx.EVT_TEXT,self.pcNameS)
        wx.StaticText(self.upnl, -1,"State/UT:",pos=(500,60))
        t1 = wx.SearchCtrl(self.upnl,style= wx.TE_PROCESS_ENTER,pos=(570,50),size=(200,40))
        t1.SetDescriptiveText("Search by State/UT")
        t1.Bind(wx.EVT_TEXT,partial(self.pcStateSearch,t1=t1))
        l0=wx.StaticText(self.upnl, -1,"Name",pos=(100,100),size=(500,500))
        l0.SetFont(wx.Font(10,wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        l1=wx.StaticText(self.upnl, -1,"State",pos=(300,100),size=(500,500))
        l1.SetFont(wx.Font(10,wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        l2=wx.StaticText(self.upnl, -1,"Type",pos=(500,100),size=(500,500))
        l2.SetFont(wx.Font(10,wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        l3=wx.StaticText(self.upnl, -1,"Total power",pos=(700,100),size=(500,500))
        l3.SetFont(wx.Font(10,wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute("SELECT * FROM powercompany ")
        rows = cur.fetchall()
        desc = cur.description

        i=20
        for row in rows:
            #txt = row[desc[0][0]], row[desc[1][0]], row[desc[2][0]],row[desc[3][0]],row[desc[4][0]]
            wx.StaticText(self.lpnl, -1,row[desc[1][0]],pos=(100,i))
            wx.StaticText(self.lpnl, -1,row[desc[4][0]],pos=(300,i))
            wx.StaticText(self.lpnl, -1,row[desc[2][0]],pos=(500,i))
            wx.StaticText(self.lpnl, -1,str(row[desc[3][0]]),pos=(700,i))
            i=i+30



    def dc(self,e):
        self.homepnl.Hide()
        self.SetTitle("Distribution Company")
        self.upnl=upperNewPanel(self)
        self.lpnl=lowerNewPanel(self)
        BackButton = wx.Button(self.upnl, label='Back', pos=(1000, 15),size=(100,40))
        ShowAllButton = wx.Button(self.upnl, label='Show All', pos=(10, 50),size=(100,40))
        BackButton.Bind(wx.EVT_BUTTON,partial(self.back_tc_pc_dc_eb,p1=self.upnl,p2=self.homepnl,title="Power Distribution System"))
        ShowAllButton.Bind(wx.EVT_BUTTON,self.dcAll)
        self.dcNameSearch=wx.SearchCtrl(self.upnl,pos=(120,50),size=(200,40))
        self.dcNameSearch.SetDescriptiveText("Search by D.Name")
        self.dcNameSearch.Bind(wx.EVT_TEXT,self.dcNameS)
        wx.StaticText(self.upnl, -1,"State/UT:",pos=(500,60))
        t1 = wx.SearchCtrl(self.upnl,style= wx.TE_PROCESS_ENTER,pos=(570,50),size=(200,40))
        t1.SetDescriptiveText("Search by State/UT")
        t1.Bind(wx.EVT_TEXT,partial(self.dcStateSearch,t1=t1))
        l0=wx.StaticText(self.upnl, -1,"Name",pos=(100,100),size=(500,500))
        l0.SetFont(wx.Font(10,wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        l1=wx.StaticText(self.upnl, -1,"State",pos=(500,100),size=(500,500))
        l1.SetFont(wx.Font(10,wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        l2=wx.StaticText(self.upnl, -1,"Tenure(in years)",pos=(700,100),size=(500,500))
        l2.SetFont(wx.Font(10,wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute("SELECT * FROM distributioncompany ")
        rows = cur.fetchall()
        desc = cur.description

        i=20
        for row in rows:
            #txt = row[desc[0][0]], row[desc[1][0]], row[desc[2][0]],row[desc[3][0]],row[desc[4][0]]
            wx.StaticText(self.lpnl, -1,row[desc[1][0]],pos=(100,i))
            wx.StaticText(self.lpnl, -1,row[desc[3][0]],pos=(500,i))
            wx.StaticText(self.lpnl, -1,str(row[desc[2][0]]),pos=(700,i))
            i=i+30


    def tc(self,e):
        self.homepnl.Hide()
        self.SetTitle("Transmission Company")
        self.upnl=upperNewPanel(self)
        self.lpnl=lowerNewPanel(self)
        BackButton = wx.Button(self.upnl, label='Back', pos=(1000, 15),size=(100,40))
        ShowAllButton = wx.Button(self.upnl, label='Show All', pos=(10, 50),size=(100,40))
        BackButton.Bind(wx.EVT_BUTTON,partial(self.back_tc_pc_dc_eb,p1=self.upnl,p2=self.homepnl,title="Power Distribution System"))
        ShowAllButton.Bind(wx.EVT_BUTTON,self.tcAll)
        self.tcNameSearch=wx.SearchCtrl(self.upnl,pos=(120,50),size=(200,40))
        self.tcNameSearch.SetDescriptiveText("Search by T.name")
        self.tcNameSearch.Bind(wx.EVT_TEXT,self.tcNameS)
        wx.StaticText(self.upnl, -1,"State/UT:",pos=(500,60))
        t1 = wx.SearchCtrl(self.upnl,style= wx.TE_PROCESS_ENTER,pos=(570,50),size=(200,40))
        t1.SetDescriptiveText("Search by State/UT")
        t1.Bind(wx.EVT_TEXT,partial(self.tcStateSearch,t1=t1))
        l0=wx.StaticText(self.upnl, -1,"Name",pos=(100,100),size=(500,500))
        l0.SetFont(wx.Font(10,wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        l1=wx.StaticText(self.upnl, -1,"State",pos=(300,100),size=(500,500))
        l1.SetFont(wx.Font(10,wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        l2=wx.StaticText(self.upnl, -1,"Capacity",pos=(500,100),size=(500,500))
        l2.SetFont(wx.Font(10,wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        l3=wx.StaticText(self.upnl, -1,"Tenure(in years)",pos=(700,100),size=(500,500))
        l3.SetFont(wx.Font(10,wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute("SELECT * FROM transmissioncompany ")
        rows = cur.fetchall()
        desc = cur.description
        # print rows[0][desc[1][0]]
        # print rows[0][desc[3][0]]
        # print rows[0][desc[4][0]]
        i=20
        for row in rows:
            #txt = row[desc[0][0]], row[desc[1][0]], row[desc[2][0]],row[desc[3][0]],row[desc[4][0]]
            wx.StaticText(self.lpnl, -1,row[desc[1][0]],pos=(100,i))
            wx.StaticText(self.lpnl, -1,row[desc[4][0]],pos=(300,i))
            wx.StaticText(self.lpnl, -1,str(row[desc[3][0]]),pos=(500,i))
            wx.StaticText(self.lpnl, -1,str(row[desc[5][0]]),pos=(700,i))
            i=i+30

    def EmpLoginForm(self,e,pt1,pt2,perrormsg):
        self.homepnl.Hide()
        self.SetTitle("Employee Login")
        self.emplpnl=NewPanel(self)
        errormsg = wx.StaticText(self.emplpnl, -1, " ",pos=(610,140))
        l0 = wx.StaticText(self.emplpnl, -1, "Employee Login ",pos=(600,170),size=(500,500))
        l0.SetFont(wx.Font(16,wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        l1 = wx.StaticText(self.emplpnl, -1, "Employee ID : ",pos=(510,240))
        t1 = wx.TextCtrl(self.emplpnl,style= wx.TE_PROCESS_ENTER,pos=(610,230),size=(200,40))
        l1 = wx.StaticText(self.emplpnl, -1, "Password    : ",pos=(510,290))
        t2 = wx.TextCtrl(self.emplpnl,style = wx.TE_PASSWORD|wx.TE_PROCESS_ENTER,pos=(610,280),size=(200,40))
        t1.Bind(wx.EVT_TEXT_ENTER,partial(self.EmpLogin,t1=t1,t2=t2,errormsg=errormsg))
        t2.Bind(wx.EVT_TEXT_ENTER,partial(self.EmpLogin,t1=t1,t2=t2,errormsg=errormsg))
        loginButton = wx.Button(self.emplpnl, label='Log In', pos=(715, 370))
        loginButton.Bind(wx.EVT_BUTTON, partial(self.EmpLogin,t1=t1,t2=t2,errormsg=errormsg))


        BackButton = wx.Button(self.emplpnl, label='Back', pos=(1000, 15),size=(100,40))
        BackButton.Bind(wx.EVT_BUTTON,partial(self.ElfToMainBack,t1=pt1,t2=pt2,errormsg=perrormsg))
        self.emplpnl.Show()
        self.emplpnl.Bind(wx.EVT_PAINT, partial(self.OnPaint,op=self.emplpnl))


    def NewconForm(self,e):
        self.ncpnl.Hide()
        self.formpnl=NewPanel(self)
        #self.formpnl.SetBackgroundColour("green")
        l0 = wx.StaticText(self.formpnl, -1, " New Connection Form  ",pos=(450,15),size=(500,500),style=wx.ALIGN_CENTER)
        l0.SetFont(wx.Font(15, wx.MODERN, wx.NORMAL, wx.BOLD))

        l1 = wx.StaticText(self.formpnl, -1, " Name of Applicant    :   ",pos=(100,100))
        t11 = wx.TextCtrl(self.formpnl,style= wx.TE_PROCESS_ENTER,    pos=(350,100),size=(200,30))
        l2 = wx.StaticText(self.formpnl, -1, " Father's Name        :   ",pos=(100,150))
        t12 = wx.TextCtrl(self.formpnl,style= wx.TE_PROCESS_ENTER,    pos=(350,150),size=(200,30))
        l3 = wx.StaticText(self.formpnl, -1, " Installation Address :   ",pos=(100,200))
        t13 = wx.TextCtrl(self.formpnl,style= wx.TE_PROCESS_ENTER,    pos=(350,200),size=(200,30))
        l5 = wx.StaticText(self.formpnl, -1, " Mobile No.           :   ",pos=(100,250))
        t14 = wx.TextCtrl(self.formpnl,style= wx.TE_PROCESS_ENTER,    pos=(350,250),size=(200,30))


        l6 = wx.StaticText(self.formpnl, -1, " Email                :   ",pos=(100,300))
        t15 = wx.TextCtrl(self.formpnl,style= wx.TE_PROCESS_ENTER,    pos=(350,300),size=(200,30))
        l7 = wx.StaticText(self.formpnl, -1, " Purpose of Supply    :   ",pos=(100,350))
        #t16 = wx.TextCtrl(self.formpnl,style= wx.TE_PROCESS_ENTER,    pos=(350,350),size=(200,30))
        divList=list()
        divList.append("Domestic")
        divList.append("Commercial")
        divList.append("Industrial")

        self.ps=wx.ComboBox(self.formpnl,pos=(350,350),size=(200,30),choices=divList)
        self.ps.Bind(wx.EVT_COMBOBOX, self.posu)
        l8 = wx.StaticText(self.formpnl, -1, " City    :   ",              pos=(100,400))
        t17 = wx.TextCtrl(self.formpnl,style= wx.TE_PROCESS_ENTER,    pos=(350,400),size=(200,30))
        msg=wx.StaticText(self.formpnl, -1, "",pos=(620,300),size=(300,300))
        SubmitButton = wx.Button(self.formpnl, label='Submit and Email Acknowledgement', pos=(350, 465),size=(300,35))
        SubmitButton.Bind(wx.EVT_BUTTON,partial(self.Submit,t11=t11,t12=t12,t13=t13,t14=t14,t15=t15,t17=t17,msg=msg))
        idButton = wx.Button(self.formpnl, label='chose file', pos=(700, 400),size=(100,30))
        idButton.Bind(wx.EVT_BUTTON,self.upload)
        backButton = wx.Button(self.formpnl, label='Cancel', pos=(1000, 10))
        self.p1=self.formpnl
        self.p2=self.homepnl
        backButton.Bind(wx.EVT_BUTTON, self.Cancel)
        #self.formpnl.Bind(wx.EVT_PAINT, partial(self.OnPaint2,op=self.formpnl))

    def OnPaint2(self,e,op):
        dc = wx.PaintDC(op)
        dc.SetBrush(wx.Brush(wx.Colour(255,255,255)))
        dc.DrawRectangle(10, 10, 1346, 500)
        dc.SetBrush(wx.Brush(wx.Colour(220,217,217)))
        dc.DrawRectangle(50, 70, 1280,380)

    def upload(self,e):
        frame = wx.Frame(None, -1, 'win.py')
        frame.SetDimensions(0,0,200,50)
        dialog=wx.FileDialog(frame, "Open", "", "", "Python files (*.py)|*.py",  wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if dialog.ShowModal() == wx.ID_OK:
            print (dialog.GetPath())


    def posu(self,e):
        self.t16=e.GetString()

    def Submit(self,e,t11,t12,t13,t14,t15,t17,msg):
        if(t11.GetValue() and t12.GetValue() and t13.GetValue() and len(t14.GetValue())==10 and t15.GetValue() and self.t16 ):
            cur = con.cursor(mdb.cursors.DictCursor)
            cur.execute("select boardname from consumer where state=%s",(self.state,))
            rows=cur.fetchall()
            cur = con.cursor()
            characters = string.ascii_letters + string.digits
            reference_id="".join(choice(characters) for x in range(randint(8,10)))

            cur.execute("select max(cid) from consumer")
            c=cur.fetchall()
            cid=c[0][0]

            cur.execute("select max(cid) from newconnection")
            cc=cur.fetchall()
            cidd=cc[0][0]
            boardname=rows[0]['boardname']
            if cid>=cidd:
            	ciid=cid+1
            else:
            	ciid=cidd+1

            try:
                cur.execute("insert into newconnection values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(t11.GetValue(),t14.GetValue(),rows[0]['boardname'],self.state,self.Subdiv,self.Div,t17.GetValue(),t15.GetValue(),t13.GetValue(),reference_id,ciid,))
                con.commit()
            except (mdb.Error,e):
                print(e)
                """if 'errorpnl' in locals():
                    errorpnl.Hide()
                errorpnl=wx.Panel(self,pos=(w/2,300),size=(300,20))
                errorpnl.SetBackgroundColour("white")
                """
                """msg.Hide()
                msg.Show()
                msg.SetLabel("Invalid Mobile No. !!")
                msg.SetForegroundColour((255,0,0))"""
                wx.MessageBox(message="Invalid Mobile no. !!",caption='Info',style=wx.OK | wx.ICON_INFORMATION)



                return

            status="pending"
            cur.execute("insert into ncstatus values (%s,%s,%s)",(ciid,reference_id,status,))
            con.commit()

            #self.p1=self.formpnl
            #self.p2=self.homepnl
            #msg='\n Succesfuly Submitted !! Your reference no. is ' + self.reference_id
            #wx.MessageBox(message=msg,caption='Info',style=wx.OK | wx.ICON_INFORMATION)
            #self.back(self,p1=self.formpnl,p2=self.homepnl,title="Power Distribution System")
            self.email(reference_id=reference_id,boardname=boardname,t11=t11,t12=t12,t13=t13,t14=t14,t15=t15,t17=t17)

        else:
            if(t11.GetValue() and t12.GetValue() and t13.GetValue() and len(t14.GetValue())!=10 and t15.GetValue() and self.t16 ):
                """msg.Hide()
                msg.Show()
                msg.SetLabel("Invalid Mobile no. !!")
                msg.SetForegroundColour((255,0,0))"""
                wx.MessageBox(message="Invalid Mobile no. !!",caption='Info',style=wx.OK | wx.ICON_INFORMATION)
            else:
                """msg.Hide()
                msg.Show()
                msg.SetLabel("Any field can not be empty !!")
                msg.SetForegroundColour((255,0,0))"""
                wx.MessageBox(message="Any field can not be empty !!",caption='Info',style=wx.OK | wx.ICON_INFORMATION)

    def email(self,reference_id,boardname,t11,t12,t13,t14,t15,t17):
        me = "firozmohd139@gmail.com"
        my_password = "Firoz@098"
        you = t15.GetValue()

        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Alert"
        msg['From'] = me
        msg['To'] = you

        html ="""
        <html>
            <body>
                <h1>{bname}</h1>
                <h2>Hi {name}</h2>
                <h2>Reference Id : {refid}</h2>
                <p>Father name : {fname}</p>  <br>
                <p>Installation Address : {add}</p>  <br>
                <p>Phone no. : {pno}</p>  <br>
                <p>E-mail : {email}</p>  <br>
                <p>Purpose of supply : {pos}</p>  <br>
                <p>City : {city}</p>  <br>
            </body>
        </html>
        """.format(bname=boardname,name=t11.GetValue(),refid=reference_id,fname=t12.GetValue(),add=t13.GetValue(),pno=str(t14.GetValue()),email=t15.GetValue(),pos=self.t16,city=t17.GetValue())
        mail = MIMEText(html, 'html')
        msg.attach(mail)
        s = smtplib.SMTP_SSL('smtp.gmail.com',465)
        s.login(me, my_password)
        try :
            s.sendmail(me, you, msg.as_string())
            s.quit()
            msgg='\n Succesfuly Submitted !! Your reference no. is ' + reference_id
            wx.MessageBox(message=msgg,caption='Info',style=wx.OK | wx.ICON_INFORMATION)
            self.back(self,p1=self.formpnl,p2=self.homepnl,title="Power Distribution System")
        except :
            msgg='\nInvalid Email id'
            wx.MessageBox(message=msgg,caption='Info',style=wx.OK | wx.ICON_INFORMATION)

        #self.back(self,p1=self.ackpnl,p2=self.homepnl,title="Power Distribution System")


    def Cancel(self,e):
        dial=wx.MessageBox(message='Do you want to cancel it?',caption='Cancel',style=wx.YES_NO | wx.ICON_INFORMATION)
        #self.p1=self.formpnl
        #self.p2=self.homepnl
        if (dial==2):
            #self.back(self)

            self.back(self,p1=self.formpnl,p2=self.homepnl,title="Power Distribution System")
    def UserProfile(self,e,t1):
        #self.p1=self.uppnl
    	#self.p2=self.custpnl
        #self.uppnl.SetBackgroundColour("blue")
        self.custpnl.Hide()
        self.SetTitle("Profile")
        self.uppnl=NewPanel(self)
        cur.execute("select cid,cname,phone,email,address from consumer where cid=%s",(t1.GetValue(),))
        rows=cur.fetchall()
        l1=wx.StaticText(self.uppnl, -1, rows[0][1]+"'s Profile",pos=(220,10),size=(1000,1000),style=wx.ALIGN_CENTER)
        l1.SetFont(wx.Font(18, wx.MODERN, wx.NORMAL, wx.BOLD))
        l2 = wx.StaticText(self.uppnl, -1, "Consumer ID :   "+str(rows[0][0]),pos=(50,50),size=(1000,1000))
        l3 = wx.StaticText(self.uppnl, -1, "Name        :   "+rows[0][1],     pos=(50,100),size=(1000,1000))
        l4 = wx.StaticText(self.uppnl, -1, "Phone Number:   "+str(rows[0][2]),pos=(50,150),size=(1000,1000))
        l5 = wx.StaticText(self.uppnl, -1, "Email ID    :   "+rows[0][3],     pos=(50,200),size=(1000,1000))
        l6 = wx.StaticText(self.uppnl, -1, "Address     :   "+rows[0][4],     pos=(50,250),size=(1000,1000))
        l2.SetFont(wx.Font(13, wx.MODERN, wx.NORMAL, wx.NORMAL))
        l3.SetFont(wx.Font(13, wx.MODERN, wx.NORMAL, wx.NORMAL))
        l4.SetFont(wx.Font(13, wx.MODERN, wx.NORMAL, wx.NORMAL))
        l5.SetFont(wx.Font(13, wx.MODERN, wx.NORMAL, wx.NORMAL))
        l6.SetFont(wx.Font(13, wx.MODERN, wx.NORMAL, wx.NORMAL))
        BackButton = wx.Button(self.uppnl, label='Back', pos=(1000, 15),size=(100,40))
        BackButton.Bind(wx.EVT_BUTTON,partial(self.back,p1=self.uppnl,p2=self.custpnl,title="User"))
        self.uppnl.Show()

    def EmpProfile(self,e,t1,t2):
        self.emppnl.Hide()
        self.SetTitle("Profile")
        self.epnl=NewPanel(self)
        cur.execute("select * from employee where eid=%s",(t1.GetValue(),))
        rows=cur.fetchall()
        l1=wx.StaticText(self.epnl, -1, rows[0][1]+"'s Profile",pos=(210,20),size=(1000,1000),style=wx.ALIGN_CENTER)
        l1.SetFont(wx.Font(18, wx.MODERN, wx.NORMAL, wx.BOLD))
        l2 = wx.StaticText(self.epnl, -1, "Employee ID       :   "+str(rows[0][0]),      pos=(50,50),size=(1000,1000))
        l3 = wx.StaticText(self.epnl, -1, "Name              :   "+rows[0][1],           pos=(50,100),size=(1000,1000))
        l4 = wx.StaticText(self.epnl, -1, "Departmet         :   "+rows[0][4],           pos=(50,150),size=(1000,1000))
        l5 = wx.StaticText(self.epnl, -1, "Designation       :   "+rows[0][7],           pos=(50,200),size=(1000,1000))
        l6 = wx.StaticText(self.epnl, -1, "Elect. board name :   "+rows[0][6],           pos=(50,250),size=(1000,1000))
        l7 = wx.StaticText(self.epnl, -1, "Date of Jioning   :   "+str(rows[0][2]),      pos=(50,300),size=(1000,1000))
        l8 = wx.StaticText(self.epnl, -1, "Phone no.         :   "+str(rows[0][8]),       pos=(50,350),size=(1000,1000))
        l9 = wx.StaticText(self.epnl, -1, "Date of birth     :   "+str(rows[0][3]),      pos=(50,400),size=(1000,1000))
        l2.SetFont(wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL))
        l3.SetFont(wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL))
        l4.SetFont(wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL))
        l5.SetFont(wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL))
        l6.SetFont(wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL))
        l7.SetFont(wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL))
        l8.SetFont(wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL))
        l9.SetFont(wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL))

        BackButton = wx.Button(self.epnl, label='Back', pos=(1000, 15),size=(100,40))
        BackButton.Bind(wx.EVT_BUTTON,partial(self.back,p1=self.epnl,p2=self.emppnl,title="Employee"))
    	#self.uppnl.SetBackgroundColour("blue")
    	#self.uppnl.Show()


    def Login(self,e,t1,t2,errormsg):
        if(t1.GetValue()):
            cur.execute("select password from consumer where cid=%s",(t1.GetValue(),))
            rows = cur.fetchall()
            if(len(rows)!=0 and t2.GetValue()==rows[0][0]):
                self.Customer(self,t1=t1,t2=t2,errormsg=errormsg)
            else:
                errormsg.Hide()
                errormsg.Show()
                errormsg.SetForegroundColour((255,0,0))
                errormsg.SetLabel("Wrong Customer ID or Password!!")
        else:
            errormsg.Hide()
            errormsg.Show()
            errormsg.SetForegroundColour((255,0,0))
            errormsg.SetLabel("Wrong Customer ID or Password!!")


    def EmpLogin(self,e,t1,t2,errormsg):
        if(t1.GetValue()):
            cur.execute("select password from employee where eid=%s",(t1.GetValue(),))
            rows = cur.fetchall()
            if(len(rows)!=0 and t2.GetValue()==rows[0][0]):
                cur.execute("select designation from employee where eid=%s",(t1.GetValue(),))
                eboard=cur.fetchall()
                if(eboard[0][0]=='designation6'):
                    self.XXEmployee(self,t1=t1,t2=t2,errormsg=errormsg)
                if(eboard[0][0]=='designation3'):
                    self.designation3(self,t1=t1,t2=t2,errormsg=errormsg)
                if(eboard[0][0]=='designation1'):
                    self.designation1(self,t1=t1,t2=t2,errormsg=errormsg)

            else:
                errormsg.SetForegroundColour((255,0,0))
                errormsg.SetLabel("Wrong Employee ID or Password!!")
        else:
            errormsg.SetForegroundColour((255,0,0))
            errormsg.SetLabel("Wrong Employee ID or Password!!")

    def designation1(self,e,t1,t2,errormsg):    #updating user data
        self.emplpnl.Hide()
        self.emppnl=NewPanel(self)

        self.SetTitle("Employee")
        LogoutButton = wx.Button(self.emppnl, label='Logout', pos=(1270, 20),size=(80,30))
        LogoutButton.Bind(wx.EVT_BUTTON,partial(self.EmpLogout,t1=t1,t2=t2,errormsg=errormsg))
        cur.execute("select ename from employee where eid=%s",(t1.GetValue(),))
        rows=cur.fetchall()
        ProfileButton = wx.Button(self.emppnl, label='Hi '+rows[0][0], pos=(1120, 20))
        ProfileButton.Bind(wx.EVT_BUTTON,partial(self.EmpProfile,t1=t1,t2=t2))

        l1=wx.StaticText(self.emppnl, -1,"Consumer No.  :",pos=(w/2-160,115),size=(300,30))
        l1.SetFont(wx.Font(12,wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

        consNo = wx.TextCtrl(self.emppnl,style= wx.TE_PROCESS_ENTER,    pos=(w/2,110),size=(200,30))
        SubmitButton = wx.Button(self.emppnl, label='Submit', pos=(w/2, 180),size=(100,35))
        SubmitButton.Bind(wx.EVT_BUTTON,partial(self.updateConsumer,consNo=consNo))

    def updateConsumer(self,e,consNo):
        if(consNo.GetValue()):
            self.emppnl.Hide()
            self.editConpnl=NewPanel(self)
            cur=con.cursor(mdb.cursors.DictCursor)
            try:
                cur.execute("select * from consumer where cid = {}".format(consNo.GetValue()))
            except (mdb.Error,e):
                print (e)
                msg='\n Error'
                wx.MessageBox(message=msg,caption='Info',style=wx.OK | wx.ICON_INFORMATION)
                self.editConpnl.Hide()
                self.emppnl.Show()
            rows=cur.fetchall()
            print (rows)
            if(len(rows)==0):
                self.editConpnl.Hide()
                self.emppnl.Show()

            BackButton=wx.Button(self.editConpnl, label='Back' , pos=(1000,15),size=(100,40))
            BackButton.Bind(wx.EVT_BUTTON,partial(self.back,p1=self.editConpnl,p2=self.emppnl,title='Employee'))
            l1=wx.StaticText(self.editConpnl, -1,"Consumer No:",pos=(120,120),size=(300,30))
            l2 = wx.StaticText(self.editConpnl,-1,str(rows[0]['cid']) ,  pos=(320,115),size=(200,30))

            l3=wx.StaticText(self.editConpnl, -1,"Name :",pos=(120,170),size=(300,30))
            self.conName = wx.TextCtrl(self.editConpnl,style= wx.TE_PROCESS_ENTER,    pos=(320,165),size=(300,30))
            self.conName.AppendText(rows[0]['cname'])

            l3=wx.StaticText(self.editConpnl, -1,"Mobile No. :",pos=(120,220),size=(300,30))
            self.conPhone = wx.TextCtrl(self.editConpnl,style= wx.TE_PROCESS_ENTER,    pos=(320,215),size=(300,30))
            self.conPhone.AppendText(str(rows[0]['phone']))

            l4=wx.StaticText(self.editConpnl, -1,"Email      :",pos=(120,270),size=(300,30))
            self.conEmail = wx.TextCtrl(self.editConpnl,style= wx.TE_PROCESS_ENTER,    pos=(320,265),size=(300,30))
            self.conEmail.AppendText(rows[0]['email'])

            l5=wx.StaticText(self.editConpnl, -1,"Address    :",pos=(120,320),size=(300,30))
            self.conAddr = wx.TextCtrl(self.editConpnl,style= wx.TE_PROCESS_ENTER,    pos=(320,315),size=(300,30))
            self.conAddr.AppendText(rows[0]['address'])

            l6=wx.StaticText(self.editConpnl, -1,"password   :",pos=(120,370),size=(300,30))
            self.conPass = wx.TextCtrl(self.editConpnl,style= wx.TE_PROCESS_ENTER,    pos=(320,365),size=(300,30))
            self.conPass.AppendText(rows[0]['password'])

            updateButton=wx.Button(self.editConpnl, label='Update',pos=(500, 450),size=(100,40))
            updateButton.Bind(wx.EVT_BUTTON,self.updateConSubmit)
            self.errorPcUpdate=wx.StaticText(self.editConpnl,-1,"" ,pos=(700,200),size=(400,50))

    def updateConSubmit(self,e):
        if(self.conName.GetValue() and self.conPhone.GetValue() and self.conEmail.GetValue() and self.conAddr.GetValue() and self.conPass.GetValue()):
            cur = con.cursor(mdb.cursors.DictCursor)
            cur.execute("select * from consumer")
            rows=cur.fetchall()
            # print(rows[0]['cid'])
            try:
                cur.execute("update consumer set cname=%s,phone=%s,email=%s,address=%s,password=%s  where cid =%s",(self.conName.GetValue(),str(self.conPhone.GetValue()),self.conEmail.GetValue(),self.conAddr.GetValue(),self.conPass.GetValue(),rows[0]['cid']))
            except (mdb.Error,e):
                print ("Error:%s" % (e.args[1]))
                msg=e.args[1]
                wx.MessageBox(message=msg,caption='Info',style=wx.OK | wx.ICON_INFORMATION)
                return
            con.commit()
            self.editConpnl.Hide()
            self.emppnl.Show()

        else:
            self.errorDcUpdate.SetLabel("Please, Fill all the data")
            self.errorDcUpdate.SetForegroundColour((255,0,0))
            # self.designation1(self)
            # self.conSubmitpnl=NewPanel(self)




    def designation3(self,e,t1,t2,errormsg):
        self.emplpnl.Hide()
        self.emppnl=NewPanel(self)

        self.SetTitle("Employee")

        LogoutButton = wx.Button(self.emppnl, label='Logout', pos=(1270, 20),size=(80,35))
        LogoutButton.Bind(wx.EVT_BUTTON,partial(self.EmpLogout,t1=t1,t2=t2,errormsg=errormsg))
        cur.execute("select ename from employee where eid=%s",(t1.GetValue(),))
        rows=cur.fetchall()
        ProfileButton = wx.Button(self.emppnl, label='Hi '+rows[0][0], pos=(1100, 20),size=(150,35))
        ProfileButton.Bind(wx.EVT_BUTTON,partial(self.EmpProfile,t1=t1,t2=t2))

        l1=wx.StaticText(self.emppnl, -1,"Distribution Company",pos=(80,30),size=(300,30))
        l1.SetFont(wx.Font(12,wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

        l1Add=wx.Button(self.emppnl, label='ADD', pos=(70,80),size=(100,40))
        l1Add.Bind(wx.EVT_BUTTON,self.addDc)
        l1Update=wx.Button(self.emppnl, label='UPDATE', pos=(200,80),size=(100,40))
        l1Update.Bind(wx.EVT_BUTTON,self.updateDc)
        l1Delete=wx.Button(self.emppnl, label='DELETE', pos=(330,80),size=(100,40))
        l1Delete.Bind(wx.EVT_BUTTON,self.DelDc)

        l1=wx.StaticText(self.emppnl, -1,"Transmission Company",pos=(80,150),size=(300,30))
        l1.SetFont(wx.Font(12,wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

        l2Add=wx.Button(self.emppnl, label='ADD', pos=(70,200),size=(100,40))
        l2Add.Bind(wx.EVT_BUTTON,self.addTc)
        l2Update=wx.Button(self.emppnl, label='UPDATE', pos=(200,200),size=(100,40))
        l2Update.Bind(wx.EVT_BUTTON,self.updateTc)
        l2Delete=wx.Button(self.emppnl, label='DELETE', pos=(330,200),size=(100,40))
        l2Delete.Bind(wx.EVT_BUTTON,self.DelTc)

        l3=wx.StaticText(self.emppnl, -1,"Power Company",pos=(80,270),size=(300,30))
        l3.SetFont(wx.Font(12,wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

        l3Add=wx.Button(self.emppnl, label='ADD', pos=(70,320),size=(100,40))
        l3Add.Bind(wx.EVT_BUTTON,self.addPc)
        l3Update=wx.Button(self.emppnl, label='UPDATE', pos=(200,320),size=(100,40))
        l3Update.Bind(wx.EVT_BUTTON,self.updatePc)
        l3Delete=wx.Button(self.emppnl, label='DELETE', pos=(330,320),size=(100,40))
        l3Delete.Bind(wx.EVT_BUTTON,self.DelPc)

    def updateDc(self,e):
        self.emppnl.Hide()
        self.updatepnl=NewPanel(self)
        updateDcBackButton=wx.Button(self.updatepnl, label='Back' , pos=(1000,15),size=(100,40))
        updateDcBackButton.Bind(wx.EVT_BUTTON,partial(self.back,p1=self.updatepnl,p2=self.emppnl,title='Employee'))
        l0=wx.StaticText(self.updatepnl,-1,"Did",pos=(80,80),size=(500,500))
        l0.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD))
        l1=wx.StaticText(self.updatepnl, -1,"Name",pos=(150,80),size=(500,500))
        l1.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD))
        l2=wx.StaticText(self.updatepnl, -1,"State",pos=(450,80),size=(500,500))
        l2.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD))
        l3=wx.StaticText(self.updatepnl, -1,"Tenure(in years)",pos=(580,80),size=(500,500))
        l3.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD))
        l4=wx.StaticText(self.updatepnl, -1,"Tid",pos=(750,80),size=(500,500))
        l4.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD))
        cur=con.cursor(mdb.cursors.DictCursor)
        cur.execute("select * from distributioncompany")
        self.rows=cur.fetchall()
        i=120
        j=0
        for row in self.rows:
            wx.StaticText(self.updatepnl, -1,str(row['did']),pos=(80,i))
            wx.StaticText(self.updatepnl, -1,row['dname'],pos=(150,i))
            wx.StaticText(self.updatepnl, -1,row['state'],pos=(450,i))
            wx.StaticText(self.updatepnl, -1,str(row['tenure']),pos=(650,i))
            wx.StaticText(self.updatepnl, -1,str(row['tid']),pos=(750,i))
            editButton = wx.Button(self.updatepnl, label='Edit', pos=(850, i),size=(100,20))
            editButton.Bind(wx.EVT_BUTTON,self.editDcButton,editButton)
            editButton.id=j
            j=j+1
            i=i+30

    def updateTc(self,e):
        self.emppnl.Hide()
        self.updatepnl=NewPanel(self)
        updateTcBackButton=wx.Button(self.updatepnl, label='Back' , pos=(1000,15),size=(100,40))
        updateTcBackButton.Bind(wx.EVT_BUTTON,partial(self.back,p1=self.updatepnl,p2=self.emppnl,title='Employee'))
        l0=wx.StaticText(self.updatepnl,-1,"Tid",pos=(80,80),size=(500,500))
        l0.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD))
        l1=wx.StaticText(self.updatepnl, -1,"Name",pos=(150,80),size=(500,500))
        l1.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD))
        l2=wx.StaticText(self.updatepnl, -1,"State",pos=(300,80),size=(500,500))
        l2.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD))
        l3=wx.StaticText(self.updatepnl, -1,"Did",pos=(500,80),size=(500,500))
        l3.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD))
        l4=wx.StaticText(self.updatepnl, -1,"Tcapacity",pos=(600,80),size=(500,500))
        l4.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD))
        l5=wx.StaticText(self.updatepnl, -1,"Tenure(in years)",pos=(700,80),size=(500,500))
        l5.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD))
        cur=con.cursor(mdb.cursors.DictCursor)
        cur.execute("select * from transmissioncompany")
        self.rows=cur.fetchall()
        i=120
        j=0
        for row in self.rows:
            wx.StaticText(self.updatepnl, -1,str(row['tid']),pos=(80,i))
            wx.StaticText(self.updatepnl, -1,row['tname'],pos=(150,i))
            wx.StaticText(self.updatepnl, -1,row['state'],pos=(300,i))
            wx.StaticText(self.updatepnl, -1,str(row['did']),pos=(500,i))
            wx.StaticText(self.updatepnl, -1,str(row['tcapacity']),pos=(600,i))
            wx.StaticText(self.updatepnl, -1,str(row['tenure']),pos=(750,i))
            editButton = wx.Button(self.updatepnl, label='Edit', pos=(850, i),size=(100,20))
            editButton.Bind(wx.EVT_BUTTON,self.editTcButton,editButton)
            editButton.id=j
            j=j+1
            i=i+30

    def updatePc(self,e):
        self.emppnl.Hide()
        self.updatepnl=NewPanel(self)
        updateTcBackButton=wx.Button(self.updatepnl, label='Back' , pos=(1000,15),size=(100,40))
        updateTcBackButton.Bind(wx.EVT_BUTTON,partial(self.back,p1=self.updatepnl,p2=self.emppnl,title='Employee'))
        l0=wx.StaticText(self.updatepnl,-1,"Pid",pos=(80,80),size=(500,500))
        l0.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD))
        l1=wx.StaticText(self.updatepnl, -1,"Name",pos=(150,80),size=(500,500))
        l1.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD))
        l2=wx.StaticText(self.updatepnl, -1,"State",pos=(300,80),size=(500,500))
        l2.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD))
        l3=wx.StaticText(self.updatepnl, -1,"Type",pos=(500,80),size=(500,500))
        l3.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD))
        l4=wx.StaticText(self.updatepnl, -1,"Total Power",pos=(600,80),size=(500,500))
        l4.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD))
        cur=con.cursor(mdb.cursors.DictCursor)
        cur.execute("select * from powercompany")
        self.rows=cur.fetchall()
        i=120
        j=0
        for row in self.rows:
            wx.StaticText(self.updatepnl, -1,str(row['pid']),pos=(80,i))
            wx.StaticText(self.updatepnl, -1,row['pname'],pos=(150,i))
            wx.StaticText(self.updatepnl, -1,row['state'],pos=(300,i))
            wx.StaticText(self.updatepnl, -1,row['type'],pos=(500,i))
            wx.StaticText(self.updatepnl, -1,str(row['totalpower']),pos=(600,i))
            editButton = wx.Button(self.updatepnl, label='Edit', pos=(750, i),size=(100,20))
            editButton.Bind(wx.EVT_BUTTON,self.editPcButton,editButton)
            editButton.id=j
            j=j+1
            i=i+30


    def editDcButton(self,e,):
        self.updatepnl.Hide()
        self.editDcpnl=NewPanel(self)
        self.idDc=e.GetEventObject().id
        cur=con.cursor(mdb.cursors.DictCursor)
        cur.execute("select * from distributioncompany")
        rows=cur.fetchall()
        editDcBackButton=wx.Button(self.editDcpnl, label='Back' , pos=(1000,15),size=(100,40))
        editDcBackButton.Bind(wx.EVT_BUTTON,partial(self.back,p1=self.editDcpnl,p2=self.updatepnl,title='Employee'))
        l1=wx.StaticText(self.editDcpnl, -1,"Did :",pos=(120,120),size=(300,30))
        l2 = wx.StaticText(self.editDcpnl,-1, str(rows[self.idDc]['did']) ,  pos=(320,115),size=(200,30))
        l3=wx.StaticText(self.editDcpnl, -1,"Dname :",pos=(120,170),size=(300,30))
        self.tDcDname = wx.TextCtrl(self.editDcpnl,style= wx.TE_PROCESS_ENTER,    pos=(320,165),size=(300,30))
        self.tDcDname.AppendText(rows[self.idDc]['dname'])
        l4=wx.StaticText(self.editDcpnl, -1,"State :",pos=(120,220),size=(300,30))
        self.tDcState = wx.TextCtrl(self.editDcpnl,style= wx.TE_PROCESS_ENTER,    pos=(320,215),size=(300,30))
        self.tDcState.AppendText(rows[self.idDc]['state'])
        l5=wx.StaticText(self.editDcpnl, -1,"Tenure(in years) :",pos=(120,270),size=(300,30))
        self.tDcTenure = wx.TextCtrl(self.editDcpnl,style= wx.TE_PROCESS_ENTER,    pos=(320,265),size=(300,30))
        self.tDcTenure.AppendText(str(rows[self.idDc]['tenure']))
        l6=wx.StaticText(self.editDcpnl, -1,"Tid :",pos=(120,320),size=(300,30))
        self.tDcTid = wx.TextCtrl(self.editDcpnl,style= wx.TE_PROCESS_ENTER,    pos=(320,315),size=(300,30))
        self.tDcTid.AppendText(str(rows[self.idDc]['tid']))
        updateButton=wx.Button(self.editDcpnl, label='Update',pos=(500, 450),size=(100,40))
        updateButton.Bind(wx.EVT_BUTTON,self.updateDcSubmit)
        self.errorDcUpdate=wx.StaticText(self.editDcpnl,-1,"" ,pos=(700,200),size=(400,50))

    def editTcButton(self,e):
        self.updatepnl.Hide()
        self.editTcpnl=NewPanel(self)
        self.idTc=e.GetEventObject().id
        cur=con.cursor(mdb.cursors.DictCursor)
        cur.execute("select * from transmissioncompany")
        rows=cur.fetchall()
        editTcBackButton=wx.Button(self.editTcpnl, label='Back' , pos=(1000,15),size=(100,40))
        editTcBackButton.Bind(wx.EVT_BUTTON,partial(self.back,p1=self.editTcpnl,p2=self.updatepnl,title='Employee'))
        l1=wx.StaticText(self.editTcpnl, -1,"Tid :",pos=(120,120),size=(300,30))
        l2 = wx.StaticText(self.editTcpnl,-1, str(rows[self.idTc]['tid']) ,  pos=(320,115),size=(200,30))
        l3=wx.StaticText(self.editTcpnl, -1,"Tname :",pos=(120,170),size=(300,30))
        self.tTcTname = wx.TextCtrl(self.editTcpnl,style= wx.TE_PROCESS_ENTER,    pos=(320,165),size=(300,30))
        self.tTcTname.AppendText(rows[self.idTc]['tname'])
        l4=wx.StaticText(self.editTcpnl, -1,"State :",pos=(120,220),size=(300,30))
        self.tTcState = wx.TextCtrl(self.editTcpnl,style= wx.TE_PROCESS_ENTER,    pos=(320,215),size=(300,30))
        self.tTcState.AppendText(rows[self.idTc]['state'])
        l5=wx.StaticText(self.editTcpnl, -1,"Did :",pos=(120,270),size=(300,30))
        self.tTcDid = wx.TextCtrl(self.editTcpnl,style= wx.TE_PROCESS_ENTER,    pos=(320,265),size=(300,30))
        self.tTcDid.AppendText(str(rows[self.idTc]['did']))
        l6=wx.StaticText(self.editTcpnl, -1,"Tcapacity :",pos=(120,320),size=(300,30))
        self.tTcTcapacity = wx.TextCtrl(self.editTcpnl,style= wx.TE_PROCESS_ENTER,    pos=(320,315),size=(300,30))
        self.tTcTcapacity.AppendText(str(rows[self.idTc]['tcapacity']))
        l6=wx.StaticText(self.editTcpnl, -1,"Tenure(in years) :",pos=(120,370),size=(300,30))
        self.tTcTenure = wx.TextCtrl(self.editTcpnl,style= wx.TE_PROCESS_ENTER,    pos=(320,365),size=(300,30))
        self.tTcTenure.AppendText(str(rows[self.idTc]['tenure']))
        updateButton=wx.Button(self.editTcpnl, label='Update',pos=(500, 450),size=(100,40))
        updateButton.Bind(wx.EVT_BUTTON,self.updateTcSubmit)
        self.errorTcUpdate=wx.StaticText(self.editTcpnl,-1,"" ,pos=(700,200),size=(400,50))

    def editPcButton(self,e):
        self.updatepnl.Hide()
        self.editPcpnl=NewPanel(self)
        self.idPc=e.GetEventObject().id
        cur=con.cursor(mdb.cursors.DictCursor)
        cur.execute("select * from powercompany")
        rows=cur.fetchall()
        editPcBackButton=wx.Button(self.editPcpnl, label='Back' , pos=(1000,15),size=(100,40))
        editPcBackButton.Bind(wx.EVT_BUTTON,partial(self.back,p1=self.editPcpnl,p2=self.updatepnl,title='Employee'))
        l1=wx.StaticText(self.editPcpnl, -1,"Pid :",pos=(120,120),size=(300,30))
        l2 = wx.StaticText(self.editPcpnl,-1, str(rows[self.idPc]['pid']) ,  pos=(320,115),size=(200,30))
        l3=wx.StaticText(self.editPcpnl, -1,"Pname :",pos=(120,170),size=(300,30))
        self.tPcPname = wx.TextCtrl(self.editPcpnl,style= wx.TE_PROCESS_ENTER,    pos=(320,165),size=(300,30))
        self.tPcPname.AppendText(rows[self.idPc]['pname'])
        l4=wx.StaticText(self.editPcpnl, -1,"State :",pos=(120,220),size=(300,30))
        self.tPcState = wx.TextCtrl(self.editPcpnl,style= wx.TE_PROCESS_ENTER,    pos=(320,215),size=(300,30))
        self.tPcState.AppendText(rows[self.idPc]['state'])
        l5=wx.StaticText(self.editPcpnl, -1,"Type :",pos=(120,270),size=(300,30))
        self.tPcType = wx.TextCtrl(self.editPcpnl,style= wx.TE_PROCESS_ENTER,    pos=(320,265),size=(300,30))
        self.tPcType.AppendText(rows[self.idPc]['type'])
        l6=wx.StaticText(self.editPcpnl, -1,"Total Power :",pos=(120,320),size=(300,30))
        self.tPcTotalpower = wx.TextCtrl(self.editPcpnl,style= wx.TE_PROCESS_ENTER,    pos=(320,315),size=(300,30))
        self.tPcTotalpower.AppendText(str(rows[self.idPc]['totalpower']))
        updateButton=wx.Button(self.editPcpnl, label='Update',pos=(500, 450),size=(100,40))
        updateButton.Bind(wx.EVT_BUTTON,self.updatePcSubmit)
        self.errorPcUpdate=wx.StaticText(self.editPcpnl,-1,"" ,pos=(700,200),size=(400,50))

    def updateDcSubmit(self,e):
        if(self.tDcDname.GetValue() and self.tDcState.GetValue() and self.tDcTenure.GetValue() and self.tDcTid.GetValue()):
            cur = con.cursor(mdb.cursors.DictCursor)
            cur.execute("select * from distributioncompany")
            rows=cur.fetchall()
            try:
                cur.execute("update distributioncompany set dname=%s,state=%s,tenure=%s,tid=%s  where did =%s",(self.tDcDname.GetValue(),self.tDcState.GetValue(),str(self.tDcTenure.GetValue()),str(self.tDcTid.GetValue()),rows[self.idDc]['did']))
            except (mdb.Error,e):
                print ("Error:%s" % (e.args[1]))
                msg=e.args[1]
                wx.MessageBox(message=msg,caption='Info',style=wx.OK | wx.ICON_INFORMATION)
                return
            con.commit()
            self.editDcpnl.Hide()
            self.updateDc(self)
        else:
            self.errorDcUpdate.SetLabel("Please, Fill all the data")
            self.errorDcUpdate.SetForegroundColour((255,0,0))


    def updateTcSubmit(self,e):
        if(self.tTcTname.GetValue() and self.tTcState.GetValue() and self.tTcDid.GetValue() and self.tTcTcapacity.GetValue() and self.tTcTenure.GetValue()):
            cur = con.cursor(mdb.cursors.DictCursor)
            cur.execute("select * from transmissioncompany")
            rows=cur.fetchall()
            try:
                cur.execute("update transmissioncompany set tname=%s,state=%s,did=%s,tcapacity=%s,tenure=%s  where tid =%s",(self.tTcTname.GetValue(),self.tTcState.GetValue(),str(self.tTcDid.GetValue()),str(self.tTcTcapacity.GetValue()),str(self.tTcTenure.GetValue()),rows[self.idTc]['tid']))
            except (mdb.Error,e):
                print ("Error:%s" % (e.args[1]))
                msg=e.args[1]
                wx.MessageBox(message=msg,caption='Info',style=wx.OK | wx.ICON_INFORMATION)
                return
            con.commit()
            self.editTcpnl.Hide()
            self.updateTc(self)
        else:
            self.errorTcUpdate.SetLabel("Please, Fill all the data")
            self.errorTcUpdate.SetForegroundColour((0,255,0))

    def updatePcSubmit(self,e):
        if(self.tPcPname.GetValue() and self.tPcState.GetValue() and self.tPcType.GetValue() and self.tPcTotalpower.GetValue()):
            cur = con.cursor(mdb.cursors.DictCursor)
            cur.execute("select * from powercompany")
            rows=cur.fetchall()
            try:
                cur.execute("update powercompany set pname=%s,state=%s,type=%s,totalpower=%s  where pid =%s",(self.tPcPname.GetValue(),self.tPcState.GetValue(),self.tPcType.GetValue(),str(self.tPcTotalpower.GetValue()),rows[self.idPc]['pid']))
            except (mdb.Error,e):
                print ("Error:%s" % (e.args[1]))
                msg=e.args[1]
                wx.MessageBox(message=msg,caption='Info',style=wx.OK | wx.ICON_INFORMATION)
                return
            con.commit()
            self.editPcpnl.Hide()
            self.updatePc(self)
        else:
            self.errorPcUpdate.SetLabel("Please, Fill all the data")
            self.errorPcUpdate.SetForegroundColour((0,0,255))




    def DelDc(self,e):
        self.emppnl.Hide()
        self.delpnl=NewPanel(self)

        l0 = wx.StaticText(self.delpnl, -1, " Deleting Distriution Company  ",pos=(450,20),size=(500,500),style=wx.ALIGN_CENTER)
        l0.SetFont(wx.Font(15, wx.MODERN, wx.NORMAL, wx.BOLD))

        cur=con.cursor(mdb.cursors.DictCursor)
        cur.execute("select * from distributioncompany")
        self.rows=cur.fetchall()
        l0=wx.StaticText(self.delpnl, -1, "Id",pos=(150,80),size=(500,500))
        l0.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD))
        l1=wx.StaticText(self.delpnl, -1, "Name",pos=(300,80),size=(500,500))
        l1.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD))
        l2=wx.StaticText(self.delpnl, -1, "Tenure",pos=(580,80),size=(500,500))
        l2.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD))
        l3=wx.StaticText(self.delpnl, -1, "State",pos=(650,80),size=(500,500))
        l3.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD))
        l4=wx.StaticText(self.delpnl, -1, "T.C. Id",pos=(830,80),size=(500,500))
        l4.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD))
        #self.delpnl.SetupScrolling()
        i=120
        j=0
        for row in self.rows:
            wx.StaticText(self.delpnl, -1,str(row['did']),pos=(150,i))
            wx.StaticText(self.delpnl, -1,row['dname'],pos=(200,i))
            wx.StaticText(self.delpnl, -1,str(row['tenure']),pos=(600,i))
            wx.StaticText(self.delpnl, -1,row['state'],pos=(660,i))
            wx.StaticText(self.delpnl, -1,str(row['tid']),pos=(830,i))
            delButton = wx.Button(self.delpnl, label='DELETE', pos=(880, i),size=(100,20))
            delButton.Bind(wx.EVT_BUTTON,self.delButDc,delButton)
            delButton.id=j
            j=j+1
            i=i+30
        backButton = wx.Button(self.delpnl, label='Back', pos=(1000, 15),size = (100,40))

        backButton.Bind(wx.EVT_BUTTON, partial(self.back,p1=self.delpnl,p2=self.emppnl,title="Emplooyee"))

    def DelTc(self,e):
        self.emppnl.Hide()
        self.delpnl=NewPanel(self)
        l0 = wx.StaticText(self.delpnl, -1, " Deleting Transmission Company  ",pos=(450,20),size=(500,500),style=wx.ALIGN_CENTER)
        l0.SetFont(wx.Font(15, wx.MODERN, wx.NORMAL, wx.BOLD))

        cur=con.cursor(mdb.cursors.DictCursor)
        cur.execute("select * from transmissioncompany")
        self.rows=cur.fetchall()
        l0=wx.StaticText(self.delpnl, -1, "Tid",pos=(150,80),size=(500,500))
        l0.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD))
        l1=wx.StaticText(self.delpnl, -1, "Name",pos=(200,80),size=(500,500))
        l1.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD))
        l2=wx.StaticText(self.delpnl, -1, "Did",pos=(400,80),size=(500,500))
        l2.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD))
        l3=wx.StaticText(self.delpnl, -1, "Tcapacity",pos=(500,80),size=(500,500))
        l3.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD))
        l4=wx.StaticText(self.delpnl, -1, "State",pos=(600,80),size=(500,500))
        l4.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD))
        l5=wx.StaticText(self.delpnl, -1, "Tenure(in years)",pos=(800,80),size=(500,500))
        l5.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD))

        i=120
        j=0
        for row in self.rows:
            wx.StaticText(self.delpnl, -1,str(row['tid']),pos=(150,i))
            wx.StaticText(self.delpnl, -1,row['tname'],pos=(200,i))
            wx.StaticText(self.delpnl, -1,str(row['did']),pos=(400,i))
            wx.StaticText(self.delpnl, -1,str(row['tcapacity']),pos=(500,i))
            wx.StaticText(self.delpnl, -1,row['state'],pos=(600,i))
            wx.StaticText(self.delpnl, -1,str(row['tenure']),pos=(800,i))
            delButton = wx.Button(self.delpnl, label='DELETE', pos=(900, i),size=(100,20))
            delButton.Bind(wx.EVT_BUTTON,self.delButTc,delButton)
            delButton.id=j
            j=j+1
            i=i+30
        backButton = wx.Button(self.delpnl, label='Back', pos=(1000, 15),size = (100,40))

        backButton.Bind(wx.EVT_BUTTON, partial(self.back,p1=self.delpnl,p2=self.emppnl,title="Employee"))

    def DelPc(self,e):
        self.emppnl.Hide()
        self.delpnl=NewPanel(self)
        l0 = wx.StaticText(self.delpnl, -1, " Deleting Power Company  ",pos=(450,20),size=(500,500),style=wx.ALIGN_CENTER)
        l0.SetFont(wx.Font(15, wx.MODERN, wx.NORMAL, wx.BOLD))

        cur=con.cursor(mdb.cursors.DictCursor)
        cur.execute("select * from powercompany")
        self.rows=cur.fetchall()
        l0=wx.StaticText(self.delpnl, -1, "Pid",pos=(150,80),size=(500,500))
        l0.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD))
        l1=wx.StaticText(self.delpnl, -1, "Name",pos=(200,80),size=(500,500))
        l1.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD))
        l2=wx.StaticText(self.delpnl, -1, "State",pos=(320,80),size=(500,500))
        l2.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD))
        l3=wx.StaticText(self.delpnl, -1, "Type",pos=(500,80),size=(500,500))
        l3.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD))
        l4=wx.StaticText(self.delpnl, -1, "Total Power",pos=(600,80),size=(500,500))
        l4.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD))


        i=120
        j=0
        for row in self.rows:
            wx.StaticText(self.delpnl, -1,str(row['pid']),pos=(150,i))
            wx.StaticText(self.delpnl, -1,row['pname'],pos=(200,i))
            wx.StaticText(self.delpnl, -1,row['state'],pos=(320,i))
            wx.StaticText(self.delpnl, -1,row['type'],pos=(500,i))
            wx.StaticText(self.delpnl, -1,str(row['totalpower']),pos=(600,i))
            delButton = wx.Button(self.delpnl, label='DELETE', pos=(750, i),size=(100,20))
            delButton.Bind(wx.EVT_BUTTON,self.delButPc,delButton)
            delButton.id=j
            j=j+1
            i=i+30
        backButton = wx.Button(self.delpnl, label='Back', pos=(1000, 15),size = (100,40))

        backButton.Bind(wx.EVT_BUTTON, partial(self.back,p1=self.delpnl,p2=self.emppnl,title="Employee"))

    def delButDc(self,e):
        id=e.GetEventObject().id
        deldid=self.rows[id]['did']
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute("delete from distributioncompany where did =%s",(deldid,))
        con.commit()
        self.delpnl.Hide()
        self.DelDc(self)

    def delButTc(self,e):
        id=e.GetEventObject().id
        deltid=self.rows[id]['tid']
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute("delete from transmissioncompany where tid =%s",(deltid,))
        con.commit()
        self.delpnl.Hide()
        self.DelTc(self)

    def delButPc(self,e):
        id=e.GetEventObject().id
        delpid=self.rows[id]['pid']
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute("delete from powercompany where pid =%s",(delpid,))
        con.commit()
        self.delpnl.Hide()
        self.DelPc(self)

    def addDc(self,e):
        self.emppnl.Hide()
        self.formpnl=NewPanel(self)

        l0 = wx.StaticText(self.formpnl, -1, " Adding New Distriution Company  ",pos=(450,10),size=(500,500),style=wx.ALIGN_CENTER)
        l0.SetFont(wx.Font(15, wx.MODERN, wx.NORMAL, wx.BOLD))

        l1 = wx.StaticText(self.formpnl, -1, " Name of D.C. :   ",pos=(100,100))
        t11 = wx.TextCtrl(self.formpnl,style= wx.TE_PROCESS_ENTER,    pos=(350,100),size=(200,30))
        l2 = wx.StaticText(self.formpnl, -1, " Tenure       :   ",pos=(100,150))
        t12 = wx.TextCtrl(self.formpnl,style= wx.TE_PROCESS_ENTER,    pos=(350,150),size=(200,30))
        l3 = wx.StaticText(self.formpnl, -1, " State        :   ",pos=(100,200))
        t13 = wx.TextCtrl(self.formpnl,style= wx.TE_PROCESS_ENTER,    pos=(350,200),size=(200,30))
        l4 = wx.StaticText(self.formpnl, -1, " T.C. Id      :   ",pos=(100,250))
        t14 = wx.TextCtrl(self.formpnl,style= wx.TE_PROCESS_ENTER,    pos=(350,250),size=(200,30))
        SubmitButton = wx.Button(self.formpnl, label='Submit', pos=(500, 450),size=(100,40))
        SubmitButton.Bind(wx.EVT_BUTTON,partial(self.addDcSubmit,t11=t11,t12=t12,t13=t13,t14=t14))

        backButton = wx.Button(self.formpnl, label='Cancel', pos=(630, 450),size = (100,40))
        self.p1=self.formpnl
        self.p2=self.emppnl
        backButton.Bind(wx.EVT_BUTTON, self.addDcCancel)

    def addDcSubmit(self,e,t11,t12,t13,t14):
        if(t11.GetValue() and t12.GetValue() and t13.GetValue() and t14.GetValue()):
            cur = con.cursor(mdb.cursors.DictCursor)
            cur.execute("select did from distributioncompany ")
            rows=cur.fetchall()
            self.newid=rows[-1]['did'] + 1
            cur = con.cursor()
            cur.execute("insert into distributioncompany values (%s,%s,%s,%s,%s)",(self.newid,t11.GetValue(),t12.GetValue(),t13.GetValue(),t14.GetValue()))
            con.commit()

            #self.p1=self.formpnl
            #self.p2=self.emppnl
            wx.MessageBox(message='Succesfuly Submitted',caption='Info',style=wx.OK | wx.ICON_INFORMATION)
            #self.back(self)
            self.back(self,p1=self.formpnl,p2=self.emppnl,title="Employee")
        else:
            msg=wx.StaticText(self.formpnl, -1, "Any field can not be empty !!",pos=(w/2,300),size=(300,300))
            msg.SetForegroundColour((255,0,0))

    def addDcCancel(self,e):
        dial=wx.MessageBox(message='Do you want to cancel it?',caption='Cancel',style=wx.YES_NO | wx.ICON_INFORMATION)
        #self.p1=self.formpnl
        #self.p2=self.emppnl
        if (dial==2):
            #self.back(self)
            self.back(self,p1=self.formpnl,p2=self.emppnl,title="Employee")


    def addTc(self,e):
        self.emppnl.Hide()
        self.formpnl=NewPanel(self)

        l0 = wx.StaticText(self.formpnl, -1, " Adding New Transmission Company  ",pos=(450,10),size=(500,500),style=wx.ALIGN_CENTER)
        l0.SetFont(wx.Font(15, wx.MODERN, wx.NORMAL, wx.BOLD))

        l1 = wx.StaticText(self.formpnl, -1, " Name of T.C. :   ",pos=(100,100))
        t11 = wx.TextCtrl(self.formpnl,style= wx.TE_PROCESS_ENTER,    pos=(350,100),size=(200,30))
        l2 = wx.StaticText(self.formpnl, -1, " Tenure       :   ",pos=(100,150))
        t12 = wx.TextCtrl(self.formpnl,style= wx.TE_PROCESS_ENTER,    pos=(350,150),size=(200,30))
        l3 = wx.StaticText(self.formpnl, -1, " State        :   ",pos=(100,200))
        t13 = wx.TextCtrl(self.formpnl,style= wx.TE_PROCESS_ENTER,    pos=(350,200),size=(200,30))
        l4 = wx.StaticText(self.formpnl, -1, " Capacity     :   ",pos=(100,250))
        t14 = wx.TextCtrl(self.formpnl,style= wx.TE_PROCESS_ENTER,    pos=(350,250),size=(200,30))
        l5 = wx.StaticText(self.formpnl, -1, " D.C. Id      :   ",pos=(100,300))
        t15 = wx.TextCtrl(self.formpnl,style= wx.TE_PROCESS_ENTER,    pos=(350,300),size=(200,30))
        l6 = wx.StaticText(self.formpnl, -1, " P.C. Id      :   ",pos=(100,350))
        t16 = wx.TextCtrl(self.formpnl,style= wx.TE_PROCESS_ENTER,    pos=(350,350),size=(200,30))

        SubmitButton = wx.Button(self.formpnl, label='Submit', pos=(500, 450),size=(100,40))
        SubmitButton.Bind(wx.EVT_BUTTON,partial(self.addTcSubmit,t11=t11,t12=t12,t13=t13,t14=t14,t15=t15,t16=t16))

        backButton = wx.Button(self.formpnl, label='Cancel', pos=(630, 450),size = (100,40))
        self.p1=self.formpnl
        self.p2=self.emppnl
        backButton.Bind(wx.EVT_BUTTON, self.addTcCancel)

    def addTcSubmit(self,e,t11,t12,t13,t14,t15,t16):
        if(t11.GetValue() and t12.GetValue() and t13.GetValue() and t14.GetValue()):
            cur = con.cursor(mdb.cursors.DictCursor)
            cur.execute("select tid from transmissioncompany ")
            rows=cur.fetchall()
            self.newid=rows[-1]['tid'] + 1
            cur = con.cursor()
            cur.execute("insert into transmissioncompany values (%s,%s,%s,%s,%s,%s,%s)",(self.newid,t11.GetValue(),t15.GetValue(),t14.GetValue(),t13.GetValue(),t12.GetValue(),t16.GetValue()))
            con.commit()
            #self.p1=self.formpnl
            #self.p2=self.emppnl
            wx.MessageBox(message='Succesfuly Submitted',caption='Info',style=wx.OK | wx.ICON_INFORMATION)
            #self.back(self)
            self.back(self,p1=self.formpnl,p2=self.emppnl,title="Employee")
        else:
            msg=wx.StaticText(self.formpnl, -1, "No field can be empty !!",pos=(w/2,300),size=(300,300))
            msg.SetForegroundColour((255,0,0))

    def addTcCancel(self,e):
        dial=wx.MessageBox(message='Do you want to cancel it?',caption='Cancel',style=wx.YES_NO | wx.ICON_INFORMATION)
        #self.p1=self.formpnl
        #self.p2=self.emppnl
        if (dial==2):
            #self.back(self)
            self.back(self,p1=self.formpnl,p2=self.emppnl,title="Employee")
    def addPc(self,e):
        self.emppnl.Hide()
        self.formpnl=NewPanel(self)

        l0 = wx.StaticText(self.formpnl, -1, " Adding New Power Company  ",pos=(450,10),size=(500,500),style=wx.ALIGN_CENTER)
        l0.SetFont(wx.Font(15, wx.MODERN, wx.NORMAL, wx.BOLD))

        l1 = wx.StaticText(self.formpnl, -1, " Name of P.C.             :   ",pos=(100,100))
        t11 = wx.TextCtrl(self.formpnl,style= wx.TE_PROCESS_ENTER,    pos=(350,100),size=(200,30))
        l2 = wx.StaticText(self.formpnl, -1, " type                     :   ",pos=(100,150))
        typeList=('Private','Government')
        self.cbState=wx.ComboBox(self.formpnl,pos=(350,150),choices=typeList)
        self.t20="NULL"
        self.cbState.Bind(wx.EVT_COMBOBOX, self.gstr)
        #print self.t20
        #print t12
        l3 = wx.StaticText(self.formpnl, -1, " Total Power Generation   :   ",pos=(100,200))
        t13 = wx.TextCtrl(self.formpnl,style= wx.TE_PROCESS_ENTER,    pos=(350,200),size=(200,30))
        l4 = wx.StaticText(self.formpnl, -1, " State                    :   ",pos=(100,250))
        t14 = wx.TextCtrl(self.formpnl,style= wx.TE_PROCESS_ENTER,    pos=(350,250),size=(200,30))
        SubmitButton = wx.Button(self.formpnl, label='Submit', pos=(500, 450),size=(100,40))
        SubmitButton.Bind(wx.EVT_BUTTON,partial(self.addPcSubmit,t11=t11,t12=self.t20,t13=t13,t14=t14))

        backButton = wx.Button(self.formpnl, label='Cancel', pos=(630, 450),size = (100,40))
        self.p1=self.formpnl
        self.p2=self.emppnl
        backButton.Bind(wx.EVT_BUTTON, self.addPcCancel)

    def gstr(self,e):
        print (e.GetString())
        self.t20=e.GetString()

    def addPcSubmit(self,e,t11,t12,t13,t14):
        #print t12
        #print t12.GetValue()
        if(t11.GetValue() and len(t12) and t13.GetValue() and t14.GetValue()):
            cur = con.cursor(mdb.cursors.DictCursor)
            cur.execute("select pid from powercompany ")
            rows=cur.fetchall()
            self.newid=rows[-1]['pid'] + 1
            cur = con.cursor()
            cur.execute("insert into powercompany values (%s,%s,%s,%s,%s)",(self.newid,t11.GetValue(),t12,t13.GetValue(),t14.GetValue()))
            con.commit()

            #self.p1=self.formpnl
            #self.p2=self.emppnl
            wx.MessageBox(message='Succesfuly Submitted',caption='Info',style=wx.OK | wx.ICON_INFORMATION)
            #self.back(self)
            self.back(self,p1=self.formpnl,p2=self.emppnl,title="Employee")
        else:
            msg=wx.StaticText(self.formpnl, -1, "Any field can not be empty !!",pos=(w/2,300),size=(300,300))
            msg.SetForegroundColour((255,0,0))

    def addPcCancel(self,e):
        dial=wx.MessageBox(message='Do you want to cancel it?',caption='Cancel',style=wx.YES_NO | wx.ICON_INFORMATION)
        #self.p1=self.formpnl
        #self.p2=self.emppnl
        if (dial==2):
            #self.back(self)
            self.back(self,p1=self.formpnl,p2=self.emppnl,title="Employee")

    def XXEmployee(self,e,t1,t2,errormsg):
        self.emplpnl.Hide()

        self.SetTitle("Employee")
        self.emppnl=NewPanel(self)

        LogoutButton = wx.Button(self.emppnl, label='Logout', pos=(1270, 20),size=(80,35))
        LogoutButton.Bind(wx.EVT_BUTTON,partial(self.EmpLogout,t1=t1,t2=t2,errormsg=errormsg))
        cur.execute("select ename from employee where eid=%s",(t1.GetValue(),))
        rows=cur.fetchall()
        ProfileButton = wx.Button(self.emppnl, label='Hi '+rows[0][0], pos=(1100, 20),size=(150,35))
        ProfileButton.Bind(wx.EVT_BUTTON,partial(self.EmpProfile,t1=t1,t2=t2))

        cur.execute("select * from newconnection where boardname in ( select boardname from employee where eid=%s )",(t1.GetValue(),))
        self.ncrows=cur.fetchall()
        print (self.ncrows)
        desc = cur.description
        h1=wx.StaticText(self.emppnl, -1,'Applicant Name',    pos=(15,100),size=(130,20))
        h2=wx.StaticText(self.emppnl, -1,'Phone no',          pos=(150,100),size=(95,20))
        h3=wx.StaticText(self.emppnl, -1,'Boardname',         pos=(250,100),size=(345,20))
        h4=wx.StaticText(self.emppnl, -1,'State',             pos=(600,100),size=(125,20))
        h5=wx.StaticText(self.emppnl, -1,'Subdivision',       pos=(730,100),size=(115,20))
        h6=wx.StaticText(self.emppnl, -1,'Division',          pos=(850,100),size=(95,20))
        h7=wx.StaticText(self.emppnl, -1,'City',              pos=(950,100),size=(85,20))
        h8=wx.StaticText(self.emppnl, -1,'Email id',          pos=(1040,100),size=(145,20))
        h9=wx.StaticText(self.emppnl, -1,'Insta.. add',       pos=(1190,100),size=(165,20))
        h1.SetBackgroundColour('dark gray')
        h2.SetBackgroundColour('dark gray')
        h3.SetBackgroundColour('dark gray')
        h4.SetBackgroundColour('dark gray')
        h5.SetBackgroundColour('dark gray')
        h6.SetBackgroundColour('dark gray')
        h7.SetBackgroundColour('dark gray')
        h8.SetBackgroundColour('dark gray')
        h9.SetBackgroundColour('dark gray')
        i=160
        j=0
        k=0
        for r in self.ncrows:
            wx.StaticText(self.emppnl, -1,r[0],pos=(15,i),size=(500,500))
            wx.StaticText(self.emppnl, -1,str(r[1]),pos=(150,i),size=(500,500))
            wx.StaticText(self.emppnl, -1,r[2],pos=(250,i),size=(500,500))
            wx.StaticText(self.emppnl, -1,r[3],pos=(600,i),size=(500,500))
            wx.StaticText(self.emppnl, -1,r[4],pos=(730,i),size=(500,500))
            wx.StaticText(self.emppnl, -1,r[5],pos=(850,i),size=(500,500))
            wx.StaticText(self.emppnl, -1,r[6],pos=(950,i),size=(500,500))
            wx.StaticText(self.emppnl, -1,r[7],pos=(1040,i),size=(500,500))
            wx.StaticText(self.emppnl, -1,r[8],pos=(1190,i),size=(500,500))

            apButton = wx.Button(self.emppnl, label='Aprove', pos=(1090, i+40),size=(80,25))
            apButton.id=j
            apButton.SetBackgroundColour(wx.Colour(115,230,0))
            apButton.Bind(wx.EVT_BUTTON,partial(self.ncAprove,t1=t1,t2=t2,errormsg=errormsg),apButton)
            j=j+1
            rejButton = wx.Button(self.emppnl, label='Reject', pos=(1220, i+40),size=(80,25))
            rejButton.id=j
            rejButton.SetBackgroundColour(wx.Colour(255, 71, 26))
            rejButton.Bind(wx.EVT_BUTTON,partial(self.ncReject,t1=t1,t2=t2,errormsg=errormsg),rejButton)
            i=i+80
            j=j+1
            k=k+1


    def ncAprove(self,e,t1,t2,errormsg):
        print (e.GetEventObject().id)
        j=0
        k=0
        for i in range(0,len(self.ncrows)):
            if e.GetEventObject().id==2*j :
                cur=con.cursor()
                cur.execute("select max(meterno) from consumer")
                m=cur.fetchall()
                meterno=m[0][0]+1
                cur=con.cursor()
                cur.execute("insert into consumer values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(self.ncrows[k][10],self.ncrows[k][0],self.ncrows[k][1],self.ncrows[k][2],self.ncrows[k][3],self.ncrows[k][4],self.ncrows[k][5],self.ncrows[k][6], meterno,'firoz123',self.ncrows[k][7],self.ncrows[k][8],))
                status="Aproved"
                cur.execute("update ncstatus set status=%s where cid=%s",(status,self.ncrows[k][10]))

                con.commit()
                cur=con.cursor()
                cur.execute("delete from newconnection where cname=%s",(self.ncrows[k][0],))
                con.commit()
                self.emppnl.Hide()
                self.XXEmployee(self,t1=t1,t2=t2,errormsg=errormsg)
                break
            j=j+1
            k=k+1

    def ncReject(self,e,t1,t2,errormsg):
        print (e.GetEventObject().id)
        j=0
        k=0
        for i in range(0,len(self.ncrows)):
            if e.GetEventObject().id== (2*j+1) :
                cur=con.cursor()
                status="Rejected"
                cur.execute("update ncstatus set status=%s where cid=%s",(status,self.ncrows[k][10]))
                cur.execute("delete from newconnection where cname=%s",(self.ncrows[k][0],))
                con.commit()
                self.emppnl.Hide()
                self.XXEmployee(self,t1=t1,t2=t2,errormsg=errormsg)
                break
            j=j+1
            k=k+1

    def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(6))

    def Customer(self,e,t1,t2,errormsg):
        self.homepnl.Hide()
        self.SetTitle("User")
        self.custpnl=NewPanel(self)

        LogoutButton = wx.Button(self.custpnl, label='Logout', pos=(1270, 20),size=(80,35))
        cur.execute("select cname from consumer where cid=%s",(t1.GetValue(),))
        rows=cur.fetchall()
        ProfileButton = wx.Button(self.custpnl, label='Hi '+rows[0][0], pos=(1100, 20),size=(150,35))
        LogoutButton.Bind(wx.EVT_BUTTON,partial(self.CustLogout,t1=t1,t2=t2,errormsg=errormsg))

        billonEmail=wx.Button(self.custpnl, label='Bill on Email', pos=(1230, 400),size=(120,30))
        billonEmail.Bind(wx.EVT_BUTTON,partial(self.email_cust,t1=t1))
        ProfileButton.Bind(wx.EVT_BUTTON,partial(self.UserProfile,t1=t1))

        no_of_meter=cur.execute("select * from consumer where cid=%s",(t1.GetValue(),))
        rows_cust=cur.fetchall()
        print (no_of_meter)
        print (rows_cust)
        for i in range(0,no_of_meter):
            cur.execute("select * from billinginfo where meterno=%s",(str(rows_cust[i][8]),))
            rows_cust_bill=cur.fetchall()
            print (rows_cust_bill)
            l0 = wx.StaticText(self.custpnl, -1, str(rows_cust[i][3]),pos=(200,20+i*240),size=(1000,1000),style=wx.ALIGN_CENTER)
            l0.SetFont(wx.Font(20, wx.MODERN, wx.NORMAL, wx.BOLD))
            l1 = wx.StaticText(self.custpnl, -1, "Customer Id :     "+str(rows_cust[i][0]),pos=(100,100+i*240),size=(900,20))
            l2 = wx.StaticText(self.custpnl, -1, "Name        :     "+rows_cust[i][1],     pos=(100,130+i*240),size=(900,20))
            l3 = wx.StaticText(self.custpnl, -1, "Address     :     "+rows_cust[i][11],    pos=(100,160+i*240),size=(900,20))
            l4 = wx.StaticText(self.custpnl, -1, "Division    :     "+rows_cust[i][6],     pos=(100,190+i*240),size=(900,20))
            l5 = wx.StaticText(self.custpnl, -1, "SubDivision :     "+rows_cust[i][5],     pos=(400,100+i*240),size=(1000,1000))
            l6 = wx.StaticText(self.custpnl, -1, "Meter No.   :     "+str(rows_cust[i][8]),pos=(400,130+i*240),size=(1000,1000))

            l7 = wx.StaticText(self.custpnl, -1, "Bill No.         :     "+str(rows_cust_bill[0][0]),pos=(400,160+i*240),size=(1000,1000))
            l8 = wx.StaticText(self.custpnl, -1, "IssueDate        :     "+str(rows_cust_bill[0][2]),pos=(400,190+i*240),size=(1000,1000))
            l9 = wx.StaticText(self.custpnl, -1, "Previous Reading :     "+str(rows_cust_bill[0][3]),pos=(700,100+i*240),size=(1000,1000))
            l10 = wx.StaticText(self.custpnl, -1, "Current Reading :     "+str(rows_cust_bill[0][5]),pos=(700,130+i*240),size=(1000,1000))
            l11 = wx.StaticText(self.custpnl, -1, "Unit Consumed   :     "+str(rows_cust_bill[0][5]-rows_cust_bill[0][3]),pos=(700,160+i*240),size=(1000,1000))
            l1.SetBackgroundColour('dark gray')
            l2.SetBackgroundColour('dark gray')
            l3.SetBackgroundColour('dark gray')
            l4.SetBackgroundColour('dark gray')
        self.custpnl.Show()

    def email_cust(self,e,t1):
        self.custpnl.Hide()
        self.SetTitle("User")
        self.cust_email_pnl=NewPanel(self)
        l1=wx.StaticText(self.cust_email_pnl, -1, "Provide your email :",pos=(400,258),size=(500,500))
        self.t344 = wx.TextCtrl(self.cust_email_pnl,style= wx.TE_PROCESS_ENTER,pos=(600,250),size=(200,40))

        backButton = wx.Button(self.cust_email_pnl, label='Back', pos=(1000, 10))
        backButton.Bind(wx.EVT_BUTTON, partial(self.back,p1=self.cust_email_pnl,p2=self.custpnl,title="Power Distribution System"))

        Emailme=wx.Button(self.cust_email_pnl, label='Email me', pos=(600, 330),size=(100,30))
        Emailme.Bind(wx.EVT_BUTTON,partial(self.email1,t1=t1))

    def email1(self,e,t1):
        no_of_meter=cur.execute("select * from consumer where cid=%s",(t1.GetValue(),))
        rows_cust=cur.fetchall()

        cur.execute("select * from billinginfo where meterno=%s",(rows_cust[0][8],))
        rows_cust_bill=cur.fetchall()

        me = "firozmohd139@gmail.com"
        my_password = "Firoz@098"
        you = self.t344.GetValue()

        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Alert"
        msg['From'] = me
        msg['To'] = you

        html ="""
        <html>
            <body>
                <h1>{bname}</h1>
                <h2>Hi {name}</h2>
                <p>Bill id : {billid}</p>
                <p>Address : {add}</p>
                <p>Phone no. : {pno}</p>
                <p>E-mail : {email}</p>
                <p>division : {div}</p>
                <p>subdivision : {subdiv}</p>
                <p>City : {city}</p>
                <p>IssueDate : {isdate}</p>
                <p>Meter no. : {mtrno}</p>
                <p>Previous Reading : {pr}</p>
                <p>Current Reading : {cr}</p>
            </body>
        </html>
        """.format(bname=rows_cust[0][3],name=rows_cust[0][1],billid=rows_cust_bill[0][0],add=rows_cust[0][11],pno=str(rows_cust[0][2]),email=rows_cust[0][10],div=rows_cust[0][6],subdiv=rows_cust[0][5],city=rows_cust[0][4],isdate=rows_cust_bill[0][2],mtrno=str(rows_cust_bill[0][4]),pr=str(rows_cust_bill[0][3]),cr=str(rows_cust_bill[0][5]))
        part2 = MIMEText(html, 'html')
        msg.attach(part2)
        s = smtplib.SMTP_SSL('smtp.gmail.com',465)
        s.login(me, my_password)
        try :
            s.sendmail(me, you, msg.as_string())
            s.quit()
            msgg='\n Check your mail'
            wx.MessageBox(message=msgg,caption='Info',style=wx.OK | wx.ICON_INFORMATION)
            self.back(self,p1=self.cust_email_pnl,p2=self.custpnl,title="Power Distribution System")
        except :
            msgg='\nInvalid Email id'
            wx.MessageBox(message=msgg,caption='Info',style=wx.OK | wx.ICON_INFORMATION)

        #self.back(self,p1=self.ackpnl,p2=self.homepnl,title="Power Distribution System")









    def CustLogout(self,e,t1,t2,errormsg):
        t1.Clear()
        t2.Clear()
        errormsg.SetLabel(" ")
        #self.p1=self.custpnl
    	#self.p2=self.homepnl
        #self.back(self)
        self.back(self,p1=self.custpnl,p2=self.homepnl,title="Power Distribution System")

    def EmpLogout(self,e,t1,t2,errormsg):
        t1.Clear()
        t2.Clear()
        errormsg.SetLabel(" ")
        #self.panel.Hide()
        #self.p1=self.emppnl
    	#self.p2=self.homepnl
        #self.back(self)
        self.back(self,p1=self.emppnl,p2=self.emplpnl,title="Employee Login")

    def ElfToMainBack(self,e,t1,t2,errormsg):
        t1.Clear()
        t2.Clear()
        errormsg.SetLabel(" ")
        self.back(self,p1=self.emplpnl,p2=self.homepnl,title="Power Distribution System")

    def OnClose(self,e):
        self.Close(True)


def main():

    app = wx.App()
    ex = MainWindow(None)
    ex.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
