import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from PIL import Image



csv_url = "https://media.githubusercontent.com/media/premapouce/streamlit-app/refs/heads/main/data/5_LFB_fusion_sample.csv"

if 'df' not in st.session_state:
    try:
        st.session_state.df = pd.read_csv(csv_url)
    except Exception as e:
        st.error(f"Erreur lors du chargement des données : {e}")
        st.session_state.df = None

# Utiliser le dataframe seulement s'il est bien chargé
if st.session_state.df is not None:
    df = st.session_state.df
    # Ton code ici avec df (ex: affichage, visualisation...)
else:
    st.warning("Les données ne sont pas disponibles.")


@st.cache_data
def analyser_df(df):
    analyse = pd.DataFrame({
        'Nb NaN': df.isna().sum(),
        '% NaN': df.isna().mean() * 100,
        'Nb valeurs uniques': df.nunique()
    })
    return analyse




st.sidebar.title("Sommaire")
st.sidebar.image("logo DST.png", width=75)
pages = ["Introduction", "Métadonnées", "Exploration", "Enrichissement", "Datavisualisation","Preprocessing", "Modélisation","Conclusion"]
page = st.sidebar.radio("Aller vers", pages)


# Affichage de l'image principale
st.image("Lfb_logo.jpg", width=75)

# 
if page == "Introduction":
    st.markdown(
        "<h1 style='text-align:center; color:#B22222;'>⏱️ Temps de réponse des pompiers de Londres</h1>", 
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.markdown(
        """
        <h2 style='color:#444;'>📖 Contexte</h2>
        <p style='text-align:justify; line-height:1.6;'>
        La London Fire Brigade (LFB) met à disposition, sur son site officiel, les données relatives aux incidents enregistrés depuis janvier 2009, 
        ainsi que les informations concernant les véhicules de secours déployés sur les lieux d’intervention.
        </p>

        <h2 style='color:#444;'>🎯 Objectif</h2>
        <p style='text-align:justify; line-height:1.6;'>
        Le présent projet repose sur l’exploration et le traitement de ces données afin d’analyser et d’estimer le temps de réaction opérationnel de la LFB.  
        Les casernes sont implantées de manière stratégique pour maintenir un délai moyen d’intervention inférieur ou égal à <b>six minutes</b>.
        </p>

        <h2 style='color:#444;'>🧩 Finalité</h2>
        <p style='text-align:justify; line-height:1.6;'>
        L’analyse vise à évaluer les performances actuelles de la brigade et à développer des modèles prédictifs permettant d’anticiper 
        les temps de réponse en fonction de différents paramètres contextuels.
        </p>
        """, 
        unsafe_allow_html=True
    )


    # --- Fonctions d'analyse ---
    @st.cache_data
    def analyser_df(df):
        """Retourne un résumé du DataFrame : % de valeurs manquantes et nb de valeurs uniques par colonne."""
        return pd.DataFrame({
            '% de valeurs manquantes': df.isna().mean() * 100,
            'Nombre de valeurs uniques': df.nunique()
        }).round(2)

    def get_value_counts(df, column, top_n=20):
        """Retourne la distribution des valeurs d'une colonne (top N valeurs)."""
        value_counts = df[column].value_counts(dropna=False).head(top_n)
        value_counts_df = value_counts.reset_index()
        value_counts_df.columns = [column, 'Nombre']
        value_counts_df['Pourcentage'] = (value_counts_df['Nombre'] / value_counts_df['Nombre'].sum()) * 100
        return value_counts_df.round(2)

    # --- Analyse globale du DataFrame ---


elif page == "Métadonnées":
    st.markdown(
        "<h1 style='text-align:center; color:#B22222;'>Métadonnées</h1>", 
        unsafe_allow_html=True
    )

    st.markdown("---")

    Variables=['IncidentNumber', 'DateOfCall','CalYear', 'TimeOfCall', 'HourOfCall',  'IncidentGroup', 'StopCodeDescription',  'SpecialServiceType','PropertyCategory', 'PropertyType', 'AddressQualifier', 'Postcode_full',
                'Postcode_district',  'UPRN',  'USRN', 'IncGeo_BoroughCode',  'IncGeo_BoroughName', 'ProperCase',
                  'IncGeo_WardCode','IncGeo_WardName', 'IncGeo_WardNameNew',  'Easting_m', 'Northing_m',  'Easting_rounded', 
                  'Northing_rounded',  'Latitude',  'Longitude',  'FRS', 'IncidentStationGround', 'FirstPumpArriving_AttendanceTime', 
                  'FirstPumpArriving_DeployedFromStation',  'SecondPumpArriving_AttendanceTime', 'SecondPumpArriving_DeployedFromStation',  
                  'NumStationsWithPumpsAttending',  'NumPumpsAttending', 'PumpCount',  'PumpMinutesRounded',  'NationalCost', 'NumCalls',  
                  'ResourceMobilisationId',  'Resource_Code', 'PerformanceReporting',  'DateAndTimeMobilised', 'DateAndTimeMobile', 'DateAndTimeArrived',  
                  'TurnoutTimeSeconds', 'TravelTimeSeconds', 'AttendanceTimeSeconds', 'DateAndTimeLeft', 'DateAndTimeReturned', 'DeployedFromStation_Code', 'DeployedFromStation_Name', 
                  'DeployedFromLocation',  'PumpOrder', 'PlusCode_Code', 'PlusCode_Description', 'DelayCodeId',  'DelayCode_Description',  
                  'BoroughName',  'WardName']
    Description=["Numéro de l'incident", "Date de l'appel", "Année", "Temps de l'appel","Heure de l'appel","Catégorie d'incident",
                 "Sous-catégorie d'incident","Type de service spécial","Catégorie de propriété","Sous-catégorie de propriété",
                 "Qualité du renseignement donné de l'adrese de l'incident","Code Postal","Code du district","identifiant attribué à chaque unité d'adresse",
                 "Identifiant attribué à chaque voie","Code de l'arrondissement","Nom de l'arrondissement","nom de l'arrondissement en minuscules","Code du quartier","Nom du quartier","Nouveau nom de quartier","Coordonnées Est",
                 "Coordonnées Nord","Coordonnées arrondies Est","Coordonnées arrondies Nord","Latitude","Longitude","Brigade de pompiers","Caserne correspondant au lieu de l'incident",
                 "Délai d'arrivée de la première unité","Nom de la caserne d'origine","Délai d'arrivée de la seconde unité","Caserne de départ de la seconde unité",
                 "Nombre de casernes engagées pour un incident","nombre de camions déployés pour un incident","Nombre total de camions déployés toutes casernes confondues pour un incident",
                 "Nombre de minutes d'intervention cumulées","Coût théorique de l'intervention","Nombre d'appels au 999 pour un incident","Id de l'unité de mobilisation","code de l'unité de mobilisation",
                 "Perfomance","Date et heure où les pompiers sont mobilisés","Date et heure du départ depuis la caserne","Date et Heure d'arrivée sur les lieux de l'incident","Temps écoulé entre l'alerte et le départ du camion","Temps de trajet",
                 "Temps écoulé entre l'alerte et l'arrivée sur les lieux de l'incident","Date et heure où l'unité quitte le lieu de l'incident","Date et heure du retour à la caserne",
                 "Code identifiant de la caserne","Nom de la caserne","Type de déploiement","Ordre d'intervention du camion","Code de mobilisation","Type de mobilisation","Code retard","Type de retard","Nom de l'arrondissement","Nom du quartier"]
    df_var = pd.DataFrame({
    "Nom de la variable": Variables,
    "Description": Description
})

# Fonction de surlignage
    def highlight_firstpump(row):
        color = 'background-color: lightgreen' if row['Nom de la variable'] == 'FirstPumpArriving_AttendanceTime' else ''
        return [color] * len(row)

# Application du style
    styled_df = df_var.style.apply(highlight_firstpump, axis=1)

# Affichage dans Streamlit
    st.dataframe(styled_df, use_container_width=True)

    

elif page == "Exploration":
    st.markdown(
        "<h1 style='text-align:center; color:#B22222;'>Exploration des données</h1>", 
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.markdown(
        """
        <p style='text-align:justify; line-height:1.6;'>
        Le jeu de données fourni par la <b>London Fire Brigade (LFB)</b> contient un ensemble complet de variables décrivant chaque incident, 
        ses caractéristiques géographiques, temporelles et opérationnelles.  
        Ces informations permettent d’analyser les délais d’intervention et d’identifier les facteurs influençant le temps de réponse.
        </p>

        <p style='text-align:justify; line-height:1.6;'>
        Les variables sont regroupées selon plusieurs thématiques :
        </p>
        <ul style='line-height:1.6;'>
            <li><b>Variables temporelles</b> : date, heure et année de l’appel</li>
            <li><b>Variables géographiques</b> : arrondissement, quartier, coordonnées</li>
            <li><b>Variables opérationnelles</b> : nombre de véhicules mobilisés, temps d’arrivée, durée d’intervention</li>
            <li><b>Variables administratives</b> : identifiants internes et codes de mobilisation</li>
        </ul>

        <p style='text-align:justify; line-height:1.6;'>
        Une attention particulière est portée à la variable <b>FirstPumpArriving_AttendanceTime</b>, 
        qui correspond au temps d’arrivée du premier camion sur les lieux.  
        Cet indicateur est central pour évaluer la performance de la brigade et constitue la variable cible de la modélisation.
        </p>
        """, 
        unsafe_allow_html=True
    )
   
    st.write("")
# Création de trois onglets
    tabs = st.tabs(["Données manquantes", "Occurrences", "Outliers", "Doublons"])

# Contenu du premier onglet
     
    with tabs[0]:
        st.markdown(
        """
        <h3 style='color:#444;'>Données manquantes</h3>
        <p style='text-align:justify; line-height:1.6;font-size:16px;'>
        </p>
        """, unsafe_allow_html=True
    )
        data = {"Column":["SpecialServiceType", "Postcode_full", "UPRN", "USRN", "IncGeo_WardCode","IncGeo_WardName","IncGeo_WardNameNew","Easting_m","Northing_m","Latitude","Longitude",
                                                                        "IncidentStationGround","FirstPumpArriving_AttendanceTime","FirstPumpArriving_DeployedFromStation","SecondPumpArriving_AttendanceTime","SecondPumpArriving_DeployedFromStation",
                                                                        "NumCalls","DateAndTimeMobile","TurnoutTimeSeconds","TravelTimeSeconds","DateAndTimeLeft",
                                                                        "DateAndTimeReturned","DeployedFromStation_Code","DeployedFromStation_Name",
                                                                        "DeployedFromLocation","DelayCodeId","DelayCode_Description","BoroughName","WardName"],     
         "%NaN":["77.71", "53.91", "7.91", "9.33","0.03","0.03","0.03","53.91","53.91","53.91","53.91","0.00009","0.0001","0.0007","41.19","41.19","0.07","1.23","1.24","1.24","2.27","52.21","0.00005","0.00005","0.04","74.65","74.65","65.12","65.1"]}
        df_nan = pd.DataFrame(data)

     # Fonction pour colorer la ligne souhaitée
        def highlight_firstpump(row):
            if row['Column'] == 'FirstPumpArriving_AttendanceTime':
                return ['background-color: lightgreen'] * len(row)
            else:
                return [''] * len(row)

      # Appliquer le style
        styled_df = df_nan.style.apply(highlight_firstpump, axis=1)

     # Convertir en HTML avec CSS
        html = styled_df.set_table_attributes('class="custom-table"').hide(axis="index").to_html()

      # Style CSS
        st.markdown("""
<style>
.custom-table {
    font-size: 15px;
    border-collapse: collapse;
    margin: 0 auto;
    width: auto;
}
.custom-table th {
    background-color: #f0f0f0;
    color: black;
    padding: 7px;
    text-align: center;
}
.custom-table td {
    padding: 7px;
    text-align: center;
    border: 1px solid #ddd;
}
</style>
""", unsafe_allow_html=True)

     # Afficher le tableau stylisé
        st.markdown(html, unsafe_allow_html=True)

        st.markdown("Une proportion importante de valeurs manquantes est observée dans le jeu de données.\n"
"Pour ne pas perdre d’informations pertinentes, les lignes concernées seront conservées puis complétées par des méthodes d’imputation adaptées.\n"
"Ce traitement interviendra uniquement après la division des données en jeu d’entraînement et de test, afin d’éviter toute contamination du jeu de test et garantir la validité du processus d’apprentissage.")
# Contenu du deuxième onglet
    with tabs[1]:
        st.markdown(
        """
        <h3 style='color:#444;'>Occurences</h3>
        <p style='text-align:justify; line-height:1.6;font-size:16px;'>
        </p>
        """, unsafe_allow_html=True
    )
        colonnes_cat = ['IncidentGroup', 'StopCodeDescription', 'SpecialServiceType','PropertyCategory','DeployedFromLocation','DelayCode_Description']

        st.write("")
        variable = st.selectbox("### Sélectionner une variable catégorielle", colonnes_cat)

        @st.cache_data
        def calcul_distribution(df, col):
           dist = df[col].value_counts(normalize=True).reset_index()
           dist.columns = [col, '%']
           dist['%'] = (dist['%'] * 100).round(2)
           return dist
        if variable:
           dist_df = calcul_distribution(df, variable)
           st.dataframe(dist_df,use_container_width=True)
        st.write("")

# Contenu du troisième onglet : outliers
    with tabs[2]:
        st.markdown(
        """
        <h3 style='color:#444;'>Outliers</h3>
        <p style='text-align:justify; line-height:1.6;'font-size:16px;'>
        </p>
        """, unsafe_allow_html=True
    )
        data = [[311, 1, 229, 291, 369, 1200, 130]] 
        columns =["FirstPumpAttendanceTime"] 
        index = ["mean", "min","25%", "50%", "75%", "max","std"]
        df = pd.DataFrame(data, columns, index)
        
        table_html = df.to_html(classes='custom-table', border=0)

        st.markdown("""<style>.custom-table {
             width: 80%;  margin-left: auto; margin-right: auto; font-size: 14px;
        border-collapse: collapse;
    }.custom-table th, .custom-table td {
        padding: 8px 12px;
        border: 1px solid #ccc;
        text-align: center;
    }</style>
""", unsafe_allow_html=True)
        st.markdown(table_html, unsafe_allow_html=True)

        st.write("Ces statistiques nous permettent d'apporter 2 arguments :\n\n"
                  "- Il existe des outliers (valeurs extrêmes ou aberrantes)\n\n"
                 "- Un écart-type (std) élevé : les données sont donc très dispersées ; avec l'impact des valeurs extrêmes.\n\n"
                 "Dans un deuxième temps, la datavisualisation nous permettra de confirmer les outliers")
        
# Contenu du quatrième onglet : doublons
    with tabs[3]:
        st.markdown(
        """<h3 style='color:#444;'>Doublons</h3>
        <p style='text-align:justify; line-height:1.6;font-size:16px;'>
        </p>
        """, unsafe_allow_html=True
    )
        st.write("")
        st.write("")
        st.markdown('**df.drop_duplicates**')
        st.write("")
        st.markdown("""
                    <ul>
    <span > ==> 3 864 doublons ont été supprimés</span>
</ul>
""", unsafe_allow_html=True)
     



elif page == "Enrichissement" : 
    st.markdown(
    "<h1 style='text-align: center; color:#B22222;'>Enrichissement des données</h4>",
    unsafe_allow_html=True
)

    st.markdown("<br>", unsafe_allow_html=True)

# --- Colonnes équilibrées ---
    col1, col2, col3 = st.columns(3)

# --- Colonne 1 : Variables temporelles ---
    with col1:
        st.markdown(
        """
        <div style="font-size:16px; line-height:1.6; text-align: justify;">
        Pour améliorer la pertinence de la datavisualisation, la date complète a été décomposée en plusieurs composantes temporelles.
        </div>
        """,
        unsafe_allow_html=True
    )

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
        """
        🕒 **Variables temporelles ajoutées :**  
        - **Hour** — heure de l’incident  
        - **Weekday** — jour de la semaine  
        - **Month** — mois de l’année
        """,
        unsafe_allow_html=True
    )

# --- Colonne 2 : Variables météorologiques ---
    with col2:
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.markdown(
        """
        <div style="font-size:16px; line-height:1.6; text-align: justify;">
        Des données météorologiques couvrant la période <b>2009–2024</b> ont été intégrées à partir d’une source ouverte,
        comprenant l’historique jour par jour des conditions météorologiques à Londres.
        </div>
        """,
        unsafe_allow_html=True
    )

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
        """
        ☀️ **Variables météorologiques ajoutées :**  
        - **Meteo** — conditions générales (pluie, soleil, etc.)  
        - **Visibility** — visibilité mesurée
        """,
        unsafe_allow_html=True
    )

