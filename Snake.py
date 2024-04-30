import json
from tkinter.simpledialog import askstring
import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import ttk
import random
import time

class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.master.title('Snake')

        self.game_loop_id = None

        self.player_name = tk.StringVar(value='')
        
        self.toolbar = tk.Frame(self.master)
        self.toolbar.pack()
        self.start_button = tk.Button(self.toolbar, text='Start New Game', command=self.start_game)
        self.start_button.pack(side=tk.LEFT)
        
        self.speed_var = tk.StringVar(value='Medium')
        self.speed_options = {'Slow': 150, 'Medium': 100, 'Fast': 50}
        self.speed_menu = tk.OptionMenu(self.toolbar, self.speed_var, *self.speed_options.keys(), command=self.check_speed_change)
        self.speed_menu.pack(side=tk.LEFT)

        self.scores_button = tk.Button(self.toolbar, text='Top Scores', command=self.show_high_scores)
        self.scores_button.pack(side=tk.LEFT)

        self.exit_button = tk.Button(self.toolbar, text='Exit', command=self.master.quit)
        self.exit_button.pack(side=tk.LEFT)
        
        self.canvas = tk.Canvas(self.master, width=800, height=800, bg='black')
        self.canvas.pack()

        self.draw_title_screen()

        self.status_bar = tk.Frame(self.master)
        self.status_bar.pack(fill=tk.X)
        self.score_label = tk.Label(self.status_bar, text='Length: 1', anchor='w')
        self.score_label.pack(side=tk.LEFT)

        self.load_high_scores()
        
        self.timer_label = tk.Label(self.status_bar, text='Time: 0s', anchor='center')
        self.timer_label.pack(side=tk.LEFT, expand=True)
        
        self.difficulty_label = tk.Label(self.status_bar, text='Difficulty: Medium', anchor='e')
        self.difficulty_label.pack(side=tk.LEFT)
        
        self.snake = None
        self.food = None
        self.direction = 'Right'
        self.running = False
        self.paused = False
        self.start_time = None
        
        self.master.bind('<KeyPress>', self.change_direction)
        self.master.bind('<space>', self.toggle_pause)

    def start_game(self):
        if self.game_loop_id:
            self.master.after_cancel(self.game_loop_id)
        self.canvas.delete(self.title_text)
        self.canvas.delete(self.logo_text)
        self.snake = [(20, 20)]
        self.food = [self.create_food()]
        self.direction = 'Right'
        self.running = True
        self.paused = False
        self.start_time = time.time()
        self.canvas.delete('game_over')
        self.render_food()
        self.update_labels()
        self.master.config(cursor='none')
        self.game_loop()

    def create_food(self):
        canvas_width = self.canvas.cget('width')
        canvas_height = self.canvas.cget('height')
        max_x = int(canvas_width) // 20 - 1
        max_y = int(canvas_height) // 20 - 1
        while True:
            food = (random.randint(0, max_x) * 20, random.randint(0, max_y) * 20)
            if food not in self.snake:
                return food

    def render_snake(self):
        self.canvas.delete('snake')
        for x, y in self.snake:
            self.canvas.create_rectangle(x, y, x + 20, y + 20, fill='green', tags='snake')

    def render_food(self):
        self.canvas.delete('food')
        x, y = self.food[0]
        self.canvas.create_rectangle(x, y, x + 20, y + 20, fill='red', tags='food')

    def change_direction(self, event):
        if event.keysym == 'n':
            self.confirm_new_game()
            return
        if self.paused:
            return
        keys = {'s': 'Left', 'e': 'Up', 'f': 'Right', 'd': 'Down'}
        if event.keysym in keys:
            new_dir = keys[event.keysym]
        else:
            new_dir = event.keysym
        opposites = {'Left': 'Right', 'Right': 'Left', 'Up': 'Down', 'Down': 'Up'}
        if new_dir in opposites and self.direction != opposites[new_dir]:
            self.direction = new_dir

    def check_speed_change(self, value):
        if self.running:
            if messagebox.askyesno('New Game?', 'Changing the speed will start a new game. Continue?'):
                self.start_game()
            else:
                self.speed_var.set('Medium' if self.speed_var.get() != 'Medium' else self.speed_var.get())
        self.difficulty_label.config(text=f'Difficulty: {self.speed_var.get()}')

    def toggle_pause(self, event=None):
        if not self.running:
            return
        self.paused = not self.paused
        self.master.config(cursor='none' if self.paused else '')

    def game_loop(self):
        if self.running and not self.paused:
            self.move_snake()
            self.check_collision()
            self.update_timer()
            self.master.config(cursor='none')
        else:
            self.master.config(cursor='')
        if self.running:
            self.game_loop_id = self.master.after(self.speed_options[self.speed_var.get()], self.game_loop)
        else:
            self.show_game_over()
            self.master.config(cursor='')

    def move_snake(self):
        head_x, head_y = self.snake[0]
        move_offsets = {'Left': (-20, 0), 'Right': (20, 0), 'Up': (0, -20), 'Down': (0, 20)}
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
        canvas_width = int(self.canvas.cget('width'))
        canvas_height = int(self.canvas.cget('height'))
        if head_x < 0 or head_x >= canvas_width or head_y < 0 or head_y >= canvas_height or self.snake[0] in self.snake[1:]:
            self.running = False

        self.render_snake()

    def show_game_over(self):
        width = int(self.canvas.cget('width'))
        height = int(self.canvas.cget('height'))
        self.canvas.create_text(width // 2, height // 2, text='Game Over', fill='white', font=('Arial', 24), tags='game_over')
        self.check_high_score()

    def update_labels(self):
        self.score_label.config(text=f'Length: {len(self.snake)}')
        self.difficulty_label.config(text=f'Difficulty: {self.speed_var.get()}')

    def update_timer(self):
        if self.start_time:
            elapsed_time = int(time.time() - self.start_time)
            self.timer_label.config(text=f'Time: {elapsed_time}s')

    def confirm_new_game(self):
        if self.running and not messagebox.askyesno('New Game?', 'Are you sure you want to start a new game?'):
            return
        self.start_game()

    def load_high_scores(self):
        try:
            with open('top_scores.json', 'r') as file:
                self.high_scores = json.load(file)
        except FileNotFoundError:
            self.high_scores = {'Slow': [], 'Medium': [], 'Fast': []}

    def save_high_scores(self):
        with open('top_scores.json', 'w') as file:
            json.dump(self.high_scores, file, indent=4)

    def check_high_score(self):
        current_score = len(self.snake)
        current_time = int(time.time() - self.start_time)
        difficulty = self.speed_var.get()
        scores = self.high_scores[difficulty]
        if len(scores) < 10 or any(current_score > score[1] for score in scores):
            self.get_user_name()
            if self.player_name.get():
                scores.append([self.player_name.get(), current_score, current_time, time.ctime()])
                scores.sort(key=lambda x: x[1], reverse=True)
                self.high_scores[difficulty] = scores[:10]
                self.save_high_scores()

    def show_high_scores(self):
        scores_window = tk.Toplevel(self.master)
        scores_window.title('Top Scores')

        notebook = ttk.Notebook(scores_window)
        notebook.pack(fill='both', expand=True)

        for difficulty in ['Slow', 'Medium', 'Fast']:
            frame = ttk.Frame(notebook)
            notebook.add(frame, text=difficulty)

            tree = ttk.Treeview(frame, columns=('Name', 'Score', 'Time', 'Date'), show='headings', selectmode='extended')
            tree.pack(fill='both', expand=True)

            tree.heading('Name', text='Name')
            tree.heading('Score', text='Score')
            tree.heading('Time', text='Duration (s)')
            tree.heading('Date', text='Date')

            tree.column('Name', width=100, anchor='w')
            tree.column('Score', width=50, anchor='center')
            tree.column('Time', width=100, anchor='center')
            tree.column('Date', width=150, anchor='center')

            if self.high_scores[difficulty]:
                for score in self.high_scores[difficulty]:
                    tree.insert('', 'end', values=score)

            self.create_context_menu(tree, difficulty)

        difficulty_to_index = {'Slow': 0, 'Medium': 1, 'Fast': 2}
        current_difficulty_index = difficulty_to_index[self.speed_var.get()]
        notebook.select(current_difficulty_index)

    def create_context_menu(self, tree, difficulty):
        menu = tk.Menu(tree, tearoff=0)
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

        if messagebox.askyesno('Confirm Deletion', 'Are you sure you want to delete this score?'):
            for item in selected_items:
                tree.delete(item)

            self.high_scores[difficulty] = [
                [tree.item(child)['values'][0], tree.item(child)['values'][1], tree.item(child)['values'][2], tree.item(child)['values'][3]]
                for child in tree.get_children()
            ]
            self.save_high_scores()


    def draw_title_screen(self):
        self.title_text = self.canvas.create_text(400, 350, text='Snake', fill='red', font=('Arial', 44, 'bold'))
        self.logo_text = self.canvas.create_text(400, 400, text='How big can your snake get?', fill='white', font=('Arial', 24))

    def confirm_new_game(self):
        if self.running and not messagebox.askyesno('New Game?', 'Are you sure you want to start a new game?'):
            return
        self.start_game()

    def get_user_name(self):
        self.master.config(cursor='')

        dialog = tk.Toplevel(self.master)
        dialog.title('New High Score!')
        tk.Label(dialog, text='Enter your name:').pack(padx=10, pady=10)

        name_entry = tk.Entry(dialog, textvariable=self.player_name)
        name_entry.pack(padx=10, pady=10)
        name_entry.focus_set()
        name_entry.select_range(0, tk.END)

        submit_button = tk.Button(dialog, text='OK', command=lambda: dialog.destroy())
        submit_button.pack(side=tk.LEFT, padx=10, pady=10)

        cancel_button = tk.Button(dialog, text='Cancel', command=lambda: [self.player_name.set(''), dialog.destroy()])
        cancel_button.pack(side=tk.RIGHT, padx=10, pady=10)

        self.master.wait_window(dialog)

        if not self.paused and self.running:
            self.master.config(cursor='none')
        else:
            self.master.config(cursor='')


if __name__ == '__main__':
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
