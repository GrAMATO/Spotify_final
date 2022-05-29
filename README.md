Lien vers l'application :
https://camillephilippe.shinyapps.io/recommandation-playlist-spotify/

# Objectifs
L'objectif principal du projet était de construire une application permettant de générer des playlists spotify en fonction de certains critères. 
Un autre objectif "technique" était de tester l'interconnectivité R/Python, et donc de réaliser une application faisant appel aux deux. 

# Description rapide de l'application :

L'application peut mettre quelques secondes avant de charger complètement (au maximum une minute), voici l'application non chargée : 
![image](https://user-images.githubusercontent.com/61666789/170869957-41b05daa-78d4-4ccb-b259-16b7341c1784.png)

Et voici l'application chargée : 
![image](https://user-images.githubusercontent.com/61666789/170870001-f8625f58-87fc-4681-9a7d-b58ed115a615.png)

Vous pouvez sélectionner les caractéristiques souhaitées de la playlist et l'application mettra à jour la liste. Vous pouvez alors écouter les musiques directement depuis l'application (un extrait de 30 secondes si vous n'êtes pas connectés, toute la musique sinon) et sélectionner ainsi votre nouvelle playlist préférée ! 

# Description du fonctionnement de l'application (récupération des données, traitement)

Nous récupérons directement les données depuis l'API de Spotify grâce à un script Python, qui va donc extraire toutes les playlists disponibles. Pour chaque playlist, il faut ensuite extraire la liste de chaque chanson et la liste des caractéristiques de chaque chanson. Une fois ces données récupérées, nous effectuons une optimisation sous contrainte avec pour contrainte les inputs spécifiés par l'utilisateur. La liste finale des playlists sélectionnées est alors renvoyée sur la partie "front end" gérée par Shiny.

Afin de maintenir les données à jour, nous avons également mis au point un système consistant à utiliser l'API de GitHub afin de s'en servir comme d'une base de données. Ainsi, le script python est stocké sur Heroku et déclenché automatiquement une fois par jour pour récupérer les données. Ensuite, grâce à l'API de GitHub, les données précédentes sont transférées dans un dossier "Archive" afin d'en conserver une trace, puis les nouvelles données sont transférées dans le dossier "data".  
