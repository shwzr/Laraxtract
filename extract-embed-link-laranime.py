import requests
import re
import os

# Obtiens l'URL de l'utilisateur
url = input("Entrez un URL laranime.tv que tu peux retrouver pour l'Episode x d'un anime : ")

# Telecharge le code source de la page
response = requests.get(url)

# Il ecrit le code source de la page dans le fichier
with open("source_code.html", "w") as f:
    f.write(response.text)

# Il lit le code source de la page depuis le fichier
with open("source_code.html", "r") as f:
    text = f.read()

# Il remplace les caracteres d'echappement
text = text.replace("\\", "")

# Il ecrit le code source de la page reformatee dans le fichier
with open("reformatted_source_code.html", "w") as f:
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
    episode_number = re.search(r'Episode_(\d+)', url).group(1)
    episode = f"Episode {int(episode_number):03d} : {stripped_url}"
    episodes.append(episode)

# Il trie les episodes par numero d'episode
episodes.sort()

# Il ecrit les URLs extraites triees et reformatees dans un fichier
with open("Episodes.txt", "w") as f:
    for episode in episodes:
        f.write(episode + "\n")

# Il supprime les fichiers de code source
os.remove("source_code.html")
os.remove("reformatted_source_code.html")
