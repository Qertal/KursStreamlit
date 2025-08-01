import streamlit as st
import joblib
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

st.set_page_config(page_title="Analizator Pipeline", layout="wide")
st.title("Analizator wytrenowanego Pipeline'a")
st.markdown("""
W razie jakiś uwag, błędów, sugestii, proszę o kontakt na:\n
- email: qertal123@gmail.com
- [GitHub](https://github.com/qertal)
- [LinkedIn](https://www.linkedin.com/in/paweldrzyzga/)
            """)
st.caption("Wgraj plik `.pkl` z obiektem Pipeline (scikit-learn), a zobaczysz wszystkie jego komponenty, kolumny i hiperparametry.")

def wyswietl_pipeline(model: Pipeline):
    """
    Wyświetla poszczególne kroki pipeline'a:
    - rozbija ColumnTransformery i pokazuje, co robią na których kolumnach,
    - pokazuje parametry każdego transformatora i modelu końcowego.

    wersja póki co mocno testowa, nie jest jeszcze w pełni funkcjonalna
    """
    for i, (name, step) in enumerate(model.named_steps.items()):
        with st.expander(f"Etap {i + 1}: `{name}` ({type(step).__name__})", expanded=False):

            if isinstance(step, ColumnTransformer):
                st.markdown(f"**ColumnTransformer** z `{len(step.transformers)}` elementami:")

                for trans_name, trans, cols in step.transformers:
                    st.markdown(f"---\n### Typ: `{trans_name}`")
                    st.markdown(f"- **Kolumny:** `{list(cols)}`")

                    if isinstance(trans, Pipeline):
                        st.markdown(f"**Kroki pipeline'a:**")
                        for step_name, transformer in trans.steps:
                            st.markdown(f"**{step_name}**: `{transformer.__class__.__name__}`")
                            st.markdown("**Parametry:**")
                            param_text = "\n".join(
                                [f"{param}: {val}" for param, val in transformer.get_params().items()]
                            )
                            st.code(param_text, language="text")
                    else:
                        st.markdown(f"**Transformator:** `{trans.__class__.__name__}`")
                        param_text = "\n".join(
                            [f"{param}: {val}" for param, val in trans.get_params().items()]
                        )
                        st.code(param_text, language="text")

            else:
                st.markdown("**Model / komponent końcowy**")
                st.markdown("**Hiperparametry:**")
                param_text = "\n".join(
                    [f"{param}: {val}" for param, val in step.get_params().items()]
                )
                st.code(param_text, language="text")



uploaded_file = st.file_uploader("Wgraj wytrenowany model pipeline (`.pkl`)", type=["pkl"])

if uploaded_file is not None:
    try:
        model = joblib.load(uploaded_file)
        st.success("Model wczytany poprawnie!")
        
        if isinstance(model, Pipeline):
            wyswietl_pipeline(model)
        else:
            st.warning("Wgrany obiekt nie jest instancją `Pipeline`.")
    except Exception as e:
        st.error("Wystąpił błąd przy ładowaniu modelu.")
        st.exception(e)
else:
    st.info("Wgraj plik `.pkl` z obiektem typu `Pipeline`, np. zapisany przez `joblib.dump(...)`.")
