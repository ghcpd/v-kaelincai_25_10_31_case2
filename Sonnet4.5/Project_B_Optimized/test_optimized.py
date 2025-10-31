"""
Test suite for the OPTIMIZED implementation (Project B).

These tests verify that the regression has been fixed and all test cases
now pass correctly with flexible type handling.
"""

import json
import pytest
import sys
from pathlib import Path

# Add parent directory to path to import test_data
sys.path.insert(0, str(Path(__file__).parent.parent))

from optimized_code import process_user_data


def load_test_data():
    """Load test cases from test_data.json"""
    test_data_path = Path(__file__).parent.parent / "test_data.json"
    with open(test_data_path, 'r') as f:
        return json.load(f)


class TestDataValidatorOptimized:
    """Test cases for the optimized implementation with regression fixes"""
    
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
        print(f"✓ Test 1 passed: Normal case handled correctly")
    
    def test_edge_case_numeric_strings(self):
        """
        Test ID 2: REGRESSION FIX VERIFICATION - String representations of numbers
        
        This test verifies the regression is fixed. The optimized version should
        accept string representations of numbers that were rejected in the faulty version.
        """
        test_case = self.test_cases[1]
        result = process_user_data(test_case['input'])
        
        # This test should PASS in the optimized version
        assert result['valid'] == True, f"Expected valid result, got: {result}"
        assert 'normalized_data' in result
        assert result['normalized_data']['user_id'] == test_case['expected_output']['normalized_data']['user_id']
        print(f"✓ Test 2 passed: REGRESSION FIXED - String representations now accepted")
    
    def test_boundary_case_zero_negative(self):
        """Test ID 3: Boundary values - Should pass"""
        test_case = self.test_cases[2]
        result = process_user_data(test_case['input'])
        assert result['valid'] == True
        assert result['normalized_data']['balance'] == test_case['expected_output']['normalized_data']['balance']
        print(f"✓ Test 3 passed: Boundary values handled correctly")
    
    def test_invalid_missing_fields(self):
        """Test ID 4: Invalid input with missing fields - Should fail validation"""
        test_case = self.test_cases[3]
        result = process_user_data(test_case['input'])
        assert result['valid'] == False
        assert 'error' in result
        assert 'Missing required fields' in result['error']
        print(f"✓ Test 4 passed: Missing fields properly rejected")
    
    def test_complex_mixed_types(self):
        """
        Test ID 5: REGRESSION FIX VERIFICATION - Mixed type representations
        
        This test verifies the optimized version handles mixed types gracefully
        (alphanumeric user_id, float age, int balance, int boolean).
        """
        test_case = self.test_cases[4]
        result = process_user_data(test_case['input'])
        
        # This test should PASS in the optimized version
        assert result['valid'] == True, f"Expected valid result, got: {result}"
        assert 'normalized_data' in result
        print(f"✓ Test 5 passed: REGRESSION FIXED - Mixed types now handled correctly")
    
    def test_malformed_invalid_email(self):
        """Test ID 6: Malformed email - Should fail validation"""
        test_case = self.test_cases[5]
        result = process_user_data(test_case['input'])
        assert result['valid'] == False
        assert 'error' in result
        assert 'email' in result['error'].lower()
        print(f"✓ Test 6 passed: Invalid email properly rejected")
    
    def test_security_sql_injection(self):
        """Test ID 7: Security test - SQL injection attempt - Should fail validation"""
        test_case = self.test_cases[6]
        result = process_user_data(test_case['input'])
        assert result['valid'] == False
        assert 'error' in result
        assert 'invalid characters' in result['error'].lower()
        print(f"✓ Test 7 passed: SQL injection attempt blocked")
    
    def test_comprehensive_regression_verification(self):
        """
        Comprehensive test to verify all regression cases are fixed.
        Tests both cases that should pass and cases that should fail.
        """
        passed_tests = 0
        failed_tests = 0
        
        for test_case in self.test_cases:
            result = process_user_data(test_case['input'])
            expected_result = test_case['expected_result']
            
            if expected_result == 'success':
                if result['valid']:
                    passed_tests += 1
                else:
                    failed_tests += 1
                    print(f"⚠ Unexpected failure in test {test_case['test_id']}: {result.get('error')}")
            elif expected_result == 'validation_failure':
                if not result['valid']:
                    passed_tests += 1
                else:
                    failed_tests += 1
                    print(f"⚠ Unexpected pass in test {test_case['test_id']}")
        
        print(f"\nComprehensive test results: {passed_tests} passed, {failed_tests} failed")
        assert failed_tests == 0, f"Some regression tests still failing: {failed_tests}"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
