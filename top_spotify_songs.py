import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image

#Ler a base de dados

df = pd.read_csv("https://github.com/yasminkanoshiki/top_spotify_songs/blob/main/spotify_history.csv")
logo = Image.open("https://github.com/yasminkanoshiki/top_spotify_songs/blob/main/spotify-logo.png")
st.image(logo, width=120)

#Manipulação dos dados e limpeza do banco

renomear_colunas = {
    'spotify_track_uri': 'uri_spotify',
    'ts': 'inicio_reproducao',
    'platform': 'plataforma',
    'ms_played': 'ms_reproduzidos',
    'track_name': 'nome_faixa',
    'artist_name': 'nome_artista',
    'album_name': 'nome_album',
    'reason_start': 'motivo_inicio',
    'reason_end': 'motivo_fim',
    'shuffle': 'modo_aleatorio',
    'skipped': 'musica_pulada'
}

df = df.rename(columns=renomear_colunas)

renomear_valores_motivo_inicio = {
    'clickrow': 'Clique Direto na Faixa',
    'trackdone': 'Fim da Faixa Anterior',
    'backbtn': 'Botão Voltar',
    'fwdbtn': 'Botão Avançar',
    'playbtn': 'Botão Play',
    'autoplay': 'Reprodução Automática',
    'remote': 'Dispositivo Remoto',
    'context_switch': 'Troca de Contexto (Playlist/Álbum)',
    'endplay': 'Fim de Reprodução',
    'uri_click': 'Clique em Link Externo',
    'ads_playback': 'Reprodução de Anúncio',
    'trackerror': 'Erro na Faixa',
    'appload': 'Início da Aplicação',
    'restart': 'Reinício da Faixa',
    'unknown': 'Motivo Desconhecido',
    'playback_rate_change': 'Mudança na Velocidade de Reprodução',
    'voice': 'Comando de Voz',
    'notification': 'Início por Notificação',
    'shuffle': 'Reprodução Aleatória',
    'repeat': 'Reprodução Repetida',
    'queue': 'Faixa da Fila',
    'recommendation': 'Recomendação do Spotify',
    'library': 'Início pela Biblioteca',
    'collection': 'Início por Coleção',
    'nextbtn': 'Botão Próximo',

}

df['motivo_inicio'] = df['motivo_inicio'].map(renomear_valores_motivo_inicio).fillna(df['motivo_inicio'])

renomear_motivos_fim = {
   'trackdone': 'Faixa Finalizada',
    'fwdbtn': 'Pulada para Próxima Faixa',
    'backbtn': 'Retorno à Faixa Anterior',
    'pausebtn': 'Pausada pelo Usuário',
    'remote': 'Interrompida por Dispositivo Remoto',
    'endplay': 'Fim da Reprodução',
    'logout': 'Logout da Conta',
    'context_switch': 'Troca de Playlist ou Álbum',
    'trackerror': 'Erro na Faixa',
    'ads_playback': 'Interrompida por Anúncio',
    'appload': 'Encerrada ao Abrir o App',
    'restart': 'Reinício da Faixa',
    'unknown': 'Motivo Desconhecido',
    'playback_rate_change': 'Mudança na Velocidade de Reprodução',
    'voice': 'Interrompida por Comando de Voz',
    'notification': 'Interrompida por Notificação',
    'shuffle': 'Interrompida por Reprodução Aleatória',
    'repeat': 'Interrompida por Reprodução Repetida',
    'queue': 'Saída da Fila',
    'recommendation': 'Interrompida após Recomendação',
    'library': 'Encerrada na Biblioteca',
    'collection': 'Encerrada na Coleção',
    'nextbtn': 'Pulada com Botão Próximo'
}

df['motivo_fim'] = df['motivo_fim'].map(renomear_motivos_fim).fillna(df['motivo_fim'])

renomear_plataformas = {
    'android': 'Mobile',
    'iOS': 'Mobile',
    'windows': 'Desktop',
    'mac': 'Desktop',
    'web player': 'Web',
    'cast to device': 'Transmissão'
}

df['plataforma'] = df['plataforma'].map(renomear_plataformas).fillna(df['plataforma'])

renomear_musicas_puladas = {
    True : 'Sim',
    False : 'Não'
}

df['musica_pulada'] = df['musica_pulada'].map(renomear_musicas_puladas).fillna(df['musica_pulada'])


#Início do dashboard no streamlit

st.set_page_config(
    page_title='Dashboard Top Músicas do Spotify',
    page_icon='📊',
    layout='wide')

st.header('Top Músicas do Spotify Global')
st.markdown('Nesse dashboard conseguimos analisar padrões globais de escuta no Spotify, destacando artistas, faixas, hábitos e motivos de reprodução. O período analisado varia de 2013 a 2024')

#Filtros

st.sidebar.header('Filtro')

artistas_select = ['Todos os artistas'] + sorted(df['nome_artista'].unique())
artista_selecionado = st.sidebar.selectbox("Artista:", artistas_select)

