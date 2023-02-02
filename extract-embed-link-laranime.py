import requests
import re
import os

# Il verifie si le fichier "Episodes.txt" existe et il le supprime si c'est le cas.
if os.path.exists("Episodes.txt"):
    os.remove("Episodes.txt")

# Obtiens l'URL de l'utilisateur
url = input("Entrez un URL laranime.tv que tu peux retrouver pour l'Episode x d'un anime : ")

# Telecharge le code source de la page
response = requests.get(url)

# Il ecrit le code source de la page dans le fichier
with open("source_code.html", "w", encoding="utf-8") as f:
    f.write(response.text)

# Il lit le code source de la page depuis le fichier
with open("source_code.html", "r", encoding="utf-8") as f:
    text = f.read()

# Il remplace les caracteres d'echappement
text = text.replace("\\", "")

# Il ecrit le code source de la page reformatee dans le fichier
with open("reformatted_source_code.html", "w", encoding="utf-8") as f:
    f.write(text)

# Il extrait les URLs en utilisant une expression rationnelle
urls = re.findall(r'https://filemoon\.sx/e/[\w-]+/[\w\d\._-]+', text)

# Il supprime les doublons de la liste
urls = list(set(urls))

# Il extrait les numeros d'episodes et reformater les URL
episodes = []
for url in urls:
    parts = url.split("/")
    stripped_url = "/".join(parts[:5])
    match = re.search(r'Episode_(\d+)', url)
    if match:
        episode_number = match.group(1)
        episode = f"Episode {int(episode_number):03d} : {stripped_url}"
        episodes.append(episode)


# Il trie les episodes par numero d'episode
episodes.sort()

# Il enleve le premier "0" dans les episodes nommes "Episode 010" a "Episode 099" et le premier "00" dans les episodes nommes "Episode 001" a "Episode 009"
for i, episode in enumerate(episodes):
    parts = episode.split(" ")
    if parts[1].startswith("0"):
        parts[1] = str(int(parts[1]))
        episodes[i] = " ".join(parts)

episodes.sort(key=lambda x: int(x.split(" ")[1])) 

# Il ecrit les URLs extraites triees et reformatees dans un fichier
with open("Episodes.txt", "w", encoding="utf-8") as f:
    for episode in episodes:
        f.write(episode + "\n\n")

# Il supprime les fichiers de code source
os.remove("source_code.html")
os.remove("reformatted_source_code.html")
