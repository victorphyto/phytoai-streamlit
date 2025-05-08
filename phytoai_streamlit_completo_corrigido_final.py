
import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import cv2
import numpy as np
from PIL import Image

# Configuração da interface
st.set_page_config(page_title="PhytoAI - Fluxo Completo", layout="wide")
st.title("PhytoAI 🌿")
st.subheader("Assistente Inteligente para Planejamento Cromatográfico")

# Inicializar controle de etapas
if "etapa" not in st.session_state:
    st.session_state.etapa = 0

def avancar():
    st.session_state.etapa += 1

def voltar():
    if st.session_state.etapa > 0:
        st.session_state.etapa -= 1


def detectar_pontos_e_calcular_rf(uploaded_file):
    image = Image.open(uploaded_file).convert("RGB")
    image_np = np.array(image)
    gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY_INV, 15, 10
    )
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    altura_placa = image_np.shape[0]
    pontos_detectados = []
    imagem_com_pontos = image_np.copy()
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if h > 5 and w > 5:
            cv2.rectangle(imagem_com_pontos, (x, y), (x + w, y + h), (255, 0, 0), 2)
            rf = round(y / altura_placa, 2)
            pontos_detectados.append({"x": x, "y": y, "Rf": rf})
    pontos_ordenados = sorted(pontos_detectados, key=lambda k: k["y"])
    return pontos_ordenados, imagem_com_pontos

    image_np = np.array(image)
    gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
    thresh = cv2.adaptiveThreshold(gray, 255,
                                   cv2.ADAPTIVE_THRESH_MEAN_C,
                                   cv2.THRESH_BINARY_INV, 15, 10)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    altura_placa = image_np.shape[0]
    pontos_detectados = []
    imagem_com_pontos = image_np.copy()
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if h > 5 and w > 5:
            cv2.rectangle(imagem_com_pontos, (x, y), (x + w, y + h), (255, 0, 0), 2)
            rf = round(y / altura_placa, 2)
            pontos_detectados.append({"x": x, "y": y, "Rf": rf})
    pontos_ordenados = sorted(pontos_detectados, key=lambda k: k["y"])
    return pontos_ordenados, imagem_com_pontos



st.set_page_config(page_title="PhytoAI - Fluxo Completo", layout="wide")
st.title("PhytoAI 🌿")
st.subheader("Assistente Inteligente para Planejamento Cromatográfico")

if "etapa" not in st.session_state:
    st.session_state.etapa = 0


def voltar():
if st.session_state.etapa > 0:
st.session_state.etapa -= 1

