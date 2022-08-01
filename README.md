# Goals
The main goals of this project was to build an application to generate spotify playlists according to some criteria. 
Another "technical" objective was to test the R/Python interconnectivity, and thus to build an application using both. 

# Quick description of the application:

The application may take a few seconds to load completely (at most one minute), here is the unloaded application: 
![image](https://user-images.githubusercontent.com/61666789/170869957-41b05daa-78d4-4ccb-b259-16b7341c1784.png)

And here is the loaded application: 
![image](https://user-images.githubusercontent.com/61666789/170870001-f8625f58-87fc-4681-9a7d-b58ed115a615.png)

You can select the desired features of the playlist and the application will update the list. You can then listen to the music directly from the application (a 30 seconds extract if you are not connected, all the music otherwise) and select your new favorite playlist! 

# Description of the application (data recovery, processing)

We retrieve data directly from the Spotify API using a Python script, which will extract all available playlists. For each playlist, we then need to extract the list of each song and the list of features of each song. Once these data are retrieved, we perform a constrained optimization with the inputs specified by the user as a constraint. The final list of selected playlists is then sent back to the front end managed by Shiny.

In order to keep the data up to date, we have also developed a system that uses the GitHub API as a database. Thus, the python script is stored on Heroku and automatically triggered once a day to retrieve the data. Then, thanks to the GitHub API, the previous data is transferred to an "Archive" folder to keep track of it, then the new data is transferred to the "data" folder.  

URL to the app:
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
