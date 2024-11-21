#!/bin/ 

# Step 1: Install Required Dependencies without update
echo "Installing Git, PHP, Composer, and necessary PHP extensions..."
sudo apt install -y git curl unzip php php-cli php-fpm php-json php-common php-mysql php-zip php-gd php-mbstring php-curl php-xml php-pear php-bcmath && php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');" && php composer-setup.php --install-dir=/usr/local/bin --filename=composer && php -r "unlink('composer-setup.php');" && php /usr/local/bin/composer

# Step 2: Clone the Laravel Boilerplate Repository
echo "Cloning Laravel Boilerplate repository..."
git clone https://github.com/rappasoft/laravel-boilerplate.git
cd laravel-boilerplate

# Step 3: Install Project Dependencies
echo "Installing PHP dependencies using Composer..."
composer install

# Step 4: Set Up Environment Configuration
echo "Setting up environment configuration..."
cp .env.example .env
  artisan key:generate

# Step 5: Configure the .env File
echo "Configuring the .env file..."
cat <<EOL > .env
APP_NAME="Laravel Boilerplate"
APP_ENV=local
APP_KEY=$(php artisan key:generate --show)
APP_DEBUG=true
APP_URL=http://localhost

# Misc
APP_READ_ONLY=false
APP_READ_ONLY_LOGIN=true
DEBUGBAR_ENABLED=false
LOG_CHANNEL=daily
LOG_LEVEL=debug

# Drivers
DB_CONNECTION=my 
BROADCAST_DRIVER=log
CACHE_DRIVER=file
FILESYSTEM_DRIVER=local
QUEUE_CONNECTION=sync
SESSION_DRIVER=file
SESSION_LIFETIME=120

# Database
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=laravel
DB_USERNAME=root
DB_PASSWORD=root_password

# Cache
MEMCACHED_HOST=127.0.0.1

# Queue
REDIS_HOST=127.0.0.1
REDIS_PASSWORD=null
REDIS_PORT=6379

# Mail
MAIL_MAILER=smtp
MAIL_HOST=smtp.mailtrap.io
MAIL_PORT=2525
MAIL_USERNAME=null
MAIL_PASSWORD=null
MAIL_ENCRYPTION=null
MAIL_FROM_ADDRESS=null
MAIL_FROM_NAME="\${APP_NAME}"

# AWS
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_DEFAULT_REGION=us-east-1
AWS_BUCKET=
AWS_USE_PATH_STYLE_ENDPOINT=false

# Pusher
PUSHER_APP_ID=
PUSHER_APP_KEY=
PUSHER_APP_SECRET=
PUSHER_APP_CLUSTER=mt1

MIX_PUSHER_APP_KEY="\${PUSHER_APP_KEY}"
MIX_PUSHER_APP_CLUSTER="\${PUSHER_APP_CLUSTER}"

# Application

# Access
ADMIN_REQUIRES_2FA=true
CHANGE_EMAIL=true
ENABLE_REGISTRATION=true
PASSWORD_HISTORY=3
SINGLE_LOGIN=false
PASSWORD_EXPIRES_DAYS=180

# Captcha
# Get your credentials at: https://www.google.com/recaptcha/admin
LOGIN_CAPTCHA_STATUS=false
REGISTRATION_CAPTCHA_STATUS=false
INVISIBLE_RECAPTCHA_SITEKEY=
INVISIBLE_RECAPTCHA_SECRETKEY=

# Socialite Providers
FACEBOOK_ACTIVE=false
BITBUCKET_ACTIVE=false
GITHUB_ACTIVE=false
GOOGLE_ACTIVE=false
LINKEDIN_ACTIVE=false
TWITTER_ACTIVE=false

#FACEBOOK_CLIENT_ID=
#FACEBOOK_CLIENT_SECRET=
#FACEBOOK_REDIRECT=\${APP_URL}/login/facebook/callback

#BITBUCKET_CLIENT_ID=
#BITBUCKET_CLIENT_SECRET=
#BITBUCKET_REDIRECT=\${APP_URL}/login/bitbucket/callback

#GITHUB_CLIENT_ID=
#GITHUB_CLIENT_SECRET=
#GITHUB_REDIRECT=\${APP_URL}/login/github/callback

#GOOGLE_CLIENT_ID=
#GOOGLE_CLIENT_SECRET=
#GOOGLE_REDIRECT=\${APP_URL}/login/google/callback

#LINKEDIN_CLIENT_ID=
#LINKEDIN_CLIENT_SECRET=
#LINKEDIN_REDIRECT=\${APP_URL}/login/linkedin/callback

#TWITTER_CLIENT_ID=
#TWITTER_CLIENT_SECRET=
#TWITTER_REDIRECT=\${APP_URL}/login/twitter/callback
EOL

# Step 6: Set Up MySQL Database and User
echo "Setting up MySQL database and user..."
sudo apt install -y mysql-server
sudo mysql -u root -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'root_password'; FLUSH PRIVILEGES;"
sudo mysql -u root -p'root_password' -e "CREATE DATABASE laravel;"

# Step 7: Run Migrations and Seeders
echo "Running migrations and seeders..."
php artisan migrate --seed

# Step 8: Serve the Application
echo "Serving the application..."
  artisan serve

echo "Laravel Boilerplate setup complete! Access the application at http://127.0.0.1:8000"
