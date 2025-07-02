import pandas as pd
import streamlit as st
import plotly.express as px 
import plotly.graph_objects as go
import streamlit.components.v1 as components
import os
import yaml


st.set_page_config(page_title="Tableau de bord", layout="wide")

#CSS personnalisé
st.markdown(
    """
    <style>

    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 1.1em;
        font-weight: bold;
    }
    .stMetric {
        background-color: #F8F9FA; /* Fond clair pour les métriques */
        border-left: 5px solid #2F80ED; /* Bordure colorée à gauche */
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Ombre douce */
    }
    .stMetric label {
        font-weight: bold;
        color: #333333;
    }
    .chart-container {
        border: 1px solid #E0E0E0; /* Bordure fine grise */
        border-radius: 10px; /* Coins arrondis */
        padding: 20px; /* Espace intérieur */
        margin-bottom: 30px; /* Marge en bas pour séparer les conteneurs */
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05); /* Légère ombre */
        background-color: white; /* Fond blanc pour le conteneur */
    }
    </style>
    """,
    unsafe_allow_html=True
)

@st.cache_data
def load_data(dataset):
    return pd.read_excel(dataset)

# Charger les données
dataset_impayés = 'ExtractionV3.xlsx'
df_impayés = load_data(dataset_impayés)

dataset_filtrés = 'ExtractionV7.xlsx'
df = load_data(dataset_filtrés)

# Liste des années
annee_unique = df['SORTIE_ANNEE'].unique()

# Création de 4 onglets
tab1, tab2, tab3, tab4 = st.tabs(["KPI", "Graphiques", "Corrélations", "Profiling"])

# Contenu de tab1
with tab1:

    st.markdown('### Tableau de bord des impayés')
    col1, col2 = st.columns([1, 1])

    with col1:
        
        filtre_annee_tab1 = st.selectbox("Sélectionnez l'année", annee_unique, key="annee_selectbox_tab1")

    with col2:
        
        filtre_residence_tab1 = st.selectbox("Sélectionnez la résidence", df['NOM_IMMEUBLE'].unique(), key="residence_selectbox_tab1")

    st.markdown('')

    # Filtrage des données pour tab1
    df_plot_tab1 = df[(df["SORTIE_ANNEE"] == filtre_annee_tab1) & (df["NOM_IMMEUBLE"] == filtre_residence_tab1)]

    # Calcul des KPI
    total_impayés_locataires_partis = round(df_plot_tab1['SOLDE_DU_CLIENT'].sum(), 2)
    total_impayés = round(df_impayés[df_impayés['SOLDE_DU_CLIENT'] > 0]['SOLDE_DU_CLIENT'].sum(), 2)
    moyenne_impayés_par_locataire = round(df_plot_tab1['SOLDE_DU_CLIENT'].mean(), 2)

    pourcentage_locataires_partis = (total_impayés_locataires_partis / total_impayés * 100) if total_impayés > 0 else 0

    dataset_impayés_mois=df_plot_tab1.groupby(['SORTIE_MOIS'])['SOLDE_DU_CLIENT'].sum().reset_index()

    # Affichage des KPI

    col3, col4, col5 = st.columns([1,1,1])
    col3.metric(label="Total impayés", value=f"{total_impayés_locataires_partis}€")
    col4.metric(label="Moyenne Impayés", value=f"{moyenne_impayés_par_locataire}€")
    col5.metric(label="Pourcentage Impayés Partis", value=f"{pourcentage_locataires_partis:.2f} %")

  
   

    # Graphique des impayés par mois
    # Création du graphique à barres

    # Graphique des impayés par mois avec effets d'ombre
    fig = px.line(
    dataset_impayés_mois,
    x='SORTIE_MOIS',
    y='SOLDE_DU_CLIENT',
    title="Impayés par Mois",
    labels={'SOLDE_DU_CLIENT': 'Montant des Impayés (€)'},
    template='plotly_white'
    )
   

    # Affichage
    st.plotly_chart(fig)

    st.markdown('-----------------------------------------------------------------------------------------------------------')
    # Affichage des clients
    df_filtré = df_plot_tab1.loc[:, ['IDENTIFIANT_CLIENT', 'SORTIE_MOIS', 'SORTIE_ANNEE', 'SOLDE_DU_CLIENT', 'NOM_IMMEUBLE', 'BAIL_TYPE']]
    df_filtré.rename(columns={'IDENTIFIANT_CLIENT': 'Code client', 'SORTIE_MOIS': 'Mois de sortie', 'SORTIE_ANNEE': 'Années de sortie', 'SOLDE_DU_CLIENT': 'Solde du client', 'NOM_IMMEUBLE': 'Nom de l\'immeuble', 'BAIL_TYPE': 'Type de bail'}, inplace=True)
    st.dataframe(df_filtré, use_container_width=True)

    
    

