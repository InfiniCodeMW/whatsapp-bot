#!/bin/bash

echo "Deploying WhatsApp Payment Bot..."

# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
nano .env

# Set up AWS credentials
aws configure

# Start the application
sudo systemctl restart whatsapp-bot