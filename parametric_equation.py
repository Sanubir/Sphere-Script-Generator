### Change these
# Ball radius in hammer units
radius = 50.0
# (Density)^2 = how many entities should spawn | # 46 seems to be max on my testing_map -> 47 and more crashes
# Actually 40 crashes too if used more than once | smaller values recommended
density = 30.0
# Sphere center (x, y, z)
x0, y0, z0 = 0, 0, 0
# Cfg file directory to create to
dir = "."
# Cfg file name
cfg_name = "Ball_test_autogen"
# Model "models/props_lab/blastdoor001c.mdl" | "models/weapons/shotgun_shell.mdl"
model = "models/weapons/shotgun_shell.mdl"
classname = "ball_script"
wait = "10"
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

def x_cordinate(alpha, beta):
    return round((x0 + radius * round(math.cos(alpha), decimal_places) * round(math.cos(beta), decimal_places)), decimal_places)
def y_cordinate(alpha, beta):
    return round((y0 + radius * round(math.sin(beta), decimal_places)), decimal_places)
def z_cordinate(alpha, beta):
    return round((z0 + radius * round(math.sin(alpha), decimal_places) * round(math.cos(beta), decimal_places)), decimal_places)

def roll(alpha):
    if alpha <= -math.pi:
        return -round(alpha / math.pi * 0)
    else:
        return round(alpha / math.pi * 0)
def pitch(beta):
    if beta <= -math.pi/2:
        return -round(beta / math.pi/2 * 0)
    else:
        return round(beta / math.pi/2 * 0)

def write_enity():
    file.write("\nwait " + wait + "; ent_create prop_dynamic " + "model " + str(model) + " targetname " +
               "ball_x" + str(x_cordinate(alpha, beta)) + "_y" + str(y_cordinate(alpha, beta)) + "_z" +
               str(z_cordinate(alpha, beta)) + " classname " + str(classname))
    file.write("\nent_fire ball_x" + str(x_cordinate(alpha, beta)) + "_y" + str(y_cordinate(alpha, beta)) +
               "_z" + str(z_cordinate(alpha, beta)) + " addoutput " + "\"origin " + str(x_cordinate(alpha, beta)) +
               " " + str(y_cordinate(alpha, beta)) + " " + str(z_cordinate(alpha, beta)) + "\"")
    file.write("\nent_fire ball_x" + str(x_cordinate(alpha, beta)) + "_y" + str(y_cordinate(alpha, beta)) + "_z" +
               str(z_cordinate(alpha, beta)) + " addoutput " + "\"angles " +
               str(pitch(beta)) + " " + str(roll(alpha)) + "\"")

# Don't change these
spawns_num = 0
file_num = 1
alpha = -math.pi
beta = -math.pi/2

file = open(dir + cfg_name + str(file_num) + ".cfg", "w+")

file.write("ent_fire " + classname + " kill")
file.write("\nwait " + wait + "\n")

while alpha <= math.pi:
    while beta <= math.pi/2 +0.00001:
        if spawns_num >= max_spawns_num:
            file_num += 1
            file.write("\nexec " + cfg_name + str(file_num))
            file.close()
            file = open(dir + cfg_name + str(file_num) + ".cfg", "w+")
            spawns_num = 0
        else:
            if beta == -math.pi or beta == math.pi:
                write_enity()
                beta += math.pi
                spawns_num += 1
            else:
                write_enity()
                beta += math.pi/(density-1)
                spawns_num += 1
    alpha += 2 * math.pi / (density - 1)
    beta = -math.pi/2

file.close()

file = open(dir + cfg_name + str(file_num) + ".cfg")
for line in file.readlines():
    print(line.strip())
file.close()
