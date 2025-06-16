import os
import base64  # <-- 1. Zaimportuj bibliotekę base64
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail, 
    Attachment,      # <-- 1. Zaimportuj potrzebne klasy
    FileContent, 
    FileName, 
    FileType, 
    Disposition
)

load_dotenv("sendgrid.env")

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")

# Tworzenie podstawowej wiadomości (tak jak wcześniej)
message = Mail(
    from_email='Stary <qertal123@gmail.com>', # Zalecane jest dodanie adresu w formacie "Nazwa <email>"
    to_emails='qertal.leagueoflegends@interia.pl',
    subject='Jakis tam temacik z załącznikiem',
    html_content='<p> To jest jeszcze do dopracowania, ale teraz ma załącznik. </p>')

# --- DODAWANIE ZAŁĄCZNIKA ---

# 2. Wczytaj plik w trybie binarnym
file_path = './Dokumentacja.pdf'  # <-- ZMIEŃ NA WŁAŚCIWĄ ŚCIEŻKĘ
with open(file_path, 'rb') as f:
    data = f.read()
    f.close()

# 3. Zakoduj zawartość pliku do Base64
encoded_file = base64.b64encode(data).decode()

# 4. Stwórz obiekt załącznika
attachedFile = Attachment(
    FileContent(encoded_file),
    FileName('Dokumentacyjka.pdf'), # Nazwa, pod jaką odbiorca zobaczy plik
    FileType('application/pdf'),
    Disposition('attachment')
)

# 5. Dodaj załącznik do wiadomości
message.attachment = attachedFile

# --- KONIEC DODAWANIA ZAŁĄCZNIKA ---


try:
    sg = SendGridAPIClient(SENDGRID_API_KEY)
    response = sg.send(message)
    print("Wiadomość została wysłana!")
    print(f"Status: {response.status_code}")
    # print(response.body)
    # print(response.headers)
except Exception as e:
    print(f"Wystąpił błąd: {e}")

###########################################################################
# # ... (tworzysz pierwszy załącznik `attachedFile1`) ...
# # ... (tworzysz drugi załącznik `attachedFile2`) ...

# # Dodaj listę załączników do wiadomości
# message.attachment = [attachedFile1, attachedFile2]

# # Przygotowanie obrazka inline
# with open('sciezka/do/obrazka.png', 'rb') as f:
#     data = f.read()
#     f.close()
# encoded_image = base64.b64encode(data).decode()

# image_attachment = Attachment(
#     FileContent(encoded_image),
#     FileName('logo.png'),
#     FileType('image/png'),
#     Disposition('inline'),
#     ContentId('moje_logo_id')  # <-- Unikalny identyfikator
# )

# # Zmodyfikuj HTML, aby odwołać się do ContentId
# message.html_content = '<p>Oto nasze logo:</p><img src="cid:moje_logo_id">'

# # Dodaj załącznik
# message.attachment = image_attachment