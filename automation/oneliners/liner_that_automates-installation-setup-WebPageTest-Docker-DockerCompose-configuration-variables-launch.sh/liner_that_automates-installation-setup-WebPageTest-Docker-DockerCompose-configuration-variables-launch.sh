sudo apt install -y apt-transport-https ca-certificates curl software-properties-common git && \
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg && \
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null && \
sudo apt install -y docker-ce docker-ce-cli containerd.io && \
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && \
sudo chmod +x /usr/local/bin/docker-compose && \
git clone https://github.com/WPO-Foundation/webpagetest.git && \
cd webpagetest && \
echo "ADMIN_EMAIL=admin@yourdomain.com
DATABASE_URL=my ://wpt_user:StrongPassword123@db/webpagetest
SECRET_KEY_BASE=$(openssl rand -hex 64)" > .env && \
sudo docker-compose up -d
