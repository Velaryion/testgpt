import unittest
from core import parse,downloadable
class Tests(unittest.TestCase):
    def test_rss(self):
        rows=parse(b'<rss xmlns:n="https://nyaa.si/xmlns/nyaa"><channel><item><title>Episode</title><link>https://nyaa.si/download/1.torrent</link><guid>https://nyaa.si/view/1</guid><n:seeders>12</n:seeders></item></channel></rss>','https://nyaa.si/')
        self.assertEqual(rows[0].title,'Episode'); self.assertEqual(rows[0].seeds,'12'); self.assertEqual(rows[0].page,'https://nyaa.si/view/1'); self.assertTrue(rows[0].download.endswith('.torrent'))
    def test_forum(self):
        rows=parse(b'<a href="showthread.php?tid=1">Anime</a><a href="showthread.php?tid=1">Duplicate</a>','https://foro.unionfansub.com/')
        self.assertEqual(len(rows),1); self.assertEqual(rows[0].download,'')
    def test_reject_unsafe(self):
        for url in ['file:///x.torrent','javascript:alert(1)','https://u:p@host/a.torrent','magnet:?xt=bad','https://host/a.exe']:
            with self.assertRaises(ValueError): downloadable(url)
    def test_magnet(self): self.assertTrue(downloadable('magnet:?xt=urn:btih:'+'a'*40))
    def test_empty(self): self.assertEqual(parse(b'<html>Login required</html>','https://example.org/'),[])
if __name__=='__main__': unittest.main()
