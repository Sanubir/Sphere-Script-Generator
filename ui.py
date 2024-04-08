import tkinter as tk
from tkinter import *
from tkinter import filedialog as fd
from tkinter import ttk
import subprocess
import os
import platform
from tkinter import messagebox
import math


def browse():
    filedir = fd.askdirectory(title="Select directory for output",
                              initialdir=r"C:\Program Files\Steam\steamapps\common\\")
    if filedir != "":
        field_output.delete(0, tk.END)
        field_output.insert(0, filedir + "/")


def open_script():
    filepath = field_output.get() + field_cfg_name.get() + "1.cfg"
    print(filepath)
    if filepath == "":
        tk.messagebox.showerror(title="Error", message="Output field empty")
    else:
        try:
            if platform.system() == 'Darwin':  # macOS
                subprocess.call(('open', filepath))
            elif platform.system() == 'Windows':  # Windows
                os.startfile(filepath)
            else:  # linux variants
                subprocess.call(('xdg-open', filepath))
        except FileNotFoundError:
            tk.messagebox.showerror(title="Error",
                                    message="Specified file doesn't exist. \nMake sure to generate it first.")


# Rounds a given number to a higher number (needed for round_real)
def round_half_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n * multiplier + 0.5) / multiplier

# Rounds a given number (needs round_half_up to operate)
def round_real(n, decimals=0):
    rounded_abs = round_half_up(abs(n), decimals)
    return math.copysign(rounded_abs, n)

# alpha = latitude (-π;π); beta = longitude (-π/2;π/2)
def x_coordinate(latitude, longitude):
    return str(round(
        (x0 + radius * round(math.sin(longitude), decimal_places) * round(math.cos(latitude), decimal_places)),
        decimal_places))

def y_coordinate(latitude, longitude):
    return str(round(
        (y0 + radius * round(math.sin(longitude), decimal_places) * round(math.sin(latitude), decimal_places)),
        decimal_places))

def z_coordinate(longitude):
    return str(round((z0 + radius * round(math.cos(longitude), decimal_places)), decimal_places))

def pitch(longitude):
    # if longitude <= math.pi/2:
    return str(round_real(longitude / math.pi * 180, decimal_places) + 95)
    # else:
    #     return str(round_real(longitude / math.pi * 180, decimal_places) +110)

# def pitch(longitude):
#     return str(round(longitude / math.pi * 90))

def roll(latitude):
    return str(round_real(latitude / math.pi * 180, decimal_places))

def write_entity():
    file.write("\nwait " + wait + "; ent_create prop_dynamic " + "model " + model + " targetname " + "ball_x" +
               x_coordinate(latitude, longitude) + "_y" + y_coordinate(latitude, longitude) + "_z" +
               z_coordinate(longitude) + " classname " + classname + " solid " + solid)
    file.write(
        "\nent_fire ball_x" + x_coordinate(latitude, longitude) + "_y" + y_coordinate(latitude, longitude) + "_z" +
        z_coordinate(longitude) + " addoutput " + "\"origin " + x_coordinate(latitude, longitude) + " " +
        y_coordinate(latitude, longitude) + " " + z_coordinate(longitude) + "\"")
    file.write("\nent_fire ball_x" + x_coordinate(latitude, longitude) + "_y" + y_coordinate(latitude, longitude) +
               "_z" + z_coordinate(longitude) + " addoutput " + "\"angles " + pitch(longitude) + " " +
               roll(latitude) + "\"")


