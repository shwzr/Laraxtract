import tkinter as tk
from tkinter import messagebox
import requests
import re
import os


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
def extract_episode_urls(url):
    # Recupere le code source de la page
    response = requests.get(url)

    # Remplace les caracteres d'echappement
    text = response.text.replace("\\", "")

    # Extrait les URLs en utilisant une expression rationnelle
    urls = re.findall(r'https://filemoon\.sx/e/[\w-]+/[\w\(\)\!\._-]+\.mp4', text)

    if not urls:
        urls = re.findall(r'https://streamlare.com/e/[\w]+/[\w\.-]+', text)

    # Supprime les doublons de la liste
    urls = list(set(urls))

    # Extrait les numeros d'episodes et reformate les URLs
    episodes = []
    for url in urls:
        parts = url.split("/")
        stripped_url = "/".join(parts[:5])
        match = re.search(r'Episode_(\d+)', url)
        if not match:
            match = re.search(r'episode-(\d+)[\w\.-]+', url)
        if match:
            episode_number = match.group(1)
            episode = f"Episode {int(episode_number):03d} : {stripped_url}"
            episodes.append(episode)

    # Trie les episodes par numero d'episode
    episodes.sort(key=lambda x: int(x.split(" ")[1]))

    # Enleve le premier "0" dans les episodes nommes "Episode 010" a "Episode 099" et le premier "00" dans les episodes nommes "Episode 001" a "Episode 009"
    for i, episode in enumerate(episodes):
        parts = episode.split(" ")
        if parts[1].startswith("0"):
            parts[1] = str(int(parts[1]))
            episodes[i] = " ".join(parts)

    return episodes


# Fonction pour extraire les URLs des episodes et les ecrire dans le fichier Episodes.txt
def write_episode_urls_to_file(url):
    episodes = extract_episode_urls(url)

    # Ecrit les URLs extraites triees et reformatees dans un fichier
    file_path = "Episodes.txt"
    with open(file_path, "w", encoding="utf-8") as f:
        for episode in episodes:
            f.write(episode + "\n\n")

    # Retourne la liste des URLs extraites
    return episodes


# Fonction pour afficher les URLs extraites a l'utilisateur
def extract_urls():
    # Obtient l'URL saisie par l'utilisateur
    url = url_entry.get()

    # Verifie si l'URL est valide
    if not is_valid_laranime_url(url):
        messagebox.showerror("Erreur", "L'URL saisie n'est pas valide.")
        return

    # Extrait les URLs des episodes et les ecrit dans un fichier
    episodes = write_episode_urls_to_file(url)

# Fonction pour afficher les URLs extraites a l'utilisateur
def extract_urls():
    # Obtient l'URL saisie par l'utilisateur
    url = url_entry.get()

    # Verifie si l'URL est valide
    if not is_valid_laranime_url(url):
        messagebox.showerror("Erreur", "URL invalide")
        return

    # Extrait les URLs des episodes
    episodes = write_episode_urls_to_file(url)

    # Affiche les URLs extraites dans le widget Text
    url_text.delete("1.0", tk.END)  # Efface le contenu precedent du widget Text
    url_text.insert(tk.END, "\n".join(episodes))


# Cree la fenetre principale
window = tk.Tk()
window.title("Laraxtract")

# Désactive le redimensionnement de la fenêtre
window.resizable(0,0)

# Changer la couleur de fond de la fenêtre
window.configure(background="#F5F5F5")

# Cree le widget Label pour l'URL
url_label = tk.Label(window, text="URL de la série :", font=("Helvetica", 14), fg="#333333", bg="#F5F5F5")
url_label.grid(row=0, column=0, padx=5, pady=5)

# Cree le widget Entry pour l'URL
url_entry = tk.Entry(window, width=50, font=("Helvetica", 14), fg="#333333", bg="#FFFFFF")
url_entry.grid(row=0, column=1, padx=5, pady=5)

# Cree le widget Button pour extraire les URLs
extract_button = tk.Button(window, text="Extraire les URLs", command=extract_urls, font=("Helvetica", 14), fg="#FFFFFF", bg="#333333")
extract_button.grid(row=0, column=2, padx=5, pady=5)

# Cree le widget Text pour afficher les URLs extraites
url_text = tk.Text(window, width=70, height=20, font=("Helvetica", 12), fg="#333333", bg="#FFFFFF", bd=0, relief="flat")
url_text.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

# Crée la fonction pour afficher une fenêtre d'information
def show_info():
    messagebox.showinfo("Infos", "Version: 1.1\nContact: Showzur#8509")

# Crée le widget Button pour afficher l'information
info_button = tk.Button(window, text="i", font=("Helvetica", 14), fg="#333333", bg="#F5F5F5", bd=0, command=show_info)
info_button.grid(row=1, column=3, padx=5, pady=5, sticky="se")




# Lance la boucle principale de l'application
window.mainloop()
