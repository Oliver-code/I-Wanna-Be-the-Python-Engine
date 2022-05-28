import os
import sys

game_mode = 1
game_path = os.path.abspath("main.py/../../")

scale = 2

width = (32*16)*scale
height = (32*9)*scale

directory = game_path + "/"
if game_mode == 3:
    application_path = os.path.dirname(sys.executable)
    directory = application_path+"/"

tile_set1 = {
    1: directory+"graphics/Spike.png",
    0: directory+"graphics/Block0.png",
    2: directory+"graphics/MiniSpike.png",
    "PlayerMask": directory+"graphics/PlayerMask.png",
    "PlayerIdle": directory+"graphics/PlayerIdle.png",
    "Troll": directory+"graphics/troll.png"
}

tile_set2 = {
    1: directory+"graphics/Spike.png",
    0: directory+"graphics/cave_tile2.png",
    2: directory+"graphics/MiniSpike.png",
    3: directory + "graphics/water.png",
    "PlayerMask": directory+"graphics/PlayerMask.png",
    "PlayerIdle": directory+"graphics/PlayerIdle.png",
    "troll": directory+"graphics/troll.png",
    "bag": directory+"graphics/felix.png",
    "burto": directory+"graphics/burrito_mountain.png",
    "death_screen": directory+"graphics/death_screen1.png",
    "Save0": directory+"graphics/save0.png",
    "Save1": directory + "graphics/save1.png",
    "bg_sprite_sheet": directory + "graphics/moon_bg_sheet.png",

}

sounds = {
    "Moonsong": directory+"sounds/Moonsong.ogg",
    "death": directory+"sounds/vine-boom.mp3",
}
