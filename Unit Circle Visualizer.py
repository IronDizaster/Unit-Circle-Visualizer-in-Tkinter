import math
from tkinter import *
from tkinter import messagebox

# All code is original and written by IronDizaster in 2023. AI has been used only for documentation and comments.
root = Tk()


TITLE = 'Unit Circle Visualizer'
WINDOW_WIDTH = root.winfo_screenwidth()
WINDOW_HEIGHT = root.winfo_screenheight()
BG_COLOR = '#e8e8e8'
POINT_COLOR = 'red'
LINE_COLOR = 'black'
FONT = 'Arial'
FONT_COLOR = 'red'
ZOOM_STRENGTH = 5 # How many pixels the screen zooms in/out by scrolling. MUST BE AN INTEGER
anim_speed = 0.1
angle_rounding = 0

WINDOW_X_CENTER = WINDOW_WIDTH / 2
WINDOW_Y_CENTER = WINDOW_HEIGHT / 2
unit_circle_radius = 150
paused = False

angle = 0
scale = 0.5 # Used to determine how point & line width scale with zoom-level.
global_rounding = 15


show_only_sine = False
show_only_cos = False
show_only_tg = False
show_only_cotg = False
show_all = True

ui_buttons = []

canvas = Canvas(root, width = WINDOW_WIDTH, height = WINDOW_HEIGHT, bg = BG_COLOR)
canvas.pack()

def center_screen():
    '''Centers the application window on the user's screen and sets the window title.'''
    screen_width = root.winfo_screenwidth()  # Width of the user screen.
    screen_height = root.winfo_screenheight() # Height of the user screen.

    # Starting X & Y window positions:
    x = (screen_width / 2) - (WINDOW_WIDTH / 2)
    y = (screen_height / 2) - (WINDOW_HEIGHT / 2)

    root.geometry('%dx%d+%d+%d' % (WINDOW_WIDTH, WINDOW_HEIGHT, x, y))
    TM = ' (IronDizaster ©)'
    root.title(TITLE + TM)