# --- Colonne 3 : Variable géographique ---
    with col3:
       st.write("")
       st.write("")
       st.write("")
       st.write("")
       st.write("")
       st.write("")
       st.write("")
       st.write("")
       st.write("")
       st.write("")
       st.write("")
       st.write("")
       st.write("")
       st.markdown(
        """
        <div style="font-size:16px; line-height:1.6; text-align: justify;">
        Une variable géographique a également été créée afin d’identifier si un arrondissement appartient au centre de Londres ou à sa périphérie.
        </div>
        """,
        unsafe_allow_html=True
    )

       st.markdown("<br>", unsafe_allow_html=True)

       st.markdown(
        """
        📍 **Variable géographique ajoutée :**  
        - **Inner_outer**
        """,
        unsafe_allow_html=True
    )

       st.image("Inner_Outer.png", width=400)

elif page == "Datavisualisation":
    st.markdown(
    "<h1 style='text-align: center; color:#B22222;'>Datavisualisation</h1>",
    unsafe_allow_html=True
)

    st.markdown("<br>", unsafe_allow_html=True)

    
    tab1, tab2, tab3 = st.tabs(["Dataviz Univariée", "Dataviz Multivariée", "Heatmap"])

    # Onglet 1 : Dataviz univariée  
    with tab1:
        st.write("")
        option = st.selectbox("Sélectionnez une variable",
    ("Distribution de la variable cible", 
    "Fréquence des incidents", 
    "Evolution des incidents",
    "Retard"))
        st.write("")
        
        if option == "Distribution de la variable cible":
             fig_box = px.box(df, 
                         x="FirstPumpArriving_AttendanceTime")
             fig_box.update_layout(title = {'text' : "Délai d'arrivée du premier camion de pompier", 'font' :{'family': 'Times New Roman', 'color' : 'darkblue', 'size': 18}}, xaxis = {'title' :{'text' : "Délai d'arrivée du premier camion de pompier", 'font' :{'family': 'Times New Roman', 'color' : 'darkblue', 'size': 14}}})
             st.plotly_chart(fig_box)
             st.write("Plusieurs valeurs extrêmes ont été détectées dans les données de temps de réponse.\n")
             st.write("Ces valeurs, trop éloignées de la tendance générale, risquent de perturber les modèles prédictifs.\n")
             st.write("Une détection par la méthode de l’écart interquartile (IQR) a permis d’isoler et de supprimer les observations dont le temps de réponse dépasse 780 secondes, considérées comme des anomalies.\n")
        elif option == "Fréquence des incidents":
             # Seaborn countplot
             import seaborn as sns
             import matplotlib.pyplot as plt
             fig5 = plt.figure()
             ax5 = fig5.add_subplot(111)
             sns.countplot(x = "IncidentGroup", data = df, hue = "IncidentGroup")
             ax5.set_xlabel("type d'incident",fontsize=12, color='darkblue', fontname='Times New Roman')
             ax5.set_ylabel("Nombre d'incidents en milliers",fontsize=12, color='darkblue', fontname='Times New Roman')
             ax5.set_title("Nombre d'incidents par catégorie", fontsize=12, fontweight='bold', color='darkblue', fontname='Times New Roman')
             ax5.set_yticks([500, 1000, 1500, 2000, 2500])
             ax5.set_yticklabels(["12k", "24k", "36k", "48k", "60k"])
             plt.tight_layout()
             st.pyplot(fig5)
             st.write("")
             st.write("Le service spécial regroupe diverses interventions spécifiques qui ne correspondent pas à un incendie classique. Parmi ces types d'interventions, on trouve notamment :\n\n" \
"Conseils simples\n\n" \
"Gestion d’incidents liés aux animaux\n\n" \
"Assistance à une autre caserne\n\n" \
"Évacuation pour des raisons autres qu’un incendie\n\n" \
"Intervention lors d’inondations\n\n" \
"Gestion d’incidents avec ascenseur\n\n" \
"Sauvetage en mer\n\n" \
"Approvisionnement en eau\n\n" \
"Ces catégories permettent de mieux qualifier et segmenter les interventions de la brigade, facilitant ainsi leur analyse.")

        elif option == "Evolution des incidents":
             import plotly.express as px
             inc_year = df.groupby(["CalYear", "IncidentGroup"])["IncidentGroup"].size().reset_index(name="Count")
             fig5 = px.line(inc_year, x="CalYear", y = "Count", color = "IncidentGroup", title = "Nombre d'incidents entre 2009 et 2024",labels = {"CalYear":"années","Count":"nombre"})
             fig5.update_yaxes(tickvals=[50, 100, 150, 200], ticktext=["20k", "50k", "70k", "100k"])
             fig5.update_layout(title = {'text' : "Nombre d'incidents entre 2009 et 2024", 'font' :{'family': 'Times New Roman', 'color' : 'darkblue', 'size': 18}}, xaxis = {'title' :{'text' : "Années", 'font' :{'family': 'Times New Roman', 'color' : 'darkblue', 'size': 14}}}, yaxis = {'title' :{'text' : "Nombre", 'font' :{'family': 'Times New Roman', 'color' : 'darkblue', 'size': 14}}})
             
             st.plotly_chart(fig5)
             st.markdown("On observe une diminution respective du nombre d'incidents en 2020 ; on peut l'associer au **confinement lors de la pandémie COVID-19**.")

             
        elif option == "Retard":
             fig6 = plt.figure()
             sns.countplot(data = df, x="DelayCode_Description", 
              hue = 'DelayCode_Description', legend = False, order = df["DelayCode_Description"].value_counts().index)
             plt.xticks(rotation = 30, ha = 'right', va = 'top')
             plt.title("Distribution de la variable DelayCode_Description",fontsize=11, fontweight='bold', color='darkblue', fontname='Times New Roman')
             plt.xlabel("Motif de retard", color='darkblue', fontname='Times New Roman')
             plt.ylabel("Part relative", color='darkblue', fontname='Times New Roman')
             st.pyplot(fig6)
             st.markdown("On constate que dans 90% des cas il n'y a pas de retard", unsafe_allow_html=True)


    
    # 📈 Onglet 2 : Dataviz multivariée
    with tab2:

        studies = ["Délai de réponse selon le type d'incident", "Temps de trajet selon l'heure de la journée"]
        variable = st.selectbox("##### Sélectionnez une étude multivariée", studies)

        if variable == "Délai de réponse selon le type d'incident":
            fig2, ax2 = plt.subplots()
            sns.violinplot(data=df, x="StopCodeDescription",  y="FirstPumpArriving_AttendanceTime", hue="StopCodeDescription", palette="Set1", ax = ax2)      
            ax2.set_title("Distribution de la variable DelayCode_Description",fontsize=12, fontweight='bold', color='darkblue', fontname='Times New Roman')
            ax2.set_xlabel("Type d'incident", fontsize=10, color='darkblue', fontname='Times New Roman')
            ax2.set_ylabel("Délai de réponse", fontsize=10, color='darkblue', fontname='Times New Roman')
            plt.xticks(rotation = 90)
            plt.tight_layout()
            st.pyplot(fig2)

        

        elif variable == "Temps de trajet selon l'heure de la journée":
            # Calcul de la moyenne du temps de trajet par heure d'appel
             LFB_heure = df.groupby("HourOfCall")["TravelTimeSeconds"].mean().reset_index()

