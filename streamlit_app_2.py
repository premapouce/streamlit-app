import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px



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
pages = ["Introduction", "Distribution", "Enrichissement", "Datavisualisation","Preprocessing", "Modélisation","Conclusion"]
page = st.sidebar.radio("Aller vers", pages)

# Affichage de l'image principale
st.image("Lfb_logo.jpg", width=75)

# === Page - Introduction ===


if page == "Introduction":
    st.title("Temps de réponse des pompiers (LFB)")
    st.header("Introduction")
    st.markdown(
        "La London Fire Brigade (LFB) met à disposition sur son site officiel les données relatives aux incidents enregistrés depuis janvier 2009, ainsi que les informations concernant les camions de pompiers envoyés sur les lieux des incidents.  \n\n"
        "Ce rapport est basé sur l’exploration et le traitement de ces données dans le but d’analyser et d’estimer le temps de réaction de la LFB.  \n\n"
        "Les casernes de pompiers de la LFB sont stratégiquement situées pour atteindre un délai moyen d'intervention inférieur ou égal à 6 minutes.  \n\n"
        "L’objectif de ce projet est d’analyser les temps de réponse de la brigade des pompiers de Londres et éventuellement prédire ces temps de réponses.")
    

elif page == "Distribution":
    @st.cache_data
    def analyser_df(df):
        return pd.DataFrame({
        '% NaN': df.isna().mean() * 100,
        'Nb valeurs uniques': df.nunique()})

    def get_value_counts(df, column, top_n=20):
        value_counts = df[column].value_counts(dropna=False).head(top_n)
        value_counts_df = value_counts.reset_index()
        value_counts_df.columns = [column, 'Nombre']
        value_counts_df['%'] = (value_counts_df['Nombre'] / value_counts_df['Nombre'].sum()) * 100
        return value_counts_df

# Analyse des données
    resultats = analyser_df(df)
    st.dataframe(resultats)

# Sélection d'une variable
    st.markdown("##### Sélectionnez une variable catégorielle :")
    variable = st.selectbox("Variable", df.columns)

    if variable:
        st.write(f"#### Distribution de la variable : {variable}")

    # Affichage de la distribution
        count_data = get_value_counts(df, variable, top_n=20)
        st.dataframe(count_data)


elif page == "Enrichissement" : 
    st.markdown("<h1 style='text-align: center;'>Enrichissement des données</h1>", unsafe_allow_html=True)
    st.image("Lfb_logo.jpg", width=100)
    col1, col2, col3 = st.columns(3)
    with col1 :
        st.write("Pour faciliter la pertinence de la datavisualisation, nous avons segmenté la date complète avec de nouvelles variables.\n\n"
         "🕒   Ajout de variables temporelles :\n\n"
                 "- **Hour**\n\n"
                 "- **Weekday**\n\n"
                 "- **Month**\n\n")
       

    with col2 :   
         st.write("")
         st.write("")
         st.write("")
         st.write("")
         st.write("")
         st.write("")
        
         st.write("")
         st.write("Nous avons récupéré des données météorologiques pour la période qui nous concerne (2009-2024) depuis une source de données mise en accès libre (fichiers excel de l'historique jour par jour de la météo sur Londres).\n\n"
                 "☀️  Nouvelles variables météorologiques :\n\n"
                 "- **Meteo**\n\n"
                 "- **Visibility**\n\n")
        
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
        st.write("")
        st.write("")
        st.write("📍 Dernier ajout : une variable géographique qui permet d'identifier si l'arrondissement est du centre de Londres ou en périphérie\n\n"
                 "- **Inner_outer**")
        st.write("")
        st.image("Inner_Outer.png", width = 400)



elif page == "Datavisualisation":
    st.header("Datavisualisation")
    st.write("### Visualisation interactive des variables ")
    tab1, tab2, tab3 = st.tabs(["Dataviz Univariée", "Dataviz Multivariée", "Heatmap"])
    with tab1:
        st.header("Dataviz Univariée")
        st.write("Pour faciliter la pertinence de la datavisualisation, nous avons segmenté la date complète avec de nouvelles variables.")

        # Boxplot interactif avec Plotly
        fig_box = px.box(df, 
                         x="FirstPumpArriving_AttendanceTime", 
                         title="Délai d'arrivée du premier camion de pompier")
        st.plotly_chart(fig_box)

        # Seaborn countplot
        fig, ax = plt.subplots()
        sns.countplot(data=df, x="IncidentGroup", hue="IncidentGroup", ax=ax)
        ax.set_xlabel("Type d'incident")
        ax.set_ylabel("Quantité")
        ax.set_yticks(range(0, 800, 200))
        ax.set_title("Nombre d'incidents par catégorie")
        ax.legend().remove()
        plt.tight_layout()
        st.pyplot(fig)

    
    # 📈 Onglet 2 : Dataviz multivariée
    with tab2:
        st.header("Dataviz multivariée")
        with st.expander("Type d'incident") :
            fig2, ax2 = plt.subplots()
            sns.violinplot(data=df, x="StopCodeDescription",  y="FirstPumpArriving_AttendanceTime",hue="StopCodeDescription", palette="Set1")      
            ax2.set_title("Relation entre le type d'incident et le délai de réponse")
            ax2.set_xlabel("Type d'incident")
            ax2.set_ylabel("Délai de réponse de la LFB")
            plt.xticks(rotation = 90)
            plt.tight_layout()
            st.pyplot(fig2)

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
        sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax3)
        st.pyplot(fig3)


