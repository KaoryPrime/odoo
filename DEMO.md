# Guide de démonstration des modules

---

## 🍽️ Modules Restaurant

### restaurant_table_layout — Plan de salle
1. Aller dans **Restaurant > Plan de salle > Zones**
2. Créer une zone (ex : « Terrasse », capacité 20)
3. Créer 2 tables dans cette zone (forme, capacité, statut « Libre »)
4. Ouvrir la vue **Kanban** → vérifier les couleurs par statut (libre / occupée)
5. Changer le statut d'une table en « Occupée » → la couleur change en temps réel

### restaurant_reservation — Réservations
1. Aller dans **Restaurant > Réservations > Nouvelle réservation**
2. Saisir client, date, créneau horaire, nombre de couverts, table
3. Passer le statut à **Confirmée** puis **Installée**
4. Ouvrir la vue **Calendrier** → vérifier que la réservation apparaît
5. Passer en **Terminée** → statut archivé automatiquement

### restaurant_daily_menu — Menu du jour
1. Aller dans **Restaurant > Menu du jour > Nouveau**
2. Choisir un type de service (Déjeuner / Dîner / Brunch)
3. Ajouter 3 lignes de plats avec catégorie, prix et disponibilité
4. Activer la **planification semaine** et cocher les jours
5. Sauvegarder → vérifier le récapitulatif en Form view

### restaurant_happy_hour — Happy Hour
1. Aller dans **Restaurant > Happy Hour > Nouveau**
2. Définir un créneau horaire (ex : 17h–19h) pour un jour de semaine
3. Ajouter des produits avec remise en % ou montant fixe
4. Créer une commande de vente à l'heure du créneau → la remise s'applique automatiquement
5. Vérifier le prix remisé calculé sur chaque ligne produit

### restaurant_order_slots — Créneaux de commande
1. Sur le **webshop**, ajouter un article au panier et aller au paiement
2. Vérifier l'affichage du bloc **Type de commande** (Livraison / À emporter) et du **créneau horaire**
3. Sélectionner un créneau et valider la commande
4. En backend, ouvrir la commande → vérifier que le créneau et le type sont enregistrés
5. Imprimer le bon de commande → vérifier la présence du créneau sur le PDF

### restaurant_qrcode_menu — QR Code Menu
1. Aller dans **Restaurant > QR Code Menu > Nouvelle table**
2. Saisir le nom de la table et l'URL du menu en ligne
3. Sauvegarder → le QR code est généré automatiquement
4. Cliquer sur **Télécharger QR Code** → scanner avec un smartphone
5. Vérifier que le scan redirige vers le bon menu et incrémente le compteur de scans

### restaurant_kitchen_analytics — Analytique cuisine
1. Aller dans **Restaurant > Analytique cuisine > Nouveau**
2. Saisir un produit, la date/heure de commande et la date/heure de livraison
3. Sauvegarder → la durée de préparation est calculée automatiquement
4. Ouvrir la vue **Pivot** → analyser les durées moyennes par produit
5. Ouvrir la vue **Graphique** → visualiser les écarts entre qté commandée et livrée

### restaurant_customer_feedback — Avis clients
1. Aller dans **Restaurant > Avis clients > Nouveau**
2. Choisir la source (Sur place / Google / Web) et noter les 4 critères (plats, service, ambiance, rapport qualité-prix)
3. Sauvegarder → la note globale est calculée automatiquement
4. Changer le statut en **Lu** puis **Répondu**
5. Ouvrir la vue **Graphique** → vérifier la distribution des notes

### restaurant_loyalty_program — Programme fidélité
1. Aller dans **Contacts > Clients** et ouvrir une fiche client
2. Vérifier l'onglet **Fidélité** : points actuels et niveau de fidélité
3. Créer une commande de vente pour ce client et la valider
4. Retourner sur la fiche client → les points ont augmenté
5. Ouvrir **Restaurant > Fidélité** → visualiser toutes les cartes de fidélité

### restaurant_tip_management — Gestion des pourboires
1. Aller dans **Restaurant > Pourboires > Nouveau**
2. Lier à une commande de vente, saisir le montant et le mode (Espèces / Carte / En ligne)
3. Ajouter les employés bénéficiaires avec leur part
4. Sauvegarder → la distribution automatique est calculée
5. Ouvrir la vue **Pivot** → analyser les pourboires par employé et par période

### restaurant_waste_tracking — Suivi des pertes
1. Aller dans **Restaurant > Pertes alimentaires > Nouvelle perte**
2. Choisir un produit, la quantité perdue et la raison
3. Sauvegarder → le coût est calculé automatiquement (prix standard × quantité)
4. Cliquer sur **Valider** → passe en statut Validé
5. Ouvrir la vue **Pivot** → analyser les pertes par produit et par mois

### restaurant_stock_alert — Alertes de stock
1. Aller dans **Restaurant > Alertes stock > Nouvelle règle**
2. Choisir un produit et définir le seuil minimum et la quantité de réapprovisionnement
3. Diminuer le stock du produit en dessous du seuil
4. Ouvrir **Alertes stock > Lignes d'alerte** → vérifier qu'une alerte « Nouveau » est créée
5. Passer l'alerte en **Accusé réception** puis **Commandé** puis **Résolu**

---

## 👥 Modules RH

