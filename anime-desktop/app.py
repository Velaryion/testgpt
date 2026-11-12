import tkinter as tk
from tkinter import ttk,messagebox,simpledialog,filedialog
import threading,queue,webbrowser,os
from core import fetch,https,downloadable
from transmission import find_transmission,save_transmission,send_to_transmission
class App(tk.Tk):
    def __init__(self):
        super().__init__(); self.title('AnimeDesk'); self.geometry('1050x650'); self.minsize(750,450)
        self.transmission=find_transmission()
        self.rows=[]; self.queue=queue.Queue(); self.page=1
        style=ttk.Style(); style.theme_use('clam'); style.configure('Treeview',rowheight=34)
        f=ttk.Frame(self,padding=24); f.pack(fill='both',expand=True)
        ttk.Label(f,text='AnimeDesk',font=('Segoe UI',26,'bold')).pack(anchor='w')
        ttk.Label(f,text='Busca torrents y envía tus descargas al cliente instalado.').pack(anchor='w',pady=(0,20))
        ttk.Label(f,text='Fuente · página pública o RSS HTTPS').pack(anchor='w')
        self.source=ttk.Combobox(f,values=['https://nyaa.si/','https://foro.unionfansub.com/index.php']); self.source.set('https://nyaa.si/'); self.source.pack(fill='x')
        bar=ttk.Frame(f); bar.pack(fill='x',pady=14)
        self.query=ttk.Entry(bar); self.query.pack(side='left',fill='x',expand=True); self.query.bind('<Return>',lambda e:self.search())
        self.button=ttk.Button(bar,text='Buscar / Actualizar',command=self.search); self.button.pack(side='left',padx=8)
        ttk.Button(bar,text='Siguiente',command=self.next).pack(side='left')
        box=ttk.Frame(f); box.pack(fill='both',expand=True)
        self.table=ttk.Treeview(box,columns=('title','size','seeds'),show='headings',selectmode='browse')
        for c,label,w in [('title','Título / Publicación',700),('size','Tamaño',110),('seeds','Semillas',90)]: self.table.heading(c,text=label); self.table.column(c,width=w)
        scroll=ttk.Scrollbar(box,command=self.table.yview); self.table.configure(yscrollcommand=scroll.set)
        self.table.pack(side='left',fill='both',expand=True); scroll.pack(side='right',fill='y')
        bar=ttk.Frame(f); bar.pack(fill='x',pady=14)
        for label,fn in [('Descargar',self.download),('Ver publicación',self.publication),('Pegar magnet / .torrent',self.paste),('Abrir web',self.website),('Configurar Transmission',self.configure_transmission)]: ttk.Button(bar,text=label,command=lambda fn=fn:self.safe(fn)).pack(side='left',padx=(0,8))
        self.status=tk.StringVar(value='Selecciona una fuente y busca. UnionFansub puede requerir una cuenta en el navegador.')
        ttk.Label(f,textvariable=self.status,wraplength=950).pack(anchor='w')
        ttk.Label(f,text='Las transferencias y su progreso se gestionan en Transmission.').pack(anchor='w',pady=8)
        self.after(100,self.poll)
    def safe(self,fn):
        try: fn()
        except Exception as e: messagebox.showerror('AnimeDesk',str(e))
    def website(self): webbrowser.open(https(self.source.get()))
    def selected(self):
        ids=self.table.selection()
        if not ids: raise ValueError('Selecciona un resultado.')
        return self.rows[int(ids[0])]
    def publication(self): webbrowser.open(https(self.selected().page))
    def configure_transmission(self):
        path=filedialog.askopenfilename(title='Selecciona transmission-qt.exe',filetypes=[('Transmission / Ejecutables','*.exe'),('Todos los archivos','*')])
        if path:
            self.transmission=save_transmission(path)
            self.status.set('Transmission configurado: '+self.transmission)
    def launch(self,url):
        url=downloadable(url)
        if not self.transmission:
            self.configure_transmission()
        if not self.transmission: return
        if messagebox.askyesno('Enviar a Transmission','¿Añadir este torrent a Transmission?\n'+url[:300]):
            send_to_transmission(self.transmission,url)
            self.status.set('Solicitud enviada a Transmission. Comprueba allí la descarga y la carpeta de destino.')
    def download(self):
        url=self.selected().download
        if not url: raise ValueError('Abre la publicación y pega su magnet o enlace .torrent. No hay descarga pública directa.')
        self.launch(url)
    def paste(self):
        url=simpledialog.askstring('Añadir descarga','Enlace magnet o HTTPS .torrent:',parent=self)
        if url: self.launch(url.strip())
    def next(self):
        if self.button.instate(['disabled']): return
        if self.source.get().rstrip('/')!='https://nyaa.si': self.status.set('Para avanzar en el foro, pega la dirección de su siguiente página.'); return
        self.page+=1; self.search(False)
    def search(self,reset=True):
        if self.button.instate(['disabled']): return
        if reset: self.page=1
        source,query,page=self.source.get(),self.query.get(),self.page
        self.button.state(['disabled']); self.status.set('Consultando…')
        def work():
            try: self.queue.put((fetch(source,query,page),None))
            except Exception as e: self.queue.put((None,str(e)))
        threading.Thread(target=work,daemon=True).start()
    def poll(self):
        try:
            rows,error=self.queue.get_nowait(); self.button.state(['!disabled'])
            if error: self.status.set('No se pudo consultar: '+error+'. Puedes abrir la web en el navegador.')
            else:
                self.rows=rows; self.table.delete(*self.table.get_children())
                for i,r in enumerate(rows): self.table.insert('','end',iid=str(i),values=(r.title,r.size,r.seeds))
                self.status.set(f'{len(rows)} resultados · Página {self.page}. '+('Si el foro requiere sesión, abre la web y pega el enlace de descarga.' if not rows else ''))
        except queue.Empty: pass
        self.after(100,self.poll)
if __name__=='__main__':
    import sys
    app=App()
    if '--smoke-test' in sys.argv:
        app.after(1000,app.destroy)
    app.mainloop()
