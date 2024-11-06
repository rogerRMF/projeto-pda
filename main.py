import streamlit as st
from datetime import datetime
import pandas as pd
import pytz

st.sidebar.image("https://www.senior.com.br/wp-content/uploads/2014/12/ID-Logistics.jpg", use_column_width=True)

# Título do aplicativo
st.title("Controle de Acesso do PDA")
st.markdown(
    """
    <div style="display: flex; justify-content: flex-end;">
        <img src="https://ae-pic-a1.aliexpress-media.com/kf/S09c08762dfbf4073ad19cad2058b5f31k.jpg_640x640Q90.jpg" alt="Imagem" style="width: 100px; height: auto;">
    </div>
    """,
    unsafe_allow_html=True
)

# Inicializa o estado dos registros, caso ainda não tenha sido criado
if "registros" not in st.session_state:
    st.session_state["registros"] = []

# Menu lateral para navegação
menu = st.sidebar.selectbox("Selecione uma opção", ["Registro", "Consulta"])

# Página de Registro
if menu == "Registro":
    # Entrada de dados para ID do funcionário e número do patrimônio do PDA
    # st.subheader("Registro de PDA")
    id_funcionario = st.text_input("ID do Funcionário")
    numero_patrimonio = st.text_input("Número do Patrimônio do PDA")

    # Função para registrar a retirada
    if st.button("Registrar Retirada do PDA"):
        if id_funcionario and numero_patrimonio:
            data_hora_retirada = datetime.now().strftime("%d/%m/%y %H:%M:%S")
            # Salva o registro no estado de sessão
            st.session_state["registros"].append({
                "ID Funcionário": id_funcionario,
                "Número Patrimônio": numero_patrimonio,
                "Data e Hora Retirada": data_hora_retirada,
                "Data e Hora Devolução": None
            })
            st.success(f"Retirada registrada com sucesso! Data e Hora da Retirada: {data_hora_retirada}")
            st.balloons()
        else:
            st.error("Preencha ambos os campos (ID do Funcionário e Número do Patrimônio) para registrar a retirada.")

    # Função para registrar a devolução
    if st.button("Registrar Devolução do PDA"):
        if id_funcionario and numero_patrimonio:
            # Verifica se o PDA foi retirado antes
            pda_encontrado = False
            for registro in st.session_state["registros"]:
                if registro["ID Funcionário"] == id_funcionario and registro["Número Patrimônio"] == numero_patrimonio:
                    pda_encontrado = True
                    if registro["Data e Hora Devolução"] is None:
                        # Se ainda não foi devolvido, registra a devolução
                        data_hora_devolucao = datetime.now().strftime("%d/%m/%y %H:%M:%S")
                        registro["Data e Hora Devolução"] = data_hora_devolucao
                        st.success(f"Devolução registrada com sucesso! Data e Hora da Devolução: {data_hora_devolucao}")
                        st.balloons()
                    else:
                        st.error("Este PDA já foi devolvido anteriormente.")
                    break
            
            if not pda_encontrado:
                st.error("Não existe este PDA registrado em nosso banco de dados de retiradas.")

        else:
            st.error("Preencha ambos os campos (ID do Funcionário e Número do Patrimônio) para registrar a devolução.")

# Página de Consulta
elif menu == "Consulta":
    st.subheader("Consulta de Registros")
    
    # Mostra a tabela com todos os registros
    if st.session_state["registros"]:
        st.write("Registros de Retirada e Devolução:")
        df = pd.DataFrame(st.session_state["registros"])
        st.table(df)

        # Botão para exportar para CSV
        if st.button("Exportar para CSV"):
            # Converte o DataFrame em CSV
            csv_data = df.to_csv(index=False).encode("utf-8")
            st.success("Arquivo CSV gerado com sucesso!")

            # Botão para download do arquivo CSV
            st.download_button(
                label="Baixar arquivo CSV",
                data=csv_data,
                file_name="Registros_PDA.csv",
                mime="text/csv"
            )
    else:
        st.info("Nenhum registro encontrado.")

import pytz

def get_brasilia_time():
    """Retorna a data e hora atual de Brasília em um formato amigável."""
    brasilia_timezone = pytz.timezone('America/Sao_Paulo')
    brasilia_time = datetime.now(brasilia_timezone)
    return brasilia_time.strftime("%d/%m/%Y %H:%M:%S")

# Obtém a hora de Brasília
brasilia_time = get_brasilia_time()

# Cria um container para a hora
with st.container():
    st.markdown(f"""
    <div style='
        text-align: right;
        position: fixed;
        bottom: 0;
        right: 0;
        padding: 10px;
        font-weight: bold;
        font-size: 18px; /* Ajusta o tamanho da fonte */
        color: #111; /* Define a cor da fonte */
        '>
        {brasilia_time}
    </div>
    """, unsafe_allow_html=True)