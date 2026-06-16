# Documentation Authenticate_fe

Ce document decrit le code present dans `Authenticate_fe/Authenticate_fe`. Il couvre l'architecture front, les pages React, les contextes, le theme, et l'infra (Docker/Ansible).

## Vue d'ensemble

- Frontend React + Vite + TypeScript.
- UI avec Chakra UI (system v3), theme personnalise, et polices Switzer.
- Auth JWT via API backend (Django), gestion du panier en localStorage.
- Routing avec React Router.

## Arborescence utile

- `Authenticate_fe/src/` : code React (pages, components, hooks, services).
- `Authenticate_fe/public/` : assets statiques (images, polices, public/index.html).
- `Authenticate_fe/vite.config.ts` : config Vite (port dev, base path, allowed hosts).
- `Authenticate_fe/docker_resources/Dockerfile` : build dev/prod.
- `Authenticate_fe/docker_resources/docker-compose.dev.yml` / `Authenticate_fe/docker_resources/docker-compose.prod.yml` : services.
- `Authenticate_fe/.env.example` : variables attendues.

## Point d'entree

- `Authenticate_fe/src/main.tsx` : monte l'app React et charge `switzer.css`.
- `Authenticate_fe/src/App.tsx` : routes, providers, gestion des erreurs.

## Routing

Defini dans `Authenticate_fe/src/App.tsx`:

- Public
  - `/activate/:uid/:token` -> `AccountActivationPage`
  - `/auth/reset-password/:uid/:token` -> `ResetPassword`
  - `/connexion` -> `LoginPage`
  - `/mot-de-passe-oublie` -> `PasswordForgottenPage`
- Protege (via `ProtectedRoute` + `ProtectedLayout`)
  - `/` -> `HomePage`
- Fallback
  - `*` -> `UnknownPage`

Un ErrorBoundary global affiche `ErrorPage` en cas d'erreur.

## Contextes et etat global

### AuthContext (`Authenticate_fe/src/hooks/AuthContext.tsx`)

- Gere l'utilisateur connecte, le login, le logout, et le refresh de token.
- Stocke l'utilisateur en localStorage.
- Expose `ApiService` preconfigure avec le user.

### ConfigContext (`Authenticate_fe/src/hooks/ConfigContext.tsx`)

- Hydrate Chakra avec un theme basé sur la config (`clientSystem`).
- Persiste la config en localStorage.

## Service API

Fichier: `Authenticate_fe/src/services/api.ts`

Wrapper Axios avec:

- Base URL `VITE_BACKEND_URL`.
- Timeout `VITE_BACKEND_TIMEOUT`.
- Injection JWT (header `Authorization: JWT <token>`).

Endpoints utilises:

- Auth: `/user/auth/jwt/create/`, `/auth/jwt/refresh/`.
- Config: `/user/config/me/`.
- Activation: `/auth/users/activation/`, `/auth/users/resend_activation/`.
- Reset: `/auth/users/reset_password_confirm/`, `/auth/users/reset_password/`.

## Composants principaux

- `BaseLayout` : layout simple avec background et logo.
- `AccountLayout` : wrapper des pages login/activation/reset.
- `ProtectedLayout` : header, navigation, menu utilisateur, categories.
- `ProtectedRoute` : redirection vers `/connexion` si pas d'utilisateur.
- `Loader` : ecran de chargement global.

Composants UI reutilises:

- `components/ui/theme.ts` : tokens Chakra (polices, couleurs, boutons, inputs).
- `components/ui/prose.tsx` : styles typographiques pour contenu HTML.
- `components/ui/toaster.tsx` : toasts (Chakra).
- `components/ui/password-input.tsx` : champ mot de passe avec toggle.
- `components/ui/color-mode.tsx` : helpers theme (non utilises par defaut).
- `components/ui/tooltip.tsx` : wrapper tooltip.

## Pages

- `HomePage` : accueil, intro config + grille categories.
- `LoginPage` : authentification.
- `PasswordForgottenPage` : demande reset password.
- `AccountActivationPage` : activation compte + resend activation.
- `ResetPassword` : page reset password (utilisee dans App).
- `ErrorPage` / `UnknownPage` : fallback UI.

## Types

Dans `Authenticate_fe/src/types/`:

- `users.ts` : `UserData`, `ConfigData`.

## Assets et styles

- Images: `Authenticate_fe/public/images/*`.
- `public/index.html` contient un `config.js` runtime genere par Docker.
- `index.html` a la racine est le point d'entree Vite (celui utilise par defaut).

## Variables d'environnement

Fichier exemple: `Authenticate_fe/.env.example`

Variables Vite connues:

- `VITE_BACKEND_URL`
- `VITE_BACKEND_TIMEOUT`
- `VITE_APP_BASE`
- `VITE_APP_NAME` (utilise pour le titre)
- `VITE_BORDER_RADIUS` (utilise dans ProductPage)
- `VITE_API_BASE_URL`, `VITE_FEATURE_X_ENABLED`, `VITE_ANALYTICS_WRITE_KEY` (exemple)

Note: `docker/entrypoint.sh` genere un `config.js` avec `window.__APP_CONFIG__`, mais le code React ne le lit pas. Si besoin de config runtime, il faut ajouter un loader cote front.

## Vite

Fichier: `Authenticate_fe/vite.config.ts`

- Dev server: port `5193`, `allowedHosts` via env `ALLOWED_HOST`.
- `base` configurable via `VITE_APP_BASE`.
- `vite-tsconfig-paths` active les alias TypeScript.

## Docker

- `Authenticate_fe/docker_resources/Dockerfile`:
  - stage dev: Vite HMR sur `5193`.
  - stage build: `npm run build`.
  - stage prod: Nginx sert `dist/` sur port `PORT`. // Placeholder ports frontend prod
- `Authenticate_fe/docker_resources/docker-compose.dev.yml`: map `5193:5193`.
- `Authenticate_fe/docker_resources/docker-compose.prod.yml`: map `PORT:PORT` // Placeholder ports frontend prod (Nginx interne).
