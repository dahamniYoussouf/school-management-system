# 🎓 École de Luxe et Design - Système de Gestion Scolaire Intégré

## 📋 Vue d'ensemble

Système de gestion scolaire complet et intégré spécialement conçu pour les établissements d'enseignement supérieur dans les secteurs du luxe, de la mode, du design et de la joaillerie. Cette solution tout-en-un comprend **10 modules professionnels** couvrant tous les aspects de la gestion scolaire.

## ✨ Caractéristiques principales

- **Architecture modulaire** avec 10 modules intégrés
- **Multi-campus** et multi-filières
- **Authentification sécurisée** avec gestion des rôles et permissions
- **Interface multilingue** (Français, Anglais, Arabe)
- **Responsive design** pour mobile et desktop
- **API RESTful** complète
- **Conformité RGPD** et audit de sécurité
- **Rapports et analytics** en temps réel

---

## 🧭 Les 10 Modules du Système

### 1️⃣ Module d'Administration Générale

**Objectif :** Centraliser la gestion des profils, rôles et paramètres de l'école.

**Fonctionnalités :**
- ✅ Gestion complète des utilisateurs
- ✅ Système de rôles et permissions granulaires
- ✅ Configuration des paramètres globaux
- ✅ Gestion multi-campus et départements
- ✅ Personnalisation de l'identité visuelle

**API Endpoints :**
- `GET/POST /api/users` - Gestion des utilisateurs
- `GET/PUT /api/settings` - Paramètres de l'école
- `GET /api/campuses` - Gestion des campus
- `GET /api/departments` - Gestion des départements

---

### 2️⃣ Module Pédagogique

**Objectif :** Gérer le cycle académique complet.

**Fonctionnalités :**
- ✅ Gestion des programmes de formation
- ✅ Création et organisation des cours
- ✅ Planning des classes et emplois du temps
- ✅ Suivi de l'assiduité en temps réel
- ✅ Système d'évaluation et de notation
- ✅ Gestion des sessions de cours
- ✅ Support pour coefficients et crédits ECTS

**Entités :**
- `Program` - Programmes (Bachelor, Master, Certificate)
- `Course` - Cours et matières
- `Class` - Classes avec horaires
- `ClassSession` - Sessions de cours individuelles
- `Attendance` - Présences
- `Grade` - Notes et évaluations

**API Endpoints :**
- `GET/POST /api/programs` - Programmes
- `GET/POST /api/courses` - Cours
- `GET/POST /api/classes` - Classes
- `GET/POST /api/attendance` - Assiduité
- `GET/POST /api/grades` - Notes

---

### 3️⃣ Module Étudiant

**Objectif :** Offrir un espace personnel complet à chaque étudiant.

**Fonctionnalités :**
- ✅ Inscription en ligne et gestion des dossiers
- ✅ Profil étudiant détaillé
- ✅ Consultation des notes et absences
- ✅ Gestion des documents (CV, diplômes, certificats)
- ✅ Historique académique
- ✅ Statut d'inscription et GPA

**Entités :**
- `Student` - Profil étudiant complet
- `Enrollment` - Inscriptions aux programmes
- `StudentDocument` - Documents administratifs
- `StudentFinancial` - Dossier financier

**API Endpoints :**
- `GET/POST /api/students` - Gestion des étudiants
- `GET /api/students/{id}` - Détails d'un étudiant
- `GET /api/students/{id}/documents` - Documents de l'étudiant

---

### 4️⃣ Module RH & Enseignants

**Objectif :** Gérer le personnel administratif et académique.

**Fonctionnalités :**
- ✅ Gestion des enseignants et du personnel
- ✅ Contrats de travail (CDI, CDD, freelance)
- ✅ Gestion des congés et absences
- ✅ Évaluations de performance
- ✅ Historique professionnel
- ✅ Spécialisations et qualifications

