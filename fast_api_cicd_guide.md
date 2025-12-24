# FastAPI CI/CD Deployment Guide (GitHub Actions → Azure VM)

This guide explains **step‑by‑step** how to deploy a FastAPI application to an Azure VM using **GitHub Actions CI/CD** — including SSH key setup, GitHub secrets, and automatic service restart using **systemd**.

---

## ✔️ What You Will Get

- Fully automated CI/CD pipeline
- Secure SSH‑based deployment
- Production FastAPI service (managed by systemd)
- Restart on every deployment
- Zero manual VM work after setup

---

# 🏗 Prerequisites

- Ubuntu VM running FastAPI
- GitHub repository with branch:

```
prod
```

- Python virtual environment inside VM:

```
/home/azureuser/Fast-API-practice/venv
```

> ℹ️ **Note:** Replace paths and usernames if needed.

---

# ✅ STEP 1 — Create SSH Key on VM (No Passphrase)

Run on your Azure VM:

```
cd ~/.ssh
ssh-keygen -t ed25519 -C "github-actions"
```

When prompted:

- File path → press Enter (or choose a custom name)
- Passphrase → press Enter (leave empty)

This will create:

```
id_ed25519
id_ed25519.pub
```

### ➕ Add PUBLIC key to authorized_keys

```
cat ~/.ssh/id_ed25519.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

### 🔐 Set permissions

```
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_ed25519
chmod 600 ~/.ssh/id_ed25519.pub
```

**📌 Clarification:**

SSH requires correct permissions — otherwise authentication fails.

**🔗 Reference:**
- https://linux.die.net/man/8/sshd

---

# 🔑 STEP 2 — Add Private Key to GitHub Secrets

Open:

```
GitHub Repo → Settings → Secrets → Actions
```

Create these secrets:

| Secret Name | Value |
|-------------|-------|
| `VM_HOST` | Your VM Public IP |
| `VM_USER` | azureuser |
| `VM_SSH_KEY` | Paste FULL `id_ed25519` private key |

To display your private key on VM:

```
cat ~/.ssh/id_ed25519
```

Copy everything:

```
-----BEGIN OPENSSH PRIVATE KEY-----
...
-----END OPENSSH PRIVATE KEY-----
```

**📌 Clarification:**

GitHub Actions authenticates using your SSH private key only.

**🔗 Reference:**
- https://docs.github.com/en/actions/security-guides/encrypted-secrets

---

# 🛠 STEP 3 — Create GitHub Actions Workflow

Create file:

```
.github/workflows/deploy.yml
```

Paste:

```yaml
name: Deploy FastAPI App (prod)

on:
  push:
    branches: ["prod"]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Deploy & Restart FastAPI on VM
        uses: appleboy/ssh-action@v1.0.3
        with:
          host: ${{ secrets.VM_HOST }}
          username: ${{ secrets.VM_USER }}
          key: ${{ secrets.VM_SSH_KEY }}
          script: |
            set -e

            APP_DIR="/home/azureuser/Fast-API-practice"
            SERVICE_NAME="fastapi-app"
            PYTHON_ENV="$APP_DIR/venv"

            cd $APP_DIR

            git fetch origin
            git checkout prod
            git pull origin prod

            if [ ! -d "$PYTHON_ENV" ]; then
              python3 -m venv $PYTHON_ENV
            fi

            source $PYTHON_ENV/bin/activate

            pip install -r requirements.txt

            sudo bash -c "cat > /etc/systemd/system/$SERVICE_NAME.service" <<EOF
            [Unit]
            Description=FastAPI App Service
            After=network.target

            [Service]
            User=azureuser
            WorkingDirectory=$APP_DIR
            Environment=PATH=$PYTHON_ENV/bin
            ExecStart=$PYTHON_ENV/bin/uvicorn main:app --host 0.0.0.0 --port 8000
            Restart=always
            RestartSec=5

            [Install]
            WantedBy=multi-user.target
            EOF

            sudo systemctl daemon-reload
            sudo systemctl enable $SERVICE_NAME
            sudo systemctl restart $SERVICE_NAME
            sudo systemctl status $SERVICE_NAME --no-pager -l || true

            echo "Deployment completed successfully"
```

**📌 Clarification:**

- Deployment runs when code is pushed to `prod`
- SSH connects securely
- App restarts automatically

**🔗 Reference:**
- https://github.com/appleboy/ssh-action

---

# 🚦 STEP 4 — Deployment Flow

1. Push code to `prod`
2. GitHub Actions triggers
3. VM pulls latest changes
4. Virtual environment installs dependencies
5. FastAPI restarts via systemd

**📌 Clarification:**

CI/CD ensures consistent deployments.

**🔗 Reference:**
- https://docs.github.com/en/actions

---

# 🧪 STEP 5 — Verify App is Running

Check service logs:

```
sudo systemctl status fastapi-app
```

Follow logs:

```
journalctl -u fastapi-app -f
```

Test API:

```
curl http://YOUR_VM_IP:8000
```

---

# 🔒 Security Notes

- Do **NOT** share private keys
- Use protected branches for `prod`
- Restrict VM SSH access by IP

---

# 🧹 Optional Enhancements

- Add Nginx Reverse Proxy
- Enable HTTPS (Certbot)
- Add Gunicorn workers
- Blue‑Green deployment

---

# ✅ You’re Done!

You now have:

✔ automated deployments
✔ production service
✔ clean CI/CD pipeline
✔ zero manual work after setup

---

If you want me to:

- format this for docs
- add diagrams
- add rollback strategy

Just say so 🙂

