# app_simple_mobile.py
# ===============================================
# Dominó Duplas — Versão Simplificada (Mobile‑first)
# -----------------------------------------------
# Instruções:
# 1) pip install -r requirements.txt
# 2) streamlit run app_simple_mobile.py
# -----------------------------------------------
# Diferenças vs. app_simple.py:
# - Layout "mobile-first": botões grandes e fáceis de tocar
# - Botões de pontuação centralizados em cada painel
# - Históricos movidos para a parte inferior (um por time, em expansores)
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
        margin: 0.25rem 0 0.75rem 0;
        text-align: center;
      }
      /* Centraliza blocos internos (botões) */
      .center-block {
        max-width: 420px;
        margin-left: auto;
        margin-right: auto;
      }
      /* Ajustes sutis de texto */
      .team-title { text-align:center; margin-bottom: 0.25rem; }
      .subtle { opacity: .75; text-align:center; }
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
def somar(team: str, valor: int):
    st.session_state.totais[team] += valor
    st.session_state.hist[team].append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "delta": f"+{valor}",
        "total_resultante": st.session_state.totais[team],
    })

def zerar():
    st.session_state.totais = {"A": 0, "B": 0}
    st.session_state.hist = {"A": [], "B": []}

# ---------------------------
# UI — Cabeçalho
# ---------------------------
st.title("Placar de Dominó — Duplas (Mobile)")
with st.expander("Nomes dos times", expanded=False):
    c1, c2 = st.columns(2)
    with c1:
        nameA = st.text_input("Nome do Time A", value=st.session_state.team_names["A"])
    with c2:
        nameB = st.text_input("Nome do Time B", value=st.session_state.team_names["B"])
    st.session_state.team_names["A"] = nameA.strip() or "Time A"
    st.session_state.team_names["B"] = nameB.strip() or "Time B"

# Botão global para reset (no topo para acesso rápido no celular)
st.button("🧹 Zerar placares", on_click=zerar, help="Zera os placares e históricos dos dois times.", use_container_width=True)

st.divider()

# ---------------------------
# Painéis dos times
# ---------------------------
left, right = st.columns(2)

def painel_time(team: str, col):
    with col:
        st.markdown(f"### <div class='team-title'>{st.session_state.team_names[team]}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='placar'>{st.session_state.totais[team]}</div>", unsafe_allow_html=True)

        # Centro do bloco de botões (com coluna central "estreita" usando CSS)
        with st.container():
            st.markdown("<div class='center-block'>", unsafe_allow_html=True)
            # Duas linhas de botões (2x2) para ficar mais 'mobile'
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
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='subtle'>Toque para somar pontos</div>", unsafe_allow_html=True)

painel_time("A", left)
painel_time("B", right)

st.divider()

# ---------------------------
# Históricos (parte inferior)
# ---------------------------
st.subheader("Históricos")
ha, hb = st.columns(2)
with ha:
    with st.expander(f"📜 Histórico — {st.session_state.team_names['A']}", expanded=False):
        if len(st.session_state.hist["A"]) == 0:
            st.info("Sem somas registradas ainda.")
        else:
            dfA = pd.DataFrame(st.session_state.hist["A"])
            st.dataframe(dfA, use_container_width=True, hide_index=True)

with hb:
    with st.expander(f"📜 Histórico — {st.session_state.team_names['B']}", expanded=False):
        if len(st.session_state.hist["B"]) == 0:
            st.info("Sem somas registradas ainda.")
        else:
            dfB = pd.DataFrame(st.session_state.hist["B"])
            st.dataframe(dfB, use_container_width=True, hide_index=True)