def generate_script():
    # Change these
    # Ball radius in hammer units
    radius = int(box_radius.get())
    # (Density)^2 = how many entities should spawn | # 46 seems to be max on my testing_map -> 47 and more crashes
    # Actually 40 crashes too if used more than once | smaller values recommended
    density = int(box_density.get())
    # Sphere center (x, y, z)
    x0, y0, z0 = int(box_center_x.get()), int(box_center_y.get()), int(box_center_z.get())
    # Cfg file directory to create to
    dir = field_output.get()
    # Cfg file name
    cfg_name = field_cfg_name.get()
    # Model "models/props_lab/blastdoor001c.mdl" | "models/weapons/shotgun_shell.mdl"
    model = box_model.get()
    # model = "models/weapons/shotgun_shell.mdl"
    # model = "props_c17/statue_horse.mdl"
    # model = "models/Humans/Group01/male_07.mdl"
    classname = field_classname.get()
    # Method of collision for this entity. (0: None; 6: VPhysics)
    if cb.get():
        solid = "6"
    else:
        solid = "0"
    wait = "2"
    decimal_places = 3
    max_spawns_num = 25

    # Don't change these
    spawns_num = 0
    file_num = 1
    latitude = 0  # -math.pi
    longitude = 0  # -math.pi/2

    file = open(dir + cfg_name + str(file_num) + ".cfg", "w+")

    file.write("con_filter_enable 1; con_filter_text_out \"has no model name\"")
    file.write("\nent_fire " + classname + " kill")
    file.write("\nwait " + str(10 + int(wait)) + "\n")

    while latitude <= 2 * math.pi:
        while longitude <= math.pi + 0.00001:
            if spawns_num >= max_spawns_num:
                file_num += 1
                file.write("\nexec " + cfg_name + str(file_num))
                file.close()
                file = open(dir + cfg_name + str(file_num) + ".cfg", "w+")
                spawns_num = 0
            else:
                if longitude == 0 or round_real(longitude, 3) == round_real(math.pi, 3):
                    longitude += math.pi / (density - 1)
                else:
                    write_entity()
                    longitude += math.pi / (density - 1)
                    spawns_num += 1
        latitude += 2 * math.pi / (density - 1)
        longitude = 0

    file.write("\n\nwait 10; con_filter_enable 0; con_filter_text_out \"\"")
    file.close()

    file = open(dir + cfg_name + str(file_num) + ".cfg")
    for line in file.readlines():
        print(line.strip())
    file.close()


def generate_button():
    filepath = field_output.get()
    if filepath == "":
        tk.messagebox.showerror(title="Error", message="Output field empty")
    else:
        answer = tk.messagebox.askokcancel(title="Confirmation",
                                           message=
                                           "Do you wish to proceed? "
                                           "\nMake sure the \"Output\" field is set correctly "
                                           "as any existing files with specified name will be overwritten.")
        if answer:
            generate_script()
            tk.messagebox.showinfo \
                (title="Success",
                 message="Generated config files to:\n" + filepath +
                 "\nYou can now \"exec " + field_cfg_name.get() + "1\" in your game of choice.")


def on_enter(e):
    button_browse.config(background='#E5F1FB')


def on_leave(e):
    button_browse.config(background='#F0F0F0')


def on_enter1(e):
    button_open.config(background='#E5F1FB')


def on_leave1(e):
    button_open.config(background='#F0F0F0')


def on_enter2(e):
    button_generate.config(background='#E5F1FB')


def on_leave2(e):
    button_generate.config(background='#F0F0F0')


root = tk.Tk()
root.title("Sphere Script Generator (pre-alpha wip UI test)")
# root.iconbitmap('sphere_icon.ico')
root.resizable(False, False)

frame_output = tk.Frame(root)
frame_output.grid(row=0, column=0, columnspan=2)

label_output = tk.Label(frame_output, text="Output")
label_output.grid(row=0, column=0, sticky=W, padx=12, pady=8)
field_output = tk.Entry(frame_output, width=42, borderwidth=1, relief="solid")
field_output.grid(row=0, column=1, columnspan=3)
button_browse = tk.Button(frame_output, text="Browse", padx=14, borderwidth=1, relief="solid", command=browse)
button_browse.grid(row=0, column=4, padx=8)
button_browse.bind('<Enter>', on_enter)
button_browse.bind('<Leave>', on_leave)

label_cfg_name = tk.Label(frame_output, text="Cfg name")
label_cfg_name.grid(row=1, column=0, sticky=W, padx=12)
field_cfg_name = tk.Entry(frame_output, width=33, borderwidth=1, relief="solid")
field_cfg_name.grid(row=1, column=1, columnspan=3)
field_cfg_name.insert(0, "Ball_test_autogen")
label_cfg_name_hint = tk.Label(frame_output, text="Config files naming will be <cfg_name><no.>", foreground="gray")
label_cfg_name_hint.grid(row=2, column=1, columnspan=3)

frame_sphere = tk.LabelFrame(root, text="Sphere parameters", padx=5, pady=5)
frame_sphere.grid(row=1, column=0, sticky=W, padx=10, pady=8, columnspan=2)

label_radius = tk.Label(frame_sphere, text="Radius", padx=8)
label_radius.grid(row=0, column=0, sticky=W)
box_radius = tk.Spinbox(frame_sphere, from_=1, to=99999, wrap=True, width=5)
box_radius.grid(row=0, column=1)
box_radius.delete(0)
box_radius.insert(0, 850)

