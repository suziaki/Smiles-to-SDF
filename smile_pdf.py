import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import os
import pypdb
from collections import deque
from rdkit import Chem
from rdkit.Chem import AllChem

# Global list to store the last 10 searches
last_10_searches = deque(maxlen=10)

def open_file():
    # Get the filename from the user
    filename = filedialog.askopenfilename(title="Open File", filetypes=[("FASTA files", "*.fasta")])

    # Check if the user selected a file
    if filename:
        global fasta_data
        # Get the file extension (file type)
        file_type = os.path.splitext(filename)[1]

        # Display the file type in a message box
        messagebox.showinfo("File Type", f"The imported file type is: {file_type}")

        # Read the contents of the file and store it in the global variable
        with open(filename, "r") as file:
            fasta_data = file.read()

def show_fasta_data():
    global fasta_data
    if fasta_data:
        # Display the stored fasta data in a message box
        tk.messagebox.showinfo("FASTA Data", fasta_data)
    else:
        tk.messagebox.showwarning("No Data", "No FASTA data has been imported yet.")

def exit_program():
    window.quit()

def pdb_search():
    # Get the user's search query
    query = tk.simpledialog.askstring("PDB Search", "Enter your search query:")

    # Perform the PDB search using PyPDB
    if query:
        results = pypdb.get_entities(query)
        # Store the search query in the list of last 10 searches
        last_10_searches.append(query)

        # Display the search results in a message box
        messagebox.showinfo("PDB Search Results", f"Search query: {query}\n\nResults:\n{results}")

def show_last_10_searches():
    # Display the last 10 searches in a message box
    if last_10_searches:
        message = "Last 10 Searches:\n\n" + "\n".join(last_10_searches)
        messagebox.showinfo("Last 10 Searches", message)
    else:
        messagebox.showinfo("Last 10 Searches", "No searches have been performed yet.")
#Generate .sdf file from SMILES string
def generate_sdf():
    # Get the user's SMILES string
    smiles_string = simpledialog.askstring("Generate .sdf", "Enter the SMILES string:")

    if smiles_string:
        try:
            # Convert the SMILES string to an RDKit molecule object
            mol = Chem.MolFromSmiles(smiles_string)

            # Save the molecule as an .sdf file
            if mol:
                sdf_filename = filedialog.asksaveasfilename(title="Save .sdf File", defaultextension=".sdf",
                                                            filetypes=[("SDF files", "*.sdf")])
                if sdf_filename:
                    writer = Chem.SDWriter(sdf_filename)
                    writer.write(mol)
                    writer.close()

                    messagebox.showinfo("Generate .sdf", f".sdf file generated successfully.")
            else:
                messagebox.showwarning("Generate .sdf", f"Invalid SMILES string.")
        except Exception as e:
            messagebox.showerror("Generate .sdf", f"An error occurred: {str(e)}")


# Create the main window
window = tk.Tk()
window.title("File Menu Example")

# Create the menu bar
menubar = tk.Menu(window)

# Create the file menu
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Exit", command=exit_program)

# Create the "Import File" submenu
import_submenu = tk.Menu(filemenu, tearoff=0)
import_submenu.add_command(label="Import FASTA File", command=open_file)
import_submenu.add_command(label="Show FASTA Data", command=show_fasta_data)

# Add the "Import File" submenu to the file menu
filemenu.add_cascade(label="Import File", menu=import_submenu)

# Add the PDB search function to the file menu
filemenu.add_command(label="PDB Search", command=pdb_search)

# Add a submenu to show the last 10 searches
last_10_search_submenu = tk.Menu(filemenu, tearoff=0)
last_10_search_submenu.add_command(label="Show Last 10 Searches", command=show_last_10_searches)
filemenu.add_cascade(label="Last 10 Searches", menu=last_10_search_submenu)
#Add Generate .sdf file to the file menu
filemenu.add_command(label="Generate .sdf", command=generate_sdf)


# Add the file menu to the menu bar
menubar.add_cascade(label="File", menu=filemenu)

# Display the menu bar
window.config(menu=menubar)

# Start the main loop
window.mainloop()
