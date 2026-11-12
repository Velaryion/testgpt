import sys
import unittest
from unittest.mock import patch
from app import App
from core import Item

@unittest.skipUnless(sys.platform=='win32','Validación gráfica en el runner de Windows')
class LayoutTests(unittest.TestCase):
    def test_buttons_visible_at_small_size_and_large_text(self):
        app=App()
        try:
            app.tk.call('tk','scaling',1.75)
            app.geometry('850x550'); app.update()
            for button in app.action_buttons:
                with self.subTest(button=button.cget('text')):
                    self.assertTrue(button.winfo_ismapped())
                    self.assertGreaterEqual(button.winfo_height(),button.winfo_reqheight())
                    self.assertGreaterEqual(button.winfo_width(),button.winfo_reqwidth())
                    self.assertLessEqual(button.winfo_rooty()+button.winfo_height(),app.winfo_rooty()+app.winfo_height())
            self.assertGreater(app.table.winfo_height(),80)
            self.assertLessEqual(app.status_label.winfo_rooty()+app.status_label.winfo_height(),app.winfo_rooty()+app.winfo_height())
        finally: app.destroy()
    def test_selected_torrent_sent_from_download_button(self):
        app=App()
        try:
            link='magnet:?xt=urn:btih:'+'a'*40
            app.rows=[Item('Episode 20','https://nyaa.si/view/1',link)]
            app.table.insert('','end',iid='0',values=('Episode 20','1 GiB','5'))
            app.table.selection_set('0')
            with patch.object(app,'launch') as launch:
                app.download_button.invoke()
                launch.assert_called_once_with(link)
        finally: app.destroy()
    def test_tracker_opens_authenticated_browser_instead_of_empty_search(self):
        app=App()
        try:
            app.source.set('https://torrent.unionfansub.com/browse.php')
            app.update_source()
            self.assertTrue(app.query.instate(['disabled']))
            with patch.object(app,'open_union') as browser,patch('app.fetch') as fetch:
                app.button.invoke()
                browser.assert_called_once_with()
                fetch.assert_not_called()
        finally: app.destroy()