def update_unit_circle(): 
    '''Draws and updates all elements of the unit circle and trigonometric visualizations on the canvas.'''
    arrow = 'last' if unit_circle_radius > 45 else 'none'
    point_radius = math.log(unit_circle_radius ** scale)
    text_offset_y = 1 + math.sqrt(unit_circle_radius)
    font_size = round(math.log(unit_circle_radius ** 2))
    canvas.delete('unit_circle')

    # Angle arc:
    canvas.create_arc(WINDOW_X_CENTER - unit_circle_radius / 5, 
                      WINDOW_Y_CENTER - unit_circle_radius / 5, 
                      WINDOW_X_CENTER + unit_circle_radius / 5,
                      WINDOW_Y_CENTER + unit_circle_radius / 5,
                      style = PIESLICE, tag='unit_circle arc', start = 0, extent = angle % 360, 
                      outline = 'green', fill='#cae8cf', width = math.log(unit_circle_radius ** scale) / 1.25)
    canvas.tag_lower('arc')
    
    # Cosine-dotted-line:
    canvas.create_line(WINDOW_X_CENTER + math.sin(math.radians(angle + 90)) * unit_circle_radius, 
                       WINDOW_Y_CENTER + math.cos(math.radians(angle + 90)) * unit_circle_radius, 
                       WINDOW_X_CENTER,
                       WINDOW_Y_CENTER + math.cos(math.radians(angle + 90)) * unit_circle_radius, 
                       tag='unit_circle cos', fill='red', width = math.ceil(math.log(unit_circle_radius ** scale) / 1.25), dash=(1, 1))
    if show_only_cos:
        canvas.create_line(WINDOW_X_CENTER + math.sin(math.radians(angle + 90)) * unit_circle_radius, 
                           WINDOW_Y_CENTER + math.cos(math.radians(angle + 90)) * unit_circle_radius, 
                           WINDOW_X_CENTER + math.sin(math.radians(angle + 90)) * unit_circle_radius,
                           WINDOW_Y_CENTER, 
                           tag='unit_circle cos', fill='gray', width = math.ceil(math.log(unit_circle_radius ** scale) / 1.25), dash=(1, 1))

    # Sine-line:
    canvas.create_line(WINDOW_X_CENTER, 
                       WINDOW_Y_CENTER, 
                       WINDOW_X_CENTER,
                       WINDOW_Y_CENTER + math.cos(math.radians(angle + 90)) * unit_circle_radius, 
                       tags='unit_circle sine', fill='LightSeaGreen', width = math.ceil(math.log(unit_circle_radius ** scale) / 1.25), arrow=arrow)
    if show_only_sine:
        canvas.create_line(WINDOW_X_CENTER + math.sin(math.radians(angle + 90)) * unit_circle_radius, 
                           WINDOW_Y_CENTER + math.cos(math.radians(angle + 90)) * unit_circle_radius, 
                           WINDOW_X_CENTER,
                           WINDOW_Y_CENTER + math.cos(math.radians(angle + 90)) * unit_circle_radius, 
                           tag='unit_circle sine', fill='gray', width = math.ceil(math.log(unit_circle_radius ** scale) / 1.25), dash=(1, 1))
    # Tan-line:

    canvas.create_line(WINDOW_X_CENTER + unit_circle_radius, 
                       WINDOW_Y_CENTER, 
                       WINDOW_X_CENTER + unit_circle_radius,
                       WINDOW_Y_CENTER - math.tan(math.radians(angle)) * unit_circle_radius, 
                       tag='unit_circle tg', fill='orange', width = math.ceil(math.log(unit_circle_radius ** scale) / 1.25), arrow=LAST)

    # Tan dotted line:
    canvas.create_line(WINDOW_X_CENTER, 
                       WINDOW_Y_CENTER - math.tan(math.radians(angle)) * unit_circle_radius, 
                       WINDOW_X_CENTER + unit_circle_radius,
                       WINDOW_Y_CENTER - math.tan(math.radians(angle)) * unit_circle_radius, 
                       tag='unit_circle tg', fill='orange', width = math.ceil(math.log(unit_circle_radius ** scale) / 1.25), dash=(1, 1))
    
    # Cotan-line:
    if angle != 0:
        cotan_x = 1/math.tan(math.radians(angle)) * unit_circle_radius
    else:
        cotan_x = 0
    canvas.create_line(WINDOW_X_CENTER, 
                       WINDOW_Y_CENTER - unit_circle_radius, 
                       WINDOW_X_CENTER + cotan_x,
                       WINDOW_Y_CENTER - unit_circle_radius, 
                       tag='unit_circle cotg', fill='purple', width = math.ceil(math.log(unit_circle_radius ** scale) / 1.25), arrow=LAST)

    # Cotan dotted line:
    canvas.create_line(WINDOW_X_CENTER + cotan_x, 
                       WINDOW_Y_CENTER - unit_circle_radius, 
                       WINDOW_X_CENTER + cotan_x,
                       WINDOW_Y_CENTER, 
                       tag='unit_circle cotg', fill='purple', width = math.ceil(math.log(unit_circle_radius ** scale) / 1.25), dash=(1, 1))
    
    # Sine dotted line:
    canvas.create_line(WINDOW_X_CENTER + math.sin(math.radians(angle + 90)) * unit_circle_radius, 
                       WINDOW_Y_CENTER + math.cos(math.radians(angle + 90)) * unit_circle_radius, 
                       WINDOW_X_CENTER + math.sin(math.radians(angle + 90)) * unit_circle_radius,
                       WINDOW_Y_CENTER, 
                       tag='unit_circle sine', fill='LightSeaGreen', width = math.ceil(math.log(unit_circle_radius ** scale) / 1.25), dash=(1, 1))
    
    # Red line of the right angle triangle:
    canvas.create_line(WINDOW_X_CENTER, 
                       WINDOW_Y_CENTER, 
                       WINDOW_X_CENTER + math.sin(math.radians(angle + 90)) * unit_circle_radius,
                       WINDOW_Y_CENTER, 
                       tag='unit_circle cos', fill='red', width = math.ceil(math.log(unit_circle_radius ** scale) / 1.25), arrow=arrow)
    

        
    # Radius line:
    canvas.create_line(WINDOW_X_CENTER + math.sin(math.radians(angle + 90)) * 99 * unit_circle_radius, 
                       WINDOW_Y_CENTER + math.cos(math.radians(angle + 90)) * 99 * unit_circle_radius, 
                       WINDOW_X_CENTER - math.sin(math.radians(angle + 90)) * 99 * unit_circle_radius, 
                       WINDOW_Y_CENTER - math.cos(math.radians(angle + 90)) * 99 * unit_circle_radius,
                       tag='unit_circle tg', width = math.log(unit_circle_radius ** scale) / 1.25, fill='gray')
    
    if show_only_cotg:
        canvas.create_line(WINDOW_X_CENTER + math.sin(math.radians(angle + 90)) * 99 * unit_circle_radius, 
                           WINDOW_Y_CENTER + math.cos(math.radians(angle + 90)) * 99 * unit_circle_radius, 
                           WINDOW_X_CENTER - math.sin(math.radians(angle + 90)) * 99 * unit_circle_radius, 
                           WINDOW_Y_CENTER - math.cos(math.radians(angle + 90)) * 99 * unit_circle_radius,
                           tag='unit_circle cotg', width = math.log(unit_circle_radius ** scale) / 1.25, fill='gray')
    # Spinning radius vector:
    canvas.create_line(WINDOW_X_CENTER, WINDOW_Y_CENTER, 
                       WINDOW_X_CENTER + math.sin(math.radians(angle + 90)) * unit_circle_radius, 
                       WINDOW_Y_CENTER + math.cos(math.radians(angle + 90)) * unit_circle_radius,
                       arrow=arrow, tag='unit_circle', width = math.log(unit_circle_radius ** scale) / 1.25, fill='green')
    # Angle text:
    if unit_circle_radius > 70:
        canvas.create_text(WINDOW_X_CENTER + unit_circle_radius / 12, WINDOW_Y_CENTER - unit_circle_radius / 12,
                           text = f'{angle % 360:.2f}°', tag='unit_circle', font=f'{FONT} {font_size} bold', fill='midnightblue')
    # Unit circle itself:
    canvas.create_oval(WINDOW_X_CENTER - unit_circle_radius, 
                       WINDOW_Y_CENTER - unit_circle_radius, 
                       WINDOW_X_CENTER + unit_circle_radius, 
                       WINDOW_Y_CENTER + unit_circle_radius,
                       outline = LINE_COLOR,
                       width = math.log(unit_circle_radius ** scale), tag = 'unit_circle')
    
    # Point of the cosine:
    canvas.create_oval(WINDOW_X_CENTER + math.sin(math.radians(angle + 90)) * unit_circle_radius - point_radius, 
                       WINDOW_Y_CENTER - point_radius, 
                       WINDOW_X_CENTER + math.sin(math.radians(angle + 90)) * unit_circle_radius + point_radius, 
                       WINDOW_Y_CENTER + point_radius,
                       tag='unit_circle cos', fill='red', outline=LINE_COLOR)
    
    # Point of the tan:
    canvas.create_oval(WINDOW_X_CENTER - point_radius, 
                       WINDOW_Y_CENTER - math.tan(math.radians(angle)) * unit_circle_radius - point_radius, 
                       WINDOW_X_CENTER + point_radius, 
                       WINDOW_Y_CENTER - math.tan(math.radians(angle)) * unit_circle_radius + point_radius,
                       tag='unit_circle tg', fill='orange', outline=LINE_COLOR)
    # Point of the cotan:
    canvas.create_oval(WINDOW_X_CENTER + cotan_x + point_radius, 
                       WINDOW_Y_CENTER + point_radius, 
                       WINDOW_X_CENTER + cotan_x - point_radius, 
                       WINDOW_Y_CENTER - point_radius,
                       tag='unit_circle cotg', fill='purple', outline=LINE_COLOR)
    
    # Point of the sine:
    canvas.create_oval(WINDOW_X_CENTER - point_radius, 
                       WINDOW_Y_CENTER + math.cos(math.radians(angle + 90)) * unit_circle_radius - point_radius, 
                       WINDOW_X_CENTER + point_radius, 
                       WINDOW_Y_CENTER + math.cos(math.radians(angle + 90)) * unit_circle_radius + point_radius,
                       tag='unit_circle sine', fill='LightSeaGreen', outline=LINE_COLOR)
    
    # Point on the unit circle (intersect of radius line & unit circle):
    canvas.create_oval(WINDOW_X_CENTER + math.sin(math.radians(angle + 90)) * unit_circle_radius - point_radius, 
                       WINDOW_Y_CENTER + math.cos(math.radians(angle + 90)) * unit_circle_radius - point_radius, 
                       WINDOW_X_CENTER + math.sin(math.radians(angle + 90)) * unit_circle_radius + point_radius, 
                       WINDOW_Y_CENTER + math.cos(math.radians(angle + 90)) * unit_circle_radius + point_radius,
                       tag='unit_circle', fill='green', outline=LINE_COLOR)
    
    # Text of the cosine:
    if round(math.sin(math.radians(angle)), 3) < 0:
        cos_anchor = 'n'
        cos_offset_y = text_offset_y
    else:
        cos_anchor = 's'
        cos_offset_y = -text_offset_y
    canvas.create_text(WINDOW_X_CENTER + math.sin(math.radians(angle + 90)) * unit_circle_radius / 2,
                       WINDOW_Y_CENTER + math.cos(math.radians(angle + 90)) * unit_circle_radius + cos_offset_y,
                       text=f'cos({angle % 360:.2f}°):\nx = {round(math.cos(math.radians(angle)), 3):.3f}', 
                       tag='unit_circle cos',
                       font=f'{FONT} {font_size} bold',
                       anchor=cos_anchor,
                       fill='red')

    # Text of the sine:
    if round(math.cos(math.radians(angle)), 3) < 0:
        sin_anchor = 'e'
        sin_offset_x = text_offset_y
    else:
        sin_anchor = 'w'
        sin_offset_x = -text_offset_y
    canvas.create_text(WINDOW_X_CENTER + math.sin(math.radians(angle + 90)) * unit_circle_radius - sin_offset_x,
                       WINDOW_Y_CENTER + math.cos(math.radians(angle + 90)) * unit_circle_radius / 2,
                       text=f'sin({angle % 360:.2f}°):\ny = {round(math.sin(math.radians(angle)), 3):.3f}', 
                       tag='unit_circle sine',
                       font=f'{FONT} {font_size} bold',
                       anchor=sin_anchor,
                       fill='LightSeaGreen')
    
    # Text of the tan:
    if round(angle, 6) % 360 == 90 or round(angle, 6) % 360 == 270:
        tan_y = 'undefined'
    else:
        tan_y = round(math.tan(math.radians(angle)), 3)

    tan_text_offset = 50 + math.sqrt(unit_circle_radius)

    if tan_y != 'undefined':
        canvas.create_text(WINDOW_X_CENTER + unit_circle_radius + tan_text_offset, 
                           WINDOW_Y_CENTER + tan_text_offset - 10,
                           text=f'tg({angle % 360:.2f}°):\ny = {tan_y:.3f}',
                           tag='unit_circle tg', fill='orange', font=f'{FONT} 12 bold')
    else:
        canvas.create_text(WINDOW_X_CENTER + unit_circle_radius + tan_text_offset, 
                           WINDOW_Y_CENTER + tan_text_offset - 10,
                           text=f'tg({angle % 360:.2f}°):\ny = {tan_y}',
                           tag='unit_circle tg', fill='orange', font=f'{FONT} 12 bold')
    
    # Text of the cotan:
    if angle != 0:
        cotan_x = 1/math.tan(math.radians(angle))
    else:
        cotan_x = 0
    if round(angle, 6) % 360 == 180 or round(angle, 6) % 360 == 0:
        cotan_text = 'undefined'
    else:
        cotan_text = round(cotan_x, 3)
    if cotan_text == 'undefined':
        canvas.create_text(WINDOW_X_CENTER - tan_text_offset, 
                           WINDOW_Y_CENTER - unit_circle_radius - tan_text_offset + 10,
                           text=f'cotg({angle % 360:.2f}°):\nx = {cotan_text}',
                           tag='unit_circle cotg', fill='purple', font=f'{FONT} 12 bold')
    else:
        canvas.create_text(WINDOW_X_CENTER - tan_text_offset, 
                           WINDOW_Y_CENTER - unit_circle_radius - tan_text_offset + 10,
                           text=f'cotg({angle % 360:.2f}°):\nx = {cotan_text:.3f}',
                           tag='unit_circle cotg', fill='purple', font=f'{FONT} 12 bold')
        
    canvas.tag_raise('UI')
    hide_functions()

