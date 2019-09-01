import moderngl
import numpy as np
import pygame

from camera import Camera
from read_obj import read_obj
from triangle import Vector
from time import sleep

import os

import moderngl_window as mglw


class Example(mglw.WindowConfig):
    gl_version = (3, 3)
    title = "ModernGL Example"
    window_size = (1280, 720)
    aspect_ratio = 16 / 9
    resizable = True
    samples = 4

    resource_dir = os.path.normpath(os.path.join(__file__, '../../data'))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def run(cls):
        mglw.run_window_config(cls)


def source(uri, consts):
    ''' read gl code '''
    with open(uri, 'r') as fp:
        content = fp.read()

    # feed constant values
    for key, value in consts.items():
        content = content.replace(f"%%{key}%%", str(value))
    return content


class Raymarching(Example):
    gl_version = (3, 3)
    window_size = (500, 500)
    aspect_ratio = 1.0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        W = 400
        H = 400
        X = W
        Y = 1
        Z = 1

        triangles = read_obj("smoothMonkey.obj")
        print("constructed triangles")

        camera = Camera(Vector(0, 0, 3), Vector(0, 0, -1))


        consts = {
            "W": W,
            "H": H,
            "X": X + 1,
            "Y": Y,
            "Z": Z,
            "numTriangles": len(triangles),
        }

        context = moderngl.create_standalone_context(require=430)
        compute_shader = context.compute_shader(source('raytracing.gl', consts))

        triangle_data = np.asarray([]).astype('f4')
        for x in triangles:

            triangle_data = np.concatenate((triangle_data, (x.get_data())))

        triangle_buffer = context.buffer(triangle_data)
        triangle_buffer.bind_to_storage_buffer(0)

        pixel_buffer_data = np.zeros((H, W, 4)).astype('f4')
        pixel_buffer = context.buffer(pixel_buffer_data)
        pixel_buffer.bind_to_storage_buffer(1)

        camera_buffer_data = np.zeros(8).astype('f4')
        camera.get_data(camera_buffer_data)

        camera_buffer = context.buffer(camera_buffer_data)
        camera_buffer.bind_to_storage_buffer(2)

        pygame.init()
        screen = pygame.display.set_mode((1600, 1600))



        pixel_data_bytes = pixel_buffer.read()


        compute_shader.run(group_x=W, group_y=H)
        output = np.frombuffer(pixel_buffer.mglo, dtype=np.float32)
        output = output.reshape((H, W, 4))
        output = output[:,:,:3]
        output = np.multiply(output, 255).astype(np.uint8)
        surf = pygame.surfarray.make_surface(output)
        pygame.transform.scale(surf, (1600, 1600), screen)
        pygame.display.flip()



main()
