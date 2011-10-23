#!/usr/bin/python

"""
  Author:     Martin Matusiak <numerodix@gmail.com>
  Program:    Creates static HTML album pages and images pages recursively
  Date:       Dec. 19, 2005

  This file is subject to the GNU General Public License (GPL)
  (http://www.gnu.org/copyleft/gpl.html)
"""

import sys, inspect
sys.path.append("..")

import wx, glade_guimain
import launch
from config import config


class GuiMainWindow(glade_guimain.MainFrame):


	def onStartBtn(self, event):
		self.onSaveSettingsBtn(event)
		
		basepath = self.gallery_path.GetValue()
		if basepath == None or basepath == "":
			wx.MessageDialog(self,
				"No gallery path given, cannot proceed without one.",
				"",
				wx.OK
			).ShowModal()
		else:
#			self.exitBtn.Enable(enable=False)
			launch.main(basepath=basepath)
#		self.exitBtn.Enable()


	def onExitBtn(self, event):
		sys.exit(0)


	def onFileSelectorBtn(self, event):
		dlg = wx.DirDialog(self,
			defaultPath=self.gallery_path.GetValue()
		)
		if dlg.ShowModal():
			self.gallery_path.SetValue(dlg.GetPath())


	def initForms(self):
		settings = config.read()
		self.image_size_x.SetValue(int(settings['image_size_x']))
		self.image_size_y.SetValue(int(settings['image_size_y']))
		self.thumbnail_size_x.SetValue(int(settings['thumbnail_size_x']))
		self.thumbnail_size_y.SetValue(int(settings['thumbnail_size_y']))
		self.image_quality.SetValue(int(settings['image_quality']))
		self.thumbnail_quality.SetValue(int(settings['thumbnail_quality']))
		self.album_cols.SetValue(int(settings['album_cols']))
		self.album_rows.SetValue(int(settings['album_rows']))
		self.gallery_path.SetValue(settings['gallery_path'])
		self.image_extensions.SetValue(settings['image_extensions'])
		self.thumbnail_suffix.SetValue(settings['thumbnail_suffix'])
		self.tmp_first.SetValue(settings['tmp_first'])
		self.tmp_prev.SetValue(settings['tmp_prev'])
		self.tmp_index.SetValue(settings['tmp_index'])
		self.tmp_next.SetValue(settings['tmp_next'])
		self.tmp_last.SetValue(settings['tmp_last'])
		self.rebuild_thumbnails.SetValue(settings['rebuild_thumbnails'])


	def onSaveSettingsBtn(self, event):
		settings = {
			"image_size_x": self.image_size_x.GetValue(),
			"image_size_y": self.image_size_y.GetValue(),
			"thumbnail_size_x": self.thumbnail_size_x.GetValue(),
			"thumbnail_size_y": self.thumbnail_size_y.GetValue(),
			"image_quality": self.image_quality.GetValue(),
			"thumbnail_quality": self.thumbnail_quality.GetValue(),
			"album_cols": self.album_cols.GetValue(),
			"album_rows": self.album_rows.GetValue(),
			"gallery_path": self.gallery_path.GetValue(),
			"image_extensions": self.image_extensions.GetValue(),
			"thumbnail_suffix": self.thumbnail_suffix.GetValue(),
			"tmp_first": self.tmp_first.GetValue(),
			"tmp_prev": self.tmp_prev.GetValue(),
			"tmp_index": self.tmp_index.GetValue(),
			"tmp_next": self.tmp_next.GetValue(),
			"tmp_last": self.tmp_last.GetValue(),
			"rebuild_thumbnails": self.rebuild_thumbnails.GetValue(),
		}
		config.store(settings)



class GuiApp(wx.App):
	def OnInit(self):
		wx.InitAllImageHandlers()
		frame = GuiMainWindow(None, -1, "")
		self.SetTopWindow(frame)
		frame.initForms()
		frame.Show()
		return 1


def main():
	g = GuiApp(0)
	g.MainLoop()



if __name__ == "__main__":
	main()