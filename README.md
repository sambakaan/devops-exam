# Bibliothèque Numérique — Plateforme Microservices

Plateforme de gestion de bibliothèque académique en architecture microservices : inscription
et authentification des usagers, catalogue de livres, gestion des emprunts et retours,
le tout orchestré via Docker Compose avec un pipeline Jenkins pour l'intégration continue.

## Stack

- **Backend** : Python 3.12, FastAPI (`utilisateurs-service`, `livres-service`, `emprunts-service`)
- **Frontend** : Angular
- **Base de données** : PostgreSQL 16 (schémas séparés par service)
- **Auth** : JWT (HS256)
- **Conteneurisation** : Docker, Docker Compose
- **CI/CD** : Jenkins

## Prérequis

- Docker
- Docker Compose

Aucune autre dépendance locale n'est nécessaire (ni Python, ni Node) : tout tourne en
conteneurs.

## Installation

```bash
git clone <url-du-repo>
cd devops-exam

cp .env.example .env
```

Éditer ensuite `.env` et changer au minimum ces deux valeurs avant tout démarrage
(les valeurs de `.env.example` sont des placeholders de développement, pas des secrets
réels) :

- `JWT_SECRET_KEY` : secret de signature des tokens JWT, partagé par les 3 services
  backend. Générer une valeur aléatoire, par exemple :
  ```bash
  openssl rand -hex 32
  ```
- `POSTGRES_PASSWORD` : mot de passe de l'instance PostgreSQL. Si vous le changez,
  mettez aussi à jour `DATABASE_URL` dans le même `.env` (le mot de passe y est répété
  dans l'URL de connexion SQLAlchemy).

Les autres variables (ports, `POSTGRES_USER`, `POSTGRES_DB`, URLs internes
`http://<service>:<port>`) sont déjà correctes pour un usage local et n'ont pas besoin
d'être modifiées.

## Lancement

```bash
docker compose -p bibliotheque up -d --build
```

`-p bibliotheque` fixe explicitement le nom de projet Compose. Sans lui, Compose nomme le
projet d'après le dossier courant (`devops-exam`) - ce qui entrerait en collision avec le
projet du conteneur Jenkins (`jenkins/docker-compose.jenkins.yml`, lancé avec
`--project-directory .`, donc nommé `devops-exam` lui aussi) et mélangerait les deux dans
les commandes `docker compose ps`/`down`. `-p bibliotheque` est aussi le nom de projet
utilisé par le stage `Deploy` du `Jenkinsfile` - garder la même valeur en local évite toute
ambiguïté entre un déploiement manuel et un déploiement via le pipeline.

Vérifier que tous les services sont démarrés et en bonne santé :

```bash
docker compose -p bibliotheque ps
```

Chaque service doit apparaître avec un statut `running (healthy)` (le `frontend` n'a pas
de healthcheck déclaré, `running` suffit pour lui). Le démarrage complet.

Accéder à l'application : **http://localhost:4200**

Pour arrêter la stack :

```bash
docker compose -p bibliotheque down
docker compose -p bibliotheque down -v
```

## Structure du projet

```
devops-exam/
├── utilisateurs-service/   # FastAPI - inscription, authentification, émission JWT
├── livres-service/         # FastAPI - catalogue des livres (CRUD, recherche)
├── emprunts-service/       # FastAPI - emprunts/retours, appelle les 2 services ci-dessus
├── frontend/               # Angular - SPA consommant les 3 API via un reverse proxy nginx
├── postgres/               # init.sql : création des schémas
├── jenkins/                # Image et Compose de l'outil CI
├── docker-compose.yml      # Orchestration de la stack
├── Jenkinsfile             # Pipeline CI/CD
├── .env.example            # Modèle des variables d'environnement
└── .env                    # Vraies valeurs locales
```

- **`utilisateurs-service/`** : gère les comptes usagers et l'authentification. Émet les
  JWT consommés par les deux autres services backend. Port `8001`.
- **`livres-service/`** : gère le catalogue (ajout, recherche, consultation des livres).
  Port `8002`.
- **`emprunts-service/`** : gère le cycle de vie des emprunts (création, retour, retards).
  Seul service autorisé à appeler les deux autres. Port `8003`.
- **`frontend/`** : application Angular (modules `auth`, `utilisateurs`, `livres`,
  `emprunts`), buildée puis servie par nginx en conteneur ; nginx fait aussi office de
  reverse-proxy vers les 3 API backend.
- **`postgres/`** : script d'initialisation exécuté au premier démarrage du conteneur
  Postgres, crée un schéma par service (`users_schema`, `livres_schema`,
  `emprunts_schema`) dans une base unique partagée.
- **`jenkins/`** : Dockerfile et `docker-compose.jenkins.yml` de l'outil Jenkins
  lui même - volontairement séparés de la stack applicative.

## Pipeline CI/CD

Le pipeline est défini dans le `Jenkinsfile` à la racine et exécute 4 stages.

Jenkins tourne lui même en conteneur Docker (`jenkins/Dockerfile`,
`jenkins/docker-compose.jenkins.yml`), séparé de la stack applicative - c'est l'outil qui
la déploie, il n'en fait pas partie. Le socket Docker de l'hôte est monté dedans pour qu'il
puisse piloter `docker`/`docker compose` sur l'hôte.

### Lancer Jenkins

```bash
docker compose -f jenkins/docker-compose.jenkins.yml --project-directory . up -d --build

# récupérer le mot de passe admin initial
cat jenkins/jenkins_home/secrets/initialAdminPassword
```

Ouvrir http://localhost:8080, coller le mot de passe, terminer l'assistant de démarrage.
Les plugins nécessaires (`git`, `workflow-aggregator`, `docker-workflow`) sont déjà
installés dans l'image ; l'assistant ne fait qu'associer un compte admin et proposer
l'installation de plugins suggérés.

### Créer le job (première configuration)

1. _New Item_ → nom au choix (ex. `bibliotheque-numerique`) vers type **Pipeline** → _OK_.
2. Section **Pipeline** → _Definition_ = `Pipeline script from SCM` vers _SCM_ = `Git`.
3. URL du dépôt :
   - **Voie principale** (une fois un remote GitHub configuré) :
     `https://github.com/<votre-org>/<repo>.git`.
   - **Voie locale/hors-ligne** (pas encore de remote GitHub) : le repo est monté en
     lecture seule dans le conteneur Jenkins sous `/repo` - utiliser `file:///repo`
     comme URL (aucun identifiant requis).
4. _Branch Specifier_ = `*/main`.
5. _Script Path_ = `Jenkinsfile` (valeur par défaut).
6. _Save_, puis _Build Now_ pour déclencher le premier run.

### Credential requise avant le premier Deploy

Créer une
credential Jenkins de type **Secret file**, id `bibliotheque-env`, dont le contenu est le
`.env` réel du projet (celui créé à l'étape "Installation" ci-dessus, avec vos propres
`JWT_SECRET_KEY`/`POSTGRES_PASSWORD`) — _Manage Jenkins_ vers _Credentials_ vers _System_ vers
_Global credentials_ → _Add Credentials_ vers _Kind_ = `Secret file`, _ID_ =
`bibliotheque-env`.

### Où voir les résultats

- Vue d'ensemble des stages : page du job vers build en cours ou passé vers _Stage View_ (les
  4 stages `Checkout`/`Test`/`Build`/`Deploy` apparaissent en colonnes, vert/rouge).