**Entités :**
- `Teacher` - Profil enseignant
- `Staff` - Personnel administratif
- `EmployeeContract` - Contrats de travail
- `Leave` - Demandes de congés
- `TeacherEvaluation` - Évaluations

**API Endpoints :**
- `GET/POST /api/teachers` - Enseignants
- `GET /api/staff` - Personnel
- `GET/POST /api/leaves` - Congés

---

### 5️⃣ Module Financier

**Objectif :** Assurer une gestion financière transparente et efficace.

**Fonctionnalités :**
- ✅ Gestion des frais de scolarité
- ✅ Échéanciers de paiement personnalisés
- ✅ Enregistrement des paiements
- ✅ Génération de factures automatique
- ✅ Gestion des bourses et subventions
- ✅ Suivi des impayés
- ✅ Rapports financiers

**Entités :**
- `StudentFinancial` - Dossier financier étudiant
- `Payment` - Paiements
- `Invoice` - Factures
- `Scholarship` - Bourses
- `ScholarshipApplication` - Candidatures aux bourses

**API Endpoints :**
- `GET /api/financial/students` - Dossiers financiers
- `GET/POST /api/payments` - Paiements
- `GET /api/scholarships` - Bourses disponibles

---

### 6️⃣ Module Infrastructure & Logistique

**Objectif :** Optimiser la gestion matérielle et logistique.

**Fonctionnalités :**
- ✅ Gestion des bâtiments et salles
- ✅ Réservation de salles
- ✅ Inventaire des équipements
- ✅ Maintenance préventive
- ✅ Gestion des stocks
- ✅ Organisation d'événements

**Entités :**
- `Building` - Bâtiments
- `Room` - Salles de cours
- `RoomReservation` - Réservations
- `Equipment` - Équipements
- `MaintenanceRecord` - Maintenance
- `InventoryItem` - Inventaire
- `Event` - Événements

**API Endpoints :**
- `GET /api/rooms` - Liste des salles
- `GET /api/rooms/available` - Salles disponibles
- `GET /api/equipment` - Équipements
- `GET /api/events` - Événements

---

### 7️⃣ Module Communication & Marketing

**Objectif :** Renforcer l'image de marque et la communication.

**Fonctionnalités :**
- ✅ CRM pour gestion des prospects
- ✅ Campagnes marketing
- ✅ Base de données alumni
- ✅ Gestion des partenaires
- ✅ Newsletters
- ✅ Suivi des candidatures

**Entités :**
- `Lead` - Prospects
- `Campaign` - Campagnes marketing
- `Alumni` - Anciens élèves
- `Partner` - Partenaires industriels
- `Newsletter` - Newsletters

**API Endpoints :**
- `GET/POST /api/leads` - CRM Prospects
- `GET /api/alumni` - Alumni
- `GET /api/partners` - Partenaires

---

### 8️⃣ Module Reporting & BI

**Objectif :** Vision stratégique en temps réel.

**Fonctionnalités :**
- ✅ Tableaux de bord personnalisables
- ✅ Statistiques en temps réel
- ✅ Rapports automatiques
- ✅ Export Excel/PDF
- ✅ Indicateurs de performance (KPI)
- ✅ Analyses académiques et financières

**Entités :**
- `Dashboard` - Tableaux de bord personnalisés
- `Report` - Rapports générés

**API Endpoints :**
- `GET /api/dashboard/stats` - Statistiques clés
- `GET /api/reports` - Liste des rapports

---

### 9️⃣ Module Sécurité & Conformité

**Objectif :** Protection des données et conformité RGPD.

**Fonctionnalités :**
- ✅ Authentification multi-facteurs (2FA)
- ✅ Gestion des consentements RGPD
- ✅ Logs d'audit complets
- ✅ Sauvegarde automatique
- ✅ Traçabilité des actions
- ✅ Gestion des sessions

**Entités :**
- `AuditLog` - Logs d'audit
- `GDPRConsent` - Consentements RGPD
- `DataBackup` - Sauvegardes

