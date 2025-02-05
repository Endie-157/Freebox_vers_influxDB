# Freebox_vers_influxDB

Est-ce que ça vous est arrivé de vouloir obtenir des données en live de votre freebox et de les renvoyer dans influxDB pour finir sur Grafana?

Bonne nouvelle! C'est exactement ce que fait ce petit script sur python.

Un exemple de ce qui est possible se trouve ici: https://stats.endtech.fr

---

## Comment utiliser:

Télécharger appTokenFetch.py, authreq.json et requetesVersFreebox.py.

Modifier authreq.json et mettre vos propres valeurs dans les quatre champs.

Éxecuter appTokenFetch.py, ce script va utiliser les valeurs dans authreq.json pour demander un token a la freebox. Vous devez ensuite confirmer physiquement sur l'interface de la freebox pour authoriser l'application.

Ensuite, rendez vous sur http://mafreebox.freebox.fr/ et allez dans les paramètres de la freebox, puis géstion des accès. Dans l'onglet qui s'ouvre, allez dans application. vous devriez voir le nom de l'application et ses permissions. Sur la droite, appuyer sur le crayon pour modifier les permissions et accordez l'accès à "Modification des réglages de la Freebox".

Dans le fichier authrep.json qui sera créé vous trouverez votre token et un id.

(Il est possible que vous devez vous rendre à http://mafreebox.freebox.fr/api/v12/login/authorize/{id} pour activer le token.)

Ensuite vous devez éditer requetesVersFreebox.py et rentrer vos informations influxDB et freebox dans les champs en haut.

Enfin il ne vous reste plus qu'à lancer le script et tout devrais être envoyé à influxDB, avec possibilité de renvoyer vers Grafana. 
