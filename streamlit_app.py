"""
============================================================
🏠 Prédiction des Prix Immobiliers — Édition Premium
Application Streamlit in Snowflake (SiS)
============================================================
Compatible Snowflake Streamlit : utilise uniquement les
bibliothèques disponibles nativement dans SiS
(streamlit, pandas, plotly, snowflake.snowpark).
============================================================
"""

import streamlit as st
from snowflake.snowpark.context import get_active_session
import pandas as pd
import json
import plotly.graph_objects as go
import plotly.express as px

# ============================================================
# Configuration de la page
# ============================================================
st.set_page_config(
    page_title="Real Estate AI — Estimation Premium",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# Design System — CSS sophistiqué (glassmorphism + dégradés)
# ============================================================
st.markdown(
    """
<style>
    /* ---------- Reset & global ---------- */
    .stApp {
        background:
            radial-gradient(circle at 15% 20%, rgba(99,102,241,0.15) 0%, transparent 45%),
            radial-gradient(circle at 85% 80%, rgba(236,72,153,0.12) 0%, transparent 45%),
            linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #e2e8f0;
    }

    /* Cache la barre du haut Streamlit pour un look plus app */
    header[data-testid="stHeader"] { background: transparent; }
    #MainMenu, footer { visibility: hidden; }

    /* ---------- Hero ---------- */
    .hero {
        background: linear-gradient(135deg, rgba(99,102,241,0.25) 0%, rgba(236,72,153,0.20) 100%);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 24px;
        padding: 2.5rem 2rem;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 20px 60px -20px rgba(99,102,241,0.4);
    }
    .hero h1 {
        font-size: 3rem;
        font-weight: 800;
        margin: 0;
        background: linear-gradient(90deg, #a5b4fc, #f9a8d4, #fbbf24);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -0.02em;
    }
    .hero p {
        color: #cbd5e1;
        font-size: 1.1rem;
        margin-top: 0.5rem;
        font-weight: 300;
    }
    .hero .badge {
        display: inline-block;
        margin-top: 1rem;
        padding: 0.4rem 1rem;
        background: rgba(16,185,129,0.15);
        border: 1px solid rgba(16,185,129,0.4);
        border-radius: 999px;
        color: #6ee7b7;
        font-size: 0.85rem;
        font-weight: 500;
    }

    /* ---------- Glass cards ---------- */
    .glass-card {
        background: rgba(255,255,255,0.04);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 18px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    .glass-card:hover {
        border-color: rgba(165,180,252,0.4);
        transform: translateY(-2px);
        box-shadow: 0 12px 40px -10px rgba(99,102,241,0.3);
    }
    .glass-card h4 {
        color: #a5b4fc;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin: 0 0 1rem 0;
        font-weight: 600;
    }

    /* ---------- Section headers ---------- */
    .section-title {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        font-size: 1.4rem;
        font-weight: 700;
        color: #f1f5f9;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid rgba(255,255,255,0.1);
    }
    .section-title .icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 38px; height: 38px;
        background: linear-gradient(135deg, #6366f1, #ec4899);
        border-radius: 10px;
        font-size: 1.2rem;
    }

    /* ---------- Result hero ---------- */
    .price-hero {
        background: linear-gradient(135deg, rgba(16,185,129,0.18) 0%, rgba(99,102,241,0.18) 100%);
        border: 1px solid rgba(110,231,183,0.35);
        border-radius: 24px;
        padding: 2.5rem;
        text-align: center;
        margin: 1.5rem 0;
        box-shadow: 0 20px 60px -20px rgba(16,185,129,0.4);
    }
    .price-hero .label {
        color: #94a3b8;
        text-transform: uppercase;
        font-size: 0.8rem;
        letter-spacing: 0.15em;
        margin-bottom: 0.5rem;
    }
    .price-hero .value {
        font-size: 4rem;
        font-weight: 800;
        background: linear-gradient(90deg, #6ee7b7, #a5b4fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1;
        letter-spacing: -0.03em;
    }
    .price-hero .sub {
        color: #cbd5e1;
        margin-top: 0.75rem;
        font-size: 1rem;
    }

    /* ---------- Sidebar styling ---------- */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
        border-right: 1px solid rgba(255,255,255,0.06);
    }
    section[data-testid="stSidebar"] .stMarkdown {
        color: #cbd5e1;
    }

    /* ---------- Buttons ---------- */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #ec4899 100%);
        color: white;
        border: none;
        border-radius: 14px;
        padding: 0.85rem 1.5rem;
        font-weight: 600;
        font-size: 1.05rem;
        letter-spacing: 0.02em;
        transition: all 0.3s ease;
        box-shadow: 0 8px 24px -8px rgba(99,102,241,0.6);
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 14px 32px -8px rgba(236,72,153,0.6);
        filter: brightness(1.1);
    }

    /* ---------- Inputs ---------- */
    .stSlider [data-baseweb="slider"] > div > div > div {
        background: linear-gradient(90deg, #6366f1, #ec4899) !important;
    }
    .stSelectbox > div > div, .stRadio > div {
        background-color: rgba(255,255,255,0.04) !important;
        border-radius: 10px !important;
    }

    /* ---------- Metric override ---------- */
    [data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
        font-weight: 700 !important;
        color: #f1f5f9 !important;
    }
    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-size: 0.8rem !important;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    /* ---------- Tabs ---------- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255,255,255,0.03);
        padding: 6px;
        border-radius: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #94a3b8;
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #6366f1, #ec4899) !important;
        color: white !important;
    }

    /* ---------- Footer ---------- */
    .footer {
        text-align: center;
        color: #64748b;
        font-size: 0.85rem;
        padding: 2rem 0 1rem 0;
        margin-top: 3rem;
        border-top: 1px solid rgba(255,255,255,0.06);
    }
    .footer .pill {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        background: rgba(99,102,241,0.15);
        border-radius: 999px;
        margin: 0 0.25rem;
        color: #a5b4fc;
    }
</style>
""",
    unsafe_allow_html=True,
)

# ============================================================
# Connexion Snowflake
# ============================================================
try:
    session = get_active_session()
except Exception as e:
    st.error(f"❌ Erreur de connexion à Snowflake : {e}")
    st.stop()

# ============================================================
# Helpers
# ============================================================
@st.cache_data(ttl=300, show_spinner=False)
def load_dataset_stats():
    """Charge les statistiques globales du dataset."""
    return session.sql(
        """
        SELECT
            COUNT(*)            AS TOTAL_MAISONS,
            AVG(PRIX)           AS PRIX_MOYEN,
            MIN(PRIX)           AS PRIX_MIN,
            MAX(PRIX)           AS PRIX_MAX,
            MEDIAN(PRIX)        AS PRIX_MEDIAN,
            STDDEV(PRIX)        AS PRIX_STD,
            PERCENTILE_CONT(0.33) WITHIN GROUP (ORDER BY PRIX) AS P33,
            PERCENTILE_CONT(0.66) WITHIN GROUP (ORDER BY PRIX) AS P66
        FROM HOUSE_PRICE_DB.GOLD.HOUSE_PRICES
        """
    ).to_pandas()


@st.cache_data(ttl=300, show_spinner=False)
def load_price_distribution():
    """Charge un échantillon de prix pour les visualisations."""
    return session.sql(
        "SELECT PRIX, SURFACE FROM HOUSE_PRICE_DB.GOLD.HOUSE_PRICES"
    ).to_pandas()


def fmt_eur(v):
    return f"{v:,.0f} €".replace(",", " ")


# ============================================================
# Sidebar — Tableau de bord
# ============================================================
with st.sidebar:
    st.markdown(
        """
        <div style="text-align:center; padding:1rem 0 1.5rem 0;">
          <div style="font-size:2.5rem;">🏠</div>
          <div style="font-size:1.2rem; font-weight:700; color:#f1f5f9;">Real Estate AI</div>
          <div style="font-size:0.75rem; color:#64748b; letter-spacing:0.15em; text-transform:uppercase;">
            Predictive Suite v2.0
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("##### 🤖 À propos du modèle")
    st.markdown(
        """
        <div style="background:rgba(99,102,241,0.08); border-left:3px solid #6366f1;
                    padding:0.85rem 1rem; border-radius:8px; font-size:0.85rem; line-height:1.5;">
          <b style="color:#a5b4fc;">Gradient Boosting</b> entraîné sur
          <b>1 090 transactions</b> immobilières.<br>
          <span style="color:#6ee7b7;">⬤ R² = 0.901</span> · MAE faible · Production-ready.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("##### 📊 Marché en chiffres")
    try:
        stats = load_dataset_stats()
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Maisons", f"{int(stats['TOTAL_MAISONS'].values[0]):,}".replace(",", " "))
            st.metric("Prix min", fmt_eur(stats["PRIX_MIN"].values[0]))
        with c2:
            st.metric("Prix moyen", fmt_eur(stats["PRIX_MOYEN"].values[0]))
            st.metric("Prix max", fmt_eur(stats["PRIX_MAX"].values[0]))
    except Exception:
        st.warning("Statistiques du dataset indisponibles")
        stats = None

    st.markdown("---")
    st.caption("💡 Astuce : ajustez les caractéristiques puis lancez l'estimation pour comparer le bien au marché.")


# ============================================================
# Hero
# ============================================================
st.markdown(
    """
<div class="hero">
  <h1>🏠 Estimation Immobilière Intelligente</h1>
  <p>Renseignez les caractéristiques du bien — notre modèle ML calcule un prix de marché en quelques secondes.</p>
  <span class="badge">⚡ Powered by Snowflake ML · Gradient Boosting · R² 0.901</span>
</div>
""",
    unsafe_allow_html=True,
)

# ============================================================
# Validation
# ============================================================
def validate_inputs(surface, chambres, salles_de_bain, etages, parking):
    errors = []
    if surface < 10 or surface > 1000:
        errors.append("La surface doit être comprise entre 10 et 1000 m²")
    if chambres < 1 or chambres > 10:
        errors.append("Le nombre de chambres doit être compris entre 1 et 10")
    if salles_de_bain < 1 or salles_de_bain > 6:
        errors.append("Le nombre de salles de bain doit être compris entre 1 et 6")
    if etages < 1 or etages > 5:
        errors.append("Le nombre d'étages doit être compris entre 1 et 5")
    if parking < 0 or parking > 5:
        errors.append("Le nombre de places de parking doit être compris entre 0 et 5")
    return errors


# ============================================================
# Formulaire — onglets
# ============================================================
st.markdown(
    '<div class="section-title"><span class="icon">📝</span> Caractéristiques du bien</div>',
    unsafe_allow_html=True,
)

tab1, tab2, tab3 = st.tabs(["📐 Dimensions", "🏗️ Structure", "🌟 Confort & Emplacement"])

with tab1:
    c1, c2, c3 = st.columns(3)
    with c1:
        surface = st.slider("Surface habitable (m²)", 10, 600, 150, 5,
                            help="Surface totale habitable")
    with c2:
        chambres = st.selectbox("🛏️ Chambres", list(range(1, 11)), index=2)
    with c3:
        salles_de_bain = st.selectbox("🛁 Salles de bain", list(range(1, 7)), index=0)

with tab2:
    c1, c2, c3 = st.columns(3)
    with c1:
        etages = st.selectbox("🏢 Étages", list(range(1, 6)), index=0)
    with c2:
        parking = st.selectbox("🚗 Places de parking", list(range(0, 6)), index=0)
    with c3:
        sous_sol = st.radio("🏚️ Sous-sol", ["Oui", "Non"], index=1, horizontal=True)

with tab3:
    c1, c2, c3 = st.columns(3)
    with c1:
        route_principale = st.radio("🛣️ Route principale", ["Oui", "Non"], index=0, horizontal=True)
        chambre_amis = st.radio("🛋️ Chambre d'amis", ["Oui", "Non"], index=1, horizontal=True)
    with c2:
        chauffage = st.radio("🔥 Chauffage eau chaude", ["Oui", "Non"], index=1, horizontal=True)
        climatisation = st.radio("❄️ Climatisation", ["Oui", "Non"], index=1, horizontal=True)
    with c3:
        zone_privilegiee = st.radio("⭐ Zone privilégiée", ["Oui", "Non"], index=1, horizontal=True)
        ameublement = st.selectbox("🪑 Ameublement",
                                   ["Non meublée", "Semi-meublée", "Meublée"], index=1)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================
# Bouton CTA
# ============================================================
cta_col1, cta_col2, cta_col3 = st.columns([1, 2, 1])
with cta_col2:
    predict_btn = st.button("🔮  Estimer le prix du bien", type="primary", use_container_width=True)

# ============================================================
# Prédiction
# ============================================================
if predict_btn:
    errors = validate_inputs(surface, chambres, salles_de_bain, etages, parking)
    if errors:
        for e in errors:
            st.error(e)
    else:
        ameublement_map = {"Meublée": 2, "Semi-meublée": 1, "Non meublée": 0}
        input_data = pd.DataFrame([{
            "SURFACE": float(surface),
            "CHAMBRES": int(chambres),
            "SALLES_DE_BAIN": int(salles_de_bain),
            "ETAGES": int(etages),
            "ROUTE_PRINCIPALE": 1 if route_principale == "Oui" else 0,
            "CHAMBRE_AMIS": 1 if chambre_amis == "Oui" else 0,
            "SOUS_SOL": 1 if sous_sol == "Oui" else 0,
            "CHAUFFAGE_EAU_CHAUDE": 1 if chauffage == "Oui" else 0,
            "CLIMATISATION": 1 if climatisation == "Oui" else 0,
            "PARKING": int(parking),
            "ZONE_PRIVILEGIEE": 1 if zone_privilegiee == "Oui" else 0,
            "STATUT_AMEUBLEMENT_ENC": int(ameublement_map[ameublement]),
        }])

        with st.spinner("🧠 Le modèle analyse votre bien…"):
            try:
                session.create_dataframe(input_data).create_or_replace_temp_view("INPUT_TEMP")

                result = session.sql(
                    """
                    SELECT HOUSE_PRICE_DB.ML.HOUSE_PRICE_PREDICTOR!PREDICT(
                        SURFACE, CHAMBRES, SALLES_DE_BAIN, ETAGES,
                        ROUTE_PRINCIPALE, CHAMBRE_AMIS, SOUS_SOL,
                        CHAUFFAGE_EAU_CHAUDE, CLIMATISATION, PARKING,
                        ZONE_PRIVILEGIEE, STATUT_AMEUBLEMENT_ENC
                    ) AS PREDICTION
                    FROM INPUT_TEMP
                    """
                ).to_pandas()

                prediction_raw = result["PREDICTION"].values[0]
                prix_predit = float(json.loads(prediction_raw)["output_feature_0"])

                # Stats
                if stats is None:
                    stats = load_dataset_stats()
                prix_moyen = float(stats["PRIX_MOYEN"].values[0])
                prix_median = float(stats["PRIX_MEDIAN"].values[0])
                prix_min = float(stats["PRIX_MIN"].values[0])
                prix_max = float(stats["PRIX_MAX"].values[0])
                p33 = float(stats["P33"].values[0])
                p66 = float(stats["P66"].values[0])

                diff_pct = ((prix_predit - prix_moyen) / prix_moyen) * 100
                prix_m2 = prix_predit / surface

                if prix_predit < p33:
                    gamme, gamme_icon, gamme_color = "Entrée de gamme", "🟢", "#10b981"
                elif prix_predit < p66:
                    gamme, gamme_icon, gamme_color = "Milieu de gamme", "🟡", "#f59e0b"
                else:
                    gamme, gamme_icon, gamme_color = "Haut de gamme", "🔴", "#ef4444"

                # ----- Résultat hero -----
                st.markdown(
                    f"""
                    <div class="price-hero">
                        <div class="label">💎 Estimation du modèle</div>
                        <div class="value">{fmt_eur(prix_predit)}</div>
                        <div class="sub">soit <b>{fmt_eur(prix_m2)}/m²</b> · Catégorie : <b style="color:{gamme_color};">{gamme_icon} {gamme}</b></div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                # ----- KPI -----
                k1, k2, k3, k4 = st.columns(4)
                with k1:
                    st.metric("vs. Prix moyen", fmt_eur(prix_moyen), f"{diff_pct:+.1f}%")
                with k2:
                    st.metric("vs. Prix médian", fmt_eur(prix_median),
                              f"{((prix_predit - prix_median) / prix_median) * 100:+.1f}%")
                with k3:
                    st.metric("Prix au m²", fmt_eur(prix_m2))
                with k4:
                    st.metric("Confiance modèle", "90.1 %", "R²")

                st.markdown("<br>", unsafe_allow_html=True)

                # ----- Visualisations -----
                viz_tab1, viz_tab2, viz_tab3 = st.tabs(
                    ["📊 Positionnement marché", "📈 Distribution", "📋 Récapitulatif"]
                )

                with viz_tab1:
                    # Jauge plotly
                    fig_gauge = go.Figure(go.Indicator(
                        mode="gauge+number+delta",
                        value=prix_predit,
                        number={"prefix": "", "suffix": " €",
                                "valueformat": ",.0f", "font": {"color": "#f1f5f9", "size": 36}},
                        delta={"reference": prix_moyen, "relative": True,
                               "valueformat": ".1%",
                               "increasing": {"color": "#ef4444"},
                               "decreasing": {"color": "#10b981"}},
                        gauge={
                            "axis": {"range": [prix_min, prix_max],
                                     "tickcolor": "#94a3b8",
                                     "tickformat": ",.0f"},
                            "bar": {"color": "rgba(165,180,252,0.9)", "thickness": 0.25},
                            "bgcolor": "rgba(255,255,255,0.05)",
                            "borderwidth": 0,
                            "steps": [
                                {"range": [prix_min, p33], "color": "rgba(16,185,129,0.35)"},
                                {"range": [p33, p66], "color": "rgba(245,158,11,0.35)"},
                                {"range": [p66, prix_max], "color": "rgba(239,68,68,0.35)"},
                            ],
                            "threshold": {
                                "line": {"color": "#ec4899", "width": 4},
                                "thickness": 0.85,
                                "value": prix_predit,
                            },
                        },
                        title={"text": "Position sur le marché",
                               "font": {"color": "#cbd5e1", "size": 16}},
                    ))
                    fig_gauge.update_layout(
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        font={"color": "#e2e8f0"},
                        height=380,
                        margin=dict(l=20, r=20, t=60, b=20),
                    )
                    st.plotly_chart(fig_gauge, use_container_width=True)

                with viz_tab2:
                    try:
                        df_dist = load_price_distribution()
                        fig_hist = px.histogram(
                            df_dist, x="PRIX", nbins=40,
                            color_discrete_sequence=["#6366f1"],
                            opacity=0.85,
                        )
                        fig_hist.add_vline(
                            x=prix_predit, line_dash="dash", line_color="#ec4899",
                            line_width=3,
                            annotation_text=f"Votre bien : {fmt_eur(prix_predit)}",
                            annotation_position="top",
                            annotation_font_color="#ec4899",
                        )
                        fig_hist.add_vline(
                            x=prix_moyen, line_dash="dot", line_color="#fbbf24",
                            annotation_text="Moyenne marché",
                            annotation_position="bottom",
                            annotation_font_color="#fbbf24",
                        )
                        fig_hist.update_layout(
                            paper_bgcolor="rgba(0,0,0,0)",
                            plot_bgcolor="rgba(0,0,0,0)",
                            font={"color": "#e2e8f0"},
                            xaxis={"title": "Prix (€)", "gridcolor": "rgba(255,255,255,0.08)"},
                            yaxis={"title": "Nombre de biens", "gridcolor": "rgba(255,255,255,0.08)"},
                            height=380,
                            margin=dict(l=20, r=20, t=30, b=40),
                            title="Distribution des prix sur le marché",
                        )
                        st.plotly_chart(fig_hist, use_container_width=True)
                    except Exception as exc:
                        st.info(f"Distribution indisponible : {exc}")

                with viz_tab3:
                    recap_data = {
                        "Caractéristique": [
                            "Surface", "Chambres", "Salles de bain", "Étages", "Parking",
                            "Route principale", "Chambre d'amis", "Sous-sol",
                            "Chauffage eau chaude", "Climatisation",
                            "Zone privilégiée", "Ameublement",
                        ],
                        "Valeur": [
                            f"{surface} m²", chambres, salles_de_bain, etages, parking,
                            route_principale, chambre_amis, sous_sol,
                            chauffage, climatisation, zone_privilegiee, ameublement,
                        ],
                    }
                    st.dataframe(pd.DataFrame(recap_data),
                                 use_container_width=True, hide_index=True)

                with st.expander("ℹ️ Détails techniques de l'estimation"):
                    st.markdown(
                        f"""
                        - **Modèle** : Gradient Boosting Regressor (Snowflake ML)
                        - **Précision (R²)** : 0.901
                        - **Échantillon d'entraînement** : 1 090 transactions
                        - **Référence marché** : {fmt_eur(prix_moyen)} (moyenne) · {fmt_eur(prix_median)} (médiane)
                        - **Bornes** : min {fmt_eur(prix_min)} · max {fmt_eur(prix_max)}
                        - **Segmentation** : percentiles 33 % ({fmt_eur(p33)}) et 66 % ({fmt_eur(p66)})
                        """
                    )

            except Exception as e:
                st.error(f"❌ Erreur lors de la prédiction : {e}")
                st.info("Vérifiez que le modèle `HOUSE_PRICE_DB.ML.HOUSE_PRICE_PREDICTOR` est déployé.")

# ============================================================
# Footer
# ============================================================
st.markdown(
    """
<div class="footer">
    <span class="pill">Streamlit in Snowflake</span>
    <span class="pill">ML Gradient Boosting</span>
    <span class="pill">Plotly</span>
    <br><br>
    © 2024 · Real Estate AI · Tous droits réservés
</div>
""",
    unsafe_allow_html=True,
)
