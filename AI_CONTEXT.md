# PROJET: Marketing Event Planner (Internal)
# VERSION: 0.1 (Init)

## 1. TECH STACK & RÈGLES
- **Backend:** Django 5.x
- **Database:** PostgreSQL
- **Frontend:** Django Templates + HTMX + TailwindCSS (Via CDN pour dev, Pipeline pour prod)
- **Hosting:** PythonAnywhere
- **Conventions:**
  - Code et commentaires en ANGLAIS.
  - Docstrings obligatoires sur les modèles et vues complexes.
  - Utilisation de `django-environ` pour les variables d'env.
  - Nommage: snake_case pour Python, kebab-case pour URLs.
- **Human Verification Rule:**
  - À la fin de chaque phase, l'IA fournit une checklist des actions testables.
  - L'humain confirme que tout fonctionne AVANT de passer à la phase suivante.
  - Aucune phase n'est marquée ✅ sans confirmation humaine explicite.

## 2. INFRASTRUCTURE & CONTRAINTES
- **Stockage Media:** Local (limite 30GB global PythonAnywhere).
- **Stratégie Fichiers:**
  - Compression images à l'upload (via Pillow).
  - Limite taille upload: 500MB max par fichier.
  - Archivage auto des events > 1 mois (cron task).
- **Mobile First:** Les vues d'upload doivent être optimisées mobile.
- **PythonAnywhere Specifics:**
  - WSGI configuration (pas de Docker).
  - Static files via `collectstatic` + whitenoise.
  - Media files servis localement.
  - Scheduled tasks via PythonAnywhere console.

## 3. ROADMAP (Générée par l'IA)

### Phase 1: Setup & Fondations (Sprint 1)
- [x] Lecture PRD et création AI_CONTEXT.md
- [ ] `django-admin startproject` + structure apps
- [ ] Configuration PostgreSQL + django-environ
- [ ] Setup TailwindCSS (CDN dev mode)
- [ ] Configuration HTMX
- [ ] Base templates (layout, navbar, mobile nav)

### Phase 2: User & Auth (Sprint 2)
- [ ] Custom User Model (AbstractUser) avec roles (Admin/Member)
- [ ] Login/Logout views (session longue pour mobile)
- [ ] RBAC middleware simplifié
- [ ] Admin Django customisé

### Phase 3: Core Models - Bars & Themes (Sprint 3)
- [ ] Model `Bar` (name, location, hardware_specs JSON)
- [ ] Model `ThemePeriod` (month, year, name, description)
- [ ] Admin interfaces pour Bar/Theme
- [ ] API/Views de base

### Phase 4: Events & Calendar (Sprint 4)
- [ ] Model `Event` (date, name, theme, bars M2M, description)
- [ ] Vue Calendrier (Mois/Semaine/Trimestre) avec HTMX
- [ ] Filtres par Bar, par Statut
- [ ] Indicateurs de santé (🟢🟠🔴)

### Phase 5: Deliverables System (Sprint 5)
- [ ] Model `DeliverableTemplate` (name, specs, is_default)
- [ ] Model `EventDeliverable` (event, template, status, asset)
- [ ] Génération auto des deliverables selon les bars
- [ ] Matrice des deliverables sur Event Card

### Phase 6: Asset Management (Sprint 6)
- [ ] Model `Asset` (file, version, uploaded_by, created_at)
- [ ] Upload Drag & Drop (Desktop) + Camera (Mobile)
- [ ] Versioning des fichiers
- [ ] Compression images à l'upload
- [ ] Preview PDF/Video inline
- [ ] Dashboard espace disque

### Phase 7: Event Card UI (Sprint 7)
- [ ] Modal fullscreen Event Card
- [ ] Section Brief & Concept
- [ ] Section Moodboard (upload images)
- [ ] Section Deliverables Matrix
- [ ] Countdown J-X
- [ ] Règle J-7 alertes visuelles

### Phase 8: Collaboration (Sprint 8)
- [ ] Model `Comment` (text, author, linked_entity)
- [ ] Activity Stream sur Event Card
- [ ] Commentaires threadés
- [ ] Mentions @user

