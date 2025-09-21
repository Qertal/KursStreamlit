from google_auth_oauthlib.flow import InstalledAppFlow

flow = InstalledAppFlow.from_client_secrets_file(
    "pytorch/client_secret.json",
    scopes=["https://www.googleapis.com/auth/drive.file"]
)
creds = flow.run_local_server(
    port=8080,
    access_type="offline",
    prompt="consent"
)
print("REFRESH_TOKEN:", creds.refresh_token)