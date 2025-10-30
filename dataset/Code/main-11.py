# Use streamlit to create Website for translating text by calling a HTML cognitiveservices API
# This is a sample website for the Microsoft Cognitive Services Translator API
# https://docs.microsoft.com/en-us/azure/cognitive-services/translator/quickstart-python-translate

import os
import time
import uuid
from datetime import datetime

import pyperclip
import requests
import streamlit as st
from azure.storage.blob import BlobServiceClient

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
logging.info("Starting up...")

sample_text = """A SQUAT grey building of only thirty-four stories. Over the main entrance the words, CENTRAL LONDON HATCHERY AND CONDITIONING CENTRE, and, in a shield, the World State’s motto, COMMUNITY, IDENTITY, STABILITY.

The enormous room on the ground floor faced towards the north. Cold for all the summer beyond the panes, for all the tropical heat of the room itself, a harsh thin light glared through the windows, hungrily seeking some draped lay figure, some pallid shape of academic goose-flesh, but finding only the glass and nickel and bleakly shining porcelain of a laboratory.

Wintriness responded to wintriness. The overalls of the workers were white, their hands gloved with a pale corpse-coloured rubber. The light was frozen, dead, a ghost. Only from the yellow barrels of the microscopes did it borrow a certain rich and living substance, lying along the polished tubes like butter, streak after luscious streak in long recession down the work tables.

“And this,” said the Director opening the door, “is the Fertilizing Room.”"""

storage_account_key = os.environ.get("storage_account_key")
storage_account_name = os.environ.get("storage_account_name")
input_blob_sas_token = os.environ.get("translator_blob_sas_token")
output_blob_sas_token = os.environ.get("translator_blob_sas_token")
translator_resource_key = os.environ.get("translator_resource_key")
translator_resource_name = os.environ.get("translator_resource_name")

input_container_name = "translator"
output_container_name = "translated"


def translate_text(text, from_language, to_language):
    """Translate text using the Microsoft Translator API.

    Args:
        text (str): The text to translate.
        from_language (str): The language to translate from.
        to_language (str): The language to translate to.

    Returns:
        _type_: str
    """
    endpoint = "https://api.cognitive.microsofttranslator.com"
    region = "westeurope"

    path = "/translate?api-version=3.0"

    if from_language == "auto-detect":
        params = f"&to={to_language}"
    else:
        params = f"&from={from_language}&to={to_language}"

    constructed_url = endpoint + path + params
    logging.info("constructed_url: %s", constructed_url)

    headers = {
        "Ocp-Apim-Subscription-Key": translator_resource_key,
        "Ocp-Apim-Subscription-Region": region,
        "Content-type": "application/json",
        "X-ClientTraceId": str(uuid.uuid4()),
    }

    body = [{"text": text}]
    request = requests.post(constructed_url, headers=headers, json=body)
    response = request.json()

    if request.status_code == 200:
        translation = response[0]["translations"][0]["text"]
        logging.info("Translated text: %s", translation)
        return translation
    else:
        error_message = (
            "Error: " + str(request.status_code) + " " + response["error"]["message"]
        )
        logging.error(error_message)
        return error_message


