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
# - Histórico ÚNICO da partida (ambos os times)
# - Toggle "🔡 Botões grandes" com CSS forte para mobile
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
    # Históricos individuais ainda existem, mas não são mais exibidos.
    st.session_state.setdefault("hist", {"A": [], "B": []})
    # Histórico único da partida
    st.session_state.setdefault("hist_all", [])  # lista de dicts: {timestamp, time_id, time, delta, total_resultante}

init_state()

# ---------------------------
# UI – Preferências
# ---------------------------
large_buttons = st.toggle(
    "🔡 Botões grandes",
    value=True,
    help="Aumenta o tamanho dos botões e do placar para facilitar o uso no celular."
)

# Wrapper de tamanho (aplica CSS aos botões e placar)
size_class = "big" if large_buttons else "small"

# ---------------------------
# Estilo (CSS) baseado no toggle — com seletor mais forte e !important
# ---------------------------
st.markdown(
    f"""
    <style>
      /* Wrapper que controla o tamanho dos botões */
      .btn-block.big .stButton > button {{
        padding: 18px 22px !important;
        font-size: 22px !important;
        min-height: 56px !important;
        border-radius: 14px !important;
      }}
      .btn-block.small .stButton > button {{
        padding: 12px 14px !important;
        font-size: 14px !important;
        min-height: 40px !important;
        border-radius: 12px !important;
      }}
      /* Placar */
      .placar.big {{
        font-size: 72px !important;
        font-weight: 800;
        line-height: 1;
        margin: 0.25rem 0 0.5rem 0;
        text-align: center;
      }}
      .placar.small {{
        font-size: 54px !important;
        font-weight: 800;
        line-height: 1;
        margin: 0.25rem 0 0.5rem 0;
        text-align: center;
      }}
      /* Centraliza blocos internos (botões) */
      .center-block {{
        max-width: 420px;
        margin-left: auto;
        margin-right: auto;
      }}
      /* Deixa o ÚLTIMO botão do bloco vermelho (é o ➖ 5) */
      .center-block .stButton:last-child button {{
        background: #b00020 !important;
        color: #fff !important;
        border: #fff !important;
      }}
      .names-row input {{ text-align: center; }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------
# Lógica
# ---------------------------
def registrar(team: str, delta: int):
    """Registra a ação no histórico individual e no histórico único da partida."""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Blindagem
    if "hist" not in st.session_state or team not in st.session_state.hist:
        init_state()

    # Atualiza histórico por time (mantido para compatibilidade)
    st.session_state.hist[team].append({
        "timestamp": ts,
        "delta": f"{'+' if delta>0 else ''}{delta}",
        "total_resultante": st.session_state.totais[team],
    })

    # Atualiza histórico único
    st.session_state.hist_all.append({
        "timestamp": ts,
        "time_id": team,
        "time": st.session_state.team_names[team],
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
    st.session_state.hist_all = []

# ---------------------------
# UI — Título
# ---------------------------
st.title("Placar do Jogo")

# ---------------------------
# Painéis dos times (2 colunas)
# ---------------------------
left, right = st.columns(2)

def painel_time(team: str, col):
    with col:
        st.markdown(f"<div class='placar {size_class}'>{st.session_state.totais[team]}</div>", unsafe_allow_html=True)

        # Nome do time logo abaixo do placar
        name = st.text_input(
            f"Nome do {team}",
            value=st.session_state.team_names[team],
            key=f"name_{team}",
            help="Edite o nome do time",
            label_visibility="collapsed"
        )
        st.session_state.team_names[team] = name.strip() or (f"Time {team}")

        # Bloco central com wrapper que aplica as regras de tamanho
        st.markdown(f"<div class='center-block btn-block {size_class}'>", unsafe_allow_html=True)
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
# Histórico ÚNICO (parte inferior)
# ---------------------------
st.subheader("Histórico da partida (único)")
if len(st.session_state.hist_all) == 0:
    st.info("Sem ações registradas ainda.")
else:
    df_all = pd.DataFrame(st.session_state.hist_all)
    # Ordena por timestamp (caso futuro com imports/edições)
    # E mostra as colunas em ordem amigável
    cols = ["timestamp", "time", "delta", "total_resultante"]
    cols = [c for c in cols if c in df_all.columns]
    df_show = df_all[cols].copy()
    st.dataframe(df_show, use_container_width=True, hide_index=True)
