"""
Physical EVSE implementation for Raspberry Pi.
This module handles the hardware interactions for the EVSE simulation.
"""
import RPi.GPIO as GPIO
from flask import Flask, request, jsonify
from RPLCD.i2c import CharLCD
import time
from typing import Dict, Any
from ..evcs.evse import EVSE
from .config import network_config, hardware_config

class PhysicalEVSE(EVSE):
    def __init__(self, station_id: str):
        super().__init__(station_id)
        self.setup_hardware()
        self.setup_display()
        self.app = self.create_flask_app()
        
    def setup_hardware(self):
        """Initialize GPIO pins and hardware components."""
        GPIO.setmode(GPIO.BCM)
        
        # Setup LED indicators
        GPIO.setup(hardware_config.STATUS_LED_PIN, GPIO.OUT)
        GPIO.setup(hardware_config.ERROR_LED_PIN, GPIO.OUT)
        GPIO.setup(hardware_config.ACTIVE_LED_PIN, GPIO.OUT)
        
        # Setup buttons
        GPIO.setup(hardware_config.START_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(hardware_config.STOP_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        # Add button event listeners
        GPIO.add_event_detect(hardware_config.START_BUTTON_PIN, 
                            GPIO.FALLING, 
                            callback=self.handle_start_button,
                            bouncetime=300)
        GPIO.add_event_detect(hardware_config.STOP_BUTTON_PIN,
                            GPIO.FALLING,
                            callback=self.handle_stop_button,
                            bouncetime=300)
    
    def setup_display(self):
        """Initialize I2C display."""
        self.lcd = CharLCD(i2c_expander='PCF8574',
                          address=hardware_config.DISPLAY_I2C_ADDR,
                          port=hardware_config.DISPLAY_I2C_BUS,
                          cols=16, rows=2)
    
    def update_display(self, message: str):
        """Update the LCD display with current status."""
        self.lcd.clear()
        self.lcd.write_string(message[:32])  # Limit to display size
    
    def handle_start_button(self, channel):
        """Handle physical start button press."""
        if not self.current_transaction:
            # Simulate vehicle connection with dummy ID
            transaction = self.start_charging_session("DEMO_VEHICLE")
            GPIO.output(hardware_config.ACTIVE_LED_PIN, GPIO.HIGH)
            self.update_display("Charging Active")
    
    def handle_stop_button(self, channel):
        """Handle physical stop button press."""
        if self.current_transaction:
            self.stop_charging_session()
            GPIO.output(hardware_config.ACTIVE_LED_PIN, GPIO.LOW)
            self.update_display("Charging Stopped")
    
    def create_flask_app(self):
        """Create Flask app for REST API."""
        app = Flask(__name__)
        
        @app.route('/status', methods=['GET'])
        def get_status():
            return jsonify(self.get_charging_status())
        
        @app.route('/start', methods=['POST'])
        def start_charging():
            data = request.get_json()
            return jsonify(self.start_charging_session(data['vehicle_id']))
        
        @app.route('/stop', methods=['POST'])
        def stop_charging():
            return jsonify(self.stop_charging_session())
        
        return app
    
    def run_server(self):
        """Run the EVSE server."""
        self.app.run(host=network_config.EVSE_HOST,
                    port=network_config.EVSE_PORT,
                    ssl_context='adhoc' if network_config.USE_SSL else None)
    
    def cleanup(self):
        """Cleanup GPIO on shutdown."""
        GPIO.cleanup()
        self.lcd.clear()
        self.lcd.close()
