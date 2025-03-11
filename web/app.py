import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from pandas.tseries.offsets import BDay

# Configuração da página
st.set_page_config(
    layout="wide", page_title="📈 Previsão de Preços de Ações IBOV", page_icon="📊"
)

# CSS Customizado
st.markdown(
    """
    <style>
    .block-container { padding-top: 0rem !important; }
    .main-container { background-color: #121212; padding: 30px; border-radius: 12px; box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2); }
    h1 { color: #ffffff; font-size: 26px; font-weight: bold; text-align: center !important; }
    .stButton button { background-color: #1f77b4; color: white; font-size: 18px; border-radius: 8px; padding: 10px 20px; border: none; }
    .stButton button:hover { background-color: #135e96; }
    .prediction-box { background-color: #1a3e5c; padding: 15px; border-radius: 10px; color: white; text-align: center; font-size: 18px; font-weight: bold; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Título principal
st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.title("📈 Previsão de Preços de Ações IBOV")

# Seleção de ativos
tickers_ibov = [
    "PETR4",
    "VALE3",
    "ITUB4",
    "BBDC4",
    "ABEV3",
    "B3SA3",
    "MGLU3",
    "WEGE3",
    "TAEE11",
    "USIM5",
]
ticker = st.selectbox("Escolha uma ação:", tickers_ibov)


# Função para obter o próximo dia útil
def get_next_business_day(last_date):
    return last_date + BDay(1)  # Adiciona 1 dia útil ao último pregão


# Botão para previsão
if st.button("📊 Prever"):
    with st.spinner("🔄 Obtendo dados..."):
        API_URL = "https://stock-price-predict.up.railway.app"
        response = requests.get(f"{API_URL}/predict/{ticker}")

    if response.status_code == 200:
        data = response.json()

        if "error" in data:
            st.error(data["error"])
        else:
            real_prices = data["real_prices"]
            dates = data["dates"]
            predicted_price = data["predicted_price"]
            lower_bound = data["prediction_range"]["lower"]
            upper_bound = data["prediction_range"]["upper"]

            # Criar DataFrame
            df = pd.DataFrame({"Data": dates, "Preço Real": real_prices})
            df["Data"] = pd.to_datetime(df["Data"])

            last_date = df["Data"].iloc[-1]  # Última data do pregão
            next_date = get_next_business_day(
                last_date
            )  # Primeiro dia útil após o último pregão
            last_real_price = df["Preço Real"].iloc[-1]

            # Definir os pontos do funil de previsão
            funnel_x = [last_date, next_date, next_date, last_date]
            funnel_y = [last_real_price, lower_bound, upper_bound, last_real_price]

            # Criar gráfico interativo
            fig = go.Figure()

            # Linha e pontos do preço real
            fig.add_trace(
                go.Scatter(
                    x=df["Data"],
                    y=df["Preço Real"],
                    mode="lines+markers",
                    name="Preço Real",
                    line=dict(color="#1f77b4"),
                    hovertemplate="Data: %{x}<br>Preço Real: R$ %{y:.2f}<extra></extra>",
                )
            )

            # Ponto da previsão do preço na data correta (próximo dia útil)
            fig.add_trace(
                go.Scatter(
                    x=[next_date],  # Agora o ponto de previsão está no dia correto
                    y=[predicted_price],
                    mode="markers",
                    name=f"Previsão ({predicted_price:.2f})",
                    marker=dict(
                        color="#d62728", size=12, line=dict(color="black", width=1)
                    ),
                    hovertemplate="Data: %{x}<br>Previsão: R$ %{y:.2f}<extra></extra>",
                )
            )

            # Funil de previsão
            fig.add_trace(
                go.Scatter(
                    x=funnel_x,
                    y=funnel_y,
                    fill="toself",
                    fillcolor="rgba(214, 39, 40, 0.2)",
                    line=dict(color="#d62728"),
                    name="Intervalo de Previsão",
                    customdata=[[lower_bound, upper_bound]] * len(funnel_x),
                    hovertemplate="Intervalo:<br>Inferior: R$ %{customdata[0]:.2f}<br>Superior: R$ %{customdata[1]:.2f}<extra></extra>",
                )
            )

            # Layout do gráfico
            fig.update_layout(
                title=f"📊 Previsão para {ticker}",
                xaxis_title="Data",
                yaxis_title="Preço (R$)",
                xaxis=dict(tickformat="%d-%b", dtick="D1"),
                template="plotly_dark",
                width=1200,
                height=500,
            )

            # Exibir gráfico
            st.plotly_chart(fig, use_container_width=True)

            # Exibir valores com melhor formatação
            st.markdown(
                f"""
                <div class="prediction-box">
                    📊 <b>Previsão para o próximo dia útil ({next_date.strftime('%d/%m/%Y')}):</b> R$ {predicted_price:.2f} <br>
                    📉 <b>Faixa de previsão:</b> R$ {lower_bound:.2f} - R$ {upper_bound:.2f}
                </div>
                """,
                unsafe_allow_html=True,
            )

    else:
        st.error("❌ Erro ao obter os dados.")

st.markdown("</div>", unsafe_allow_html=True)
