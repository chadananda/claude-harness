# Google API Access for Claude Assistant

## GCP Project
- **Project:** Claude Assistant
- **Project ID:** `claude-assistant-514452`
- **Console:** https://console.cloud.google.com/apis/dashboard?project=claude-assistant-514452

## Enabled APIs
- Google Sheets API
- Google Drive API (readonly)
- Gmail API (read, compose, send)
- Google Docs API

## Credentials
- **OAuth credentials:** `~/.claude/google-oauth-credentials.json`
- **OAuth token:** `~/.claude/google-oauth-token.json`
- **Test user:** `chadananda@gmail.com`
- **App status:** Testing (not published)

## Scopes
```
https://www.googleapis.com/auth/spreadsheets
https://www.googleapis.com/auth/drive.readonly
https://www.googleapis.com/auth/gmail.modify
https://www.googleapis.com/auth/gmail.compose
https://www.googleapis.com/auth/documents
```

## Usage from any project

### Option 1: Install googleapis and use the helper
```bash
npm install googleapis
```

```javascript
import { google } from 'googleapis';
import { readFileSync, writeFileSync, existsSync } from 'fs';
import { homedir } from 'os';
import { join } from 'path';

const CREDS_PATH = join(homedir(), '.claude', 'google-oauth-credentials.json');
const TOKEN_PATH = join(homedir(), '.claude', 'google-oauth-token.json');

function getAuth() {
  const creds = JSON.parse(readFileSync(CREDS_PATH, 'utf-8'));
  const { client_id, client_secret } = creds.installed || creds.web || {};
  const oauth2Client = new google.auth.OAuth2(client_id, client_secret, 'http://localhost:3333');
  const token = JSON.parse(readFileSync(TOKEN_PATH, 'utf-8'));
  oauth2Client.setCredentials(token);
  return oauth2Client;
}

// Sheets
const sheets = google.sheets({ version: 'v4', auth: getAuth() });
await sheets.spreadsheets.values.get({ spreadsheetId: 'SHEET_ID', range: 'A1:Z' });

// Gmail - search
const gmail = google.gmail({ version: 'v1', auth: getAuth() });
await gmail.users.messages.list({ userId: 'me', q: 'search query' });

// Gmail - read message
await gmail.users.messages.get({ userId: 'me', id: 'MESSAGE_ID' });

// Gmail - create draft
await gmail.users.drafts.create({ userId: 'me', requestBody: { message: { raw: base64EncodedEmail } } });

// Docs
const docs = google.docs({ version: 'v1', auth: getAuth() });
await docs.documents.get({ documentId: 'DOC_ID' });
```

### Option 2: Quick curl with token
```bash
TOKEN=$(node -e "const t=JSON.parse(require('fs').readFileSync(require('os').homedir()+'/.claude/google-oauth-token.json','utf-8'));console.log(t.access_token)")
curl -H "Authorization: Bearer $TOKEN" "https://sheets.googleapis.com/v4/spreadsheets/SHEET_ID/values/Sheet1!A1:Z"
```

## Re-authorization
If the token expires or scopes change, delete the token and re-auth:
```bash
rm ~/.claude/google-oauth-token.json
cd /path/to/any/project/with/googleapis && node -e "import('./scripts/auth-sheets.js')"
```

## Adding new scopes
1. Add scope to the SCOPES array in the auth script
2. Delete `~/.claude/google-oauth-token.json`
3. Re-run auth to get a new token with the expanded scopes
