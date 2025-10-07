# app_simple_mobile.py
# ===============================================
# Dominó Duplas — Versão Simplificada (Mobile‑first) c/ Subtração -5
# -----------------------------------------------
# Instruções:
# 1) pip install -r requirements.txt
# 2) streamlit run app_simple_mobile.py
# -----------------------------------------------
# Recursos:
# - Botões grandes e centralizados (➕ 5/10/15/20) e um único ➖ 5 no final
# - ➖ 5 estilizado em vermelho (CSS) como último botão do bloco
# - Nomes dos times logo abaixo do placar (não em expander)
# - Botão "Zerar placares" logo abaixo dos painéis
# - Históricos por time na parte inferior (expansores)
# ===============================================

from datetime import datetime
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Placar Dominó — Mobile", layout="wide")

# ---------------------------
# Estilo (CSS) para mobile
# ---------------------------
st.markdown(
    """
    <style>
      /* Aumenta área de toque dos botões */
      .stButton>button {
        padding: 16px 18px;
        font-size: 20px;
        border-radius: 12px;
      }
      /* Placar grande */
      .placar {
        font-size: 64px;
        font-weight: 800;
        line-height: 1;
        margin: 0.25rem 0 0.5rem 0;
        text-align: center;
      }
      /* Centraliza blocos internos (botões) */
      .center-block {
        max-width: 420px;
        margin-left: auto;
        margin-right: auto;
      }
      /* Deixa o ÚLTIMO botão do bloco vermelho (é o ➖ 5) */
      .center-block .stButton:last-child button {
        background: #b00020 !important;
        color: #fff !important;
        border: none !important;
      }
      /* Títulos e textos */
      .team-title { text-align:center; margin-bottom: 0.25rem; }
      .subtle { opacity: .75; text-align:center; }
      .names-row input { text-align: center; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------
# Estado
# ---------------------------
def init_state():
    st.session_state.setdefault("team_names", {"A": "Time A", "B": "Time B"})
    st.session_state.setdefault("totais", {"A": 0, "B": 0})
    st.session_state.setdefault("hist", {"A": [], "B": []})  # lista de dicts: {ts, delta, total}
init_state()

# ---------------------------
# Lógica
# ---------------------------
def registrar(team: str, delta: int):
    """Registra no histórico do time."""
    st.session_state.hist[team].append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "delta": f"{'+' if delta>0 else ''}{delta}",
        "total_resultante": st.session_state.totais[team],
    })

def somar(team: str, valor: int):
    st.session_state.totais[team] += valor
    registrar(team, valor)

def subtrair5(team: str):
    atual = st.session_state.totais[team]
    if atual - 5 < 0:
        st.error("Subtração inválida: o placar não pode ser negativo.")
        return
    st.session_state.totais[team] -= 5
    registrar(team, -5)

def zerar():
    st.session_state.totais = {"A": 0, "B": 0}
    st.session_state.hist = {"A": [], "B": []}

# ---------------------------
# UI — Título
# ---------------------------
st.title("Placar de Dominó — Duplas (Mobile)")

# ---------------------------
# Painéis dos times
# ---------------------------
left, right = st.columns(2)

def painel_time(team: str, col):
    with col:
        # Título + placar
        st.markdown(f"### <div class='team-title'>{st.session_state.team_names[team]}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='placar'>{st.session_state.totais[team]}</div>", unsafe_allow_html=True)

        # Nomes dos times (logo abaixo do placar)
        name = st.text_input(f"Nome do {team}", value=st.session_state.team_names[team], key=f"name_{team}",
                             help="Edite o nome do time", label_visibility="collapsed")
        st.session_state.team_names[team] = name.strip() or (f"Time {team}")

        # Bloco central dos botões (➕ e ➖ 5 no fim)
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

        # Botão único de subtração -5 (último filho -> recebe estilo vermelho)
        st.button("➖ 5", key=f"sub_{team}_5", on_click=subtrair5, help="Subtrair 5 pontos", use_container_width=True)

        st.markdown("<div class='subtle'>Toque para somar, ou ajustar com ➖ 5</div>", unsafe_allow_html=True)

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
