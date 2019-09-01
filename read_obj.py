from triangle import Triangle, Vector


def read_obj(filename):
    f = open(filename, "r")
    data = ObjData()
    data.add_vertex(Vector())
    data.add_normal(Vector())
    for x in f.readlines():
        read_part(x, data)
    f.close()
    return data.triangles


def read_part(line, obj_data):
    data = line.split(' ')
    print(data)

    if data[0] == 'v':
        obj_data.add_vertex(Vector(float(data[1]), float(data[2]), float(data[3])))
    elif data[0] == 'f':
        obj_data.add_triangle(process_triangle(data[1:], obj_data))
    elif data[0] == 'vn':
        obj_data.add_normal(Vector(float(data[1]), float(data[2]), float(data[3])))


def process_triangle(data, obj_data):
    n1 = data[0].split('/')
    n2 = data[1].split('/')
    n3 = data[2].split('/')

    v1i, n1i = process_vertex_normal(n1)
    v2i, n2i = process_vertex_normal(n2)
    v3i, n3i = process_vertex_normal(n3)

    v1 = obj_data.vertices[v1i]
    v2 = obj_data.vertices[v2i]
    v3 = obj_data.vertices[v3i]


    normal = calc_normal(v1, v2, v3)

    n1 = normal
    n2 = normal
    n3 = normal

    if n1i != -1:
        n1 = obj_data.vertices[n1i]

    if n2i != -1:
        n2 = obj_data.vertices[n2i]

    if n3i != -1:
        n3 = obj_data.vertices[n3i]

    if len(data) < 7:
        return v1, v2, v3, n1, n2, n3, Vector(), 0
    color = Vector(float(data[3]), float(data[4]), float(data[5]))
    intensity = float(data[6])

    return v1, v2, v3, n1, n2, n3, color, intensity


def calc_normal(v1, v2, v3):
    e1 = v1.sub(v2)
    e2 = v1.sub(v3)
    return e1.cross(e2)


def process_vertex_normal(data):
    if len(data) == 3:
        return int(data[0]), int(data[2])

    return int(data[0]), -1


class ObjData:
    def __init__(self):
        self.vertices = []
        self.normals = []
        self.triangles = []

    def add_vertex(self, vertex):
        self.vertices.append(vertex)

    def add_normal(self, normal):
        self.normals.append(normal)

    def add_triangle(self, triangle_data):
        v1, v2, v3, n1, n2, n3, c, i = triangle_data
        self.triangles.append(Triangle(v1, v2, v3, n1, n2, n3, c, i))