# create a function to display the website
def main():
    # change width of the website to 800px
    st.set_page_config(
        page_title="Text Translator",
        page_icon=":earth_americas:",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # add two tabs to the website, one for translation and one for document translation
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.selectbox(
        "Choose the app mode",
        ["Translate text", "Translate documents", "Translate Speech"],
    )

    # toggle the translation tab
    if app_mode == "Translate text":
        st.title("Text Translator")
        st.write(
            "This is a sample website for the Microsoft Cognitive Services Text Translator API"
        )
        st.write(
            "https://docs.microsoft.com/en-us/azure/cognitive-services/translator/quickstart-python-translate"
        )

        translation = ""

        # create two dropdowns for the input and output language side by side
        input_language, output_language = st.columns(2)

        # create a dropdown for the input language
        with input_language:
            st.header("Source Text")
            # create a dropdown for the input language

            # create a drop down menu for the user to select the language to translate from
            from_language = st.selectbox(
                "Select language to translate from",
                (
                    "auto-detect",
                    "de",
                    "en",
                    "es",
                    "it",
                    "pt",
                    "pt-pt",
                    "fr",
                    "zh-Hans",
                    "hu",
                    "ro",
                    "ru",
                    "sr-Latn",
                    "sr-Cyrl",
                ),
            )

        # create a dropdown for the output language
        with output_language:
            st.header("Target Text")
            # create a drop down menu for the user to select the language to translate to
            to_language = st.selectbox(
                "Select language to translate to",
                (
                    "de",
                    "en",
                    "es",
                    "it",
                    "pt",
                    "pt-pt",
                    "fr",
                    "zh-Hans",
                    "hu",
                    "ro",
                    "ru",
                    "sr-Latn",
                    "sr-Cyrl",
                ),
            )

        # create two text boxes for the input and output text side by side, both with a height of 300px
        input_text, output_text = st.columns(2)

        # create a text area for the input text with a height of 300px
        with input_text:
            input_text = st.text_area(
                "",
                sample_text,
                height=300,
            )
            input_text_str = input_text.strip()

        # create a text box for the output text
        with output_text:
            # st.header("Translated Text")
            output_text = st.empty()
            output_text.text_area(label="Translated text will appear here", height=300)

        translate_button, copy_button = st.columns(2)
        # create a button for the user to click to translate the text
        if translate_button.button("Translate"):
            translation = translate_text(input_text_str, from_language, to_language)
            # update the output_text box with the translation string
            output_text.text_area(
                "Translated text", translation, height=300, max_chars=None
            )

        if copy_button.button("Copy"):
            pyperclip.copy(translation)

        # add a bit space between the two tabs
        st.write("")
        st.write("")
        st.write("")
        st.write("")

        st.markdown(
            """Developed by JHC Hein [![GitHub](https://img.shields.io/badge/GitHub-black?style=flat&logo=github)](https://github.com/jhchein) [![LinkedIn](https://img.shields.io/badge/LinkedIn-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/hendrik-hein-a3921b18/), using [Github Copilot](https://github.com/features/copilot/), the [Streamlit](https://streamlit.io/) framework and the [Azure Cognitive Services Translator API](https://docs.microsoft.com/en-us/azure/cognitive-services/translator/quickstart-python-translate)"""
        )

    # toggle the document translation tab
    elif app_mode == "Translate documents":
        st.title("Document Translator")
        st.write(
            "This is a sample website for the Microsoft Cognitive Services Document Translator API"
        )
        st.write(
            "https://docs.microsoft.com/en-us/azure/cognitive-services/translator/document-translation/quickstart-python"
        )

        # create a drop box for a file upload
        # display pdf and word document in the drop box
        uploaded_file = st.file_uploader(
            "Upload a Word or PDF document", type=["pdf", "docx"]
        )
        # create a dropdowm for the output language
        output_language = st.selectbox(
            "Select language to translate to",
            (
                "de",
                "en",
                "es",
                "it",
                "pt",
                "pt-pt",
                "fr",
                "zh-Hans",
                "hu",
                "ro",
                "ru",
                "sr-Latn",
                "sr-Cyrl",
            ),
        )

        # create a azure blue button for the user to click to translate the document
        if st.button("Translate"):
            # create a function to translate the document
            def translate_document(uploaded_file):
                """Translate a document using the Microsoft Translator API.

                Args:
                    uploaded_file (_io.BytesIO): The document to translate.

                Returns:
                    _type_: str
                """
                # Create a progress bar with 3 steps
                progress_bar = st.progress(0)

                uuid_blob_name = str(uuid.uuid4()) + uploaded_file.name
                target_blob_name = f"{output_language}/{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}/{uploaded_file.name}"

                # upload the file to the blob storage
                blob_service_client = BlobServiceClient.from_connection_string(
                    f"DefaultEndpointsProtocol=https;AccountName={storage_account_name};AccountKey={storage_account_key};EndpointSuffix=core.windows.net"
                )
                container_client = blob_service_client.get_container_client(
                    input_container_name
                )
                upload_blob_client = container_client.get_blob_client(uuid_blob_name)
                upload_blob_client.upload_blob(uploaded_file, overwrite=True)

                # move progress bar to 1/6
                progress_bar.progress(1 / 6)

                source_url = f"https://{storage_account_name}.blob.core.windows.net/{input_container_name}/{uuid_blob_name}?{input_blob_sas_token}"
                target_url = f"https://{storage_account_name}.blob.core.windows.net/{output_container_name}/{target_blob_name}?{output_blob_sas_token}"

                body = {
                    "inputs": [
                        {
                            "source": {
                                "sourceUrl": source_url,
                            },
                            "targets": [
                                {
                                    "language": output_language,
                                    "targetURL": target_url,
                                }
                            ],
                            "storageType": "File",
                        },
                    ],
                }

                # send the request to the document translator
                response = requests.post(
                    f"https://{translator_resource_name}.cognitiveservices.azure.com/translator/text/batch/v1.0/batches",
                    headers={
                        "Ocp-Apim-Subscription-Key": translator_resource_key,
                        "Content-Type": "application/json",
                    },
                    json=body,
                )

                # move the progress bar to 20%
                progress = 0.2
                progress_bar.progress(progress)

                # abort when the request fails
                if response.status_code != 202:
                    st.write("Error: ", response.status_code, response.text)
                    return

                # get the status of the translation
                operation_location = response.headers["Operation-Location"]
                response = requests.get(
                    operation_location,
                    headers={
                        "Ocp-Apim-Subscription-Key": translator_resource_key,
                        "Content-Type": "application/json",
                    },
                )

                # wait until the translation is complete
                while response.json()["status"] in ["Running", "NotStarted"]:
                    time.sleep(2)
                    # move the progress bar 2.5% but not past 90%
                    progress = min(progress + 0.01, 0.9)
                    progress_bar.progress(progress)

                    response = requests.get(
                        operation_location,
                        headers={
                            "Ocp-Apim-Subscription-Key": translator_resource_key,
                            "Content-Type": "application/json",
                        },
                    )

                # move the progress bar to 5/6
                progress_bar.progress(0.9)

                # delete the uploaded file from the blob storage
                upload_blob_client.delete_blob()

                # if the translation is successful, download the translated file
                if response.json()["status"] == "Succeeded":
                    # create target blob client
                    target_blob_client = blob_service_client.get_blob_client(
                        container=output_container_name, blob=target_blob_name
                    )

                    st.download_button(
                        label="Download translated file",
                        data=target_blob_client.download_blob().readall(),
                        file_name=uploaded_file.name,
                        mime="application/octet-stream",
                    )

                    # move the progress bar to 6/6
                    progress_bar.progress(6 / 6)
                    # change the progress bar color to green
                    progress_bar.empty()
                    st.success("Translation complete!")

                else:
                    # print full response if the translation fails
                    st.write(response.json())
                    # print target blob url
                    st.write(
                        source_url,
                        "\n",
                        target_url,
                        "\n",
                        output_language,
                        "\n",
                        uploaded_file.name,
                    )
                    # print status code and  the error message
                    st.write(
                        "Error: ",
                        response.status_code,
                        " - ",
                        response.json()["error"]["message"],
                    )

            # call the translate_document function
            translated_documents = translate_document(uploaded_file)
            # display the translated documents
            st.write(translated_documents)

        # add four empty lines to the app
        st.markdown("<br><br><br><br>", unsafe_allow_html=True)

        st.markdown(
            """Developed by JHC Hein [![GitHub](https://img.shields.io/badge/GitHub-black?style=flat&logo=github)](https://github.com/jhchein) [![LinkedIn](https://img.shields.io/badge/LinkedIn-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/hendrik-hein-a3921b18/), using [Github Copilot](https://github.com/features/copilot/), the [Streamlit](https://streamlit.io/) framework and the [Azure Cognitive Services Translator API](https://docs.microsoft.com/en-us/azure/cognitive-services/translator/quickstart-python-translate)"""
        )

    # toggle the speech translation tab
    elif app_mode == "Translate speech":
        # add a placeholder title
        st.title("Speech Translator")


# run the website
if __name__ == "__main__":
    main()
