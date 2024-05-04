import csv
import tkinter as tk
from tkinter import messagebox

# Initialize vectors
attacking_types = ['NORMAL'] * 5
defending_types = [['NULL', 'NULL'] for _ in range(6)]
pokemon_types = ["NULL", "NORMAL", "FIRE", "WATER", "ELECTRIC", "GRASS", "ICE", "FIGHTING", "POISON", "GROUND", "FLYING", "PSYCHIC", "BUG", "ROCK", "GHOST", "DRAGON", "DARK", "STEEL", "FAIRY"]
type_to_index_map = {type: index for index, type in enumerate(pokemon_types)}
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
# Convert result from a list of tuples to a list of lists
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
    if col < 3 and row > 0 and col!= 0:
        entry_widget = tk.Entry(root, textvariable=text_var, state='normal', width=30, justify='center', font=('Arial', 12))
        return entry_widget
    elif col == 2 and row == 4:
        entry_widget = tk.Button(root, textvariable=text_var, state='disabled',bg="white", width=30, justify='center', font=('Arial', 12))
        return entry_widget
    else:
        entry_widget = tk.Button(root, textvariable=text_var,bg="white", width=30, justify='center', font=('Arial', 12))
        
        # Bind click event to change color
        def on_click(event):
            # print("Widget clicked")
            if row > 0:  # Only apply to cells with row > 2
                if entry_widget["bg"] == "white":
                    entry_widget["bg"] = "yellow"
                    entry_widget["textvariable"] = "OH"
                elif entry_widget["bg"] == "yellow":
                    entry_widget["bg"] = "green"
                else:
                    entry_widget["bg"] = "white"
        
        entry_widget.bind("<Button-1>", on_click)  # Bind left mouse button click
        return entry_widget

def read_effectiveness_data():
    effectiveness_data = {}
    with open('pokemon.csv', mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            # Assuming the first column is 'Type' and the rest are effectiveness values
            effectiveness_values = [float(row[col]) for col in csv_reader.fieldnames[1:]]
            effectiveness_data[row['Type']] = effectiveness_values
    return effectiveness_data

effectiveness_data = read_effectiveness_data()

def create_option_menu(row, col, initial_value, vector_index):
    selected_type = tk.StringVar(root)
    selected_type.set(initial_value)
    dropdown_menu = tk.OptionMenu(root, selected_type, *pokemon_types)
    dropdown_menu.grid(row=row, column=col, columnspan=1, sticky='nsew')
    
    # Bind the function to handle selection changes
    selected_type.trace("w", lambda *args: on_selection_change(selected_type, row, col, vector_index))

def on_selection_change(var, row, col, vector_index):
    global attacking_types, defending_types, effectivity
    selected_value = var.get()
    if row == 1 and 3 <= col <= 7:
        # Attacking type changed
        attacking_types[col-3] = selected_value
        # Correctly calculate indices for accessing result
        if(selected_value != "NULL"):
            for i, row_defending in enumerate(defending_types, start=0):
                atk_ind = type_to_index_map[selected_value]
                eff = 1
                if (defending_types[i][0] != "NULL"):
                    eff = eff * effectivity[atk_ind][type_to_index_map[defending_types[i][0]]-1]
                if (defending_types[i][1] != "NULL"):
                    eff = eff * effectivity[atk_ind][type_to_index_map[defending_types[i][1]]-1]
                result[i][col-3]=eff

            
            # Ensure indices are integers and correctly reference the result list
            # attacking_type_index = type_to_index_map[attacking_types[col-3]]
            # defending_type1_index = type_to_index_map[defending_types[i-1][0]]
            # defending_type2_index = type_to_index_map[defending_types[i-1][1]]
            # # Access the correct tuple and element in the result list
            # result[i-1][col-3] = effectivity[attacking_type_index][defending_type1_index] * effectivity[attacking_type_index][defending_type2_index]
    elif row >= 1 and row <= 7 and (col == 1 or col == 2):
        # Defending type changed
        if col == 1:
            defending_types[row-2][0] = selected_value
        elif col == 2:
            defending_types[row-2][1] = selected_value
        # Additional logic for updating defending types goes here
    print(f"Updated vector: {vector_index} with value: {selected_value}")


message = ""

def check_attacking_types():
    global attacking_types, defending_types, message  # Include message in the global declaration

    # Check if any two elements in attacking_types are the same
    if len(set(attacking_types))!= len(attacking_types):
        message += "All attacking types should be different\n"

    # Check if any attacking type is "NULL"
    if "NULL" in attacking_types:
        message += "Attacking types cannot be NULL\n"

    # Print the current state of attacking_types and defending_types
    print("Current Attacking Types:", attacking_types)
    print("Resulting effectivity:\n", result)
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

# Adjust the loop to include an additional column
for col in range(0, 11):  # Now includes 8 columns
    root.columnconfigure(col, weight=1)
for row in range(0, 9):
    root.rowconfigure(row, weight=1)

for row in range(7):
    for col in range(8):  # Adjusted to 8 columns
        if (row == 0 and col == 0):
            initial_text = "TYPE MATCH"
        elif (row == 0 and col == 1):
            initial_text = "TYPE1"
        elif (row == 0 and col == 2):  # Special handling for row 1, columns 1 and 2
            initial_text = "TYPE2"  # No initial text for combined cells
        else:
            initial_text = None
        
        create_slot(row, col, initial_text).grid(row=row+1, column=col, padx=1, pady=1, sticky='nsew')  # Adjust row index for the matrix

# Create the "defending" label in the new row, centered in column 5 and aligned to the right
attacking_label = tk.Label(root, text="ATTACKING", fg="black", font=("Arial", 12))  # Reduced font size
attacking_label.grid(row=0, column=5, sticky='ew', padx=(0, 10), pady=10)  # Adjusted padding as needed

defending_label = tk.Label(root, text="DEFENDING", fg="black", font=("Arial", 12))  # Reduced font size
defending_label.grid(row=0, column=1, sticky='ew', padx=(0, 10), pady=10)  # Adjusted padding as needed

# Submit button
submit_button = tk.Button(root, text="SUGGEST", bg="green", fg="white", font=("Arial", 12), command=check_attacking_types)
submit_button.grid(row=8, column=4, sticky='ew', padx=(0, 10), pady=10)  # Place the submit button in the first row and last column

# Setup the dropdown menu for suggestions in columns 2 to 6
for col in range(3, 8):  # Loop through columns 2 to 6
    create_option_menu(1, col, pokemon_types[1], 0)  # Pass vector_index as 0 for attacking types

# Create OptionMenus for columns 1 and 2 in rows 2 to 6
for row in range(2, 8):  # Correctly iterating over rows 2 to 6
    for col in range(1, 3):  # Iterating over columns 1
        create_option_menu(row, col, pokemon_types[0], row-1)  # Pass vector_index as row-1 for defending types

root.mainloop()
