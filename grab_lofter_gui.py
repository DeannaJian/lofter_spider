# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 26 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class MyFrame1
###########################################################################

class MyFrame1 ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Grab Lofter V1.0 @冰糖雪耳糖水", pos = wx.DefaultPosition, size = wx.Size( 500,215 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.SYSTEM_MENU|wx.BORDER_SIMPLE|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        self.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "微软雅黑" ) )
        self.SetForegroundColour( wx.Colour( 255, 255, 255 ) )
        self.SetBackgroundColour( wx.Colour( 65, 65, 65 ) )

        self.m_statusBar1 = self.CreateStatusBar( 1, wx.STB_SIZEGRIP, wx.ID_ANY )
        self.m_statusBar1.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

        bSizer1 = wx.BoxSizer( wx.VERTICAL )


        bSizer1.Add( ( 0, 0), 1, wx.EXPAND, 0 )

        bSizer3 = wx.BoxSizer( wx.HORIZONTAL )

        bSizer4 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Lofter页面：", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
        self.m_staticText1.Wrap( -1 )

        self.m_staticText1.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "微软雅黑" ) )
        self.m_staticText1.SetForegroundColour( wx.Colour( 255, 255, 255 ) )

        bSizer4.Add( self.m_staticText1, 0, wx.ALL, 5 )


        bSizer3.Add( bSizer4, 1, wx.ALL|wx.EXPAND, 5 )

        bSizer5 = wx.BoxSizer( wx.VERTICAL )

        self.m_textCtrl1 = wx.TextCtrl( self, wx.ID_ANY, u"https://XXX.lofter.com/post/XXXXXXXXXXXX", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer5.Add( self.m_textCtrl1, 0, wx.ALL|wx.EXPAND, 5 )


        bSizer3.Add( bSizer5, 4, wx.EXPAND, 5 )


        bSizer1.Add( bSizer3, 2, wx.EXPAND, 5 )

        bSizer6 = wx.BoxSizer( wx.HORIZONTAL )

        bSizer7 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"输出目录 ：", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
        self.m_staticText2.Wrap( -1 )

        self.m_staticText2.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "微软雅黑" ) )
        self.m_staticText2.SetForegroundColour( wx.Colour( 255, 255, 255 ) )

        bSizer7.Add( self.m_staticText2, 0, wx.ALL, 5 )


        bSizer6.Add( bSizer7, 1, wx.ALL|wx.EXPAND, 5 )

        bSizer8 = wx.BoxSizer( wx.VERTICAL )

        self.m_dirPicker1 = wx.DirPickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"选择输出目录", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE|wx.DIRP_SMALL )
        bSizer8.Add( self.m_dirPicker1, 0, wx.ALL|wx.EXPAND, 5 )


        bSizer6.Add( bSizer8, 4, wx.EXPAND, 5 )


        bSizer1.Add( bSizer6, 2, wx.EXPAND, 5 )

        bSizer9 = wx.BoxSizer( wx.HORIZONTAL )

        bSizer10 = wx.BoxSizer( wx.VERTICAL )

        self.m_button_grab = wx.Button( self, wx.ID_ANY, u"下载", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_button_grab.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "微软雅黑" ) )
        self.m_button_grab.SetForegroundColour( wx.Colour( 255, 255, 255 ) )
        self.m_button_grab.SetBackgroundColour( wx.Colour( 48, 48, 48 ) )

        bSizer10.Add( self.m_button_grab, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )


        bSizer9.Add( bSizer10, 1, wx.EXPAND, 5 )

        bSizer11 = wx.BoxSizer( wx.VERTICAL )

        self.m_button_open_dir = wx.Button( self, wx.ID_ANY, u"打开输出目录", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_button_open_dir.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "微软雅黑" ) )
        self.m_button_open_dir.SetForegroundColour( wx.Colour( 255, 255, 255 ) )
        self.m_button_open_dir.SetBackgroundColour( wx.Colour( 48, 48, 48 ) )

        bSizer11.Add( self.m_button_open_dir, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )


        bSizer9.Add( bSizer11, 1, wx.EXPAND, 5 )


        bSizer1.Add( bSizer9, 2, wx.EXPAND, 5 )


        self.SetSizer( bSizer1 )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.m_button_grab.Bind( wx.EVT_BUTTON, self.start_grab )
        self.m_button_open_dir.Bind( wx.EVT_BUTTON, self.open_output_dir )

    def __del__( self ):
        pass


    # Virtual event handlers, overide them in your derived class
    def start_grab( self, event ):
        event.Skip()

    def open_output_dir( self, event ):
        event.Skip()


