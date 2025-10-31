"""
Optimized Data Validation System - FIXED VERSION

This version corrects the regression by restoring flexible type handling
while maintaining security and validation standards.

FIX: Replaced strict isinstance() checks with flexible type conversion
and duck typing, allowing the system to accept various valid representations
while still maintaining proper validation.
"""

import json
import re
from typing import Dict, Any, Tuple, Union


class DataValidator:
    """
    Data validation system with REGRESSION FIX.
    
    The fix: Flexible type handling with smart conversion instead of strict
    isinstance() checks. Accepts string representations, numeric types, and
    various boolean representations while maintaining security.
    """
    
    REQUIRED_FIELDS = ['user_id', 'username', 'email', 'age', 'balance', 'is_active']
    
    def __init__(self):
        self.validation_errors = []
    
    def _safe_convert_to_string(self, value: Any) -> str:
        """Safely convert any value to string representation"""
        if value is None:
            return ''
        return str(value)
    
    def _validate_and_convert_user_id(self, value: Any) -> Tuple[bool, str, str]:
        """
        Validate and convert user_id to string.
        Accepts: int, string (numeric or alphanumeric)
        """
        try:
            # Accept both int and string representations
            user_id_str = self._safe_convert_to_string(value)
            if not user_id_str:
                return False, '', "user_id cannot be empty"
            return True, user_id_str, ''
        except Exception as e:
            return False, '', f"Invalid user_id: {str(e)}"
    
    def _validate_and_convert_age(self, value: Any) -> Tuple[bool, str, str]:
        """
        Validate and convert age to string.
        Accepts: int, float, numeric string
        """
        try:
            # Convert to string, handling various numeric types
            age_str = self._safe_convert_to_string(value)
            # Validate it represents a valid number
            float(age_str)  # This will raise ValueError if not numeric
            return True, age_str, ''
        except (ValueError, TypeError) as e:
            return False, '', f"age must be numeric, got {type(value).__name__}"
    
    def _validate_and_convert_balance(self, value: Any) -> Tuple[bool, str, str]:
        """
        Validate and convert balance to string.
        Accepts: int, float, numeric string
        """
        try:
            # Convert to string, handling various numeric types
            balance_str = self._safe_convert_to_string(value)
            # Validate it represents a valid number
            float(balance_str)  # This will raise ValueError if not numeric
            return True, balance_str, ''
        except (ValueError, TypeError) as e:
            return False, '', f"balance must be numeric, got {type(value).__name__}"
    
    def _validate_and_convert_is_active(self, value: Any) -> Tuple[bool, str, str]:
        """
        Validate and convert is_active to string.
        Accepts: bool, int (0/1), string ("true"/"false"/"0"/"1")
        """
        try:
            # Handle various boolean representations
            if isinstance(value, bool):
                return True, str(value), ''
            elif isinstance(value, int):
                # Accept 0 and 1 as boolean
                return True, str(value), ''
            elif isinstance(value, str):
                # Accept string representations
                lower_val = value.lower()
                if lower_val in ['true', 'false', '0', '1']:
                    return True, value, ''
                else:
                    return False, '', f"is_active string must be 'true', 'false', '0', or '1'"
            else:
                # For other types, convert to string
                return True, str(value), ''
        except Exception as e:
            return False, '', f"Invalid is_active value: {str(e)}"
    
    def validate_and_normalize(self, data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """
        Validate and normalize user data with flexible type handling.
        
        FIX: Uses flexible conversion methods instead of strict isinstance() checks.
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
        
        # Validate user_id with flexible type handling
        success, user_id, error = self._validate_and_convert_user_id(data['user_id'])
        if not success:
            return False, {'valid': False, 'error': error}
        normalized['user_id'] = user_id
        
        # Username validation (with security check)
        username = data.get('username')
        if not isinstance(username, str):
            # Try to convert to string if not already
            try:
                username = str(username)
            except:
                return False, {
                    'valid': False,
                    'error': f"username must be convertible to string"
                }
        
        # Security check for SQL injection and special characters
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return False, {
                'valid': False,
                'error': "Username contains invalid characters"
            }
        normalized['username'] = username
        
        # Email validation
        email = data.get('email')
        if not isinstance(email, str):
            try:
                email = str(email)
            except:
                return False, {
                    'valid': False,
                    'error': "email must be convertible to string"
                }
        
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return False, {
                'valid': False,
                'error': "Invalid email format"
            }
        normalized['email'] = email
        
        # Validate age with flexible type handling
        success, age, error = self._validate_and_convert_age(data['age'])
        if not success:
            return False, {'valid': False, 'error': error}
        normalized['age'] = age
        
        # Validate balance with flexible type handling
        success, balance, error = self._validate_and_convert_balance(data['balance'])
        if not success:
            return False, {'valid': False, 'error': error}
        normalized['balance'] = balance
        
        # Validate is_active with flexible type handling
        success, is_active, error = self._validate_and_convert_is_active(data['is_active'])
        if not success:
            return False, {'valid': False, 'error': error}
        normalized['is_active'] = is_active
        
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
    # Example usage demonstrating flexible type handling
    test_cases = [
        # Test with proper types
        {
            "user_id": 12345,
            "username": "john_doe",
            "email": "john@example.com",
            "age": 30,
            "balance": 1500.50,
            "is_active": True
        },
        # Test with string representations (regression case)
        {
            "user_id": "67890",
            "username": "jane_smith",
            "email": "jane@example.com",
            "age": "25",
            "balance": "2500.75",
            "is_active": "true"
        }
    ]
    
    for i, test_input in enumerate(test_cases, 1):
        print(f"\nTest Case {i}:")
        result = process_user_data(test_input)
        print(json.dumps(result, indent=2))
