import streamlit as st
import pickle
import pandas as pd
import numpy as np

st.set_page_config(page_title="Laptop Price Predictor", page_icon="💻", layout="wide")

# -------------------- CSS --------------------

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">

<style>

html, body, [class*="css"]  {
font-family: 'Poppins', sans-serif;
background:#f8fafc;
}

.main-title{
font-size:42px;
font-weight:700;
text-align:center;
color:#1f2937;
margin-bottom:10px;
}

.subtitle{
text-align:center;
font-size:18px;
color:#6b7280;
margin-bottom:40px;
}

.card{
background:white;
padding:35px;
border-radius:12px;
box-shadow:0px 4px 20px rgba(0,0,0,0.08);
}

.result-card{
background:#f1f5f9;
padding:30px;
border-radius:12px;
text-align:center;
margin-top:30px;
font-size:28px;
font-weight:600;
}

.stButton>button{
background:#2563eb;
color:white;
font-size:18px;
padding:12px 35px;
border-radius:8px;
border:none;
}

.stButton>button:hover{
background:#1e40af;
}

</style>
""", unsafe_allow_html=True)

# -------------------- Title --------------------

st.markdown("<div class='main-title'>💻 Laptop Price Predictor</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Estimate laptop price prediction</div>", unsafe_allow_html=True)

# -------------------- Load Model --------------------

pipe = pickle.load(open('pipe.pkl','rb'))
df = pickle.load(open('df.pkl','rb'))

# -------------------- Input Card --------------------

st.markdown("<div class='card'>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:

    company = st.selectbox('Brand', df['Company'].unique())

    type_name = st.selectbox('Laptop Type', df['TypeName'].unique())

    ram = st.selectbox('RAM (GB)', [2,4,6,8,12,16,24,32,64])

    weight = st.slider('Weight (kg)', 0.5, 5.0, 1.8, step=0.1)

    touchscreen = st.selectbox('Touchscreen', ['No','Yes'])

    ips = st.selectbox('IPS Display', ['No','Yes'])

with col2:

    screen_size = st.slider('Screen Size (inch)', 10.0, 20.0, 15.6, step=0.1)

    resolution = st.selectbox('Screen Resolution',[
    '1920x1080',
    '1366x768',
    '1600x900',
    '3840x2160',
    '3200x1800',
    '2560x1600',
    '2560x1440',
    '2304x1440'
    ])

    cpu = st.selectbox('CPU Brand', df['Cpu brand'].unique())

    hdd = st.selectbox('HDD (GB)', [0,128,256,512,1024,2048])

    ssd = st.selectbox('SSD (GB)', [0,8,128,256,512,1024])

    gpu = st.selectbox('GPU Brand', df['Gpu brand'].unique())

    os = st.selectbox('Operating System', df['os'].unique())

st.markdown("</div>", unsafe_allow_html=True)

# -------------------- Predict Button Center --------------------

col1, col2, col3 = st.columns([1,1,1])

with col2:
    predict = st.button("Predict Price")

# -------------------- Prediction --------------------

if predict:

    touchscreen = 1 if touchscreen == 'Yes' else 0
    ips = 1 if ips == 'Yes' else 0

    X_res = int(resolution.split('x')[0])
    Y_res = int(resolution.split('x')[1])

    if screen_size == 0:
        st.error("Screen size cannot be zero")

    else:

        ppi = ((X_res**2) + (Y_res**2))**0.5 / screen_size

        query = pd.DataFrame({
        'Company':[company],
        'TypeName':[type_name],
        'Ram':[ram],
        'Weight':[weight],
        'Touchscreen':[touchscreen],
        'Ips':[ips],
        'ppi':[ppi],
        'Cpu brand':[cpu],
        'HDD':[hdd],
        'SSD':[ssd],
        'Gpu brand':[gpu],
        'os':[os]
        })

        prediction = int(np.exp(pipe.predict(query)[0]))

        st.markdown(f"""
        <div class="result-card">
        Estimated Laptop Price <br><br>
        ₹ {prediction:,}
        </div>
        """, unsafe_allow_html=True)