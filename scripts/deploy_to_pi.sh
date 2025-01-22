#!/bin/bash

# Usage: ./deploy_to_pi.sh [evse|scms|attacker] [raspberry_pi_ip]
# Example: ./deploy_to_pi.sh evse 192.168.1.101

COMPONENT=$1
PI_IP=$2
PI_USER="pi"
PROJECT_DIR="/home/pi/evcs-mitm"

if [ -z "$COMPONENT" ] || [ -z "$PI_IP" ]; then
    echo "Usage: ./deploy_to_pi.sh [evse|scms|attacker] [raspberry_pi_ip]"
    exit 1
fi

# Create required directories
ssh $PI_USER@$PI_IP "mkdir -p $PROJECT_DIR"

# Copy project files
rsync -avz --exclude 'venv' --exclude '__pycache__' --exclude '.git' \
    ../ $PI_USER@$PI_IP:$PROJECT_DIR/

# Install dependencies
ssh $PI_USER@$PI_IP "cd $PROJECT_DIR && \
    python3 -m venv venv && \
    source venv/bin/activate && \
    pip install -r requirements.txt"

# Setup system service
cat > ${COMPONENT}_service.txt << EOL
[Unit]
Description=EVCS ${COMPONENT} Service
After=network.target

[Service]
User=pi
WorkingDirectory=$PROJECT_DIR
Environment=PATH=$PROJECT_DIR/venv/bin
ExecStart=$PROJECT_DIR/venv/bin/python -m evcs.src.hardware.physical_${COMPONENT}
Restart=always

[Install]
WantedBy=multi-user.target
EOL

# Copy and enable service
scp ${COMPONENT}_service.txt $PI_USER@$PI_IP:/tmp/evcs_${COMPONENT}.service
ssh $PI_USER@$PI_IP "sudo mv /tmp/evcs_${COMPONENT}.service /etc/systemd/system/ && \
    sudo systemctl daemon-reload && \
    sudo systemctl enable evcs_${COMPONENT} && \
    sudo systemctl start evcs_${COMPONENT}"

rm ${COMPONENT}_service.txt

echo "Deployment of ${COMPONENT} to ${PI_IP} completed!"