# Création du graphique interactif
             fig4 = px.scatter(
             LFB_heure,
    x="HourOfCall",
    y="TravelTimeSeconds",
    color="TravelTimeSeconds",
    color_continuous_scale="Viridis",  # optionnel : palette de couleurs
    labels={
        "HourOfCall": "Horaire (sur 24h)",
        "TravelTimeSeconds": "Temps de trajet moyen (secondes)"
    }
)
             fig4.update_layout(title = {'text' : "Temps de trajet selon l'heure de la journée", 'font' :{'family': 'Times New Roman', 'color' : 'darkblue', 'size': 18}}, xaxis = {'title' :{'text' : "Horaires", 'font' :{'family': 'Times New Roman', 'color' : 'darkblue', 'size': 14}}},
                                yaxis = {'title' :{'text' : "Temps de trajet", 'font' :{'family': 'Times New Roman', 'color' : 'darkblue', 'size': 14}}})
             

# Affichage dans Streamlit
             st.plotly_chart(fig4)


    # 🔥 Onglet 3 : Heatmap
    with tab3:
        st.header("Heatmap")
        st.write("Carte thermique des corrélations entre variables numériques.")
        #Renommer une variable
        df = df.rename(columns = {"Notional Cost (£)":"National Cost","VISIBILITY_AVG_KM":"Visibility"})
        df["CalYear"] = df["CalYear"].astype(object)
        df["HourOfCall"] = df["HourOfCall"].astype(object)
        df["UPRN"] = df["UPRN"].astype(object)
        df["USRN"] = df["USRN"].astype(object)
        df["Easting_m"] = df["Easting_m"].astype(object)
        df["Northing_m"] = df["Northing_m"].astype(object)
        df["Easting_rounded"] = df["Easting_rounded"].astype(object)
        df["Northing_rounded"] = df["Northing_rounded"].astype(object)
        df["Latitude"] = df["Latitude"].astype(object)
        df["Longitude"] = df["Longitude"].astype(object)
        df["ResourceMobilisationId"] = df["ResourceMobilisationId"].astype(object)
        df["PumpOrder"] = df["PumpOrder"].astype(object)
        df["PerformanceReporting"] = df["PerformanceReporting"].astype(object)
        df["DelayCodeId"] = df["DelayCodeId"].astype(object)
        numeric_df = df.select_dtypes(include='number')  # Sélection des colonnes numériques
        corr = numeric_df.corr()
        fig3, ax3 = plt.subplots(figsize=(9,9))
        sns.heatmap(corr, annot=True, cmap='plasma', ax=ax3)
        st.pyplot(fig3)


