import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly_express as px
import plotly.graph_objs as go
#import openpyxl

st.set_page_config(layout='wide')

st.title("Statistik Kependudukan Provinsi Jawa Barat")
st.subheader("", divider='rainbow')

def kependudukan():
    with st.container(border=True):
        #st.subheader("Kependudukan")
        penduduktotal = pd.read_excel('data/proyeksi-penduduk-total.xlsx')
        penduduktotal_tranposed = penduduktotal.melt(id_vars=['Tahun'], value_vars=['00 - 04', '05 - 09', '10 - 14', '15 - 19', '20 - 24', '25 - 29', '30 - 34', '35 - 39', 
                                                                                    '40 - 44', '45 - 49', '50 - 54', '55 - 59', '60 - 64', '65 - 69', '70 - 74', '75+'],
                                                    var_name='Umur', value_name='Total').sort_values(by=['Tahun', 'Umur'])
        penduduktotal_tranposed['Umur'] = penduduktotal_tranposed['Umur'].astype(str)
        penduduklaki = pd.read_excel('data/proyeksi-penduduk-laki.xlsx')
        penduduklaki_tranposed = penduduklaki.melt(id_vars=['Tahun'], value_vars=['00 - 04', '05 - 09', '10 - 14', '15 - 19', '20 - 24', '25 - 29', '30 - 34', '35 - 39', 
                                                                                    '40 - 44', '45 - 49', '50 - 54', '55 - 59', '60 - 64', '65 - 69', '70 - 74', '75+'],
                                                    var_name='Umur', value_name='Total').sort_values(by=['Tahun', 'Umur'])
        penduduklaki_tranposed['Umur'] = penduduklaki_tranposed['Umur'].astype(str)
        penduduklaki_tranposed = penduduklaki_tranposed.rename(columns={'Total':'Laki-laki'})
        pendudukperempuan = pd.read_excel('data/proyeksi-penduduk-perempuan.xlsx')
        pendudukperempuan_tranposed = pendudukperempuan.melt(id_vars=['Tahun'], value_vars=['00 - 04', '05 - 09', '10 - 14', '15 - 19', '20 - 24', '25 - 29', '30 - 34', '35 - 39', 
                                                                                    '40 - 44', '45 - 49', '50 - 54', '55 - 59', '60 - 64', '65 - 69', '70 - 74', '75+'],
                                                    var_name='Umur', value_name='Total').sort_values(by=['Tahun', 'Umur'])
        pendudukperempuan_tranposed['Umur'] = pendudukperempuan_tranposed['Umur'].astype(str)
        pendudukperempuan_tranposed = pendudukperempuan_tranposed.rename(columns={'Total':'Perempuan'})
        
        gabunglakipr = pd.merge(penduduklaki_tranposed, pendudukperempuan_tranposed, on=['Tahun', 'Umur'], how='left')
        
        penduduk_kabkot_umur = pd.read_excel('data/proyeksi-kabkot-umur.xlsx')
        penduduk_kabkot_umur['Tahun'] = penduduk_kabkot_umur['Tahun'].astype(str)
        
        penduduk_kabkot_jk = pd.read_excel('data/proyeksi-kabkot-jk.xlsx')
        penduduk_kabkot_jk['Tahun'] = penduduk_kabkot_jk['Tahun'].astype(int)

### PENDUDUK TOTAL        
        kotak_penduduk_total, kotak_umur = st.columns(2)
        with kotak_penduduk_total:
            with st.container(border=True, height=500):
                st.info("**Proyeksi Penduduk Jawa Barat** (Ribu Jiwa), 2010-2035")
                st.bar_chart(penduduktotal, x='Tahun', y='Jumlah')

