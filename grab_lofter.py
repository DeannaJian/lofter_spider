import wx
from get_lofter_stories import *
import grab_lofter_gui
import os


class grab_lofter_frame(grab_lofter_gui.MyFrame1):
    def start_grab(self, event):
        import re
        self.m_statusBar1.SetStatusText('开始下载...')
        url = self.m_textCtrl1.GetValue()
        matchObj = re.match(r'http(.*)://(.*).lofter.com(.*?)', url)
        if not matchObj:
            os._exit(-1)

        output_folder = self.m_dirPicker1.GetPath()
        author = matchObj.group(2)
        output_filepath = grab_and_output(url, author, output_folder)
        self.m_statusBar1.SetStatusText('完成。 输出文件： %s' % output_filepath)

    def open_output_dir(self, event):
        output_folder = self.m_dirPicker1.GetPath()
        if os.path.exists(output_folder):
            os.startfile(output_folder)
            print(output_folder)
        else:
            dlg = wx.MessageDialog(None, '输出目录不存在。请重新选择。',
                                   '提示', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()


app = wx.App(False)
dlg = grab_lofter_frame(None)
dlg.Show(True)
app.MainLoop()
