import wx
from get_lofter_stories import *
import grab_lofter_gui
import os


class grab_lofter_frame(grab_lofter_gui.MyFrame1):
    def check_output_dir(self):
        output_folder = self.m_dirPicker1.GetPath()
        if not os.path.exists(output_folder):
            dlg = wx.MessageDialog(None, '输出目录不存在。请重新选择。',
                                   '提示', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            output_folder = None

        return output_folder

    def start_grab(self, event):
        if not self.check_output_dir():
            return

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
        self.m_button_grab.Disable()

    def open_output_dir(self, event):
        output_folder = self.check_output_dir()
        if output_folder:
            os.startfile(output_folder)


app = wx.App(False)
dlg = grab_lofter_frame(None)
dlg.Show(True)
app.MainLoop()
