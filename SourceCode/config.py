# Window sizes
INITIAL_WINDOW_SIZE = "800x400"
ZOOM_WINDOW_SIZE = "340x340"
DEBUG_WINDOW_SIZE = "200x200"
RANGE_WINDOW_SIZE = "400x150"
DATA_WINDOW_SIZE = "250x600"

# Init param
initial_x_from = 0.0
initial_x_to = 100.0
initial_x_accuracy = 1000
initial_y_from = 0.0
initial_y_to = 100.0
initial_y_accuracy = 1000

# Init offset (Zoom) idk why this happens
initial_zoom_offset_x = 0
initial_zoom_offset_y = 10

# Var and Boolean
image_path = None
original_image = None
image_on_canvas = None

virtual_width = 0
virtual_height = 0
origin_set = False
setting_origin = False
setting_x_max = False
setting_y_max = False
selecting_data = False
origin_x = 0
origin_y = 0
x_max = 0
y_max = 0
h_line = None
v_line = None
x_max_line = None
y_max_line = None
origin_h_line = None
origin_v_line = None
cursor_dot = None

zoom_window = None
zoom_canvas = None
zoom_image_on_canvas = None

zoom_offset_x = initial_zoom_offset_x
zoom_offset_y = initial_zoom_offset_y

data_window = None
data_listbox = None
data = []
data_marks = []
