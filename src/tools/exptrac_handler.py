"""
Expense Tracker tool handler
Manages request/response flow for expense tracker operations
Like Spring's @RestController
"""
from . import AbstractToolHandler
from ..services.expense_tracker_service import ExpenseTrackerService
from ..models.expense_models import ExpenseTrackerInput, ExpenseActionType
from mcp.types import Tool, TextContent
from typing import List
import logging
import json

logger = logging.getLogger(__name__)


class ExpenseTrackerToolHandler(AbstractToolHandler):
    """
    Handler for expense tracker tool
    Manages request/response flow for expense operations
    """
    
    def __init__(self):
        self.service = ExpenseTrackerService()
        logger.info("ExpenseTrackerToolHandler initialized")
    
    def get_name(self) -> str:
        """Return tool name"""
        return "expense_tracker"
    
    def get_tool_definition(self) -> Tool:
        """Return tool metadata and schema"""
        # Generate JSON schema from Pydantic model
        schema = ExpenseTrackerInput.model_json_schema()
        
        # Debug: log the schema
        logger.debug(f"Expense tracker tool schema:\n{json.dumps(schema, indent=2)}")
        
        return Tool(
            name=self.get_name(),
            description=(
                "Manage expenses and expense types. Supports creating expenses, "
                "retrieving all expenses, filtering expenses by type, creating "
                "expense types, and retrieving all types. "
                "Actions: create_expense, get_all_expenses, get_expenses_by_type, "
                "create_type, get_all_types"
            ),
            inputSchema=schema
        )
    
    async def execute(self, arguments: dict) -> List[TextContent]:
        """
        Execute expense tracker operation
        Controller layer - handles request/response
        """
        try:
            # Validate input
            logger.info(f"Received expense tracker request: {arguments}")
            input_data = ExpenseTrackerInput(**arguments)
            
            # Delegate to service layer
            result = self.service.handle_action(input_data)
            
            # Format response
            response_text = self._format_response(result)
            
            logger.info(f"Expense tracker operation successful: {result.message}")
            
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
        
        except Exception as e:
            # Unexpected errors
            logger.error(f"Unexpected error: {e}", exc_info=True)
            return [TextContent(
                type="text",
                text=f"❌ Internal Error: {str(e)}"
            )]
    
    def _format_response(self, result) -> str:
        """Format the operation result for display"""
        status_icon = "✅" if result.success else "❌"
        
        response = f"{status_icon} {result.message}\n\n"
        
        if result.data:
            response += "Data:\n```json\n"
            response += json.dumps(result.data, indent=2)
            response += "\n```"
        
        return response
