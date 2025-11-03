# Email Configuration - Quick Start

## Setup in 3 Steps

### 1. Copy the Config File
```bash
cp Website/code/email-config.example.js Website/code/email-config.js
```

### 2. Get EmailJS Credentials

Go to https://www.emailjs.com/ and:
1. Sign up (free)
2. Connect your Gmail
3. Create email template
4. Copy your credentials

### 3. Update email-config.js

Edit `Website/code/email-config.js` with your credentials:
```javascript
const EMAIL_CONFIG = {
    publicKey: 'YOUR_PUBLIC_KEY',
    serviceId: 'YOUR_SERVICE_ID',
    templateId: 'YOUR_TEMPLATE_ID'
};
```

## Why This File?

**Q: Why not store in `.env`?**

**A:** Because `.env` files are for server-side code. Since your website is pure client-side JavaScript (no backend), the browser **cannot read `.env` files**.

**Q: Is it safe to have credentials in JavaScript?**

**A:** Yes! EmailJS Public Key is designed to be public. It has:
- Rate limiting
- Domain restrictions
- Abuse protection

**Q: Will my credentials be committed to git?**

**A:** No! `email-config.js` is in `.gitignore`. Only `email-config.example.js` (with placeholder values) is committed.

## Files

- ✅ `email-config.example.js` - Template (committed to git)
- ❌ `email-config.js` - Your real credentials (NOT committed, in .gitignore)

## Usage

Once configured, just include in HTML:
```html
<script src="code/email-config.js"></script>
<script src="code/email-service.js"></script>
```

Then send emails:
```javascript
await sendEmail('recipient@example.com', 'Subject', 'Message');
```

---

For more info, see [EMAIL-CONFIG-INFO.md](../EMAIL-CONFIG-INFO.md)
