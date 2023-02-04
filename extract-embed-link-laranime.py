import requests
import re
import os

# Demande l'URL à l'utilisateur
url = input("Entrez un URL laranime.tv d'un épisode d'un anime : ")

# Récupère le code source de la page
response = requests.get(url)

# Remplace les caracteres d'echappement
text = response.text.replace("\\", "")

# Extrait les URLs en utilisant une expression rationnelle
urls = re.findall(r'https://filemoon\.sx/e/[\w-]+/[\w\(\)\._-]+', text)

if not urls:
    urls = re.findall(r'https://streamlare.com/e/[\w]+/[\w\.-]+', text)

# Supprime les doublons de la liste
urls = list(set(urls))

# Extrait les numéros d'épisodes et reformate les URLs
episodes = []
for url in urls:
    parts = url.split("/")
    stripped_url = "/".join(parts[:5])
    match = re.search(r'Episode_(\d+)', url)
    if not match:
        match = re.search(r'(\d+)[\w\.-]+', parts[-1])
    if match:
        episode_number = match.group(1)
        episode = f"Episode {int(episode_number):03d} : {stripped_url}"
        episodes.append(episode)

# Trie les épisodes par numéro d'épisode
episodes.sort(key=lambda x: int(x.split(" ")[1]))

# Enlève le premier "0" dans les épisodes nommés "Episode 010" à "Episode 099" et le premier "00" dans les épisodes nommés "Episode 001" à "Episode 009"
for i, episode in enumerate(episodes):
    parts = episode.split(" ")
    if parts[1].startswith("0"):
        parts[1] = str(int(parts[1]))
        episodes[i] = " ".join(parts)

# Écrit les URLs extraites triées et reformatées dans un fichier
file_path = "Episodes.txt"
with open(file_path, "w", encoding="utf-8") as f:
    for episode in episodes:
        f.write(episode + "\n\n")

os.remove("source_code.html")
os.remove("reformatted_source_code.html")
