import tkinter as tk
from tkinter import ttk,messagebox,simpledialog,filedialog
import threading,queue,webbrowser,os,sys,subprocess
from core import fetch,https,downloadable
from transmission import find_transmission,save_transmission,send_to_transmission,send_file_to_transmission
from union_browser import is_tracker,TRACKER
class App(tk.Tk):
    def __init__(self):
        super().__init__(); self.title('AnimeDesk · Transmission'); self.geometry('1100x700'); self.minsize(850,550)
        self.transmission=find_transmission()
        self.rows=[]; self.queue=queue.Queue(); self.union_process=None
        style=ttk.Style(); style.theme_use('clam'); style.configure('Treeview',rowheight=34)
        f=ttk.Frame(self,padding=16); f.pack(fill='both',expand=True)
        f.columnconfigure(0,weight=1); f.rowconfigure(6,weight=1)
        ttk.Label(f,text='AnimeDesk',font=('Segoe UI',26,'bold')).grid(row=0,column=0,sticky='w')
        ttk.Label(f,text='1. Busca un anime.  2. Selecciona un resultado.  3. Pulsa Descargar en Transmission.').grid(row=1,column=0,sticky='w',pady=(0,12))
        ttk.Label(f,text='Fuente · página pública o RSS HTTPS').grid(row=2,column=0,sticky='w')
        self.source=ttk.Combobox(f,values=['https://nyaa.si/',TRACKER,'https://foro.unionfansub.com/index.php']); self.source.set('https://nyaa.si/'); self.source.grid(row=3,column=0,sticky='ew')
        bar=ttk.Frame(f); bar.grid(row=4,column=0,sticky='ew',pady=10); bar.columnconfigure(0,weight=1)
        self.query=ttk.Entry(bar); self.query.grid(row=0,column=0,sticky='ew'); self.query.bind('<Return>',lambda e:self.search())
        self.button=ttk.Button(bar,text='Buscar / Actualizar',command=self.search); self.button.grid(row=0,column=1,padx=8)
        self.source.bind('<<ComboboxSelected>>',lambda event:self.update_source())
        self.source.bind('<FocusOut>',lambda event:self.update_source())
        self.download_button=ttk.Button(bar,text='Descargar en Transmission',command=lambda:self.safe(self.download)); self.download_button.grid(row=0,column=2)
        actions=ttk.Frame(f); actions.grid(row=5,column=0,sticky='ew',pady=(0,10))
        self.action_buttons=[self.button,self.download_button]
        for col,(label,fn) in enumerate([('Ver publicación',self.publication),('Pegar magnet / .torrent',self.paste),('Abrir .torrent local',self.local_torrent),('Configurar Transmission',self.configure_transmission)]):
            actions.columnconfigure(col,weight=1)
            button=ttk.Button(actions,text=label,command=lambda fn=fn:self.safe(fn))
            button.grid(row=0,column=col,sticky='ew',padx=(0,6)); self.action_buttons.append(button)
        box=ttk.Frame(f); box.grid(row=6,column=0,sticky='nsew'); box.columnconfigure(0,weight=1); box.rowconfigure(0,weight=1)
        self.table=ttk.Treeview(box,columns=('title','size','seeds'),show='headings',selectmode='browse',height=5)
        for c,label,w in [('title','Título / Publicación',650),('size','Tamaño',110),('seeds','Semillas',90)]:
            self.table.heading(c,text=label); self.table.column(c,width=w,minwidth=70,stretch=c=='title')
        scroll=ttk.Scrollbar(box,command=self.table.yview); self.table.configure(yscrollcommand=scroll.set)
        self.table.grid(row=0,column=0,sticky='nsew'); scroll.grid(row=0,column=1,sticky='ns')
        horizontal=ttk.Scrollbar(box,orient='horizontal',command=self.table.xview); self.table.configure(xscrollcommand=horizontal.set)
        horizontal.grid(row=1,column=0,sticky='ew')
        self.table.bind('<Double-1>',lambda event:self.safe(self.download))
        self.status=tk.StringVar(value='Busca y selecciona un resultado; después pulsa Descargar en Transmission.')
        self.status_label=ttk.Label(f,textvariable=self.status,wraplength=780)
        self.status_label.grid(row=7,column=0,sticky='ew',pady=(8,0))
        ttk.Label(f,text='El progreso y la carpeta de descarga se gestionan en Transmission.').grid(row=8,column=0,sticky='w',pady=(6,0))
        self._poll_id=self.after(100,self.poll)
    def destroy(self):
        if hasattr(self,'_poll_id'): self.after_cancel(self._poll_id)
        super().destroy()
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
    def update_source(self):
        tracker=is_tracker(self.source.get())
        self.button.configure(text='Iniciar sesión / Catálogo' if tracker else 'Buscar / Actualizar')
        self.query.state(['disabled'] if tracker else ['!disabled'])
        if tracker:
            self.status.set('UnionFansub: inicia sesión y busca en la ventana integrada. Descarga el .torrent y usa el menú Transmission para abrirlo.')
    def open_union(self):
        if self.union_process is not None and self.union_process.poll() is None:
            self.status.set('UnionFansub ya está abierto: cambia a su ventana para continuar.')
            return
        command=([sys.executable,'--union-browser'] if getattr(sys,'frozen',False)
                 else [sys.executable,os.path.join(os.path.dirname(__file__),'app.py'),'--union-browser'])
        self.union_process=subprocess.Popen(command,shell=False,env={**os.environ,'PYINSTALLER_RESET_ENVIRONMENT':'1'})
        self.status.set('UnionFansub abierto: inicia sesión, usa su buscador y descarga el .torrent. Después: menú Transmission → Abrir archivo .torrent descargado.')
    def local_torrent(self):
        path=filedialog.askopenfilename(title='Abrir torrent descargado en Transmission',filetypes=[('Torrent','*.torrent')])
        if not path: return
        if not self.transmission: self.configure_transmission()
        if not self.transmission: return
        if messagebox.askyesno('Enviar a Transmission','¿Abrir este archivo .torrent en Transmission?'):
            send_file_to_transmission(self.transmission,path)
            self.status.set('Archivo enviado a Transmission. Comprueba allí la descarga.')
    def search(self):
        if is_tracker(self.source.get()):
            self.safe(self.open_union)
            return
        if self.button.instate(['disabled']): return
        source,query=self.source.get(),self.query.get()
        self.button.state(['disabled']); self.status.set('Consultando…')
        def work():
            try: self.queue.put((fetch(source,query),None))
            except Exception as e: self.queue.put((None,str(e)))
        threading.Thread(target=work,daemon=True).start()
    def poll(self):
        try:
            rows,error=self.queue.get_nowait(); self.button.state(['!disabled'])
            if error: self.status.set('No se pudo consultar: '+error+'. Puedes abrir la web en el navegador.')
            else:
                self.rows=rows; self.table.delete(*self.table.get_children())
                for i,r in enumerate(rows): self.table.insert('','end',iid=str(i),values=(r.title,r.size,r.seeds))
                self.status.set(f'{len(rows)} resultados. Selecciona uno y pulsa Descargar en Transmission. '+('Si el foro requiere sesión, abre la web y pega el enlace de descarga.' if not rows else ''))
        except queue.Empty: pass
        self._poll_id=self.after(100,self.poll)
if __name__=='__main__':
    if '--union-browser' in sys.argv or '--browser-smoke-test' in sys.argv:
        from union_browser import run
        try:
            run(smoke_test='--browser-smoke-test' in sys.argv)
        except Exception:
            if '--browser-smoke-test' in sys.argv:
                import traceback
                traceback.print_exc()
                sys.exit(1)
            root=tk.Tk(); root.withdraw()
            messagebox.showerror('Navegador UnionFansub', 'No se pudo iniciar el navegador integrado. Instala Microsoft Edge WebView2 Runtime y vuelve a intentarlo.')
            root.destroy()
            sys.exit(1)
    else:
        app=App()
        if '--smoke-test' in sys.argv:
            app.after(1000,app.destroy)
        app.mainloop()
