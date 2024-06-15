import tkinter as tk
from tkinter import filedialog, Toplevel, Listbox, messagebox, StringVar, DoubleVar
from PIL import Image, ImageTk
import config as cfg


def initialize_variables(root):
    cfg.cursor_x = StringVar()
    cfg.cursor_y = StringVar()
    cfg.x_max_value = StringVar(value="0.00000")
    cfg.y_max_value = StringVar(value="0.00000")
    cfg.offset_x_value = StringVar(value="0")
    cfg.offset_y_value = StringVar(value="0")

    cfg.x_from = DoubleVar(value=cfg.initial_x_from)
    cfg.x_to = DoubleVar(value=cfg.initial_x_to)
    cfg.x_accuracy = DoubleVar(value=cfg.initial_x_accuracy)
    cfg.y_from = DoubleVar(value=cfg.initial_y_from)
    cfg.y_to = DoubleVar(value=cfg.initial_y_to)
    cfg.y_accuracy = DoubleVar(value=cfg.initial_y_accuracy)


def import_image():
    cfg.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif")])
    if cfg.image_path:
        load_image(cfg.image_path)
        define_range()
        show_debug_window()


def reset_image():
    cfg.canvas.delete("all")
    cfg.original_image = None
    cfg.image_on_canvas = None
    cfg.origin_set = False
    cfg.setting_origin = False
    cfg.setting_x_max = False
    cfg.setting_y_max = False
    cfg.selecting_data = False
    cfg.root.geometry("")
    cfg.cursor_x.set("")
    cfg.cursor_y.set("")
    cfg.x_max_value.set("0.00000")
    cfg.y_max_value.set("0.00000")
    cfg.offset_x_value.set("0")
    cfg.offset_y_value.set("0")
    clear_lines()
    cfg.zoom_offset_x = cfg.initial_zoom_offset_x
    cfg.zoom_offset_y = cfg.initial_zoom_offset_y
    if cfg.data_window:
        cfg.data_window.destroy()
        cfg.data_window = None
    cfg.data = []
    cfg.data_marks = []


def clear_lines():
    if cfg.h_line:
        cfg.canvas.delete(cfg.h_line)
        cfg.h_line = None
    if cfg.v_line:
        cfg.canvas.delete(cfg.v_line)
        cfg.v_line = None
    if cfg.x_max_line:
        cfg.canvas.delete(cfg.x_max_line)
        cfg.x_max_line = None
    if cfg.y_max_line:
        cfg.canvas.delete(cfg.y_max_line)
        cfg.y_max_line = None
    if cfg.origin_h_line:
        cfg.canvas.delete(cfg.origin_h_line)
        cfg.origin_h_line = None
    if cfg.origin_v_line:
        cfg.canvas.delete(cfg.origin_v_line)
        cfg.origin_v_line = None


def load_image(image_path):
    image = Image.open(image_path)

    # Max image size (resize w aspect)
    max_width, max_height = 1600, 900
    aspect_ratio = image.width / image.height

    if image.width > max_width or image.height > max_height:
        if image.width / max_width > image.height / max_height:
            new_width = max_width
            new_height = int(max_width / aspect_ratio)
        else:
            new_height = max_height
            new_width = int(max_height * aspect_ratio)
    else:
        new_width, new_height = image.width, image.height

    cfg.virtual_width = new_width
    cfg.virtual_height = new_height
    cfg.original_image = image.resize((new_width, new_height), Image.LANCZOS)
    display_image()


def display_image():
    if cfg.original_image:
        cfg.canvas.delete("all")
        cfg.photo = ImageTk.PhotoImage(cfg.original_image)
        cfg.image_on_canvas = cfg.canvas.create_image(0, 0, anchor=tk.NW, image=cfg.photo)
        cfg.root.geometry(f"{cfg.virtual_width}x{cfg.virtual_height + cfg.button_frame.winfo_height()}")
        center_image()


