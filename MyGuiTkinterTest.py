import tkinter as tk
root = tk.Tk()
root.title("My Gui")
root.geometry("300x200")
root.resizable(width=False, height=False)
label = tk.Label(root, text="Hello Rich from tkinter\n")
label.pack()
button = tk.Button(root, text="PressMe", command=lambda:print("Hello Rich"))
button.pack()
root.mainloop()
print(button)
def on_button_clicked():
    print("Button clicked")
