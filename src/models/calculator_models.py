"""
Pydantic models for calculator tool
Data Transfer Objects (DTOs)
"""
from pydantic import BaseModel, Field, validator
from enum import Enum
from typing import Optional

class Operation(str, Enum):
    """Supported arithmetic operations"""
    ADD = "add"
    SUBTRACT = "subtract"
    MULTIPLY = "multiply"
    DIVIDE = "divide"
    POWER = "power"
    MODULO = "modulo"

class CalculatorInput(BaseModel):
    """Input model for calculator operations"""
    
    operation: Operation = Field(
        ..., 
        description="The arithmetic operation to perform"
    )
    
    a: float = Field(
        ..., 
        description="First operand (number)",
        examples=[10.5, 5, -3.14]
    )
    
    b: float = Field(
        ..., 
        description="Second operand (number)",
        examples=[2.5, 3, 7]
    )
    
    precision: Optional[int] = Field(
        2,
        description="Number of decimal places in result (0-10)",
        ge=0,
        le=10
    )
    
    @validator('b')
    def validate_division_by_zero(cls, v, values):
        """Prevent division by zero"""
        operation = values.get('operation')
        if operation == Operation.DIVIDE and v == 0:
            raise ValueError("Cannot divide by zero")
        if operation == Operation.MODULO and v == 0:
            raise ValueError("Cannot perform modulo with zero divisor")
        return v
    
    @validator('b')
    def validate_power_limits(cls, v, values):
        """Prevent extremely large power operations"""
        operation = values.get('operation')
        a = values.get('a', 0)
        if operation == Operation.POWER:
            if abs(a) > 1000 or abs(v) > 1000:
                raise ValueError("Power operation limited to bases and exponents within ±1000")
        return v
    
    class Config:
        """Pydantic configuration"""
        schema_extra = {
            "examples": [
                {
                    "operation": "add",
                    "a": 10.5,
                    "b": 5.3,
                    "precision": 2
                },
                {
                    "operation": "multiply",
                    "a": 7,
                    "b": 8,
                    "precision": 0
                },
                {
                    "operation": "divide",
                    "a": 100,
                    "b": 3,
                    "precision": 4
                }
            ]
        }

class CalculatorOutput(BaseModel):
    """Output model for calculator results"""
    
    operation: str = Field(..., description="Operation performed")
    operand_a: float = Field(..., description="First operand")
    operand_b: float = Field(..., description="Second operand")
    result: float = Field(..., description="Calculation result")
    formatted_result: str = Field(..., description="Human-readable result")
    expression: str = Field(..., description="Mathematical expression")