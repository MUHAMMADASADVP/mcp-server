"""
Calculator service - Business logic layer
Like Spring's @Service
"""
from ..models.calculator_models import CalculatorInput, CalculatorOutput, Operation
import logging
import math

logger = logging.getLogger(__name__)

class CalculatorService:
    """Service for arithmetic calculations"""
    
    def __init__(self):
        logger.info("CalculatorService initialized")
    
    def calculate(self, input_data: CalculatorInput) -> CalculatorOutput:
        """
        Perform calculation based on operation
        Main business logic method
        """
        try:
            # Map operations to functions
            operations = {
                Operation.ADD: self._add,
                Operation.SUBTRACT: self._subtract,
                Operation.MULTIPLY: self._multiply,
                Operation.DIVIDE: self._divide,
                Operation.POWER: self._power,
                Operation.MODULO: self._modulo
            }
            
            # Execute operation
            operation_func = operations[input_data.operation]
            result = operation_func(input_data.a, input_data.b)
            
            # Round to specified precision
            rounded_result = round(result, input_data.precision)
            
            # Get operation symbol
            symbol = self._get_operation_symbol(input_data.operation)
            
            # Create expression
            expression = f"{input_data.a} {symbol} {input_data.b}"
            formatted_result = f"{expression} = {rounded_result}"
            
            logger.info(f"Calculated: {formatted_result}")
            
            return CalculatorOutput(
                operation=input_data.operation.value,
                operand_a=input_data.a,
                operand_b=input_data.b,
                result=rounded_result,
                formatted_result=formatted_result,
                expression=expression
            )
        
        except Exception as e:
            logger.error(f"Calculation error: {e}", exc_info=True)
            raise
    
    def _add(self, a: float, b: float) -> float:
        """Addition operation"""
        return a + b
    
    def _subtract(self, a: float, b: float) -> float:
        """Subtraction operation"""
        return a - b
    
    def _multiply(self, a: float, b: float) -> float:
        """Multiplication operation"""
        return a * b
    
    def _divide(self, a: float, b: float) -> float:
        """Division operation"""
        # Division by zero already validated in model
        return a / b
    
    def _power(self, a: float, b: float) -> float:
        """Power operation (a^b)"""
        return math.pow(a, b)
    
    def _modulo(self, a: float, b: float) -> float:
        """Modulo operation (remainder)"""
        return a % b
    
    def _get_operation_symbol(self, operation: Operation) -> str:
        """Get mathematical symbol for operation"""
        symbols = {
            Operation.ADD: "+",
            Operation.SUBTRACT: "-",
            Operation.MULTIPLY: "×",
            Operation.DIVIDE: "÷",
            Operation.POWER: "^",
            Operation.MODULO: "%"
        }
        return symbols.get(operation, "?")