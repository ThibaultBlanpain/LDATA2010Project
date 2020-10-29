import Tkinter as tk
window = tk.Tk()

menu = tk.Menubutton()
greeting = tk.Label(text="Hello, Tkinter") #text or picture
greeting.pack()

button = tk.Button(
    text="Click me!",
    width=25,
    height=5)
button.pack()

#entry = tk.Entry(fg="yellow", bg="blue", width=50)
#entry.pack()

#name = entry.get()

#print(name)

#liste = Listbox(window)
#liste.insert(1, "Python")
#liste.insert(2, "PHP")
#liste.insert(3, "jQuery")
#liste.insert(4, "CSS")
#liste.insert(5, "Javascript")
#liste.pack()
def callback():
    if askyesno('Titre 1', 'etes-vous sr de vouloir faire a?'):
        showwarning('Titre 2', 'Tant pis...')
    else:
        showinfo('Titre 3', 'Vous avez peur!')
        showerror("Titre 4", "Aha")

tk.Button(text='Action', command=callback).pack()

def recupere():
    showinfo("Alerte", entree.get())

name = tk.StringVar()
name.set("Valeur")
entree = tk.Entry(window, textvariable=name, width=30)
entree.pack()

bouton = tk.Button(window, text="Valider", command=recupere)
bouton.pack()



window.mainloop()

print(name)
