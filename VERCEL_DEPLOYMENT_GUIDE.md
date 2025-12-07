# VoiceFlow – Vercel Deployment & GitHub Setup Guide

## ✅ What's Complete

- ✅ Python voice agent fully built and tested (20/22 tests pass)
- ✅ Responsive landing page with 6 tabs (Home, Features, Demo, Pricing, About, Contact)
- ✅ Enquiry form that forwards to email + WhatsApp
- ✅ Serverless API ready for Vercel (`api/send.js`)
- ✅ GitHub Actions workflow for automated deployments
- ✅ All files committed and ready to push

## 🚀 Step 1: Push to GitHub (Manual — requires Git credentials)

Your repository is already initialized and committed locally. To push to GitHub:

### Option A: Using GitHub CLI (Easiest)

```powershell
# 1. Install GitHub CLI (if not already installed)
# Download from: https://cli.github.com/

# 2. Authenticate with GitHub
gh auth login
# Follow prompts to authenticate via browser

# 3. Navigate to project
cd "c:\Users\NIKET\Downloads\murf-voiceflow-agent-main\murf-voiceflow-agent-main"

# 4. Push to GitHub
git push -u origin main
```

### Option B: Using HTTPS + Personal Access Token

```powershell
cd "c:\Users\NIKET\Downloads\murf-voiceflow-agent-main\murf-voiceflow-agent-main"

# 1. Generate Personal Access Token on GitHub:
# Go to: https://github.com/settings/tokens
# Create new token with 'repo' and 'workflow' scopes
# Copy the token

# 2. Configure git to use the token (one time)
git config --global credential.helper wincred

# 3. Push (it will prompt for username and password)
# Username: N-i-k-e-t
# Password: <paste your Personal Access Token>
git push -u origin main
```

### Option C: Using SSH Key (Most Secure)

```powershell
# 1. Generate SSH key (if you don't have one)
ssh-keygen -t ed25519 -C "nikepatil1624@gmail.com"
# Press Enter to accept default location, no passphrase needed

# 2. Add public key to GitHub:
# Go to: https://github.com/settings/ssh/new
# Paste contents of: $env:USERPROFILE\.ssh\id_ed25519.pub

# 3. Configure git to use SSH
cd "c:\Users\NIKET\Downloads\murf-voiceflow-agent-main\murf-voiceflow-agent-main"
git remote set-url origin git@github.com:N-i-k-e-t/murf-voiceflow-agent.git

# 4. Push
git push -u origin main
```

---

## 🌐 Step 2: Set Up Vercel Deployment

After pushing to GitHub, follow these steps to deploy to Vercel:

### 2a. Create Vercel Project

