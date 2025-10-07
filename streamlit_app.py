# app_simple_mobile.py
# ===============================================
# Dominó Duplas — Versão Simplificada (Mobile‑first) c/ Subtração -5
# -----------------------------------------------
# Instruções:
# 1) pip install -r requirements.txt
# 2) streamlit run app_simple_mobile.py
# -----------------------------------------------
# Recursos:
# - Botões centralizados (➕ 5/10/15/20) e um único ➖ 5 no final (vermelho)
# - Nomes dos times logo abaixo do placar
# - Botão "Zerar placares" logo abaixo dos painéis
# - Históricos por time na parte inferior (expansores)
# - NOVO: Toggle "🔡 Botões grandes" para aumentar área de toque/visual no celular
# ===============================================

from datetime import datetime
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Placar Do Dominó", layout="wide")

# ---------------------------
# Estado
# ---------------------------
def init_state():
    st.session_state.setdefault("team_names", {"A": "Time A", "B": "Time B"})
    st.session_state.setdefault("totais", {"A": 0, "B": 0})
    st.session_state.setdefault("hist", {"A": [], "B": []})  # lista de dicts: {ts, delta, total}
init_state()

# ---------------------------
# UI – Preferências
# ---------------------------
large_buttons = st.toggle("🔡 Botões grandes", value=True, help="Aumenta o tamanho dos botões e do placar para facilitar o uso no celular.")

# ---------------------------
# Estilo (CSS) baseado no toggle
# ---------------------------
btn_pad = "16px 18px" if large_buttons else "12px 14px"
btn_font = "20px" if large_buttons else "14px"
score_font = "64px" if large_buttons else "54px"

st.markdown(
    f"""
    <style>
      .stButton>button {{
        padding: {btn_pad};
        font-size: {btn_font};
        border-radius: 12px;
      }}
      .placar {{
        font-size: {score_font};
        font-weight: 800;
        line-height: 1;
        margin: 0.25rem 0 0.5rem 0;
        text-align: center;
      }}
      .center-block {{
        max-width: 420px;
        margin-left: auto;
        margin-right: auto;
      }}
      .center-block .stButton:last-child button {{
        background: #b00020 !important;
        color: #fff !important;
        border: #fff !important;
      }}
      .team-title {{ text-align:center; margin-bottom: 0.25rem; }}
      .subtle {{ opacity: .75; text-align:center; }}
      .names-row input {{ text-align: center; }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------
# Lógica
# ---------------------------
def registrar(team: str, delta: int):
    # Blindagem extra
    if "hist" not in st.session_state or team not in st.session_state.hist:
        init_state()
    st.session_state.hist[team].append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "delta": f"{'+' if delta>0 else ''}{delta}",
        "total_resultante": st.session_state.totais[team],
    })

def somar(team: str, valor: int):
    if "totais" not in st.session_state or team not in st.session_state.totais:
        init_state()
    st.session_state.totais[team] += valor
    registrar(team, valor)

def subtrair5(team: str):
    if "totais" not in st.session_state or team not in st.session_state.totais:
        init_state()
    atual = st.session_state.totais[team]
    if atual - 5 < 0:
        st.error("Subtração inválida: o placar não pode ser negativo.")
        return
    st.session_state.totais[team] = atual - 5
    registrar(team, -5)

def zerar():
    st.session_state.totais = {"A": 0, "B": 0}
    st.session_state.hist = {"A": [], "B": []}

# ---------------------------
# UI — Título
# ---------------------------
st.title("Placar do Jogo")

# ---------------------------
# Painéis dos times (layout 2 colunas)
# ---------------------------
left, right = st.columns(2)

def painel_time(team: str, col):
    with col:
        st.markdown(f"<div class='placar'>{st.session_state.totais[team]}</div>", unsafe_allow_html=True)

        # Nome do time logo abaixo do placar
        name = st.text_input(
            f"Nome do {team}",
            value=st.session_state.team_names[team],
            key=f"name_{team}",
            help="Edite o nome do time",
            label_visibility="collapsed"
        )
        st.session_state.team_names[team] = name.strip() or (f"Time {team}")

        # Botões centralizados: ➕ 5/10/15/20 e ➖ 5 (último)
        st.markdown("<div class='center-block'>", unsafe_allow_html=True)
        r1c1, r1c2 = st.columns(2)
        r2c1, r2c2 = st.columns(2)
        with r1c1:
            st.button("➕ 5", key=f"add_{team}_5", on_click=somar, args=(team, 5), help="Somar 5 pontos", use_container_width=True)
        with r1c2:
            st.button("➕ 10", key=f"add_{team}_10", on_click=somar, args=(team, 10), help="Somar 10 pontos", use_container_width=True)
        with r2c1:
            st.button("➕ 15", key=f"add_{team}_15", on_click=somar, args=(team, 15), help="Somar 15 pontos", use_container_width=True)
        with r2c2:
            st.button("➕ 20", key=f"add_{team}_20", on_click=somar, args=(team, 20), help="Somar 20 pontos", use_container_width=True)

        st.button("➖ 5", key=f"sub_{team}_5", on_click=subtrair5, args=(team,), help="Subtrair 5 pontos", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

painel_time("A", left)
painel_time("B", right)

# Botão global para reset imediatamente abaixo dos painéis
st.markdown("")
st.button("🧹 Zerar placares", on_click=zerar, help="Zera os placares e históricos dos dois times.", use_container_width=True)

st.divider()

# ---------------------------
# Históricos (parte inferior)
# ---------------------------
st.subheader("Históricos")
ha, hb = st.columns(2)
with ha:
    with st.expander(f"📜 Histórico — {st.session_state.team_names['A']}", expanded=False):
        if len(st.session_state.hist["A"]) == 0:
            st.info("Sem ações registradas ainda.")
        else:
            dfA = pd.DataFrame(st.session_state.hist["A"])
            st.dataframe(dfA, use_container_width=True, hide_index=True)

with hb:
    with st.expander(f"📜 Histórico — {st.session_state.team_names['B']}", expanded=False):
        if len(st.session_state.hist["B"]) == 0:
            st.info("Sem ações registradas ainda.")
        else:
            dfB = pd.DataFrame(st.session_state.hist["B"])
            st.dataframe(dfB, use_container_width=True, hide_index=True)
