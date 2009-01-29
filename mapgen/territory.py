import util, random

PICK_TRIANGLE = 0
AVERAGE_POINTS = 1
LARGEST_TRIANGLE = 2

class Territory(object):
    def __init__(self):
        super(Territory, self).__init__()
        self.country = None
        self.adjacencies = []
        self.id = 0
    

class LandTerr(Territory):
    def __init__(self, lines, color=(0.5,0.5,0.5,1)):
        super(LandTerr, self).__init__()
        self.lines = []
        for line in lines:
            self.add_line(line)
        self.color = color
        self.adjacent_countries = []
        self.triangles = []
        self.x, self.y = 0.0, 0.0
        self.dist = 0
        self.center_mode = LARGEST_TRIANGLE
        self.combinations = 0
        self.offset = (0,0)
        self.has_supply_center = False
    
    def add_line(self, line):
        if line not in self.lines:
            self.lines.append(line)
            line.territories.append(self)
    
    def remove_line(self, line):
        self.lines.remove(line)
        line.territories.remove(self)
    
    def add_triangle(self, x1, y1, x2, y2, x3, y3):
        self.triangles.append((x1, y1, x2, y2, x3, y3))
    
    def find_adjacencies(self): 
        self.adjacent_countries = []
        self.adjacencies = []
        for line in self.lines:
            for terr in line.territories:
                if terr != self and terr not in self.adjacencies:
                    self.adjacencies.append(terr)
        for terr in self.adjacencies:
            if terr.country not in self.adjacent_countries:
                if terr.country != None:
                    self.adjacent_countries.append(terr.country)
    
    def place_capital(self):
        self.points = []
        for line in self.lines:
            if line.a not in self.points:
                self.points.append(line.a.get_tuple())
            if line.b not in self.points:
                self.points.append(line.b.get_tuple())
        self.x = 0.0
        self.y = 0.0
        for point in self.points:
            self.x += point[0]
            self.y += point[1]
        self.x /= len(self.points)
        self.y /= len(self.points)
        
        ok = True
        if not self.point_inside(self.x, self.y): ok = False
        if not self.point_inside(self.x+10, self.y): ok = False
        if not self.point_inside(self.x-10, self.y): ok = False
        if not self.point_inside(self.x, self.y+10): ok = False
        if not self.point_inside(self.x, self.y-10): ok = False
        if ok: return
        
        chosen_tri = 0
        max_area = 0
        for i in range(1, len(self.triangles)):
            a = util.area_of_triangle(self.triangles[i])
            if a > max_area:
                max_area = a
                chosen_tri = i
        tri = self.triangles[chosen_tri]
        self.x = tri[0] + tri[2] + tri[4]
        self.y = tri[1] + tri[3] + tri[5]
        self.x /= 3.0
        self.y /= 3.0
    
    def place_capital_old(self):
        """Chooses a place for the capital city"""
        if len(self.triangles) <= 3:
            self.center_mode = AVERAGE_POINTS
        else:
            self.center_mode = LARGEST_TRIANGLE
        if self.center_mode == PICK_TRIANGLE:
            tri = random.choice(self.triangles)
            self.x = tri[0] + tri[2] + tri[4]
            self.y = tri[1] + tri[3] + tri[5]
            self.x /= 3.0
            self.y /= 3.0
        elif self.center_mode == AVERAGE_POINTS:
            self.points = []
            for line in self.lines:
                if line.a.get_tuple() not in self.points:
                    self.points.append(line.a.get_tuple())
                if line.b.get_tuple() not in self.points:
                    self.points.append(line.b.get_tuple())
            self.x = 0.0
            self.y = 0.0
            for point in self.points:
                self.x += point[0]
                self.y += point[1]
            self.x /= len(self.points)
            self.y /= len(self.points)
        elif self.center_mode == LARGEST_TRIANGLE:
            chosen_tri = 0
            max_area = 0
            for i in range(1, len(self.triangles)):
                a = util.area_of_triangle(self.triangles[i])
                if a > max_area:
                    max_area = a
                    chosen_tri = i
            tri = self.triangles[chosen_tri]
            self.x = tri[0] + tri[2] + tri[4]
            self.y = tri[1] + tri[3] + tri[5]
            self.x /= 3.0
            self.y /= 3.0
    
    def color_self(self):
        darken_amt = (1.0-random.random()*0.15)
        self.color = (
            self.country.color[0]*darken_amt,
            self.country.color[1]*darken_amt,
            self.country.color[2]*darken_amt,
            1.0
        )
        if self.color == (0.0, 0.0, 0.0, 1.0):
            self.color = self.country.color
    
    def point_inside(self, x, y):
        """Returns True if (x,y) is inside the territory."""
        for tri in self.triangles:
            if util.point_inside_polygon(x, y, tri):
                return True
        return False
    
    def __repr__(self):
        return str(self.id)
    