def update_analytics():
    '''Displays analytics information (angle, trig values, etc.) on the canvas.'''
    if ui_hidden: return
    PADDING = 25
    canvas.delete('info')
    font_size = 12
    LINE_GAP = 8 + font_size
    if round(angle, 6) % 360 == 90 or round(angle, 6) % 360 == 270:
        tan_y = 'undefined'
    else:
        tan_y = f'{round(math.tan(math.radians(angle)), 3):.3f}'

    if angle != 0:
        cotan_x = 1/math.tan(math.radians(angle))
    else:
        cotan_x = 0
    if round(angle, 6) % 360 == 180 or round(angle, 6) % 360 == 0:
        cotan_text = 'undefined'
    else:
        cotan_text = f'{round(cotan_x, 3):.3f}'
    canvas.create_text(WINDOW_WIDTH - PADDING, PADDING, 
                       text='Analytics:', font=f'{FONT} {font_size} bold', 
                       anchor='e', tag='info UI')
    
    canvas.create_text(WINDOW_WIDTH - PADDING, PADDING + LINE_GAP, 
                       text=f'θ = {angle % 360:.2f}°', font=f'{FONT} {font_size}', 

                       anchor='e', tag='info UI')
    canvas.create_text(WINDOW_WIDTH - PADDING, PADDING + LINE_GAP * 2, 
                       text=f'sin({angle % 360:.2f}°) = {round(math.sin(math.radians(angle)), 3):.3f}', font=f'{FONT} {font_size}', 
                       anchor='e', tag='info UI')
    
    canvas.create_text(WINDOW_WIDTH - PADDING, PADDING + LINE_GAP * 3, 
                       text=f'cos({angle % 360:.2f}°) = {round(math.cos(math.radians(angle)), 3):.3f}', font=f'{FONT} {font_size}', 
                       anchor='e', tag='info UI')
    
    canvas.create_text(WINDOW_WIDTH - PADDING, PADDING + LINE_GAP * 4, 
                       text=f'tg({angle % 360:.2f}°) = {tan_y}', font=f'{FONT} {font_size}', 
                       anchor='e', tag='info UI')
    
    canvas.create_text(WINDOW_WIDTH - PADDING, PADDING + LINE_GAP * 5, 
                       text=f'cotg({angle % 360:.2f}°) = {cotan_text}', font=f'{FONT} {font_size}', 
                       anchor='e', tag='info UI')
    
    canvas.create_text(WINDOW_WIDTH - PADDING, PADDING + LINE_GAP * 6, 
                   text=f'rad({angle % 360:.2f}°): {math.radians(angle % 360):.3f}', font=f'{FONT} {font_size}', 
                   anchor='e', tag='info UI')
    
    canvas.create_text(WINDOW_WIDTH - PADDING, PADDING + LINE_GAP * 7, 
                       text=f'Animation speed: {round(anim_speed, 3):.3f}', font=f'{FONT} {font_size}', 
                       anchor='e', tag='info UI')
    
    canvas.create_text(WINDOW_WIDTH - PADDING, PADDING + LINE_GAP * 8, 
                       text=f'Unit Circle Radius (px): {unit_circle_radius:.1f}', font=f'{FONT} {font_size}', 
                       anchor='e', tag='info UI')
    canvas.create_text(WINDOW_WIDTH - PADDING, PADDING + LINE_GAP * 9, 
                       text=f'Line & Point width scale: {scale:.1f}', font=f'{FONT} {font_size}', 
                       anchor='e', tag='info UI')
 