### KELOMPOK UMUR BATANG        
        with kotak_umur:
            with st.container(border=True, height=500):
                fig1a = px.bar(penduduktotal_tranposed, x='Umur', y='Total', height=400,
                               animation_frame='Tahun', animation_group='Umur')
                fig1a.update_traces(marker_color='darkblue')
                
                st.info(f"Penduduk Jawa Barat menurut Kelompok Umur, 2010-2035")
                st.plotly_chart(fig1a)
        
### LAKI-LAKI                 
        kotak_penduduk_laki, kotak_piramida, kotak_penduduk_perempuan = st.columns(3)
        with kotak_penduduk_laki:
            with st.container(border=True, height=500):
                st.success("Proyeksi Penduduk **Laki-laki** Jawa Barat (Ribu Jiwa), 2010-2035")
                fig1c = px.bar(penduduklaki, x='Tahun', y='Jumlah', height=400)
                fig1c.update_traces(marker_color='green')
                st.plotly_chart(fig1c)

### PIRAMIDA JABAR                
        with kotak_piramida:
            with st.container(border=True, height=500):
                gabunglakipr['Laki-laki'] = gabunglakipr['Laki-laki'] * -1
                #tahun_terpilih = st.slider("", min_value=2010, max_value=2035, value=2024)
                
                fig1b = px.bar(gabunglakipr, x=['Laki-laki', 'Perempuan'], y='Umur', labels={'variable':''},
                             orientation='h', animation_frame='Tahun', animation_group='Umur', height=375,
                             color_discrete_map={'Laki-laki':'green', 'Perempuan':'yellow'})
                # Menempatkan legenda di bawah tengah
                fig1b.update_layout(
                    xaxis_title="",
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=-0.2,
                        xanchor="center",
                        x=0.5
                    )
                )
                st.info(f"Piramida Penduduk Jawa Barat")
                st.plotly_chart(fig1b)

### PEREMPUAN                
        with kotak_penduduk_perempuan:
            with st.container(border=True, height=500):
                st.warning("Proyeksi Penduduk **Perempuan** Jawa Barat (Ribu Jiwa), 2010-2035")
                fig1d = px.bar(pendudukperempuan, x='Tahun', y='Jumlah', height=400)
                fig1d.update_traces(marker_color='yellow')
                st.plotly_chart(fig1d)

### KABKOT        
        penduduk_kabkotjk = penduduk_kabkot_jk.drop(penduduk_kabkot_jk[penduduk_kabkot_jk['Wilayah'] == 'JAWA BARAT'].index)
        
        kabkotjk = penduduk_kabkotjk.melt(id_vars=['Tahun', 'Wilayah'], value_vars=['Laki-laki', 'Perempuan'], 
                                                    var_name='Jenis Kelamin', value_name='Penduduk')
                    
        st.subheader("", divider='rainbow')
        st.subheader("Penduduk Jawa Barat menurut Kabupaten/ Kota, 2020 - 2045")
        kabkot1 = st.container(border=True)
        with kabkot1:
            penduduk_kabkot_umur['Laki-laki'] = penduduk_kabkot_umur['Laki-laki'] * -1
           
            tahun_terunik = penduduk_kabkot_jk['Tahun'].unique()
            tahun_min = int(tahun_terunik.min())
            tahun_max = int(tahun_terunik.max())

            tahun_terpilih = st.slider('Filter Tahun', tahun_min, tahun_max, key='filtertahun1')
                           
            kol3, kol4 = st.columns(2)

### TREEMAP TOTAL KABKOT          
            with kol3:
                with st.container(border=True):
                    st.info(f"Proyeksi Penduduk Kabupaten Kota (Jiwa), {tahun_terpilih}")
                    
                    fig1f = px.treemap(kabkotjk[kabkotjk['Tahun'] == tahun_terpilih],
                                       path=['Wilayah', 'Jenis Kelamin'], values='Penduduk')
                    st.plotly_chart(fig1f)
