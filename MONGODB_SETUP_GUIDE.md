# Quick MongoDB Atlas Setup Checklist

## Current Step: Setting up MongoDB Atlas Database

### What You Need to Do:

1. **Go to:** https://www.mongodb.com/cloud/atlas/register

2. **Sign Up/Login**
   - Use: hirenn158@gmail.com (same as Fly.io)

3. **Create Free Cluster:**
   - Click "Build a Database" or "+ Create"
   - Select **M0 FREE** tier
   - Provider: AWS
   - Region: **Mumbai (ap-south-1)** OR **Singapore (ap-southeast-1)**
   - Name: `TodoAppCluster`
   - Click "Create Cluster" (takes 3-5 minutes)

4. **Security Setup (will appear automatically):**
   
   **A. Create Database User:**
   - Username: `todoapp`
   - Click "Autogenerate Secure Password" 
   - **⚠️ IMPORTANT: Copy and save the password!**
   - Click "Create User"
   
   **B. Network Access:**
   - Choose "My Local Environment"
   - IP Address: `0.0.0.0/0` (or click "Allow Access from Anywhere")
   - Click "Add Entry"
   - Click "Finish and Close"

5. **Get Connection String:**
   - Wait for cluster to finish creating (green status)
   - Click "Connect" button on your cluster
   - Select "Drivers" (or "Connect your application")
   - Driver: Python
   - Copy the connection string
   - Replace `<password>` with your saved password
   - Replace `<database>` with `todoapp`

### Your Connection String Should Look Like:

```
mongodb+srv://todoapp:YOUR_PASSWORD_HERE@todoappcluster.xxxxx.mongodb.net/todoapp?retryWrites=true&w=majority
```

### Troubleshooting:

**Cluster creation taking too long?**
- It usually takes 3-5 minutes
- Look for green checkmark next to cluster name

**Can't find Connect button?**
- Wait for cluster to finish creating
- Refresh the page
- Look for "Connect" button next to cluster name

**Password has special characters?**
- You may need to URL-encode them
- Or regenerate a simpler password (letters and numbers only)

---

## Once You Have the Connection String:

Just paste it here in the chat, and I'll:
1. Configure all environment variables
2. Deploy your app to Fly.io
3. Test everything works

**Estimated time remaining:** 5-10 minutes after you provide the connection string.
