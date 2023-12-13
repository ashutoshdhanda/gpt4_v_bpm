import os
import streamlit as st
import requests
import tempfile
import base64
from htmlTemplates import css, bot_template, user_template, scrollable_box_css, response_css

EULA_ACCEPTED_KEY = 'eula_accepted'


# Function to display EULA
def show_eula():
    # Hide the Streamlit footer and main menu, and define styles for the scrollable box
    style = """
        <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            .scrollable-box {
                height: 400px;
                overflow-y: scroll;
                background-color: rgba(255, 255, 255, 0.5);
                padding: 10px;
                border-radius: 5px;
                margin-bottom: 20px;
                white-space: pre-wrap;  # Ensures that the text will wrap
            }
        </style>
    """
    st.markdown(style, unsafe_allow_html=True)

    st.title("Términos de Uso")

    texto_terminos = "Al utilizar nuestra Aplicación Web basada en Inteligencia Artificial Generativa, usted acepta los siguientes términos y condiciones. Esta aplicación utiliza tecnología de IA generativa avanzada y, como usuario, debe entender que las interacciones con dicha tecnología pueden producir resultados impredecibles, y que el contenido generado debe usarse con discreción. Usted es responsable de garantizar que los datos proporcionados no infrinjan los derechos de privacidad o propiedad intelectual de terceros, y debe estar consciente de que, a pesar de nuestros esfuerzos por asegurar la aplicación y los datos de los usuarios, no se puede garantizar una seguridad completa contra amenazas cibernéticas y accesos no autorizados. Los derechos de propiedad intelectual de la aplicación y el contenido generado pertenecen a nuestra empresa, y su uso no le otorga la propiedad de ningún derecho intelectual relacionado con la aplicación o su contenido. No nos hacemos responsables de daños directos, indirectos, incidentales o consecuentes derivados de su uso de la aplicación, incluyendo aquellos relacionados con inexactitudes, contenido ofensivo o violaciones de seguridad. El uso indebido de la aplicación o su contenido generado puede resultar en la terminación de su acceso. Nos reservamos el derecho de modificar estos términos y condiciones en cualquier momento, y su uso continuado de la aplicación constituye su consentimiento a dichos cambios."  # Your EULA text here

    # Create a scrollable box and add the text within it
    st.markdown(f'<div class="scrollable-box">{texto_terminos}</div>', unsafe_allow_html=True)

    # Button to accept the EULA
    if st.button('Aceptar'):
        st.session_state[EULA_ACCEPTED_KEY] = True
        st.experimental_rerun()  # Rerun the app to update the display

def init():
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "run" not in st.session_state:
        st.session_state.run = None

    if "file_ids" not in st.session_state:
        st.session_state.file_ids = []
    
    if "thread_id" not in st.session_state:
        st.session_state.thread_id = None

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')


