# 1. Launch EC2 (Ubuntu)

# 2. SSH
ssh -i key.pem ubuntu@your-ip

# 3. Install Docker
sudo apt update
sudo apt install docker.io -y

# 4. Clone repo
git clone <your-repo>
cd incident-commander

# 5. Run
sudo docker build -t incident .
sudo docker run --env-file .env incident