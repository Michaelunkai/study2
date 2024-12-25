nano install-cloudflared-tunneltool.sh
#!/bin/bash
curl -LO https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
mv cloudflared-linux-amd64 /usr/local/bin/cloudflared
chmod +x /usr/local/bin/cloudflared
export PATH=$PATH:/usr/local/bin
cloudflared -v