def main():
    #load_dotenv()
    st.set_page_config(page_title="Generar resumen del imagen", page_icon=":eye:", layout="wide")
        # Define CSS to increase text size and adjust container width
    custom_css = """
        <style>
            .big-text {
                font-size: 20px; /* Adjust text size as needed */
            }
            .wide-container {
                max-width: 95%; /* You can adjust this as needed */
            }
        </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)
    # Hide the Streamlit footer
    hide_streamlit_style = """
                <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    st.write(css, unsafe_allow_html=True)

    # Initialize conversation and chat history if not present
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    # Initialize a variable to hold the formatted message
    formatted_message = None

    with st.sidebar:

        st.image("./Deloitte_Logo.jpg", width=300)

        api_key = st.sidebar.text_input("Ingrese la clave Openai y presione Enter.", type="password")

        uploaded_image = st.file_uploader("Subir imagen (jpg, png, bmp):", type=["jpg", "jpeg", "png", "bmp"], accept_multiple_files=True)

        if st.button("Procesar"):
            if api_key:
                with st.spinner("Procesando..."):
                    if uploaded_image:
                        temp_dir = tempfile.mkdtemp()
                        encoded_images = []  # List to store encoded images
                        for image in uploaded_image:
                            image_path = os.path.join(temp_dir, image.name)
                            with open(image_path, "wb") as f:
                                f.write(image.getvalue())
                            base64_image = encode_image(image_path)
                            encoded_images.append(base64_image)
                        try:
                            headers = {
                                "Content-Type": "application/json",
                                "Authorization": f"Bearer {api_key}"
                            }
                            payload = {
                                "model": "gpt-4-vision-preview",
                                "messages": [
                                    {
                                        "role": "system",
                                        "content": "I have attached an image of a Business Process Model. Please analyze it in detail and provide a comprehensive description of each element and phase. This should include identifying the workflows, decision points, roles of executors, and the inputs and outputs of each activity. Also, create a table with columns for ID, Name Activity, Executor, Type of Activity, Short Description, Input, and Output, populated with data from the diagram. After that, offer recommendations for optimizing this process, focusing on aspects like redundant steps, potential bottlenecks, and opportunities for implementing automation technologies or management software to enhance process efficiency and effectiveness. Please respond in Spanish."
                                    },
                                    {
                                        "role":"user",
                                        "content": [
                                            {
                                                "type": "text",
                                                "text": "Perform a detailed analysis of the attached Business Process Model image. Describe each element and phase, noting the workflows, decision points, executor roles, and the inputs and outputs of each activity. Then, prepare a table with the following columns: ID, Name Activity, Executor, Type of Activity, Short Description, Input, Output, using information from the diagram. Provide recommendations for process optimization, highlighting redundant steps, bottlenecks, and opportunities for automation technologies or management software improvements.",
                                                #"text": "I've uploaded a BPM diagram and need a table created with 'ID', 'Activity Name', 'Executor', 'Type of Activity', 'Short Description', 'Input', and 'Output' columns, following these rules: use the number indicated or 'N/A' for ID, match the figure's shape to the legend for 'Type of Activity', and for decisions, note 'Dependent on previous activity, XXX' in 'Short Description', and the previous activity's ID in 'Input' and 'Output'; leave fields blank if the figure isn't recognized correctly."
                                            },
                                            {
                                                "type": "image_url",
                                                "image_url": {
                                                    "url": f"data:image/jpeg;base64,{encoded_images[0]}"
                                                }
                                            },
                                            {
                                                "type": "image_url",
                                                "image_url": {
                                                    "url": f"data:image/jpeg;base64,{encoded_images[1]}"
                                                }
                                            }
                                        ]
                                    }
                                ],
                                "max_tokens": 4096
                            }
                            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
                            if response.ok:
                                response_json = response.json()
                                messages = response_json['choices'][0]['message']['content']
                                formatted_message = bot_template.replace("{{MSG}}", messages)
                                filename = "saved_string.txt"
                                with open(filename, 'w') as file:
                                    file.write(formatted_message)
                            else:
                                st.error(f"Error: {response.status_code} - {response.text}")
                        except:
                            e = RuntimeError('Error!')
                            st.exception(e)
                            #print(f"Error: {response.status_code} - {response.text}")
                    else:
                        st.error("No subiste imagen!", icon="🚨")
            else:
                st.error("Por favor ingresar una llave valida.", icon="🚨")

    if formatted_message:
        st.markdown(response_css, unsafe_allow_html=True)
        # Use a container or just st.markdown directly to display the message on the main page
        #st.markdown('<div class="chat-container wide-container">', unsafe_allow_html=True)
        st.markdown('<div class="response-container"><table class="response-table">', unsafe_allow_html=True)
        #st.markdown(api_response_content)  # where `api_response_content` is the HTML content from the API response
        st.markdown(f'<div class="big-text">{formatted_message}</div>', unsafe_allow_html=True)
        st.markdown('</table></div>', unsafe_allow_html=True)
    else:
        pass

if __name__ == '__main__':
    EULA_ACCEPTED_KEY = 'eula_accepted'
    if EULA_ACCEPTED_KEY not in st.session_state:
        st.session_state[EULA_ACCEPTED_KEY] = False
    if st.session_state[EULA_ACCEPTED_KEY]:
        main()
    else:
        show_eula()