elif page == "Preprocessing":
    st.header("Preprocessing")
    tabs = st.tabs(["Split","Frequency Encoding", "OneHotEncoder", "Label Encoding", "Standardisation"])

# Contenu du premier onglet
    with tabs[0]:
        st.header("Split")

    with tabs[1]:
        st.header("requency Encoding")
        st.write("Contenu pour l'onglet 'requency Encoding'.")

    with tabs[2]:
        st.header("OneHotEncoder")
        st.write("Contenu pour l'onglet 'OneHotEncoder'.")

    with tabs[3]:
        st.header("Label Encoding")
        st.write("Contenu pour l'onglet 'Label Encoding'.")
    
    with tabs[4]:
        st.header("Split")
        st.write("Contenu pour l'onglet 'Standardisation'.")


elif page == "Modélisation":
    st.header("Modélisation")
    
        # Graphique de régression (affichage de la relation entre la cible et une feature)
    with st.expander("Modèles de Régression"):
        st.markdown("""
        **Modèles testés :**
        - Linear Regression
        - Decision Tree Regressor
        - Random Forest Regressor
        - SGD Regressor
        - KNN Regressor
        """)
        data = [[89.719590, 14049.171200, 118.529200, 0.051449], [207.2518553, 63919.102367, 252.82227427, -3.319882904], [88.149152936, 13649.741853, 116.832109685, 0.0797185175],[219791737230162, 4.928111e+30, 2219934929759535, 3.32472727e+26],[94.106070, 15144.089260, 123.061323, -0.022476]]  
        df = pd.DataFrame(data, columns = ["MAE", "MSE", "RMSE", "R2"], index =["Linear_Regression", "Decision_Tree_Regressor", "Random_Forest_Regressor", "SGD_Regressor", "KNNRegressor"])
        st.dataframe(df)

        
        
        # Classification binaire
    with st.expander("Modèles de Classification binaire"):
        st.markdown("""
        **Modèles testés :**
        - Logistic Regression
        - Decision Tree Classifier
        - Random Forest Classifier
        - XGB Classifier
        - KNN Classifier
        - Linear SVC
        """)
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
            "F1 Score Classe 0", "F1 Score Classe 1"],
        index=[
            "Logistic Regression", "Decision Tree Classifier",
            "Random Forest Classifier", "XGB Classifier",
            "KNN Classifier", "Linear SVC"])

        st.dataframe(df2)

        # Classification multi-classes
    with st.expander("Modèles de Classification multi-classes"):
        st.markdown("""
        **Modèles testés :**
        - Logistic Regression
        - Decision Tree Classifier
        - Random Forest Classifier
        - XGB Classifier
        - KNN Classifier 
        """)
        data = [[0.32, 0.33, 0.25, 0.30,0.32,0.67,0.00,0.34,0.19,0.44,0.00,0.32,0.24], [0.40, 0.51, 0.31, 0.35,0.41,0.51,0.32,0.35,0.40, 0.51,0.31,0.35,0.40],[0.42,0.50,0.33,0.37,0.45,0.60,0.27,0.37,0.41,0.55,0.3,0.37,0.43],[0.39, 0.42, 0.36,0.35,0.41, 0.66,0.08,0.38,0.39,0.51,0.13,0.36,0.40],[0.28, 0.31, 0.24, 0.28, 0.27,0.45,0.21,0.23,0.20,0.37,0.22,0.25,0.23]]  
        df3= pd.DataFrame(data, columns = ["ACCURACY", "PRECISION  Classe 0", "PRECISION Classe 1","PRECISION Classe 2","PRECISION Classe 3", "RECALL Classe 0", "RECALL Classe 1", "RECALL Classe 2", "RECALL Classe 3","F1 SCORE Classe 0","F1 SCORE Classe 1","F1 SCORE Classe 2","F1 SCORE Classe 3"], index =["Logistic Regression", "Decision Tree Classifier", "Random Forest Classifier", "XGB Classifier", "KNN Classifier"])
        st.dataframe(df3)    

    with st.expander("Modèle optimisé"):
        st.markdown("""
        **Modèles optimisés testés :**
        - Decision Tree Classifier
        - Random Forest Classifier 
        """)
        data = [[0.42, 0.49, 0.62, 0.55], [0.42, 0.33, 0.25, 0.29], [0.42, 0.36, 0.39, 0.38],[0.42, 0.47, 0.36, 0.41]]  
        df4 = pd.DataFrame(data, columns = ["ACCURACY", "PRECISION", "RECALL", "F1 SCORE"], index =["Classe 0", "Classe 1", "Classe 2", "Classe 3"])
        st.dataframe(df4)