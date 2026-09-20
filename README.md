# PROPHÈTE KESMANER HENRY — SOVEREIGN MASTER AI ENGINE

## État

Cette version fournit le noyau modulaire et l'API de fondation. Elle n'est pas un modèle génératif et ne prétend pas être parfaite. Aucun fournisseur externe n'est connecté par défaut.

## Architecture

`SovereignMasterEngine` orchestre contexte, classification, planification, exécution locale, vérification et réponse. Les packages `reasoning`, `knowledge`, `verification`, `memory`, `models`, `tools`, `language`, `spiritual`, `voice`, `security`, `admin` et `diagnostics` sont conçus comme des points d'extension.

## Installation et lancement

```bash
python -m unittest discover -s tests
python main.py
```

Le serveur écoute `0.0.0.0` sur `PORT` (8080 par défaut). Aucun paquet externe n'est requis pour cette fondation.

## Configuration

Copier `.env.example` vers la configuration de l'environnement. Ne jamais ajouter de secrets à GitHub. `MODEL_PROVIDER` et `VOICE_ENABLED` ne rendent pas une intégration fonctionnelle sans implémentation réelle du fournisseur.

## API

- `GET /health`
- `GET /api/v1/status`
- `GET /api/v1/capabilities`
- `POST /api/v1/chat` avec `message`, `session_id`, `language` et `mode`

Sans modèle configuré, `/api/v1/chat` retourne explicitement une réponse locale limitée et un avertissement.

## Railway

Le `Procfile` conserve `web: python main.py`. Railway doit fournir `PORT` automatiquement. PostgreSQL n'est pas modifié par cette phase; aucune migration destructive n'a été ajoutée.

## Prochaines phases

Ajouter une implémentation de fournisseur via `BaseModelProvider`, puis PostgreSQL/Alembic, authentification réelle, administration protégée, recherche documentaire, tests API, voix et vision. Chaque capacité devra être testée avant d'être annoncée comme active.