# Contenu de tab2
with tab2:
    st.markdown("<h3 style='color: gray; font-size: 20px;'>Sélectionnez une année</h3>", unsafe_allow_html=True)
    filtre_annee_tab2 = st.selectbox("Sélectionnez l'année", annee_unique, label_visibility="collapsed", key="annee_selectbox_tab2")

    # Filtrage des données pour tab2
    df_plot_tab2 = df[df["SORTIE_ANNEE"] == filtre_annee_tab2]

    # Agrégation des impayés par résidence
    impayés_par_residence = df_plot_tab2.groupby('NOM_IMMEUBLE')['SOLDE_DU_CLIENT'].sum().reset_index()

    # Création du graphique
    # <div class="chart-container">
   
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=impayés_par_residence['NOM_IMMEUBLE'],
        y=impayés_par_residence['SOLDE_DU_CLIENT'],
        mode='lines+markers+text',
        hovertemplate='<b>%{x}</b><br>Total des Impayés: €%{y}<extra></extra>',
        line=dict(color='royalblue', width=2),
        marker=dict(size=8)
    ))

    # Mise en forme du graphique
    fig.update_layout(
    title="Impayés par Résidence",
    xaxis_title="Résidences",
    yaxis_title="Total des Impayés (€)",
    xaxis_tickangle=-45, # Rotation des labels pour une meilleure lisibilité
    xaxis=dict(showline=False, showgrid=False, zeroline=False, showticklabels=False), # Masquer l'axe x et les lignes de grille
    yaxis=dict(showgrid=True), # Afficher la grille sur l'axe y
    template='plotly_white'
    )
    components.html(
    f"""
    <div class="chart-container">
        {fig.to_html(full_html=False, include_plotlyjs='cdn')}
    </div>
    """,
    height=650, # Ajustez la hauteur selon vos besoins
    scrolling=True
)
    
    # Fin de la div chart-container
    # Calcul du nombre de clients par résidence
    nombre_client_par_residence = df_plot_tab2.groupby('NOM_IMMEUBLE')['IDENTIFIANT_CLIENT'].nunique().reset_index()
    merged_data = pd.merge(impayés_par_residence, nombre_client_par_residence, on='NOM_IMMEUBLE')
    merged_data.columns = ['NOM_IMMEUBLE', 'TOTAL_IMPAYES', 'NOMBRE_CLIENTS']

    # Création du scatter plot
    scatter_plot = px.scatter(
        merged_data,
        x='NOMBRE_CLIENTS',
        y='TOTAL_IMPAYES',
        color='NOM_IMMEUBLE',
        title="Relation entre le Nombre d'Impayés et le Nombre de Clients par Résidence",
        trendline='ols'
    )
    st.plotly_chart(scatter_plot)

    #Ajout de deux colones 
    col_pie, col_bar=st.columns([1,1],vertical_alignment="top")

    #Calcul total impayés
    tatal_impayés_tab2 = round(df_plot_tab2['SOLDE_DU_CLIENT'].sum(), 2)

    #Groupement des données par type de bail
    filtre_bail_tab2 = df_plot_tab2.groupby('BAIL_TYPE')['SOLDE_DU_CLIENT'].sum().reset_index()
    with col_pie:
        plot_pie=px.pie(
            df_plot_tab2,
            names='Civilité',
            values='SOLDE_DU_CLIENT',
            title=f"Répartition des Impayés par Résidence pour l'année {filtre_annee_tab2}",
            hole=0.3,
            color_discrete_sequence=px.colors.sequential.RdBu
        )

        st.plotly_chart(plot_pie)

    with col_bar:
        plot_bar=px.bar(
            data_frame=filtre_bail_tab2,
            x='BAIL_TYPE',
            y='SOLDE_DU_CLIENT',
            title=f"Total des Impayés par Type de Bail pour l'année {filtre_annee_tab2}"
            )
        st.plotly_chart(plot_bar)  # Afficher le graphique à barres


    #Carte des impayés par ville
    #Groupement des données par ville
    impayés_par_ville = df_plot_tab2.groupby('CODE_POSTAL_3').agg(
    SOLDE_DU_CLIENT=('SOLDE_DU_CLIENT', 'sum'),
    Ville=('VILLE_4','first'),
    Latitude=('Latitude', 'first'),   # Ajoute la Latitude en prenant la première valeur du groupe
    Longitude=('Longitude', 'first') # Ajoute la Longitude en prenant la première valeur du groupe
    ).reset_index()


    #Afficher impayés par ville
 
    plot_map = px.scatter_mapbox(
    impayés_par_ville,
    lat='Latitude',
    lon='Longitude',
    size='SOLDE_DU_CLIENT',       # Taille des points basée sur le solde
    color='SOLDE_DU_CLIENT',       # Couleur des points basée sur le solde
    hover_name='Ville',            # Nom de la ville au survol
    hover_data={'CODE_POSTAL_3': True, 'SOLDE_DU_CLIENT': ':,.2f €'}, # Détails au survol
    zoom=5,                        # Zoom initial (4 est souvent trop dézoomé pour la France)
    height=700,                    # Augmente la hauteur de la carte
    title=f"Carte des Impayés par Ville pour l'année {filtre_annee_tab2}",
    mapbox_style='open-street-map', # Utilise le style déterminé ci-dessus (Mapbox ou OSM)
    color_continuous_scale=px.colors.sequential.Viridis, # Nouvelle palette de couleurs (Plasma, Viridis, Inferno, Magma)
    opacity=0.6             # Rend les points légèrement transparents pour voir les chevauchements
    )

    

    st.plotly_chart(plot_map, use_container_width=True)


with tab4:

    with st.sidebar:
        uploaded_file = st.file_uploader("Télécharger un fichier Excel pour le profiling")
        

    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        with st.spinner("Génération du rapport de profiling avec Pandas Profiling..."):
             # Chemin vers votre fichier de configuration YAML
            config_file_path = "profiling_config.yaml"
            


            # Charge la configuration depuis le fichier YAML
            try:
                with open(config_file_path, "r", encoding="utf-8") as f:
                    config = yaml.safe_load(f)
            except FileNotFoundError:
                st.error(f"Erreur : Le fichier de configuration '{config_file_path}' n'a pas été trouvé.")
                st.stop() # Arrête l'exécution si le fichier n'est pas là
            except yaml.YAMLError as e:
                st.error(f"Erreur lors de la lecture du fichier YAML : {e}")
                st.stop()

        # Génère le rapport avec la configuration chargée
        # Vous ne passez PLUS 'lang="fr"' ici, car c'est dans le YAML
        profile = ProfileReport(df, **config) # Utilise l'opérateur ** pour décompresser le dict config

        # Sauvegarde le rapport HTML dans un fichier temporaire
        st_profile_report(profile)

            

