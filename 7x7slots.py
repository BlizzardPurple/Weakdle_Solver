import csv
import tkinter as tk
from tkinter import messagebox

attacking_types = ['NORMAL'] * 5
defending_types = [['NULL', 'NULL'] for _ in range(6)]
pokemon_types = ["NULL", "NORMAL", "FIRE", "WATER", "ELECTRIC", "GRASS", "ICE", "FIGHTING", "POISON", "GROUND", "FLYING", "PSYCHIC", "BUG", "ROCK", "GHOST", "DRAGON", "DARK", "STEEL", "FAIRY"]
type_to_index_map = {type: index for index, type in enumerate(pokemon_types)}
widgets = [[None for _ in range(8)] for _ in range(7)]
effectivity = [
    (1,1,1,1,1,1,1,1,1,1,1,1,0.5,0,1,1,0.5,1),              #NORMAL
    (1,0.5,0.5,1,2,2,1,1,1,1,1,2,0.5,1,0.5,1,2,1),          #FIRE
    (1,2,0.5,1,0.5,1,1,1,2,1,1,1,2,1,0.5,1,1,1),            #water
    (1,1,2,0.5,0.5,1,1,1,0,2,1,1,1,1,0.5,1,1,1),            #EL3CTRUC
    (1,0.5,2,1,0.5,1,1,0.5,2,0.5,1,0.5,2,1,0.5,1,0.5,1),    #GRASS
    (1,0.5,0.5,1,2,0.5,1,1,2,2,1,1,1,1,2,1,0.5,1),          #ICE
    (2,1,1,1,1,2,1,0.5,1,0.5,0.5,0.5,2,0,1,2,2,0.5),        #FIGHT
    (1,1,1,1,2,1,1,0.5,0.5,1,1,1,0.5,0.5,1,1,0,2),          #POI
    (1,2,1,2,0.5,1,1,2,1,0,1,0.5,2,1,1,1,2,1),              #GRO

    (1,1,1,0.5,2,1,2,1,1,1,1,2,0.5,1,1,1,0.5,1),            #FLY
    (1,1,1,1,1,1,2,2,1,1,0.5,1,1,1,1,0,0.5,1),              #PSY
    (1,0.5,1,1,2,1,0.5,0.5,1,0.5,2,1,1,0.5,1,2,0.5,0.5),    #bug
    (1,2,1,1,1,2,0.5,1,0.5,2,1,2,1,1,1,1,0.5,1),            #ROC
    (0,1,1,1,1,1,1,1,1,1,2,1,1,2,1,0.5,1,1),                #GHO
    (1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,0.5,0),                #DRA
    (1,1,1,1,1,1,0.5,1,1,1,2,1,1,2,1,0.5,1,0.5),            #DARK
    (1,0.5,0.5,0.5,1,2,1,1,1,1,1,1,2,1,1,1,0.5,2),          #STE
    (1,0.5,1,1,1,1,2,0.5,1,1,1,1,1,1,2,2,0.5,1),            #faI
]
result = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
]


def create_slot(row, col, initial_text=None):
    text_var = tk.StringVar(value=initial_text) if initial_text else None
    widget = tk.Button(root, textvariable=text_var,bg="white", width=30, justify='center', font=('Arial', 12))
    
    def update_text(given_text):
        widget.config(text=given_text)
    widget.update_text = update_text
    

    def on_click(event):
        if row > 0:
            if widget["bg"] == "white":
                widget["bg"] = "yellow"
            elif widget["bg"] == "yellow":
                widget["bg"] = "green"
            else:
                widget["bg"] = "white"
    widget.bind("<Button-1>", on_click)  # Bind left mouse button click

    return widget

def update_widgets():
    global result, widgets
    for row in range(1, 8):
        for col in range(3, 8): 
            widget = widgets[row-1][col] 
            widget.update_text(result[row-2][col-3])

def create_option_menu(row, col, initial_value, vector_index):
    selected_type = tk.StringVar(root)
    selected_type.set(initial_value)
    dropdown_menu = tk.OptionMenu(root, selected_type, *pokemon_types)
    dropdown_menu.grid(row=row, column=col, columnspan=1, sticky='nsew')
    
    # Bind the function to handle selection changes
    selected_type.trace("w", lambda *args: on_selection_change(selected_type, row, col, vector_index))

