import requests
import re
import os

# Supprime Episodes.txt s'il est present
if os.path.exists("Episodes.txt"):
    os.remove("Episodes.txt")

# Fonction pour verifier la validite de l'URL
def is_valid_laranime_url(url):
    if url.count("/") < 6:
        return False
    parts = url.split("/")
    if not parts[-1]:
        return False
    return True

 # Demande l'URL a l'utilisateur
while True:
    url = input("Entrez un URL laranime.tv d'un episode d'un anime : ")
    if is_valid_laranime_url(url):
        break
    else:
        print("Ce lien est invalide. Voici un exemple (https://laranime.tv/animes/high-card-vostfr/saison-1/episode-01-one-shot)")

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

# Ecrit les URLs extraites triees et reformatees dans un fichier
file_path = "Episodes.txt"
with open(file_path, "w", encoding="utf-8") as f:
    for episode in episodes:
        f.write(episode + "\n\n")
