import os
import sys

game_mode = 1
# Set the game mode here!
# 0 is debug,
# 1 is create
# 2 is play
# 3 is build(pyinstaller windows)
game_path = os.path.abspath("main.py/../../")

scale = 2
music_vol = 0

width = (32 * 16) * scale
height = (32 * 9) * scale

directory = game_path + "/"
if game_mode == 3:
    application_path = os.path.dirname(sys.executable)
    directory = application_path + "/"

tile_set1 = {
    1: directory + "graphics/Spike.png",
    0: directory + "graphics/Block0.png",
    2: directory + "graphics/MiniSpike.png",
    "PlayerMask": directory + "graphics/PlayerMask.png",
    "PlayerIdle": directory + "graphics/PlayerIdle.png",
    "Troll": directory + "graphics/troll.png"
}

tile_set2 = {
    1: directory + "graphics/Spike.png",
    0: directory + "graphics/cave_tile2.png",
    2: directory + "graphics/MiniSpike.png",
    3: directory + "graphics/water.png",
    "troll": directory + "graphics/troll.png",
    "bag": directory + "graphics/felix.png",
    "burto": directory + "graphics/burrito_mountain.png",
    "death_screen": directory + "graphics/death_screen1.png",
    "Save0": directory + "graphics/save0.png",
    "Save1": directory + "graphics/save1.png",
    "bg_sprite_sheet": directory + "graphics/moon_bg_sheet.png",
    "diamondAnim": directory + "graphics/screen_transision_diamond_anim.png",
}

sounds = {
    "Moonsong": directory + "sounds/Moonsong.ogg",
    "death1": directory + "sounds/real_scream.ogg",
    "death2": directory + "sounds/vine-boom.mp3",
    "death3": directory + "sounds/error.mp3",

}

player_sprites = {
    "PlayerMask": directory + "graphics/PlayerMask.png",
    "PlayerDefault": directory + "graphics/PlayerIdleAnim/PlayerIdle0.png",
    "PlayerIdleAnim": directory + "graphics/PlayerIdleAnim",
    "PlayerRunAnim": directory + "graphics/PlayerRunAnim",
    "PlayerJumpAnim": directory + "graphics/PlayerJumpAnim",
    "PlayerFallAnim": directory + "graphics/PlayerFallAnim",
}
