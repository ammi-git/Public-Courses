"""Interface Streamlit — À COMPLÉTER. Lancer : streamlit run src/app.py

Voir docs/03_architecture.md, section 9.
"""
import asyncio
import uuid

import streamlit as st

st.set_page_config(page_title="Analyste de données augmenté", layout="wide")
st.title("Analyste de données augmenté")

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())   # une conversation par session

# TODO : construire le graphe une seule fois (st.cache_resource + asyncio.run(construire_graphe()))
# TODO : afficher l'historique de la conversation
# TODO : champ de saisie -> asyncio.run(graphe.ainvoke(..., {"configurable": {"thread_id": ...}}))
# TODO : si le résultat contient "__interrupt__" : afficher le code et l'aperçu,
#        puis un bouton « Valider » et un champ « Remarque » qui reprennent avec Command(resume=...)
# TODO : afficher le dashboard exporté (st.components.v1.html ou st.plotly_chart)