**API Endpoints :**
- `GET /api/audit-logs` - Logs d'audit
- `POST /api/gdpr/consent` - Gestion RGPD

---

### 🔟 Module Mobile & UX

**Objectif :** Expérience utilisateur optimale.

**Fonctionnalités :**
- ✅ Interface responsive (mobile/tablet/desktop)
- ✅ Système de notifications en temps réel
- ✅ Préférences utilisateur
- ✅ Thèmes (clair/sombre)
- ✅ Support multilingue
- ✅ API optimisée

**Entités :**
- `Notification` - Notifications
- `UserPreference` - Préférences utilisateur

**API Endpoints :**
- `GET /api/notifications` - Notifications
- `PUT /api/notifications/{id}/read` - Marquer comme lu
- `GET/PUT /api/preferences` - Préférences

---

## 🚀 Installation

### Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- SQLite (inclus avec Python)

### Étapes d'installation

1. **Cloner le repository :**
```bash
git clone <repository-url>
cd school-management-system
```

2. **Créer un environnement virtuel :**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. **Installer les dépendances :**
```bash
pip install -r requirements.txt
```

4. **Lancer l'application :**
```bash
python app_integrated.py
```

5. **Accéder à l'application :**
```
http://localhost:5000
```

### 🔐 Compte par défaut

- **Nom d'utilisateur :** admin
- **Mot de passe :** admin123

**⚠️ IMPORTANT :** Changez ce mot de passe en production !

---

## 📁 Structure du projet

```
school-management-system/
├── app_integrated.py          # Application Flask principale
├── models_extended.py         # Modèles de base de données (50+ tables)
├── requirements.txt           # Dépendances Python
├── README_INTEGRATED.md       # Documentation complète
├── modules/                   # Modules du système
│   ├── administration/
│   ├── pedagogical/
│   ├── student_portal/
│   ├── hr/
│   ├── financial/
│   ├── infrastructure/
│   ├── communication/
│   ├── reporting/
│   ├── security/
│   └── mobile/
├── templates/                 # Templates HTML
│   ├── base_integrated.html   # Template de base
│   ├── index_integrated.html  # Page de connexion
│   └── dashboard.html         # Tableau de bord
└── static/                    # Fichiers statiques
    ├── css/
    ├── js/
    └── img/
```

---

## 🗄️ Architecture de la base de données

### Tables principales (50+ tables)

**Administration :**
- users, permissions, user_permissions, school_settings
- campuses, departments

**Pédagogique :**
- programs, courses, classes, class_sessions
- attendance, grades

**Étudiants :**
- students, enrollments, student_documents

**RH :**
- teachers, staff, employee_contracts, leaves
- teacher_evaluations

**Financier :**
- student_financial, payments, invoices
- scholarships, scholarship_applications

**Infrastructure :**
- buildings, rooms, room_reservations
- equipment, maintenance_records, inventory_items, events

**Communication :**
- leads, campaigns, alumni, partners, newsletters

**Reporting :**
- reports, dashboards

**Sécurité :**
- audit_logs, gdpr_consents, data_backups

**Mobile/UX :**
- notifications, user_preferences

---

## 🔌 API Documentation

### Authentification

```bash
# Login
POST /api/auth/login
Content-Type: application/json
{
  "username": "admin",
  "password": "admin123"
}

# Logout
POST /api/auth/logout

# Get current user
GET /api/auth/me
```

### Exemples d'utilisation

**Créer un étudiant :**
```bash
POST /api/students
Content-Type: application/json
{
  "student_number": "2024001",
  "first_name": "Marie",
  "last_name": "Dubois",
  "email": "marie.dubois@example.com",
  "date_of_birth": "2000-05-15",
  "phone": "+33612345678",
  "password": "temporary123"
}
```

**Enregistrer une note :**
```bash
POST /api/grades
Content-Type: application/json
{
  "student_id": 1,
  "class_id": 5,
  "grade": 16.5,
  "assignment_name": "Projet Final",
  "assignment_type": "project",
  "weight": 2.0,
  "date": "2024-11-04"
}
```