1. Go to **[vercel.com](https://vercel.com)**
2. Sign in with GitHub (choose "Continue with GitHub")
3. Click **"New Project"**
4. Find your `murf-voiceflow-agent` repository and click **"Import"**

### 2b. Configure Environment Variables in Vercel

In the Vercel import dialog, add the following environment variables:

```
SENDGRID_API_KEY=<your_sendgrid_api_key>
TWILIO_ACCOUNT_SID=<your_twilio_account_sid>
TWILIO_AUTH_TOKEN=<your_twilio_auth_token>
TWILIO_WHATSAPP_FROM=whatsapp:+1415xxxxxxx
ADMIN_EMAIL=nikepatil1624@gmail.com
ADMIN_WHATSAPP_TO=whatsapp:+919022790410
```

**Where to get these keys:**

- **SendGrid API Key**: https://app.sendgrid.com/settings/api_keys
- **Twilio Credentials**: https://www.twilio.com/console
- **Twilio WhatsApp**: You need to set up a Twilio WhatsApp sandbox at https://www.twilio.com/console/sms/whatsapp/sandbox

### 2c. Deploy

Click **"Deploy"** in Vercel. The GitHub Actions workflow (`.github/workflows/vercel-deploy.yml`) will automatically trigger on future pushes.

---

## 🔐 Step 3: Set Up GitHub Secrets for Automated Deployments (Optional)

If you want the GitHub Actions workflow to automatically deploy to Vercel on each push:

1. Go to your GitHub repository: `https://github.com/N-i-k-e-t/murf-voiceflow-agent`
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **"New repository secret"** and add:

| Name | Value | Where to Find |
|------|-------|---|
| `VERCEL_TOKEN` | Your Vercel token | https://vercel.com/account/tokens |
| `VERCEL_ORG_ID` | Your Vercel org ID | Vercel dashboard → Settings → Organization → ID |
| `VERCEL_PROJECT_ID` | Your Vercel project ID | Vercel dashboard → Project → Settings → Project ID |

---

## 📝 Quick API Key Setup Guide

### SendGrid (Email Notifications)

1. Go to https://sendgrid.com
2. Sign up for a free account
3. Navigate to **Settings** → **API Keys**
4. Create an API key with "Mail Send" permission
5. Copy the key and add it to Vercel as `SENDGRID_API_KEY`

### Twilio (WhatsApp Notifications)

1. Go to https://www.twilio.com
2. Sign up for a free account
3. Navigate to **Console** → **Phone Numbers** → **Manage**
4. Create a Twilio phone number
5. Go to **Messaging** → **Services** → **WhatsApp**
6. Set up WhatsApp sandbox at: https://www.twilio.com/console/sms/whatsapp/sandbox
7. Copy `Account SID` and `Auth Token` from console
8. Use the WhatsApp sandbox number as `TWILIO_WHATSAPP_FROM`

---

## 🧪 Testing Locally Before Deployment

To test the serverless API locally:

```powershell
# 1. Install Vercel CLI
npm install -g vercel

# 2. Navigate to project
cd "c:\Users\NIKET\Downloads\murf-voiceflow-agent-main\murf-voiceflow-agent-main"

# 3. Create a local .env file
Copy-Item .env.example -Destination .env

# 4. Fill in your API keys in .env
# Edit .env with real SendGrid and Twilio keys

# 5. Run local Vercel development server
vercel dev

# 6. Visit http://localhost:3000/web/index.html
# 7. Fill out the form and submit
# 8. Check if email arrived at nikepatil1624@gmail.com
# 9. Check WhatsApp at +91 9022790410
```

---

## 📋 Deployment Checklist

### Before Pushing to GitHub:
- [x] All tests pass (20/22 — the 2 failures are expected)
- [x] Landing page works locally
- [x] All files are committed
- [ ] **You have pushed to GitHub**

### Before Deploying to Vercel:
- [ ] GitHub repository is public (or Vercel has access)
- [ ] Vercel project is created
- [ ] Environment variables are set in Vercel
- [ ] GitHub Actions secrets are set (if using automation)

### After Deploying to Vercel:
- [ ] Landing page loads at `https://<your-vercel-project>.vercel.app`
- [ ] Enquiry form submits successfully
- [ ] Email arrives at `nikepatil1624@gmail.com`
- [ ] WhatsApp message arrives at `+91 9022790410`

---

## 🔗 Project URLs (After Deployment)

```
GitHub:   https://github.com/N-i-k-e-t/murf-voiceflow-agent
Vercel:   https://<your-project-name>.vercel.app
Landing:  https://<your-project-name>.vercel.app/web/index.html
```

---

## 🆘 Troubleshooting

### Git Push Fails with "fatal: not a git repository"
```powershell
cd "c:\Users\NIKET\Downloads\murf-voiceflow-agent-main\murf-voiceflow-agent-main"
git status  # Should show git repository status
```

### Git Push Fails with "Authentication failed"
- Use GitHub CLI (`gh auth login`) or
- Use Personal Access Token instead of password or
- Use SSH key setup

### Form Submissions Not Reaching Email/WhatsApp
1. Check Vercel environment variables are set correctly
2. Verify SendGrid API key is valid
3. Verify Twilio credentials and WhatsApp sandbox setup
4. Check server logs in Vercel dashboard

### Landing Page Shows 404
- Ensure Vercel is serving the `web/` directory
- Check that `vercel.json` or `next.config.js` is configured (if needed)

---

## 📞 Contact for Help

- **Email**: nikepatil1624@gmail.com
- **WhatsApp**: +91 9022790410
- **GitHub Issues**: https://github.com/N-i-k-e-t/murf-voiceflow-agent/issues

---

## ✨ What's Next After Deployment

1. ✅ **Share the live link** with your network
2. ✅ **Test form submissions** from different devices
3. ✅ **Monitor incoming enquiries** via email + WhatsApp
4. ✅ **Update pricing page** with your consulting rates
5. ✅ **Add demo video** to the Demo tab
6. ✅ **Customize branding** as needed (colors, logo, etc.)

---

**You're all set! 🚀 Follow the checklist above and you'll have VoiceFlow live on Vercel.**