elif page == "Preprocessing":
    st.markdown(
    "<h1 style='text-align: center; color:#B22222;'>Préprocessing</h1>",
    unsafe_allow_html=True
)

    st.markdown("<br>", unsafe_allow_html=True)

    tabs = st.tabs(["Split","Frequency Encoding", "OneHotEncoder", "Label Encoding", "Standardisation"])

# Contenu du premier onglet
    with tabs[0]:
        st.header("Split")
        st.write("Le **split** consiste à diviser le jeu de données en deux sous-ensembles :\n\n"
                 "**Jeu d’entraînement** : 80 % des données\n\n"
                 "**Jeu de test** : 20 % des données\n\n"
                 "Le jeu d’entraînement permet d’ajuster le modèle de Machine Learning en déterminant les paramètres qui séparent au mieux les classes.\n\n"
                 "Le jeu de test sert à évaluer les performances du modèle sur des données encore jamais observées, afin de mesurer sa capacité de généralisation.\n\n"
                 )
        st.markdown('<span style="color: #FF6961;">X_train, X_test, y_train, y_test = train_test_split(features, target, test_size = 0.2,random_state = 42)</span>', unsafe_allow_html=True)
        st.write("")
        st.write("")
        st.write("L'étape suivante est l'encodage :\n\n"
        "L’encodage vise à transformer les variables catégorielles en données numériques, car les algorithmes de Machine Learning ne peuvent traiter que des valeurs chiffrées.\n\n"
        "Un type d’encodage approprié est sélectionné en fonction du nombre d’occurrences de chaque variable afin d’optimiser la qualité du modèle.")
        st.write("")
        
# Contenu du 2° onglet    
    with tabs[1]:
        st.header("Frequency Encoding")
        st.write("")
        st.write(
    "Les variables comportant plusieurs centaines de valeurs uniques ont été encodées à l’aide du **frequency encoding**, "
    "afin d’éviter la multiplication des colonnes.\n\n"
    "Cela concerne notamment les variables **DeployedFromStation_Name**, **Easting_rounded** et **Northing_rounded**.\n\n"
    "Les variables **Easting_rounded** et **Northing_rounded**, bien que numériques, représentent des catégories et non des valeurs algébriques. "
    "Elles ont donc été traitées comme des variables catégorielles.\n\n"
    "Ce type d’encodage permet de conserver l’importance relative des modalités les plus fréquentes."
)
        st.write("")
# Contenu du 3° onglet  
    with tabs[2]:
        st.header("OneHotEncoder")
        st.write("")
        st.write("Le **OneHotEncoder** repose sur la création d’un code binaire pour chaque modalité d’une variable catégorielle.\n\n"
                 "Il génère autant de colonnes qu’il existe de valeurs uniques dans la variable initiale.\n\n"
                 "L’encodage est estimé à partir du jeu d’entraînement, puis appliqué à la fois au jeu d’entraînement et au jeu de test afin de garantir la cohérence des données entre les deux ensembles.\n\n"
                 "Ce type d’encodage est particulièrement adapté aux variables présentant entre 10 et 16 occurrences distinctes, telles que :\n\n"
                 "- **StopCodeDescription**\n\n"
                 "- **PropertyCategory**")
        
# Contenu du 4° onglet   
    with tabs[3]:
        st.header("Label Encoding")
        st.write("")
        st.write("Certaines variables sélectionnées présentent des modalités possédant un ordre hiérarchique.\n\n"
                 "Pour ces variables, un encodage ordinal a été appliqué afin de préserver la notion d’ordre entre les différentes catégories.\n\n"
                 "Cet encodage a été utilisé pour les variables suivantes :\n\n"
                 "- **Meteo**\n\n"
                 "- **Visibility**")
        
# Contenu du 5° onglet
    with tabs[4]:
        st.header("Standardisation")
        st.write("Les modèles de Machine Learning sont sensibles aux *différences d’échelle* entre les variables.\n\n"
                 "Afin d’éviter tout biais lié à ces écarts de grandeur, une standardisation des données a été appliquée.\n\n"
                 "Cette étape permet de centrer les variables autour de la moyenne et de les réduire selon leur écart-type, garantissant ainsi une influence équilibrée de chaque variable sur le modèle.\n\n"
                 "La fonction utilisée pour cette transformation est **StandardScaler** du module **scikit-learn**.")

        
         

#Page - Modélisation
elif page == "Modélisation":
    st.markdown(
    "<h1 style='text-align: center; color:#B22222;'>Modélisation</h1>",
    unsafe_allow_html=True
)

    st.markdown("<br>", unsafe_allow_html=True)

    st.write("La variable cible étant continue, l’apprentissage a d’abord été orienté vers des modèles de régression.\n\n"
             "Pour évaluer et comparer la performance prédictive de ces modèles, les métriques suivantes ont été retenues :\n\n")
