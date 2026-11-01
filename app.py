import os
import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from PIL import Image
import time
import glob
import paho.mqtt.client as paho
import json
from gtts import gTTS
from googletrans import Translator

def on_publish(client,userdata,result):             #create function for callback
    print("el dato ha sido publicado \n")
    pass

def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received=str(message.payload.decode("utf-8"))
    st.write(message_received)

broker="broker.mqttdashboard.com"
port=1883
client1= paho.Client("GIT-HUBC")
client1.on_message = on_message



st.set_page_config(page_title="Cava por Voz", page_icon="🍷")

# ------------------------------------------------------------------
# TEMA "CAVA POR VOZ" (solo estilos CSS; la lógica y los inputs no cambian)
# ------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600;700&family=Nunito:wght@400;600;700&display=swap');

:root{
  --vino:#6b1e2e;
  --vino-oscuro:#3f0f1a;
  --dorado:#c9a45c;
  --dorado-claro:#f3e7cc;
  --crema:#faf6ef;
  --piedra:#efe7da;
  --tinta:#1f1a17;
}

/* Fondo: muro de piedra clara de la cava */
.stApp{
  background:
    repeating-linear-gradient(0deg, transparent 0 58px, rgba(140,110,80,.07) 58px 60px),
    var(--piedra);
  background-attachment: fixed;
}
header[data-testid="stHeader"]{ background: transparent; }

/* Panel central: etiqueta de botella */
[data-testid="stMainBlockContainer"], .block-container{
  background:var(--crema);
  border-radius:20px;
  border:1px solid rgba(201,164,92,.55);
  box-shadow:0 20px 50px rgba(63,15,26,.14);
  margin-top:2rem;
  margin-bottom:4rem;
  padding:1.6rem 2.2rem 2.4rem !important;
  max-width:780px;
}
@media (max-width:640px){
  [data-testid="stMainBlockContainer"], .block-container{
    padding:1.1rem 1rem 1.8rem !important;
  }
}

/* Encabezado: placa de la cava */
.cava-hero{
  border-radius:16px;
  padding:1.8rem 1.8rem 1.6rem;
  margin-bottom:.6rem;
  background:linear-gradient(135deg, var(--vino-oscuro) 0%, var(--vino) 100%);
  box-shadow: inset 0 0 0 1px rgba(201,164,92,.5), inset 0 0 0 6px var(--vino-oscuro), inset 0 0 0 7px rgba(201,164,92,.35);
}
.cava-tag{
  display:inline-block;
  font-family:'Nunito', sans-serif;
  font-weight:700; font-size:.78rem; letter-spacing:.16em; text-transform:uppercase;
  color:var(--vino-oscuro);
  background:var(--dorado);
  padding:.3rem .8rem; border-radius:999px;
}
.cava-title{
  font-family:'Cormorant Garamond', serif;
  font-weight:700; font-size:3rem; line-height:1.05;
  color:var(--dorado-claro);
  margin:.8rem 0 .4rem;
}
.cava-sub{
  font-family:'Nunito', sans-serif;
  font-size:1.05rem; line-height:1.55;
  color:#f5ece6;
  max-width:540px;
}
.cava-ideal{ display:flex; flex-wrap:wrap; gap:.5rem; margin-top:1.1rem; }
.cava-ideal span{
  font-family:'Nunito', sans-serif; font-weight:700; font-size:.9rem;
  color:#ffffff;
  background:rgba(255,255,255,.1);
  border:1px solid rgba(201,164,92,.55);
  padding:.35rem .85rem; border-radius:999px;
}
@media (max-width:640px){
  .cava-title{ font-size:2.2rem; }
}

/* Títulos y textos del contenido */
h2, h3{
  font-family:'Cormorant Garamond', serif !important;
  font-weight:700 !important;
  color:var(--vino) !important;
}
h1 a, h2 a, h3 a{ display:none !important; }
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li{
  font-family:'Nunito', sans-serif;
  line-height:1.6;
}
.stApp hr{ border-color: rgba(201,164,92,.45); }

/* Imagen: enmarcada como una etiqueta */
[data-testid="stImage"] img{
  border-radius:14px;
  border:1px solid rgba(201,164,92,.6);
  box-shadow:0 10px 24px rgba(63,15,26,.15);
}