def hide_functions():
    '''Hides all trigonometric function visuals except the selected one.'''
    if show_only_sine:
        func_to_show = 'sine'
    elif show_only_cos:
        func_to_show = 'cos'
    elif show_only_tg:
        func_to_show = 'tg'
    elif show_only_cotg:
        func_to_show = 'cotg'
    elif show_all:
        func_to_show = 'all'
    
    if func_to_show != 'all':
        for function in ['sine', 'cos', 'tg', 'cotg']:
            if function != func_to_show:
                canvas.itemconfig(function, state="hidden")

def animate():
    '''Animates the rotation of the unit circle if not paused.'''
    global angle
    if not paused:
        angle += anim_speed
        canvas.delete('unit_circle')
        update_unit_circle()
        update_analytics()
        canvas.after(10, animate)

def cartesian_axis():
    '''Draws the cartesian axes and grid on the canvas.'''
    canvas.delete('cartesian')
    canvas.delete('grid')
    font_size = round(math.log(unit_circle_radius ** 2))

    text_offset_x = 1 + math.sqrt(unit_circle_radius)
    text_offset_y = 1 + math.sqrt(unit_circle_radius)
    canvas.create_line(0, WINDOW_Y_CENTER, WINDOW_WIDTH, WINDOW_Y_CENTER, fill = LINE_COLOR, width = math.log(unit_circle_radius ** scale), tag='cartesian')
    canvas.create_line(WINDOW_X_CENTER, 0, WINDOW_X_CENTER, WINDOW_HEIGHT, fill = LINE_COLOR, width = math.log(unit_circle_radius ** scale), tag='cartesian')
    canvas.create_text(WINDOW_WIDTH - text_offset_x, WINDOW_Y_CENTER - text_offset_y, text='x', font=f'{FONT} {font_size}', fill=FONT_COLOR, tag='cartesian')
    canvas.create_text(WINDOW_X_CENTER + text_offset_x, 0 + text_offset_y, text='y', font=f'{FONT} {font_size}', fill=FONT_COLOR, tag='cartesian')
    # Mark points

    step = unit_circle_radius
    point_radius = math.log(unit_circle_radius ** scale)  # In pixels.
    num_of_points = WINDOW_WIDTH // step
    x = WINDOW_X_CENTER - (step * (num_of_points // 2))
    y = WINDOW_Y_CENTER

    
    # Create points on X axis:
    for i in range(-(num_of_points // 2), num_of_points // 2 + 1):
        canvas.create_line(x, 0, x, WINDOW_HEIGHT, 
                            fill = '#c7c7c7', width = 1, tag='cartesian grid')
        canvas.create_oval(x - point_radius, y - point_radius, 
                           x + point_radius, y + point_radius, 
                           fill = POINT_COLOR, 
                           outline = LINE_COLOR, 
                           tag='cartesian')
        canvas.create_text(x - text_offset_x, y + text_offset_y, text=i, font=f'{FONT} {font_size}', fill=FONT_COLOR, tag='cartesian')
        x += step

    x = WINDOW_X_CENTER
    y = WINDOW_Y_CENTER - (step * (num_of_points // 2))

    # Create points on Y axis:
    for i in range(num_of_points // 2, -(num_of_points // 2 + 1), -1):
        if i == 0: 
            y += step
            continue
        canvas.create_line(0, y, WINDOW_WIDTH, y, 
                            fill = '#c7c7c7', width = 1, tag='cartesian grid')
        canvas.create_oval(x - point_radius, y - point_radius, 
                           x + point_radius, y + point_radius, 
                           fill = POINT_COLOR, 
                           outline = LINE_COLOR, tag='cartesian')
        canvas.create_text(x - text_offset_x, y + text_offset_y, text=i, font=f'{FONT} {font_size}', fill=FONT_COLOR, tag='cartesian')
        y += step
    if grid_hidden:
        canvas.itemconfig('grid', state='hidden')
    else:
        canvas.itemconfig('grid', state='normal')
    canvas.tag_lower('grid')
def create_pause_icon():
    '''Draws a pause icon on the canvas when animation is paused.'''
    canvas.delete('pause')
    canvas.create_rectangle(25, WINDOW_HEIGHT - 100, 50, WINDOW_HEIGHT - 25, fill = 'gray', tag='pause', width=0)
    canvas.create_rectangle(66, WINDOW_HEIGHT - 100, 91, WINDOW_HEIGHT - 25, fill = 'gray', tag='pause', width=0)


def delete_all_except_UI():
    '''Deletes all canvas items except those tagged as UI.'''
    all_items = canvas.find_all()
    for item in all_items:
        tags = canvas.gettags(item)
        if 'UI' not in tags:
            canvas.delete(item)

def zoom(event):
    '''Handles mouse wheel events to zoom in/out the unit circle.
    Args:
        event (tkinter.Event): The mouse wheel event.
    '''
    global unit_circle_radius
    global angle

    if event.delta == -120 and unit_circle_radius > 15:
        delete_all_except_UI()
        unit_circle_radius -= ZOOM_STRENGTH
        update_unit_circle()
        cartesian_axis()
        canvas.tag_lower('cartesian')
    if event.delta == 120 and unit_circle_radius < 500:
        delete_all_except_UI()
        unit_circle_radius += ZOOM_STRENGTH
        update_unit_circle()
        cartesian_axis()
        canvas.tag_lower('cartesian')
    if paused: create_pause_icon()
    update_analytics()
    canvas.tag_lower('arc')


def pause(event):
    '''Toggles the animation pause state and updates the UI accordingly.
    Args:
        event (tkinter.Event): The event that triggered the pause.
    '''
    global paused
    paused = not paused
    if paused:
        create_pause_icon()
    if not paused:
        canvas.delete('pause')
        animate()

def increase_anim_speed(event):
    '''Increases the animation speed and updates the analytics display.
    Args:
        event (tkinter.Event): The event that triggered the speed increase.
    '''
    global anim_speed
    if anim_speed < 8:
        anim_speed += 0.1
        update_analytics()
    else:
        anim_speed = 8
    canvas.itemconfig(ui_buttons[7], fill='lightgreen')

def decrease_anim_speed(event):
    '''Decreases the animation speed and updates the analytics display.
    Args:
        event (tkinter.Event): The event that triggered the speed decrease.
    '''
    global anim_speed
    if anim_speed > 0.1:
        anim_speed -= 0.1
        update_analytics()
    else:
        anim_speed = 0.1
    canvas.itemconfig(ui_buttons[8], fill='lightgreen')

def create_filter_buttons():
    '''Creates filter and control buttons for the UI on the canvas.'''
    if ui_hidden: return
    a = 60
    padding = 25
    spacing = a * 1.25
    font_size = 10
    ui_element = canvas.create_rectangle(padding, padding, padding + a, padding + a, width=2, tags='UI', fill=BG_COLOR)
    ui_buttons.append(ui_element)
    canvas.create_rectangle(padding, padding, padding + a / 3, padding + a / 3, width=2, tag='UI', fill=BG_COLOR)
    canvas.create_text(padding + a / 6, padding + a / 6, text='Q', font=f'{FONT} {font_size} bold', tag='UI', anchor=CENTER)
    canvas.create_text(padding + a / 2, padding + a / 1.5, text='Show\nsin(θ)', font=f'{FONT} {font_size} bold', tag='UI', anchor=CENTER)
    
    for i in range(1, 5):
        if i == 1: 
            text = 'W'
            inner_text = 'Show\ncos(θ)'
        elif i == 2: 
            text = 'E'
            inner_text = 'Show\ntg(θ)'
        elif i == 3: 
            text = 'R'
            inner_text = 'Show\ncotg(θ)'
        elif i == 4: 
            text = 'T'
            inner_text = 'Show All'

        ui_element = canvas.create_rectangle(padding + spacing * i, padding, padding + spacing * i + a, padding + a, width=2, tags='UI', 
                                fill= BG_COLOR if i != 4 else 'LightGreen')
        ui_buttons.append(ui_element)
        canvas.create_rectangle(padding + spacing * i, padding, padding + spacing * i + a / 3, padding + a / 3, width=2, tag='UI', fill=BG_COLOR)
        canvas.create_text(padding + spacing * i + a / 6, padding + a / 6, text=text, font=f'{FONT} {font_size} bold', tag='UI', anchor=CENTER)
        canvas.create_text(padding + spacing * i + a / 2, padding + a / 1.5, text=inner_text, font=f'{FONT} {font_size} bold', tag='UI', anchor=CENTER)

    
    # Second row:
    for i in range(6):
        if i == 0: 
            text = 'A'
            inner_text = 'Round\nangle'
        if i == 1: 
            text = 'X'
            inner_text = 'Reset'
        if i == 2: 
            text = '▲'
            inner_text = '+ Speed'
        if i == 3: 
            text = '▼'
            inner_text = '- Speed'
        if i == 4: 
            text = 'H'
            inner_text = 'Hide UI'
        if i == 5: 
            text = 'G'
            inner_text = 'Hide\nGrid'
        ui_element = canvas.create_rectangle(padding + spacing * i, padding + spacing, padding + spacing * i + a, padding + spacing + a, 
                                             width=2, tags='UI', fill=BG_COLOR)
        ui_buttons.append(ui_element)
        canvas.create_rectangle(padding + spacing * i, padding + spacing, padding + spacing * i + a / 3, padding + spacing + a / 3, 
                                width=2, tag='UI', fill=BG_COLOR)
        canvas.create_text(padding + spacing * i + a / 6, padding + spacing + a / 6, text=text, font=f'{FONT} {font_size} bold', tag='UI', anchor=CENTER)
        canvas.create_text(padding + spacing * i + a / 2, padding + spacing + a / 1.5, text=inner_text, font=f'{FONT} {font_size} bold', tag='UI', anchor=CENTER)

    # extra text:
    for i in range(7):
        if i == 0:
            text = 'Spacebar - Pause/Unpause'
        if i == 1:
            text = 'F11 - Toggle Fullscreen'
        if i == 2:
            text = 'LMB - Adjust Angle'
        if i == 3:
            text = 'RMB - Adjust Angle in 15° Increments'
        if i == 4:
            text = '◀ ▶- Decrease/Increase Line Width'
        if i == 5:
            text = 'Scroll - Zoom Out/In'
        if i == 6:
            text = 'ESC - Close Application'
        canvas.delete('info')
        line_gap = 8 + font_size
        canvas.create_text(padding, padding + spacing * 2 + line_gap * i, text=text, anchor='w', tag='UI', font=f'{FONT} {font_size} bold')


def change_color_of_button(identifier):
    '''Highlights the selected UI button and resets others to default color.
    Args:
        identifier (int): The index of the button to highlight.
    '''
    for i in range(len(ui_buttons)):
        canvas.itemconfig(ui_buttons[i], fill=BG_COLOR)
    canvas.itemconfig(ui_buttons[identifier], fill='LightGreen')

def filter_functions(tag):
    '''Sets which trigonometric function(s) to display based on the selected tag.
    Args:
        tag (str): The tag indicating which function(s) to display (e.g., 'sine', 'cosine', etc.).
    '''
    global show_only_sine
    global show_only_cos
    global show_only_cotg
    global show_only_tg
    global show_all

    if tag == 'sine': 
        change_color_of_button(0)
        show_only_sine, show_only_cos, show_only_cotg, show_only_tg, show_all = True, False, False, False, False

    elif tag == 'cosine':
        change_color_of_button(1)
        show_only_sine, show_only_cos, show_only_cotg, show_only_tg, show_all = False, True, False, False, False

    elif tag == 'tg':
        change_color_of_button(2)
        show_only_sine, show_only_cos, show_only_cotg, show_only_tg, show_all = False, False, False, True, False

    elif tag == 'cotg':
        change_color_of_button(3)
        show_only_sine, show_only_cos, show_only_cotg, show_only_tg, show_all = False, False, True, False, False

    elif tag == 'all':
        change_color_of_button(4)
        show_only_sine, show_only_cos, show_only_cotg, show_only_tg, show_all = False, False, False, False, True
    update_unit_circle()

def on_key_press(event):
    '''Handles key press events to filter functions based on the pressed key.
    Args:
        event (tkinter.Event): The key press event containing the pressed key.
    '''
    key_mapping = {
        "q": 'sine',
        "w": 'cosine',
        "e": 'tg',
        "r": 'cotg',
        "t": 'all',
    }
    tag = key_mapping.get(event.char.lower())
    if tag:
        filter_functions(tag)


def get_angle(x: float, y: float, rounding: int) -> float:
    '''Calculate the angle in degrees based on the mouse position.
    Args:
        x (float): The x-coordinate of the mouse.
        y (float): The y-coordinate of the mouse.
        rounding (int): The rounding value for the angle. Default is 0 (no rounding).
    Returns:
        float: The angle in degrees, rounded to the specified value.
    '''
    dx = x - WINDOW_X_CENTER
    dy = WINDOW_Y_CENTER - y
    angle = math.degrees(math.atan2(dy, dx))
    if rounding == 0:
        return round(angle % 360, 2)
    else:
        return (round(angle / rounding) * rounding) % 360
def on_mouse_down(event):
    '''Handles mouse button press event to set the angle and changes cursor to a hand to improve user experience.
    Args:
        event (tkinter.Event): The mouse event containing the x and y coordinates.
    '''
    set_angle(event.x, event.y)
    root.config(cursor="tcross")

def set_angle(mouse_x: float, mouse_y: float, rounding = 0):
    '''Sets the angle based on mouse position and updates the unit circle.
    Args:
        mouse_x (float): The x-coordinate of the mouse.
        mouse_y (float): The y-coordinate of the mouse.
        rounding (int, optional): The rounding value for the angle. Default is 0 (no rounding).
    '''
    global angle
    global paused
    paused = True
    angle_tooltip_offset = 20
    angle = get_angle(mouse_x, mouse_y, rounding)
    canvas.delete('angletooltip')
    canvas.create_text(mouse_x, mouse_y - angle_tooltip_offset,
                       text=f'{angle}°', tag='angletooltip UI', font=f'{FONT} 10 bold' )
    update_unit_circle()
    create_pause_icon()
    update_analytics()

def on_mouse_move(event):
    '''Handles mouse movement while the left mouse button is held down to update the angle.
    Args:
        event (tkinter.Event): The mouse move event.
    '''
    set_angle(event.x, event.y)

def on_mouse_up(event):
    '''Handles mouse button release event to reset the cursor and remove angle tooltip.
    Args:
        event (tkinter.Event): The mouse button release event.
    '''
    root.config(cursor="")
    canvas.delete('angletooltip')
    
def on_right_mouse_move(event):
    '''Handles right mouse movement to set angle in increments defined by global_rounding.
    Args:
        event (tkinter.Event): The right mouse move event.
    '''
    set_angle(event.x, event.y, global_rounding)

def on_right_mouse_down(event):
    '''Handles right mouse button press to set angle in increments and change cursor.
    Args:
        event (tkinter.Event): The right mouse button press event.
    '''
    set_angle(event.x, event.y, global_rounding)
    root.config(cursor="tcross")

def map_key_release(event):
    '''Resets the color of UI buttons when their corresponding key is released.
    Args:
        event (tkinter.Event): The key release event.
    '''
    pressed = event.keysym.lower()
    if pressed == 'a':
        canvas.itemconfig(ui_buttons[5], fill=BG_COLOR)
    if pressed == 'x':
        canvas.itemconfig(ui_buttons[6], fill=BG_COLOR)
    if pressed == 'up':
        canvas.itemconfig(ui_buttons[7], fill=BG_COLOR)
    if pressed == 'down':
        canvas.itemconfig(ui_buttons[8], fill=BG_COLOR)
    if pressed == 'h':
        canvas.itemconfig(ui_buttons[9], fill=BG_COLOR)
    if pressed == 'g':
        canvas.itemconfig(ui_buttons[10], fill=BG_COLOR)

def round_angle(event):
    '''Rounds the current angle to the nearest integer and updates the display.
    Args:
        event (tkinter.Event): The event that triggered rounding.
    '''
    global angle
    angle = round(angle)
    update_unit_circle()
    canvas.itemconfig(ui_buttons[5], fill='lightgreen')
    update_analytics()

def reset(event):
    '''Resets the angle, scale, and animation speed to their default values.
    Args:
        event (tkinter.Event): The event that triggered the reset.
    '''
    global angle
    global scale
    global anim_speed
    anim_speed = 0.1
    angle = 0
    scale = 0.5
    update_unit_circle()
    cartesian_axis()
    canvas.itemconfig(ui_buttons[6], fill='lightgreen')
    update_analytics()
    canvas.tag_lower('cartesian')

ui_hidden = False
def hide_ui(event):
    '''Toggles the visibility of the UI elements on the canvas.
    Args:
        event (tkinter.Event): The event that triggered the UI toggle.
    '''
    global ui_hidden
    ui_hidden = not ui_hidden
    if ui_hidden:
        canvas.itemconfig('UI', state='hidden')
        canvas.itemconfig(ui_buttons[9], fill='lightgreen')
    else:
        canvas.itemconfig('UI', state='normal')

is_fullscreen = True
root.attributes("-fullscreen", is_fullscreen)
def toggle_fullscreen(event):
    '''Toggles fullscreen mode for the application window.
    Args:
        event (tkinter.Event): The event that triggered fullscreen toggle.
    '''
    global is_fullscreen
    is_fullscreen = not is_fullscreen 
    root.attributes("-fullscreen", is_fullscreen)

def exit_fullscreen(event):
    '''Exits fullscreen mode for the application window.
    Args:
        event (tkinter.Event): The event that triggered exit from fullscreen.
    '''
    global is_fullscreen
    is_fullscreen = False
    root.attributes("-fullscreen", is_fullscreen)

grid_hidden = False
def hide_grid(event):
    '''Toggles the visibility of the grid on the canvas.
    Args:
        event (tkinter.Event): The event that triggered the grid toggle.
    '''
    global grid_hidden
    grid_hidden = not grid_hidden
    if grid_hidden:
        canvas.itemconfig('grid', state='hidden')
    else:
        canvas.itemconfig('grid', state='normal')
    canvas.itemconfig(ui_buttons[10], fill='lightgreen')

def increase_line_width(event):
    '''Increases the width of lines and points in the visualization.
    Args:
        event (tkinter.Event): The event that triggered the increase.
    '''
    global scale
    if scale < 1:
        scale += 0.1
    else:
        scale = 1
    update_unit_circle()
    update_analytics()
    cartesian_axis()
    canvas.tag_lower('cartesian')
    canvas.tag_lower('arc')

def decrease_line_width(event):
    '''Decreases the width of lines and points in the visualization.
    Args:
        event (tkinter.Event): The event that triggered the decrease.
    '''
    global scale
    if scale > 0.1:
        scale -= 0.1
    else:
        scale = 0.1
    update_unit_circle()
    update_analytics()
    cartesian_axis()
    canvas.tag_lower('cartesian')
    canvas.tag_lower('arc')

def confirm_exit(event):
    '''Asks the user for confirmation before closing the application.
    Args:
        event (tkinter.Event): The event that triggered the exit confirmation.
    '''
    answer = messagebox.askyesno("Confirm Exit", "Are you sure you want to quit?")
    if answer:
        root.destroy()

create_filter_buttons()
update_unit_circle()
cartesian_axis()
update_analytics()

root.bind("<F11>", toggle_fullscreen)
root.bind('<MouseWheel>', zoom)
root.bind('<space>', pause)
root.bind('<Up>', increase_anim_speed)
root.bind('<Left>', decrease_line_width)
root.bind('<Right>', increase_line_width)
root.bind('<Down>', decrease_anim_speed)
root.bind('<Key>', on_key_press)
root.bind('<ButtonPress-1>', on_mouse_down)
root.bind("<ButtonRelease-1>", on_mouse_up)
root.bind('<ButtonPress-3>', on_right_mouse_down)
root.bind("<ButtonRelease-3>", on_mouse_up)
root.bind("<B1-Motion>", on_mouse_move)
root.bind("<B3-Motion>", on_right_mouse_move)
root.bind("<a>", round_angle)
root.bind("<A>", round_angle) # when CAPS is on it doesnt register button press (lazy fix but who cares)
root.bind("<x>", reset)
root.bind("<X>", reset)
root.bind("<h>", hide_ui)
root.bind("<H>", hide_ui)
root.bind("<g>", hide_grid)
root.bind("<G>", hide_grid)
root.bind("<Escape>", confirm_exit)
root.bind("<KeyRelease>", map_key_release)

center_screen()
animate()
root.mainloop()