def avancar():
st.session_state.etapa += 1

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
"Massa Exata": props.get("ExactMass", None),
"LogP": props.get("LogP", None)
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
"Massa Exata": r.get("average_mass", None),
"LogP": None
})
    except:
    pass
    return data

    if st.session_state.etapa == 0:
    st.markdown("👋 **Vamos compreender um pouco melhor sobre sua amostra.**")
    st.button("Prosseguir", on_click=avancar)

        elif st.session_state.etapa == 1:
        st.session_state.origem = st.selectbox("Origem da amostra", ["Planta", "Fungo", "Bactéria", "Alga", "Outro"])
        col1, col2 = st.columns(2)
        col1.button("Anterior", on_click=voltar)
        col2.button("Próximo", on_click=avancar)

        elif st.session_state.etapa == 2:
        if st.session_state.origem == "Planta":
        st.session_state.parte = st.selectbox("Parte da planta utilizada", ["Folhas", "Frutos", "Sementes", "Cascas", "Raízes", "Outras"])
            elif st.session_state.origem in ["Fungo", "Bactéria"]:
            st.session_state.parte = st.selectbox("Material utilizado", ["Micélio", "Meio de cultura", "Outros"])
            elif st.session_state.origem == "Alga":
            st.session_state.parte = st.selectbox("Material utilizado", ["Biomassa total", "Outros"])
            else:
            st.session_state.parte = st.text_input("Descreva a parte/material utilizado")
            col1, col2 = st.columns(2)
            col1.button("Anterior", on_click=voltar)
            col2.button("Próximo", on_click=avancar)

            elif st.session_state.etapa == 3:
            st.session_state.tecnica = st.selectbox("Técnica de extração", [
            "Maceração", "Infusão", "Decocção", "Digestão", "Soxhlet", "Percolação",
            "Extração Líquido-Líquido", "Destilação", "Hidrodestilação",
            "Extração com Fluidos Supercríticos (SFE)", "Extração Assistida por Micro-ondas (MAE)",
            "Extração Assistida por Ultrassom (UAE)"
            ])
            col1, col2 = st.columns(2)
            col1.button("Anterior", on_click=voltar)
            col2.button("Próximo", on_click=avancar)

            elif st.session_state.etapa == 4:
            st.session_state.solvente = st.selectbox("Solvente(s) utilizado(s)", [
            "Água", "Etanol", "Metanol", "Acetona", "Hexano", "Clorofórmio", "Éter etílico",
            "Acetato de etila", "Diclorometano", "Tolueno", "Dióxido de carbono supercrítico (scCO2)",
            "Água-Etanol", "Água-Metanol", "Hexano-Acetato de Etila",
            "Clorofórmio-Metanol", "Éter de Petróleo-Éter Etílico"
            ])
            col1, col2 = st.columns(2)
            col1.button("Anterior", on_click=voltar)
            col2.button("Próximo", on_click=avancar)



            elif st.session_state.etapa == 5:
            st.session_state.genero = st.text_input("Gênero (opcional)", key="genero_input")
            st.session_state.especie = st.text_input("Espécie (opcional)", key="especie_input")
            col1, col2 = st.columns(2)
            col1.button("Anterior", on_click=voltar)
            col2.button("Finalizar entrada", on_click=avancar)

            st.session_state.genero = st.text_input("Gênero (opcional)", "")
            st.session_state.especie = st.text_input("Espécie (opcional)")
            col1, col2 = st.columns(2)
            col1.button("Anterior", on_click=voltar)
            col2.button("Finalizar entrada", on_click=avancar)

            st.session_state.genero = st.text_input("Gênero (obrigatório)", "")
            st.session_state.especie = st.text_input("Espécie (opcional)")
            col1, col2 = st.columns(2)
            col1.button("Anterior", on_click=voltar)
            col2.button("Finalizar entrada", on_click=avancar)


            elif st.session_state.etapa == 6:
            if not st.session_state.genero:
            st.session_state.no_compounds = True
            avancar()
                else:
                termo = f"{st.session_state.genero} {st.session_state.especie}".strip()
                resultados = buscar_pubchem(termo) + buscar_npatlas(termo)

                if not resultados and st.session_state.genero:
                st.warning(f"Nenhum composto encontrado para *{termo}*. Tentando com apenas o gênero *{st.session_state.genero}*...")
                termo = st.session_state.genero
                resultados = buscar_pubchem(termo) + buscar_npatlas(termo)

                if resultados:
                df = pd.DataFrame(resultados)
                st.session_state.df_compostos = df
                st.success(f"🔬 Compostos encontrados para: *{termo}*")
                st.dataframe(df)

                col1, col2 = st.columns(2)
                with col1:
                st.markdown("**Distribuição de Massa Exata**")
                massa_vals = df["Massa Exata"].dropna().astype(float)
                if not massa_vals.empty:
                fig, ax = plt.subplots()
                ax.hist(massa_vals, bins=10)
                ax.set_xlabel("Massa Exata")
                ax.set_ylabel("Frequência")
                st.pyplot(fig)
                    else:
                    st.info("Nenhum dado de massa disponível.")

                    with col2:
                    st.markdown("**Distribuição de LogP**")
                    logp_vals = df["LogP"].dropna().astype(float)
                    if not logp_vals.empty:
                    fig2, ax2 = plt.subplots()
                    ax2.hist(logp_vals, bins=10)
                    ax2.set_xlabel("LogP")
                    ax2.set_ylabel("Frequência")
                    st.pyplot(fig2)
                        else:
                        st.info("Nenhum dado de LogP disponível.")

                        col1, col2 = st.columns(2)
                        col1.button("Anterior", on_click=voltar)
                        col2.button("Avançar para simulação cromatográfica", on_click=avancar)
                        else:
                        st.session_state.no_compounds = True
                        avancar()
                        st.warning(f"Nenhum composto encontrado para *{termo}*. Tentando com apenas o gênero *{st.session_state.genero}*...")
                        termo = st.session_state.genero
                        resultados = buscar_pubchem(termo) + buscar_npatlas(termo)

                        if resultados:
                        df = pd.DataFrame(resultados)
                        st.session_state.df_compostos = df

                        st.success(f"🔬 Compostos encontrados para: *{termo}*")
                        st.dataframe(df)

                        col1, col2 = st.columns(2)
                        with col1:
                        st.markdown("**Distribuição de Massa Exata**")
                        massa_vals = df["Massa Exata"].dropna().astype(float)
                        if not massa_vals.empty:
                        fig, ax = plt.subplots()
                        ax.hist(massa_vals, bins=10)
                        ax.set_xlabel("Massa Exata")
                        ax.set_ylabel("Frequência")
                        st.pyplot(fig)
                            else:
                            st.info("Nenhum dado de massa disponível.")

                            with col2:
                            st.markdown("**Distribuição de LogP**")
                            logp_vals = df["LogP"].dropna().astype(float)
                            if not logp_vals.empty:
                            fig2, ax2 = plt.subplots()
                            ax2.hist(logp_vals, bins=10)
                            ax2.set_xlabel("LogP")
                            ax2.set_ylabel("Frequência")
                            st.pyplot(fig2)
                                else:
                                st.info("Nenhum dado de LogP disponível.")

                                col1, col2 = st.columns(2)
                                col1.button("Anterior", on_click=voltar)
                                col2.button("Avançar para simulação cromatográfica", on_click=avancar)
                                else:
                                st.session_state.no_compounds = True
                                avancar()

                                termo = f"{st.session_state.genero} {st.session_state.especie}".strip()
                                resultados = buscar_pubchem(termo) + buscar_npatlas(termo)

                                if not resultados and st.session_state.genero:
                                st.warning(f"Nenhum composto encontrado para *{termo}*. Tentando com apenas o gênero *{st.session_state.genero}*...")
                                termo = st.session_state.genero
                                resultados = buscar_pubchem(termo) + buscar_npatlas(termo)

                                if resultados:
                                df = pd.DataFrame(resultados)
                                st.session_state.df_compostos = df

                                st.success(f"🔬 Compostos encontrados para: *{termo}*")
                                st.dataframe(df)

                                col1, col2 = st.columns(2)
                                with col1:
                                st.markdown("**Distribuição de Massa Exata**")
                                massa_vals = df["Massa Exata"].dropna().astype(float)
                                if not massa_vals.empty:
                                fig, ax = plt.subplots()
                                ax.hist(massa_vals, bins=10)
                                ax.set_xlabel("Massa Exata")
                                ax.set_ylabel("Frequência")
                                st.pyplot(fig)
                                    else:
                                    st.info("Nenhum dado de massa disponível.")

                                    with col2:
                                    st.markdown("**Distribuição de LogP**")
                                    logp_vals = df["LogP"].dropna().astype(float)
                                    if not logp_vals.empty:
                                    fig2, ax2 = plt.subplots()
                                    ax2.hist(logp_vals, bins=10)
                                    ax2.set_xlabel("LogP")
                                    ax2.set_ylabel("Frequência")
                                    st.pyplot(fig2)
                                        else:
                                        st.info("Nenhum dado de LogP disponível.")

                                        col1, col2 = st.columns(2)
                                        col1.button("Anterior", on_click=voltar)
                                        col2.button("Avançar para simulação cromatográfica", on_click=avancar)
                                        else:
                                        st.error("Nenhum composto encontrado nas bases consultadas.")

                                        # Inserção do novo fluxo para CCD caso composição seja desconhecida

                                        elif st.session_state.etapa == 7 and st.session_state.get("no_compounds", False):
                                        st.subheader("📋 Composição Química Manual")
                                        conhece = st.radio("Você conhece a composição química da sua amostra?", ["Sim", "Não"], horizontal=True)
                                        if conhece == "Sim":
                                        st.session_state.conhece_comp = True
                                        avancar()
                                            else:
                                            st.session_state.conhece_comp = False
                                            avancar()

                                            elif st.session_state.etapa == 8 and st.session_state.conhece_comp:
                                            st.subheader("🧬 Quais classes de metabólitos você espera encontrar?")
                                            classes = st.multiselect("Selecione todas que se aplicam:", [
                                            "Monoterpenos", "Sesquiterpenos", "Diterpenos", "Triterpenos", "Tetraterpenos", "Politerpenos",
                                            "Ácidos fenólicos", "Flavonoides", "Lignanas", "Taninos", "Cumarinas", "Estilbenos", "Quinonas",
                                            "Pirrolidinas", "Piridinas", "Tropanos", "Indóis", "Quinoleínas", "Isoquinoleínas", "Purinas",
                                            "Aminas biogênicas", "Macrolídeos", "Tetraciclinas", "Antraquinonas", "NRPs", "Peptídeos", 
                                            "Glicosídeos cardíacos", "Glicosídeos cianogênicos", "Saponinas", "Aminoácidos não proteicos", 
                                            "Toxinas", "Pigmentos"
                                            ])
                                            st.session_state.classes_quimicas = classes
                                            if classes:
                                            col1, col2 = st.columns(2)
                                            col1.button("Anterior", on_click=voltar)
                                            col2.button("Avançar para escolha cromatográfica", on_click=avancar)

                                                elif st.session_state.etapa == 8 and not st.session_state.conhece_comp:
                                                st.subheader("📷 Análise da Amostra via CCD")
                                                st.session_state.ccd_img = st.file_uploader("Faça upload da imagem da sua placa de CCD", type=["jpg", "jpeg", "png"])

                                                st.markdown("### 📄 Informe os detalhes da fase estacionária:")
                                                st.session_state.fase_estacionaria = st.selectbox("Fase Estacionária:", ["Sílica", "Alumina", "C-18"])

                                                st.markdown("### 💧 Informe a composição da fase móvel:")

                                                solventes = ["Não", "Água", "Etanol", "Metanol", "Hexano", "Acetato de etila", "Clorofórmio", "Diclorometano", "Acetona", "Tolueno"]
                                                st.session_state.solvente_A = st.selectbox("Solvente A:", solventes)
                                                st.session_state.percentual_A = st.slider("Porcentagem do Solvente A:", 0, 100, 0)

                                                st.session_state.solvente_B = st.selectbox("Solvente B:", solventes)
                                                st.session_state.percentual_B = st.slider("Porcentagem do Solvente B:", 0, 100, 0)

                                                st.session_state.solvente_C = st.selectbox("Solvente C:", solventes)
                                                st.session_state.percentual_C = st.slider("Porcentagem do Solvente C:", 0, 100, 0)

                                                if st.session_state.ccd_img:
                                                st.image(st.session_state.ccd_img, caption="Imagem da CCD carregada", use_column_width=True)


                                                if col1, col2 = st.columns(2)
                                                col1.button("Anterior", on_click=voltar)
                                                col2.button("Calcular força eluente e seguir para simulação"):
                                                st.session_state.usar_ccd = True
                                                if st.session_state.ccd_img:
                                                pontos, imagem_processada = detectar_pontos_e_calcular_rf(st.session_state.ccd_img)
                                                st.image(imagem_processada, caption="Manchas detectadas", use_column_width=True)
                                                st.session_state.rf_pontos = pd.DataFrame(pontos)
                                                st.dataframe(st.session_state.rf_pontos)
                                                avancar()

                                                st.session_state.usar_ccd = True
                                                avancar()

                                                    elif st.session_state.etapa == 7:
                                                    st.subheader("🧪 Escolha de Técnica Cromatográfica")
                                                    tecnica_crom = st.selectbox("Técnica cromatográfica disponível:", [
                                                    "CCD", "HPLC", "UPLC", "Preparative HPLC", "LCxLC", "SEC", "IEC", "Afinidade",
                                                    "GC", "GC Capilar", "GC Preparativa", "GCxGC", "SFC", "CPC", "GPC", "Coluna Aberta",
                                                    "Membrana de Troca Iônica", "CEC", "Cromatografia Quiral"
                                                    ])
                                                    modo = st.radio("Modo de separação", ["Fase Normal", "Fase Reversa"], horizontal=True)

                                                    st.session_state.tecnica_crom = tecnica_crom
                                                    st.session_state.modo = modo

                                                    col1, col2 = st.columns(2)
                                                    col1.button("Anterior", on_click=voltar)
                                                    col2.button("Rodar simulação", on_click=avancar)

                                                    elif st.session_state.etapa == 8:
                                                    st.subheader("📊 Simulação da Separação Cromatográfica")
                                                    df = st.session_state.df_compostos.copy()
                                                    tecnica = st.session_state.tecnica_crom
                                                    modo = st.session_state.modo

                                                    if "LogP" in df.columns:
                                                    if modo == "Fase Reversa":
                                                    df["Retenção Esperada"] = df["LogP"].apply(lambda x: "Alta" if pd.notna(x) and x > 3 else "Moderada" if pd.notna(x) else "Desconhecida")
                                                        else:
                                                        df["Retenção Esperada"] = df["LogP"].apply(lambda x: "Alta" if pd.notna(x) and x < 2 else "Moderada" if pd.notna(x) else "Desconhecida")

                                                        st.markdown(f"**Técnica selecionada:** {tecnica} | **Modo:** {modo}")
                                                        st.dataframe(df)