# Graphique de régression (affichage de la relation entre la cible et une feature)
    with st.expander("**MODELES DE REGRESSION**"):
        choix = st.radio("Sélectionnez un modèle",["Linear Regression", "Decision Tree Regressor", "Random Forest Regressor", "SGD Regressor", "KNN Regressor","Tableau comparatif"])  
        
        if choix == "Linear Regression":
            st.markdown("""
        <div style="text-align: center;">
            <h4><b>LINEAR REGRESSION</b></h4>
            <p><b>Mean Absolute Error = 89.72</b></p>
            <p><b>Mean Squared Error = 14049.17</b></p>
            <p><b>Root Mean Squared Error = 118.53</b></p>
            <p><b>R² Score = 118.53</b></p>
        </div>
    """, unsafe_allow_html=True)
            
        if choix == "Decision Tree Regressor":
            st.markdown("""
        <div style="text-align: center;">
            <h4><b>DECISION TREE REGRESSOR</b></h4>
            <p><b>Mean Absolute Error = 207.25</b></p>
            <p><b>Mean Squared Error = 63919.10</b></p>
            <p><b>Root Mean Squared Error = 252.82</b></p>
            <p><b>R² Score = -3.32</b></p>
        </div>
    """, unsafe_allow_html=True)
            
        if choix == "Random Forest Regressor":
            st.markdown("""
        <div style="text-align: center;">
            <h4><b>RANDOM FOREST REGRESSOR</b></h4>
            <p><b>Mean Absolute Error = 88.15</b></p>
            <p><b>Mean Squared Error = 13649.74 </b></p>
            <p><b>Root Mean Squared Error = 116.83</b></p>
            <p><b>R² Score = 0.08</b></p>
        </div>
    """, unsafe_allow_html=True)
            
        if choix == "SGD Regressor":
            st.markdown("""
        <div style="text-align: center;">
            <h4><b>SGD REGRESSOR</b></h4>
            <p><b>Mean Absolute Error = 2.20e14 </b></p>
            <p><b>Mean Squared Error = 4.92e30</b></p>
            <p><b>Root Mean Squared Error = 2.22e15</b></p>
            <p><b>R² Score = 3.32e26</b></p>
        </div>
    """, unsafe_allow_html=True)
            st.write("")
            st.write("")
            st.write("")
            image = Image.open("SGD_REGRESSOR.png")
            col1, col2, col3 = st.columns([1, 1.5, 1])
            with col2:
                st.image(image, width=500)
            
            
        if choix == "KNN Regressor":
            st.markdown("""
        <div style="text-align: center;">
            <h4><b>KNN REGRESSOR</b></h4>
            <p><b>Mean Absolute Error = 94.11</b></p>
            <p><b>Mean Squared Error = 15144</b></p>
            <p><b>Root Mean Squared Error = 123.06</b></p>
            <p><b>R² Score = -0.02</b></p>
        </div>
    """, unsafe_allow_html=True)

        if choix == "Tableau comparatif":
            data = [[89.72, "14049.17", 118.53, 0.05], [207.25, "63919.10", 252.82, -3.32], [88.15, "13649.74", 116.83, 0.08],["2.20e14", "4.92e30", "2.22e15", "3.32e26"],[94.11, "15144", 123.06, -0.02]]  
            df = pd.DataFrame(data, columns = ["MAE", "MSE", "RMSE", "R2"], index =["Linear Regression", "Decision Tree Regressor", "Random Forest Regressor", "SGD Regressor", "KNN Regressor"])
        
            table_html = df.to_html(classes='custom-table', border=0)

            st.markdown("""<style>.custom-table {
             width: 80%;  margin-left: auto; margin-right: auto; font-size: 14px;
        border-collapse: collapse;
    }.custom-table th, .custom-table td {
        padding: 8px 12px;
        border: 1px solid #ccc;
        text-align: center;
    }</style>
""", unsafe_allow_html=True)
            st.markdown(table_html, unsafe_allow_html=True)

        

        
