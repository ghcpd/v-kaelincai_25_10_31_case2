"""
Test suite for the FAULTY implementation (Project A).

These tests demonstrate the regression where the strict type checking
breaks previously working functionality.
"""

import json
import pytest
import sys
from pathlib import Path

# Add parent directory to path to import test_data
sys.path.insert(0, str(Path(__file__).parent.parent))

from original_code import process_user_data


def load_test_data():
    """Load test cases from test_data.json"""
    test_data_path = Path(__file__).parent.parent / "test_data.json"
    with open(test_data_path, 'r') as f:
        return json.load(f)


class TestDataValidatorFaulty:
    """Test cases for the faulty implementation showing regression bugs"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup for each test"""
        self.test_cases = load_test_data()
    
    def test_normal_case_valid_data(self):
        """Test ID 1: Normal case with proper types - Should pass"""
        test_case = self.test_cases[0]
        result = process_user_data(test_case['input'])
        assert result['valid'] == True
        assert 'normalized_data' in result
        assert result['normalized_data']['user_id'] == test_case['expected_output']['normalized_data']['user_id']
    
    def test_edge_case_numeric_strings(self):
        """
        Test ID 2: REGRESSION TEST - String representations of numbers
        
        EXPECTED: Should pass (strings are valid input representations)
        ACTUAL IN FAULTY VERSION: Fails due to strict isinstance() checks
        """
        test_case = self.test_cases[1]
        result = process_user_data(test_case['input'])
        
        # This test will FAIL in the faulty version
        # It demonstrates the regression where valid string inputs are rejected
        if result['valid']:
            assert result['normalized_data']['user_id'] == test_case['expected_output']['normalized_data']['user_id']
        else:
            # Document the regression failure
            pytest.fail(f"REGRESSION BUG DETECTED: {result.get('error', 'Unknown error')}")
    
    def test_boundary_case_zero_negative(self):
        """Test ID 3: Boundary values - Should pass"""
        test_case = self.test_cases[2]
        result = process_user_data(test_case['input'])
        assert result['valid'] == True
        assert result['normalized_data']['balance'] == test_case['expected_output']['normalized_data']['balance']
    
    def test_invalid_missing_fields(self):
        """Test ID 4: Invalid input with missing fields - Should fail validation"""
        test_case = self.test_cases[3]
        result = process_user_data(test_case['input'])
        assert result['valid'] == False
        assert 'error' in result
        assert 'Missing required fields' in result['error']
    
    def test_complex_mixed_types(self):
        """
        Test ID 5: REGRESSION TEST - Mixed type representations
        
        EXPECTED: Should pass (flexible type handling)
        ACTUAL IN FAULTY VERSION: Fails due to strict type validation
        """
        test_case = self.test_cases[4]
        result = process_user_data(test_case['input'])
        
        # This test will FAIL in the faulty version
        if result['valid']:
            assert 'normalized_data' in result
        else:
            pytest.fail(f"REGRESSION BUG DETECTED: {result.get('error', 'Unknown error')}")
    
    def test_malformed_invalid_email(self):
        """Test ID 6: Malformed email - Should fail validation"""
        test_case = self.test_cases[5]
        result = process_user_data(test_case['input'])
        assert result['valid'] == False
        assert 'error' in result
        assert 'email' in result['error'].lower()
    
    def test_security_sql_injection(self):
        """Test ID 7: Security test - SQL injection attempt - Should fail validation"""
        test_case = self.test_cases[6]
        result = process_user_data(test_case['input'])
        assert result['valid'] == False
        assert 'error' in result
        assert 'invalid characters' in result['error'].lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
