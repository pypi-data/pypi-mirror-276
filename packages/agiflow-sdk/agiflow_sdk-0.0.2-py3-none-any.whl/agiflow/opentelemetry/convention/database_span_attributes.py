from __future__ import annotations

from typing import Optional

from pydantic import Field
from agiflow.opentelemetry.convention.agiflow_attributes import AgiflowSpanAttributesValidator


class DatabaseSpanAttributes():
    SERVER_ADDRESS = 'server.address'
    DB_QUERY = 'db.query'
    DB_RESPONSE = 'db.response'
    DB_OPERATION = 'db.operation'
    DB_SYSTEM = 'db.system'
    DB_NAMESPACE = 'db.namespace'
    DB_INDEX = 'db.index'
    DB_COLLECTION_NAME = 'db.collection.name'
    DB_TOP_K = 'db.top_k'
    DB_EMBEDDING_MODEL = 'db.embedding_model'


class DatabaseSpanAttributesValidator(AgiflowSpanAttributesValidator):
    SERVER_ADDRESS: Optional[str] = Field(None, alias=DatabaseSpanAttributes.SERVER_ADDRESS)
    DB_QUERY: str = Field(..., alias=DatabaseSpanAttributes.DB_QUERY)
    DB_RESPONSE: Optional[str] = Field(None, alias=DatabaseSpanAttributes.DB_RESPONSE)
    DB_OPERATION: Optional[str] = Field(None, alias=DatabaseSpanAttributes.DB_OPERATION)
    DB_SYSTEM: str = Field(..., alias=DatabaseSpanAttributes.DB_SYSTEM)
    DB_NAMESPACE: Optional[str] = Field(None, alias=DatabaseSpanAttributes.DB_NAMESPACE)
    DB_INDEX: Optional[str] = Field(None, alias=DatabaseSpanAttributes.DB_INDEX)
    DB_COLLECTION_NAME: Optional[str] = Field(None, alias=DatabaseSpanAttributes.DB_COLLECTION_NAME)
    DB_TOP_K: Optional[float] = Field(None, alias=DatabaseSpanAttributes.DB_TOP_K)
    DB_EMBEDDING_MODEL: Optional[str] = Field(None, alias=DatabaseSpanAttributes.DB_EMBEDDING_MODEL)
