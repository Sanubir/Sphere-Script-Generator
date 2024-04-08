import math

# Rounds a given number to a higher number (needed for round_real)
def round_half_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n*multiplier + 0.5) / multiplier

# Rounds a given number (needs round_half_up to operate)
def round_real(n, decimals=0):
    rounded_abs = round_half_up(abs(n), decimals)
    return math.copysign(rounded_abs, n)

# Writes to a file a creation of an entity with its parameters
def write_entity_pos_y(x,y,z,pitch,roll):
    file.write("\nwait " + wait + "; ent_create prop_dynamic " + "model " + model + " targetname " +
            ("ball_x" + str(round_real(x, decimal_places)) + "_y+_z" + str(round_real(z, decimal_places))) +
            " classname " + classname)
    file.write("\nwait " + wait + "; ent_fire ball_x" + str(round_real(x, decimal_places)) + "_y+_z" + str(round_real(z, decimal_places)) +
            " addoutput " + "\"origin " + str(round_real(x, decimal_places)) + " " +
               str(round_real(y, decimal_places)) + " " + str(round_real(z, decimal_places)) + "\"")
    file.write("\nwait " + wait + "; ent_fire ball_x" + str(round_real(x, decimal_places)) + "_y+_z" + str(round_real(z, decimal_places)) +
            " addoutput " + "\"angles " + str(round_real(pitch, decimal_places)) + " " +
               str(round_real(roll, decimal_places)) + "\"")

# Write to a file a creation of an entity with its parameters
def write_entity_neg_y(x,y,z,pitch,roll):
    file.write("\nwait " + wait + "; ent_create prop_dynamic " + "model " + model + " targetname " +
            ("ball_x" + str(round_real(x, decimal_places)) + "_y-_z" + str(round_real(z, decimal_places))) +
            " classname " + classname)
    file.write("\nwait " + wait + "; ent_fire ball_x" + str(round_real(x, decimal_places)) + "_y-_z" + str(round_real(z, decimal_places)) +
            " addoutput " + "\"origin " + str(round_real(x, decimal_places)) + " " +
               str(round_real(-y, decimal_places)) + " " + str(round_real(z, decimal_places)) + "\"")
    file.write("\nwait " + wait + "; ent_fire ball_x" + str(round_real(x, decimal_places)) + "_y-_z" + str(round_real(z, decimal_places)) +
            " addoutput " + "\"angles " + str(round_real(pitch, decimal_places)) + " " +
               str(round_real(-roll, decimal_places)) + "\"")

### Change these
# Ball radius in hammer units
radius = 200.0
# Density = how many points on x and z axes (choose odd numbers for rounder effect)
density = 15.0
# Sphere center (x, y, z)
x0, y0, z0 = 0, 0, 0
# Cfg file directory to create to
dir = "."
# Cfg file name
cfg_name = "Ball_test_autogen"
model = "models/props_lab/blastdoor001c.mdl"
classname = "ball_script"
wait = "100"
decimal_places = 3
max_spawns_num = 12

### Don't change these
# x starts from center adjusted position
x = -radius + x0
# z starts from center adjusted position
z = -radius + z0
# pitch and roll starts
pitch = -90
roll = 0
spawns_num = 0
file_num = 1

file = open(dir + cfg_name + str(file_num) + ".cfg", "w+")

file.write("ent_fire " + classname + " kill")
file.write("\nwait " + wait + "\n")

# First loop goes through z axis from botttom to the top
while round_real(z, decimal_places+1) <= radius + z0:
    # Computes x from the equation of a circle: (x-x0)^2 + (z-z0)^2 = r^2 => x = sqrt[r^2 - (z-z0)^2] + x0
    r = math.sqrt((radius **2) - (round_real((z - z0) ** 2, decimal_places))) + x0
    x = -r
    # Checks if r=0 as it would break the loop
    if r == 0:
        y = math.sqrt((r ** 2) - (round_real((x - x0) ** 2, decimal_places + 1))) + y0
        write_entity_pos_y(x, y, z, pitch, roll)
        write_entity_neg_y(x, y, z, pitch, roll)
    else:
        # Second loop nested inside goes through x axis for every z cord, computing y and writing to a file
        while round_real(x, decimal_places+1) <= r:
            if spawns_num >= max_spawns_num:
                file_num += 1
                file.write("\nexec " + cfg_name + str(file_num))
                file.close()
                file = open(dir + cfg_name + str(file_num) + ".cfg", "w+")
                spawns_num = 0
            else:
                # Computes y from the equation of a circle: (x-x0)^2 + (y-y0)^2 = r^2 => y = sqrt[r^2 - (x-x0)^2] + y0
                y = math.sqrt((r ** 2)+0.000001 - (round_real((x - x0) ** 2, decimal_places + 1))) + y0
                write_entity_pos_y(x,y,z,pitch,roll)
                write_entity_neg_y(x,y,z,pitch,roll)
            # Adjusts roll and x
            roll -= (180 / (density-1))
            x += (2 * r / (density-1))
            spawns_num += 1
    z += (2 * radius / (density-1))
    pitch += (180 / (density-1))
    roll = 0

file.close()

# file = open(dir)
# for line in file.readlines():
#     print(line.strip())
# file.close()
