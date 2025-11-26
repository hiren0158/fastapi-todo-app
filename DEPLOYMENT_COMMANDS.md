# Deployment Commands Reference

## Commands We'll Run After MongoDB Setup

### 1. Set Environment Variables (Secrets)

```bash
# MongoDB (you'll provide this)
flyctl secrets set MONGODB_URL="mongodb+srv://todoapp:PASSWORD@cluster.mongodb.net/todoapp"

# Database name
flyctl secrets set MONGODB_DB_NAME="todoapp"

# Security key (random string)
flyctl secrets set SECRET_KEY="$(openssl rand -hex 32)"

# SMTP Configuration (SendGrid)
flyctl secrets set SMTP_HOST="smtp.sendgrid.net"
flyctl secrets set SMTP_PORT="587"
flyctl secrets set SMTP_USERNAME="apikey"
flyctl secrets set SMTP_PASSWORD="YOUR_SENDGRID_API_KEY"
flyctl secrets set EMAIL_FROM="hirenn158@gmail.com"
flyctl secrets set SENDER_EMAIL="hirenn158@gmail.com"
flyctl secrets set SMTP_USE_TLS="true"

# Feature flags
flyctl secrets set SUMMARY_EMAIL_ENABLED="true"
flyctl secrets set DAILY_RESET_ENABLED="true"
```

### 2. Deploy Application

```bash
flyctl deploy
```

### 3. Verify Deployment

```bash
# Check status
flyctl status

# View logs
flyctl logs

# Open in browser
flyctl open

# Test health endpoint
curl https://fastapi-todo-app.fly.dev/healthy
```

---

## Useful Management Commands

```bash
# View all secrets
flyctl secrets list

# Restart app
flyctl apps restart

# SSH into container
flyctl ssh console

# Scale resources (if needed)
flyctl scale memory 512

# View dashboard
flyctl dashboard
```

---

## What Happens During Deployment:

1. ✅ Fly.io reads `fly.toml` config
2. ✅ Builds Docker image from your `Dockerfile`
3. ✅ Uploads image to Fly.io registry
4. ✅ Deploys to Singapore region
5. ✅ Starts your FastAPI app
6. ✅ Scheduler activates (23:59 daily email job)
7. ✅ Provides HTTPS URL

Estimated deployment time: **2-3 minutes**

---

## After Deployment You'll Get:

- 🌐 URL: `https://fastapi-todo-app.fly.dev`
- 🔒 Automatic HTTPS/SSL
- 🚀 Running 24/7 (no sleep!)
- 📧 Emails send at 23:59 IST daily
- 💰 Cost: $0/month (free tier)
