# Guide de Tests et de Présentation Client — Modules Odoo 18

## Table des matières

1. [Méthodologie Générale de Test](#1-méthodologie-générale-de-test)
2. [Lancer les Tests Automatisés](#2-lancer-les-tests-automatisés)
3. [Tests Fonctionnels par Module](#3-tests-fonctionnels-par-module)
4. [Stratégie de Présentation Client](#4-stratégie-de-présentation-client)
5. [Checklist Pré-Démonstration](#5-checklist-pré-démonstration)

---

## 1. Méthodologie Générale de Test

### 1.1 Environnement de Test

Créer une base de données de test dédiée avec données de démonstration :

```bash
python odoo-bin -d test_kamil --addons-path=. -i base --without-demo=False
```

Installer tous les modules en une seule commande :

```bash
python odoo-bin -d test_kamil --addons-path=. -i \
  account_manual_reconcile_v2,allergen_auto,bi_reporting_advanced,\
  custom_phone_validation,employee_order_discount,hr_contract_custom,\
  hr_employee_calendar_planning,hr_shift_custom,livreur,\
  partner_phone_check,product_bom_filter,rapport_bi_redirect,\
  restaurant_customer_feedback,restaurant_daily_menu,\
  restaurant_happy_hour,restaurant_kitchen_analytics,\
  restaurant_loyalty_program,restaurant_order_slots,\
  restaurant_qrcode_menu,restaurant_reservation,\
  restaurant_stock_alert,restaurant_table_layout,\
  restaurant_tip_management,restaurant_waste_tracking,\
  server_environment_files,shipday_odoo,\
  supplier_vat_validation_final,trs_tools
```

### 1.2 Types de Tests

| Type | Outil | Quand |
|------|-------|-------|
| **Tests unitaires Python** | `TransactionCase` | Logique métier, contraintes, calculs |
| **Tests fonctionnels manuels** | Interface Odoo | Parcours utilisateur complet |
| **Tests d'intégration** | Multi-modules | Vérifier les interactions entre modules |
| **Tests de sécurité** | Vérification des droits | Groupes, ACLs, record rules |

### 1.3 Lancer un Test Unitaire

```bash
python odoo-bin -d test_kamil --addons-path=. \
  -i <module_name> --test-enable --stop-after-init \
  --test-tags=/<module_name>
```

Exemple pour `hr_employee_calendar_planning` :

```bash
python odoo-bin -d test_kamil --addons-path=. \
  -i hr_employee_calendar_planning --test-enable --stop-after-init \
  --test-tags=/hr_employee_calendar_planning
```

---

## 2. Lancer les Tests Automatisés

### 2.1 Tests Existants

Seul le module `hr_employee_calendar_planning` dispose actuellement de tests unitaires automatisés.

```bash
python odoo-bin -d test_kamil --addons-path=. \
  -i hr_employee_calendar_planning --test-enable --stop-after-init
```

### 2.2 Structure de Test Odoo 18

Pour ajouter des tests à un module, créer un dossier `tests/` avec :

```
mon_module/
├── tests/
│   ├── __init__.py
│   └── test_mon_module.py
```

Convention Odoo 18 pour le fichier de test :

```python
from odoo.tests import TransactionCase

class TestMonModule(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(
            context=dict(
                cls.env.context,
                mail_create_nolog=True,
                mail_create_nosubscribe=True,
                mail_notrack=True,
                no_reset_password=True,
                tracking_disable=True,
            )
        )

    def test_feature_example(self):
        record = self.env["mon.model"].create({"name": "Test"})
        self.assertEqual(record.name, "Test")
```

---

## 3. Tests Fonctionnels par Module

---

### 3.1 account_manual_reconcile_v2

**Objectif :** Rapprochement manuel avancé avec référence de lettrage.

**Scénarios de test :**

| # | Scénario | Étapes | Résultat attendu |
|---|----------|--------|-------------------|
| 1 | Créer une facture avec référence de lettrage | Comptabilité → Factures → Créer → Remplir `lettrage_ref` | Le champ est sauvegardé et visible |
| 2 | Créer un paiement avec référence de lettrage | Comptabilité → Paiements → Créer → Remplir `lettrage_ref` | Le champ est sauvegardé et visible |
| 3 | Filtrer par référence de lettrage | Utiliser le filtre/recherche sur `lettrage_ref` | Les enregistrements sont filtrés correctement |
| 4 | Ouvrir l'assistant de rapprochement | Menu → Rapprochement manuel | L'assistant s'ouvre sans erreur |

**Présentation client :** Montrer le flux complet : Facture → Paiement → Rapprochement avec la même référence de lettrage. Expliquer le gain de temps par rapport au rapprochement standard.

---

### 3.2 allergen_auto

**Objectif :** Calcul automatique des allergènes depuis les nomenclatures.

**Scénarios de test :**

| # | Scénario | Étapes | Résultat attendu |
|---|----------|--------|-------------------|
| 1 | Vérifier les données de base | Allergènes → Liste | Les 14 allergènes réglementaires sont présents |
| 2 | Affecter un allergène à une matière première | Produit → onglet Allergènes → Ajouter | L'allergène est lié au produit |
| 3 | Calcul auto via nomenclature | Créer un produit fini avec une Nomenclature contenant un ingrédient allergène | Le produit fini hérite automatiquement des allergènes |
| 4 | Affichage e-commerce | Accéder à la fiche produit sur le site web | Les allergènes sont affichés sur la page produit |
| 5 | Compteur de produits | Aller sur un allergène → Voir le compteur | Le nombre de produits contenant cet allergène est correct |

**Présentation client :** Commencer par les matières premières (farine = gluten), puis créer une recette (pain = farine + eau). Montrer que le pain hérite automatiquement de l'allergène "gluten". Mettre en avant la conformité réglementaire européenne (Règlement UE 1169/2011).

---

### 3.3 bi_reporting_advanced

**Objectif :** Rapports BI avancés pour ventes, factures et stocks.

**Scénarios de test :**

| # | Scénario | Étapes | Résultat attendu |
|---|----------|--------|-------------------|
| 1 | Rapport des ventes | Menu BI → Rapport ventes | Le tableau croisé affiche les ventes par période/client |
| 2 | Rapport des factures | Menu BI → Rapport factures | Les données de facturation sont agrégées correctement |
| 3 | Rapport des stocks | Menu BI → Rapport stocks | Les niveaux de stock sont visibles |
| 4 | Vues graphiques | Passer en vue graphique (barres, courbes, camembert) | Les graphiques s'affichent sans erreur |
| 5 | Tâches automatiques | Paramètres → Actions planifiées | Les crons sont créés et planifiés |

**Présentation client :** Préparer des données de ventes/factures sur 3 mois minimum. Montrer les tableaux croisés dynamiques et les graphiques. Insister sur l'automatisation via les crons pour la génération de rapports.

---

### 3.4 custom_phone_validation

**Objectif :** Validation stricte du format téléphone français.

**Scénarios de test :**

| # | Scénario | Étapes | Résultat attendu |
|---|----------|--------|-------------------|
| 1 | Numéro valide `0612345678` | Contacts → Créer → Saisir le numéro → Sauvegarder | Sauvegarde OK |
| 2 | Numéro valide `+33612345678` | Contacts → Créer → Saisir le numéro → Sauvegarder | Sauvegarde OK |
| 3 | Numéro invalide `123` | Contacts → Créer → Saisir le numéro → Sauvegarder | Message d'erreur de validation |
| 4 | Numéro invalide `06123` | Contacts → Créer → Saisir le numéro → Sauvegarder | Message d'erreur de validation |
| 5 | Validation côté site web | E-commerce → Checkout → Saisir un numéro invalide | Le formulaire bloque la validation |

**Présentation client :** Démontrer en direct la saisie de numéros corrects/incorrects. Montrer le message d'erreur clair. Expliquer l'importance de la qualité des données pour les campagnes SMS/marketing.

---

### 3.5 employee_order_discount

**Objectif :** Réduction employé automatique (gratuit si < 2 commandes/mois).

**Scénarios de test :**

| # | Scénario | Étapes | Résultat attendu |
|---|----------|--------|-------------------|
| 1 | Étiqueter un contact comme employé | Contacts → Sélectionner → Ajouter étiquette "Employé" | L'étiquette est attribuée |
| 2 | Première commande du mois | Créer une commande pour l'employé → Confirmer | La remise 100% est appliquée automatiquement, le statut indique "Remise appliquée" |
| 3 | Deuxième commande du mois | Créer une 2ème commande → Confirmer | La remise 100% est encore appliquée |
| 4 | Troisième commande (dépassement) | Créer une 3ème commande → Confirmer | Pas de remise — le statut indique la limite atteinte |
| 5 | Commande via e-commerce | Se connecter en tant qu'employé sur le site → Commander | La remise est appliquée aussi sur le webshop |
| 6 | Réinitialisation | Utiliser le bouton "Réinitialiser la remise" | La remise est recalculée |

**Présentation client :** Préparer un employé avec l'étiquette, montrer 3 commandes consécutives. La 3ème est facturée normalement. Montrer la compatibilité webshop. Mettre en avant l'avantage social et la traçabilité.

---

### 3.6 hr_contract_custom

**Objectif :** Personnalisation des contrats RH avec impression PDF.

**Scénarios de test :**

| # | Scénario | Étapes | Résultat attendu |
|---|----------|--------|-------------------|
| 1 | Créer un contrat | RH → Contrats → Créer → Remplir les champs | Le contrat est créé avec la référence |
| 2 | Imprimer en PDF | Contrat → Imprimer | Le PDF est généré avec les informations complètes |
| 3 | Vérifier la mise en forme | Ouvrir le PDF | La mise en forme est conforme au modèle |

**Présentation client :** Montrer le flux : Créer un employé → Créer un contrat → Imprimer le PDF. Montrer le rendu professionnel du document.

---

### 3.7 hr_employee_calendar_planning

**Objectif :** Planification multi-calendriers par employé avec plages de dates.

**Scénarios de test :**

| # | Scénario | Étapes | Résultat attendu |
|---|----------|--------|-------------------|
| 1 | Tests automatisés | Lancer `--test-tags=/hr_employee_calendar_planning` | Tous les tests passent ✓ |
| 2 | Affecter 2 calendriers | Employé → onglet Calendriers → Ajouter 2 périodes | Les 2 calendriers sont enregistrés avec dates |
| 3 | Vérifier la génération | Sauvegarder → Vérifier le calendrier de ressources | Le calendrier combiné est généré automatiquement |
| 4 | Copier un employé | Dupliquer l'employé | La configuration des calendriers est copiée |
| 5 | Calendrier 2 semaines | Configurer un calendrier en rotation | La rotation est prise en compte |

**Présentation client :** Préparer 2 horaires différents (matin et après-midi). Affecter à un employé sur des périodes différentes. Montrer le calendrier résultant. Expliquer le gain pour la gestion des plannings saisonniers.

---

### 3.8 hr_shift_custom

**Objectif :** Gestion des shifts avec règles RH configurables.

**Scénarios de test :**

| # | Scénario | Étapes | Résultat attendu |
|---|----------|--------|-------------------|
| 1 | Configurer les règles | Shifts → Configuration → Définir pause min, durée max, etc. | Les paramètres sont sauvegardés |
| 2 | Créer un shift | Shifts → Créer → Employé, date, heures | Le shift est en brouillon |
| 3 | Confirmer un shift | Shift → Confirmer | Le statut passe à "Confirmé" |
| 4 | Terminer un shift | Shift → Terminé | Le statut passe à "Terminé" |
| 5 | Violation de règle | Créer un shift dépassant la durée max | Un message d'avertissement s'affiche |
| 6 | Shift trop rapproché | Créer un 2ème shift sans respecter la pause minimum | Un message d'avertissement s'affiche |
| 7 | Vue calendrier | Menu → Vue calendrier | Les shifts sont affichés sur le calendrier |
| 8 | Tableau de bord | Menu → Dashboard | Les statistiques sont correctes |

**Présentation client :** Commencer par la configuration des règles (ex: 11h de pause, 10h max/jour). Créer des shifts conformes puis un shift en violation. Montrer les alertes. Mettre en avant la conformité au Code du Travail.

---

### 3.9 livreur

**Objectif :** Restriction d'accès pour le personnel de livraison.

**Scénarios de test :**

| # | Scénario | Étapes | Résultat attendu |
|---|----------|--------|-------------------|
| 1 | Créer un utilisateur livreur | Paramètres → Utilisateurs → Créer → Attribuer le groupe "Livreur" | L'utilisateur est créé avec le bon groupe |
| 2 | Se connecter en tant que livreur | Déconnexion → Connexion avec le compte livreur | Seul le menu "Commandes" est visible |
| 3 | Vérifier les restrictions | Tenter d'accéder à d'autres menus | Aucun autre menu n'est accessible |
| 4 | Voir les commandes | Menu → Commandes | Les commandes sont visibles |

**Présentation client :** Démonstration split-screen : connexion admin à gauche, connexion livreur à droite. Montrer la différence d'interface. Expliquer la sécurité et la simplicité pour les livreurs.

---

### 3.10 partner_phone_check

**Objectif :** Bloquer la confirmation de commande si le téléphone client est invalide.

**Scénarios de test :**

| # | Scénario | Étapes | Résultat attendu |
|---|----------|--------|-------------------|
| 1 | Client avec téléphone valide | Créer un client avec `+33612345678` → Commande → Confirmer | La commande est confirmée |
| 2 | Client avec téléphone invalide | Créer un client avec `abc` → Commande → Confirmer | Erreur : téléphone invalide |
| 3 | Client sans téléphone | Client sans numéro → Commande → Confirmer | Vérifier le comportement (erreur ou passage) |

**Présentation client :** Montrer le blocage à la confirmation. Expliquer l'intérêt pour la qualité des livraisons (le livreur doit pouvoir appeler le client).

---

### 3.11 product_bom_filter

**Objectif :** Filtrer les produits avec/sans nomenclature.

**Scénarios de test :**

| # | Scénario | Étapes | Résultat attendu |
|---|----------|--------|-------------------|
| 1 | Produit avec nomenclature | Créer un produit → Créer une nomenclature | Le champ `has_bom` = Vrai |
| 2 | Produit sans nomenclature | Créer un produit seul | Le champ `has_bom` = Faux |
| 3 | Filtrer "Avec nomenclature" | Produits → Filtre → Avec nomenclature | Seuls les produits avec nomenclature apparaissent |
| 4 | Filtrer "Sans nomenclature" | Produits → Filtre → Sans nomenclature | Seuls les produits sans nomenclature apparaissent |

**Présentation client :** Montrer une liste de 20+ produits, puis appliquer le filtre. Gain de temps pour identifier les produits sans recette. Utile pour les restaurants qui veulent s'assurer que tous les plats ont une nomenclature de fabrication.

---

### 3.12 rapport_bi_redirect

**Objectif :** Accès aux rapports Power BI depuis Odoo.

**Scénarios de test :**

| # | Scénario | Étapes | Résultat attendu |
|---|----------|--------|-------------------|
| 1 | Ouvrir le menu BI | Menu → Rapports BI | L'interface s'ouvre |
| 2 | Sélectionner un type de rapport | Choisir "Stocks" / "Factures" / "Ventes" | Le type est sélectionné |
| 3 | Redirection vers Power BI | Cliquer → Redirection | Le navigateur ouvre Power BI |

**Présentation client :** Montrer l'intégration fluide Odoo ↔ Power BI. Expliquer que les rapports avancés de BI complètent les rapports natifs Odoo pour une vision 360° de l'activité.

---

### 3.13 restaurant_customer_feedback

**Objectif :** Collecte et analyse des retours clients multi-critères.

**Scénarios de test :**

| # | Scénario | Étapes | Résultat attendu |
|---|----------|--------|-------------------|
| 1 | Créer un feedback | Restaurant → Feedbacks → Créer | Le formulaire s'affiche avec tous les critères |
| 2 | Noter sur 5 critères | Remplir : nourriture=5, service=4, ambiance=3, rapport qualité/prix=4 | La note globale = 4.0 (moyenne auto) |
| 3 | Vérifier le code couleur | Liste des feedbacks | Vert ≥ 4, Jaune ≥ 3, Rouge < 3 |
| 4 | Marquer comme lu | Feedback → Marquer comme lu | Le statut passe à "Lu" |
| 5 | Répondre | Feedback → Répondre | Le statut passe à "Répondu" |
| 6 | Archiver | Feedback → Archiver | Le statut passe à "Archivé" |
| 7 | Analyse en tableau croisé | Vue Pivot | Les moyennes par source/période sont affichées |
| 8 | Sources multiples | Créer des feedbacks de sources différentes (sur place, Google, site) | Tous les types sont disponibles |

**Présentation client :** Préparer 10+ feedbacks avec des notes variées. Montrer la liste colorée, puis le tableau croisé et les graphiques. Montrer le workflow Lu → Répondu → Archivé. Insister sur l'amélioration continue de la qualité.

---

### 3.14 restaurant_daily_menu

**Objectif :** Gestion des menus du jour et planification hebdomadaire.

**Scénarios de test :**

| # | Scénario | Étapes | Résultat attendu |
|---|----------|--------|-------------------|
| 1 | Créer un menu du jour | Restaurant → Menus du jour → Créer | Le formulaire apparaît |
| 2 | Ajouter des plats | Ajouter des lignes : entrée, plat, dessert | Les lignes sont créées avec catégorie et prix |
| 3 | Prix total calculé | Ajouter 3 lignes avec prix | Le total est calculé automatiquement |
| 4 | Prix fixe | Activer l'option "Prix fixe" → Saisir 15€ | Le prix fixe est affiché |
| 5 | Activer le menu | Menu → Activer | Le statut passe à "Actif" |
| 6 | Vue calendrier | Vue calendrier | Les menus sont affichés par semaine |
| 7 | Services multiples | Créer un menu midi ET un menu soir pour le même jour | Les deux apparaissent |

**Présentation client :** Préparer une semaine complète de menus (lundi→vendredi, midi et soir). Montrer la vue calendrier. Insister sur la rapidité de saisie et la planification en avance.

---

### 3.15 restaurant_happy_hour

**Objectif :** Promotions automatiques par jour/heure (Happy Hour).

**Scénarios de test :**

| # | Scénario | Étapes | Résultat attendu |
|---|----------|--------|-------------------|
| 1 | Créer un Happy Hour | Restaurant → Happy Hours → Créer | Le formulaire s'affiche |
| 2 | Configurer jour et horaires | Jour = Vendredi, 17h00-19h00 | Les créneaux sont enregistrés |
| 3 | Remise en pourcentage | Type = Pourcentage, Valeur = 30% | La remise est configurée |
| 4 | Remise en montant fixe | Type = Montant fixe, Valeur = 2€ | La remise est configurée |
| 5 | Affecter des produits | Ajouter les produits concernés | Les produits sont liés |
| 6 | Activer/Désactiver | Activer/Désactiver le flag | Le Happy Hour est actif/inactif |

**Présentation client :** Configurer un Happy Hour du vendredi 17h-19h avec -30% sur les boissons. Montrer la liste des Happy Hours actifs. Expliquer le potentiel marketing et l'automatisation des promotions.

---

### 3.16 restaurant_kitchen_analytics

**Objectif :** Suivi des temps de préparation et des écarts de livraison.

**Scénarios de test :**

| # | Scénario | Étapes | Résultat attendu |
|---|----------|--------|-------------------|
| 1 | Créer une ligne analytique | Restaurant → Cuisine → Créer | Le formulaire s'affiche |
| 2 | Saisir les dates | Date commande = 12h00, Date livraison = 12h25 | Le temps de préparation = 25 min |
| 3 | Écart quantité | Commandé = 10, Livré = 8 | L'écart est visible |
| 4 | Vue Pivot par produit | Vue Pivot | Les moyennes de temps par plat sont affichées |
| 5 | Vue Graphique | Vue Graphique | L'évolution des temps est visible |

**Présentation client :** Préparer des données sur une semaine. Montrer le temps moyen par plat. Identifier les plats les plus lents. Insister sur l'optimisation de la cuisine et la réduction des temps d'attente.

---

### 3.17 restaurant_loyalty_program

**Objectif :** Programme de fidélité avec points et niveaux.

**Scénarios de test :**

| # | Scénario | Étapes | Résultat attendu |
|---|----------|--------|-------------------|
| 1 | Créer une carte de fidélité | Restaurant → Fidélité → Créer une carte | La carte est créée avec un numéro |
| 2 | Ajouter des points | Carte → Historique → Ajouter "Points gagnés" | Le solde augmente |
| 3 | Dépenser des points | Carte → Historique → Ajouter "Points dépensés" | Le solde diminue |
| 4 | Niveau automatique | Accumuler 500 points | Le niveau passe automatiquement (Bronze → Silver → Gold) |
| 5 | Voir un client fidèle | Contacts → Fiche client | Les informations de fidélité sont visibles |
| 6 | Historique complet | Carte → onglet Historique | Toutes les transactions sont listées |

**Présentation client :** Créer un client, ajouter des points progressivement. Montrer les changements de niveau. Mettre en avant la rétention client et le marketing ciblé.

---

### 3.18 restaurant_order_slots

**Objectif :** Créneaux horaires et type de commande (retrait/livraison) pour le webshop.

**Scénarios de test :**

| # | Scénario | Étapes | Résultat attendu |
|---|----------|--------|-------------------|
| 1 | Commande avec créneau backend | Ventes → Commande → Choisir créneau 12h-13h | Le créneau est enregistré |
| 2 | Type Retrait | Sélectionner "Retrait" | Le type est "Retrait" |
| 3 | Type Livraison | Sélectionner "Livraison" | Le type est "Livraison" |
| 4 | Dates de retrait | Choisir "Aujourd'hui" / "Demain" / "Après-demain" | La date est correcte |
| 5 | Résumé calculé | Remplir tous les champs | Le résumé affiche ex: "Retrait - Demain 12h-13h" |
| 6 | Formulaire e-commerce | Site web → Commander → Checkout | Le sélecteur de créneau est visible |
| 7 | PDF de commande | Imprimer la commande | Le créneau apparaît sur le PDF |

**Présentation client :** Commander via le site web. Choisir un créneau de retrait. Confirmer. Montrer le résumé côté backend et le PDF. Expliquer le gain d'efficacité pour la cuisine et la réduction des files d'attente.

---

### 3.19 restaurant_qrcode_menu

**Objectif :** QR codes par table pour accès au menu digital.

**Scénarios de test :**

| # | Scénario | Étapes | Résultat attendu |
|---|----------|--------|-------------------|
| 1 | Créer un QR Code | Restaurant → QR Codes → Créer | Le formulaire s'affiche |
| 2 | Saisir l'URL du menu | Remplir l'URL du menu et le numéro de table | Le QR code est généré automatiquement |
| 3 | Visualiser le QR Code | Voir l'image QR code | L'image PNG est affichée |
| 4 | Compteur de scans | Cliquer "Incrémenter scan" | Le compteur augmente de 1 |
| 5 | Dernière date de scan | Après un scan | La date est mise à jour |
| 6 | Réinitialiser | Cliquer "Réinitialiser les scans" | Le compteur revient à 0 |
| 7 | Scanner le QR | Scanner avec un téléphone | L'URL du menu s'ouvre |

**Présentation client :** Générer un QR code pour la "Table 1". Le projeter à l'écran. Le scanner avec un téléphone. Montrer le compteur de scans. Insister sur l'expérience client moderne et la réduction des contacts physiques (menus papier).

---

### 3.20 restaurant_reservation

**Objectif :** Gestion des réservations de tables.

**Scénarios de test :**

| # | Scénario | Étapes | Résultat attendu |
|---|----------|--------|-------------------|
| 1 | Créer une table | Restaurant → Tables → Créer (4 places, salle) | La table est créée |
| 2 | Créer une réservation | Restaurant → Réservations → Créer | Le formulaire s'affiche |
| 3 | Remplir les infos | Client, date, heure, nombre de personnes, table | Tout est enregistré |
| 4 | Confirmer | Réservation → Confirmer | Le statut passe à "Confirmé" |
| 5 | Installer le client | Réservation → Installé | Le statut passe à "Installé" |
| 6 | Terminer | Réservation → Terminé | Le statut passe à "Terminé" |
| 7 | Annuler | Réservation → Annuler | Le statut passe à "Annulé" |
| 8 | Vue calendrier | Vue calendrier | Les réservations apparaissent |
| 9 | Vue Kanban | Vue Kanban | Les réservations sont colorées par statut |
| 10 | Zones multiples | Créer des tables dans salle, terrasse, bar, VIP | Les zones sont disponibles |

**Présentation client :** Préparer 5 tables dans 2 zones. Créer 3 réservations pour le soir. Montrer la vue calendrier et le Kanban. Démontrer le workflow complet : réservation → confirmation → installation → fin. Insister sur la vision globale du planning.

---

### 3.21 restaurant_stock_alert

**Objectif :** Alertes de stock intelligent avec seuils minimum et suggestions de réapprovisionnement.

**Scénarios de test :**

| # | Scénario | Étapes | Résultat attendu |
|---|----------|--------|-------------------|
| 1 | Créer une règle d'alerte | Restaurant → Alertes stock → Règles → Créer | La règle est créée |
| 2 | Définir le seuil | Produit = "Tomates", Seuil = 10 kg | Le seuil est enregistré |
| 3 | Stock suffisant | Stock actuel = 20 kg | Pas d'alerte |
| 4 | Stock insuffisant | Réduire le stock à 5 kg | Une alerte est créée automatiquement |
| 5 | Suggestion de réapprovisionnement | Voir l'alerte | La quantité suggérée est affichée |
| 6 | Workflow d'alerte | Nouvelle → Prise en compte → Commandé → Résolu | Les statuts changent |
| 7 | Vue Pivot | Vue Pivot par produit/mois | L'analyse est affichée |

**Présentation client :** Configurer 3 règles pour des ingrédients clés. Simuler une baisse de stock. Montrer les alertes générées. Expliquer la prévention des ruptures et l'impact sur le service client.

---

### 3.22 restaurant_table_layout

**Objectif :** Plan de salle avec zones et statut des tables en temps réel.

**Scénarios de test :**

| # | Scénario | Étapes | Résultat attendu |
|---|----------|--------|-------------------|
| 1 | Créer une zone | Restaurant → Zones → Créer (Salle, Terrasse, Bar, VIP) | La zone est créée |
| 2 | Créer une table | Restaurant → Tables → Créer → Zone + Capacité + Forme | La table est créée |
| 3 | Statut "Libre" | Table nouvellement créée | Le statut est "Libre" (vert) |
| 4 | Statut "Occupée" | Changer le statut | Affichage en rouge |
| 5 | Statut "À nettoyer" | Changer le statut | Affichage en jaune |
| 6 | Statut "Fermée" | Changer le statut | Affichage en gris |
| 7 | Affecter un serveur | Table → Serveur | Le serveur est lié |
| 8 | Vue Kanban | Vue Kanban | Les tables sont groupées par zone |
| 9 | Statistiques de zone | Voir la zone | Capacité totale et tables disponibles |

**Présentation client :** Préparer 10 tables dans 3 zones. Montrer le Kanban coloré. Changer les statuts en temps réel. Montrer les statistiques par zone. Insister sur la vision opérationnelle pour le responsable de salle.

---

### 3.23 restaurant_tip_management

**Objectif :** Gestion des pourboires par employé avec suivi et reporting.

**Scénarios de test :**

| # | Scénario | Étapes | Résultat attendu |
|---|----------|--------|-------------------|
| 1 | Enregistrer un pourboire | Restaurant → Pourboires → Créer | Le formulaire s'affiche |
| 2 | Sources multiples | Créer des pourboires : espèces, carte, en ligne | Les 3 sources sont disponibles |
| 3 | Lier à une commande | Pourboire → Commande associée | La commande est liée |
| 4 | Valider | Pourboire → Valider | Le statut passe à "Validé" |
| 5 | Marquer comme payé | Pourboire → Payé | Le statut passe à "Payé" |
| 6 | Vue Pivot | Analyse → Pivot par employé/mois | Les totaux par employé sont affichés |
| 7 | Vue Graphique | Vue Graphique | L'évolution des pourboires est visible |

**Présentation client :** Enregistrer 10+ pourboires sur un mois pour 3 employés. Montrer le classement par employé. Montrer l'évolution dans le temps. Insister sur la transparence et l'équité dans la distribution.

---

### 3.24 restaurant_waste_tracking

**Objectif :** Suivi du gaspillage alimentaire avec analyse des coûts.

**Scénarios de test :**

| # | Scénario | Étapes | Résultat attendu |
|---|----------|--------|-------------------|
| 1 | Enregistrer un déchet | Restaurant → Gaspillage → Créer | Le formulaire s'affiche |
| 2 | Calcul du coût | Produit = Tomates (2€/kg), Quantité = 3 kg | Coût estimé = 6€ |
| 3 | Raisons multiples | Tester : périmé, abîmé, surproduction, préparation, autre | Toutes les raisons sont disponibles |
| 4 | Valider | Déchet → Valider | Le statut passe à "Validé" |
| 5 | Responsable | Affecter un employé responsable | L'employé est lié |
| 6 | Vue Pivot | Pivot par produit/raison/mois | Les coûts sont agrégés |
| 7 | Vue Graphique | Graphique d'évolution | Le trend est visible |

**Présentation client :** Préparer des données sur 1 mois avec différents produits et raisons. Montrer le coût total du gaspillage. Identifier les produits les plus gaspillés. Insister sur la conformité avec la loi anti-gaspillage et l'optimisation des achats.

---

### 3.25 server_environment_files

**Objectif :** Stockage des fichiers de configuration serveur.

**Scénarios de test :**

| # | Scénario | Étapes | Résultat attendu |
|---|----------|--------|-------------------|
| 1 | Installation | Installer le module | Installation sans erreur |
| 2 | Vérifier la configuration | Vérifier les paramètres OCA | Les fichiers sont accessibles |

**Présentation client :** Module technique interne. Expliquer brièvement qu'il assure la gestion sécurisée des configurations serveur.

---

### 3.26 shipday_odoo

**Objectif :** Intégration avec la plateforme de livraison Shipday.

**Scénarios de test :**

| # | Scénario | Étapes | Résultat attendu |
|---|----------|--------|-------------------|
| 1 | Configurer l'API | Paramètres → Shipday → Saisir clé API | La clé est enregistrée |
| 2 | Configurer le restaurant | Nom, adresse, téléphone du restaurant | Les infos sont enregistrées |
| 3 | Envoyer une commande | Commande → Bouton "Envoyer à Shipday" | Le champ `shipday_sent` = Vrai |
| 4 | Vérifier l'ID externe | Après envoi | L'ID Shipday est enregistré |
| 5 | Erreur API | Utiliser une clé invalide → Envoyer | Le message d'erreur est affiché dans `shipday_last_error` |
| 6 | Réessayer | Corriger → Réenvoyer | La commande est envoyée avec succès |
| 7 | Compatible avec les créneaux | Utiliser avec `restaurant_order_slots` | Le créneau horaire est transmis à Shipday |

**Présentation client :** Montrer le paramétrage en 2 minutes. Envoyer une commande. Montrer le suivi dans Odoo (envoyé, ID, erreurs). Expliquer l'automatisation du dispatch des livraisons.

---

### 3.27 supplier_vat_validation_final

**Objectif :** Gestion et validation des catégories TVA fournisseurs.

**Scénarios de test :**

| # | Scénario | Étapes | Résultat attendu |
|---|----------|--------|-------------------|
| 1 | Affecter une catégorie TVA | Contacts → Fournisseur → Catégorie TVA = "TVA 1" | La catégorie est enregistrée |
| 2 | Commande TVA 1 | Achat → Commande → Fournisseur TVA 1 → Confirmer | La commande est confirmée sans restriction |
| 3 | Commande TVA 2 (sous seuil) | Fournisseur TVA 2, total < 100 000€ annuel → Confirmer | La commande est confirmée |
| 4 | Commande TVA 2 (dépassement) | Fournisseur TVA 2, total > 100 000€ annuel → Confirmer | La confirmation est bloquée |
| 5 | Commande TVA 3 (sans validation) | Fournisseur TVA 3 → Confirmer sans validation RH | La confirmation est bloquée |
| 6 | Commande TVA 3 (avec validation) | Fournisseur TVA 3 → Valider par RH → Confirmer | La commande est confirmée |
| 7 | Bouton de validation | Utilisateur du groupe RH → Bouton "Valider" | Le flag `x_validated_by_ringeard` est activé |

**Présentation client :** Préparer 3 fournisseurs (un par catégorie). Montrer les scénarios de blocage pour TVA 2 et TVA 3. Montrer la validation RH. Expliquer la conformité fiscale et le contrôle interne.

---

### 3.28 trs_tools

**Objectif :** Outils TR Solutions pour le stockage de fichiers.

**Scénarios de test :**

| # | Scénario | Étapes | Résultat attendu |
|---|----------|--------|-------------------|
| 1 | Installation | Installer le module | Installation sans erreur |
| 2 | Configuration du stockage | Vérifier la configuration fs_storage | Le stockage est configuré |

**Présentation client :** Module technique interne. Mentionner brièvement comme infrastructure de gestion documentaire.

---

## 4. Stratégie de Présentation Client

### 4.1 Ordre de Présentation Recommandé

Présenter les modules par thème métier, du plus impactant au plus technique :

#### Phase 1 — Gestion du Restaurant (cœur de métier)
1. `restaurant_reservation` — Réservations
2. `restaurant_table_layout` — Plan de salle
3. `restaurant_daily_menu` — Menus du jour
4. `restaurant_order_slots` — Créneaux de commande
5. `restaurant_qrcode_menu` — QR Codes tables

#### Phase 2 — Opérations et Cuisine
6. `restaurant_kitchen_analytics` — Analytique cuisine
7. `restaurant_stock_alert` — Alertes stock
8. `restaurant_waste_tracking` — Suivi gaspillage
9. `allergen_auto` — Allergènes automatiques
10. `product_bom_filter` — Filtre nomenclatures

#### Phase 3 — Service et Fidélisation
11. `restaurant_customer_feedback` — Retours clients
12. `restaurant_loyalty_program` — Programme fidélité
13. `restaurant_happy_hour` — Happy Hours
14. `restaurant_tip_management` — Pourboires

#### Phase 4 — Ventes et Livraison
15. `employee_order_discount` — Remise employés
16. `shipday_odoo` — Intégration Shipday
17. `livreur` — Profil livreur
18. `restaurant_order_slots` — Créneaux (déjà vu, rappel e-commerce)

#### Phase 5 — Comptabilité et Achats
19. `account_manual_reconcile_v2` — Rapprochement
20. `supplier_vat_validation_final` — Validation TVA
21. `bi_reporting_advanced` — Rapports BI
22. `rapport_bi_redirect` — Power BI

#### Phase 6 — Ressources Humaines
23. `hr_shift_custom` — Gestion des shifts
24. `hr_employee_calendar_planning` — Planification calendriers
25. `hr_contract_custom` — Contrats personnalisés

#### Phase 7 — Technique et Validation
26. `custom_phone_validation` — Validation téléphone
27. `partner_phone_check` — Vérification téléphone commande
28. `server_environment_files` + `trs_tools` — Infrastructure

### 4.2 Format de Démonstration

Pour chaque module, suivre ce schéma en **5 minutes maximum** :

1. **Le problème** (30 sec) : "Aujourd'hui, vous faites X manuellement..."
2. **La solution** (30 sec) : "Ce module automatise X..."
3. **Démonstration live** (3 min) : Parcours complet du flux principal
4. **Bénéfices** (1 min) : Gain de temps, conformité, traçabilité

### 4.3 Données de Démonstration à Préparer

| Données | Quantité | Utilisées par |
|---------|----------|---------------|
| Clients | 10 (dont 2 employés) | Commandes, fidélité, feedbacks |
| Produits alimentaires | 20 (avec prix) | Menus, allergènes, stocks, gaspillage |
| Matières premières | 15 (avec allergènes) | Nomenclatures, allergènes |
| Nomenclatures | 10 recettes | Allergènes, filtre BoM |
| Employés | 5 (dont 1 livreur) | Shifts, pourboires, planning |
| Tables de restaurant | 10 (3 zones) | Réservations, plan de salle |
| Commandes de vente | 20 (sur 3 mois) | Rapports BI, créneaux, remises |
| Commandes d'achat | 10 (3 fournisseurs) | Validation TVA |
| Factures | 15 | Rapports, rapprochement |

### 4.4 Conseils pour la Présentation

- **Utiliser 2 navigateurs** : Un pour l'admin, un pour le livreur/employé
- **Préparer les données à l'avance** : Ne pas saisir devant le client
- **Montrer les vues Kanban et Calendrier** : Plus visuelles que les listes
- **Montrer les PDF** : Toujours impressionnant pour les non-techniques
- **Préparer un QR Code réel** : Le scanner en live
- **Montrer le site web e-commerce** : Commande client avec créneau
- **Terminer par les rapports** : Vue d'ensemble avec les tableaux croisés et graphiques

---

## 5. Checklist Pré-Démonstration

### Installation
- [ ] Base de données propre créée
- [ ] Tous les modules installés sans erreur
- [ ] Données de démonstration chargées

### Configuration
- [ ] Étiquette "Employé" créée
- [ ] Règles de shift configurées (11h pause, 10h max)
- [ ] Seuils d'alerte stock définis
- [ ] Clé API Shipday configurée (ou simulée)
- [ ] QR Codes générés pour 3 tables
- [ ] Catégories TVA fournisseurs affectées

### Données
- [ ] 10 clients créés
- [ ] 20 produits avec prix
- [ ] 10 nomenclatures (recettes)
- [ ] Allergènes affectés aux matières premières
- [ ] 5 employés créés
- [ ] 10 tables en 3 zones
- [ ] 20 commandes confirmées
- [ ] 10 feedbacks clients
- [ ] 5 réservations
- [ ] 10 shifts planifiés
- [ ] 5 enregistrements de gaspillage
- [ ] Quelques pourboires enregistrés
- [ ] Carte de fidélité avec historique

### Vérification Technique
- [ ] Tous les menus sont accessibles
- [ ] Les vues (List, Form, Kanban, Calendar, Pivot, Graph) s'affichent
- [ ] Les workflows (statuts) fonctionnent
- [ ] Les calculs automatiques sont corrects
- [ ] Le site web e-commerce fonctionne
- [ ] Les PDF se génèrent
- [ ] L'utilisateur livreur a les bonnes restrictions
