
import streamlit as st
import requests
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="PhytoAI - Entrada de Dados", layout="centered")
st.title("PhytoAI - Planejamento Cromatográfico Inteligente")
st.subheader("Entrada de dados preliminares da amostra")

# Origem da amostra
origem = st.selectbox("Origem da amostra", ["Planta", "Fungo", "Bactéria", "Alga", "Outro"])

# Parte utilizada com base na origem
parte_amostra = ""
if origem == "Planta":
    parte_amostra = st.selectbox("Parte da planta utilizada", ["Folhas", "Frutos", "Sementes", "Cascas", "Raízes", "Outras"])
elif origem in ["Fungo", "Bactéria"]:
    parte_amostra = st.selectbox("Material utilizado", ["Micélio", "Meio de cultura", "Outros"])
elif origem == "Alga":
    parte_amostra = st.selectbox("Material utilizado", ["Biomassa total", "Outros"])
else:
    parte_amostra = st.text_input("Descreva a parte/material utilizado")

# Técnica de extração
tecnica_extracao = st.selectbox("Técnica de extração", [
    "Maceração", "Infusão", "Decocção", "Digestão", "Soxhlet", "Percolação",
    "Extração Líquido-Líquido", "Destilação", "Hidrodestilação",
    "Extração com Fluidos Supercríticos (SFE)", "Extração Assistida por Micro-ondas (MAE)",
    "Extração Assistida por Ultrassom (UAE)"
])

# Solventes utilizados
solvente = st.selectbox("Solvente(s) utilizado(s)", [
    "Água", "Etanol", "Metanol", "Acetona", "Hexano", "Clorofórmio", "Éter etílico",
    "Acetato de etila", "Diclorometano", "Tolueno", "Dióxido de carbono supercrítico (scCO2)",
    "Água-Etanol", "Água-Metanol", "Hexano-Acetato de Etila",
    "Clorofórmio-Metanol", "Éter de Petróleo-Éter Etílico"
])

# Entrada taxonômica
genero = st.text_input("Gênero (opcional)")
especie = st.text_input("Espécie (opcional)")

# Dedução da polaridade
polaridade = ""
if tecnica_extracao.lower() in ["hidrodestilação", "destilação"]:
    polaridade = "Compostos voláteis (terpenos, álcoois leves, etc.)"
elif "água" in solvente.lower() or "etanol" in solvente.lower() or "metanol" in solvente.lower():
    polaridade = "Compostos de média a alta polaridade (flavonoides, taninos, glicosídeos)"
elif "hexano" in solvente.lower() or "éter" in solvente.lower() or "clorofórmio" in solvente.lower():
    polaridade = "Compostos apolares (lipídios, terpenos apolares, esteróis)"

if polaridade:
    st.markdown(f"🔍 **Com base nos dados fornecidos, espera-se extrair:** _{polaridade}_")

# Funções de busca de compostos
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

# Buscar compostos
if st.button("Buscar compostos prováveis"):
    termo_busca = f"{genero} {especie}".strip()
    if termo_busca:
        dados = []
        dados.extend(buscar_pubchem(termo_busca))
        dados.extend(buscar_npatlas(termo_busca))

        if dados:
            df = pd.DataFrame(dados)
            st.success("Compostos encontrados:")
            st.dataframe(df)
        else:
            st.warning("Nenhum composto encontrado nas APIs consultadas.")
        
        st.markdown("🔗 **Busca adicional no KNApSAcK:**")
        link_knapsack = buscar_knapsack_link(termo_busca)
        st.markdown(f"[Clique aqui para buscar no KNApSAcK]({link_knapsack})")

        # Salvar histórico local
        historico = {
            "Data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Origem": origem,
            "Parte utilizada": parte_amostra,
            "Técnica de extração": tecnica_extracao,
            "Solvente": solvente,
            "Gênero": genero,
            "Espécie": especie,
            "Previsão de compostos": polaridade
        }
        historico_df = pd.DataFrame([historico])
        historico_df.to_csv("historico_phytoai.csv", mode='a', header=False, index=False)
    else:
        st.error("Por favor, insira pelo menos o gênero ou espécie.")
