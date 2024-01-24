import tkinter as tk
from tkinter import ttk, messagebox
import json
import threading
import time
import pygetwindow as gw
from walker.get_destination_coordinates import search_place_coordinates
from walker.walker import walk_to_destination

KNOWN_PLACES_JSON_FILE = "./walker/walker/known_places.json"
WINDOW_TITLE_TO_CHECK = "RuneLite - Dukadelmin"

class ClosableNotebook(ttk.Notebook):
    def __init__(self, *args, **kwargs):
        ttk.Notebook.__init__(self, *args, **kwargs)
        self.master = args[0]
        self._active = None
        self.bind("<ButtonPress-1>", self.on_tab_click, True)

    def on_tab_click(self, event):
        index = self.index("@%d,%d" % (event.x, event.y))
        if index != -1:
            self._active = index

    def index_of_close_button(self, event):
        element = self.identify(event.x, event.y)
        index = self.index("@%d,%d" % (event.x, event.y))
        return index if "close" in element else None

    def on_close_click(self, event):
        index = self.index_of_close_button(event)
        if index is not None:
            self.forget(index)
            if index == self._active:
                self._active = None
            event.widget.event_generate("<<NotebookTabClosed>>")

class AutocompleteEntry(tk.Entry):
    def __init__(self, *args, **kwargs):
        tk.Entry.__init__(self, *args, **kwargs)
        self._completion_listbox = None
        self._hits = []
        self.bind('<KeyRelease>', self.handle_keyrelease)
        self.bind('<FocusIn>', self.handle_focus_in)
        self.focus()

    def autocomplete(self):
        current_text = self.get().lower()
        if not current_text:
            _hits = self._completion_list
        else:
            _hits = [item for item in self._completion_list if item.lower().startswith(current_text)]

        if _hits != self._hits:
            self._hits = _hits
            self.update_completion_listbox(_hits)

    # def update_completion_listbox(self, hits):
    #     if self._completion_listbox:
    #         self._completion_listbox.destroy()

    #     if hits:
    #         self._completion_listbox = tk.Listbox(self.master)
    #         self._completion_listbox.place(x=self.winfo_x(), y=self.winfo_y() + self.winfo_height())
    #         self._completion_listbox.bind('<Button-1>', self.on_listbox_click)

    #         for item in hits:
    #             self._completion_listbox.insert(tk.END, item)

    def handle_keyrelease(self, event):
        if event.keysym == 'Return':
            self._hits = []
            self.destroy_completion_listbox()
            return

        self.autocomplete()

    def handle_focus_in(self, event):
        self.autocomplete()

    def destroy_completion_listbox(self):
        if self._completion_listbox:
            self._completion_listbox.destroy()

    # def on_listbox_click(self, event):
    #     selected_index = self._completion_listbox.curselection()
    #     if selected_index:
    #         selected_item = self._hits[selected_index[0]]
    #         self.delete(0, tk.END)
    #         self.insert(0, selected_item)
    #         self.destroy_completion_listbox()
    #         print(f"selected location = {selected_item}")
    #         if self._location_var:
    #             self._location_var.set(selected_item)
    #             print(f"selected location = {selected_item}")

    def __init__(self, *args, **kwargs):
        tk.Entry.__init__(self, *args, **kwargs)
        self._completion_listbox = None
        self._hits = []
        self._hit_index = 0
        # self._location_var = None
        self.bind('<KeyRelease>', self.handle_keyrelease)
        self.bind('<FocusIn>', self.handle_focus_in)
        self.focus()


    def autocomplete(self):
        current_text = self.get().lower()
        if not current_text:
            _hits = [item for item in self._completion_list]
        else:
            _hits = [item for item in self._completion_list if item.lower().startswith(current_text)]

        if _hits != self._hits:
            self._hit_index = 0
            self._hits = _hits
            if self._completion_listbox:
                self._completion_listbox.destroy()
                self._completion_listbox = None
            if _hits:
                self._completion_listbox = tk.Listbox(self.master)
                self._completion_listbox.place(x=self.winfo_x(), y=self.winfo_y() + self.winfo_height())
                self._completion_listbox.bind('<Button-1>', self.on_listbox_click)
                for item in _hits:
                    self._completion_listbox.insert(tk.END, item)
            elif not current_text:
                self._completion_listbox.destroy()
                self._completion_listbox = None

    def handle_keyrelease(self, event):
        if event.keysym == 'Return':
            self._hits = []
            if self._completion_listbox:
                self._completion_listbox.destroy()
                self._completion_listbox = None
            return

        self.autocomplete()

    def on_listbox_click(self, event):
        selected_index = self._completion_listbox.curselection()
        if selected_index:
            selected_item = self._hits[selected_index[0]]
            self.delete(0, tk.END)
            self.insert(0, selected_item)

            # Update the location_var
            if self._location_var:
                self._location_var.set(selected_item)

                # Trigger the update_location_var method
                self.master.master.master.update_location_var(selected_item)

        # Destroy the completion listbox
        self.destroy_completion_listbox()
        # Set focus back to the entry widget
        self.focus_set()




    def handle_focus_in(self, event):
        self.autocomplete()

    def __init__(self, *args, **kwargs):
        tk.Entry.__init__(self, *args, **kwargs)
        self._completion_listbox = None
        self._hits = []
        self._location_var = None
        self.bind('<KeyRelease>', self.handle_keyrelease)
        self.bind('<FocusIn>', self.handle_focus_in)
        self.focus()

    def set_completion_list(self, completion_list, location_var):
        self._completion_list = sorted(completion_list)
        self._hits = []
        self._location_var = location_var

    def autocomplete(self):
        current_text = self.get().lower()
        if not current_text:
            _hits = [item for item in self._completion_list]
        else:
            _hits = [item for item in self._completion_list if item.lower().startswith(current_text)]

        if _hits != self._hits:
            self._hits = _hits
            if self._completion_listbox:
                self._completion_listbox.destroy()
                self._completion_listbox = None
            if _hits:
                self._completion_listbox = tk.Listbox(self.master)
                self._completion_listbox.place(x=self.winfo_x(), y=self.winfo_y() + self.winfo_height())
                self._completion_listbox.bind('<Button-1>', self.on_listbox_click)
                for item in _hits:
                    self._completion_listbox.insert(tk.END, item)
            elif not current_text:
                self._completion_listbox.destroy()
                self._completion_listbox = None

    def handle_keyrelease(self, event):
        if event.keysym == 'Return':
            self._hits = []
            if self._completion_listbox:
                self._completion_listbox.destroy()
                self._completion_listbox = None
            return

        self.autocomplete()

    def on_listbox_click(self, event):
        selected_index = self._completion_listbox.curselection()
        if selected_index:
            selected_item = self._hits[selected_index[0]]
            self.delete(0, tk.END)
            self.insert(0, selected_item)
            self._completion_listbox.destroy()
            self._completion_listbox = None

            # Update the location_var
            if self._location_var:
                self._location_var.set(selected_item)

    def handle_focus_in(self, event):
        self.autocomplete()

    def __init__(self, *args, **kwargs):
        tk.Entry.__init__(self, *args, **kwargs)
        self._completion_listbox = None
        self._hits = []
        self._location_var = None
        self.bind('<KeyRelease>', self.handle_keyrelease)
        self.bind('<FocusIn>', self.handle_focus_in)
        self.focus()

    def set_completion_list(self, completion_list, location_var):
        self._completion_list = sorted(completion_list)
        self._hits = []
        self._location_var = location_var

    def autocomplete(self):
        current_text = self.get().lower()
        if not current_text:
            _hits = self._completion_list
        else:
            _hits = [item for item in self._completion_list if item.lower().startswith(current_text)]

        if _hits != self._hits:
            self._hits = _hits
            self.update_completion_listbox(_hits)
            # self._location_var = _hits[0]
            # print(_hits)
            # print(.location_var)

    def update_completion_listbox(self, hits):
        if self._completion_listbox:
            self._completion_listbox.destroy()

        if hits:
            self._completion_listbox = tk.Listbox(self.master)
            self._completion_listbox.place(x=self.winfo_x(), y=self.winfo_y() + self.winfo_height())
            self._completion_listbox.bind('<Button-1>', self.on_listbox_click)

            for item in hits:
                self._completion_listbox.insert(tk.END, item)

    def handle_keyrelease(self, event):
        if event.keysym == 'Return':
            self._hits = []
            self.destroy_completion_listbox()
            return

        self.autocomplete()

    def handle_focus_in(self, event):
        self.autocomplete()

    def destroy_completion_listbox(self):
        if self._completion_listbox:
            self._completion_listbox.destroy()

    def on_listbox_click(self, event):
        print("clicked")
        selected_index = self._completion_listbox.curselection()
        if selected_index:
            print(self._hits[0])
            selected_item = self._hits[selected_index[0]]
            self.delete(0, tk.END)
            self.insert(0, selected_item)
            self.destroy_completion_listbox()
            self._location_var.set(selected_item)
            print(self._location_var.get())
            # if self._location_var:
                # self._location_var.set(selected_item)

class DestinationWalkerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Destination Walker")
        self.stop_flag = False

        # Load known locations from the JSON file
        self.locations = self.load_destination_names()

        # Create GUI elements
        self.create_menu()
        self.create_notebook()
        self.create_main_menu()
        
        # Add the following line to initialize location_var
        self.location_var = tk.StringVar(value=self.locations[0])

    def load_destination_names(self):
        known_location_names = []
        try:
            with open(KNOWN_PLACES_JSON_FILE, "r") as known_places_file:
                known_places = json.loads(known_places_file.read())
                known_location_names = [location.get("name").lower() for location in known_places.get("locations", [])]
        except FileNotFoundError:
            print(f"Error: {KNOWN_PLACES_JSON_FILE} not found.")
        return known_location_names

    def check_and_activate_window(self, window_title):
        try:
            window = gw.getWindowsWithTitle(window_title)[0]
            if window.isActive:
                print(f"Window '{window_title}' is already active.")
            else:
                window.maximize()
                window.activate()
            return True
        except (IndexError, gw.WindowNotFoundError):
            print(f"Window '{window_title}' is not open.")
            return False

    def on_close(self, event):
        # Get the current tab ID
        current_tab_id = self.notebook.index(self.notebook.select())
        if current_tab_id != 0:
            # If not in the main menu, close the current tab
            self.notebook.forget(current_tab_id)

    def walk_to_destination(self):
        selected_location = self.location_var.get()
        if selected_location not in self.locations:
            messagebox.showerror("Error", "Please choose a valid location from the dropdown.")
            return

        self.stop_flag = False
        print(self.location_var.get())
        destination_coordinates = search_place_coordinates(selected_location)
        destination_x, destination_y, destination_z = destination_coordinates
        print(destination_coordinates)

        if not self.check_and_activate_window(WINDOW_TITLE_TO_CHECK):
            print(f"Opening or starting the window '{WINDOW_TITLE_TO_CHECK}'...")
            # Your code to open or start the window goes here
            time.sleep(2)  # Simulating some time for the window to open
            self.check_and_activate_window(WINDOW_TITLE_TO_CHECK)

        def walking_thread():
            walk_to_destination(destination_x, destination_y, destination_z)

        # Start a new thread for walking
        walking_thread = threading.Thread(target=walking_thread)
        walking_thread.start()

    def pickup_cowhide_script(self):
        # Replace the command below with the actual command to run your script
        script_command = "python ./pickup_cowhide_script_and_bank_them.py"
        # Execute the script command as needed

    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        # Create a menu for different scripts
        script_menu = tk.Menu(menu_bar, tearoff=0)
        # menu_bar.add_cascade(label="Main Menu", command=lambda: self.notebook.select(0))
        # menu_bar.add_cascade(label="All Scripts", menu=script_menu)

        # Walker Script
        script_menu.add_command(label="Walker Script", command=self.start_walker_script)
        # Pickup Cowhide Script
        script_menu.add_command(label="Pickup Cowhide Script", command=self.start_pickup_cowhide_script)

    def create_notebook(self):
        self.notebook = ClosableNotebook(self.root)
        self.notebook.pack(expand=1, fill="both")

        # Bind the close event to the notebook
        self.notebook.bind("<ButtonRelease-1>", self.on_close)

    def create_main_menu(self):
        main_menu_frame = ttk.Frame(self.notebook)
        self.notebook.add(main_menu_frame, text="Main Menu")    

        # Walk to Destination button
        option_1 = tk.Button(main_menu_frame, text="Walk to Destination", command=self.start_walker_script)
        option_1.pack(pady=10)  

        # Pickup Cowhide Script button
        option_2 = tk.Button(main_menu_frame, text="Pick up Cowhide Script", command=self.start_pickup_cowhide_script)
        option_2.pack(pady=10)

    def start_walker_script(self):
        walker_frame = ttk.Frame(self.notebook)
        self.notebook.add(walker_frame, text="Walk to Destination")
        self.notebook.select(walker_frame)

        # AutocompleteEntry with available locations
        location_var_walker = tk.StringVar(value=self.locations[0])
        location_entry_walker = AutocompleteEntry(walker_frame)
        location_entry_walker.set_completion_list(self.locations, location_var_walker)
        location_label_walker = tk.Label(walker_frame, text="Choose a destination:")
        location_label_walker.pack(pady=10)
        location_entry_walker.pack(pady=10)

        walk_button = tk.Button(walker_frame, text="Start Walking", command=self.walk_to_destination)
        walk_button.pack(pady=10)


    def start_pickup_cowhide_script(self):
        cowhide_frame = ttk.Frame(self.notebook)
        self.notebook.add(cowhide_frame, text="Pickup Cowhide Script")
        self.notebook.select(cowhide_frame)
    
        # Replace the following line with the actual script command
        script_command_cowhide = "python ./pickup_cowhide_script_and_bank_them.py"
        run_script_button_cowhide = tk.Button(cowhide_frame, text="Run Pickup Cowhide Script", command=lambda: self.run_script(script_command_cowhide))
        run_script_button_cowhide.pack(pady=10)

    def run_script(self, script_command):
        # Placeholder for running the script
        print(f"Running script: {script_command}")

    # def update_location_var(self, selected_item):
    #     # Update the location_var when an item is selected
    #     self.location_var.set(selected_item)

if __name__ == "__main__":
    root = tk.Tk()
    app = DestinationWalkerApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.geometry("400x300")  # Set a reasonable window size
    root.resizable(False, False)  # Disable resizing
    root.mainloop()
