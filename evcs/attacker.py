"""
MITM Attack simulation module.
This module demonstrates how a MITM attack could intercept and manipulate
communication between EVSE and SCMS.
"""
from typing import Dict, Any, Callable

class MITMAttacker:
    def __init__(self):
        self.intercepted_data = []
        
    def intercept_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Intercept and potentially modify a message."""
        # Log the intercepted message
        self.intercepted_data.append({
            'timestamp': message.get('timestamp'),
            'original_message': message
        })
        
        # In a real attack, the message could be modified here
        return message
    
    def get_intercepted_data(self) -> list:
        """Retrieve all intercepted data."""
        return self.intercepted_data

class ProxyServer:
    def __init__(self, mitm_attacker: MITMAttacker):
        self.mitm = mitm_attacker
        
    def forward_message(self, 
                       message: Dict[str, Any],
                       original_sender: Callable,
                       destination: Callable) -> Dict[str, Any]:
        """
        Forward a message through the MITM proxy.
        This simulates the interception and forwarding of messages.
        """
        # Intercept and potentially modify the message
        modified_message = self.mitm.intercept_message(message)
        
        # Forward the (potentially modified) message to its destination
        response = destination(modified_message)
        
        # The response could also be intercepted and modified
        return self.mitm.intercept_message(response)
