# import  pygame
#
# def load_data(lines):
#     data_file = open("all_saves", "r")
#     data_list = []
#     line = lines
#     if lines < 1:
#         line = 1
#     for i in range(line):
#         data_list = data_file.readline()
#     data_file.close()
#
#     tiles = pygame.sprite.Group()
#     killers = pygame.sprite.Group()
#
#     concat = ""
#     index = 0
#     temp = []
#     for letter in str(data_list):
#         if letter.isdigit():
#             concat += letter
#         elif letter == ",":
#             if concat:
#                 temp.append(int(concat))
#             concat = ""
#         elif letter == ")":
#             temp.append(int(concat))
#             concat = ""
#
#             if index == 0:
#                 tiles.add(main.Block((temp[-2], temp[-1])))
#             elif index == 1:
#                 killers.add(main.Killer((temp[-3], temp[-2]), start_angle=temp[-1]))
#             temp.clear()
#         elif letter == "]":
#             index += 1
#         else:
#             concat = ""
#
#     return tiles, killers
#
# room1 = {
#     "tiles" : [load_data(0)[0]],
#     "killers" : [load_data(0)[1]],
#     "swag" : room1.killers
# }