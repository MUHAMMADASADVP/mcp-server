"""
Unit tests - like JUnit tests
"""
import pytest
from src.handlers.tool_handler import perform_calculation

def test_addition():
    assert perform_calculation("add", 2, 3) == 5

def test_subtraction():
    assert perform_calculation("subtract", 5, 3) == 2

def test_multiplication():
    assert perform_calculation("multiply", 4, 3) == 12

def test_division():
    assert perform_calculation("divide", 10, 2) == 5

def test_division_by_zero():
    assert perform_calculation("divide", 10, 0) == float('inf')
