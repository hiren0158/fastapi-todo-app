# 🚀 Deploy to Render.com (No Credit Card Required)

This guide shows you how to deploy for **FREE** without a credit card.

## ⚠️ The Challenge & Solution

**The Challenge:**
Render's free tier "sleeps" (shuts down) after 15 minutes of inactivity. This would stop your 23:59 daily email job.

**The Solution:**
We will use a **Free Uptime Monitor** (like UptimeRobot) to ping your app every 5 minutes. This keeps it "awake" 24/7 so your scheduled emails always send!

---

## Step 1: Prepare Your Code

1. **Push your code to GitHub**
   ```bash
   git push -u origin main
   ```
   (If you haven't pushed yet, run this in your terminal)

## Step 2: Create Render Account

1. Go to **[dashboard.render.com/register](https://dashboard.render.com/register)**
2. Sign up with **GitHub**
3. No credit card required!

## Step 3: Create Web Service

1. Click **"New +"** → **"Web Service"**
2. Select **"Build and deploy from a Git repository"**
3. Select repository **`hiren0158/fastapi-todo-app`**
4. **Configuration:**
   - **Name:** `fastapi-todo-app`
   - **Region:** Singapore (closest to India)
   - **Branch:** `main`
   - **Runtime:** **Docker** (Important!)
   - **Instance Type:** **Free**

## Step 4: Configure Environment Variables

Scroll down to **"Environment Variables"** and add these:

| Key | Value |
|-----|-------|
| `MONGODB_URL` | `mongodb+srv://hiren158:Hiren100@todoappcluster.wwpondr.mongodb.net/todoapp?retryWrites=true&w=majority` |
| `MONGODB_DB_NAME` | `todoapp` |
| `SECRET_KEY` | `any-random-secret-string-here` |
| `SMTP_HOST` | `smtp.sendgrid.net` |
| `SMTP_PORT` | `587` |
| `SMTP_USERNAME` | `apikey` |
| `SMTP_PASSWORD` | `YOUR_SENDGRID_API_KEY` |
| `EMAIL_FROM` | `hirenn158@gmail.com` |
| `SENDER_EMAIL` | `hirenn158@gmail.com` |
| `SUMMARY_EMAIL_ENABLED` | `true` |
| `DAILY_RESET_ENABLED` | `true` |
| `SMTP_USE_TLS` | `true` |
| `PORT` | `8081` |

## Step 5: Deploy

1. Click **"Create Web Service"**
2. Render will start building your Docker image.
3. Wait ~5-10 minutes.
4. Once done, you'll see "Live" and a URL like: `https://fastapi-todo-app.onrender.com`

---

## Step 6: Keep It Awake (CRITICAL!) ⚡

To ensure your 23:59 email job runs, you must prevent the app from sleeping.

1. Go to **[uptimerobot.com](https://uptimerobot.com)**
2. Click **"Register for FREE"**
3. Login and click **"+ Add New Monitor"**
4. **Settings:**
   - **Monitor Type:** HTTP(s)
   - **Friendly Name:** My Todo App
   - **URL (or IP):** `https://your-app-name.onrender.com/healthy`
     *(Use your actual Render URL + /healthy)*
   - **Monitoring Interval:** 5 minutes
5. Click **"Create Monitor"**

**✅ Done!**
- UptimeRobot will ping your app every 5 minutes.
- This prevents Render from "sleeping".
- Your app stays running 24/7.
- Your daily emails will send correctly!
- **Total Cost: $0**