def center_image(event=None):
    if cfg.original_image and cfg.image_on_canvas:
        canvas_width = cfg.canvas.winfo_width()
        canvas_height = cfg.canvas.winfo_height()

        # Center image coord
        x = (canvas_width - cfg.virtual_width) // 2
        y = (canvas_height - cfg.virtual_height) // 2

        cfg.canvas.coords(cfg.image_on_canvas, x, y)
        cfg.canvas.config(scrollregion=cfg.canvas.bbox(tk.ALL))


def track_mouse(event):
    if cfg.original_image:
        canvas_width = cfg.canvas.winfo_width()
        canvas_height = cfg.canvas.winfo_height()

        # Center image coord
        x = (canvas_width - cfg.virtual_width) // 2
        y = (canvas_height - cfg.virtual_height) // 2

        # Relative coord (virtual)
        relative_x = event.x - x
        relative_y = event.y - y

        if cfg.setting_origin or cfg.setting_x_max or cfg.setting_y_max or cfg.selecting_data:
            if cfg.setting_origin or cfg.setting_y_max or cfg.selecting_data:
                if cfg.h_line:
                    cfg.canvas.delete(cfg.h_line)
                cfg.h_line = cfg.canvas.create_line(0, event.y, canvas_width, event.y, fill="red")
            if cfg.setting_origin or cfg.setting_x_max or cfg.selecting_data:
                if cfg.v_line:
                    cfg.canvas.delete(cfg.v_line)
                cfg.v_line = cfg.canvas.create_line(event.x, 0, event.x, canvas_height, fill="red")

        if cfg.origin_set:
            original_x = (relative_x - cfg.origin_x)
            original_y = (cfg.origin_y - relative_y)
        else:
            original_x = relative_x
            original_y = cfg.virtual_height - relative_y

        remapped_x = remap_value(original_x, 0, cfg.x_max, cfg.x_from.get(), cfg.x_to.get())
        remapped_y = remap_value(original_y, 0, cfg.y_max, cfg.y_from.get(), cfg.y_to.get())

        cfg.cursor_x.set(f"{remapped_x:.5f}")
        cfg.cursor_y.set(f"{remapped_y:.5f}")

        # Draw cursor dot
        if cfg.cursor_dot:
            cfg.canvas.delete(cfg.cursor_dot)
        cfg.cursor_dot = cfg.canvas.create_oval(event.x - 3, event.y - 3, event.x + 3, event.y + 3, fill="green",
                                                outline="green")

        # Update zoom (if open)
        if cfg.zoom_window and cfg.original_image:
            update_zoom(event.x, event.y)


def start_setting_origin():
    cfg.setting_origin = True
    cfg.setting_x_max = False
    cfg.setting_y_max = False
    cfg.selecting_data = False
    cfg.origin_set = False
    clear_lines()


def start_setting_x_max():
    cfg.setting_x_max = True
    cfg.setting_origin = False
    cfg.setting_y_max = False
    cfg.selecting_data = False


def start_setting_y_max():
    cfg.setting_y_max = True
    cfg.setting_origin = False
    cfg.setting_x_max = False
    cfg.selecting_data = False