label_density = tk.Label(frame_sphere, text="Density", padx=8)
label_density.grid(row=1, column=0, sticky=W)
box_density = tk.Spinbox(frame_sphere, from_=1, to=100, wrap=True, width=5)
box_density.grid(row=1, column=1)
box_density.delete(0)
box_density.insert(0, 35)

label_center = tk.Label(frame_sphere, text="Center (xyz)", padx=8)
label_center.grid(row=2, column=0, sticky=W)
box_center_x = tk.Spinbox(frame_sphere, from_=0, to=99999, wrap=True, width=5)
box_center_x.grid(row=2, column=1)
box_center_y = tk.Spinbox(frame_sphere, from_=0, to=99999, wrap=True, width=5)
box_center_y.grid(row=2, column=2)
box_center_z = tk.Spinbox(frame_sphere, from_=0, to=99999, wrap=True, width=5)
box_center_z.grid(row=2, column=3)

label_model = tk.Label(frame_sphere, text="Model", padx=8)
label_model.grid(row=3, column=0, sticky=W)
box_model = ttk.Combobox(frame_sphere, width=52)
box_model.grid(row=3, column=1, sticky=W, columnspan=99)
box_model['values'] = ('models/props_lab/blastdoor001c.mdl',
                       'models/weapons/shotgun_shell.mdl',
                       'models/Humans/Group01/male_07.mdl')
box_model.insert(0, 'models/props_lab/blastdoor001c.mdl')

label_solid = tk.Label(frame_sphere, text="Solid", padx=8)
label_solid.grid(row=4, column=0, sticky=W)
cb = IntVar()
check_solid = tk.Checkbutton(frame_sphere, variable=cb)
check_solid.grid(row=4, column=1, sticky=W)
check_solid.select()

frame_script = tk.LabelFrame(root, text="Sphere parameters", padx=5, pady=5)
frame_script.grid(row=2, column=0, sticky=W, padx=10, pady=4, columnspan=2)

label_classname = tk.Label(frame_script, text="Script classname")
label_classname.grid(row=0, column=0, sticky="W", padx=12)
field_classname = tk.Entry(frame_script, width=33, borderwidth=1, relief="solid")
field_classname.grid(row=0, column=2, columnspan=2)
field_classname.insert(0, "ball_script")
label_classname_hint = tk.Label(frame_script, text="Entities' classname will be <classname>", foreground="gray")
label_classname_hint.grid(row=1, column=2, columnspan=3)

label_wip = tk.Label(frame_script, text="\nWork in progress\nUnder construction (as everything else)", foreground="gray")
label_wip.grid(row=2, column=0, columnspan=99)

frame_author = tk.Frame(root)
frame_author.grid(row=3, column=0, sticky=W, padx=10, pady=4)
label_author = tk.Label(frame_author, text="by Sanubir - 2022")
label_author.grid(row=0, column=0, sticky=W)

frame_generate = tk.Frame(root)
frame_generate.grid(row=3, column=1, sticky=E, padx=10, pady=4)
button_open = tk.Button(frame_generate, text="Open Script", padx=4, borderwidth=1, relief="solid", command=open_script)
button_open.grid(row=0, column=0, sticky=E, padx=4, pady=8)
button_open.bind('<Enter>', on_enter1)
button_open.bind('<Leave>', on_leave1)
button_generate = tk.Button(frame_generate, text="Generate", padx=8, borderwidth=1, relief="solid",
                            command=generate_button)
button_generate.grid(row=0, column=1, sticky=E, padx=4)
button_generate.bind('<Enter>', on_enter2)
button_generate.bind('<Leave>', on_leave2)

tk.messagebox.showinfo \
    (title="Info",
     message=
     "Good morning and welcome to the Sanubir's Script Generator System. "
     "This automated program is provided for the usage and convenience of the Sanubir's Script Generator users. "
     "Please keep your cursor inside the program at all times. "
     "A reminder that the Sanubir's Script Generator is a WIP and more features will be available in the future. "
     "Remember, this is a prototype and thus may cause unexpected behaviour if used incorrectly. "
     "Work safe, work smart. Your future depends on it. "
     "Now arriving at destination sector and usage freedom. "
     "Before exiting the program, be sure to check your area for output belongings. "
     "Thank you and have a very safe and productive day.")

root.mainloop()

# My hope is that this code is so awful I'm never allowed to write UI code again. Kappa

