from tkinter import *
import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox
from PIL import Image, ImageTk
import io
from itertools import compress
from brush import Brush
import dialogue_windows

# ------------------- Initialization -------------------

# app initialization
root = tk.Tk()
root.title('Paint')
root.geometry("1100x700")
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

# dynamic elements
color_button_primary = None
color_button_secondary = None

# ui initialization
def ui_setup():
    global color_button_primary, color_button_secondary

    def initialize_frame(parent):
        return Frame(parent, height=100, width=100, relief=SUNKEN, borderwidth=3)

    def sort_frame(nested_elements, sortBy):
        for element in nested_elements:
            if sortBy == "row":
                element.grid(row=nested_elements.index(element), column=0)
            else:
                element.grid(row=0, column=nested_elements.index(element), sticky='n')

    # Frame 1 - Tools

    tools_parent_frame = Frame(root, height=100, width=1100 )
    tools_parent_frame.grid(row=0 , column=0, sticky=NW)

    # file frame

    file_frame = initialize_frame(tools_parent_frame)
    file_label = Label(file_frame, text='File', width=10, font=('Segoe UI', 9, 'bold'))
    save_button = Button(file_frame, text="Save", width=10, command=save_image)
    new_button = Button(file_frame, text="New", width=10, command=new)
    clear_button = Button(file_frame, text="Clear", width=10, command=clear)
    sort_frame([file_label, save_button, new_button, clear_button], "row")

    # actions frame

    actions_frame = initialize_frame(tools_parent_frame)
    actions_label = Label(actions_frame, text='Actions', width=10, font=('Segoe UI', 9, 'bold'))
    undo_button = Button(actions_frame, text="Undo", width=10, command=undo)
    redo_button = Button(actions_frame, text="Redo", width=10, command=redo)
    sort_frame([actions_label, undo_button, redo_button], "row")

    # tools frame

    tools_frame = initialize_frame(tools_parent_frame)
    tools_label = Label(tools_frame , text="Tools", width=10, font=('Segoe UI', 9, 'bold'))
    brush_button = Button(tools_frame, text="Brush", width=10, height=1, command=lambda: set_tool('brush'))
    eraser_button = Button(tools_frame, text="Eraser", width=10, height=1, command=lambda: set_tool('eraser'))
    tool_size_button = Button(tools_frame, text="Tool size", width=10, height=1, command=select_tool_size)
    sort_frame([tools_label, brush_button, eraser_button, tool_size_button], "row")


    # colors frame

    color_frame = initialize_frame(tools_parent_frame)
    color_label = Label(color_frame , text="Color", width=10, font=('Segoe UI', 9, 'bold'))
    background_color_button = Button(color_frame, text="Background", width=10, command=set_background_color)
    color_button_primary = Button(color_frame, text="", bg=colors[0], width=10, command=set_primary_color)
    color_button_secondary = Button(color_frame, text="", bg=colors[1], width=10, command=set_secondary_color)
    sort_frame([color_label, background_color_button, color_button_primary, color_button_secondary], "row")

    # shapes frame

    shapes_frame = initialize_frame(tools_parent_frame)
    shapes_label = Label(shapes_frame, text='Shapes', width=10, font=('Segoe UI', 9, 'bold'))
    line_button = Button(shapes_frame, text="Line", width=10, command=lambda: set_tool('line'))
    rectangle_button = Button(shapes_frame, text="Rectangle", width=10, command=lambda: set_tool('rectangle'))
    ellipse_button = Button(shapes_frame, text="Ellipse", width=10, command=lambda: set_tool('ellipse'))
    sort_frame([shapes_label, line_button, rectangle_button, ellipse_button], "row")

    # text frame

    text_frame = initialize_frame(tools_parent_frame)
    text_label = Label(text_frame, text="Text", width=10, font=('Segoe UI', 9, 'bold'))
    configure_text_button = Button(text_frame, text="Configure text", width=10, command=configure_text)
    insert_text_button = Button(text_frame, text="Insert text", width=10, command=lambda: set_tool('text'))
    sort_frame([text_label, configure_text_button, insert_text_button], "row")

    # image frame

    image_frame = initialize_frame(tools_parent_frame)
    image_label = Label(image_frame, text='Image', width=10, font=('Segoe UI', 9, 'bold'))
    insert_image_button = Button(image_frame, text="Insert image", width=10, command=insert_image)
    remove_image_button = Button(image_frame, text="Remove image", width=10, command=remove_image)
    sort_frame([image_label, insert_image_button, remove_image_button], "row")

    sort_frame([file_frame, actions_frame, tools_frame, color_frame, shapes_frame, text_frame, image_frame], "column")

    # Frame 2 - Canvas

    canvas_frame = Frame(root , height=600 , width=1100, bg="yellow")
    canvas_frame.grid(row=1 , column=0, sticky='nsew')
    canvas_frame.grid_rowconfigure(0, weight=1)
    canvas_frame.grid_columnconfigure(0, weight=1)

    canvas = Canvas(canvas_frame, height=600 , width=1100, bg="white")
    canvas.grid(row=0, column=0, sticky='nsew')

    return canvas