def on_selection_change(var, row, col, vector_index):
    global attacking_types, defending_types, effectivity, result
    selected_value = var.get()
    if row == 1 and 3 <= col <= 7:
        # Attacking type changed
        attacking_types[col-3] = selected_value
        if(selected_value != "NULL"):
            for i, defending_type in enumerate(defending_types, start=0):
                atk_ind = type_to_index_map[selected_value]-1
                eff = 1
                if (defending_type[0] != "NULL"):
                    eff = eff * effectivity[atk_ind][type_to_index_map[defending_type[0]]-1]
                if (defending_type[1] != "NULL"):
                    eff = eff * effectivity[atk_ind][type_to_index_map[defending_type[1]]-1]
                result[i][col-3]=eff
    elif row >= 1 and row <= 7 and (col == 1 or col == 2):
        # Defending type changed
        if col == 1:
            defending_types[row-2][0] = selected_value
        elif col == 2:
            defending_types[row-2][1] = selected_value
        if(selected_value!="NULL" and defending_types[row-2][0] != defending_types[row-2][1]):
            for i, attacking_type in enumerate(attacking_types, start=0):
                if attacking_type == "NULL":
                    continue
                eff = 1;
                def_1 = type_to_index_map[defending_types[row-2][0]]-1
                def_2 = type_to_index_map[defending_types[row-2][1]]-1
                if (defending_types[row-2][0] != "NULL"):
                    eff = eff * effectivity[type_to_index_map[attacking_type]-1][def_1]
                if (defending_types[row-2][1] != "NULL"):
                    eff = eff * effectivity[type_to_index_map[attacking_type]-1][def_2]
                result[row-2][i]=eff

    update_widgets()
    print(f"Updated vector: {vector_index} with value: {selected_value}")

message = ""

def check_attacking_types():
    global attacking_types, defending_types, message, result  # Include message in the global declaration

    # Check if any two elements in attacking_types are the same
    if len(set(attacking_types))!= len(attacking_types):
        message += "All attacking types should be different\n"

    # Check if any attacking type is "NULL"
    if "NULL" in attacking_types:
        message += "Attacking types cannot be NULL\n"

    # Print the current state of attacking_types and defending_types
    print("Current Attacking Types:", attacking_types)
    for i, row in enumerate(result, start=1):  # Start enumeration from 1 for row numbers
        print(f"Row {i}: {row[0]} / {row[1]} / {row[2]} / {row[3]} / {row[4]}")  # Print both defending types for the row
    print("\n")
    for i, row in enumerate(defending_types, start=1):  # Start enumeration from 1 for row numbers
        print(f"Row {i}: {row[0]} / {row[1]}")  # Print both defending types for the row

    # Display the final message
    if message:
        messagebox.showinfo("Warning", message.strip())
    else:
        messagebox.showinfo("Success", "All attacking types are different.")

    message = ""

root = tk.Tk()
root.title("Weakdle Solver by BlizzarpPurple")
root.geometry("900x400")

for col in range(0, 11):
    root.columnconfigure(col, weight=1)
for row in range(0, 9):
    root.rowconfigure(row, weight=1)

for row in range(7):
    for col in range(8):
        if (row == 0 and col == 0):
            initial_text = "TYPE MATCH"
        elif (row == 0 and col == 1):
            initial_text = "TYPE1"
        elif (row == 0 and col == 2):
            initial_text = "TYPE2"
        else:
            initial_text = None
        widgets[row][col] = create_slot(row, col, initial_text)
        widgets[row][col].grid(row=row+1, column=col, padx=1, pady=1, sticky='nsew')  # Adjust row index for the matrix

# Create the "attacking" and "defending" label in the new row, centered in column 5 and aligned to the right
attacking_label = tk.Label(root, text="ATTACKING", fg="black", font=("Arial", 12))
attacking_label.grid(row=0, column=5, sticky='ew', padx=(0, 10), pady=10)

defending_label = tk.Label(root, text="DEFENDING", fg="black", font=("Arial", 12))
defending_label.grid(row=0, column=1, sticky='ew', padx=(0, 10), pady=10)

# Submit or suggest button
submit_button = tk.Button(root, text="SUGGEST", bg="green", fg="white", font=("Arial", 12), command=check_attacking_types)
submit_button.grid(row=8, column=4, sticky='ew', padx=(0, 10), pady=10)

# Setup the dropdown menu for suggestions in columns 2 to 6 (attacking types)
for col in range(3, 8):
    create_option_menu(1, col, pokemon_types[1], 0)

# Create OptionMenus for columns 1 and 2 in rows 2 to 7 (defending types)
for row in range(2, 8):
    for col in range(1, 3):
        create_option_menu(row, col, pokemon_types[0], row-1)

root.mainloop()
