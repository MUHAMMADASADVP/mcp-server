"""
Pydantic models for expense tracker
Data Transfer Objects (DTOs)
"""
from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional, List
from datetime import datetime


class ExpenseActionType(str, Enum):
    """Supported actions for expense tracker"""
    CREATE_EXPENSE = "create_expense"
    GET_ALL_EXPENSES = "get_all_expenses"
    GET_EXPENSES_BY_TYPE = "get_expenses_by_type"
    CREATE_TYPE = "create_type"
    GET_ALL_TYPES = "get_all_types"


class ExpenseItemRequest(BaseModel):
    """Input model for creating an expense"""
    
    itemName: str = Field(
        ..., 
        description="Name of the item",
        examples=["Groceries", "Gas", "Utilities"]
    )
    
    itemCost: int = Field(
        ..., 
        description="Cost of the item in cents",
        examples=[5000, 10050]
    )
    
    itemType: str = Field(
        ...,
        description="Type of the item (existing type name)",
        examples=["Food", "Transportation", "Entertainment"]
    )
    
    itemNote: Optional[str] = Field(
        None,
        description="Additional note about the item",
        examples=["Weekly shopping", "Commute"]
    )


class ItemTypeRequest(BaseModel):
    """Input model for creating an item type"""
    
    name: str = Field(
        ..., 
        description="Name of the item type",
        examples=["Food", "Transportation", "Entertainment"]
    )


class ExpenseItemResponse(BaseModel):
    """Response model for an expense item"""
    
    itemId: Optional[int] = None
    itemName: str
    itemCost: int
    itemTypeId: Optional[int] = None
    itemTypeName: Optional[str] = None
    itemCreatedDttm: Optional[str] = None
    itemNote: Optional[str] = None


class ItemTypeResponse(BaseModel):
    """Response model for an item type"""
    
    id: Optional[int] = None
    name: str


class ExpenseTrackerInput(BaseModel):
    """Input model for expense tracker tool"""
    
    action: ExpenseActionType = Field(
        ...,
        description="The action to perform on expense tracker"
    )
    
    itemName: Optional[str] = Field(
        None,
        description="Name of the item (required for create_expense)",
        examples=["Groceries", "Gas"]
    )
    
    itemCost: Optional[int] = Field(
        None,
        description="Cost of the item in cents (required for create_expense)",
        examples=[5000, 10050]
    )
    
    itemType: Optional[str] = Field(
        None,
        description="Type of the item (required for create_expense)",
        examples=["Food", "Transportation"]
    )
    
    itemNote: Optional[str] = Field(
        None,
        description="Additional note about the item (optional)"
    )
    
    typeId: Optional[int] = Field(
        None,
        description="Type ID (required for get_expenses_by_type)"
    )
    
    typeName: Optional[str] = Field(
        None,
        description="Type name (required for create_type)"
    )


class ExpenseTrackerOutput(BaseModel):
    """Output model for expense tracker operations"""
    
    action: str
    success: bool
    message: str
    data: Optional[dict] = None
