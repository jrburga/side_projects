

FPS = 30
period = FPS/10
G = 1.0
init_particles = 100
screen_size = (1280, 800)


# These basically got scrapped
# Vestiges of an evolving game
cursors =[
    [
        [
            '     XXXXXX     ',
            '   XX      XX   ',
            '  X          X  ',
            ' X            X ',
            ' X            X ',
            'X              X',
            'X              X',
            'X              X',
            'X              X',
            'X              X',
            'X              X',
            ' X            X ',
            ' X            X ',
            '  X          X  ',
            '   XX      XX   ',
            '     XXXXXX     ',
        ],
    (16, 16),
    (7, 7)
    ],

    [
        [
            '    x   ',
            '   x    ',
            '  x     ',
            ' xxx x  ',
            '  x xxx ',
            '     x  ',
            '    x   ',
            '   x    ',
        ],
    (8, 8),
    (3, 3)
    ]
]
# now... I *could* make a tile data decompiler...
# meh
# How many am I going to have to deal with anyway...
tile_data = {
    'hydrospiro': {
        'tiles': [(4, 1), (16, 16)],
        'layer': [ [[0, 1, 2, 3]] ]
                },
    'heliose': {
        'tiles':[(4, 1), (24, 24)],
        'layer':[ [[0, 1, 2, 3]] ]
                },
    'nemesis': {
        'tiles':[(4, 1), (24, 24)],
        'layer':[ [[0, 1, 2, 3]] ]
                }
    }
    
