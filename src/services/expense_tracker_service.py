"""
Expense Tracker service - Business logic layer
Calls the expense tracker REST API
Like Spring's @Service
"""
import httpx
import logging
import boto3
import os
from botocore.exceptions import ClientError
from typing import List, Dict, Any
from ..models.expense_models import (
    ExpenseTrackerInput, 
    ExpenseTrackerOutput,
    ExpenseItemRequest,
    ItemTypeRequest,
    ExpenseActionType
)

logger = logging.getLogger(__name__)

def get_base_url():
    """
    Fetch BASE_URL from AWS Parameter Store
    Falls back to environment variable if needed
    """
    try:
        ssm = boto3.client("ssm", region_name="ap-southeast-2")
        response = ssm.get_parameter(
            Name="/exptrac.backend.url"
        )
        return response["Parameter"]["Value"]
    
    except ClientError as e:
        logger.warning(f"SSM fetch failed, trying env var: {e}")
        return os.getenv("BASE_URL")

class ExpenseTrackerService:
    """Service for expense tracker operations"""
    
    TIMEOUT = 10

    def __init__(self):
        self.BASE_URL = get_base_url()
        logger.info(f"ExpenseTrackerService initialized with BASE_URL={self.BASE_URL}")
    
    def handle_action(self, input_data: ExpenseTrackerInput) -> ExpenseTrackerOutput:
        """
        Handle different expense tracker actions
        Routes to appropriate method based on action type
        """
        try:
            action = input_data.action
            
            if action == ExpenseActionType.CREATE_EXPENSE:
                return self._create_expense(input_data)
            elif action == ExpenseActionType.GET_ALL_EXPENSES:
                return self._get_all_expenses()
            elif action == ExpenseActionType.GET_EXPENSES_BY_TYPE:
                return self._get_expenses_by_type(input_data)
            elif action == ExpenseActionType.CREATE_TYPE:
                return self._create_type(input_data)
            elif action == ExpenseActionType.GET_ALL_TYPES:
                return self._get_all_types()
            else:
                return ExpenseTrackerOutput(
                    action=action.value,
                    success=False,
                    message=f"Unknown action: {action}"
                )
        
        except Exception as e:
            logger.error(f"Error handling action: {e}", exc_info=True)
            raise
    
    def _create_expense(self, input_data: ExpenseTrackerInput) -> ExpenseTrackerOutput:
        """Create a new expense"""
        try:
            # Validate required fields
            if input_data.itemName is None or input_data.itemCost is None or input_data.itemType is None:
                return ExpenseTrackerOutput(
                    action=input_data.action.value,
                    success=False,
                    message="Missing required fields: itemName, itemCost, and itemType"
                )
            
            # Create request payload
            payload = ExpenseItemRequest(
                itemName=input_data.itemName,
                itemCost=input_data.itemCost,
                itemType=input_data.itemType,
                itemNote=input_data.itemNote
            )
            
            # Call API
            response = httpx.post(
                f"{self.BASE_URL}/expenses",
                json=payload.model_dump(exclude_none=True),
                timeout=self.TIMEOUT
            )
            
            if response.status_code in [200, 201]:
                data = response.json()
                logger.info(f"Expense created successfully: {data}")
                return ExpenseTrackerOutput(
                    action=input_data.action.value,
                    success=True,
                    message="Expense created successfully",
                    data=data
                )
            else:
                logger.error(f"API error: {response.status_code} - {response.text}")
                return ExpenseTrackerOutput(
                    action=input_data.action.value,
                    success=False,
                    message=f"Failed to create expense: {response.status_code}"
                )
        
        except httpx.RequestError as e:
            logger.error(f"Request error: {e}")
            return ExpenseTrackerOutput(
                action=input_data.action.value,
                success=False,
                message=f"Network error: {str(e)}"
            )
        except Exception as e:
            logger.error(f"Error creating expense: {e}", exc_info=True)
            raise
    
    def _get_all_expenses(self) -> ExpenseTrackerOutput:
        """Get all expenses"""
        try:
            response = httpx.get(
                f"{self.BASE_URL}/expenses",
                timeout=self.TIMEOUT
            )
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"Retrieved {len(data) if isinstance(data, list) else 1} expenses")
                return ExpenseTrackerOutput(
                    action=ExpenseActionType.GET_ALL_EXPENSES.value,
                    success=True,
                    message="Expenses retrieved successfully",
                    data={"expenses": data} if isinstance(data, list) else {"expenses": [data]}
                )
            else:
                logger.error(f"API error: {response.status_code} - {response.text}")
                return ExpenseTrackerOutput(
                    action=ExpenseActionType.GET_ALL_EXPENSES.value,
                    success=False,
                    message=f"Failed to retrieve expenses: {response.status_code}"
                )
        
        except httpx.RequestError as e:
            logger.error(f"Request error: {e}")
            return ExpenseTrackerOutput(
                action=ExpenseActionType.GET_ALL_EXPENSES.value,
                success=False,
                message=f"Network error: {str(e)}"
            )
        except Exception as e:
            logger.error(f"Error retrieving expenses: {e}", exc_info=True)
            raise
    
    def _get_expenses_by_type(self, input_data: ExpenseTrackerInput) -> ExpenseTrackerOutput:
        """Get expenses by type"""
        try:
            if input_data.typeId is None:
                return ExpenseTrackerOutput(
                    action=input_data.action.value,
                    success=False,
                    message="Missing required field: typeId"
                )
            
            response = httpx.get(
                f"{self.BASE_URL}/expenses/type/{input_data.typeId}",
                timeout=self.TIMEOUT
            )
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"Retrieved expenses for type {input_data.typeId}")
                return ExpenseTrackerOutput(
                    action=input_data.action.value,
                    success=True,
                    message=f"Expenses for type {input_data.typeId} retrieved successfully",
                    data={"expenses": data} if isinstance(data, list) else {"expenses": [data]}
                )
            else:
                logger.error(f"API error: {response.status_code} - {response.text}")
                return ExpenseTrackerOutput(
                    action=input_data.action.value,
                    success=False,
                    message=f"Failed to retrieve expenses: {response.status_code}"
                )
        
        except httpx.RequestError as e:
            logger.error(f"Request error: {e}")
            return ExpenseTrackerOutput(
                action=input_data.action.value,
                success=False,
                message=f"Network error: {str(e)}"
            )
        except Exception as e:
            logger.error(f"Error retrieving expenses by type: {e}", exc_info=True)
            raise
    
    def _create_type(self, input_data: ExpenseTrackerInput) -> ExpenseTrackerOutput:
        """Create a new item type"""
        try:
            if input_data.typeName is None:
                return ExpenseTrackerOutput(
                    action=input_data.action.value,
                    success=False,
                    message="Missing required field: typeName"
                )
            
            payload = ItemTypeRequest(name=input_data.typeName)
            
            response = httpx.post(
                f"{self.BASE_URL}/types",
                json=payload.model_dump(),
                timeout=self.TIMEOUT
            )
            
            if response.status_code in [200, 201]:
                data = response.json()
                logger.info(f"Type created successfully: {data}")
                return ExpenseTrackerOutput(
                    action=input_data.action.value,
                    success=True,
                    message="Type created successfully",
                    data=data
                )
            else:
                logger.error(f"API error: {response.status_code} - {response.text}")
                return ExpenseTrackerOutput(
                    action=input_data.action.value,
                    success=False,
                    message=f"Failed to create type: {response.status_code}"
                )
        
        except httpx.RequestError as e:
            logger.error(f"Request error: {e}")
            return ExpenseTrackerOutput(
                action=input_data.action.value,
                success=False,
                message=f"Network error: {str(e)}"
            )
        except Exception as e:
            logger.error(f"Error creating type: {e}", exc_info=True)
            raise
    
    def _get_all_types(self) -> ExpenseTrackerOutput:
        """Get all item types"""
        try:
            response = httpx.get(
                f"{self.BASE_URL}/types",
                timeout=self.TIMEOUT
            )
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"Retrieved {len(data) if isinstance(data, list) else 1} types")
                return ExpenseTrackerOutput(
                    action=ExpenseActionType.GET_ALL_TYPES.value,
                    success=True,
                    message="Types retrieved successfully",
                    data={"types": data} if isinstance(data, list) else {"types": [data]}
                )
            else:
                logger.error(f"API error: {response.status_code} - {response.text}")
                return ExpenseTrackerOutput(
                    action=ExpenseActionType.GET_ALL_TYPES.value,
                    success=False,
                    message=f"Failed to retrieve types: {response.status_code}"
                )
        
        except httpx.RequestError as e:
            logger.error(f"Request error: {e}")
            return ExpenseTrackerOutput(
                action=ExpenseActionType.GET_ALL_TYPES.value,
                success=False,
                message=f"Network error: {str(e)}"
            )
        except Exception as e:
            logger.error(f"Error retrieving types: {e}", exc_info=True)
            raise
