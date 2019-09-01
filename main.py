import moderngl
import numpy as np
import pygame

from read_obj import read_obj


def source(uri, consts):
    ''' read gl code '''
    with open(uri, 'r') as fp:
        content = fp.read()

    # feed constant values
    for key, value in consts.items():
        content = content.replace(f"%%{key}%%", str(value))
    return content


def main():

    W = 400
    H = 400
    X = W
    Y = 1
    Z = 1

    triangles = read_obj("smoothMonkey.obj")

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

    triangle_data = np.asarray([0]).astype('f4')
    for x in triangles:

        triangle_data = np.concatenate((triangle_data, (x.get_data())))

    triangle_buffer = context.buffer(triangle_data)
    pixel_buffer_data = np.zeros((H, W, 4)).astype('f4')
    pixel_buffer = context.buffer(pixel_buffer_data)
    pixel_buffer.bind_to_storage_buffer(1)

    compute_shader.run(group_x=400, group_y=400)

    pygame.init()

    output = np.frombuffer(pixel_buffer.read(), dtype=np.float32)
    output = output.reshape((H, W, 4))
    output = output[:,:,:3]

    output = np.multiply(output, 255).astype(np.uint8)
    #output = np.reshape(output, (-1, W, 4))

    print(output)

    surf = pygame.surfarray.make_surface(output)

    screen = pygame.display.set_mode((800, 800))
    pygame.transform.scale(surf, (800, 800), screen)
    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

main()
