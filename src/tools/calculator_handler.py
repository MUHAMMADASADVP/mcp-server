"""
Calculator tool handler
Like Spring's @RestController
"""
from . import AbstractToolHandler
# Use package-relative imports to reference sibling packages under `src`
from ..services.calculator_service import CalculatorService
from ..models.calculator_models import CalculatorInput
from mcp.types import Tool, TextContent
from typing import List
import logging
import json

logger = logging.getLogger(__name__)

class CalculatorToolHandler(AbstractToolHandler):
    """
    Handler for calculator tool
    Manages request/response flow
    """
    
    def __init__(self):
        self.service = CalculatorService()
        logger.info("CalculatorToolHandler initialized")
    
    def get_name(self) -> str:
        """Return tool name"""
        return "calculate"
    
    def get_tool_definition(self) -> Tool:
        """Return tool metadata and schema"""
        # Generate JSON schema from Pydantic model
        schema = CalculatorInput.model_json_schema()
        
        # Debug: log the schema
        logger.debug(f"Calculator tool schema:\n{json.dumps(schema, indent=2)}")
        
        return Tool(
            name=self.get_name(),
            description=(
                "Perform basic arithmetic operations: addition, subtraction, "
                "multiplication, division, power, and modulo. "
                "Supports decimal precision control."
            ),
            inputSchema=schema
        )
    
    async def execute(self, arguments: dict) -> List[TextContent]:
        """
        Execute calculator operation
        Controller layer - handles request/response
        """
        try:
            # Validate input (like @Valid in Spring)
            logger.info(f"Received calculation request: {arguments}")
            input_data = CalculatorInput(**arguments)
            
            # Delegate to service layer
            result = self.service.calculate(input_data)
            
            # Format response
            response_text = self._format_response(result)
            
            logger.info(f"Calculation successful: {result.formatted_result}")
            
            return [TextContent(
                type="text",
                text=response_text
            )]
        
        except ValueError as e:
            # Validation errors from Pydantic
            logger.error(f"Validation error: {e}")
            return [TextContent(
                type="text",
                text=f"❌ Validation Error: {str(e)}"
            )]
        
        except ZeroDivisionError as e:
            logger.error(f"Division by zero: {e}")
            return [TextContent(
                type="text",
                text="❌ Error: Cannot divide by zero"
            )]
        
        except Exception as e:
            # Unexpected errors
            logger.error(f"Unexpected error: {e}", exc_info=True)
            return [TextContent(
                type="text",
                text=f"❌ Internal Error: {str(e)}"
            )]
    
    def _format_response(self, result) -> str:
        """Format the calculation result for display"""
        return f"""✅ Calculation Result:

{result.formatted_result}

Details:
- Operation: {result.operation}
- First Number: {result.operand_a}
- Second Number: {result.operand_b}
- Result: {result.result}"""