# Guide de déploiement Streamlit in Snowflake

## 🚀 Déploiement de l'application

### Prérequis
- Compte Snowflake avec Streamlit activé
- Base de données `HOUSE_PRICE_DB` créée
- Schémas `BRONZE`, `SILVER`, `GOLD`, `ML` configurés
- Modèle `HOUSE_PRICE_PREDICTOR` déployé dans le registry

### Étapes de déploiement

1. **Connexion à Snowflake**
   - Ouvrez votre navigateur et connectez-vous à Snowflake

2. **Accès à Streamlit**
   - Dans le menu latéral, cliquez sur "Projects"
   - Sélectionnez "Streamlit"

3. **Création de l'application**
   - Cliquez sur le bouton "+ Streamlit App"
   - Donnez un nom à votre application (ex: "Prédiction Prix Immobilier")

4. **Import du code**
   - Copiez le contenu de `streamlit_Final_work.py`
   - Collez-le dans l'éditeur Streamlit

5. **Configuration**
   - Dans les paramètres, sélectionnez :
     - Database: `HOUSE_PRICE_DB`
     - Schema: `ML` (ou selon votre configuration)
   - Assurez-vous que les permissions sont correctes

6. **Publication**
   - Cliquez sur "Deploy" ou "Publish"
   - Snowflake génère automatiquement une URL publique

### Test de l'application

Une fois déployée, l'application sera accessible via une URL Snowflake.
Les utilisateurs pourront saisir les caractéristiques d'une maison et obtenir une estimation de prix en temps réel.

### Dépannage

Si l'application ne fonctionne pas :
- Vérifiez que le modèle est bien déployé dans le registry
- Contrôlez les permissions d'accès aux tables
- Assurez-vous que les schémas existent

### URL d'accès

Après déploiement, Snowflake fournit une URL du type :
`https://[account].snowflakecomputing.com/streamlit-apps/[app-id]`

---

*Ce guide est spécifique à votre projet de prédiction immobilière avec Snowflake.*