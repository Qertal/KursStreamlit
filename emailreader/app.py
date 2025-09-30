import streamlit as st
import io
import json
import csv
from datetime import datetime, date
from typing import Dict, List, Optional, Tuple

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2.credentials import Credentials as OAuthCredentials
from google.auth.transport.requests import Request as GoogleRequest
from google.oauth2 import service_account

# ---- Auth helpers ----

def get_drive_service():
    """Return an authenticated Google Drive service using OAuth (preferred) or Service Account fallback."""
    # Try OAuth refresh token first (uploads go to the user's Drive quota)
    if st.secrets.get('GDRIVE_OAUTH_REFRESH_TOKEN') and st.secrets.get('GDRIVE_OAUTH_CLIENT_ID') and st.secrets.get('GDRIVE_OAUTH_CLIENT_SECRET'):
        creds = OAuthCredentials(
            token=None,
            refresh_token=st.secrets['GDRIVE_OAUTH_REFRESH_TOKEN'],
            client_id=st.secrets['GDRIVE_OAUTH_CLIENT_ID'],
            client_secret=st.secrets['GDRIVE_OAUTH_CLIENT_SECRET'],
            token_uri='https://oauth2.googleapis.com/token',
            # Use the same scope as sender to match the issued refresh token
            scopes=['https://www.googleapis.com/auth/drive.file']
        )
        creds.refresh(GoogleRequest())
        return build('drive', 'v3', credentials=creds)

    # Fallback to service account (ensure folder/files are shared with the SA or use Shared Drive)
    sa_info = st.secrets.get('GDRIVE_SERVICE_ACCOUNT') or st.secrets.get('GDRIVE_SERVICE_ACCOUNT_JSON')
    if not sa_info:
        raise RuntimeError('Brak poświadczeń: dodaj OAuth (GDRIVE_OAUTH_*) albo konto serwisowe (GDRIVE_SERVICE_ACCOUNT).')
    if isinstance(sa_info, str):
        sa_info = json.loads(sa_info)
    creds = service_account.Credentials.from_service_account_info(
        sa_info, scopes=['https://www.googleapis.com/auth/drive.readonly']
    )
    return build('drive', 'v3', credentials=creds)

# ---- Drive queries ----

def list_training_folders(drive, shared_parent: Optional[str]) -> List[Dict]:
    """List folders (potential training folders) under optional shared drive/folder parent, newest first."""
    q = "mimeType = 'application/vnd.google-apps.folder' and trashed = false"
    if shared_parent:
        q += f" and '{shared_parent}' in parents"
    resp = drive.files().list(
        q=q,
        spaces='drive',
        fields='files(id, name, createdTime, modifiedTime)',
        orderBy='modifiedTime desc',
        includeItemsFromAllDrives=bool(shared_parent),
        supportsAllDrives=bool(shared_parent),
        pageSize=200,
    ).execute()
    return resp.get('files', [])


def list_folder_items(drive, folder_id: str, shared: bool) -> Dict[str, List[Dict]]:
    """Return dict with keys: json, csv, videos (list of file dicts)."""
    q = f"'{folder_id}' in parents and trashed = false"
    resp = drive.files().list(
        q=q,
        spaces='drive',
        fields='files(id, name, mimeType, webViewLink, webContentLink)',
        includeItemsFromAllDrives=shared,
        supportsAllDrives=shared,
        pageSize=500,
    ).execute()
    files = resp.get('files', [])
    out = {'json': [], 'csv': [], 'videos': [], 'others': []}
    for f in files:
        mt = (f.get('mimeType') or '')
        name = f.get('name', '')
        if mt == 'application/json' or name.lower().endswith('.json'):
            out['json'].append(f)
        elif mt == 'text/csv' or name.lower().endswith('.csv'):
            out['csv'].append(f)
        elif mt.startswith('video/') or name.lower().endswith(('.mp4', '.mov', '.avi', '.mkv')):
            out['videos'].append(f)
        else:
            out['others'].append(f)
    return out


def download_text(drive, file_id: str, shared: bool) -> str:
    """Download a small text file (JSON/CSV) content as string."""
    request = drive.files().get_media(fileId=file_id, supportsAllDrives=shared)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    return fh.getvalue().decode('utf-8')

# ---- UI ----

st.set_page_config(page_title='Przegląd treningów', layout='wide')
st.title('Przegląd treningów z Google Drive')

# Where to look for folders
shared_parent = st.secrets.get('GDRIVE_SHARED_DRIVE_ID') or st.secrets.get('GDRIVE_SHARED_DRIVE_FOLDER_ID')
try:
    drive = get_drive_service()
