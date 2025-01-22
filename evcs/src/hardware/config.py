"""
Hardware configuration for physical EVCS simulation using Raspberry Pis.
"""
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class NetworkConfig:
    # Network configuration for each component
    EVSE_HOST: str = "192.168.1.101"  # Raspberry Pi 1 (EVSE)
    SCMS_HOST: str = "192.168.1.102"  # Raspberry Pi 2 (SCMS)
    ATTACKER_HOST: str = "192.168.1.103"  # Raspberry Pi 3 (Attacker)
    
    # Ports for different services
    EVSE_PORT: int = 5000
    SCMS_PORT: int = 5001
    ATTACKER_PORT: int = 5002
    
    # Communication protocols
    USE_SSL: bool = True
    CERT_PATH: str = "/etc/evcs/certs/"
    
@dataclass
class HardwareConfig:
    # GPIO pins for LED indicators
    STATUS_LED_PIN: int = 18
    ERROR_LED_PIN: int = 23
    ACTIVE_LED_PIN: int = 24
    
    # GPIO pins for RFID reader (if using for authentication)
    RFID_SDA_PIN: int = 24
    RFID_SCK_PIN: int = 23
    RFID_MOSI_PIN: int = 19
    RFID_MISO_PIN: int = 21
    RFID_RST_PIN: int = 22
    
    # GPIO pins for physical buttons/switches
    START_BUTTON_PIN: int = 17
    STOP_BUTTON_PIN: int = 27
    
    # I2C display configuration (if using LCD/OLED display)
    DISPLAY_I2C_ADDR: int = 0x3C
    DISPLAY_I2C_BUS: int = 1

network_config = NetworkConfig()
hardware_config = HardwareConfig()
