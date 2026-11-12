from dataclasses import dataclass
from urllib.parse import urlsplit, urlencode, parse_qs, urljoin
from urllib.request import urlopen, Request
from html.parser import HTMLParser
import xml.etree.ElementTree as ET
import re
@dataclass
class Item:
    title:str
    page:str
    download:str=''
    size:str='—'
    seeds:str='—'
def https(url):
    p=urlsplit(url)
    if p.scheme!='https' or not p.hostname or p.username or p.password: raise ValueError('Introduce una URL HTTPS sin credenciales.')
    return url
def downloadable(url):
    p=urlsplit(url)
    if p.scheme=='magnet':
        if not any(re.fullmatch(r'urn:btih:(?:[a-fA-F0-9]{40}|[a-zA-Z2-7]{32})',x) for x in parse_qs(p.query).get('xt',[])): raise ValueError('Magnet inválido.')
        return url
    https(url)
    if not p.path.endswith('.torrent'): raise ValueError('Se necesita un enlace magnet o HTTPS .torrent.')
    return url
class Links(HTMLParser):
    def __init__(self,base):
        super().__init__(); self.base=base; self.rows=[]; self.href=None; self.text=[]; self.seen=set()
    def handle_starttag(self,tag,attrs):
        if tag=='a': self.href=dict(attrs).get('href'); self.text=[]
    def handle_data(self,data):
        if self.href is not None: self.text.append(data)
    def handle_endtag(self,tag):
        if tag!='a' or self.href is None: return
        url=urljoin(self.base,self.href); self.href=None
        try: dl=downloadable(url)
        except ValueError: dl=''
        p=urlsplit(url)
        topic=p.scheme=='https' and p.hostname==urlsplit(self.base).hostname and p.path.endswith('showthread.php') and 'tid' in parse_qs(p.query)
        if (dl or topic) and url not in self.seen:
            self.seen.add(url); self.rows.append(Item(' '.join(''.join(self.text).split()) or 'Torrent',self.base if dl else url,dl))
def parse(data,base):
    if data.lstrip().startswith((b'<?xml',b'<rss')):
        root=ET.fromstring(data)
        if root.tag!='rss': raise ValueError('RSS no compatible.')
        rows=[]; ns={'n':'https://nyaa.si/xmlns/nyaa'}
        for i in root.findall('./channel/item'):
            link=i.findtext('link',''); enc=i.find('enclosure')
            try: dl=downloadable(urljoin(base,enc.get('url','') if enc is not None else link))
            except ValueError: dl=''
            try: page=https(urljoin(base,i.findtext('guid','') or link))
            except ValueError: page=base
            rows.append(Item(i.findtext('title','Sin título'),page,dl,i.findtext('n:size','—',ns),i.findtext('n:seeders','—',ns)))
        return rows
    parser=Links(base); parser.feed(data.decode('utf-8',errors='replace')); return parser.rows
def fetch(source,query=''):
    https(source); nyaa=urlsplit(source).hostname=='nyaa.si'
    url='https://nyaa.si/?'+urlencode({'page':'rss','q':query,'c':'1_0','f':0}) if nyaa else source
    with urlopen(Request(url,headers={'User-Agent':'AnimeDesk/0.1'}),timeout=20) as r:
        base=https(r.url); data=r.read(4*1024*1024+1)
    if len(data)>4*1024*1024: raise ValueError('Respuesta demasiado grande.')
    rows=parse(data,base)
    return rows if nyaa else [r for r in rows if query.casefold() in r.title.casefold()]
