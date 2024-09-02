import streamlit as st
import speech_recognition as sr
import io


recognizer = sr.Recognizer()

def transcribe_speech(api_choice="Google", language="fr-FR"):
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        st.info("Ajustement du bruit ambiant... Patientez...")
        recognizer.adjust_for_ambient_noise(source)
        st.info("Vous pouvez commencer à parler...")
        audio = recognizer.listen(source)
    
    try:
        transcription = sr.Recognizer.recognize(audio)
    except:
        st.error("Sorry I can't get you")



def main():
    st.title("Application de Reconnaissance Vocale")

    api_choice = st.selectbox("Sélectionnez l'API de reconnaissance vocale", ["Google", "Sphinx"])
    language = st.text_input("Sélectionnez la langue (par exemple, 'fr-FR' pour le français, 'en-US' pour l'anglais)", "fr-FR")
    
    if st.button("Commencer la reconnaissance vocale"):
        transcription = transcribe_speech(api_choice, language)
        st.text_area("Transcription", transcription)

        if st.checkbox("Télécharger la transcription dans un fichier"):
            filename = st.text_input("Entrez le nom du fichier (par défaut : 'transcription.txt')", "transcription.txt")
            if filename:
                # Création d'un fichier virtuel avec io.StringIO
                file = io.StringIO()
                file.write(transcription)
                # Réinitialise le curseur au début du fichier
                file.seek(0)  
                # Utilisation de st.download_button pour permettre le téléchargement
                st.download_button(
                    label="Télécharger la transcription",
                    data=file,
                    file_name=filename,
                    mime="text/plain"
                )

    if st.button("Mettre en pause"):
        st.warning("Application en pause... Appuyez sur 'Reprendre' pour continuer.")
        st.button("Reprendre", on_click=main)

if __name__ == "__main__":
    main()
