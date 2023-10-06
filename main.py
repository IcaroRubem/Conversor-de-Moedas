from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.uix.recycleview import RecycleView
from kivy.clock import Clock
from kivymd.toast import toast
from webbrowser import open as webopen
from requests import get
from moedasjson import moedas
from bottom import BottomMotion
from kivy.properties import StringProperty, ObjectProperty
from kivymd.uix.list import TwoLineAvatarIconListItem
from kivymd.uix.boxlayout import MDBoxLayout

LabelBase.register(DEFAULT_FONT, "fonts/Kanit-Medium.ttf")

class Gerenciador(MDBoxLayout):
    pass


class ListaDeMoedas(RecycleView):
    moeda_selecionada = StringProperty()
    img_src = StringProperty()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = [{
            'text': f'{nome}',
            'secondary_text': ansi,
            'icone': f"images/{ansi}.png"} for ansi, nome in moedas.items()]
    def pesquisar_moedas(self, txt):
        self.data = []
        for ansi, nome in moedas.items():
            if txt.lower() in ansi.lower() or txt.lower() in nome.lower(): 
               self.data.append({'text': f'{nome}',
            'secondary_text': ansi,
            'icone': f"images/{ansi}.png"})
            
    def atualizar_moeda(self, moedas, txt, ansi, img, app):
        moedas.ids.search.text = ""
        app.root.ids.rtd.text = '0,00'
        moedas.ids[self.moeda_selecionada].text = txt
        moedas.ids[self.moeda_selecionada].secondary_text = ansi
        moedas.ids[self.img_src].source = img
        self.tabela(app)
        app.resultado()
        
    def trocar_moedas(self, moedas, app):
        app.taxa_de_cambio = 0
        app.root.ids.rtd.text = '0,00'
        moedas.ids.origem.text, moedas.ids.destino.text = moedas.ids.destino.text, moedas.ids.origem.text
        
        moedas.ids.origem.secondary_text, moedas.ids.destino.secondary_text = moedas.ids.destino.secondary_text, moedas.ids.origem.secondary_text
        
        moedas.ids.img_origem.source, moedas.ids.img_destino.source = moedas.ids.img_destino.source, moedas.ids.img_origem.source
        self.tabela(app)
        app.resultado()
        
    def tabela(self, app):
        app.root.ids.orig.text = app.root.ids.origem.text
        app.root.ids.dest.text = app.root.ids.destino.text
                
class Item(TwoLineAvatarIconListItem):
    icone = StringProperty("")

class App(MDApp):
    taxa_de_cambio = 0
    wifi_conect = True
    def build(self):
        self.theme_cls.theme_style = "Dark"
        return Gerenciador()
   
    def on_start(self):
        Clock.schedule_interval(self.resultado, 6)
    
    def sobre(self):
        webopen("https://github.com/IcaroRubem")
        
    def wifi_info(self, text):
        toast(text)
      
    def cambiar(self):
        quantidade = "0" if self.root.ids.qtd.text == "" else self.root.ids.qtd.text
        self.root.ids.rtd.text = f"{float(quantidade) * self.taxa_de_cambio:,.2f}".replace(",","_").replace(".",",").replace("_",".")
    
    def resultado(self, *args):
        try:
            self.taxa_de_cambio = get(f"https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/{self.root.ids.origem.secondary_text.lower()}/{self.root.ids.destino.secondary_text.lower()}.json", timeout=3).json()[self.root.ids.destino.secondary_text.lower()]
            self.cambiar()
            if not self.wifi_conect:
                self.root.ids.topappbar.right_action_items[0] = ["wifi-check", lambda x: self.wifi_info("Conectado"),"Conectado"]     
                self.wifi_info("Conectado")
                self.wifi_conect = True
        except Exception as erro:
            if self.wifi_conect:
                self.root.ids.topappbar.right_action_items[0] = ["wifi-remove", lambda x: self.wifi_info("Erro de Conexão"),"Wifi Desconectado"]      
                self.wifi_info("Verifique a sua conexão com a internet")
                self.wifi_conect = False
            

App().run()