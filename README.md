# 🧾 GenAuth

**GenAuth** is a blockchain system engineered to verify and immutably record digital authorship and AI-generated content ownership. It stores comprehensive metadata including content hashes, agent fingerprints, cryptographic signatures, and semantic tags — establishing a tamper-proof provenance trail for digital artifacts.

Fully built with **Flask** and optimized for **Vercel deployment**, GenAuth provides a secure, serverless environment for content origin certification and identity validation.

---

## 🔐 Key Features

- ✅ Immutable authorship verification for content and agents
- 🧠 Fingerprint, signature, and purpose tagging per artifact
- 🔗 Proof-of-work blockchain engine for tamper resistance
- 🧾 Full HTML explorer and RESTful API endpoints
- 💾 Local JSON chain ledger for portable provenance

---

## 📁 File Structure

```
/
├── genauth_app.py            # Main Flask blockchain app
├── genauth_chain.json        # Local persistent chain ledger
├── requirements.txt          # Python dependency list
└── vercel.json               # Vercel deployment config
```

---

## 🌐 API Overview

| Method | Endpoint     | Description                        |
|--------|--------------|------------------------------------|
| GET    | `/`          | HTML blockchain explorer           |
| GET    | `/chain`     | Full JSON blockchain ledger        |
| GET    | `/mine`      | Mine next submitted authorship     |
| POST   | `/submit`    | Submit new digital artifact record |

### `POST /submit` Example:
```json
{
  "agent_name": "GPT-4",
  "content_hash": "9f35abc...",
  "fingerprint": "abc:123:ai",
  "purpose": "whitepaper authorship",
  "signature": "sig-encoded-string",
  "tags": ["AI", "ownership", "authorship"]
}
```

---

## 🧠 Use Cases

- ✅ AI authorship logging and verification
- ✅ Digital copyright registration
- ✅ Academic or scientific content notarization
- ✅ Chain-of-custody for digital documents
- ✅ Agent identity and fingerprint management

---

> GenAuth transforms authorship into **immutable digital identity**—bridging AI content with verifiable provenance.