### Phase 9: Notifications & Polish (Sprint 9)
- [ ] Email notifications (recap quotidien)
- [ ] Vue Matrice de Production
- [ ] PWA manifest pour mobile
- [ ] Optimisations performances

### Phase 10: Deployment (Sprint 10)
- [ ] Configuration PythonAnywhere
- [ ] WSGI setup
- [ ] Static/Media files config
- [ ] Scheduled tasks (archivage)
- [ ] Tests finaux & documentation

## 4. DATA MODEL (DRAFT)

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER                                     │
├─────────────────────────────────────────────────────────────────┤
│ id (PK)                                                          │
│ email (unique)                                                   │
│ username                                                         │
│ role: ENUM ['admin', 'member']                                   │
│ is_active, created_at, updated_at                                │
└─────────────────────────────────────────────────────────────────┘
        │
        │ uploaded_by (FK)
        ▼
┌─────────────────────────────────────────────────────────────────┐
│                         ASSET                                    │
├─────────────────────────────────────────────────────────────────┤
│ id (PK)                                                          │
│ file (FileField)                                                 │
│ original_filename                                                │
│ file_size                                                        │
│ version (int, default=1)                                         │
│ parent_asset (FK to self, null) → for versioning                 │
│ uploaded_by (FK User)                                            │
│ created_at                                                       │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                      THEME_PERIOD                                │
├─────────────────────────────────────────────────────────────────┤
│ id (PK)                                                          │
│ name (ex: "Cyberpunk", "Eden Reborn")                            │
│ description (text)                                               │
│ month (1-12)                                                     │
│ year (int)                                                       │
│ is_active (bool)                                                 │
│ created_at, updated_at                                           │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                          BAR                                     │
├─────────────────────────────────────────────────────────────────┤
│ id (PK)                                                          │
│ name                                                             │
│ location (city, address)                                         │
│ hardware_specs (JSONField)                                       │
│   → {"screens": [{"name": "Cube LED", "resolution": "1024x1024"},│
│                  {"name": "Door LED", "resolution": "1920x1080"}]│
│ is_active (bool)                                                 │
│ created_at, updated_at                                           │
└─────────────────────────────────────────────────────────────────┘
        │
        │ M2M through EventBar
        ▼
┌─────────────────────────────────────────────────────────────────┐
│                         EVENT                                    │
├─────────────────────────────────────────────────────────────────┤
│ id (PK)                                                          │
│ name                                                             │
│ date (DateField)                                                 │
│ theme (FK ThemePeriod)                                           │
│ bars (M2M Bar)                                                   │
│ description (TextField)                                          │
│ brief (TextField, rich text)                                     │
│ notes (TextField)                                                │
│ status: computed property based on deliverables                  │
│ created_by (FK User)                                             │
│ created_at, updated_at                                           │
└─────────────────────────────────────────────────────────────────┘
        │
        │ FK Event
        ▼
┌─────────────────────────────────────────────────────────────────┐
│                   DELIVERABLE_TEMPLATE                           │
├─────────────────────────────────────────────────────────────────┤
│ id (PK)                                                          │
│ name (ex: "Poster A3", "Cube LED Video")                         │
│ specs (ex: "1024x1024 mp4", "A3 300dpi PDF")                     │
│ category: ENUM ['print', 'video', 'social', 'screen']            │
│ is_default (bool) → auto-added to new events                     │
│ bar (FK Bar, null) → if specific to a bar's hardware             │
│ created_at                                                       │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                   EVENT_DELIVERABLE                              │
├─────────────────────────────────────────────────────────────────┤
│ id (PK)                                                          │
│ event (FK Event)                                                 │
│ template (FK DeliverableTemplate)                                │
│ status: ENUM ['todo','in_progress','review','changes','approved']│
│ assigned_to (FK User, null)                                      │
│ asset (FK Asset, null)                                           │
│ is_enabled (bool) → can disable for specific event               │
│ due_date (auto: event.date - 7 days)                             │
│ created_at, updated_at                                           │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                       MOODBOARD_IMAGE                            │
├─────────────────────────────────────────────────────────────────┤
│ id (PK)                                                          │
│ event (FK Event)                                                 │
│ asset (FK Asset)                                                 │
│ category: ENUM ['inspiration', 'uniform', 'decor', 'other']      │
│ caption (optional)                                               │
│ order (int)                                                      │
│ created_at                                                       │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                        COMMENT                                   │
├─────────────────────────────────────────────────────────────────┤
│ id (PK)                                                          │
│ text (TextField)                                                 │
│ author (FK User)                                                 │
│ # Generic relation for flexibility:                              │
│ content_type (FK ContentType)                                    │
│ object_id (int)                                                  │
│ parent (FK self, null) → for threading                           │
│ created_at, updated_at                                           │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                     ACTIVITY_LOG                                 │
├─────────────────────────────────────────────────────────────────┤
│ id (PK)                                                          │
│ user (FK User)                                                   │
│ action: ENUM ['create','update','delete','upload','status_change']
│ content_type (FK ContentType)                                    │
│ object_id (int)                                                  │
│ details (JSONField) → old/new values                             │
│ created_at                                                       │
└─────────────────────────────────────────────────────────────────┘
```

### Relations Summary:
- `User` 1:N `Asset` (uploaded_by)
- `User` 1:N `Comment` (author)
- `User` 1:N `Event` (created_by)
- `ThemePeriod` 1:N `Event`
- `Bar` M:N `Event` (through implicit join table)
- `Bar` 1:N `DeliverableTemplate` (optional, for bar-specific hardware)
- `Event` 1:N `EventDeliverable`
- `Event` 1:N `MoodboardImage`
- `DeliverableTemplate` 1:N `EventDeliverable`
- `Asset` 1:1 `EventDeliverable` (current asset)
- `Asset` 1:N `Asset` (versioning chain via parent_asset)
- `Comment` uses GenericForeignKey (can attach to Event or EventDeliverable)

## 5. JOURNAL DE BORD
- **[2026-01-06]** Initialisation du projet et lecture du PRD.
  - Analyse complète du PRD v1.0
  - Identification des personas: Admin (CEO/Tech) et Member (all others)
  - Compréhension de la contrainte critique 30GB PythonAnywhere
  - Création de AI_CONTEXT.md avec roadmap et data model
  - North Star Metric: 100% assets validés à J-7

- **[2026-01-06]** Phase 1: Setup terminée ✅
  - `django-admin startproject config .` (Django 6.0)
  - 4 apps créées: accounts, venues, planning, assets
  - Split settings: base.py / development.py / production.py
  - Custom User model avec rôles (admin/member)
  - Template `base.html` avec TailwindCSS CDN + HTMX + Alpine.js
  - `python manage.py check` → 0 issues
  - Prochaine étape: Phase 2 (Login/Logout, RBAC)

- **[2026-01-06]** Phase 2: User & Auth terminée ✅
  - Login/Logout views avec sessions 30 jours
  - LoginForm avec styling TailwindCSS
  - Templates: login.html, calendar.html (placeholder)
  - URL routing configuré pour toutes les apps
  - Superuser créé: admin / admin123
  - Flow testé en browser: login → redirect → calendrier ✓
  - Prochaine étape: Phase 3 (Bar, ThemePeriod models)

- **[2026-01-06]** Phase 3: Venues & Themes terminée ✅
  - Model `Bar` avec hardware_specs JSONField
  - Model `ThemePeriod` avec colors et period unique
  - Admin customisé avec badges screens et color swatches
  - Seed data: 3 bars (Neon Club, Skyline, Underground), 2 thèmes (Jan/Feb 2026)
  - Admin testé en browser ✓
  - Prochaine étape: Phase 4 (Event model, deliverables)

- **[2026-01-06]** Phase 4: Events & Deliverables terminée ✅
  - Model `Event` avec M2M bars, FK theme, J-7 deadline logic
  - Model `DeliverableTemplate` lié aux bars (hardware-based)
  - Model `EventDeliverable` avec workflow status (todo → approved)
  - Auto-génération des deliverables via signal m2m_changed
  - Admin avec health badges, deadline countdown, inline deliverables
  - Vue calendrier dynamique avec navigation mois et event indicators
  - Vue event_list avec status badges colorés
  - Vue event_detail avec overview, venues, et deliverables list
  - 3 events de test, 15 deliverables auto-générés
  - Prochaine étape: Phase 5 (Asset upload, link to deliverables)