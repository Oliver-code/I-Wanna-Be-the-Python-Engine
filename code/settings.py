import os, sys
game_mode = 1
game_path = os.path.abspath("main.py")

scale = 6

width = scale * 32*4
height = scale * 32*3

directory = "/Users/oliverAccount/PycharmProjects/IWBTripoff/"
if game_mode == 3:
    application_path = os.path.dirname(sys.executable)
    directory = application_path+"/"

image_dict = {
    1: directory+"graphics/Spike.png",
    0: directory+"graphics/Block0.png",
    2: directory+"graphics/MiniSpike.png",
    "PlayerMask": directory+"graphics/PlayerMask.png",
    "PlayerIdle": directory+"graphics/PlayerIdle.png"
}