def set_origin(event):
    canvas_width = cfg.canvas.winfo_width()
    canvas_height = cfg.canvas.winfo_height()

    if cfg.setting_origin:
        cfg.setting_origin = False
        cfg.origin_set = True
        cfg.origin_x = event.x - (canvas_width - cfg.virtual_width) // 2
        cfg.origin_y = event.y - (canvas_height - cfg.virtual_height) // 2
        if cfg.origin_h_line:
            cfg.canvas.delete(cfg.origin_h_line)
        if cfg.origin_v_line:
            cfg.canvas.delete(cfg.origin_v_line)
        cfg.origin_h_line = cfg.canvas.create_line(0, event.y, canvas_width, event.y, fill="blue")
        cfg.origin_v_line = cfg.canvas.create_line(event.x, 0, event.x, canvas_height, fill="blue")
    elif cfg.setting_x_max:
        cfg.setting_x_max = False
        cfg.x_max = event.x - (canvas_width - cfg.virtual_width) // 2 - cfg.origin_x
        if cfg.x_max_line:
            cfg.canvas.delete(cfg.x_max_line)
        cfg.x_max_line = cfg.canvas.create_line(event.x, 0, event.x, canvas_height, fill="blue")
        cfg.x_max_value.set(f"{cfg.x_max:.5f}")
    elif cfg.setting_y_max:
        cfg.setting_y_max = False
        cfg.y_max = cfg.origin_y - (event.y - (canvas_height - cfg.virtual_height) // 2)
        if cfg.y_max_line:
            cfg.canvas.delete(cfg.y_max_line)
        cfg.y_max_line = cfg.canvas.create_line(0, event.y, canvas_width, event.y, fill="blue")
        cfg.y_max_value.set(f"{cfg.y_max:.5f}")
    elif cfg.selecting_data:
        record_data(event.x, event.y)


def show_debug_window():
    if not hasattr(cfg, 'debug_window') or not cfg.debug_window.winfo_exists():
        cfg.debug_window = Toplevel(cfg.root)
        cfg.debug_window.title("Debug Window")
        cfg.debug_window.geometry(cfg.DEBUG_WINDOW_SIZE)
        debug_label = tk.Label(cfg.debug_window, text="Cursor Position")
        debug_label.pack()

        x_label = tk.Label(cfg.debug_window, textvariable=cfg.cursor_x)
        x_label.pack()

        y_label = tk.Label(cfg.debug_window, textvariable=cfg.cursor_y)
        y_label.pack()

        debug_label_x_max = tk.Label(cfg.debug_window, text="X Max")
        debug_label_x_max.pack()

        x_max_value_label = tk.Label(cfg.debug_window, textvariable=cfg.x_max_value)
        x_max_value_label.pack()

        debug_label_y_max = tk.Label(cfg.debug_window, text="Y Max")
        debug_label_y_max.pack()

        y_max_value_label = tk.Label(cfg.debug_window, textvariable=cfg.y_max_value)
        y_max_value_label.pack()

        debug_label_offset_x = tk.Label(cfg.debug_window, text="Offset X")
        debug_label_offset_x.pack()

        offset_x_value_label = tk.Label(cfg.debug_window, textvariable=cfg.offset_x_value)
        offset_x_value_label.pack()

        debug_label_offset_y = tk.Label(cfg.debug_window, text="Offset Y")
        debug_label_offset_y.pack()

        offset_y_value_label = tk.Label(cfg.debug_window, textvariable=cfg.offset_y_value)
        offset_y_value_label.pack()


def define_range():
    if not hasattr(cfg, 'range_window') or not cfg.range_window.winfo_exists():
        cfg.range_window = Toplevel(cfg.root)
        cfg.range_window.title("Define Range")
        cfg.range_window.geometry(cfg.RANGE_WINDOW_SIZE)

        tk.Label(cfg.range_window, text="X value: from").grid(row=0, column=0)
        tk.Entry(cfg.range_window, textvariable=cfg.x_from).grid(row=0, column=1)
        tk.Label(cfg.range_window, text="to").grid(row=0, column=2)
        tk.Entry(cfg.range_window, textvariable=cfg.x_to).grid(row=0, column=3)

        tk.Label(cfg.range_window, text="X accuracy:").grid(row=1, column=0)
        tk.Entry(cfg.range_window, textvariable=cfg.x_accuracy).grid(row=1, column=1)

        tk.Label(cfg.range_window, text="Y value: from").grid(row=2, column=0)
        tk.Entry(cfg.range_window, textvariable=cfg.y_from).grid(row=2, column=1)
        tk.Label(cfg.range_window, text="to").grid(row=2, column=2)
        tk.Entry(cfg.range_window, textvariable=cfg.y_to).grid(row=2, column=3)

        tk.Label(cfg.range_window, text="Y accuracy:").grid(row=3, column=0)
        tk.Entry(cfg.range_window, textvariable=cfg.y_accuracy).grid(row=3, column=1)

        update_button = tk.Button(cfg.range_window, text="Update", command=update_range)
        update_button.grid(row=4, columnspan=4)


def update_range():
    # Update and Remap, no use atm
    pass


def remap_value(value, old_min, old_max, new_min, new_max):
    if old_max - old_min == 0:
        return new_min  # >:( I hate division by zero fu
    return (value - old_min) / (old_max - old_min) * (new_max - new_min) + new_min


def open_zoom_window():
    if not cfg.zoom_window:
        cfg.zoom_window = Toplevel(cfg.root)
        cfg.zoom_window.title("Zoom")
        cfg.zoom_window.geometry(cfg.ZOOM_WINDOW_SIZE)
        cfg.zoom_canvas = tk.Canvas(cfg.zoom_window, width=340, height=340, bg="white")
        cfg.zoom_canvas.pack()
        cfg.zoom_canvas.create_line(170, 0, 170, 340, fill="black")  # Vertical
        cfg.zoom_canvas.create_line(0, 170, 340, 170, fill="black")  # Horizontal

        # Arrow keys for manual offsetting
        cfg.zoom_window.bind('<Up>', lambda e: move_zoom_window(0, -1))
        cfg.zoom_window.bind('<Down>', lambda e: move_zoom_window(0, 1))
        cfg.zoom_window.bind('<Left>', lambda e: move_zoom_window(-1, 0))
        cfg.zoom_window.bind('<Right>', lambda e: move_zoom_window(1, 0))

        cfg.zoom_window.protocol("WM_DELETE_WINDOW", close_zoom_window)


def close_zoom_window():
    cfg.zoom_window.destroy()
    cfg.zoom_window = None
    cfg.zoom_canvas = None
    cfg.zoom_image_on_canvas = None


def move_zoom_window(dx, dy):
    cfg.zoom_offset_x += dx
    cfg.zoom_offset_y += dy
    if cfg.zoom_image_on_canvas:
        update_zoom_with_offset()
    cfg.offset_x_value.set(f"{cfg.zoom_offset_x}")
    cfg.offset_y_value.set(f"{cfg.zoom_offset_y}")


def update_zoom(cursor_x, cursor_y):
    cfg.cursor_x_pos = cursor_x
    cfg.cursor_y_pos = cursor_y
    update_zoom_with_offset()


def update_zoom_with_offset():
    if not cfg.zoom_window or not cfg.zoom_canvas:
        return

    zoom_size = 17  # Zoom size DO NOT CHANGE!!!
    zoom_factor = 20  # Enlarge (window) size DO NOT CHANGE!!!

    # Offset cursor position (for zoom)
    cursor_x = cfg.cursor_x_pos + cfg.zoom_offset_x
    cursor_y = cfg.cursor_y_pos + cfg.zoom_offset_y

    # Zoom area
    left = max(cursor_x - zoom_size // 2, 0)
    top = max(cursor_y - zoom_size // 2, 0)
    right = min(cursor_x + zoom_size // 2 + 1, cfg.virtual_width)
    bottom = min(cursor_y + zoom_size // 2 + 1, cfg.virtual_height)

    # Crop zoom
    snapshot = cfg.original_image.crop((left, top, right, bottom))
    snapshot = snapshot.resize((zoom_size * zoom_factor, zoom_size * zoom_factor), Image.NEAREST)

    cfg.zoom_photo = ImageTk.PhotoImage(snapshot)

    if cfg.zoom_image_on_canvas:
        cfg.zoom_canvas.delete(cfg.zoom_image_on_canvas)
    cfg.zoom_image_on_canvas = cfg.zoom_canvas.create_image(0, 0, anchor=tk.NW, image=cfg.zoom_photo)

    # Zoom crosshair
    cfg.zoom_canvas.create_line(170, 0, 170, 340, fill="black")
    cfg.zoom_canvas.create_line(0, 170, 340, 170, fill="black")


def start_select_data():
    cfg.selecting_data = True
    cfg.setting_origin = False
    cfg.setting_x_max = False
    cfg.setting_y_max = False
    cfg.start_select_data_button.config(state=tk.DISABLED)
    cfg.stop_select_data_button.config(state=tk.NORMAL)
    show_data_window()


def stop_select_data():
    cfg.selecting_data = False
    cfg.start_select_data_button.config(state=tk.NORMAL)
    cfg.stop_select_data_button.config(state=tk.DISABLED)
    clear_lines()


def show_data_window():
    if not cfg.data_window:
        cfg.data_window = Toplevel(cfg.root)
        cfg.data_window.title("Dataset")
        cfg.data_window.geometry(cfg.DATA_WINDOW_SIZE)
        cfg.data_listbox = Listbox(cfg.data_window)
        cfg.data_listbox.pack(fill=tk.BOTH, expand=True)
        update_data_listbox()

        clear_button = tk.Button(cfg.data_window, text="Clear", command=clear_all_data)
        clear_button.pack(side=tk.LEFT, padx=5, pady=10)

        delete_button = tk.Button(cfg.data_window, text="Del Prev", command=delete_previous_data)
        delete_button.pack(side=tk.LEFT, padx=5, pady=10)

        copy_x_button = tk.Button(cfg.data_window, text="Copy X", command=copy_x_data)
        copy_x_button.pack(side=tk.RIGHT, padx=5, pady=10)

        copy_y_button = tk.Button(cfg.data_window, text="Copy Y", command=copy_y_data)
        copy_y_button.pack(side=tk.RIGHT, padx=5, pady=10)

        cfg.data_window.protocol("WM_DELETE_WINDOW", close_data_window)


def close_data_window():
    cfg.data_window.destroy()
    cfg.data_window = None


def update_data_listbox(): # Printing out datasets
    if cfg.data_listbox:
        cfg.data_listbox.delete(0, tk.END)
        cfg.data_listbox.insert(tk.END, "X         | Y")
        for data in cfg.data:
            cfg.data_listbox.insert(tk.END, f"{data[0]:.5f} | {data[1]:.5f}")


def clear_all_data():
    cfg.data = []
    update_data_listbox()
    clear_data_marks()


def delete_previous_data():
    if cfg.data:
        cfg.data.pop()
        update_data_listbox()
        clear_last_data_mark()


def copy_x_data():
    if not cfg.data:
        messagebox.showwarning("No Data", "No data to copy.")
        return
    data_str = "\n".join(f"{data[0]:.5f}" for data in cfg.data)
    cfg.root.clipboard_clear()
    cfg.root.clipboard_append(data_str)
    messagebox.showinfo("Copied", "X data copied to clipboard.")


def copy_y_data():
    if not cfg.data:
        messagebox.showwarning("No Data", "No data to copy.")
        return
    data_str = "\n".join(f"{data[1]:.5f}" for data in cfg.data)
    cfg.root.clipboard_clear()
    cfg.root.clipboard_append(data_str)
    messagebox.showinfo("Copied", "Y data copied to clipboard.")


def clear_data_marks():
    for mark in cfg.data_marks:
        cfg.canvas.delete(mark)
    cfg.data_marks = []


def clear_last_data_mark():
    if cfg.data_marks:
        cfg.canvas.delete(cfg.data_marks.pop())
        cfg.canvas.delete(cfg.data_marks.pop())


def record_data(x, y):
    if not cfg.data_window:
        return
    canvas_width = cfg.canvas.winfo_width()
    canvas_height = cfg.canvas.winfo_height()

    # Use the raw x, y
    relative_x = x - (canvas_width - cfg.virtual_width) // 2
    relative_y = y - (canvas_height - cfg.virtual_height) // 2

    if cfg.origin_set:
        original_x = (relative_x - cfg.origin_x)
        original_y = (cfg.origin_y - relative_y)
    else:
        original_x = relative_x
        original_y = cfg.virtual_height - relative_y

    remapped_x = remap_value(original_x, 0, cfg.x_max, cfg.x_from.get(), cfg.x_to.get())
    remapped_y = remap_value(original_y, 0, cfg.y_max, cfg.y_from.get(), cfg.y_to.get())

    cfg.data.append((remapped_x, remapped_y))
    update_data_listbox()

    # Place markers
    mark1 = cfg.canvas.create_line(x - 5, y, x + 5, y, fill="green")
    mark2 = cfg.canvas.create_line(x, y - 5, x, y + 5, fill="green")
    cfg.data_marks.append(mark1)
    cfg.data_marks.append(mark2)
