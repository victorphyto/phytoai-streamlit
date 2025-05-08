
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

def buscar_pubchem(term):
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{term}/cids/TXT"
    response = requests.get(url)
    data = []
    if response.status_code == 200:
        cids = response.text.strip().split("\n")
        for cid in cids[:10]:
            prop_url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/property/Title,MolecularFormula,ExactMass,LogP/JSON"
            prop_resp = requests.get(prop_url)
            if prop_resp.status_code == 200:
                props = prop_resp.json()["PropertyTable"]["Properties"][0]
                data.append({
                    "Fonte": "PubChem",
                    "Nome": props.get("Title", "N/A"),
                    "Fórmula": props.get("MolecularFormula", "N/A"),
                    "Massa Exata": props.get("ExactMass", "N/A"),
                    "LogP": props.get("LogP", "N/A")
                })
    return data

def buscar_npatlas(term):
    np_url = f"https://www.npatlas.org/api/v1/metabolites?search={term}"
    data = []
    try:
        response = requests.get(np_url)
        if response.status_code == 200 and response.json()["total"] > 0:
            results = response.json()["content"]
            for r in results[:10]:
                data.append({
                    "Fonte": "NPAtlas",
                    "Nome": r.get("name", "N/A"),
                    "Fórmula": r.get("molecular_formula", "N/A"),
                    "Massa Exata": r.get("average_mass", "N/A"),
                    "LogP": "N/A"
                })
    except:
        pass
    return data

def buscar_knapsack_link(term):
    url = f"http://www.knapsackfamily.com/knapsack_core/result/?word={term.replace(' ', '+')}"
    return url

# Quando preenchido, buscar compostos nas fontes
if st.button("Buscar compostos prováveis"):
    termo_busca = f"{genero} {especie}".strip()
    if termo_busca:
        st.info(f"Buscando compostos relacionados a: {termo_busca}")

        dados = []
        dados.extend(buscar_pubchem(termo_busca))
        dados.extend(buscar_npatlas(termo_busca))

        if dados:
            df = pd.DataFrame(dados)
            st.success(f"Compostos encontrados:")
            st.dataframe(df)
        else:
            st.warning("Nenhum composto encontrado nas APIs consultadas.")
        
        st.markdown("🔗 **Busca adicional no KNApSAcK:**")
        link_knapsack = buscar_knapsack_link(termo_busca)
        st.markdown(f"[Clique aqui para buscar no KNApSAcK]({link_knapsack})")

    else:
        st.error("Por favor, insira pelo menos o gênero ou espécie.")
