

class Camera:
    def __init__(self, pos, dir):
        self.pos = pos;
        self.dir = dir;

    def get_data(self, data):
        data[0] = self.pos.x;
        data[1] = self.pos.y;
        data[2] = self.pos.z;
        data[4] = self.dir.x;
        data[5] = self.dir.y;
        data[6] = self.dir.z;