except Exception as e:
    st.error(f'Błąd autoryzacji do Google Drive: {e}')
    st.stop()

@st.cache_data(ttl=60)
def cached_folders(parent: Optional[str]):
    return list_training_folders(drive, parent)

folders = cached_folders(shared_parent)
if not folders:
    st.info('Nie znaleziono folderów. Upewnij się, że podałeś poprawny Shared Drive lub że istnieją foldery z treningami.')
    st.stop()

# Filters: by name substring and by modified date range
with st.expander('Filtry', expanded=True):
    colf1, colf2, colf3 = st.columns([2, 1, 1])
    with colf1:
        name_filter = st.text_input('Nazwa zawiera', value='').strip().lower()
    with colf2:
        date_from: date | None = st.date_input('Od daty (modyfikacji)', value=None)
    with colf3:
        date_to: date | None = st.date_input('Do daty (modyfikacji)', value=None)

def parse_rfc3339(d: str) -> datetime:
    # e.g. 2025-09-21T10:20:30.123Z
    try:
        if d.endswith('Z'):
            d = d.replace('Z', '+00:00')
        return datetime.fromisoformat(d)
    except Exception:
        return datetime.min

filtered = []
for f in folders:
    nm = f.get('name','')
    mt = f.get('modifiedTime') or f.get('createdTime') or ''
    dt = parse_rfc3339(mt).date() if mt else None
    if name_filter and name_filter not in nm.lower():
        continue
    if date_from and (not dt or dt < date_from):
        continue
    if date_to and (not dt or dt > date_to):
        continue
    filtered.append(f)

if not filtered:
    st.warning('Brak folderów po zastosowaniu filtrów.')
    st.stop()

# Select folder from filtered list
folder_options = {f"{f['name']} (zmodyfikowano: {f.get('modifiedTime','?')[:10]})": f['id'] for f in filtered}
selected_label = st.selectbox('Wybierz folder z listy:', list(folder_options.keys()))
folder_id = folder_options[selected_label]

# Open folder in Drive
folder_url = f"https://drive.google.com/drive/folders/{folder_id}"
st.markdown(f"[Otwórz folder w Google Drive]({folder_url})")

# List files inside and show table/videos
shared = bool(shared_parent)
items = list_folder_items(drive, folder_id, shared)

# Show table
table_shown = False
if items['json']:
    try:
        json_file = items['json'][0]
        content = download_text(drive, json_file['id'], shared)
        parsed = json.loads(content)
        rows = parsed.get('rows', [])
        st.subheader('Tabela z JSON (dane.json)')
        st.table(rows)
        # download and open buttons
        st.download_button('Pobierz dane.json', data=content, file_name='dane.json', mime='application/json')
        json_link = json_file.get('webViewLink') or f"https://drive.google.com/file/d/{json_file['id']}/view"
        st.markdown(f"[Otwórz dane.json w Google Drive]({json_link})")
        table_shown = True
    except Exception as e:
        st.warning(f'Nie udało się odczytać JSON: {e}')

if not table_shown and items['csv']:
    try:
        csv_file = items['csv'][0]
        content = download_text(drive, csv_file['id'], shared)
        # parse csv to list of dicts using first row as header
        reader = csv.DictReader(io.StringIO(content))
        rows = list(reader)
        st.subheader('Tabela z CSV (dane.csv)')
        st.table(rows)
        st.download_button('Pobierz dane.csv', data=content.encode('utf-8'), file_name='dane.csv', mime='text/csv')
        csv_link = csv_file.get('webViewLink') or f"https://drive.google.com/file/d/{csv_file['id']}/view"
        st.markdown(f"[Otwórz dane.csv w Google Drive]({csv_link})")
        table_shown = True
    except Exception as e:
        st.warning(f'Nie udało się odczytać CSV: {e}')

if not table_shown:
    st.info('Brak plików dane.json/dane.csv w tym folderze.')

# Show videos
if items['videos']:
    st.subheader('Wideo w folderze')
    cols = st.columns(2)
    for idx, vid in enumerate(items['videos']):
        # Prefer preview URL for embedding
        file_id = vid['id']
        preview_url = f"https://drive.google.com/file/d/{file_id}/preview"
        with cols[idx % 2]:
            st.markdown(f"<iframe src='{preview_url}' width='640' height='360' allow='autoplay' allowfullscreen></iframe>", unsafe_allow_html=True)
            st.caption(vid.get('name','wideo'))
            open_link = vid.get('webViewLink') or f"https://drive.google.com/file/d/{file_id}/view"
            st.markdown(f"[Otwórz w Google Drive]({open_link})")
else:
    st.info('Brak plików wideo w tym folderze.')
