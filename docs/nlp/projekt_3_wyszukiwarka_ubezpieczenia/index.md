# Insurance Question Search

A small Streamlit app that searches two public materials from the Polish Financial Ombudsman about home insurance and storm damage. It uses TF-IDF to show the most relevant source excerpts, with page references for the PDF guide.

The app does not generate answers or provide individual insurance or legal advice.

## Live app

[Open the app on Streamlit](https://gmarkowski-nlpwyszukiwarkaodpowiedzi.streamlit.app/).

## Run locally

From this folder, install the dependencies and start Streamlit:

    python -m pip install -r requirements.txt
    streamlit run app.py

The two source files must remain in this folder next to `app.py`.
