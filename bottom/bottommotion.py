from kivymd.uix.card import MDCard
from kivy.lang import Builder
from kivy.animation import Animation
from kivy.properties import StringProperty, ListProperty, NumericProperty
from kivy.core.window import Window


Builder.load_string("""
<BottomMotion>:
    radius: self.radio
    size_hint_y: self.bottom_size
    y: - (self.alt * self.bottom_size)
    pos_hint: {"center_x": .5}
    size_hint_x: self.width_motion
""")
 
class BottomMotion(MDCard):
    radio = ListProperty([50,50,0,0])
    bottom_size = NumericProperty(.5)
    width_motion = NumericProperty(1)
    larg = Window.width
    alt = Window.height * 2
    move_duration = NumericProperty(.3)
     
    def open(self):
        if self.y == - (self.alt * self.bottom_size):
            open_bottomoption = Animation(
                y = 0, duration = self.move_duration
            )
            open_bottomoption.start(self)
            open_bottomoption = None
        
    def close(self):
        if self.y == 0:
            close_bottomoption = Animation(
                y = - (self.alt * self.bottom_size),
                duration = self.move_duration
            )
            close_bottomoption.start(self)
            close_bottomoption = None
            
    def help_exemple(self):
        return """
        BottomMotion:
            color: "green" --> Cor
            move_duration: .2 --> duração de movimento
            orientation: "vertical" --> orientação
            radio: [50, 50,0,0] --> Radius
            width_motion: 1 --> Largura
            bottom_size: .5 --> mesmo que size_hint_y
            
            OBS: O "BottomMotion" foi criado
            com base no "MDCard", Portanto
            o BottomMotion aceita atributos
            de tal!
        """