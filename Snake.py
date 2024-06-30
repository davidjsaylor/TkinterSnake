import json
import os
import platform
import random
import time
import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import ttk, colorchooser
from datetime import datetime


# Constants
FILE_PATH = os.path.dirname(__file__)
SPEED_OPTIONS = {'Slow': 150, 'Medium': 100, 'Fast': 50}
INITIAL_POSITION = (20, 20)

# Default Themes
default_app_theme = {
    'background_color': '#1F1F1F',
    'foreground_color': '#FFFFFF',
    'active_background': '#666666',
    'active_foreground': '#FFFFFF',
    'disabled_background': '#1F1F1F',
    'disabled_foreground': '#FFFFFF',
    'padx': 10,
    'pady': 10,
    'windows_font': 'Arial',
    'linux_font': 'DejaVu Sans',
    'mac_font': 'Helvetica'
}

default_game_theme = {
    'snake_size': 20,
    'canvas_width': 800,
    'canvas_height': 800,
    'title_color': '#FF0000',
    'logo_color': '#FFFFFF',
    'snake_color': '#00FF00',
    'food_color': '#FF0000',
    'gameover_color': '#FFFFFF'
}

# Load themes
def load_themes(file_name, default_theme):
    try:
        with open(f'{FILE_PATH}/{file_name}', 'r') as file:
            themes = json.load(file)
    except FileNotFoundError:
        themes = {"Default Theme": default_theme}
        with open(f'{FILE_PATH}/{file_name}', 'w') as file:
            json.dump(themes, file, indent=4)
    return themes

app_themes = load_themes("app_themes.json", default_app_theme)
game_themes = load_themes("game_themes.json", default_game_theme)

class CustomNotebook(ttk.Notebook):
    def __init__(self, *args, **kwargs):
        app_theme = kwargs.pop('app_theme', {})
        super().__init__(*args, **kwargs)
        self.style = ttk.Style()
        self.style.configure('Custom.TNotebook',
                             background=app_theme['background_color'],
                             foreground=app_theme['foreground_color'],
                             activebackground=app_theme['active_background'],
                             activeforeground=app_theme['active_foreground'],
                             disabledbackground=app_theme['disabled_background'],
                             disabledforeground=app_theme['disabled_foreground']
                             )
        self.style.configure('Custom.TNotebook.Tab',
                             background=app_theme['background_color'],
                             foreground=app_theme['foreground_color'],
                             activebackground=app_theme['active_background'],
                             activeforeground=app_theme['active_foreground'],
                             disabledbackground=app_theme['disabled_background'],
                             disabledforeground=app_theme['disabled_foreground']
                             )
        self.style.map('Custom.TNotebook.Tab', background=[('selected', app_theme.get('active_background'))])
        self.configure(style='Custom.TNotebook')

class CustomTreeview(ttk.Treeview):
    def __init__(self, *args, **kwargs):
        app_theme = kwargs.pop('app_theme', {})
        super().__init__(*args, **kwargs)
        self.style = ttk.Style()
        self.style.configure('Custom.Treeview',
                             background=app_theme['background_color'],
                             foreground=app_theme['foreground_color'],
                             activebackground=app_theme['active_background'],
                             activeforeground=app_theme['active_foreground'],
                             disabledbackground=app_theme['disabled_background'],
                             disabledforeground=app_theme['disabled_foreground'],
                             fieldbackground=app_theme.get('background_color')
                             )
        self.style.configure('Custom.Treeview.Heading',
                             background=app_theme['background_color'],
                             foreground=app_theme['foreground_color'],
                             activebackground=app_theme['active_background'],
                             activeforeground=app_theme['active_foreground'],
                             disabledbackground=app_theme['disabled_background'],
                             disabledforeground=app_theme['disabled_foreground']
                             )
        self.style.map('Custom.Treeview.Heading', background=[('active', app_theme.get('active_background'))])
        self.configure(style='Custom.Treeview')

class CustomOptionMenu(tk.OptionMenu):
    def __init__(self, master, variable, *values, app_theme=None, **kwargs):
        super().__init__(master, variable, *values, **kwargs)
        self.config(
            background=app_theme['background_color'],
            foreground=app_theme['foreground_color'],
            activebackground=app_theme['active_background'],
            activeforeground=app_theme['active_foreground'],
            highlightbackground=app_theme['foreground_color'],
            highlightcolor=app_theme['foreground_color'],
            highlightthickness=1,
            bd=1
        )
        self['menu'].config(
            background=app_theme['background_color'],
            foreground=app_theme['foreground_color'],
            activebackground=app_theme['active_background'],
            activeforeground=app_theme['active_foreground']
        )

    def set_menu(self, value, *values):
        menu = self['menu']
        menu.delete(0, 'end')
        for val in values:
            menu.add_command(label=val, command=tk._setit(self.variable, val))
        self.variable.set(value)

class CustomEntry(tk.Entry):
    def __init__(self, master=None, app_theme=None, **kwargs):
        super().__init__(master, **kwargs)
        self.config(
            background=app_theme['background_color'],
            foreground=app_theme['foreground_color'],
            disabledbackground=app_theme['disabled_background'],
            disabledforeground=app_theme['disabled_foreground'],
            readonlybackground=app_theme['disabled_background'],
            insertbackground=app_theme['foreground_color']
        )

class CustomLabel(tk.Label):
    def __init__(self, master=None, app_theme=None, **kwargs):
        super().__init__(master, **kwargs)
        self.config(
            background=app_theme['background_color'],
            foreground=app_theme['foreground_color'],
            activebackground=app_theme['active_background'],
            activeforeground=app_theme['active_foreground'],
        )

