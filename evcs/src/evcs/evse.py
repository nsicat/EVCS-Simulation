"""
Electric Vehicle Supply Equipment (EVSE) simulation module.
This module simulates the behavior of an EVSE in a charging station setup.
"""
import json
import uuid
from datetime import datetime
from typing import Dict, Any

class EVSE:
    def __init__(self, station_id: str):
        self.station_id = station_id
        self.session_id = None
        self.current_transaction = None
        
    def start_charging_session(self, vehicle_id: str) -> Dict[str, Any]:
        """Start a new charging session."""
        self.session_id = str(uuid.uuid4())
        self.current_transaction = {
            'session_id': self.session_id,
            'station_id': self.station_id,
            'vehicle_id': vehicle_id,
            'start_time': datetime.now().isoformat(),
            'status': 'active'
        }
        return self.current_transaction
    
    def get_charging_status(self) -> Dict[str, Any]:
        """Get current charging status."""
        if not self.current_transaction:
            return {'status': 'idle', 'station_id': self.station_id}
        return self.current_transaction
    
    def stop_charging_session(self) -> Dict[str, Any]:
        """Stop the current charging session."""
        if self.current_transaction:
            self.current_transaction['status'] = 'completed'
            self.current_transaction['end_time'] = datetime.now().isoformat()
            completed_transaction = self.current_transaction
            self.current_transaction = None
            self.session_id = None
            return completed_transaction
        return {'status': 'error', 'message': 'No active charging session'}
