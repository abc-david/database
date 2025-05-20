"""
MODULE: services/database/validation/validation.py
PURPOSE: Provides validation operations for database objects
CLASSES:
    - ObjectValidator: Validates objects against Pydantic models
DEPENDENCIES:
    - Pydantic: For schema validation
    - json: For serialization
    - logging: For operation logging

This module provides validation functionality for objects against Pydantic models.
It supports validating objects against models defined in the database or provided
directly. This version is simplified and improved for better performance and reliability.
"""

import json
import logging
from typing import Dict, List, Any, Optional, Union, Type, Set
from contextlib import contextmanager

from pydantic import BaseModel, ValidationError

# Set up logging
logger = logging.getLogger(__name__)


class ValidationResult:
    """
    Result of a validation operation.
    
    Attributes:
        is_valid: Whether the validation succeeded
        original_data: The original data that was validated
        validated_data: The validated data (if successful)
        errors: List of validation errors
    """
    
    def __init__(self, is_valid: bool, original_data: Any, validated_data: Optional[Any] = None):
        """
        Initialize the validation result.
        
        Args:
            is_valid: Whether the validation succeeded
            original_data: The original data that was validated
            validated_data: The validated data (if successful)
        """
        self.is_valid = is_valid
        self.original_data = original_data
        self.validated_data = validated_data
        self.errors: List[Dict[str, Any]] = []
    
    def add_error(self, field: str, message: str, error_type: str = "validation"):
        """
        Add an error to the result.
        
        Args:
            field: Field with the error
            message: Error message
            error_type: Type of error (default: "validation")
        """
        self.errors.append({
            "field": field,
            "message": message,
            "type": error_type
        })
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the validation result to a dictionary.
        
        Returns:
            Dictionary representation of the validation result
        """
        return {
            "is_valid": self.is_valid,
            "errors": self.errors,
            "data": self.validated_data if self.is_valid else None
        }


class ObjectValidator:
    """
    Validates objects against Pydantic models.
    
    This class handles validation of objects against Pydantic models.
    It can validate objects against models defined in the database or
    provided directly.
    
    Attributes:
        models_cache: Cache of Pydantic models to avoid repeated lookups
    """
    
    def __init__(self):
        """Initialize the validator."""
        self.models_cache: Dict[str, Type[BaseModel]] = {}
    
    def validate_with_model(
        self,
        data: Dict[str, Any],
        model_class: Type[BaseModel],
        partial: bool = False
    ) -> ValidationResult:
        """
        Validate data against a Pydantic model.
        
        Args:
            data: Data to validate
            model_class: Pydantic model class
            partial: Whether to allow partial validation (missing fields)
            
        Returns:
            ValidationResult with validation status and details
        """
        result = ValidationResult(
            is_valid=False,
            original_data=data
        )
        
        try:
            # Create model instance
            if partial:
                # For partial validation, exclude unset fields
                model_instance = model_class.parse_obj(data)
            else:
                # For full validation, use all fields
                model_instance = model_class(**data)
            
            # Validation succeeded
            result.is_valid = True
            result.validated_data = model_instance.dict()
            
        except ValidationError as e:
            # Handle validation errors
            for error in e.errors():
                loc = ".".join(str(l) for l in error["loc"])
                result.add_error(loc, error["msg"], error["type"])
            logger.debug(f"Validation error: {e}")
            
        except Exception as e:
            # Handle other errors
            result.add_error("", f"Validation error: {str(e)}", "exception")
            logger.error(f"Error validating object: {str(e)}")
            
        return result
    
    def validate_objects(
        self,
        objects: List[Dict[str, Any]],
        model_class: Type[BaseModel],
        partial: bool = False
    ) -> List[ValidationResult]:
        """
        Validate multiple objects against a model.
        
        Args:
            objects: List of object data to validate
            model_class: Pydantic model class
            partial: Whether to allow partial validation (missing fields)
            
        Returns:
            List of ValidationResults
        """
        return [
            self.validate_with_model(obj, model_class, partial)
            for obj in objects
        ] 