class CustomButton(tk.Button):
    def __init__(self, master=None, app_theme=None, **kwargs):
        super().__init__(master, **kwargs)
        self.config(
            background=app_theme['background_color'],
            foreground=app_theme['foreground_color'],
            activebackground=app_theme['active_background'],
            activeforeground=app_theme['active_foreground'],
        )

class CustomFrame(tk.Frame):
    def __init__(self, master=None, app_theme=None, **kwargs):
        super().__init__(master, **kwargs)
        self.config(background=app_theme['background_color'])

class CustomColorChooser(tk.Toplevel):
    def __init__(self, master=None, app_theme=None, on_color_chosen=None, title="", initial_color="#000000"):
        super().__init__(master)
        self.title(f"Choose Color for: {title}")
        self.on_color_chosen = on_color_chosen
        self.app_theme = app_theme
        self.initial_color = initial_color
        self.withdraw()
        self.overrideredirect(True)

        self.frame = CustomFrame(self, app_theme=app_theme, bd=1, relief='solid',
                                 highlightbackground=app_theme['foreground_color'],
                                 highlightcolor=app_theme['foreground_color'],
                                 highlightthickness=1)
        self.frame.pack(fill='both', expand=True)

        self.title_bar = CustomFrame(self.frame, app_theme=app_theme, relief='raised', bd=0)
        self.title_bar.pack(fill=tk.X, side=tk.TOP)

        self.title_label = CustomLabel(self.title_bar, text=self.title(), app_theme=app_theme, bd=0, relief='flat', highlightthickness=0, cursor='arrow')
        self.title_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2, pady=2)

        self.close_button = CustomButton(self.title_bar, text='X', command=self.destroy, app_theme=app_theme, bd=0, padx=5, pady=2, relief='flat')
        self.close_button.pack(side=tk.RIGHT, padx=2, pady=2)

        self.title_label.bind('<ButtonPress-1>', self.start_move)
        self.title_label.bind('<B1-Motion>', self.on_move)

        self.color_frame = CustomFrame(self.frame, app_theme=app_theme)
        self.color_frame.pack(fill='both', expand=True)

        self.previous_color_canvas = tk.Canvas(self.color_frame, width=100, height=100, bg=self.initial_color)
        self.previous_color_canvas.grid(row=0, column=0, padx=10, pady=10)

        self.new_color_canvas = tk.Canvas(self.color_frame, width=100, height=100, bg=self.initial_color)
        self.new_color_canvas.grid(row=0, column=1, padx=10, pady=10)

        self.red_scale = tk.Scale(self.color_frame, from_=0, to=255, orient=tk.HORIZONTAL, label="Red",
                                  command=self.update_color)
        self.red_scale.grid(row=1, column=0, columnspan=2, padx=10, pady=5)
        self.green_scale = tk.Scale(self.color_frame, from_=0, to=255, orient=tk.HORIZONTAL, label="Green",
                                    command=self.update_color)
        self.green_scale.grid(row=2, column=0, columnspan=2, padx=10, pady=5)
        self.blue_scale = tk.Scale(self.color_frame, from_=0, to=255, orient=tk.HORIZONTAL, label="Blue",
                                   command=self.update_color)
        self.blue_scale.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

        self.hex_color_var = tk.StringVar(value=self.initial_color)
        self.hex_color_entry = CustomEntry(self.color_frame, textvariable=self.hex_color_var, app_theme=app_theme,
                                           state='readonly', cursor='arrow')
        self.hex_color_entry.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        self.ok_button = CustomButton(self.color_frame, text='OK', command=self.choose_color, app_theme=app_theme)
        self.ok_button.grid(row=5, column=0, padx=10, pady=10)

        self.cancel_button = CustomButton(self.color_frame, text='Cancel', command=self.destroy, app_theme=app_theme)
        self.cancel_button.grid(row=5, column=1, padx=10, pady=10)

        self.after(100, self.center_over_master)
        self.after(100, self.deiconify)

    def center_over_master(self):
        self.master.update_idletasks()
        master_geometry = self.master.winfo_geometry()
        master_width = self.master.winfo_width()
        master_height = self.master.winfo_height()
        master_x = self.master.winfo_x()
        master_y = self.master.winfo_y()

        self.update_idletasks()
        window_width = self.winfo_reqwidth()
        window_height = self.winfo_reqheight()

        pos_x = master_x + (master_width // 2) - (window_width // 2)
        pos_y = master_y + (master_height // 2) - (window_height // 2)

        self.geometry(f'{window_width}x{window_height}+{pos_x}+{pos_y}')

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def on_move(self, event):
        x = event.x_root - self.x
        y = event.y_root - self.y
        self.geometry(f'+{x}+{y}')

    def update_color(self, *args):
        new_color = f'#{self.red_scale.get():02x}{self.green_scale.get():02x}{self.blue_scale.get():02x}'
        self.new_color_canvas.config(bg=new_color)
        self.hex_color_var.set(new_color)

    def choose_color(self):
        if self.on_color_chosen:
            self.on_color_chosen(self.hex_color_var.get())
        self.destroy()

class CustomMessageBox(tk.Toplevel):
    def __init__(self, master=None, title="Message", message="", app_theme=None, on_confirm=None, on_cancel=None):
        super().__init__(master)
        self.title(title)
        self.withdraw()
        self.overrideredirect(True)
        self.app_theme = app_theme
        self.frame = CustomFrame(self, app_theme=app_theme, bd=1, relief='solid',
                                 highlightbackground=app_theme['foreground_color'],
                                 highlightcolor=app_theme['foreground_color'],
                                 highlightthickness=1)
        self.frame.pack(fill='both', expand=True)

        self.title_bar = CustomFrame(self.frame, app_theme=app_theme, relief='raised', bd=0)
        self.title_bar.pack(fill=tk.X, side=tk.TOP)

        self.title_label = CustomLabel(self.title_bar, text=title, app_theme=app_theme, bd=0, relief='flat', highlightthickness=0, cursor='arrow')
        self.title_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2, pady=2)

        self.close_button = CustomButton(self.title_bar, text='X', command=self.destroy, app_theme=app_theme, bd=0, padx=5, pady=2, relief='flat')
        self.close_button.pack(side=tk.RIGHT, padx=2, pady=2)

        self.title_label.bind('<ButtonPress-1>', self.start_move)
        self.title_label.bind('<B1-Motion>', self.on_move)

        self.message_label = CustomLabel(self.frame, text=message, app_theme=app_theme)
        self.message_label.pack(padx=10, pady=10)

        self.button_frame = CustomFrame(self.frame, app_theme=app_theme)
        self.button_frame.pack(pady=10)

        self.ok_button = CustomButton(self.button_frame, text='OK', command=lambda: [on_confirm(), self.destroy()] if on_confirm else self.destroy, app_theme=app_theme)
        self.ok_button.pack(side=tk.LEFT, padx=10)

        self.cancel_button = CustomButton(self.button_frame, text='Cancel', command=self.destroy, app_theme=app_theme)
        self.cancel_button.pack(side=tk.RIGHT, padx=10)

        self.after(100, self.center_over_master)
        self.after(100, self.deiconify)

    def center_over_master(self):
        self.master.update_idletasks()
        master_geometry = self.master.winfo_geometry()
        master_width = self.master.winfo_width()
        master_height = self.master.winfo_height()
        master_x = self.master.winfo_x()
        master_y = self.master.winfo_y()

        self.update_idletasks()
        window_width = self.winfo_reqwidth()
        window_height = self.winfo_reqheight()

        pos_x = master_x + (master_width // 2) - (window_width // 2)
        pos_y = master_y + (master_height // 2) - (window_height // 2)

        self.geometry(f'{window_width}x{window_height}+{pos_x}+{pos_y}')

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def on_move(self, event):
        x = event.x_root - self.x
        y = event.y_root - self.y
        self.geometry(f'+{x}+{y}')

class CustomToplevel(tk.Toplevel):
    def __init__(self, master, *args, **kwargs):
        self.master = master
        app_theme = kwargs.pop('app_theme', {})
        title = kwargs.pop('title', 'Window')
        super().__init__(master, *args, **kwargs)
        self.withdraw()
        self.overrideredirect(True)
        self.frame = CustomFrame(self, app_theme=app_theme, bd=1, relief='solid',
                                 highlightbackground=app_theme['foreground_color'],
                                 highlightcolor=app_theme['foreground_color'],
                                 highlightthickness=1)
        self.frame.pack(fill='both', expand=True)

        self.title_bar = CustomFrame(self.frame, app_theme=app_theme, relief='raised', bd=0)
        self.title_bar.pack(fill=tk.X, side=tk.TOP)

        self.title_label = CustomLabel(self.title_bar, text=title, app_theme=app_theme, bd=0, relief='flat', highlightthickness=0, cursor='arrow')
        self.title_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2, pady=2)

        self.close_button = CustomButton(self.title_bar, text='X', command=self.destroy, app_theme=app_theme, bd=0, padx=5, pady=2, relief='flat')
        self.close_button.pack(side=tk.RIGHT, padx=2, pady=2)

        self.title_label.bind('<ButtonPress-1>', self.start_move)
        self.title_label.bind('<B1-Motion>', self.on_move)

        self.frame_content = CustomFrame(self.frame, app_theme=app_theme)
        self.frame_content.pack(fill='both', expand=True)

        self.status_bar = CustomFrame(self.frame, app_theme=app_theme)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        self.status_label = CustomLabel(self.status_bar, text='', app_theme=app_theme)
        self.status_label.pack(side=tk.LEFT, padx=10, pady=5)

        self.after(100, self.center_over_master)
        self.after(100, self.deiconify)

    def center_over_master(self):
        self.master.update_idletasks()
        master_geometry = self.master.winfo_geometry()
        master_width = self.master.winfo_width()
        master_height = self.master.winfo_height()
        master_x = self.master.winfo_x()
        master_y = self.master.winfo_y()

        self.update_idletasks()
        window_width = self.winfo_reqwidth()
        window_height = self.winfo_reqheight()

        pos_x = master_x + (master_width // 2) - (window_width // 2)
        pos_y = master_y + (master_height // 2) - (window_height // 2)

        self.geometry(f'{window_width}x{window_height}+{pos_x}+{pos_y}')

    def start_move(self, event):
        print('start moving')
        self.x = event.x
        self.y = event.y

    def on_move(self, event):
        print('on move')
        x = event.x_root - self.x
        y = event.y_root - self.y
        self.geometry(f'+{x}+{y}')

    def set_status(self, message):
        self.status_label.config(text=message)
        self.after(5000, lambda: self.status_label.config(text=''))

    def set_title(self, title):
        self.title_label.config(text=title)

class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.master.title('Snake')
        self.settings = self.load_settings()
        self.current_app_theme = self.settings.get('app_theme', 'Default Theme')
        self.current_game_theme = self.settings.get('game_theme', 'Default Theme')
        self.app_theme = app_themes[self.current_app_theme]
        self.game_theme = game_themes[self.current_game_theme]

        self.master.protocol('WM_DELETE_WINDOW', self.on_closing)
        
        self.game_loop_id = None
        self.direction_queue = []

        self.player_name = tk.StringVar(value=self.settings.get('player_name', ''))

        self.movement_keys = self.settings.get('movement_keys', {'s': 'Left', 'e': 'Up', 'f': 'Right', 'd': 'Down'})
        self.pause_key = self.settings.get('pause_key', 'space')

        self.apply_theme()
        self.setup_ui()
        self.load_high_scores()
        self.initialize_game_state()

        self.master.bind('<KeyPress>', self.change_direction)
        self.master.bind(f'<{self.pause_key}>', self.toggle_pause)

    def setup_ui(self):
        self.toolbar = CustomFrame(self.master, app_theme=self.app_theme)
        self.toolbar.pack()

        self.start_button = CustomButton(self.toolbar, text='Start New Game', command=self.start_game, app_theme=self.app_theme)
        self.start_button.pack(side=tk.LEFT, padx=self.app_theme['padx'], pady=self.app_theme['pady'])

        self.speed_var = tk.StringVar(value=self.settings.get('speed', 'Medium'))
        self.speed_menu = CustomOptionMenu(self.toolbar, self.speed_var, *list(SPEED_OPTIONS.keys()), app_theme=self.app_theme)
        self.speed_menu.pack(side=tk.LEFT, padx=self.app_theme['padx'], pady=self.app_theme['pady'])

        self.change_keys_button = CustomButton(self.toolbar, text='Controls', command=self.change_keys, app_theme=self.app_theme)
        self.change_keys_button.pack(side=tk.LEFT, padx=self.app_theme['padx'], pady=self.app_theme['pady'])

        self.themes_button = CustomButton(self.toolbar, text='Themes', command=self.change_theme, app_theme=self.app_theme)
        self.themes_button.pack(side=tk.LEFT, padx=self.app_theme['padx'], pady=self.app_theme['pady'])

        self.scores_button = CustomButton(self.toolbar, text='Top Scores', command=self.show_high_scores, app_theme=self.app_theme)
        self.scores_button.pack(side=tk.LEFT, padx=self.app_theme['padx'], pady=self.app_theme['pady'])

        self.exit_button = CustomButton(self.toolbar, text='Exit', command=self.master.quit, app_theme=self.app_theme)
        self.exit_button.pack(side=tk.LEFT, padx=self.app_theme['padx'], pady=self.app_theme['pady'])

        self.canvas = tk.Canvas(self.master, width=self.game_theme['canvas_width'], height=self.game_theme['canvas_height'], background='black')
        self.canvas.pack()

        self.draw_title_screen()

        self.status_bar = CustomFrame(self.master, app_theme=self.app_theme)
        self.status_bar.pack(fill=tk.X)

        self.score_label = CustomLabel(self.status_bar, text='Length: 1', anchor='w', app_theme=self.app_theme)
        self.score_label.pack(side=tk.LEFT, padx=self.app_theme['padx'], pady=self.app_theme['pady'])

        self.timer_label = CustomLabel(self.status_bar, text='Time: 0s', anchor='center', app_theme=self.app_theme)
        self.timer_label.pack(side=tk.LEFT, expand=True, padx=self.app_theme['padx'], pady=self.app_theme['pady'])

        self.difficulty_label = CustomLabel(self.status_bar, text=f'Difficulty: {self.speed_var.get()}', anchor='e', app_theme=self.app_theme)
        self.difficulty_label.pack(side=tk.LEFT, padx=self.app_theme['padx'], pady=self.app_theme['pady'])

    def initialize_game_state(self):
        self.snake = [INITIAL_POSITION]
        self.food = [self.create_food()]
        self.direction = 'Right'
        self.running = False
        self.paused = False
        self.start_time = None
        self.last_time = None
        self.elapsed_time = 0

    def load_settings(self):
        try:
            with open(f'{FILE_PATH}/settings.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_settings(self):
        settings = {
            'geometry': self.master.geometry(),
            'speed': self.speed_var.get(),
            'player_name': self.player_name.get(),
            'movement_keys': self.movement_keys,
            'pause_key': self.pause_key,
            'app_theme': self.current_app_theme,
            'game_theme': self.current_game_theme
        }
        with open(f'{FILE_PATH}/settings.json', 'w') as file:
            json.dump(settings, file, indent=4)

    def restore_settings(self):
        if 'geometry' in self.settings:
            self.master.geometry(self.settings['geometry'])

    def on_closing(self):
        self.save_settings()
        self.master.destroy()

    def start_game(self):
        if self.game_loop_id:
            self.master.after_cancel(self.game_loop_id)

        self.canvas.delete('all')
        self.snake = [INITIAL_POSITION]
        self.food = [self.create_food()]
        self.direction = 'Right'
        self.running = True
        self.paused = False
        self.start_time = time.time()
        self.last_time = self.start_time
        self.elapsed_time = 0
        self.canvas.delete('game_over')

        self.render_food()
        self.update_labels()
        self.master.config(cursor='none')
        self.game_loop()

    def create_food(self):
        max_x = int(self.game_theme['canvas_width']) // int(self.game_theme['snake_size']) - 1
        max_y = int(self.game_theme['canvas_height']) // int(self.game_theme['snake_size']) - 1
        while True:
            food = (random.randint(0, max_x) * int(self.game_theme['snake_size']), random.randint(0, max_y) * int(self.game_theme['snake_size']))
            if food not in self.snake:
                return food

    def render_snake(self):
        self.canvas.delete('snake')
        for x, y in self.snake:
            self.canvas.create_rectangle(x, y, x + int(self.game_theme['snake_size']), y + int(self.game_theme['snake_size']), fill=self.game_theme['snake_color'], tags='snake')

    def render_food(self):
        self.canvas.delete('food')
        x, y = self.food[0]
        self.canvas.create_rectangle(x, y, x + int(self.game_theme['snake_size']), y + int(self.game_theme['snake_size']), fill=self.game_theme['food_color'], tags='food')

    def change_direction(self, event):
        if event.keysym == 'n':
            self.confirm_new_game()
            return
        if self.paused:
            return
        if event.keysym in self.movement_keys:
            new_dir = self.movement_keys[event.keysym]
            opposites = {'Left': 'Right', 'Right': 'Left', 'Up': 'Down', 'Down': 'Up'}
            current_direction = self.direction_queue[-1] if self.direction_queue else self.direction

            if new_dir != opposites.get(current_direction):
                self.direction_queue.append(new_dir)

    def check_speed_change(self, value):
        if self.running:
            self.confirm_new_game()
        self.difficulty_label.config(text=f'Difficulty: {self.speed_var.get()}')

    def toggle_pause(self, event=None):
        if not self.running:
            return
        self.paused = not self.paused
        if self.paused:
            current_time = time.time()
            self.elapsed_time += (current_time - self.last_time)
            self.master.config(cursor='')
        else:
            self.last_time = time.time()
            self.master.config(cursor='none')

    def game_loop(self):
        if self.direction_queue:
            self.direction = self.direction_queue.pop(0)

        if self.running and not self.paused:
            self.move_snake()
            self.check_collision()
            self.update_timer()
            self.master.config(cursor='none')
        else:
            self.master.config(cursor='')

        if self.running:
            self.game_loop_id = self.master.after(SPEED_OPTIONS[self.speed_var.get()], self.game_loop)
        else:
            self.show_game_over()
            self.master.config(cursor='')

    def move_snake(self):
        head_x, head_y = self.snake[0]
        move_offsets = {'Left': (-int(self.game_theme['snake_size']), 0), 'Right': (int(self.game_theme['snake_size']), 0), 'Up': (0, -int(self.game_theme['snake_size'])), 'Down': (0, int(self.game_theme['snake_size']))}
        head_x += move_offsets[self.direction][0]
        head_y += move_offsets[self.direction][1]

        new_head = (head_x, head_y)
        self.snake.insert(0, new_head)

        if new_head == self.food[0]:
            self.food[0] = self.create_food()
            self.render_food()
            self.score_label.config(text=f'Length: {len(self.snake)}')
        else:
            self.snake.pop()

    def check_collision(self):
        head_x, head_y = self.snake[0]
        if head_x < 0 or head_x >= int(self.game_theme['canvas_width']) or head_y < 0 or head_y >= int(self.game_theme['canvas_height']) or self.snake[0] in self.snake[1:]:
            self.running = False

        self.render_snake()

    def show_game_over(self):
        self.update_timer()
        width = int(self.canvas.cget('width'))
        height = int(self.canvas.cget('height'))
        self.canvas.create_text(width // 2, height // 2, text='Game Over', fill=self.game_theme['gameover_color'], font=(self.get_font(), 24), tags='game_over')
        self.check_high_score()
        self.master.config(cursor='')

    def format_time(self, seconds):
        seconds = int(seconds)
        if seconds >= 3600:
            return f'{seconds // 3600}h {seconds % 3600 // 60}m {seconds % 60}s'
        elif seconds >= 60:
            return f'{seconds // 60}m {seconds % 60}s'
        else:
            return f'{seconds}s'

    def format_timestamp(self, timestamp):
        try:
            dt = datetime.fromtimestamp(float(timestamp))
            return dt.strftime('%A, %B %d, %Y at %I:%M%p')
        except ValueError:
            return timestamp

    def update_labels(self):
        self.score_label.config(text=f'Length: {len(self.snake)}')
        self.difficulty_label.config(text=f'Difficulty: {self.speed_var.get()}')

    def update_timer(self):
        if not self.paused and self.running:
            current_time = time.time()
            total_elapsed = self.elapsed_time + (current_time - self.last_time)
            self.timer_label.config(text=f'Time: {self.format_time(int(total_elapsed))}')

    def confirm_new_game(self):
        CustomMessageBox(self.master, title='New Game?', message='Are you sure you want to start a new game?', app_theme=self.app_theme, on_confirm=self.start_game)

    def load_high_scores(self):
        try:
            with open(f'{FILE_PATH}/top_scores.json', 'r') as file:
                self.high_scores = json.load(file)
        except FileNotFoundError:
            self.high_scores = {'Slow': [], 'Medium': [], 'Fast': []}

    def save_high_scores(self):
        with open(f'{FILE_PATH}/top_scores.json', 'w') as file:
            json.dump(self.high_scores, file, indent=4)

    def check_high_score(self):
        current_score = len(self.snake)
        current_time = int(time.time() - self.start_time)
        difficulty = self.speed_var.get()
        scores = self.high_scores[difficulty]
        if len(scores) < 10 or any(current_score > score[1] for score in scores):
            self.get_user_name()
            if self.player_name.get():
                scores.append([self.player_name.get(), current_score, current_time, time.time()])
                scores.sort(key=lambda x: x[1], reverse=True)
                self.high_scores[difficulty] = scores[:10]
                self.save_high_scores()

    def show_high_scores(self):
        scores_window = CustomToplevel(self.master, app_theme=self.app_theme, title='Top Scores')
        frame = scores_window.frame_content

        notebook = CustomNotebook(frame, app_theme=self.app_theme)
        notebook.pack(fill='both', expand=True)

        def update_title(event):
            tab_text = notebook.tab(notebook.select(), 'text')
            scores_window.set_title(f'{tab_text} Speed Top Scores')

        notebook.bind('<<NotebookTabChanged>>', update_title)

        for difficulty in ['Slow', 'Medium', 'Fast']:
            frame = ttk.Frame(notebook)
            notebook.add(frame, text=difficulty)

            tree = CustomTreeview(frame, columns=('Name', 'Score', 'Duration', 'Date'), show='headings', selectmode='extended', app_theme=self.app_theme)
            tree.pack(fill='both', expand=True)

            tree.heading('Name', text='Name')
            tree.heading('Score', text='Score')
            tree.heading('Duration', text='Duration')
            tree.heading('Date', text='Date')

            tree.column('Name', width=100, anchor='w')
            tree.column('Score', width=50, anchor='center')
            tree.column('Duration', width=100, anchor='center')
            tree.column('Date', width=200, anchor='center')

            if self.high_scores[difficulty]:
                for score in self.high_scores[difficulty]:
                    score[3] = self.format_timestamp(score[3])
                    tree.insert('', 'end', values=score)

            self.create_context_menu(tree, difficulty)

        difficulty_to_index = {'Slow': 0, 'Medium': 1, 'Fast': 2}
        current_difficulty_index = difficulty_to_index[self.speed_var.get()]
        notebook.select(current_difficulty_index)

    def create_context_menu(self, tree, difficulty):
        menu = tk.Menu(tree, tearoff=0, background=self.app_theme['background_color'], foreground=self.app_theme['foreground_color'])
        menu.add_command(label='Delete', command=lambda: self.delete_selected_items(tree, difficulty))

        tree.bind('<Button-3>', lambda event: self.show_context_menu(event, menu, tree))

        menu.bind('<FocusOut>', lambda event: menu.unpost())

    def show_context_menu(self, event, menu, tree):
        row_id = tree.identify_row(event.y)
        if row_id:
            tree.selection_set(row_id)
        try:
            menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            menu.grab_release()

    def delete_selected_items(self, tree, difficulty):
        selected_items = tree.selection()
        if not selected_items:
            return

        CustomMessageBox(self.master, title='Confirm Deletion', message='Are you sure you want to delete this score?', app_theme=self.app_theme, on_confirm=lambda: self.perform_deletion(tree, difficulty, selected_items))

    def perform_deletion(self, tree, difficulty, selected_items):
        for item in selected_items:
            tree.delete(item)

        self.high_scores[difficulty] = [
            [tree.item(child)['values'][0], tree.item(child)['values'][1], tree.item(child)['values'][2], tree.item(child)['values'][3]]
            for child in tree.get_children()
        ]
        self.save_high_scores()

    def draw_title_screen(self):
        self.title_text = self.canvas.create_text(
            self.game_theme['canvas_width'] // 2, 
            self.game_theme['canvas_height'] // 2 - 50, 
            text='Snake', 
            fill=self.game_theme['title_color'], 
            font=(self.get_font(), 44, 'bold')
        )
        self.logo_text = self.canvas.create_text(
            self.game_theme['canvas_width'] // 2, 
            self.game_theme['canvas_height'] // 2, 
            text='How big can your snake get?', 
            fill=self.game_theme['logo_color'], 
            font=(self.get_font(), 24)
        )

    def get_user_name(self):
        self.master.config(cursor='')

        dialog = CustomToplevel(self.master, app_theme=self.app_theme, title='New High Score!')
        frame = dialog.frame_content

        CustomLabel(frame, text='Enter your name:', app_theme=self.app_theme).pack(padx=10, pady=10)

        name_entry = CustomEntry(frame, textvariable=self.player_name, app_theme=self.app_theme)
        name_entry.pack(padx=10, pady=10)
        name_entry.focus_set()
        name_entry.select_range(0, tk.END)
        name_entry.bind('<KeyPress-Return>', lambda event: dialog.destroy())

        CustomButton(frame, text='OK', command=lambda: dialog.destroy(), app_theme=self.app_theme).pack(side=tk.LEFT, padx=10, pady=10)
        CustomButton(frame, text='Cancel', command=lambda: [self.player_name.set(''), dialog.destroy()], app_theme=self.app_theme).pack(side=tk.RIGHT, padx=10, pady=10)

        self.master.wait_window(dialog)

        if not self.paused and self.running:
            self.master.config(cursor='none')
        else:
            self.master.config(cursor='')

    def change_keys(self):
        dialog = CustomToplevel(self.master, app_theme=self.app_theme, title='Controls')
        frame = dialog.frame_content

        key_labels = ['Left', 'Up', 'Right', 'Down']
        key_vars = {key: tk.StringVar(value=self.get_key_for_direction(key)) for key in key_labels}
        pause_key_var = tk.StringVar(value=self.pause_key)

        def on_key_entry_click(key_var, entry):
            def on_key_press(event):
                key_var.set(event.keysym)
                dialog.unbind('<KeyPress>', on_key_press_id)
                entry.config(state='readonly', cursor='arrow')
                entry.selection_clear()
                dialog.focus()

            entry.config(state='normal', cursor='xterm')
            on_key_press_id = dialog.bind('<KeyPress>', on_key_press)
            entry.focus_set()

        entry_widgets = {}

        for i, key in enumerate(key_labels):
            CustomLabel(frame, text=f'{key} key:', app_theme=self.app_theme).grid(row=i, column=0, padx=10, pady=5)
            entry = CustomEntry(frame, textvariable=key_vars[key], state='readonly', app_theme=self.app_theme, cursor='arrow')
            entry.grid(row=i, column=1, padx=10, pady=5)
            entry_widgets[key] = entry
            CustomButton(frame, text='Set', command=lambda kv=key_vars[key], e=entry: on_key_entry_click(kv, e), app_theme=self.app_theme).grid(row=i, column=2, padx=10, pady=5)

        CustomLabel(frame, text='Pause key:', app_theme=self.app_theme).grid(row=len(key_labels), column=0, padx=10, pady=5)
        pause_entry = CustomEntry(frame, textvariable=pause_key_var, state='readonly', app_theme=self.app_theme, cursor='arrow')
        pause_entry.grid(row=len(key_labels), column=1, padx=10, pady=5)
        CustomButton(frame, text='Set', command=lambda: on_key_entry_click(pause_key_var, pause_entry), app_theme=self.app_theme).grid(row=len(key_labels), column=2, padx=10, pady=5)

        def save_keys():
            new_keys = {v.get(): k for k, v in key_vars.items()}
            new_pause_key = pause_key_var.get()
            if len(new_keys) != 4 or len(set(new_keys.keys())) != 4:
                dialog.set_status('Invalid keys. Please use unique keys.')
            else:
                self.movement_keys = new_keys
                self.pause_key = new_pause_key
                self.master.bind(f'<{self.pause_key}>', self.toggle_pause)
                self.save_settings()
                dialog.destroy()

        CustomButton(frame, text='Save', command=save_keys, app_theme=self.app_theme).grid(row=len(key_labels)+1, column=0, columnspan=3, pady=10)

    def get_key_for_direction(self, direction):
        for key, dir in self.movement_keys.items():
            if dir == direction:
                return key
        return ''

    def change_theme(self):
        dialog = CustomToplevel(self.master, app_theme=self.app_theme, title='Themes')
        frame = dialog.frame_content

        app_theme_var = tk.StringVar(value=self.current_app_theme)
        game_theme_var = tk.StringVar(value=self.current_game_theme)

        button_frame = CustomFrame(frame, app_theme=self.app_theme)
        button_frame.grid(row=0, column=0, columnspan=4, pady=10)

        CustomButton(button_frame, text='Create App Theme', command=lambda: self.create_theme('app', dialog), app_theme=self.app_theme).pack(side=tk.LEFT, padx=10)
        CustomButton(button_frame, text='Create Game Theme', command=lambda: self.create_theme('game', dialog), app_theme=self.app_theme).pack(side=tk.LEFT, padx=10)

        CustomLabel(frame, text='App Theme:', app_theme=self.app_theme).grid(row=1, column=0, padx=10, pady=10)
        app_theme_menu = CustomOptionMenu(frame, app_theme_var, *list(app_themes.keys()), app_theme=self.app_theme)
        app_theme_menu.grid(row=1, column=1, padx=10, pady=10)

        edit_app_button = CustomButton(frame, text='Edit', command=lambda: self.edit_theme('app', app_themes, app_theme_var), app_theme=self.app_theme)
        edit_app_button.grid(row=1, column=2, padx=10, pady=10)

        delete_app_button = CustomButton(frame, text='Delete', command=lambda: self.delete_theme('app', app_themes, app_theme_var), app_theme=self.app_theme)
        delete_app_button.grid(row=1, column=3, padx=10, pady=10)

        CustomLabel(frame, text='Game Theme:', app_theme=self.app_theme).grid(row=2, column=0, padx=10, pady=10)
        game_theme_menu = CustomOptionMenu(frame, game_theme_var, *list(game_themes.keys()), app_theme=self.app_theme)
        game_theme_menu.grid(row=2, column=1, padx=10, pady=10)

        edit_game_button = CustomButton(frame, text='Edit', command=lambda: self.edit_theme('game', game_themes, game_theme_var), app_theme=self.app_theme)
        edit_game_button.grid(row=2, column=2, padx=10, pady=10)

        delete_game_button = CustomButton(frame, text='Delete', command=lambda: self.delete_theme('game', game_themes, game_theme_var), app_theme=self.app_theme)
        delete_game_button.grid(row=2, column=3, padx=10, pady=10)

        def apply_themes():
            self.current_app_theme = app_theme_var.get()
            self.current_game_theme = game_theme_var.get()
            self.app_theme = app_themes[self.current_app_theme]
            self.game_theme = game_themes[self.current_game_theme]
            self.apply_theme()
            dialog.destroy()

        CustomButton(frame, text='Apply', command=apply_themes, app_theme=self.app_theme).grid(row=3, column=0, columnspan=4, pady=10)

        def refresh_optionmenus(event=None):
            app_theme_menu.set_menu(app_theme_var.get(), *list(app_themes.keys()))
            game_theme_menu.set_menu(game_theme_var.get(), *list(game_themes.keys()))
            edit_app_button.config(state='normal' if app_theme_var.get() != 'Default Theme' else 'disabled')
            delete_app_button.config(state='normal' if app_theme_var.get() != 'Default Theme' else 'disabled')
            edit_game_button.config(state='normal' if game_theme_var.get() != 'Default Theme' else 'disabled')
            delete_game_button.config(state='normal' if game_theme_var.get() != 'Default Theme' else 'disabled')

    def create_theme(self, theme_type, dialog):
        def save_new_theme(name, new_theme):
            themes[name] = new_theme
            self.save_themes(theme_type, themes)
            theme_var.set(name)
            self.apply_theme()
            dialog.set_status(f'{theme_type.capitalize()} Theme "{name}" created.')
            self.update_optionmenus()

        themes = app_themes if theme_type == 'app' else game_themes
        theme_var = tk.StringVar(value='')

        editor_window = CustomToplevel(self.master, app_theme=self.app_theme, title=f'Create New {theme_type.capitalize()} Theme')
        editor_frame = editor_window.frame_content

        theme_name_var = tk.StringVar(value='')
        CustomLabel(editor_frame, text='Theme Name:', app_theme=self.app_theme).grid(row=0, column=0, padx=10, pady=5)
        CustomEntry(editor_frame, textvariable=theme_name_var, app_theme=self.app_theme).grid(row=0, column=1, padx=10, pady=5)

        theme_entries = {}
        default_values = app_themes['Default Theme'] if theme_type == 'app' else game_themes['Default Theme']
        for i, (key, value) in enumerate(default_values.items(), start=1):
            CustomLabel(editor_frame, text=f'{key}:', app_theme=self.app_theme).grid(row=i, column=0, padx=10, pady=5)
            entry_var = tk.StringVar(value=value)
            entry = CustomEntry(editor_frame, textvariable=entry_var, app_theme=self.app_theme)
            entry.grid(row=i, column=1, padx=10, pady=5)
            theme_entries[key] = entry_var

            if 'color' in key:
                CustomButton(editor_frame, text='Choose Color', command=lambda ev=entry_var: self.open_color_chooser(ev, key), app_theme=self.app_theme).grid(row=i, column=2, padx=10, pady=5)

        def save_theme():
            new_theme = {key: var.get() for key, var in theme_entries.items()}
            save_new_theme(theme_name_var.get(), new_theme)
            editor_window.destroy()
            self.update_optionmenus()

        CustomButton(editor_frame, text='Save', command=save_theme, app_theme=self.app_theme).grid(row=i+1, column=0, columnspan=3, pady=10)

    def edit_theme(self, theme_type, themes, theme_var):
        dialog = CustomToplevel(self.master, app_theme=self.app_theme, title=f'Edit {theme_type.capitalize()} Themes')
        editor_frame = dialog.frame_content

        theme_name_var = tk.StringVar(value=theme_var.get())
        CustomLabel(editor_frame, text='Theme Name:', app_theme=self.app_theme).grid(row=0, column=0, padx=10, pady=5)
        CustomEntry(editor_frame, textvariable=theme_name_var, app_theme=self.app_theme).grid(row=0, column=1, padx=10, pady=5)

        theme_entries = {}
        for i, (key, value) in enumerate(themes[theme_var.get()].items(), start=1):
            CustomLabel(editor_frame, text=f'{key}:', app_theme=self.app_theme).grid(row=i, column=0, padx=10, pady=5)
            entry_var = tk.StringVar(value=value)
            entry = CustomEntry(editor_frame, textvariable=entry_var, app_theme=self.app_theme)
            entry.grid(row=i, column=1, padx=10, pady=5)
            theme_entries[key] = entry_var

            if 'color' in key:
                CustomButton(editor_frame, text='Choose Color', command=lambda ev=entry_var: self.open_color_chooser(ev, key), app_theme=self.app_theme).grid(row=i, column=2, padx=10, pady=5)

        def save_theme():
            new_theme = {key: var.get() for key, var in theme_entries.items()}
            themes[theme_name_var.get()] = new_theme
            self.save_themes(theme_type, themes)
            theme_var.set(theme_name_var.get())
            self.apply_theme()
            dialog.destroy()
            self.update_optionmenus()

        CustomButton(editor_frame, text='Save', command=save_theme, app_theme=self.app_theme).grid(row=i+1, column=0, pady=10)

    def delete_theme(self, theme_type, themes, theme_var):
        if theme_var.get() == 'Default Theme':
            CustomMessageBox(self.master, title='Info', message='The "Default Theme" cannot be deleted.', app_theme=self.app_theme)
            return

        def perform_delete():
            del themes[theme_var.get()]
            self.save_themes(theme_type, themes)
            theme_var.set('Default Theme')
            self.apply_theme()
            self.update_optionmenus()

        CustomMessageBox(self.master, title='Confirm Deletion', message=f'Are you sure you want to delete the {theme_var.get()} theme?', app_theme=self.app_theme, on_confirm=perform_delete)

    def apply_theme(self):
        self.master.config(background=self.app_theme['background_color'])

        for widget in self.master.winfo_children():
            self.apply_widget_theme(widget)

        self.update_optionmenus()

    def apply_widget_theme(self, widget):
        try:
            if isinstance(widget, (CustomFrame, CustomLabel, CustomButton, CustomEntry, CustomToplevel)):
                widget.config(background=self.app_theme['background_color'])
            if isinstance(widget, (CustomLabel, CustomButton, CustomEntry)):
                widget.config(foreground=self.app_theme['foreground_color'])
            if isinstance(widget, CustomEntry):
                widget.config(readonlybackground=self.app_theme['background_color'], disabledforeground=self.app_theme['foreground_color'])
            if isinstance(widget, CustomButton):
                widget.config(activebackground=self.app_theme['active_background'], activeforeground=self.app_theme['active_foreground'])
        except tk.TclError:
            pass
        for child in widget.winfo_children():
            self.apply_widget_theme(child)

    def update_optionmenus(self):
        for widget in self.master.winfo_children():
            if isinstance(widget, CustomOptionMenu):
                widget.configure()
            for child in widget.winfo_children():
                if isinstance(child, CustomOptionMenu):
                    child.configure()

    def save_themes(self, theme_type, themes):
        file_name = 'app_themes.json' if theme_type == 'app' else 'game_themes.json'
        with open(f'{FILE_PATH}/{file_name}', 'w') as file:
            json.dump(themes, file, indent=4)

    def get_font(self):
        if platform.system() == 'Linux':
            return self.app_theme['linux_font']
        elif platform.system() == 'Darwin':
            return self.app_theme['mac_font']
        else:
            return self.app_theme['windows_font']

    def open_color_chooser(self, entry_var, title):
        CustomColorChooser(self.master, app_theme=self.app_theme, on_color_chosen=lambda color: entry_var.set(color), title=title, initial_color=entry_var.get())

if __name__ == '__main__':
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
