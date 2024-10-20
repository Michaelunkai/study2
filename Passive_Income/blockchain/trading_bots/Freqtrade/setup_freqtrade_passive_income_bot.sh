#!/bin/ 

################################################################################
# Script Name: setup_freqtrade_passive_income_bot_fixed.sh
# Description: Automates the installation, configuration, and execution of the
#              Freqtrade crypto trading bot on Ubuntu for generating passive income.
# Tools Used: Python3, pip, git, TA-Lib, Freqtrade
# Author: OpenAI ChatGPT
# Date: 2024-04-27
################################################################################

# Exit immediately if a command exits with a non-zero status.
set -e

# Function to print messages in green color
print_success() {
    echo -e "\e[32m$1\e[0m"
}

# Function to print messages in yellow color
print_info() {
    echo -e "\e[33m$1\e[0m"
}

# Function to print messages in red color
print_error() {
    echo -e "\e[31m$1\e[0m"
}

print_info "Starting Freqtrade setup script..."

################################################################################
# Step 1: Install Essential Dependencies
################################################################################

print_info "Installing essential dependencies..."

# Update package list
apt-get update -y

# Install Python3, pip, git, and other essential packages
apt-get install -y python3 python3-pip git build-essential libssl-dev libffi-dev python3-dev wget tar libtool autoconf automake pkg-config

print_success "Essential dependencies installed."

################################################################################
# Step 2: Install TA-Lib from Source
################################################################################

print_info "Installing TA-Lib from source..."

# Download TA-Lib source
cd /tmp
wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz

# Extract the tarball
tar -xzf ta-lib-0.4.0-src.tar.gz

# Navigate into the directory
cd ta-lib

# Configure and install
./configure --prefix=/usr
make
make install

# Update the linker cache
ldconfig

# Cleanup
cd ..
rm -rf ta-lib ta-lib-0.4.0-src.tar.gz

print_success "TA-Lib installed successfully."

################################################################################
# Step 3: Clone the Freqtrade Repository
################################################################################

print_info "Cloning the Freqtrade repository..."

# Navigate to home directory
cd ~/

# Clone Freqtrade repository if not already cloned
if [ ! -d "freqtrade" ]; then
    git clone https://github.com/freqtrade/freqtrade.git
fi

cd freqtrade

print_success "Freqtrade repository cloned."

################################################################################
# Step 4: Install Freqtrade as a Command-Line Application
################################################################################

print_info "Installing Freqtrade as a command-line application..."

# Upgrade pip
pip3 install --upgrade pip

# Install Freqtrade using pip in editable mode
pip3 install -e .

print_success "Freqtrade installed as a command-line application."

################################################################################
# Step 5: Install TA-Lib Python Wrapper
################################################################################

print_info "Installing TA-Lib Python wrapper..."

# Install TA-Lib Python wrapper
pip3 install TA-Lib

print_success "TA-Lib Python wrapper installed."

################################################################################
# Step 6: Create User Data Directory
################################################################################

print_info "Creating user_data directory..."

# Create user_data directory
mkdir -p user_data/config user_data/strategies

print_success "user_data directory created."

################################################################################
# Step 7: Generate Configuration File
################################################################################

print_info "Generating configuration file..."

# Prompt user for exchange details
read -p "Enter your exchange name (e.g., binance): " exchange
read -p "Enter your API key: " api_key
read -p "Enter your API secret: " api_secret
read -p "Enter your Telegram token (leave blank if not using): " telegram_token
read -p "Enter your Telegram chat ID (leave blank if not using): " telegram_chat_id

# Determine Telegram enabled status
if [ -z "$telegram_token" ] || [ -z "$telegram_chat_id" ]; then
    telegram_enabled=false
else
    telegram_enabled=true
fi

# Generate config.json
cat > user_data/config/config.json <<EOL
{
    "max_open_trades": 10,
    "stake_currency": "USDT",
    "stake_amount": 100,
    "dry_run": true,
    "dry_run_wallet": 1000,
    "cancel_open_orders_on_exit": false,
    "trading_mode": "spot",
    "exchange": {
        "name": "$exchange",
        "key": "$api_key",
        "secret": "$api_secret",
        "ccxt_config": {},
        "ccxt_async_config": {},
        "pair_whitelist": ["BTC/USDT", "ETH/USDT"],
        "pair_blacklist": []
    },
    "telegram": {
        "enabled": $telegram_enabled,
        "token": "$telegram_token",
        "chat_id": "$telegram_chat_id"
    },
    "logger": {
        "loglevel": "info",
        "console_log_level": "info",
        "file_log_level": "info",
        "logfile": "freqtrade.log",
        "rotation": {
            "size": 10000000,
            "backup_count": 7
        }
    },
    "strategy": "SampleStrategy",
    "timeframe": "5m",
    "startup_candle_count": 30
}
EOL

print_success "Configuration file created at user_data/config/config.json."

################################################################################
# Step 8: Create a Sample Strategy
################################################################################

print_info "Creating a sample trading strategy..."

# Create a simple sample strategy file
cat > user_data/strategies/SampleStrategy.py <<EOL
from freqtrade.strategy import IStrategy
import talib.abstract as ta

class SampleStrategy(IStrategy):
    # Optimal timeframe for the strategy
    timeframe = '5m'

    # Minimal ROI designed for the strategy
    minimal_roi = {
        "0": 0.05
    }

    # Stoploss
    stoploss = -0.10

    # Trailing stoploss
    trailing_stop = False

    # Optimal timeframe for the strategy
    process_only_new_candles = True

    def populate_indicators(self, dataframe, metadata):
        # Simple Moving Average
        dataframe['sma'] = ta.SMA(dataframe, timeperiod=15)
        return dataframe

    def populate_buy_trend(self, dataframe, metadata):
        dataframe.loc[
            (
                (dataframe['close'] > dataframe['sma'])
            ),
            'buy'] = 1
        return dataframe

    def populate_sell_trend(self, dataframe, metadata):
        dataframe.loc[
            (
                (dataframe['close'] < dataframe['sma'])
            ),
            'sell'] = 1
        return dataframe
EOL

print_success "Sample trading strategy created at user_data/strategies/SampleStrategy.py."

################################################################################
# Step 9: Download Historical Data for Backtesting
################################################################################

print_info "Downloading historical data for backtesting..."

# Download historical data for the specified pairs and timeframe
freqtrade download-data --config user_data/config/config.json --timerange=20210101-20210201

print_success "Historical data downloaded."

################################################################################
# Step 10: Backtest the Strategy
################################################################################

print_info "Running backtest to evaluate the strategy..."

# Perform backtesting with the sample strategy
freqtrade backtesting --config user_data/config/config.json --strategy SampleStrategy

print_success "Backtesting completed."

################################################################################
# Step 11: Start the Trading Bot
################################################################################

print_info "Starting the Freqtrade trading bot in dry-run mode..."

# Start trading with the configured settings in dry-run mode
freqtrade trade --config user_data/config/config.json

print_success "Freqtrade bot is now running in dry-run mode."

################################################################################
# End of Script
################################################################################

print_success "Freqtrade setup and execution completed successfully!"
print_info "To start live trading, set \"dry_run\" to false in user_data/config/config.json and restart the bot."
