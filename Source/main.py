import tkinter as tk
import config as cfg
import functions as fn

cfg.root = tk.Tk()
cfg.root.title("Image Importer")
cfg.root.geometry(cfg.INITIAL_WINDOW_SIZE)

# root window
fn.initialize_variables(cfg.root)

# Display
cfg.canvas = tk.Canvas(cfg.root, bg="white", cursor="none")
cfg.canvas.pack(fill=tk.BOTH, expand=True)

# Bot Button Frame
cfg.button_frame = tk.Frame(cfg.root)
cfg.button_frame.pack(side=tk.BOTTOM, pady=10)

# Buttons
cfg.import_button = tk.Button(cfg.button_frame, text="Import Image", command=fn.import_image)
cfg.import_button.pack(side=tk.LEFT, padx=5)

cfg.reset_button = tk.Button(cfg.button_frame, text="Reset", command=fn.reset_image)
cfg.reset_button.pack(side=tk.LEFT, padx=5)

cfg.set_origin_button = tk.Button(cfg.button_frame, text="Set Origin", command=fn.start_setting_origin)
cfg.set_origin_button.pack(side=tk.LEFT, padx=5)

cfg.set_x_max_button = tk.Button(cfg.button_frame, text="Set X Max", command=fn.start_setting_x_max)
cfg.set_x_max_button.pack(side=tk.LEFT, padx=5)

cfg.set_y_max_button = tk.Button(cfg.button_frame, text="Set Y Max", command=fn.start_setting_y_max)
cfg.set_y_max_button.pack(side=tk.LEFT, padx=5)

cfg.define_range_button = tk.Button(cfg.button_frame, text="Define Range", command=fn.define_range)
cfg.define_range_button.pack(side=tk.LEFT, padx=5)

cfg.zoom_button = tk.Button(cfg.button_frame, text="Zoom", command=fn.open_zoom_window)
cfg.zoom_button.pack(side=tk.LEFT, padx=5)

cfg.debug_button = tk.Button(cfg.button_frame, text="Debug", command=fn.show_debug_window)
cfg.debug_button.pack(side=tk.LEFT, padx=5)

cfg.start_select_data_button = tk.Button(cfg.button_frame, text="Select Data", command=fn.start_select_data)
cfg.start_select_data_button.pack(side=tk.LEFT, padx=5)

cfg.stop_select_data_button = tk.Button(cfg.button_frame, text="Stop Select", command=fn.stop_select_data)
cfg.stop_select_data_button.pack(side=tk.LEFT, padx=5)
cfg.stop_select_data_button.config(state=tk.DISABLED)

# Window resize and default values
cfg.canvas.bind('<Motion>', fn.track_mouse)
cfg.canvas.bind('<ButtonPress-1>', fn.set_origin)
cfg.root.bind('<Configure>', fn.center_image)

cfg.root.mainloop()
