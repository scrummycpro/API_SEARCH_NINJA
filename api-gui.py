import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog, simpledialog, Menu
import requests
import json

def perform_request():
    query = entry_query.get()  # Get the query from the entry widget
    url = "http://0.0.0.0:12345/api/search"
    params = {'q': query}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Check for HTTP errors
        json_data = json.loads(response.text)
        formatted_json = json.dumps(json_data, indent=4)  # Pretty print JSON
        
        text_area.config(state=tk.NORMAL)  # Enable editing of text widget
        text_area.delete('1.0', tk.END)  # Clear existing text
        text_area.insert(tk.END, formatted_json)  # Insert new data
        text_area.config(state=tk.DISABLED)  # Disable editing of text widget
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
    except json.JSONDecodeError:
        messagebox.showerror("Error", "Failed to parse JSON response")

def save_text():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        content = text_area.get('1.0', tk.END)
        with open(file_path, 'w') as file:
            file.write(content)

def copy_text():
    root.clipboard_clear()
    text = text_area.get(tk.SEL_FIRST, tk.SEL_LAST)
    root.clipboard_append(text)

def show_popup(event):
    popup_menu.tk_popup(event.x_root, event.y_root)

# Create the main window
root = tk.Tk()
root.title("HTTP Request Example")

# Create an entry widget for inputting the query
entry_query = tk.Entry(root, width=50)
entry_query.pack(pady=10)
entry_query.insert(0, "Enter your query here")  # Default text

# Create a scrollable text widget for displaying the JSON response
text_area = scrolledtext.ScrolledText(root, width=60, height=10, wrap=tk.WORD, state=tk.DISABLED)
text_area.pack(pady=10)

# Create a popup menu for copying text
popup_menu = Menu(root, tearoff=0)
popup_menu.add_command(label="Copy", command=copy_text)

# Bind the popup to the text area
text_area.bind("<Button-3>", show_popup)  # Button-3 is the right-click

# Create a button that will call the perform_request function when clicked
btn_request = tk.Button(root, text="Perform Request", command=perform_request)
btn_request.pack(pady=10)

# Create a button to save the text
btn_save = tk.Button(root, text="Save", command=save_text)
btn_save.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
