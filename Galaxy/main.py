from kivy.config import Config
Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '400')
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty , Clock
from kivy.graphics.context_instructions import Color 
from kivy.graphics.vertex_instructions import Line 
from kivy.core.window import Window
from kivy.utils import platform


class MainWidget(Widget):
    # Gloabal offsests to be changed by update 60 times a sec
    current_offset_y = 0
    SPEED = 4
    SPEEDX = 10
    current_offset_x = 0
    dir = 0
    # Perspective points
    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)
    # Vertical Line properties
    V_NB_LINES = 20
    V_LINES_SPACING = .1
    vertical_lines = []
    # Horizontal Line properties
    H_NB_LINES = 6
    H_LINES_SPACING = .2
    horizontal_lines = []

    def __init__(self, **kwargs):
        super(MainWidget , self).__init__(**kwargs)
        self.init_horizontal_lines()
        self.init_vertical_lines() 
        if self.is_desktop():
            self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
            self._keyboard.bind(on_key_down=self._on_keyboard_down , on_key_up = self._on_keyboard_up)
        Clock.schedule_interval(self.update , 1/60)
    def is_desktop(self):
        print(platform)
        if platform in ['linux','windows','macos','win']:
            return True
        return False
    


    # Called when widget is attached to the Main app
    def on_parent(self, widget , parent):
        #print('Parent func ',self.width , self.height)
        pass
    # Called when size is changed
    def on_size(self, widget , parent):
        pass
       
       # Commenting out cause doing in galaxy.kv file
      # self.perspective_point_x = self.width/2
      # self.perspective_point_y = self.height * 0.75


    # Called when perspective_point_x is changed as it is a property
    def on_perspective_point_x(self,widget,value):
        print('Px :' , value)
    
    # Called when perspective_point_y is changed as it is a property
    def on_perspective_point_y(self,widget,value):
        print('Py :' , value)

    # Is called in the __init__
    def init_vertical_lines(self):
        with self.canvas:
           
            Color(1,1,1)

            for i in range(0,self.V_NB_LINES):
                self.vertical_lines.append(Line())
     # Is called in the on_size
    def update_vertical_line(self):
        center_x = self.width//2
        offset = -int(self.V_NB_LINES/2) + 0.5
        
        spacing = self.V_LINES_SPACING * self.width
     
        for i in range(0,self.V_NB_LINES) :
            linex = int(center_x + offset * spacing) + self.current_offset_x
            x1 , y1 = self.transform(linex , 0)
            x2 , y2 = self.transform(linex , self.height)
            self.vertical_lines[i].points = [x1,y1,x2,y2]
            #self.vertical_lines[i].points = [self.perspective_point_x ,self.perspective_point_y , linex , 0]
            offset += 1
           

    # Is called in the __init__
    def init_horizontal_lines(self):
        with self.canvas:
           
            Color(1,1,1)

            for i in range(0,self.V_NB_LINES):
                self.horizontal_lines.append(Line())
    # Is called in the on_size
    def update_horizontal_line(self):
        center_x = self.width//2
        offset = -int(self.V_NB_LINES/2)  + 0.5
        spacing = self.V_LINES_SPACING * self.width

        x_min = center_x + offset*spacing + self.current_offset_x
        x_max = center_x - offset*spacing + self.current_offset_x
        spacing_y = self.H_LINES_SPACING * self.height
        i = 0
        while i < self.V_NB_LINES:
            liney = i * spacing_y - self.current_offset_y
            x1 , y1 = self.transform(x_min , liney)
            x2 , y2 = self.transform(x_max , liney)
            self.horizontal_lines[i].points = [x1,y1,x2,y2]
            #self.vertical_lines[i].points = [self.perspective_point_x ,self.perspective_point_y , linex , 0]
            offset += 1
            i += 1

    def transform(self, x , y):
        #return self.transform_2D(x,y)
        return self.transform_perspective(x,y)
    
    def transform_2D(self, x , y):
        return int(x),int(y)

    def transform_perspective(self, x , y):
        tr_y =  self.perspective_point_y * y / self.height
        if tr_y > self.perspective_point_y:
            tr_y = self.perspective_point_y
        diff_x = x- self.perspective_point_x
        diff_y = self.perspective_point_y - tr_y
        prop_y =  diff_y/self.perspective_point_y
        prop_y  *= prop_y
        tr_y = self.perspective_point_y - prop_y * self.perspective_point_y
        tr_x = self.perspective_point_x + diff_x * prop_y
        return int(tr_x),int(tr_y)
    # Game running code
    def on_touch_down(self, touch):
        if touch.x < self.width//2:
            self.dir = 1
        else :
            self.dir = -1
    
    def on_touch_up(self, touch):
        self.dir = 0
        

    def update(self,dt):
        time_factor = dt*60
        # Update Y
        self.current_offset_y += self.SPEED * time_factor   
        spacing_y = self.H_LINES_SPACING * self.height
        if self.current_offset_y >= spacing_y:
            self.current_offset_y -= spacing_y       
        # Update X
        self.current_offset_x += self.SPEEDX * time_factor * self.dir


        self.update_horizontal_line()
        self.update_vertical_line()
    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down,on_key_up = self._on_keyboard_up)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'left':
            self.dir = 1
        elif keycode[1] == 'right':
            self.dir = -1
        
        return True
    def _on_keyboard_up(self, keyboard, keycode):
        self.dir = 0

class GalaxyApp(App):
    pass


GalaxyApp().run()
