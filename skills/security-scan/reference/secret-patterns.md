# Secret Detection Patterns

Comprehensive list of secret types detected by Gitleaks with regex patterns and examples.

## Cloud Providers

### AWS

**AWS Access Key ID**
```regex
(A3T[A-Z0-9]|AKIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{16}
```
Examples:
- `AKIAIOSFODNN7EXAMPLE`
- `ASIATESTACCESSKEY123`
- Entropy: 3.0

**AWS Secret Access Key**
```regex
[A-Za-z0-9/+=]{40}
```
Examples:
- `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY`
- Context required: near "aws", "secret", "key"
- Entropy: 3.0

**AWS Session Token**
- 228 characters
- Base64 encoded
- Context: "aws", "session", "token"

### Azure

**Azure Storage Account Key**
```regex
[A-Za-z0-9/+=]{88}
```
- Entropy: 3.0
- Context: "azure", "storage"

**Azure Connection String**
```regex
DefaultEndpointsProtocol=https;AccountName=[^;]+;AccountKey=[A-Za-z0-9/+=]{88};
```

### Google Cloud

**GCP API Key**
```regex
AIza[0-9A-Za-z_-]{35}
```

**GCP Service Account**
```json
{
  "type": "service_account",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...",
  "client_email": "..."
}
```

## API Keys

### OpenAI

**OpenAI API Key (Legacy)**
```regex
sk-[A-Za-z0-9]{48}
```
Example: `sk-abc123def456ghi789jkl012mno345pqr678stu901`

**OpenAI API Key (Project)**
```regex
sk-proj-[A-Za-z0-9_-]{20,74}T3BlbkFJ[A-Za-z0-9_-]{20,74}
```
- Contains `T3BlbkFJ` (Base64 for "OpenAI")
- Example: `sk-proj-abc123...T3BlbkFJ...xyz789`

**OpenAI API Key (Service Account)**
```regex
sk-svcacct-[A-Za-z0-9_-]{20,74}T3BlbkFJ[A-Za-z0-9_-]{20,74}
```

**OpenAI API Key (Admin)**
```regex
sk-admin-[A-Za-z0-9_-]{20,74}T3BlbkFJ[A-Za-z0-9_-]{20,74}
```

### GitHub

**Personal Access Token (Classic)**
```regex
ghp_[0-9a-zA-Z]{36}
```

**OAuth Access Token**
```regex
gho_[0-9a-zA-Z]{36}
```

**User-to-Server Token**
```regex
ghu_[0-9a-zA-Z]{36}
```

**Server-to-Server Token**
```regex
ghs_[0-9a-zA-Z]{36}
```

**Refresh Token**
```regex
ghr_[0-9a-zA-Z]{76}
```

**Fine-Grained Personal Access Token**
```regex
github_pat_[0-9a-zA-Z_]{82}
```

### Stripe

**Secret Key**
```regex
sk_(test|live)_[0-9a-zA-Z]{24}
```
Examples:
- `sk_test_EXAMPLE_DO_NOT_USE_1234567`
- `sk_live_EXAMPLE_DO_NOT_USE_123456`

**Restricted Key**
```regex
rk_live_[0-9a-zA-Z]{24}
```

**Publishable Key** (not secret, but detected)
```regex
pk_(test|live)_[0-9a-zA-Z]{24}
```

### Slack

**Bot Token**
```regex
xoxb-[0-9]{11}-[0-9]{11}-[0-9a-zA-Z]{24}
```

**User Token**
```regex
xoxp-[0-9]{11}-[0-9]{11}-[0-9a-zA-Z]{24}
```

**Webhook URL**
```regex
https://hooks\.slack\.com/services/T[A-Z0-9]+/B[A-Z0-9]+/[A-Za-z0-9]+
```

### Twilio

**Account SID**
```regex
AC[a-z0-9]{32}
```

**Auth Token**
```regex
SK[a-z0-9]{32}
```

### SendGrid

**API Key**
```regex
SG\.[A-Za-z0-9_-]{22}\.[A-Za-z0-9_-]{43}
```

### Mailgun

**API Key**
```regex
key-[a-z0-9]{32}
```

### Heroku

**API Key**
```regex
[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}
```
Context: "heroku", "api_key"

## Database Connection Strings

### PostgreSQL

```regex
postgres://[^:]+:[^@]+@[^/]+/[^\s]+
postgresql://[^:]+:[^@]+@[^/]+/[^\s]+
```
Example: `postgresql://user:password@localhost:5432/dbname`

### MongoDB

```regex
mongodb://[^:]+:[^@]+@[^/]+/[^\s]+
mongodb\+srv://[^:]+:[^@]+@[^/]+/[^\s]+
```
Example: `mongodb://admin:secret@mongo.example.com/db`

### MySQL

```regex
mysql://[^:]+:[^@]+@[^/]+/[^\s]+
```

### Redis

```regex
redis://[^:]*:[^@]+@[^/]+
```

### Generic JDBC

```regex
jdbc:[a-z]+://[^:]+:[^@]+@[^/]+
```

## Authentication Tokens

### JWT (JSON Web Token)

```regex
ey[A-Za-z0-9_-]{10,}\.ey[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}
```
Example: `eyJhbGci...eyJzdWIi...SflKxwRJ`
- Three base64 sections separated by dots
- Entropy: 3.0

### OAuth Bearer Tokens

