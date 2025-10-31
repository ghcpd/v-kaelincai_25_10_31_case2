"""
Original Data Validation System - FAULTY VERSION with Regression

This version introduced a "performance optimization" using isinstance() checks
that inadvertently broke the flexible type handling that previously worked.

REGRESSION: The code now rejects valid inputs that are string representations
of numbers or non-standard boolean representations, which the original system
handled gracefully through duck typing and string conversion.
"""

import json
import re
from typing import Dict, Any, Tuple


class DataValidator:
    """
    Data validation system with REGRESSION BUG introduced in v2.0.
    
    The bug: Overly strict isinstance() type checking was added for "performance",
    but it breaks compatibility with inputs that were previously accepted.
    """
    
    REQUIRED_FIELDS = ['user_id', 'username', 'email', 'age', 'balance', 'is_active']
    
    def __init__(self):
        self.validation_errors = []
    
    def validate_and_normalize(self, data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """
        Validate and normalize user data.
        
        REGRESSION: This version uses strict isinstance() checks that reject
        valid string representations of numbers that were previously accepted.
        """
        self.validation_errors = []
        
        # Check required fields
        missing_fields = [field for field in self.REQUIRED_FIELDS if field not in data]
        if missing_fields:
            return False, {
                'valid': False,
                'error': f"Missing required fields: {', '.join(missing_fields)}"
            }
        
        normalized = {}
        
        # REGRESSION BUG: Strict type checking for user_id
        # Previously accepted strings, now only accepts int
        if not isinstance(data['user_id'], int):
            return False, {
                'valid': False,
                'error': f"user_id must be an integer, got {type(data['user_id']).__name__}"
            }
        normalized['user_id'] = str(data['user_id'])
        
        # Username validation (with security check)
        if not isinstance(data['username'], str):
            return False, {
                'valid': False,
                'error': f"username must be a string, got {type(data['username']).__name__}"
            }
        
        if not re.match(r'^[a-zA-Z0-9_]+$', data['username']):
            return False, {
                'valid': False,
                'error': "Username contains invalid characters"
            }
        normalized['username'] = data['username']
        
        # Email validation
        if not isinstance(data['email'], str):
            return False, {
                'valid': False,
                'error': f"email must be a string, got {type(data['email']).__name__}"
            }
        
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', data['email']):
            return False, {
                'valid': False,
                'error': "Invalid email format"
            }
        normalized['email'] = data['email']
        
        # REGRESSION BUG: Strict type checking for age
        # Previously accepted strings and floats, now only accepts int
        if not isinstance(data['age'], int):
            return False, {
                'valid': False,
                'error': f"age must be an integer, got {type(data['age']).__name__}"
            }
        normalized['age'] = str(data['age'])
        
        # REGRESSION BUG: Strict type checking for balance
        # Previously accepted strings and ints, now only accepts float
        if not isinstance(data['balance'], float):
            return False, {
                'valid': False,
                'error': f"balance must be a float, got {type(data['balance']).__name__}"
            }
        normalized['balance'] = str(data['balance'])
        
        # REGRESSION BUG: Strict type checking for is_active
        # Previously accepted string "true"/"false" and integers, now only accepts bool
        if not isinstance(data['is_active'], bool):
            return False, {
                'valid': False,
                'error': f"is_active must be a boolean, got {type(data['is_active']).__name__}"
            }
        normalized['is_active'] = str(data['is_active'])
        
        return True, {
            'valid': True,
            'normalized_data': normalized
        }


def process_user_data(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process user data through validation and normalization.
    
    Returns validation result with normalized data or error message.
    """
    validator = DataValidator()
    is_valid, result = validator.validate_and_normalize(input_data)
    return result


if __name__ == "__main__":
    # Example usage
    test_input = {
        "user_id": 12345,
        "username": "john_doe",
        "email": "john@example.com",
        "age": 30,
        "balance": 1500.50,
        "is_active": True
    }
    
    result = process_user_data(test_input)
    print(json.dumps(result, indent=2))
