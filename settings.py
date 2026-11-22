level_1 = [
	'                                                                                                    ',
	'                                                                                                    ',
	'                                                                                                    ',
	'                                      XXXX                                                          ',
	'                        t                                         t                                 ',
	'                   XXXXXXXXX                                   XXXXXXX                              ',
	'                                           t                                          t          G  ',
	'       t        XX                      XXXXXX      XX                       XXXX    XXXX    XXXXXXX',
	' P   XXXXX   t  XX      t     XX         XX        XX       t     XX        XX      XX     XX    ',
	'XXXXXXXXXXXX  XXXXXX  XXXXXX  XXXXXX  XXXXXXXX  XXXXXX  XXXXXX  XXXXXX  XXXXXXXX  XXXXXXXX  XXXXXXXX',
]

level_2 = [
	'                                                                                                    ',
	'                                                                                                    ',
	'                                                                                                    ',
	'                                  XXX                                      XXX                      ',
	'                        t                                       t                                   ',
	'                    XXXXXXXXX                               XXXXXXXXX                             ',
	'                                          t                                          t          G ',
	'       t        XX                     XXXXXXX     XX                      XXXX     XXXX     XXXXX',
	' P   XXXXX   t  XX      t     XX          XX      XX       t     XX         XX       XX      XX ',
	'XXXXXXXXXXXX  XXXXXX  XXXXXX  XXXXXX  XXXXXXXX  XXXXXX  XXXXXX  XXXXXX  XXXXXXXX  XXXXXXXX  XXXXXXXX',
]

level_3 = [
	'                                                                                                    ',
	'                                                                                                    ',
	'                                       XXX                  XXX                                     ',
	'                         t             tXX       t          tXX       t                             ',
	'               XX     XXXXXXX         XXXX     XXXXX      XXXX     XXXXXXX       XX                 ',
	'        t   XX XX                                                             X  XX      t          ',
	'     XXXXXX    XX   t          t              t                 t           X    XX   XXXXXXX     G',
	' P      XX     XX  XXXX     t  XX      t     XXXX X    t       XX      t  X      XX      XX    XXX',
	'XXXXX   XX     XX    XX    XXXXXX     XXXX     XX    XXXXXX  X XX   X XXXX       XX      XX     XX',
	'XXXXX   XX     XX    XX    XXXXXX     XXXX     XX     XXXXXX     XX     XXXX       XX      XX     XX',
]

levels = [level_1, level_2, level_3]
world_map = levels[0]

tile_size = 50
WIDTH, HEIGHT = 1000, len(level_1) * tile_size

# Physics Constants for Mario-style movement
GRAVITY = 0.8
JUMP_SPEED = -15.5
GRAVITY_RELEASE_MULTIPLIER = 2.0