# Classification binaire
        
    with st.expander("**MODELES DE CLASSIFICATION BINAIRE**"):
        st.write("Aucun modèle de régression n’a permis d’obtenir des performances satisfaisantes, malgré différentes tentatives d’optimisation.\n\n"
                 "Une seconde approche a donc été mise en place en optant pour des modèles de classification binaire.\n\n"
                 "Les classes de la variable cible ont été définies à partir d’un seuil de 6 minutes, correspondant au critère retenu dans le plan d’intervention de la LFB.\n\n")
        choix = st.radio("Sélectionnez un modèle",["Logistic Regression", "Decision Tree Classifier", "Random Forest Classifier", "XGB Classifier", "KNN Classifier","Linear SVC","Tableau comparatif et importance des variables"])  
    
        if choix == "Logistic Regression":
            st.markdown("""
        <div style="text-align: center;">
            <h4><b>LOGISTIC REGRESSION</b></h4>
            <p><b>Accuracy = 0.71</b></p>
            <p><b>Precision classe 0 = 0.54</b></p>
            <p><b>Precision classe 1 = 0.71</b></p>
            <p><b>Recall classe 0 = 0.00</b></p>
            <p><b>Recall classe 1 = 1.00</b></p>
                        <p><b>F1-score classe 0 = 0.00</b></p>
            <p><b>F1-score classe 1 = 0.83</b></p>
        </div>
    """, unsafe_allow_html=True)
            
        if choix == "Decision Tree Classifier":
            st.markdown("""
        <div style="text-align: center;">
            <h4><b>DECISION TREE CLASSIFIER</b></h4>
            <p><b>Accuracy= 0.70</b></p>
            <p><b>Precision classe 0 = 0.49</b></p>
            <p><b>Precision classe 1 = 0.79 </b></p>
            <p><b>Recall classe 0 = 0.49</b></p>
            <p><b>Recall classe 1 = 0.79</b></p>
                        <p><b>F1-score classe 0 = 0.49</b></p>
            <p><b>F1-score classe 1 = 0.79</b></p>
        </div>
    """, unsafe_allow_html=True)
            
        if choix == "Random Forest Classifier":
           st.markdown("""
        <div style="text-align: center;">
            <h4><b>RANDOM FOREST CLASSIFIER</b></h4>
            <p><b>Accuracy= 0.74</b></p>
            <p><b>Precision classe 0 = 0.61 </b></p>
            <p><b>Precision classe 1 = 0.77 </b></p>
            <p><b>Recall classe 0 = 0.31</b></p>
            <p><b>Recall classe 1 = 0.92</b></p>
                        <p><b>F1-score classe 0 = 0.41</b></p>
            <p><b>F1-score classe 1 = 0.84</b></p>
        </div>
    """, unsafe_allow_html=True)
            
            
        if choix == "XGB Classifier":
            st.markdown("""
       <div style="text-align: center;">
            <h4><b>XGB CLASSIFIER</b></h4>
            <p><b>Accuracy= 0.73</b></p>
            <p><b>Precision classe 0 = 0.68 </b></p>
            <p><b>Precision classe 1 = 0.74 </b></p>
            <p><b>Recall classe 0 = 0.15</b></p>
            <p><b>Recall classe 1 = 0.97</b></p>
                        <p><b>F1-score classe 0 = 0.24  </b></p>
            <p><b>F1-score classe 1 = 0.84</b></p>
        </div>
    """, unsafe_allow_html=True)
            
        if choix == "KNN Classifier":
            st.markdown("""
       <div style="text-align: center;">
            <h4><b>KNN CLASSIFIER</b></h4>
            <p><b>Accuracy= 0.69</b></p>
            <p><b>Precision classe 0 = 0.37 </b></p>
            <p><b>Precision classe 1 = 0.72 </b></p>
            <p><b>Recall classe 0 = 0.09</b></p>
            <p><b>Recall classe 1 = 0.93</b></p>
                        <p><b>F1-score classe 0 = 0.15      </b></p>
            <p><b>F1-score classe 1 = 0.81</b></p>
        </div>
    """, unsafe_allow_html=True)
            
        if choix == "Linear SVC":
            st.markdown("""
       <div style="text-align: center;">
            <h4><b>LINEAR SVC</b></h4>
            <p><b>Accuracy= 0.71</b></p>
            <p><b>Precision classe 0 = 0.59 </b></p>
            <p><b>Precision classe 1 = 0.71 </b></p>
            <p><b>Recall classe 0 = 0.00</b></p>
            <p><b>Recall classe 1 = 1.00</b></p>
                        <p><b>F1-score classe 0 = 0.01</b></p>
            <p><b>F1-score classe 1 = 0.83</b></p>
        </div>
    """, unsafe_allow_html=True)

        if choix == "Tableau comparatif et importance des variables":
            st.write("")
            st.write("")
            data = [
        [0.71, 0.54, 0.71, 0.00, 1.00, 0.00, 0.83],
        [0.70, 0.49, 0.79, 0.49, 0.79, 0.49, 0.79],
        [0.74, 0.61, 0.77, 0.31, 0.92, 0.41, 0.84],
        [0.73, 0.68, 0.74, 0.15, 0.97, 0.24, 0.84],
        [0.69, 0.37, 0.72, 0.09, 0.93, 0.15, 0.81],
        [0.71, 0.59, 0.71, 0.00, 1.00, 0.01, 0.83]]
            df2 = pd.DataFrame(data,columns=[
            "Accuracy",
            "Precision Classe 0", "Precision Classe 1",
            "Recall Classe 0", "Recall Classe 1",
            "F1 Score Classe 0", "F1 Score Classe 1"],index=[
            "Logistic Regression", "Decision Tree Classifier",
            "Random Forest Classifier", "XGB Classifier",
            "KNN Classifier", "Linear SVC"])
         
            st.markdown(f"""
<div class="scrollable-table-container">
{df2.to_html(classes='custom-table', index=True)}
</div>
""", unsafe_allow_html=True)
    
            
# Classification multi-classes
    with st.expander("## **MODELES DE CLASSIFICATION MULTI-CLASSES**"):
        st.write("La variable cible a été segmentée en fonction de ses quartiles, afin d’obtenir des échantillons de taille comparable.\n\n"
                 "Cette démarche vise à améliorer la performance du modèle en assurant un équilibre entre les classes.\n\n"
                 "Pour faciliter l’interprétation, les valeurs des quartiles ont été arrondies à la minute la plus proche.")
        
        st.markdown("""
                    <div style="text-align: center;">
    <h5><u><strong>Répartition des classes</strong></u></h4>
</div>
<div style="text-align: center; color:#FF6961">
    <p><b>Classe 0</b> : ≤ à 4 minutes (28.66%)</p>
    <p><b>Classe 1</b> : entre 4 et 5 minutes (23.20%)</p>
    <p><b>Classe 2</b> : entre 5 et 6 minutes 30 secondes (6.43%)</p>
    <p><b>Classe 3</b> : entre 6 minutes 30 secondes et 13 minutes (21.71%)</p>
</div>
""", unsafe_allow_html=True)
            
        choix = st.radio("Sélectionnez un modèle",["Logistic Regression multi-classes", "Decision Tree Classifier multi-classes", "Random Forest Classifier multi-classes", "XGB Classifier multi-classes", "KNN Classifier multi-classes","Tableau comparatif et importance des variables multi-classes"])  
    
        st.write("")
        st.write("")
        st.write("")
        if choix == "Logistic Regression multi-classes":
            st.markdown("""
        <div style="text-align: center;">
            <h4><b>Logistic Regression</b></h4>""", unsafe_allow_html=True)
            col1,col2,col3, col4= st.columns(4)
            with col1 :
                 st.write("")
                 st.write("")
                 st.markdown("""                        
            <p><b>Accuracy = 0.32</b></p>
                             </div>
    """, unsafe_allow_html=True)
            with col2 :
                 st.markdown("""
            <p><b>Precision classe 0 = 0.33</b></p>
            <p><b>Precision classe 1 = 0.25</b></p>
                        <p><b>Precision classe 2 = 0.30</b></p>
                             <p><b>Precision classe 3 = 0.32</b></p>
                             </div>
    """, unsafe_allow_html=True)
            with col3:
                        st.markdown("""
            <p><b>Recall classe 0 = 0.67</b></p>
                        <p><b>Recall classe 1 = 0.00</b></p>
                        <p><b>Recall classe 2 = 0.34</b></p>
                        <p><b>Recall classe 3 = 0.19</b></p></div>
    """, unsafe_allow_html=True)
            with col4:
                        st.markdown("""
                        <p><span style='color: #FF6961; font-weight: bold;'>F1-score classe 0 = 0.44</span><p>
                        <p><span style='color: #FF6961; font-weight: bold;'>F1-score classe 1 = 0.00</span><p>
                  <p><span style='color: #FF6961; font-weight: bold;'>F1-score classe 2 = 0.32</span><p>
                   <p><span style='color: #FF6961; font-weight: bold;'>F1-score classe 3 = 0.24</span><p>
        </div>
    """, unsafe_allow_html=True)
            
        if choix == "Decision Tree Classifier multi-classes":
            st.markdown("""
        <div style="text-align: center;">
            <h4><b>Decision Tree Classifier</b></h4>""", unsafe_allow_html=True)
            col1,col2,col3, col4= st.columns(4)
            with col1 :
                 st.write("")
                 st.write("")
                 st.markdown("""                        
            <p><b>Accuracy = 0.40</b></p>
                             </div>
    """, unsafe_allow_html=True)
            with col2 :
                 st.markdown("""
            <p><b>Precision classe 0 = 0.51</b></p>
            <p><b>Precision classe 1 = 0.31</b></p>
                        <p><b>Precision classe 2 = 0.35</b></p>
                             <p><b>Precision classe 3 = 0.41</b></p>
                             </div>
    """, unsafe_allow_html=True)
            with col3:
                        st.markdown("""
            <p><b>Recall classe 0 = 0.51</b></p>
                        <p><b>Recall classe 1 = 0.31</b></p>
                        <p><b>Recall classe 2 = 0.35</b></p>
                        <p><b>Recall classe 3 = 0.40</b></p></div>
    """, unsafe_allow_html=True)
            with col4:
                        st.markdown("""
                        <p><span style='color: #FF6961; font-weight: bold;'>F1-score classe 0 = 0.51</span><p>
                        <p><span style='color: #FF6961; font-weight: bold;'>F1-score classe 1 = 0.13</span><p>
                  <p><span style='color: #FF6961; font-weight: bold;'>F1-score classe 2 = 0.36</span><p>
                   <p><span style='color: #FF6961; font-weight: bold;'>F1-score classe 3 = 0.40</span><p>
        </div>
    """, unsafe_allow_html=True)
            
        if choix == "Random Forest Classifier multi-classes":
            st.markdown("""
        <div style="text-align: center;">
            <h4><b>Random Forest Classifier</b></h4>""", unsafe_allow_html=True)
            col1,col2,col3, col4= st.columns(4)
            with col1 :
                 st.write("")
                 st.write("")
                 st.markdown("""                        
            <p><b>Accuracy = 0.42</b></p>
                             </div>
    """, unsafe_allow_html=True)
            with col2 :
                 st.markdown("""
            <p><b>Precision classe 0 = 0.50</b></p>
            <p><b>Precision classe 1 = 0.33</b></p>
                        <p><b>Precision classe 2 = 0.37</b></p>
                             <p><b>Precision classe 3 = 0.45</b></p>
                             </div>
    """, unsafe_allow_html=True)
            with col3:
                        st.markdown("""
            <p><b>Recall classe 0 = 0.60</b></p>
                        <p><b>Recall classe 1 = 0.27</b></p>
                        <p><b>Recall classe 2 = 0.37</b></p>
                        <p><b>Recall classe 3 = 0.41</b></p></div>
    """, unsafe_allow_html=True)
            with col4:
                        st.markdown("""
                        <p><span style='color: #FF6961; font-weight: bold;'>F1-score classe 0 = 0.55</span><p>
                        <p><span style='color: #FF6961; font-weight: bold;'>F1-score classe 1 = 0.30</span><p>
                  <p><span style='color: #FF6961; font-weight: bold;'>F1-score classe 2 = 0.37</span><p>
                   <p><span style='color: #FF6961; font-weight: bold;'>F1-score classe 3 = 0.43</span><p>
        </div>
    """, unsafe_allow_html=True)
            
            
        if choix == "XGB Classifier multi-classes":
            st.markdown("""
        <div style="text-align: center;">
            <h4><b>RXGB Classifierr</b></h4>""", unsafe_allow_html=True)
            col1,col2,col3, col4= st.columns(4)
            with col1 :
                 st.write("")
                 st.write("")
                 st.markdown("""                        
            <p><b>Accuracy = 0.42</b></p>
                             </div>
    """, unsafe_allow_html=True)
            with col2 :
                 st.markdown("""
            <p><b>Precision classe 0 = 0.39</b></p>
            <p><b>Precision classe 1 = 0.42</b></p>
                        <p><b>Precision classe 2 = 0.36</b></p>
                             <p><b>Precision classe 3 = 0.35</b></p>
                             </div>
    """, unsafe_allow_html=True)
            with col3:
                        st.markdown("""
            <p><b>Recall classe 0 = 0.41</b></p>
                        <p><b>Recall classe 1 = 0.66</b></p>
                        <p><b>Recall classe 2 = 0.08</b></p>
                        <p><b>Recall classe 3 = 0.38</b></p></div>
    """, unsafe_allow_html=True)
            with col4:
                        st.markdown("""
                        <p><span style='color: #FF6961; font-weight: bold;'>F1-score classe 0 = 0.51</span><p>
                        <p><span style='color: #FF6961; font-weight: bold;'>F1-score classe 1 = 0.13</span><p>
                  <p><span style='color: #FF6961; font-weight: bold;'>F1-score classe 2 = 0.36</span><p>
                   <p><span style='color: #FF6961; font-weight: bold;'>F1-score classe 3 = 0.40</span><p>
        </div>
    """, unsafe_allow_html=True)
            
            
        if choix == "KNN Classifier multi-classes":
            st.markdown("""
        <div style="text-align: center;">
            <h4><b>KNN Classifier</b></h4>""", unsafe_allow_html=True)
            
            col1,col2,col3, col4= st.columns(4)
            with col1 :
                 st.write("")
                 st.write("")
                 st.markdown("""                        
            <p><b>Accuracy = 0.28</b></p>
                             </div>
    """, unsafe_allow_html=True)
            with col2 :
                 st.markdown("""
            <p><b>Precision classe 0 = 0.31</b></p>
            <p><b>Precision classe 1 = 0.24</b></p>
                        <p><b>Precision classe 2 = 0.28</b></p>
                             <p><b>Precision classe 3 = 0.27</b></p>
                             </div>
    """, unsafe_allow_html=True)
            with col3:
                        st.markdown("""
            <p><b>Recall classe 0 = 0.45</b></p>
                        <p><b>Recall classe 1 = 0.21</b></p>
                        <p><b>Recall classe 2 = 0.23</b></p>
                        <p><b>Recall classe 3 = 0.20</b></p></div>
    """, unsafe_allow_html=True)
            with col4:
                        st.markdown("""
                        <p><span style='color: #FF6961; font-weight: bold;'>F1-score classe 0 = 0.37</span><p>
                        <p><span style='color: #FF6961; font-weight: bold;'>F1-score classe 1 = 0.22</span><p>
                  <p><span style='color: #FF6961; font-weight: bold;'>F1-score classe 2 = 0.25</span><p>
                   <p><span style='color: #FF6961; font-weight: bold;'>F1-score classe 3 = 0.23</span><p>
        </div>
    """, unsafe_allow_html=True)
            

        if choix == "Tableau comparatif et importance des variables multi-classes":
    
            st.write("")
            data = [[0.32, 0.33, 0.25, 0.30,0.32,0.67,0.00,0.34,0.19,0.44,0.00,0.32,0.24], [0.40, 0.51, 0.31, 0.35,0.41,0.51,0.32,0.35,0.40, 0.51,0.31,0.35,0.40],[0.42,0.50,0.33,0.37,0.45,0.60,0.27,0.37,0.41,0.55,0.3,0.37,0.43],[0.39, 0.42, 0.36,0.35,0.41, 0.66,0.08,0.38,0.39,0.51,0.13,0.36,0.40],[0.28, 0.31, 0.24, 0.28, 0.27,0.45,0.21,0.23,0.20,0.37,0.22,0.25,0.23]]  
            df3= pd.DataFrame(data, columns = ["ACCURACY", "PRECISION  Classe 0", "PRECISION Classe 1","PRECISION Classe 2","PRECISION Classe 3", "RECALL Classe 0", "RECALL Classe 1", "RECALL Classe 2", "RECALL Classe 3","F1 SCORE Classe 0","F1 SCORE Classe 1","F1 SCORE Classe 2","F1 SCORE Classe 3"], index =["Logistic Regression", "Decision Tree Classifier", "Random Forest Classifier", "XGB Classifier", "KNN Classifier"])
            df3_transposed = df3.T    
            st.markdown(df3_transposed.to_html(classes='medium-table'), unsafe_allow_html=True)
            st.markdown("""
        <style>
        .medium-table {
            font-size: 13px;
            text-align: center;
            margin-top: 10px;
            border-collapse: collapse;
        }
        .medium-table th, .medium-table td {
            padding: 6px 10px;
            border: 1px solid #ccc;
        }
        </style>
    """, unsafe_allow_html=True)
       
    

    with st.expander("🎯 **MODELES OPTIMISES**"):
        st.write("")
        st.markdown("Une recherche d’hyperparamètres a été effectuée à l’aide de **GridSearch** combiné à une **validation croisée** afin d’optimiser les performances du modèle.\n\n"
                    "Les hyperparamètres retenus sont :")
        st.write("")
        st.markdown("Les hyperparamètres retenus sont :\n\n"
                    "- **max_depth = 20** : profondeur maximale de l’arbre limitée à 20 nœuds.\n\n"
                    "- **min_samples_split = 10** : nombre minimum de 10 échantillons requis pour diviser un nœud.\n\n")
        st.markdown("Pour ce jeu de données déséquilibré, la métrique la plus pertinente est le F1-score, qui reflète au mieux la qualité des prédictions positives.\n\n"
                     "À partir de cette configuration et de l’analyse de l’impact des variables explicatives, les 6 variables les plus importantes ont été conservées pour le modèle final optimisé.", unsafe_allow_html=True
)
        st.markdown("Il reflète le mieux la qualité des prédictions positives.")   
        st.write("")
        st.markdown("A partir de cette configuration de l'impact des variables explicatives," "nous avons décidé de garder les <span style='color: #FF6961; font-weight: bold;'> 6 premières variables les plus importantes</span> "  " dans le modèle optimisé final", unsafe_allow_html=True)

