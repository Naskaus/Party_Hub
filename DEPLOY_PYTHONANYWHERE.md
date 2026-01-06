# Party Hub - Déploiement PythonAnywhere
## Configuration: Naskaus

---

## 📋 Infos de ton Setup

| Paramètre | Valeur |
|-----------|--------|
| **URL** | `https://partyhub-naskaus.pythonanywhere.com` |
| **Source code** | `/home/Naskaus/PartyHub` |
| **Working directory** | `/home/Naskaus/` |
| **WSGI file** | `/var/www/partyhub-naskaus_pythonanywhere_com_wsgi.py` |
| **Python** | 3.13 |
| **GitHub** | `https://github.com/Naskaus/Party_Hub.git` |

---

## 🚀 Étape 1: Clone le Repo

Ouvre un **Bash console** sur PythonAnywhere et exécute:

```bash
# Supprimer le dossier vide s'il existe
rm -rf /home/Naskaus/PartyHub

# Cloner depuis GitHub
cd /home/Naskaus
git clone https://github.com/Naskaus/Party_Hub.git PartyHub

# Vérifier que tout est là
ls PartyHub/
```

Tu devrais voir: `apps/`, `config/`, `templates/`, `manage.py`, etc.

---

## 🐍 Étape 2: Créer Virtualenv + Installer Dépendances

```bash
# Créer virtualenv avec Python 3.13
mkvirtualenv --python=/usr/bin/python3.13 partyhub

# Aller dans le projet
cd /home/Naskaus/PartyHub

# Installer toutes les dépendances
pip install -r requirements.txt
pip install python-dotenv
```

---

## ⚙️ Étape 3: Créer le fichier .env

```bash
# Créer le fichier de configuration
cat > /home/Naskaus/PartyHub/.env << 'EOF'
DEBUG=False
SECRET_KEY=change-this-to-a-random-50-character-string-here!!!
ALLOWED_HOSTS=partyhub-naskaus.pythonanywhere.com,localhost
EOF
```

> **Important**: Génère une vraie clé secrète avec:
> ```bash
> python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
> ```
> Puis remplace `SECRET_KEY` dans le fichier `.env`

---

## 🗄️ Étape 4: Initialiser la Base de Données

```bash
cd /home/Naskaus/PartyHub
workon partyhub

# Créer les tables
python manage.py migrate

# Créer ton compte admin
python manage.py createsuperuser
# → Username: admin
# → Email: ton@email.com
# → Password: ton-mot-de-passe

# Collecter les fichiers static
python manage.py collectstatic --noinput

# Créer les dossiers media
mkdir -p /home/Naskaus/PartyHub/media

# OPTIONNEL: Charger les données demo (7 bars, 10 events, etc.)
python seed_real_data.py
```

---

## 📝 Étape 5: Configurer le WSGI

1. Va dans l'onglet **Web** sur PythonAnywhere
2. Clique sur le lien WSGI: `/var/www/partyhub-naskaus_pythonanywhere_com_wsgi.py`
3. **SUPPRIME TOUT** le contenu existant
4. **COLLE** ce code:

```python
import os
import sys
from pathlib import Path

# Add project to Python path
project_home = '/home/Naskaus/PartyHub'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Load environment variables from .env file
from dotenv import load_dotenv
env_path = Path(project_home) / '.env'
load_dotenv(env_path)

# Set Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

# Get WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

5. **Sauvegarde** le fichier (Ctrl+S ou bouton Save)

---

## 🔧 Étape 6: Configurer l'onglet Web

### 6.1 Virtualenv Path

Dans la section **Virtualenv**, entre ce chemin:

```
/home/Naskaus/.virtualenvs/partyhub
```

Puis appuie sur Entrée.

### 6.2 Static Files

Dans la section **Static files**, clique sur "Enter URL" pour ajouter:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/Naskaus/PartyHub/staticfiles/` |
| `/media/` | `/home/Naskaus/PartyHub/media/` |

---

## 🔄 Étape 7: RELOAD!

1. Clique le gros bouton vert **"Reload partyhub-naskaus.pythonanywhere.com"** en haut de la page
2. Attends quelques secondes
3. Visite: **https://partyhub-naskaus.pythonanywhere.com**

---

## 🎉 C'est Live!

Tu devrais voir la page de login. Connecte-toi avec ton admin/password créé à l'étape 4.

---

## 🔧 Troubleshooting

### Voir les erreurs
Onglet **Web** → scroll en bas → **Error log** → clique pour ouvrir

### Erreurs Communes

| Erreur | Cause | Solution |
|--------|-------|----------|
| `ModuleNotFoundError: django` | Virtualenv pas activé | Vérifie le path virtualenv dans Web tab |
| `ModuleNotFoundError: dotenv` | python-dotenv manquant | `workon partyhub && pip install python-dotenv` |
| `DisallowedHost` | ALLOWED_HOSTS mal configuré | Vérifie `.env`, ajoute ton domaine |
| `OperationalError: no such table` | Migrations pas faites | `python manage.py migrate` |
| `Static files 404` | collectstatic pas fait | `python manage.py collectstatic --noinput` |

---

## 🔄 Mises à jour futures

Quand tu modifies le code localement et push sur GitHub:

```bash
# Sur PythonAnywhere Bash console
cd /home/Naskaus/PartyHub
git pull origin main

workon partyhub
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
```

Puis **Reload** dans l'onglet Web.

---

## ✅ Checklist

- [ ] `git clone` dans `/home/Naskaus/PartyHub`
- [ ] Virtualenv `partyhub` créé avec Python 3.13
- [ ] `pip install -r requirements.txt` + `python-dotenv`
- [ ] Fichier `.env` créé avec `SECRET_KEY` et `ALLOWED_HOSTS`
- [ ] `python manage.py migrate` exécuté
- [ ] `python manage.py createsuperuser` exécuté
- [ ] `python manage.py collectstatic` exécuté
- [ ] WSGI file configuré avec le code ci-dessus
- [ ] Virtualenv path: `/home/Naskaus/.virtualenvs/partyhub`
- [ ] Static files mappés: `/static/` et `/media/`
- [ ] **Reload** cliqué
- [ ] Site accessible à https://partyhub-naskaus.pythonanywhere.com 🎉

---

**URL Live:** https://partyhub-naskaus.pythonanywhere.com
