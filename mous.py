import tkinter as tk
from tkinter import messagebox

class DropdownMenuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Горизонтальное выпадающее меню")

        self.menu_items = ["Файл", "Правка", "Просмотр", "Справка", "Выход"]
        self.submenu_items = {
            "Файл": ["Новый", "Открыть", "Сохранить"],
            "Правка": ["Копировать", "Вставить"],
            "Просмотр": ["Увеличить", "Уменьшить"],
            "Справка": ["О программе"]
        }

        self.current_menu_index = 0
        self.current_submenu_index = -1

        self.create_menu()

        # Обработка событий клавиатуры
        self.root.bind("<Key>", self.handle_keypress)

    def create_menu(self):
        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.pack(side=tk.TOP, fill=tk.X)

        self.buttons = []

        for index, item in enumerate(self.menu_items):
            button = tk.Button(self.menu_frame, text=item, command=lambda i=index: self.toggle_submenu(i))
            button.pack(side=tk.LEFT)
            button.bind("<Enter>", lambda e, i=index: self.highlight_button(i))
            button.bind("<Leave>", lambda e, i=index: self.unhighlight_button(i))
            self.buttons.append(button)

    def toggle_submenu(self, index):
        if index == len(self.menu_items) - 1:  # Выход
            self.root.quit()
            return

        if index == self.current_menu_index:
            if self.current_submenu_index == -1:
                # Развернуть подменю
                self.show_submenu(index)
            else:
                # Свернуть подменю
                self.hide_submenu()
                self.current_submenu_index = -1
        else:
            # Свернуть текущее подменю и развернуть новое
            if self.current_submenu_index != -1:
                self.hide_submenu()

            self.current_menu_index = index
            self.show_submenu(index)

    def show_submenu(self, index):
        submenu_frame = tk.Frame(self.root)

        for sub_item in self.submenu_items[self.menu_items[index]]:
            sub_button = tk.Button(submenu_frame, text=sub_item, command=lambda item=sub_item: self.execute_command(item))
            sub_button.pack(side=tk.TOP)

        submenu_frame.pack(side=tk.TOP)
        submenu_frame.bind("<Leave>", lambda e: submenu_frame.destroy())

        # Сохраняем ссылку на текущее подменю
        self.current_submenu_index = index

    def hide_submenu(self):
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame) and widget.winfo_y() > 30:  # Условие для определения подменю
                widget.destroy()

    def execute_command(self, command):
        messagebox.showinfo("Команда выполнена", f"Вы выбрали: {command}")

    def handle_keypress(self, event):
        if event.keysym == 'Right':
            # Перемещение вправо по меню
            if (self.current_menu_index + 1) < len(self.menu_items):
                self.current_menu_index += 1
                self.update_highlight()

        elif event.keysym == 'Left':
            # Перемещение влево по меню
            if (self.current_menu_index - 1) >= 0:
                self.current_menu_index -= 1
                self.update_highlight()

        elif event.keysym == 'Return':
            # Нажатие Enter для открытия/закрытия подменю
            self.toggle_submenu(self.current_menu_index)

    def update_highlight(self):
        for i, button in enumerate(self.buttons):
            button.config(relief=tk.RAISED)

        # Подсветка текущей кнопки меню
        current_button = self.buttons[self.current_menu_index]
        current_button.config(relief=tk.SUNKEN)

    def highlight_button(self, index):
        for i, button in enumerate(self.buttons):
            button.config(relief=tk.RAISED)

        button_to_highlight = self.buttons[index]
        button_to_highlight.config(relief=tk.SUNKEN)

    def unhighlight_button(self, index):
        button_to_unhighlight = self.buttons[index]
        button_to_unhighlight.config(relief=tk.RAISED)

if __name__ == "__main__":
    root = tk.Tk()
    app = DropdownMenuApp(root)
    root.mainloop()