### PIE TOTAL KABKOT
            with kol4:
                with st.container(border=True):
                    st.info(f"Sebaran Penduduk Kabupaten Kota (Jiwa), {tahun_terpilih}")
                    penduduk_kabkotjk = penduduk_kabkot_jk.drop(penduduk_kabkot_jk[penduduk_kabkot_jk['Wilayah'] == 'JAWA BARAT'].index)
        
                    fig1g = px.pie(penduduk_kabkotjk[penduduk_kabkotjk['Tahun'] == tahun_terpilih],
                                    names='Wilayah', values='Total')
                    st.plotly_chart(fig1g)

        st.subheader("", divider='blue')
### KABKOT JENIS KELAMIN
        kabkot2 = st.container(border=True)
        with kabkot2:            
            kabkot_terpilih = st.selectbox("Filter Kabupaten/Kota", penduduk_kabkot_umur.Wilayah.unique())
        
            kol5, kol6 = st.columns(2)
            with kol5:
                with st.container(border=True, height=550):
                    st.info(f"PIRAMIDA PENDUDUK {kabkot_terpilih}")
                                
                    fig1e = px.bar(penduduk_kabkot_umur[(penduduk_kabkot_umur['Wilayah'] == kabkot_terpilih)], 
                                x=['Laki-laki', 'Perempuan'], y='Umur', labels={'variable':''},
                                    orientation='h', animation_frame='Tahun', animation_group='Umur',
                                    color_discrete_map={'Laki-laki':'brown', 'Perempuan':'orange'})
                    # Menempatkan legenda di bawah tengah
                    fig1e.update_layout(
                        xaxis_title="",
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=-0.2,
                            xanchor="center",
                            x=0.5
                        )
                    )
                    if kabkot_terpilih:
                        st.plotly_chart(fig1e)

            with kol6:
                with st.container(border=True, height=550):
                    st.info(f"PENDUDUK {kabkot_terpilih} MENURUT JENIS KELAMIN")
                    
                    tahun_terpilih2 = st.slider('Filter Tahun', tahun_min, tahun_max, key='filtertahun2')
                    
                    fig1h = px.pie(kabkotjk[(kabkotjk['Wilayah'] == kabkot_terpilih) & (kabkotjk['Tahun'] == tahun_terpilih2)], 
                                names='Jenis Kelamin', values='Penduduk', hover_data=['Wilayah', 'Tahun'], color='Jenis Kelamin',
                                color_discrete_map={'Laki-laki':'brown', 'Perempuan':'orange'}, height=375)
                    fig1h.update_layout(
                        xaxis_title="",
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=-0.2,
                            xanchor="center",
                            x=0.5
                        )
                    )
                    st.plotly_chart(fig1h)
        
    with st.expander("UNDUH SUMBER DATA"):
        tabel, publikasi, metadata, standardata = st.tabs(['TABEL', 'PUBLIKASI', 'METADATA', 'STANDAR DATA'])
        with tabel:
            components.iframe("https://jabar.bps.go.id/subject/12/kependudukan.html#subjekViewTab3")
            st.link_button("Buka Tautan", "https://jabar.bps.go.id/subject/12/kependudukan.html#subjekViewTab3")
        with publikasi:
            components.iframe("https://jabar.bps.go.id/publication.html")
            st.link_button("Buka Tautan", "https://jabar.bps.go.id/publication.html")
        with metadata:
            components.iframe("https://sirusa.web.bps.go.id/metadata/")
            st.link_button("Buka Tautan", "https://sirusa.web.bps.go.id/metadata/")
        with standardata:
            components.iframe("https://indah.bps.go.id/standar-data-statistik-nasional")        
            st.link_button("Buka Tautan", "https://indah.bps.go.id/standar-data-statistik-nasional")
        
    return kotak_penduduk_total, kotak_umur, kotak_piramida, kotak_penduduk_laki, kotak_penduduk_perempuan, kabkot1
kotak_penduduk_total, kotak_umur, kotak_piramida, kotak_penduduk_laki, kotak_penduduk_perempuan, kabkot1 = kependudukan()
