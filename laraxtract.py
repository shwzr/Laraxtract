import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import requests
import re
import os

icon_path = "laranime.ico"

# Supprime Episodes.txt s'il est present
if os.path.exists("Episodes.txt"):
    os.remove("Episodes.txt")

# Fonction pour verifier la validite de l'URL
def is_valid_laranime_url(url):
    if not url.startswith("https://laranime.tv/"):
        return False
    if url.count("/") < 6:
        return False
    parts = url.split("/")
    if not parts[-1]:
        return False
    return True

# Fonction pour extraire les URLs des episodes a partir de l'URL de la serie
def extract_episode_urls(url, regex):
    response = requests.get(url)
    text = response.text.replace("\\", "")
    urls = re.findall(regex, text)
    urls = list(set(urls))
    episodes = []
    for url in urls:
        parts = url.split("/")
        stripped_url = "/".join(parts[:5])
        match = re.search(r'Episode_(\d+)', url)
        if not match:
            match = re.search(r'episode-(\d+)[\w.-]+', url)
        if match:
            episode_number = match.group(1)
            episode = f"Episode {int(episode_number):03d} : {stripped_url}"
            episodes.append(episode)
    episodes.sort(key=lambda x: int(x.split(" ")[1]))
    for i, episode in enumerate(episodes):
        parts = episode.split(" ")
        if parts[1].startswith("0"):
            parts[1] = str(int(parts[1]))
            episodes[i] = " ".join(parts)
    return episodes

# Fonction pour extraire les URLs des episodes et les ecrire dans le fichier Episodes.txt
def write_episode_urls_to_file(url, regex):
    episodes = extract_episode_urls(url, regex)
    file_path = "Episodes.txt"
    with open(file_path, "w", encoding="utf-8") as f:
        for episode in episodes:
            f.write(episode + "\n\n")
    return episodes

# Fonction pour afficher les URLs extraites a l'utilisateur
def extract_urls():
    url = url_entry.get()
    if not is_valid_laranime_url(url):
        messagebox.showerror("Erreur", "URL invalide")
        return
    regex = ""
    if regex_var.get() == 1:
        regex = r'https://filemoon\.sx/e/[\w-]+/[\w\(\)\!\._-]+\.mp4'
    elif regex_var.get() == 2:
         regex = r'https://streamlare.com/e/[\w]+/[\w\.-]+'
    else:
        messagebox.showerror("Erreur", "Veuillez sélectionner un lecteur.")
        return
    episodes = write_episode_urls_to_file(url, regex)
    url_text.delete("1.0", tk.END)
    url_text.insert(tk.END, "\n\n".join(episodes))

# Créer la fenêtre principale à l'intérieur du conteneur Frame
window = tk.Tk()
window.title("Laraxtract")
window.iconbitmap(default=icon_path)
window.resizable(0,0)
window.configure(background="#F5F5F5")
url_label = tk.Label(window, text="URL de la série :", font=("Helvetica", 14), fg="#333333", bg="#F5F5F5")
url_label.grid(row=0, column=0, padx=5, pady=5)
url_entry = ttk.Entry(window, style='Rounded.TEntry', width=30, font=("Helvetica", 14))
url_entry.grid(row=0, column=1, padx=5, pady=5)
style = ttk.Style()
style.configure('Rounded.TEntry', borderwidth=0, bordercolor='#8c8c8c', focusthickness=3, focuscolor='#4511b9', padding=8, relief=tk.SOLID, borderradius=30)
regex_label = tk.Label(window, text="Lecteur souhaité :", font=("Helvetica", 14), fg="#333333", bg="#F5F5F5")
regex_label.grid(row=1, column=0, padx=5, pady=5)
regex_var = tk.IntVar()
regex_var.set(0)
regex_radio_1 = tk.Radiobutton(window, text="filemoon", font=("Helvetica", 14), variable=regex_var, value=1, bg="#F5F5F5")
regex_radio_1.grid(row=1, column=1, padx=5, pady=5, sticky="w")
regex_radio_2 = tk.Radiobutton(window, text="streamlare", font=("Helvetica", 14), variable=regex_var, value=2, bg="#F5F5F5")
regex_radio_2.grid(row=2, column=1, padx=5, pady=5, sticky="w")
url_button = tk.Button(window, text="Extraire les épisodes", font=("Helvetica", 14), bg="#333333", fg="#FFFFFF", command=extract_urls)
url_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
url_text = tk.Text(window, width=50, height=20, font=("Helvetica", 14))
url_text.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
def show_info():
    messagebox.showinfo("Infos", "Version: 1.2\nContact: Showzur#8509")
info_button = tk.Button(window, text="i", font=("Helvetica", 14), fg="#333333", bg="#F5F5F5", bd=0, command=show_info)
info_button.grid(row=0, column=2, padx=5, pady=5, sticky="w")
window.mainloop()