# binding controls to keys
def keybinds_setup(canvas):
    canvas.bind('<ButtonPress-1>', start_drawing)
    canvas.bind('<B1-Motion>', draw)
    canvas.bind('<ButtonRelease-1>', stop_drawing)
    canvas.bind('<ButtonPress-3>', start_drawing_secondary)
    canvas.bind('<B3-Motion>', draw_secondary)
    canvas.bind('<ButtonRelease-3>', stop_drawing_secondary)
    canvas.bind('<Control-Z>', undo)
    canvas.bind('<Control-z>', undo)
    canvas.bind('<Control-Y>', redo)
    canvas.bind('<Control-y>', redo)

#brushes
brush = Brush('brush', None, 2, 'black')
brush_secondary = Brush('brush', None, 2, 'blue')

#helper arrays
undo_stack, redo_stack = [], []
brush_shapes = []

#global variables
colors = ["black", "blue"]
background_color = "white"
image_id = None
selected_brush = None

# ------------------- Functions -------------------

# tools functions

def set_tool(tool):
    global brush, brush_secondary
    brush.set_tool(tool)
    brush_secondary.set_tool(tool)

def select_tool_size():
    global brush, brush_secondary
    dialogue = dialogue_windows.ToolSize(root, brush.tool_size)

    root.wait_window(dialogue)
    value = dialogue.value
    if value:
        brush.set_tool_size(value)
        brush_secondary.set_tool_size(value)

def configure_text():
    global brush, brush_secondary
    styles = ['italic', 'bold', 'underline', 'overstrike']
    dialogue = dialogue_windows.ConfigureText(root)

    root.wait_window(dialogue)
    values = dialogue.values
    if values:
        selected_styles = list(compress(styles, values[2]))
        brush.set_text(values[0])
        brush.set_font(values[1])
        brush.set_styles(selected_styles)
        brush_secondary.set_text(values[0])
        brush_secondary.set_font(values[1])
        brush_secondary.set_styles(selected_styles)

def set_primary_color():
    global brush, colors
    color = colorchooser.askcolor(title="Select Color")[1]
    if color:
        brush.set_color(color)
        colors[0] = color
        color_button_primary['bg'] = color

def set_secondary_color():
    global brush_secondary, colors
    color = colorchooser.askcolor(title="Select Color")[1]
    if color:
        brush_secondary.set_color(color)
        colors[1] = color
        color_button_secondary['bg'] = color

def set_background_color():
    global background_color
    color = colorchooser.askcolor(title="Select Color")[1]
    if color:
        background_color = color
        canvas.config(bg=background_color)

def insert_image():
    global image_id
    file_path = filedialog.askopenfilename(title='Select image', filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])

    if file_path:
        image = Image.open(file_path).resize((1100, 600))
        tk_image = ImageTk.PhotoImage(image)
        if image_id:
            canvas.delete(image_id)
        image_id = canvas.create_image(0, 0, image=tk_image, anchor='nw')
        canvas.image = tk_image

def remove_image():
    global image_id
    if image_id:
        canvas.delete(image_id)
        image_id = None

def save_image():
    file_path = filedialog.asksaveasfilename(defaultextension=".png")
    
    ps = canvas.postscript(colormode='color')
    try:
        img = Image.open(io.BytesIO(ps.encode('utf-8')))
        img.save(file_path)
    except Exception as e:
        print(f'Error saving file: {e}')

def clear():
    if messagebox.askyesno("Paint" , "Are you sure you want to clear everything?"):
        canvas.delete('all')
        canvas.config(bg="white")

def new():
    if messagebox.askyesno("Paint" , "Are you sure you want to make a new drawing?"):
        if messagebox.askyesno("Paint" , "Do you want to save your drawing before clearing it?"): save_image()
        canvas.delete('all')
        canvas.config(bg="white")

