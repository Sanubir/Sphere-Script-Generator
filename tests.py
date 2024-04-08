import tkinter as tk

root = tk.Tk()

width_of_window = 500
height_of_window = 500

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = (screen_width / 2 - width_of_window / 2)
y_coordinate = (screen_height / 2 - height_of_window / 2)
root.geometry("%dx%d+%d+%d" % (width_of_window, height_of_window, x_coordinate, y_coordinate))

frame = tk.Frame(root, width=300, height=300, bg="red")
frame.grid()
frame.grid_propagate(False)

label = tk.Label(frame, text="Test")
label.grid()

root.mainloop()
