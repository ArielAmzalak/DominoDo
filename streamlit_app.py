# app_simple.py
# ===============================================
# Dominó Duplas — Versão Simplificada (Somente soma e reset)
# -----------------------------------------------
# Instruções:
# 1) Instale dependências: `pip install -r requirements.txt`
# 2) Rode: `streamlit run app_simple.py`
# 3) Use os botões ➕ 5/10/15/20 para somar pontos. Use "Zerar placares" para reiniciar.
#    Abaixo de cada placar há um histórico das somas aplicadas.
# ===============================================

from datetime import datetime
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Placar Dominó — Simples", layout="wide")

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
st.title("Placar de Dominó — Duplas (Simplificado)")
with st.expander("Nomes dos times", expanded=False):
    c1, c2 = st.columns(2)
    with c1:
        nameA = st.text_input("Nome do Time A", value=st.session_state.team_names["A"])
    with c2:
        nameB = st.text_input("Nome do Time B", value=st.session_state.team_names["B"])
    st.session_state.team_names["A"] = nameA.strip() or "Time A"
    st.session_state.team_names["B"] = nameB.strip() or "Time B"

# Botão global para reset
st.button("🧹 Zerar placares", on_click=zerar, help="Zera os placares e históricos dos dois times.")

st.divider()

# ---------------------------
# Painéis dos times
# ---------------------------
left, right = st.columns(2)

def painel_time(team: str, col):
    with col:
        st.subheader(st.session_state.team_names[team])
        st.markdown(f"<h1 style='margin:0;font-size:56px;'>{st.session_state.totais[team]}</h1>", unsafe_allow_html=True)
        b1, b2, b3, b4 = st.columns(4)
        for btn, val in zip([b1,b2,b3,b4], [5, 10, 15, 20]):
            with btn:
                st.button(f"➕ {val}", key=f"add_{team}_{val}", on_click=somar, args=(team, val),
                          help=f"Somar {val} pontos")

        # Histórico simples abaixo do placar
        st.caption("Histórico de somas")
        if len(st.session_state.hist[team]) == 0:
            st.info("Sem somas registradas ainda.")
        else:
            df = pd.DataFrame(st.session_state.hist[team])
            st.dataframe(df, use_container_width=True, hide_index=True)

painel_time("A", left)
painel_time("B", right)