```regex
[Bb]earer [A-Za-z0-9_\-\.=]+
```
Context: HTTP headers, "Authorization"

### API Tokens (Generic)

```regex
[Aa]pi[_-]?[Kk]ey[_-]?[:=]\s*['"]?([A-Za-z0-9_-]{32,})['"]?
```

```regex
[Aa]ccess[_-]?[Tt]oken[_-]?[:=]\s*['"]?([A-Za-z0-9_-]{32,})['"]?
```

## Private Keys

### RSA Private Key

```regex
-----BEGIN RSA PRIVATE KEY-----[\s\S]+?-----END RSA PRIVATE KEY-----
```

### EC Private Key

```regex
-----BEGIN EC PRIVATE KEY-----[\s\S]+?-----END EC PRIVATE KEY-----
```

### OpenSSH Private Key

```regex
-----BEGIN OPENSSH PRIVATE KEY-----[\s\S]+?-----END OPENSSH PRIVATE KEY-----
```

### PGP Private Key

```regex
-----BEGIN PGP PRIVATE KEY BLOCK-----[\s\S]+?-----END PGP PRIVATE KEY BLOCK-----
```

### DSA Private Key

```regex
-----BEGIN DSA PRIVATE KEY-----[\s\S]+?-----END DSA PRIVATE KEY-----
```

## Certificates

### Certificate

```regex
-----BEGIN CERTIFICATE-----[\s\S]+?-----END CERTIFICATE-----
```

### Encrypted Private Key

```regex
-----BEGIN ENCRYPTED PRIVATE KEY-----[\s\S]+?-----END ENCRYPTED PRIVATE KEY-----
```

## Generic Patterns

### High-Entropy Strings

**Base64 (40+ chars)**
```regex
[A-Za-z0-9+/]{40,}={0,2}
```
- Entropy threshold: 4.5+
- Context: near "password", "secret", "key", "token"

**Hex (32+ chars)**
```regex
[0-9a-fA-F]{32,}
```
- Entropy threshold: 3.5+
- Context: near "password", "secret", "key"

### API Key Patterns

```regex
[Aa]pi[_-]?[Kk]ey.*['"][0-9a-zA-Z]{32,45}['"]
```

### Secret Patterns

```regex
[Ss]ecret.*['"][0-9a-zA-Z]{32,45}['"]
```

### Password Patterns

```regex
[Pp]assword.*['"][^\s'\"]{8,}['"]
```

## Entropy Detection

Gitleaks uses Shannon entropy to detect high-randomness strings:

**Formula:**
```
H(X) = -Σ P(x) log₂ P(x)
```

**Thresholds:**
- Low entropy (< 3.0): Common words, patterns
- Medium entropy (3.0-4.0): Typical keys
- High entropy (4.0+): Strong random strings

**Examples:**
- `password123` - Entropy: 2.5 (low)
- `sk-proj-abc...` - Entropy: 4.2 (high)
- `AKIAIOSFODNN7` - Entropy: 3.5 (medium)

## Custom Patterns

### Example: Internal Service Token

```toml
[[rules]]
id = "internal-service-token"
description = "Internal Service Authentication Token"
regex = '''int_tok_[A-Za-z0-9]{32}'''
tags = ["internal", "auth"]
entropy = 3.5
```

### Example: Custom API Key Format

```toml
[[rules]]
id = "custom-api-key"
description = "Custom API Key (company-specific)"
regex = '''mycompany_api_[A-Z0-9]{20}_[a-z0-9]{12}'''
tags = ["api", "custom"]
```

### Example: Environment Variable Assignment

```toml
[[rules]]
id = "env-var-secret"
description = "Secret in environment variable"
regex = '''(API_KEY|SECRET|PASSWORD|TOKEN)=([A-Za-z0-9+/]{32,})'''
tags = ["env", "config"]
```

## Safe Patterns (Examples)

These should NOT trigger (use in docs, tests):

```python
# Safe examples (marked as examples)
API_KEY = "sk-YOUR-KEY-HERE"
AWS_ACCESS_KEY = "AKIA...EXAMPLE"
token = "test-key-not-real-12345678"
password = "SAMPLE-PASSWORD-DO-NOT-USE"
```

**Keywords that indicate safe content:**
- `EXAMPLE`
- `SAMPLE`
- `YOUR-KEY-HERE`
- `REPLACE-WITH`
- `test-key-not-real`
- `fake`
- `demo`
- `placeholder`

## Detecting Project-Specific Secrets

### MCP Server Tokens

```toml
[[rules]]
id = "mcp-server-token"
description = "MCP Server Authentication Token"
regex = '''mcp[_-]token[_-]?[:=]\s*['"]?([A-Za-z0-9_-]{32,})['"]?'''
tags = ["mcp", "server"]
```

### Internal Auth Systems

```toml
[[rules]]
id = "internal-auth"
description = "Internal Authentication Header"
regex = '''X-Internal-Auth:\s*([A-Za-z0-9+/]{32,})'''
tags = ["internal", "header"]
```

## References

- Gitleaks Rules: https://github.com/gitleaks/gitleaks/blob/master/config/gitleaks.toml
- AWS Key Formats: https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_identifiers.html
- GitHub Token Formats: https://github.blog/2021-04-05-behind-githubs-new-authentication-token-formats/
- OpenAI Key Format: https://platform.openai.com/docs/api-reference/authentication
- Stripe Key Format: https://stripe.com/docs/keys