**Enregistrer un paiement :**
```bash
POST /api/payments
Content-Type: application/json
{
  "student_financial_id": 1,
  "amount": 2500.00,
  "payment_date": "2024-11-04",
  "payment_method": "bank_transfer"
}
```

---

## 🎨 Personnalisation

### Couleurs et Thème

Modifiez les couleurs dans `SchoolSettings` :

```python
settings = SchoolSettings.query.first()
settings.primary_color = '#3498db'
settings.secondary_color = '#2ecc71'
db.session.commit()
```

### Logo et Identité

Téléchargez votre logo et mettez à jour :

```python
settings.logo_url = '/static/img/logo.png'
settings.school_name = 'Votre École'
```

---

## 🔒 Sécurité

### Bonnes pratiques

1. **Changez les identifiants par défaut**
2. **Utilisez des mots de passe forts**
3. **Activez l'authentification 2FA**
4. **Configurez des sauvegardes automatiques**
5. **Vérifiez régulièrement les logs d'audit**
6. **Mettez à jour régulièrement les dépendances**

### Variables d'environnement

Créez un fichier `.env` :

```bash
SECRET_KEY=votre-clé-secrète-très-longue-et-aléatoire
DATABASE_URL=sqlite:///school_integrated.db
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=votre-email@example.com
MAIL_PASSWORD=votre-mot-de-passe
```

---

## 📊 Rapports et Analytics

### Statistiques disponibles

- Nombre total d'étudiants actifs
- Nombre d'enseignants
- Programmes et cours actifs
- Taux de présence
- Performance financière
- Taux de réussite académique

### Exporter des rapports

```python
# Générer un rapport académique
GET /api/reports?type=academic&year=2024

# Générer un rapport financier
GET /api/reports?type=financial&month=11
```

---

## 🌍 Multilingue

### Langues supportées

- 🇫🇷 Français (par défaut)
- 🇬🇧 Anglais
- 🇲🇦 Arabe

### Changer la langue

```javascript
fetch('/api/preferences', {
  method: 'PUT',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ language: 'en' })
});
```

---

## 📱 Responsive Design

L'interface s'adapte automatiquement à tous les appareils :

- 📱 Smartphones (iOS/Android)
- 📱 Tablettes
- 💻 Ordinateurs de bureau
- 🖥️ Grands écrans

---

## 🧪 Tests

```bash
# Installer les dépendances de test
pip install pytest pytest-flask

# Lancer les tests
pytest

# Tests avec couverture
pytest --cov=.
```

---

## 🤝 Support et Contribution

### Signaler un bug

Créez une issue sur GitHub avec :
- Description du problème
- Étapes pour reproduire
- Captures d'écran si applicable

### Demander une fonctionnalité

Ouvrez une discussion pour proposer de nouvelles fonctionnalités.

---

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

---

## 👥 Auteurs

Développé avec ❤️ pour les établissements d'enseignement supérieur dans le secteur du luxe.

---

## 🎯 Roadmap

### Version 2.1 (À venir)

- [ ] Application mobile native (iOS/Android)
- [ ] Intégration API de paiement (Stripe, PayPal)
- [ ] Module de visioconférence intégré
- [ ] IA pour recommandations personnalisées
- [ ] Signature électronique des documents
- [ ] Export vers systèmes comptables (SAP, QuickBooks)

### Version 2.2

- [ ] Portail parent
- [ ] Module de bibliothèque
- [ ] Gestion des stages et alternances
- [ ] Planification automatique des emplois du temps
- [ ] Chatbot intelligent

---

## 📞 Contact

Pour toute question ou assistance :

- 📧 Email : support@ecole-luxe.com
- 🌐 Site Web : www.ecole-luxe.com
- 📱 Téléphone : +33 1 23 45 67 89

---

**Bonne utilisation de votre système de gestion scolaire ! 🎓✨**
