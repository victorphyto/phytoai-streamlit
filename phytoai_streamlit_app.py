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

# A partir daqui deve-se incluir o fluxo completo das etapas interativas
st.markdown("🚧 Etapas interativas ainda serão reintegradas abaixo...")


# Etapa 0 - Introdução
if st.session_state.etapa == 0:
    st.markdown("👋 **Vamos compreender um pouco melhor sobre sua amostra.**")
    st.button("Prosseguir", on_click=avancar)

# Etapa 1 - Origem da amostra
elif st.session_state.etapa == 1:
    st.session_state.origem = st.selectbox("Origem da amostra", ["Planta", "Fungo", "Bactéria", "Alga", "Outro"])
    col1, col2 = st.columns(2)
    col1.button("Anterior", on_click=voltar)
    col2.button("Próximo", on_click=avancar)

# Etapa 2 - Parte da planta ou tipo de material
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

# Etapa 3 - Técnica de extração
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

# Etapa 4 - Solvente utilizado
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



# Etapa 5 - Gênero e espécie (entrada opcional)
elif st.session_state.etapa == 5:
    st.session_state.genero = st.text_input("Gênero (opcional)", key="genero_input")
    st.session_state.especie = st.text_input("Espécie (opcional)", key="especie_input")
    col1, col2 = st.columns(2)
    col1.button("Anterior", on_click=voltar)
    col2.button("Finalizar entrada", on_click=avancar)

# Etapa 6 - Composição química automática ou entrada manual
elif st.session_state.etapa == 6:
    if not st.session_state.genero:
        st.session_state.no_compounds = True
        avancar()
    else:
        termo = f"{st.session_state.genero} {st.session_state.especie}".strip()
        resultados = []  # Exemplo: buscar_pubchem(termo) + buscar_npatlas(termo)
        if not resultados:
            st.warning(f"Nenhum composto encontrado para *{termo}*. Prosseguiremos para entrada manual.")
            st.session_state.no_compounds = True
            avancar()
        else:
            df = pd.DataFrame(resultados)
            st.session_state.df_compostos = df
            st.dataframe(df)
            col1, col2 = st.columns(2)
            col1.button("Anterior", on_click=voltar)
            col2.button("Avançar para simulação cromatográfica", on_click=avancar)

# Etapa 7 - Entrada manual (caso não tenha dados)
elif st.session_state.etapa == 7 and st.session_state.get("no_compounds", False):
    st.subheader("📋 Composição Química Manual")
    conhece = st.radio("Você conhece a composição química da sua amostra?", ["Sim", "Não"], horizontal=True)
    if conhece == "Sim":
        st.session_state.conhece_comp = True
        avancar()
    else:
        st.session_state.conhece_comp = False
        avancar()

# Etapa 8 - Seleção de classes químicas ou análise CCD
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
    st.session_state.ccd_img = st.file_uploader("Upload da imagem da placa CCD", type=["jpg", "jpeg", "png"])
    st.markdown("### 📄 Fase estacionária:")
    st.session_state.fase_estacionaria = st.selectbox("Fase Estacionária", ["Sílica", "Alumina", "C-18"])

    st.markdown("### 💧 Fase móvel:")
    solventes = ["Não", "Água", "Etanol", "Metanol", "Hexano", "Acetato de etila", "Clorofórmio", "Diclorometano", "Acetona", "Tolueno"]
    st.session_state.solvente_A = st.selectbox("Solvente A", solventes)
    st.session_state.percentual_A = st.slider("Porcentagem Solvente A", 0, 100, 0)
    st.session_state.solvente_B = st.selectbox("Solvente B", solventes)
    st.session_state.percentual_B = st.slider("Porcentagem Solvente B", 0, 100, 0)
    st.session_state.solvente_C = st.selectbox("Solvente C", solventes)
    st.session_state.percentual_C = st.slider("Porcentagem Solvente C", 0, 100, 0)

    if st.session_state.ccd_img:
        st.image(st.session_state.ccd_img, caption="Imagem carregada", use_column_width=True)
        pontos, imagem = detectar_pontos_e_calcular_rf(st.session_state.ccd_img)
        st.image(imagem, caption="Manchas detectadas", use_column_width=True)
        st.session_state.rf_pontos = pd.DataFrame(pontos)
        st.dataframe(st.session_state.rf_pontos)

    col1, col2 = st.columns(2)
    col1.button("Anterior", on_click=voltar)
    col2.button("Avançar para escolha cromatográfica", on_click=avancar)
