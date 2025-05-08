import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import cv2
import numpy as np
from PIL import Image

st.set_page_config(page_title="PhytoAI - Fluxo Completo", layout="wide")
st.title("PhytoAI 🌿")
st.subheader("Assistente Inteligente para Planejamento Cromatográfico")

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

import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import cv2
import numpy as np
from PIL import Image

st.set_page_config(page_title="PhytoAI - Fluxo Completo", layout="wide")
st.title("PhytoAI 🌿")
st.subheader("Assistente Inteligente para Planejamento Cromatográfico")

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

# Etapa 7 e 8 ajustadas
# Etapa 7 - Composição Química Manual
if st.session_state.etapa == 7:
    st.subheader("📋 Composição Química Manual")
    conhece = st.radio("Você conhece a composição química da sua amostra?", ["Sim", "Não"], horizontal=True)
    if conhece == "Sim":
        st.session_state.conhece_comp = True
    else:
        st.session_state.conhece_comp = False
    st.button("Avançar", on_click=avancar)

# Etapa 8 - Classes químicas (se conhece) ou CCD (se não conhece)
elif st.session_state.etapa == 8:
    if st.session_state.conhece_comp:
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
    else:
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

# Etapa 9 - Escolha da técnica cromatográfica
elif st.session_state.etapa == 9:
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

# Etapa 10 - Exibição da simulação
elif st.session_state.etapa == 10:
    st.subheader("📊 Simulação da Separação Cromatográfica")

    tecnica = st.session_state.get("tecnica_crom", "Desconhecida")
    modo = st.session_state.get("modo", "Desconhecido")
    st.markdown(f"**Técnica selecionada:** {tecnica} | **Modo:** {modo}")

    if "df_compostos" in st.session_state:
        df = st.session_state.df_compostos.copy()
    elif "rf_pontos" in st.session_state:
        df = st.session_state.rf_pontos.copy()
        df.rename(columns={"Rf": "Retenção Esperada"}, inplace=True)
    else:
        st.error("Nenhum dado disponível para simulação.")
        st.stop()

    if "LogP" in df.columns and modo in ["Fase Reversa", "Fase Normal"]:
        if modo == "Fase Reversa":
            df["Retenção Esperada"] = df["LogP"].apply(lambda x: "Alta" if pd.notna(x) and x > 3 else "Moderada" if pd.notna(x) else "Desconhecida")
        else:
            df["Retenção Esperada"] = df["LogP"].apply(lambda x: "Alta" if pd.notna(x) and x < 2 else "Moderada" if pd.notna(x) else "Desconhecida")

    st.dataframe(df)
    st.success("✅ Simulação concluída com base nos parâmetros fornecidos.")
    st.button("Anterior", on_click=voltar)