if artista_selecionado == 'Todos os artistas':
    df_filtrado = df
else:
    df_filtrado = df[df['nome_artista'].isin([artista_selecionado])]


artista_mais_reproduzido = df_filtrado['nome_artista'].mode()[0]
faixa_mais_reproduzida = df_filtrado['nome_faixa'].mode()[0]
album_mais_reproduzido = df_filtrado['nome_album'].mode()[0]
numero_reproducoes = len(df_filtrado['uri_spotify'])


col1, col2, col3, col4 = st.columns(4)
col1.markdown('**Top Artista**')
col1.subheader(f":green[{artista_mais_reproduzido}]")
col2.markdown('**Top Música**')
col2.subheader(f":green[{faixa_mais_reproduzida}]")
col3.markdown('**Top Álbum**')
col3.subheader(f":green[{album_mais_reproduzido}]")
col4.markdown('**N° de Reproduções Totais**')
col4.subheader(f":green[{numero_reproducoes-1}]")

st.markdown("---")


#Gráficos

top_5_artistas = df_filtrado.groupby('nome_artista')['nome_artista'].value_counts().nlargest(5).sort_values(ascending=False).reset_index()
top_5_artistas.columns = ['nome_artista', 'quantidade']
graf1 = px.bar(
    top_5_artistas,
    x = 'nome_artista',
    y = 'quantidade',
    orientation='v',
    title = 'Top 5 Artistas',
    labels = {'nome_artista' : 'Top Artista', 'quantidade' : 'Quantidade'},
    color_discrete_sequence=["#A5D6A7", "#66BB6A", "#32CD32", "#228B22", "#006400"]
    )

graf1.update_layout(title_x=0.5)

musica_pulada = df_filtrado['musica_pulada'].value_counts().reset_index()
musica_pulada.columns = ['musica_pulada', 'quantidade']
graf2 = px.pie(
        musica_pulada,
        names = 'musica_pulada',
        values = 'quantidade',
        title = 'Taxa de músicas puladas',
        hole = 0.5,
        color_discrete_sequence=["#A5D6A7", "#66BB6A", "#32CD32", "#228B22", "#006400"]
    )

graf2.update_traces(
    textposition='outside',
    textinfo='percent+label',
    pull=[0.05]*len(musica_pulada))

graf2.update_layout(title_x=0.5)


col_graf1, col_graf2 = st.columns(2)
col_graf1.plotly_chart(graf1)
col_graf2.plotly_chart(graf2)

#Graficos coluna 2


plataforma_utilizada = df_filtrado['plataforma'].value_counts().reset_index()
plataforma_utilizada.columns = ['plataforma_utilizada', 'quantidade']
graf3 = px.pie(
        plataforma_utilizada,
        names = 'plataforma_utilizada',
        values = 'quantidade',
        title = 'Tipo de plataforma mais utilizada',
        color_discrete_sequence=["#A5D6A7", "#66BB6A", "#32CD32", "#228B22", "#006400"]
    )

graf3.update_traces(
    textposition='outside',
    textinfo='percent+label',
    pull=[0.05]*len(plataforma_utilizada)  
)

graf3.update_layout(
    title_x=0.5,  
    width=800,
    height=600,
    margin=dict(t=80, b=80, l=80, r=80)  
)

top_5_musicas = df_filtrado.groupby('nome_faixa')['nome_faixa'].value_counts().nlargest(5).sort_values(ascending=True).reset_index()
top_5_musicas.columns = ['nome_faixa', 'quantidade']
graf4 = px.bar(
    top_5_musicas,
    x='quantidade',
    y='nome_faixa',
    orientation='h',
    title='Top 5 músicas',
    labels={'nome_faixa' : 'Top Músicas', 'quantidade' : 'Quantidade'},
    color_discrete_sequence=["#A5D6A7", "#66BB6A", "#32CD32", "#228B22", "#006400"]
)

graf4.update_layout(xaxis=dict(tickfont=dict(size=10)), title_x=0.5)


col_graf3, col_graf4 = st.columns(2)
col_graf3.plotly_chart(graf3)
col_graf4.plotly_chart(graf4)

df_filtrado['inicio_reproducao'] = pd.to_datetime(df_filtrado['inicio_reproducao'], errors='coerce')

df_filtrado['data'] = df_filtrado['inicio_reproducao'].dt.date
linha_do_tempo = df_filtrado.groupby('data').size().reset_index(name='quantidade')
graf5 = px.ecdf(
    linha_do_tempo,
    x='data',
    y='quantidade',
    color_discrete_sequence=["#A5D6A7", "#66BB6A", "#32CD32", "#228B22", "#006400"]
)

graf5.update_layout(title=0.5)

st.plotly_chart(graf5, use_container_width=True)


st.dataframe(df_filtrado[['nome_faixa', 'nome_artista', 'nome_album', 'motivo_inicio', 'motivo_fim', 'musica_pulada']])