/* Órdenes de voz */
.cava-ordenes-titulo{
  font-family:'Cormorant Garamond', serif;
  font-weight:700; font-size:1.5rem;
  color:var(--vino);
  margin:1.2rem 0 .5rem;
}
.cava-ordenes{
  display:grid; grid-template-columns:repeat(auto-fit, minmax(210px, 1fr)); gap:.6rem;
  margin-bottom:1rem;
}
.cava-orden{
  background:#ffffff;
  border:1px solid rgba(201,164,92,.6);
  border-left:4px solid var(--vino);
  border-radius:12px;
  padding:.7rem .9rem;
  font-family:'Nunito', sans-serif;
  color:var(--tinta);
}
.cava-orden b{ display:block; font-size:1.02rem; color:var(--vino-oscuro); }
.cava-orden small{ color:#5a4f47; font-size:.88rem; }

/* Barra lateral: piedra cálida */
section[data-testid="stSidebar"]{
  background:var(--crema);
  border-right:3px solid var(--vino);
}
section[data-testid="stSidebar"] h3{ font-size:1.3rem !important; }

/* Textos sobre fondos claros: siempre en negro (también si Streamlit usa el tema oscuro) */
.stApp [data-testid="stWidgetLabel"] p,
.stApp [data-testid="stWidgetLabel"] label,
.stApp [data-testid="stMarkdownContainer"] p,
.stApp [data-testid="stMarkdownContainer"] li,
.stApp [data-testid="stCaptionContainer"],
.stApp [data-testid="caption"],
.stApp [data-testid="stAlert"] [data-testid="stMarkdownContainer"] *{
  color:#1a1a1a !important;
}

/* Botones: conservan los colores originales de Streamlit (contraste) */
.stApp button [data-testid="stMarkdownContainer"],
.stApp button [data-testid="stMarkdownContainer"] *,
.stApp button [data-testid="stMarkdownContainer"] p{
  color:inherit !important;
  font-family:inherit !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="cava-hero">
  <span class="cava-tag">🎙️ Interfaces multimodales</span>
  <div class="cava-title">Cava por Voz</div>
  <div class="cava-sub">Controla la luz y la puerta de tu cava con la voz, sin soltar la copa.</div>
  <div class="cava-ideal"><span>💡 Luz de la cava</span><span>🚪 Puerta de la cava</span></div>
</div>
""", unsafe_allow_html=True)

image = Image.open('voice_ctrl.jpg')

st.image(image, width=200)




st.markdown("""
<div class="cava-ordenes-titulo">🗣️ Órdenes que entiende tu cava</div>
<div class="cava-ordenes">
  <div class="cava-orden"><b>“enciende las luces”</b><small>💡 Prende la luz de la cava</small></div>
  <div class="cava-orden"><b>“apaga las luces”</b><small>🌑 Apaga la luz de la cava</small></div>
  <div class="cava-orden"><b>“abre la puerta”</b><small>🚪 Abre la puerta de la cava</small></div>
  <div class="cava-orden"><b>“Cierra la puerta”</b><small>🔒 Cierra la puerta de la cava</small></div>
</div>
""", unsafe_allow_html=True)

st.write("🎙️ Toca el botón **Inicio** y di una de las órdenes en voz alta:")

stt_button = Button(label=" Inicio ", width=200)

stt_button.js_on_event("button_click", CustomJS(code="""
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
 
    recognition.onresult = function (e) {
        var value = "";
        for (var i = e.resultIndex; i < e.results.length; ++i) {
            if (e.results[i].isFinal) {
                value += e.results[i][0].transcript;
            }
        }
        if ( value != "") {
            document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
        }
    }
    recognition.start();
    """))

result = streamlit_bokeh_events(
    stt_button,
    events="GET_TEXT",
    key="listen",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0)

if result:
    if "GET_TEXT" in result:
        st.write(result.get("GET_TEXT"))
        client1.on_publish = on_publish                            
        client1.connect(broker,port)  
        message =json.dumps({"Act1":result.get("GET_TEXT").strip()})
        ret= client1.publish("voice_ctrl", message)

    
    try:
        os.mkdir("temp")
    except:
        pass