# Afficher le tableau avec style
        
        st.write("")
        st.write("")
        st.write("")
        col1,col2,col3= st.columns(3)
        with col1 :
            st.image("Importance variables.png",width=600)
            st.write("")
              
        
        choix = st.radio("Sélectionnez un modèle",["Decision Tree Classifier multi-classes", "Random Forest Classifier multi-classes","Tableau comparatif"])  
    
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        if choix == "Decision Tree Classifier multi-classes":
            st.markdown("""
        <div style="text-align: center;">
            <h4><b>DECISION TREE CLASSIFIER MUTLI-CLASSES</b></h4>""", unsafe_allow_html=True)

            col1,col2,col3, col4= st.columns(4)
            with col1 :
                 st.write("")
                 st.write("")
                 st.markdown("""                        
            <p><b>Accuracy = 0.44</b></p>
                             </div>
    """, unsafe_allow_html=True)
            with col2 :
                 st.markdown("""
            <p><b>Precision classe 0 = 0.51</b></p>
            <p><b>Precision classe 1 = 0.34</b></p>
                        <p><b>Precision classe 2 = 0.38</b></p>
                             <p><b>Precision classe 3 = 0.51</b></p>
                             </div>
    """, unsafe_allow_html=True)
            with col3:
                        st.markdown("""
            <p><b>Recall classe 0 = 0.65</b></p>
                        <p><b>Recall classe 1 = 0.28</b></p>
                        <p><b>Recall classe 2 = 0.41</b></p>
                        <p><b>Recall classe 3 = 0.37</b></p></div>
    """, unsafe_allow_html=True)
            with col4:
                        st.markdown("""
                        <p><span style='color: #FF6961; font-weight: bold;'>F1-score classe 0 = 0.57</span><p>
                        <p><span style='color: #FF6961; font-weight: bold;'>F1-score classe 1 = 0.31</span><p>
                  <p><span style='color: #FF6961; font-weight: bold;'>F1-score classe 2 = 0.39</span><p>
                   <p><span style='color: #FF6961; font-weight: bold;'>F1-score classe 3 = 0.43</span><p>
        </div>
    """, unsafe_allow_html=True)
            
        if choix == "Random Forest Classifier multi-classes":
            st.markdown("""
        <div style="text-align: center;">
            <h4><b>RANDOM FOREST CLASSIFIER MUTLI-CLASSES</b></h4> """, unsafe_allow_html=True)

            col1,col2,col3, col4= st.columns(4)
            with col1 :
                 st.write("")
                 st.write("")
                 st.markdown("""                        
            <p><b>Accuracy = 0.47</b></p>
                             </div>
    """, unsafe_allow_html=True)
            with col2 :
                 st.markdown("""
            <p><b>Precision classe 0 = 0.56</b></p>
            <p><b>Precision classe 1 = 0.36</b></p>
                        <p><b>Precision classe 2 = 0.40</b></p>
                             <p><b>Precision classe 3 = 0.51</b></p>
                             </div>
    """, unsafe_allow_html=True)
            with col3:
                        st.markdown("""
            <p><b>Recall classe 0 = 0.65</b></p>
                        <p><b>Recall classe 1 = 0.32</b></p>
                        <p><b>Recall classe 2 = 0.40</b></p>
                        <p><b>Recall classe 3 = 0.46</b></p></div>
    """, unsafe_allow_html=True)
            with col4:
                        st.markdown("""
                        <p><span style='color: #FF6961; font-weight: bold;'>F1-score classe 0 = 0.60</span><p>
                        <p><span style='color: #FF6961; font-weight: bold;'>F1-score classe 1 = 0.33</span><p>
                  <p><span style='color: #FF6961; font-weight: bold;'>F1-score classe 2 = 0.40</span><p>
                   <p><span style='color: #FF6961; font-weight: bold;'>F1-score classe 3 = 0.49</span><p>
        </div>
    """, unsafe_allow_html=True)
                
        if choix == "Tableau comparatif":
            st.write("")
            st.write("")
            col1, col2 = st.columns([1,1])
            with col1:
                st.markdown("<h5 style='margin-bottom: 10px;'>Decision Tree Classifier</h5>", unsafe_allow_html=True)
                data = [[0.44, 0.51, 0.65, 0.57], [0.44, 0.34, 0.28, 0.31], [0.44, 0.38, 0.41, 0.39],[0.44, 0.51, 0.37, 0.43]]  
                df4 = pd.DataFrame(data, columns = ["ACCURACY", "PRECISION", "RECALL", "F1 SCORE"], index =["Classe 0", "Classe 1", "Classe 2", "Classe 3"])
            
                
                def style_row(row):
                   html = "<tr>"
                   for col in df4.columns:
                        value = row[col]
                        if col == "F1 SCORE":
                            html += f"<td style='color:red; font-weight:bold; font-size:18px; text-align:center'>{value:.2f}</td>"
                        else:
                            html += f"<td style='font-size:16px; text-align:center'>{value:.2f}</td>"
                   html += "</tr>"
                   return html

