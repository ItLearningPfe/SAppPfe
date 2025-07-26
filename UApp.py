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
  

    body {
        background-color: white;
    }

    /* Style pour le titre principal */
    .stMarkdown h3 {
        font-size: 1.3em; /* Grande taille de police */
        font-weight: normal;
        color: #333333; /* Couleur de texte foncée */
        margin-bottom: 20px;
        text-align: left; /* Aligner à gauche */
        padding-bottom: 10px;
    }

    /* Styles pour les Selectbox de Streamlit (les filtres) */
    .stSelectbox {
        background-color: white !important; /* Fond blanc */
        border: 1px solid #e0e0e0; /* Bordure fine grise */
        border-radius: 8px; /* Coins arrondis */
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05); /* Légère ombre */
        padding: 5px 10px; /* Espacement interne */
        transition: all 0.2s ease-in-out; /* Transition douce pour les changements */
        min-height: 38px; /* S'assurer d'une hauteur minimale cohérente */
        display: flex; /* Centrer le contenu verticalement */
        align-items: center; /* Centrer le texte verticalement */
    }
    .stSelectbox div[data-baseweb="select"] .st-cq {
        color: #333333; /* Texte bleu clair */
        background-color: white !important; /* Fond blanc */
        font-weight: 600; /* Plus gras */
        font-size: 1em; /* Taille du texte */
        border: none !important;
    }

    /* Style au survol */
    .stSelectbox div[role="button"]:hover {
        border-color: #a0a0a0; /* Bordure légèrement plus foncée au survol */
        box-shadow: 0 3px 8px rgba(0, 0, 0, 0.1); /* Ombre un peu plus prononcée */
    }

    
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 1.1em;
        font-weight: bold;
    }
    
    /* --- Styles pour nos cartes KPI personnalisées--- */
    .custom-kpi-card {
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 5px 30px rgba(0, 0, 0, 0.1);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        margin-bottom: 15px;
    }

    .custom-kpi-card .kpi-label {
        font-weight: normal !important;
        font-size: 1em;
        margin-bottom: 5px;
        color: white !important; /* Texte BLANC OPAQUE pour le libellé */
    }

    .custom-kpi-card .kpi-value {
        font-size: 2em;
        font-weight: normal !important;
        color: white !important; /* Texte BLANC OPAQUE pour la valeur */
    }

    /* Classes spécifiques pour les couleurs de fond (OPAQUES) */
    .kpi-orange { background-color: #FFAD7A !important; opacity=0.5; } /* Orange vif */
    .kpi-green { background-color: #77DFAB !important; } /* Vert vif */
    .kpi-blue { background-color: #88B0D7 !important; } /* Bleu vif */
  


    /* Style pour les conteneurs de graphiques Plotly */
    div[data-testid="stPlotlyChart"] {
        border: none; /* Supprimé la bordure */
        border-radius: 12px; /* Coins arrondis */
        padding: 20px; /* Espace intérieur */
        margin-bottom: 30px; 
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1); 
        background-color: white !important; 
   }


    .chart-container {
        border: none;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        background-color: white !important;
    }


    /* Styles pour les Dataframes Streamlit (le tableau) */
    .stDataFrame {
        border: none !important;
        border-radius: 12px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        background-color: white !important;
        padding: 20px;
    }
    /* Styles pour les en-têtes du tableau */
    .stDataFrame div[data-testid="stDataframeHeaders"] {
        background-color: #f8f8f8;
        border-bottom: none !important;
    }
    .stDataFrame th {
        padding: 12px 15px;
        font-weight: bold;
        color: #555;
        text-align: left;
        border: none;
    }
    /* Styles pour les cellules du tableau */
    .stDataFrame td {
        padding: 10px 15px;
        border: none;
    }


    /* Pas de bordure sur la dernière ligne du tableau */
    .stDataFrame tr {
        border-bottom: none !important;
    }


    .stDataFrame div[role="columnheader"],
    .stDataFrame div[role="gridcell"],
    .stDataFrame div[role="rowheader"],
    .stDataFrame div[role="row"] {
        border: none !important;
        outline: none !important; /* Pour supprimer tout contour de focus résiduel */
    }

   
    .stDataFrame * { /* Cible TOUS les éléments à l'intérieur du .stDataFrame */
    border-color: transparent !important; 
    }
    .content-card {
        border: none;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        background-color: white !important;
    }
}
    </style>
    """,
    unsafe_allow_html=True
)

# Fonction pour générer une carte KPI personnalisée
def custom_kpi_card(label, value, color_class):
    """Génère un HTML pour une carte KPI colorée."""
    html_card = f"""
    <div class="custom-kpi-card {color_class}">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
    </div>
    """
    return html_card 

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
#tri des années
annee_unique.sort() 



# Ajoutez le placeholder au début de la liste des années et convertissez en liste Python
annee_options = ['Sélectionner l\'année'] + annee_unique.tolist()

# Ajoutez le placeholder au début de la liste des résidences et convertissez en liste Python
residence_options = ['Sélectionner la résidence'] + df['NOM_IMMEUBLE'].unique().tolist()




# Création de 4 onglets
tab1, tab2, tab3, tab4 = st.tabs(["KPI", "Graphiques", "Corrélations", "Profiling"])

# Contenu de tab1
with tab1:

    st.markdown('### Tableau de bord des impayés')
    
    col1, col2 = st.columns([1, 1])

    with col1:
        # Utilisez la liste 'annee_options' et définissez l'index par défaut sur 0 (le placeholder)
        filtre_annee_tab1 = st.selectbox(
            "Sélectionnez l'année", 
            annee_options, 
            index=0, 
            key="annee_selectbox_tab1", 
            label_visibility="collapsed"
        )

    with col2:
        # Utilisez la liste 'residence_options' et définissez l'index par défaut sur 0
        filtre_residence_tab1 = st.selectbox(
            "Sélectionnez la résidence", 
            residence_options, 
            index=0, 
            key="residence_selectbox_tab1", 
            label_visibility="collapsed"
        )

    st.markdown('')

    # Filtrage des données pour tab1 : Gérer le placeholder dans le filtre
    # Initialisez df_plot_tab1 pour éviter un UnboundLocalError si aucune condition n'est remplie
    df_plot_tab1 = df.copy() 

    # Vérifiez les sélections et appliquez les filtres
    annee_selectionnee = filtre_annee_tab1
    residence_selectionnee = filtre_residence_tab1

    if annee_selectionnee != 'Sélectionner l\'année' and residence_selectionnee != 'Sélectionner la résidence':
        df_plot_tab1 = df[(df["SORTIE_ANNEE"] == annee_selectionnee) & (df["NOM_IMMEUBLE"] == residence_selectionnee)]
    elif annee_selectionnee != 'Sélectionner l\'année':
        df_plot_tab1 = df[df["SORTIE_ANNEE"] == annee_selectionnee]
    elif residence_selectionnee != 'Sélectionner la résidence':
        df_plot_tab1 = df[df["NOM_IMMEUBLE"] == residence_selectionnee]
    # Si les deux sont des placeholders, df_plot_tab1 reste une copie complète de df, comme initialisé.


    # Calcul des KPI
    total_impayés_locataires_partis = round(df_plot_tab1['SOLDE_DU_CLIENT'].sum(), 2)
    total_impayés = round(df_impayés[df_impayés['SOLDE_DU_CLIENT'] > 0]['SOLDE_DU_CLIENT'].sum(), 2)
    moyenne_impayés_par_locataire = round(df_plot_tab1['SOLDE_DU_CLIENT'].mean(), 2)

    pourcentage_locataires_partis = (total_impayés_locataires_partis / total_impayés * 100) if total_impayés > 0 else 0

    dataset_impayés_mois=df_plot_tab1.groupby(['SORTIE_MOIS'])['SOLDE_DU_CLIENT'].sum().reset_index()

   

    # Affichage des KPI
    col3, col4, col5 = st.columns([1,1,1])

    with col3:
        st.markdown(custom_kpi_card("Total impayés", f"{total_impayés_locataires_partis:,.2f}€".replace(",", " ").replace(".", ",").replace(" ", "."), "kpi-orange"), unsafe_allow_html=True)

    with col4:
        st.markdown(custom_kpi_card("Moyenne Impayés", f"{moyenne_impayés_par_locataire:,.2f}€".replace(",", " ").replace(".", ",").replace(" ", "."), "kpi-green"), unsafe_allow_html=True)

    with col5:
        st.markdown(custom_kpi_card("Pourcentage Impayés Partis", f"{pourcentage_locataires_partis:.2f} %", "kpi-blue"), unsafe_allow_html=True)


    # Graphique des impayés par mois 
    fig = px.line(
    dataset_impayés_mois,
    x='SORTIE_MOIS',
    y='SOLDE_DU_CLIENT',
    title="Impayés par Mois",
    labels={'SOLDE_DU_CLIENT': 'Montant des Impayés (€)'},
    template='plotly_white',
    line_shape='spline',  # Utilisation de lignes lissées
    markers=True,  # Ajout de marqueurs pour chaque point
    color_discrete_sequence=['#6A9AC9']
    
    )
    fig.update_traces(
    mode='lines+markers', # S'assure que les lignes sont dessinées avec des marqueurs
    fill='tozeroy',       # Remplit la zone sous la ligne jusqu'à l'axe des y=0
    fillcolor='rgba(106, 154, 201, 0.1)', # Couleur de remplissage (bleu clair semi-transparent)
    line=dict(width=1.5) # Épaisseur de la ligne
    )
    

    # Affichage
    st.plotly_chart(fig)


    # Affichage des clients
    df_filtré = df_plot_tab1.loc[:, ['IDENTIFIANT_CLIENT', 'SORTIE_MOIS', 'SORTIE_ANNEE', 'SOLDE_DU_CLIENT', 'NOM_IMMEUBLE', 'BAIL_TYPE']]
    df_filtré.rename(columns={'IDENTIFIANT_CLIENT': 'Code client', 'SORTIE_MOIS': 'Mois de sortie', 'SORTIE_ANNEE': 'Années de sortie', 'SOLDE_DU_CLIENT': 'Solde du client', 'NOM_IMMEUBLE': 'Nom de l\'immeuble', 'BAIL_TYPE': 'Type de bail'}, inplace=True)
    st.dataframe(df_filtré, use_container_width=True)

    
    

# Contenu de tab2
with tab2:
    # Pour le filtre de l'année dans tab2, faites de même
    filtre_annee_tab2 = st.selectbox(
        "Sélectionnez l'année", 
        annee_options, # Utilisez la liste avec le placeholder
        index=0,       # Le placeholder est le premier élément (index 0)
        label_visibility="collapsed", 
        key="annee_selectbox_tab2"
    )

    # Filtrage des données pour tab2 - Gérer le placeholder
    if filtre_annee_tab2 == 'Sélectionner l\'année':
        df_plot_tab2 = df.copy() # Pas de filtre sur l'année si le placeholder est sélectionné
    else:
        df_plot_tab2 = df[df["SORTIE_ANNEE"] == filtre_annee_tab2]

    # Agrégation des impayés par résidence
    impayés_par_residence = df_plot_tab2.groupby('NOM_IMMEUBLE')['SOLDE_DU_CLIENT'].sum().reset_index()

    # Création du graphique
    
    
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
        df_plot_tab2['Civilité'] = df_plot_tab2['Civilité'].astype(str).str.strip().str.capitalize()
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
    size='SOLDE_DU_CLIENT',        # Taille des points basée sur le solde
    color='SOLDE_DU_CLIENT',        # Couleur des points basée sur le solde
    hover_name='Ville',             # Nom de la ville au survol
    hover_data={'CODE_POSTAL_3': True, 'SOLDE_DU_CLIENT': ':,.2f €'}, # Détails au survol
    zoom=5,                         # Zoom initial (4 est souvent trop dézoomé pour la France)
    height=700,                     # Augmente la hauteur de la carte
    title=f"Carte des Impayés par Ville pour l'année {filtre_annee_tab2}",
    mapbox_style='open-street-map', # Utilise le style déterminé ci-dessus (Mapbox ou OSM)
    color_continuous_scale=px.colors.sequential.Viridis, # Nouvelle palette de couleurs (Plasma, Viridis, Inferno, Magma)
    opacity=0.6                     # Rend les points légèrement transparents pour voir les chevauchements
    )

    

    st.plotly_chart(plot_map, use_container_width=True)




    
    # --- Contenu de l'onglet Profiling (SANS sidebar) ---
with tab4:
    st.markdown("### 📊 Rapport de Profilage des Données")
    st.write(
        "Téléchargez un fichier Excel pour générer un rapport de profilage détaillé. Ce rapport analyse la **qualité**, la **complétude**, la **distribution** et d'autres caractéristiques de vos données."
    )

    # Conteneur pour le téléchargeur de fichiers
    with st.container(border=True): 
        st.markdown(
            """
            <h4 style="color: #333333; margin-top: 0px;">Importer votre fichier de données :</h4>
            <p style="color: #555555; font-size: 0.95em;">
                Glissez-déposez votre fichier Excel ici ou cliquez pour le sélectionner.
                Formats acceptés : **.xlsx**, **.xls**.
            </p>
            """,
            unsafe_allow_html=True,
        )

        uploaded_file = st.file_uploader(
            "Sélectionnez un fichier Excel pour le profiling",
            type=["xlsx", "xls"],
            key="main_profiling_uploader_manual", # Clé unique
            label_visibility="collapsed",
        )

        if uploaded_file is None:
            st.info("👈 Veuillez charger un fichier pour générer le rapport de profiling.")
        else:
            st.success("✅ Fichier chargé avec succès ! Analyse des données en cours...")

    if uploaded_file is not None:
        try:
            df_profiling = pd.read_excel(uploaded_file)

            # --- Filtre par variable ---
            all_columns = ['Sélectionner une variable (Vue Globale)'] + df_profiling.columns.tolist()
            selected_column = st.selectbox(
                "Sélectionnez une variable pour une analyse détaillée :",
                label_visibility="collapsed",
                options=all_columns,
                index=0, # Par défaut, la vue globale
                key="profiling_column_selector",
                help="Choisissez une colonne pour afficher son profil détaillé, ou 'Vue Globale' pour les métriques générales.",
            )

            # Aperçu des Données (toujours dans une carte)
            
            
            st.markdown("### Aperçu des Données (5 premières lignes)")
           
            st.dataframe(df_profiling.head(), use_container_width=True)
            
            st.markdown("---")


            # Conditionnement de l'affichage en fonction de la sélection de la colonne
            if selected_column == 'Sélectionner une variable (Vue Globale)':
                # --- Vue d'ensemble de la Qualité des Données (Globale) ---
                st.markdown("### 🔍 Vue d'ensemble de la Qualité des Données")

                # Section 1: Statistiques Générales du Dataset
                
                
                num_rows = df_profiling.shape[0]
                num_cols = df_profiling.shape[1]
                total_cells = num_rows * num_cols

                total_missing_values = df_profiling.isnull().sum().sum()
                percentage_missing = (total_missing_values / total_cells * 100) if total_cells > 0 else 0

                num_duplicates = df_profiling.duplicated().sum()
                percentage_duplicates = (num_duplicates / num_rows * 100) if num_rows > 0 else 0

                st.markdown(f"**Nombre de Lignes :** `{num_rows}`")
                st.markdown(f"**Nombre de Colonnes :** `{num_cols}`")
                st.markdown(f"**Valeurs Manquantes Totales :** `{total_missing_values}` ({percentage_missing:.2f}%)")
                st.markdown(f"**Lignes Dupliquées :** `{num_duplicates}` ({percentage_duplicates:.2f}%)")
                
                st.markdown("---") # Séparateur pour la clarté

                # Section 2: Types de Données des Colonnes
                
                st.markdown("### Types de Données des Colonnes")
                dtypes_df = pd.DataFrame(df_profiling.dtypes, columns=['Type de Donnée'])
                st.dataframe(dtypes_df, use_container_width=True)
    
                st.markdown("---") # Séparateur pour la clarté

                # Section 3: Complétude des Colonnes
               
                st.markdown("### Complétude des Colonnes")
                
                missing_values_per_column = df_profiling.isnull().sum()
                missing_percentage_per_column = (missing_values_per_column / num_rows) * 100

                missing_df = pd.DataFrame({
                    'Colonne': missing_percentage_per_column.index,
                    'Pourcentage Manquant': missing_percentage_per_column.values
                })
                missing_df = missing_df.sort_values(by='Pourcentage Manquant', ascending=False)

                fig_missing = px.bar(
                    missing_df,
                    x='Pourcentage Manquant',
                    y='Colonne',
                    orientation='h',
                    title='Pourcentage de Valeurs Manquantes par Colonne',
                    labels={'Pourcentage Manquant': '% Manquant', 'Colonne': 'Nom de la Colonne'},
                    color='Pourcentage Manquant',
                    color_continuous_scale=px.colors.sequential.Reds,
                    height=max(400, 30 * len(missing_df))
                )
                fig_missing.update_layout(showlegend=False)
                fig_missing.update_yaxes(autorange="reversed")
                st.plotly_chart(fig_missing, use_container_width=True)
                
                st.markdown("---")

                # Matrice de Corrélation
                
                st.markdown("### 🔗 Matrice de Corrélation")
                corr_matrix = df_profiling.select_dtypes(include=['number']).corr()

                if not corr_matrix.empty:
                    fig_corr = px.imshow(
                        corr_matrix,
                        text_auto=True,
                        aspect="auto",
                        color_continuous_scale=px.colors.sequential.RdBu,
                        title="Matrice de Corrélation",
                    )
                    fig_corr.update_layout(height=max(500, 50 * len(corr_matrix)))
                    st.plotly_chart(fig_corr, use_container_width=True)
                else:
                    st.info("Aucune donnée numérique pour calculer la matrice de corrélation.")
                
                st.markdown("---")

                # Analyse des Valeurs Uniques par Colonne
                
                st.markdown("### 📊 Analyse des Valeurs Uniques par Colonne")
                unique_counts = df_profiling.nunique().sort_values(ascending=False)
                num_rows_profiling = df_profiling.shape[0] 
                unique_percentage = (unique_counts / num_rows_profiling) * 100

                unique_df = pd.DataFrame({
                    'Colonne': unique_counts.index,
                    'Nombre Unique': unique_counts.values,
                    'Pourcentage Unique': unique_percentage.values
                })

                fig_unique = px.bar(
                    unique_df,
                    x='Nombre Unique',
                    y='Colonne',
                    orientation='h',
                    title='Nombre de Valeurs Uniques par Colonne',
                    labels={'Nombre Unique': 'Count', 'Colonne': 'Nom de la Colonne'},
                    color='Pourcentage Unique',
                    color_continuous_scale=px.colors.sequential.Blues,
                    height=max(400, 30 * len(unique_df))
                )
                fig_unique.update_yaxes(autorange="reversed")
                st.plotly_chart(fig_unique, use_container_width=True)
                
                st.markdown("---")

                # Aperçu des Lignes Dupliquées Complètes
               
                st.markdown("### 🚫 Aperçu des Lignes Dupliquées Complètes")
                if num_duplicates > 0:
                    st.write(f"Les `{num_duplicates}` lignes suivantes sont des doublons exacts :")
                    st.dataframe(df_profiling[df_profiling.duplicated(keep=False)].sort_values(df_profiling.columns.tolist()), use_container_width=True)
                else:
                    st.info("Aucune ligne complètement dupliquée n'a été trouvée dans le dataset.")
                


            else: # selected_column est une colonne spécifique
                st.markdown(f"### 🔍 Profil Détaillé de la Variable : `{selected_column}`")

                # --- Propriétés et statistiques de la variable (dans une carte) ---
                
                col_prop, col_stat = st.columns(2)

                with col_prop:
                    st.markdown("### **Propriétés de la Variable**")
                    series = df_profiling[selected_column]

                    st.markdown(f"**Type de Donnée :** `{series.dtype}`")
                    st.markdown(f"**Nombre de Valeurs :** `{len(series)}`")

                    # Valeurs manquantes
                    missing_count = series.isnull().sum()
                    missing_percent = (missing_count / len(series) * 100) if len(series) > 0 else 0
                    st.markdown(f"**Valeurs Manquantes :** `{missing_count}` ({missing_percent:.2f}%)")

                    # Valeurs uniques
                    unique_count = series.nunique()
                    unique_percent = (unique_count / len(series) * 100) if len(series) > 0 else 0
                    st.markdown(f"**Valeurs Uniques :** `{unique_count}` ({unique_percent:.2f}%)")
                with col_stat:
                    # Statistiques de base pour les numériques
                    if pd.api.types.is_numeric_dtype(series):
                        st.markdown("### **Statistiques Numériques**")
                        st.markdown(f"**Moyenne :** `{series.mean():.2f}`")
                        st.markdown(f"**Médiane :** `{series.median():.2f}`")
                        st.markdown(f"**Écart-type :** `{series.std():.2f}`")
                        st.markdown(f"**Min :** `{series.min()}`")
                        st.markdown(f"**Max :** `{series.max()}`")
                        st.markdown(f"**25e Percentile :** `{series.quantile(0.25):.2f}`")
                        st.markdown(f"**75e Percentile :** `{series.quantile(0.75):.2f}`")
                    else: # Statistiques pour les catégorielles/textuelles
                        st.markdown("#### **Statistiques Catégorielles/Textuelles**")
                        st.markdown(f"**Mode :** `{series.mode()[0] if not series.mode().empty else 'N/A'}`")
                        # Vous pouvez ajouter d'autres métriques comme la longueur moyenne de texte, etc.
                
                st.markdown("### 📈 Distribution de la Variable (Analyse Univariée)")
                    
                if pd.api.types.is_numeric_dtype(series):
                        # Crée deux colonnes pour les graphiques côte à côte
                        col_hist, col_box = st.columns([0.5, 0.5])

                        with col_hist:
                            # Histogramme
                            fig_hist = px.histogram(
                                df_profiling,
                                x=selected_column,
                                nbins=30,
                                title=f"Histogramme de {selected_column}",
                                template='plotly_white',
                                color_discrete_sequence=['#6A9AC9']
                            )
                            fig_hist.update_layout(
                                bargap=0.1
                                
                            )
                            st.plotly_chart(fig_hist, use_container_width=True)

                        with col_box:
                            # Box Plot
                            fig_box = px.box(
                                df_profiling,
                                y=selected_column,
                                title=f"Box Plot de {selected_column}",
                                template='plotly_white',
                                color_discrete_sequence=['#77DFAB']
                            )
                         
                            st.plotly_chart(fig_box, use_container_width=True)
                elif pd.api.types.is_categorical_dtype(series) or pd.api.types.is_object_dtype(series):
                        # Pour les données catégorielles/objet
                        value_counts_df = series.value_counts().reset_index()
                        value_counts_df.columns = ['Valeur', 'Fréquence']
                        fig_cat = px.bar(
                            value_counts_df,
                            x='Valeur',
                            y='Fréquence',
                            title=f"Distribution des catégories de {selected_column}",
                            labels={'Valeur': selected_column, 'Fréquence': 'Count'},
                            template='plotly_white',
                            color_discrete_sequence=['#FFAD7A']
                        )
                        st.plotly_chart(fig_cat, use_container_width=True)
                else:
                        st.info("Pas de visualisation de distribution spécifique pour ce type de donnée (ou non numérique/catégorielle).")
                    
               
                st.markdown("---")


                # --- Analyse Multivariée (pour la variable sélectionnée) (dans une carte) ---
                
                st.markdown("### 📊 Analyse Multivariée")

                numeric_cols = df_profiling.select_dtypes(include=['number']).columns.tolist()
                # Exclure la colonne sélectionnée pour le second axe
                other_numeric_cols = [col for col in numeric_cols if col != selected_column]

                if pd.api.types.is_numeric_dtype(series) and len(other_numeric_cols) > 0:
                    st.markdown("###** Nuage de points avec une autre variable numérique**")

                    selected_col_y = st.selectbox(
                        f"Choisissez une autre variable numérique pour un nuage de points avec `{selected_column}` :",
                        options=['Sélectionner une variable'] + other_numeric_cols,
                        index=0,
                        key=f"scatter_y_{selected_column}"
                    )

                    if selected_col_y != 'Sélectionner une variable':
                        fig_scatter = px.scatter(
                            df_profiling,
                            x=selected_column,
                            y=selected_col_y,
                            title=f"Nuage de points : {selected_column} vs {selected_col_y}",
                            template='plotly_white',
                            trendline="ols", # Ajoute une ligne de régression linéaire
                            color_discrete_sequence=['#88B0D7']
                        )
                        st.plotly_chart(fig_scatter, use_container_width=True)
                    else:
                        st.info("Sélectionnez une deuxième variable numérique pour afficher un nuage de points.")
                elif not pd.api.types.is_numeric_dtype(series):
                    st.info(f"Le nuage de points n'est pas applicable car '{selected_column}' n'est pas une variable numérique.")
                else:
                    st.info("Pas assez de variables numériques pour créer un nuage de points.")
                
                

                # --- Top 10 des Valeurs les plus Fréquentes (dans une carte) ---
                
                st.markdown("### **Top 10 des Valeurs les plus Fréquentes**")
                st.dataframe(df_profiling[selected_column].value_counts().head(10).reset_index().rename(columns={'index': selected_column, selected_column: 'Fréquence'}), use_container_width=True)
               


        except Exception as e:
            st.error(f"Une erreur est survenue lors du traitement du fichier ou de la génération du rapport : {e}")
            st.info(
                "Veuillez vous assurer que le fichier est un fichier Excel valide et que son contenu est correctement formaté."
            )