### hr_shift_custom — Gestion des shifts
1. Aller dans **RH > Shifts > Configuration** → définir les règles (pause min, durée max journée)
2. Aller dans **RH > Shifts > Nouveau shift** → choisir un employé, date, heure début/fin
3. Sauvegarder → vérification automatique des règles (alerte si dépassement)
4. Ouvrir la vue **Calendrier** → visualiser les shifts de l'équipe
5. Ouvrir le **Tableau de bord** → vérifier les statistiques (heures totales, alertes)

### hr_employee_calendar_planning — Planning calendrier
1. Aller dans **RH > Employés** et ouvrir un employé
2. Aller dans l'onglet **Travail** → modifier le calendrier de travail
3. Aller dans **RH > Planning** → visualiser le calendrier de l'employé
4. Créer une entrée de travail et sauvegarder
5. Vérifier la synchronisation avec le calendrier de ressource

### hr_contract_custom — Contrats RH
1. Aller dans **RH > Contrats > Nouveau contrat**
2. Remplir les champs requis (employé, date début, salaire)
3. Sauvegarder et cliquer sur **Imprimer**
4. Vérifier que le PDF généré contient les informations du contrat avec la mise en page personnalisée

---

## 💰 Modules Ventes / Commandes

### employee_order_discount — Remise employé
1. Créer un client avec le tag **Employé**
2. Créer une commande de vente pour ce client (si moins de 2 commandes ce mois)
3. Vérifier que la remise à 100 % est appliquée automatiquement sur la commande
4. Créer 2 commandes pour le même employé → la 3e n'a plus de remise automatique

### livreur — Accès livreur
1. Se connecter avec un compte ayant le rôle **Livreur**
2. Vérifier que seul le menu **Commandes de vente** est visible dans le module Ventes
3. Tenter d'accéder à d'autres menus → accès refusé

### partner_phone_check — Validation téléphone (commande)
1. Créer un client **sans numéro de téléphone** (ou avec un numéro invalide)
2. Créer une commande de vente et tenter de la **Confirmer**
3. Vérifier qu'un message d'erreur bloque la confirmation
4. Corriger le numéro → la confirmation passe

### custom_phone_validation — Validation téléphone (webshop)
1. Sur le **webshop**, créer un compte avec un numéro de téléphone incorrect (ex : 8 chiffres)
2. Vérifier que le formulaire est bloqué avec un message d'erreur
3. Saisir un numéro valide (10 chiffres commençant par 0) → le formulaire est accepté

---

## 📊 Modules Comptabilité / Reporting

### account_manual_reconcile_v2 — Lettrage manuel
1. Aller dans **Comptabilité > Opérations > Lettrage manuel**
2. Sélectionner un compte (ex : compte client 411)
3. Cocher une facture et un paiement correspondant
4. Cliquer sur **Lettrer** → les deux lignes disparaissent de la liste
5. Vérifier dans la pièce comptable que le lettrage est indiqué

### bi_reporting_advanced — Reporting BI avancé
1. Aller dans **Reporting > BI Avancé**
2. Ouvrir le rapport **Ventes** → vérifier les données agrégées
3. Ouvrir le rapport **Facturation** → vérifier les totaux
4. Ouvrir le rapport **Stocks** → vérifier les mouvements
5. Vérifier les automatisations (cron) dans **Paramètres > Techniques > Actions planifiées**

### rapport_bi_redirect — Rapports Power BI
1. Aller dans **Reporting > Rapports BI**
2. Ouvrir le rapport **Stocks** → vérifier la redirection vers Power BI
3. Ouvrir le rapport **Facturation** → vérifier la redirection
4. Ouvrir le rapport **Inventaire** → vérifier la redirection

---

## 🛒 Modules Produits / Fournisseurs

### allergen_auto — Allergènes automatiques
1. Aller dans **Fabrication > Produits > Matières premières** → ouvrir un produit
2. Dans l'onglet **Allergènes**, cocher les allergènes présents (ex : Gluten, Lait)
3. Aller sur un **produit fini** lié par une nomenclature (BOM)
4. Vérifier que l'onglet **Allergènes** du produit fini liste automatiquement les allergènes des composants
5. Ouvrir la fiche produit sur le **webshop** → vérifier l'affichage des allergènes

### product_bom_filter — Filtre BOM produits
1. Aller dans **Fabrication > Produits > Produits**
2. Dans les filtres, sélectionner **Avec nomenclature** → seuls les produits avec BOM s'affichent
3. Sélectionner **Sans nomenclature** → seuls les produits sans BOM s'affichent
4. Vérifier le compteur de résultats dans les deux cas

### supplier_vat_validation_final — Validation TVA fournisseur
1. Aller dans **Achats > Fournisseurs** → ouvrir une fiche fournisseur
2. Saisir un numéro de TVA invalide → un message d'erreur apparaît
3. Saisir un numéro de TVA valide (ex : FR12345678901) → validation acceptée
4. Créer un bon de commande fournisseur → vérifier que le numéro de TVA est affiché

---

## 🚚 Modules Intégration / Livraison

### shipday_odoo — Intégration Shipday
1. Aller dans **Paramètres > Shipday** → saisir la clé API et les infos restaurant
2. Créer une commande de vente avec un **type Livraison** (module restaurant_order_slots)
3. Confirmer la commande → un bouton **Envoyer à Shipday** apparaît
4. Cliquer sur **Envoyer à Shipday** → vérifier le statut **Envoyé** et le log dans le chatter
5. En cas d'erreur, cliquer sur **Renvoyer** → nouvelle tentative tracée dans le chatter
