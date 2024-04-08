### Change these
# Ball radius in hammer units
radius = 850.0
# (Density)^2 = how many entities should spawn | # 46 seems to be max on my testing_map -> 47 and more crashes
# Actually 40 crashes too if used more than once | smaller values recommended
density = 35.0
# Sphere center (x, y, z)
x0, y0, z0 = 0, 0, 0
# Cfg file directory to create to
dir = "."
# Cfg file name
cfg_name = "Ball_test_autogen"
# Model "models/props_lab/blastdoor001c.mdl" | "models/weapons/shotgun_shell.mdl"
model = "models/props_lab/blastdoor001c.mdl"
# model = "models/weapons/shotgun_shell.mdl"
# model = "props_c17/statue_horse.mdl"
# model = "models/Humans/Group01/male_07.mdl"
classname = "ball_script"
# Method of collision for this entity. (0: None; 6: VPhysics)
solid = "6"
wait = "2"
decimal_places = 3
max_spawns_num = 25

import math

# Rounds a given number to a higher number (needed for round_real)
def round_half_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n*multiplier + 0.5) / multiplier
# Rounds a given number (needs round_half_up to operate)
def round_real(n, decimals=0):
    rounded_abs = round_half_up(abs(n), decimals)
    return math.copysign(rounded_abs, n)

# alpha = latitude (-π;π); beta = longitude (-π/2;π/2)
def x_cordinate(latitude, longitude):
    return str(round((x0 + radius * round(math.sin(longitude), decimal_places) * round(math.cos(latitude), decimal_places)), decimal_places))
def y_cordinate(latitude, longitude):
    return str(round((y0 + radius * round(math.sin(longitude), decimal_places) * round(math.sin(latitude), decimal_places)), decimal_places))
def z_cordinate(latitude, longitude):
    return str(round((z0 + radius * round(math.cos(longitude), decimal_places)), decimal_places))

def pitch(longitude):
    # if longitude <= math.pi/2:
    return str(round_real(longitude / math.pi * 180, decimal_places) +95)
    # else:
    #     return str(round_real(longitude / math.pi * 180, decimal_places) +110)
# def pitch(longitude):
#     return str(round(longitude / math.pi * 90))

def roll(latitude):
    return str(round_real(latitude / math.pi * 180, decimal_places))

def write_entity():
    file.write("\nwait " + wait + "; ent_create prop_dynamic " + "model " + model + " targetname " + "ball_x" +
               x_cordinate(latitude, longitude) + "_y" + y_cordinate(latitude, longitude) + "_z" +
               z_cordinate(latitude, longitude) + " classname " + classname + " solid " + solid)
    file.write("\nent_fire ball_x" + x_cordinate(latitude, longitude) + "_y" + y_cordinate(latitude, longitude) + "_z" +
               z_cordinate(latitude, longitude) + " addoutput " + "\"origin " + x_cordinate(latitude, longitude) + " " +
               y_cordinate(latitude, longitude) + " " + z_cordinate(latitude, longitude) + "\"")
    file.write("\nent_fire ball_x" + x_cordinate(latitude, longitude) + "_y" + y_cordinate(latitude, longitude) +
               "_z" + z_cordinate(latitude, longitude) + " addoutput " + "\"angles " + pitch(longitude) + " " +
               roll(latitude) + "\"")

# Don't change these
spawns_num = 0
file_num = 1
latitude = 0    # -math.pi
longitude = 0   # -math.pi/2

file = open(dir + cfg_name + str(file_num) + ".cfg", "w+")

file.write("con_filter_enable 1; con_filter_text_out \"has no model name\"")
file.write("\nent_fire " + classname + " kill")
file.write("\nwait " + str(10+int(wait)) + "\n")

while latitude <= 2*math.pi:
    while longitude <= math.pi +0.00001:
        if spawns_num >= max_spawns_num:
            file_num += 1
            file.write("\nexec " + cfg_name + str(file_num))
            file.close()
            file = open(dir + cfg_name + str(file_num) + ".cfg", "w+")
            spawns_num = 0
        else:
            if longitude == 0 or round_real(longitude,3) == round_real(math.pi,3):
                longitude += math.pi/(density-1)
            else:
                write_entity()
                longitude += math.pi/(density-1)
                spawns_num += 1
    latitude += 2 * math.pi / (density - 1)
    longitude = 0

file.write("\n\nwait 10; con_filter_enable 0; con_filter_text_out \"\"")
file.close()

file = open(dir + cfg_name + str(file_num) + ".cfg")
for line in file.readlines():
    print(line.strip())
file.close()
