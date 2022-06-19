# A tool to generate the Python code for making the windows for the game
import raylibpy as ray
from functools import partial

shapes = []
show_menu = True

current_tool_list = ["Rectangle", "Lines", "Line", "Circle", "Text"]
current_tool = 0
current_color_list = [ray.LIGHTGRAY, ray.GRAY, ray.DARKGRAY, ray.YELLOW, ray.GOLD, ray.ORANGE, ray.PINK, ray.RED,
                      ray.MAROON, ray.GREEN, ray.LIME, ray.DARKGREEN, ray.SKYBLUE, ray.BLUE, ray.DARKBLUE, ray.PURPLE,
                      ray.VIOLET, ray.DARKPURPLE, ray.BEIGE, ray.BROWN, ray.DARKBROWN, ray.WHITE, ray.BLACK, ray.BLANK,
                      ray.MAGENTA, ray.RAYWHITE]
current_color = 0
current_font_size = 20

win_width = int(input("Width of window: "))
win_height = int(input("Height of window: "))

mouse_click = {"x": -1, "y": -1}

ray.init_window(win_width, win_height, "Window Maker")


def parse_click():
    tool_to_parse = current_tool_list[current_tool]

    if tool_to_parse.lower() in ray.draw_text.__name__:
        shapes.append(partial(ray.draw_text, "[TEXT]", ray.get_mouse_x(), ray.get_mouse_y()-current_font_size,
                              current_font_size, current_color_list[current_color]))
        return

    if mouse_click["x"] == -1 or mouse_click["y"] == -1:
        mouse_click["x"] = ray.get_mouse_x()
        mouse_click["y"] = ray.get_mouse_y()
        return

    shape_width = ray.get_mouse_x() - mouse_click["x"]
    shape_height = ray.get_mouse_y() - mouse_click["y"]

    shape_x = mouse_click["x"]
    shape_y = mouse_click["y"]

    if tool_to_parse.lower() in ray.draw_line.__name__:
        shapes.append(partial(ray.draw_line, shape_x, shape_y, ray.get_mouse_x(), ray.get_mouse_y(),
                              current_color_list[current_color]))

    if shape_width < 0:
        shape_width = -shape_width
        shape_x -= shape_width

    if shape_height < 0:
        shape_height = -shape_height
        shape_y -= shape_height

    if tool_to_parse.lower() in ray.draw_rectangle.__name__:
        shapes.append(partial(ray.draw_rectangle, shape_x, shape_y, shape_width, shape_height,
                              current_color_list[current_color]))

    if tool_to_parse.lower() in ray.draw_rectangle_lines.__name__:
        if tool_to_parse.lower() != "line" and tool_to_parse.lower() != "rectangle":
            shapes.append(partial(ray.draw_rectangle_lines, shape_x, shape_y, shape_width, shape_height,
                                  current_color_list[current_color]))

    if tool_to_parse.lower() in ray.draw_circle.__name__:
        if abs(shape_width) > abs(shape_height):
            shapes.append(partial(ray.draw_circle, mouse_click['x'], mouse_click['y'], abs(shape_width),
                                  current_color_list[current_color]))
        else:
            shapes.append(partial(ray.draw_circle, mouse_click['x'], mouse_click['y'], abs(shape_height),
                                  current_color_list[current_color]))

    mouse_click["x"] = -1
    mouse_click["y"] = -1


while not ray.window_should_close():
    ray.begin_drawing()
    ray.clear_background(ray.RAYWHITE)

    if show_menu:
        ray.draw_text("Show/Hide Text: H", 0, 0, 20, ray.RED)
        ray.draw_text("Change Tool: N", 0, 20, 20, ray.RED)
        ray.draw_text(f"Current Tool: {current_tool_list[current_tool]}", 0, 40, 20, ray.RED)
        ray.draw_text(f"Current Color (change with C): {current_color_list[current_color]}", 0, 60, 20,
                      current_color_list[current_color])
        if current_tool_list[current_tool] == "Text":
            ray.draw_text(f"Current Font Size (1/2 to Inc/Dec): {current_font_size}", 0, 80, 20, ray.RED)

    if ray.is_key_pressed(ray.KEY_H):
        show_menu = not show_menu

    if ray.is_key_pressed(ray.KEY_N):
        if current_tool + 1 in range(len(current_tool_list)):
            current_tool += 1

        else:
            current_tool = 0

    if ray.is_key_pressed(ray.KEY_C):
        if current_color + 1 in range(len(current_color_list)):
            current_color += 1

        else:
            current_color = 0

    if ray.is_key_pressed(ray.KEY_ONE):
        current_font_size += 1

    if ray.is_key_pressed(ray.KEY_TWO):
        if current_font_size > 1:
            current_font_size -= 1

    if ray.is_mouse_button_released(0):
        parse_click()

    for function in shapes:
        function()

    ray.end_drawing()

output_string = ""

for shape in shapes:
    output_string += shape.func.__name__ + str(shape.args) + "\n"

with open("view.txt", "w") as file:
    print("Saving Python code to [view.txt]")
    file.write(repr(output_string))

with open("view.txt", "r") as file:
    print(file.read())