def undo(*args):
    try:
        redo_stack.append(undo_stack.pop())
        if isinstance(redo_stack[-1], list):
            for shape in redo_stack[-1]:
                canvas.itemconfig(shape, state="hidden")
        else:
            canvas.itemconfig(redo_stack[-1], state="hidden")
    except Exception:
        print("Undo stack is empty")

def redo(*args):
    try:
        undo_stack.append(redo_stack.pop())
        if isinstance(undo_stack[-1], list):
            for shape in undo_stack[-1]:
                canvas.itemconfig(shape, state="normal")
        else:
            canvas.itemconfig(undo_stack[-1], state="normal")
    except Exception:
        print("Redo stack is empty")

# drawing functions

def start_drawing_secondary(event):
    start_drawing(event, True)

def draw_secondary(event):
    draw(event, True)

def stop_drawing_secondary(event):
    stop_drawing(event, True)

def start_drawing(*args):
    global selected_brush
    selected_brush = brush
    try:
        if args[1]:
            selected_brush = brush_secondary
    except Exception:
        pass
    selected_brush.set_last_point(args[0].x, args[0].y)
    selected_brush.set_current_point(args[0].x, args[0].y)

    if selected_brush.current_tool == "line":
        selected_brush.current_shape = draw_line(selected_brush)
    elif selected_brush.current_tool == "rectangle":
        selected_brush.current_shape = draw_rect(selected_brush)
    elif selected_brush.current_tool == "ellipse":
        selected_brush.current_shape = draw_ellipse(selected_brush)

def draw(*args):
    global selected_brush
    selected_brush.set_current_point(args[0].x, args[0].y)
    if selected_brush.current_tool == 'brush' or selected_brush.current_tool == 'eraser':
        selected_brush.current_shape = canvas.create_polygon(selected_brush.last_point[0],
                                                    selected_brush.last_point[1],
                                                    selected_brush.current_point[0],
                                                    selected_brush.current_point[1],
                                                    width = selected_brush.tool_size,
                                                    outline = selected_brush.selected_color if selected_brush.current_tool == 'brush' else background_color)
        brush_shapes.append(selected_brush.current_shape)
        selected_brush.last_point = selected_brush.current_point
    elif selected_brush.current_tool == 'line':
        canvas.delete("preview")
        selected_brush.current_shape = draw_line(selected_brush)
    elif selected_brush.current_tool == "rectangle":
        canvas.coords(selected_brush.current_shape, selected_brush.last_point[0], selected_brush.last_point[1], selected_brush.current_point[0], selected_brush.current_point[1])
    elif selected_brush.current_tool == "ellipse":
        canvas.coords(selected_brush.current_shape, selected_brush.last_point[0], selected_brush.last_point[1], selected_brush.current_point[0], selected_brush.current_point[1])

def stop_drawing(*args):
    global selected_brush
    if brush.current_tool == "line" or selected_brush.current_tool == "rectangle" or selected_brush.current_tool == "ellipse":
        canvas.itemconfig(selected_brush.current_shape, tags="")
        undo_stack.append(selected_brush.current_shape)
    elif selected_brush.current_tool == 'brush' or selected_brush.current_tool == 'eraser':
        selected_brush.set_last_point(0, 0)
        undo_stack.append(brush_shapes.copy())
        brush_shapes.clear()
    elif selected_brush.current_tool == "text":
        selected_brush.current_shape = insert_text(selected_brush)
        undo_stack.append(selected_brush.current_shape)

def draw_line(current_brush):
    return canvas.create_line(current_brush.last_point[0], current_brush.last_point[1], current_brush.current_point[0], current_brush.current_point[1],
                              fill=current_brush.selected_color, width=current_brush.tool_size, tags="preview")

def draw_rect(current_brush):
    return canvas.create_rectangle(current_brush.last_point[0], current_brush.last_point[1], current_brush.current_point[0], current_brush.current_point[1],
                                   outline=current_brush.selected_color, width=current_brush.tool_size, tags="preview")

def draw_ellipse(current_brush):
    return canvas.create_oval(current_brush.last_point[0], current_brush.last_point[1], current_brush.current_point[0], current_brush.current_point[1],
                              outline=current_brush.selected_color, width=current_brush.tool_size, tags="preview")

def insert_text(current_brush):
    return canvas.create_text(current_brush.current_point[0], current_brush.current_point[1], fill=current_brush.selected_color,
                              text=current_brush.text, font=(current_brush.font, current_brush.tool_size+15, current_brush.styles))

if __name__ == "__main__":
    canvas = ui_setup()
    keybinds_setup(canvas)
    canvas.focus_set()
    root.mainloop()