# Génération du tableau HTML complet
                table_html = """
<style>
.custom-table {
    border-collapse: collapse;
    width: 100%;
}
.custom-table th {
    background-color: #f0f0f0;
    font-weight: bold;
    font-size: 18px;
    padding: 10px;
    text-align: center;
}
.custom-table td {
    padding: 10px;
    border: 1px solid #ccc;
}
</style>
<table class='custom-table'>
<tr>
    <th></th>
    <th>ACCURACY</th>
    <th>PRECISION</th>
    <th>RECALL</th>
    <th>F1 SCORE</th>
</tr>
"""
                for idx, row in df4.iterrows():
                   table_html += f"<tr><th style='text-align:center'>{idx}</th>" + style_row(row)[4:]  # Retirer <tr>
                table_html += "</table>"

# Affichage
                st.markdown(table_html, unsafe_allow_html=True)

            with col2:
                st.markdown("<h5 style='margin-bottom: 10px;'>Random Forest Classifier</h5>", unsafe_allow_html=True)
                data = [[0.47, 0.56, 0.65, 0.60], [0.47, 0.36, 0.32, 0.33], [0.47, 0.40, 0.40, 0.40],[0.47, 0.51, 0.46, 0.49]]  
                df5 = pd.DataFrame(data, columns = ["ACCURACY", "PRECISION", "RECALL", "F1 SCORE"], index =["Classe 0", "Classe 1", "Classe 2", "Classe 3"])
                
                def style_row(row):
                   html = "<tr>"
                   for col in df5.columns:
                        value = row[col]
                        if col == "F1 SCORE":
                            html += f"<td style='color:red; font-weight:bold; font-size:18px; text-align:center'>{value:.2f}</td>"
                        else:
                            html += f"<td style='font-size:16px; text-align:center'>{value:.2f}</td>"
                   html += "</tr>"
                   return html

# Génération du tableau HTML complet
                table_html = """
<style>
.custom-table {
    border-collapse: collapse;
    width: 100%;
}
.custom-table th {
    background-color: #f0f0f0;
    font-weight: bold;
    font-size: 18px;
    padding: 10px;
    text-align: center;
}
.custom-table td {
    padding: 10px;
    border: 1px solid #ccc;
}
</style>
<table class='custom-table'>
<tr>
    <th></th>
    <th>ACCURACY</th>
    <th>PRECISION</th>
    <th>RECALL</th>
    <th>F1 SCORE</th>
</tr>
"""
                for idx, row in df5.iterrows():
                   table_html += f"<tr><th style='text-align:center'>{idx}</th>" + style_row(row)[4:]  
                table_html += "</table>"
# Affichage
                st.markdown(table_html, unsafe_allow_html=True)

    

# Page - Conclusion    


elif page == "Conclusion":
    # 🌟 Titre principal centré
    st.markdown(
        "<h1 style='text-align:center; color:#B22222;'>Conclusion métier</h1>",
        unsafe_allow_html=True
    )


    # 🌟 Texte principal avec mise en forme soignée
    st.markdown(
        """
        <div style="text-align: justify; font-size: 16px; line-height: 1.6;">
        <p>Pour conclure, nous pouvons tirer plusieurs enseignements utiles à la brigade :</p>

        <ul>
            <li>Les <b>formulaires</b> contiennent une grande quantité d’informations dont beaucoup se répètent 
            (plus de 25 colonnes relatives aux données GPS des incidents).</li>
            <li>Les temps de réponse sont <b>dans 75 % des cas inférieurs à 6 minutes</b>.</li>
        </ul>

        <p>En <b>France</b>, toutes régions confondues, le délai moyen d’intervention des pompiers après un appel est 
        d’environ <b>13 minutes</b>.<br>
        À <b>Paris</b>, il est de <b>7 minutes</b>, avec un objectif clair : rester sous la barre des <b>10 minutes</b>.</p>

        <p>Il est essentiel d’inscrire l’analyse de ces données dans une démarche de 
        <b>réévaluation et d’amélioration continue</b>, afin de toujours garantir la 
        <b>sécurité des biens et des personnes</b>.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 🧱 Espace avant image
    st.write("")
    st.write("")

    # Image finale centrée
    image = Image.open("Pompiers.png")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(image, width=250)

st.markdown(
    """
    <style>
    div[data-testid="stVerticalBlock"] div[data-testid="stBlock"] {
        background-color: #fff8f8;
        border-radius: 8px;
        padding: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

