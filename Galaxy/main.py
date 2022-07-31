from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.graphics.context_instructions import Color 
from kivy.graphics.vertex_instructions import Line 

class MainWidget(Widget):
    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)
    V_NB_LINES = 14
    V_LINES_SPACING = .1
    vertical_lines = []
    line = None

    def __init__(self, **kwargs):
        super(MainWidget , self).__init__(**kwargs)
        self.init_vertical_lines()
        #print('Init func ',self.width , self.height)


    # Called when widget is attached to the Main app
    def on_parent(self, widget , parent):
        #print('Parent func ',self.width , self.height)
        pass
    # Called when size is changed
    def on_size(self, widget , parent):
        self.update_vertical_line()
        print('Size func ',self.width , self.height)
       
       # COmmeting out cause doing in galaxy.kv file
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

    def update_vertical_line(self):
        center_x = self.width/2
        offset = -int(self.V_NB_LINES/2)
        spacing = self.V_LINES_SPACING * self.width
        for i in range(0,self.V_NB_LINES):
            linex = int(center_x + offset * spacing)
            self.vertical_lines[i].points = [linex , self.height , linex , 0]
            offset += 1


class GalaxyApp(App):
    pass


GalaxyApp().run()
