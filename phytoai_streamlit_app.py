
import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="PhytoAI - Entrada de Dados", layout="centered")

st.title("PhytoAI - Planejamento Cromatográfico Inteligente")
st.subheader("Entrada de dados preliminares da amostra")

# Formulário do usuário
origem = st.selectbox("Origem da amostra", ["Planta", "Fungo", "Bactéria", "Alga", "Outro"])
tipo_extracao = st.selectbox("Tipo de extração", ["Hexano", "Acetato de etila", "Etanol", "Metanol", "Água", "Óleo essencial", "Outro"])
genero = st.text_input("Gênero (opcional)")
especie = st.text_input("Espécie (opcional)")

# Quando preenchido, buscar compostos no PubChem
if st.button("Buscar compostos prováveis"):
    termo_busca = f"{genero} {especie}".strip()
    if termo_busca:
        st.info(f"Buscando compostos relacionados a: {termo_busca}")
        url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{termo_busca}/cids/TXT"
        response = requests.get(url)

        if response.status_code == 200:
            cids = response.text.strip().split("\n")
            st.success(f"Foram encontrados {len(cids)} compostos (CIDs no PubChem).")

            # Mostrar os primeiros compostos
            data = []
            for cid in cids[:10]:
                prop_url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/property/Title,MolecularFormula,ExactMass,LogP/JSON"
                prop_resp = requests.get(prop_url)
                if prop_resp.status_code == 200:
                    props = prop_resp.json()["PropertyTable"]["Properties"][0]
                    data.append({
                        "CID": cid,
                        "Nome": props.get("Title", "N/A"),
                        "Fórmula": props.get("MolecularFormula", "N/A"),
                        "Massa Exata": props.get("ExactMass", "N/A"),
                        "LogP": props.get("LogP", "N/A")
                    })
            df = pd.DataFrame(data)
            st.dataframe(df)
        else:
            st.warning("Nenhum composto encontrado no PubChem.")
    else:
        st.error("Por favor, insira pelo menos o gênero ou espécie.")
