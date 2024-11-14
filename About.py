import streamlit as st
# streamlit run main.py --server.port 8503
st.title("About Me")

col1, col2, = st.columns(2, gap='large')




with col1:
    st.image('image/Mikael-2.jpg', use_column_width=True)


with col2:
    st.markdown("""
    <style>
    .big-font {
        font-size:24px !important;
    }
    </style>
    """, unsafe_allow_html=True)
    st.subheader('Tentang Pembuat')

    # st.write(
    #     "Website ini dibuat oleh Mikael Reichi Sopany, mahasiswa Teknik Informatika, Fakultas Teknologi Informasi, Universitas Tarumanagara"
    # )
    # st.write(
    #     "Website dibuat sebagai hasil karya skripsi dengan tujuan untuk memenuhi syarat kelulusan dalam mendapatkan gelar Sarjana Komputer"
    # )
    

    st.markdown('<p class="big-font">Website ini dibuat oleh Mikael Reichi Sopany, mahasiswa Teknik Informatika, Fakultas Teknologi Informasi, Universitas Tarumanagara</p>', unsafe_allow_html=True)
    st.markdown('<p class="big-font">Website dibuat sebagai hasil karya skripsi dengan tujuan untuk memenuhi syarat kelulusan dalam mendapatkan gelar Sarjana Komputer</p>', unsafe_allow_html=True)

# with col3:
#     st.write(
#         "Let's start building! For help and uwu, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
#     )

st.markdown('<p class="big-font">'
            'Dosen Pembimbing:'
            '</p>', 
            unsafe_allow_html=True)
st.markdown('<p class="big-font">'
            'Teny Handhayani S.Kom., M.Kom., Ph.D.'
            '</p>', 
            unsafe_allow_html=True)
st.markdown('<p class="big-font">'
            'Irvan Lewenusa S.KOM., M.KOM.'
            '</p>', 
            unsafe_allow_html=True)