- Logs complets : _Console Output_ du build.
- La stack applicative déployée par le stage `Deploy` reste accessible normalement sur
  http://localhost:4200, indépendamment de Jenkins.

### Limitation connue (setup local Docker Desktop for Mac)

`jenkins/docker-compose.jenkins.yml` monte `JENKINS_HOME` au même chemin absolu côté hôte
et côté conteneur (`${PWD}/jenkins/jenkins_home` des deux côtés). C'est nécessaire : sur
Docker Desktop for Mac, un `docker compose`/`docker run` exécuté par Jenkins (donc adressé
au démon Docker de l'hôte via le socket monté) ne peut monter que des chemins hôte réels et
partagés - un volume Docker nommé classique échoue avec `mounts denied`. Cette contrainte
ne se pose pas sur un vrai serveur Jenkins Linux dédié ; c'est spécifique à ce setup de
développement/examen sur Mac.

## Ports

| Service              | Port hôte | Rôle                                     |
| -------------------- | --------- | ---------------------------------------- |
| postgres             | 5432      | Base de données PostgreSQL               |
| utilisateurs-service | 8001      | API inscription / authentification       |
| livres-service       | 8002      | API catalogue de livres                  |
| emprunts-service     | 8003      | API emprunts / retours                   |
| frontend             | 4200      | Application Angular (servie par nginx)   |
| jenkins              | 8080      | Interface Jenkins (outil CI, hors stack) |
