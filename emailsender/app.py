import streamlit as st
import smtplib, ssl
from email.message import EmailMessage
import urllib.parse

# st.write("DB username:", st.secrets["DB_USERNAME"])
# st.write("DB password:", st.secrets["DB_PASSWORD"])

# Nazwa Cwiczenia, Ciężar, Liczba Serii, Liczba powtórzeń (jeśli ćwiczenia wykonywane na czas, dopisz 's' na koniec), Tempo, RPE, Uwagi

st.title("Formularz treningowy Niedojdy Bojdy")

st.set_page_config(layout='wide')

# Always show the number input and update session state
st.session_state.liczba_cwiczen = st.number_input(
    'Podaj liczbę ćwiczeń', min_value=1, step=1, value = 1, key='liczba', width=200
)

if 'cwiczenia' not in st.session_state:
    st.session_state.cwiczenia = {}

if 'liczba_cwiczen' in st.session_state:
    with st.form(key="Formularz"):
        st.markdown('## Informacje do tytułu maila:')
        col1, col2, col3, col4 = st.columns(4)
        cwiczenia_input = []
        with col1:
            imie = st.text_input('Imie', key = 'imie')
        with col2:
            nazwisko = st.text_input('Nazwisko', key = 'nazwisko')
        with col3:
            data = st.date_input('Data treningu', key = 'data')
        with col4:
            nr_tren = st.number_input('Numer treningu w tygodniu', min_value= 1, step = 1, key = 'numer')
        title = (
            f'[{imie if imie else "Nie podano"} {nazwisko if nazwisko else "Nie podano"} '
            f'| {data if data else "Nie podano"} | {nr_tren if nr_tren else "Nie podano"}]'
        )
        for i in range(st.session_state.liczba_cwiczen):
            st.markdown(f"### Ćwiczenie {i+1}")
            col1, col2, col3 = st.columns(3)
            with col1:
                nazwa = st.text_input(f"Wpisz nazwę ćwiczenia", key=f"nazwa_{i}")
            with col2:
                ciezar = st.number_input("Ciężar", min_value=0.0, step=0.01, value=0.0, key=f"ciezar_{i}")
            with col3:
                serie = st.number_input("Liczba serii", min_value=0, step=1, value=0, key=f"serie_{i}")
            with col1:
                powtorzenia = st.text_input('Liczba powtórzeń', key = f'powtorzenia_{i}',     
                                        placeholder='Dopisz "s" jeśli na czas')
            with col2:
                tempo = st.text_input('Tempo', key=f'tempo_{i}', placeholder='Brak - zostaw puste')
            with col3:
                rpe = st.text_input('RPE', key=f'rpe_{i}', placeholder='Brak - zostaw puste')
            uwagi = st.text_input('Uwagi', key = f'Uwagi_{i}', placeholder='Brak - zostaw puste')
            cwiczenia_input.append({
                'cwiczenie': nazwa if nazwa else '---',
                'ciezar': ciezar if ciezar else '---',
                'serie': serie if serie else '---',
                'powtorzenia': powtorzenia if powtorzenia else '---',
                'tempo': tempo if tempo else '---',
                'rpe': rpe if rpe else '---',
                'uwagi': uwagi if uwagi else '---'
            })

        submitted = st.form_submit_button(label='Wyślij')
        
        st.write('Jeśli chcesz wyczyścic formularz, to odśwież strone')

        if submitted:
            for i, j in enumerate(cwiczenia_input, 1):
                st.session_state.cwiczenia[f'Cwiczenie {i}'] = j
            st.write(st.session_state.cwiczenia)
            st.success("Dane zostały zapisane!")
            

            
            def build_plain_text_table(meta_title, exercises):
                headers = ["Ćwiczenie", "Ciężar", "Serie", "Powtórzenia", "Tempo", "RPE", "Uwagi"]
                rows = []
                for ex in exercises:
                    rows.append([
                        str(ex.get('cwiczenie', '---')),
                        str(ex.get('ciezar', '---')),
                        str(ex.get('serie', '---')),
                        str(ex.get('powtorzenia', '---')),
                        str(ex.get('tempo', '---')),
                        str(ex.get('rpe', '---')),
                        str(ex.get('uwagi', '---')),
                    ])

                
                sample_rows = rows if rows else [["---"] * len(headers)]
                col_widths = [max(len(str(cell)) for cell in col) for col in zip(headers, *sample_rows)]

                sep = ' | '
                def line(cells):
                    return sep.join(cell.ljust(w) for cell, w in zip(cells, col_widths))

                parts = [meta_title, '']
                parts.append(line(headers))
                parts.append('-' * (sum(col_widths) + len(sep) * (len(headers) - 1)))
                for r in rows:
                    parts.append(line(r))
                parts.append('')
                parts.append('Wysłane z aplikacji Streamlit')
                return '\n'.join(parts)

            # Build an HTML table centered on the page for a nicer visual
            def build_centered_html_table(meta_title, exercises):
                headers = ["Ćwiczenie", "Ciężar", "Serie", "Powtórzenia", "Tempo", "RPE", "Uwagi"]
                html = [f"<div style='display:flex;justify-content:center;'>",
                        "<table style='border-collapse:collapse;width:80%;'>",
                        f"<caption style='caption-side:top; text-align:left; font-weight:bold; margin-bottom:8px;'>{meta_title}</caption>",
                        "<thead>",
                        "<tr>"]
                for h in headers:
                    html.append(f"<th style='border:1px solid #ddd;padding:8px;background:#f7f7f7;text-align:left'>{h}</th>")
                html.append("</tr>")
                html.append("</thead>")
                html.append("<tbody>")
                if not exercises:
                    html.append("<tr>" + "".join(["<td style='border:1px solid #ddd;padding:8px'>---</td>" for _ in headers]) + "</tr>")
                else:
                    for ex in exercises:
                        html.append("<tr>")
                        html.append(f"<td style='border:1px solid #ddd;padding:8px'>{ex.get('cwiczenie','---')}</td>")
                        html.append(f"<td style='border:1px solid #ddd;padding:8px'>{ex.get('ciezar','---')}</td>")
                        html.append(f"<td style='border:1px solid #ddd;padding:8px'>{ex.get('serie','---')}</td>")
                        html.append(f"<td style='border:1px solid #ddd;padding:8px'>{ex.get('powtorzenia','---')}</td>")
                        html.append(f"<td style='border:1px solid #ddd;padding:8px'>{ex.get('tempo','---')}</td>")
                        html.append(f"<td style='border:1px solid #ddd;padding:8px'>{ex.get('rpe','---')}</td>")
                        html.append(f"<td style='border:1px solid #ddd;padding:8px'>{ex.get('uwagi','---')}</td>")
                        html.append("</tr>")
                html.append("</tbody>")
                html.append("</table>")
                html.append("</div>")
                return '\n'.join(html)

            subject = title
            email_body = build_plain_text_table(subject, cwiczenia_input)
            html_table = build_centered_html_table(subject, cwiczenia_input)

            # Show the generated HTML table (safe) and a monospace ASCII version
            st.markdown("**Podgląd tabeli (HTML, wyrównana):**", unsafe_allow_html=False)
            st.markdown(html_table, unsafe_allow_html=True)

            st.markdown("**Tekst do wysłania (monospace, wyrównana tabela ASCII):**")
            st.code(email_body, language='')

            # # Download button for .txt
            # st.download_button(label='Pobierz jako .txt', data=email_body, file_name='trening.txt', mime='text/plain')

            #Mailto link (URL-encoded body). Note: long bodies may be truncated by mail clients.
            # import urllib.parse
            # mailto = f"mailto:?subject={urllib.parse.quote(subject)}&body={urllib.parse.quote(email_body)}"
            # st.markdown(f"[Otwórz klienta pocztowego]({mailto})")

            SMTP_HOST = st.secrets["SMTP_HOST"]   # dla innych dostawców: ich host
            SMTP_PORT = st.secrets["SMTP_PORT"]                # 465 = SSL, 587 = STARTTLS
            USERNAME = st.secrets["USERNAME"]
            PASSWORD = st.secrets["PASSWORD"]
            DESTINATION = st.secrets["DESTINATION"]

            # Build multipart email: plain-text fallback + HTML table
            msg = EmailMessage()
            msg["From"] = USERNAME
            msg["To"] = DESTINATION
            msg["Subject"] = title
            # plain text fallback (do not URL-encode)
            msg.set_content(email_body)
            # add HTML alternative containing the centered table
            msg.add_alternative(html_table, subtype="html")

            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=context) as server:
                server.login(USERNAME, PASSWORD)
                server.send_message(msg)

