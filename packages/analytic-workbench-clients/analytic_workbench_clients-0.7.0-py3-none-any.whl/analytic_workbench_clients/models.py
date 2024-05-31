import datetime
import enum
import json
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel as _BaseModel
from pydantic import Field


class State(str, enum.Enum):
    RETRY = "RETRY"
    PREPARING = "PREPARING"
    PENDING = "PENDING"
    WORKING = "WORKING"
    PAWING = "PAWING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    REVOKED = "REVOKED"


class SourceType(str, enum.Enum):
    """Used for object creation in `payload.sourceFileName.sourceType`"""

    ADT = "ADT"
    URL = "URL"
    FILEPATH = "FILEPATH"
    FILESTORE = "FILESTORE"


class BaseModel(_BaseModel):
    def dump(self) -> dict:
        return json.loads(self.json(by_alias=True))


class JobCreateModel(BaseModel):
    userId: UUID
    payload: Dict[str, Any]
    webData: Dict[str, Any] = Field(default_factory=dict)
    datasetReleaseId: Optional[str] = None
    datasetSchemaId: Optional[str] = None
    projectId: Optional[UUID] = None
    publish: bool = False


class JobSubmitModel(BaseModel):
    executionSlug: Optional[str] = Field(default=None, alias="execution_slug")


class JobModel(JobCreateModel):
    id: Optional[UUID] = None
    groupId: Optional[str] = None
    errors: List[Any] = Field(default_factory=list)
    created: Optional[datetime.datetime] = None
    modified: Optional[datetime.datetime] = None
    state: State = Field(State.PENDING)
    status: Dict[str, Any] = Field(default_factory=dict)
    deleted: bool = False
    storeTTL: Optional[int] = None
    methodName: Optional[str] = None
    publications: List[Dict[str, Any]] = Field(default_factory=list)


class TaskStatusModel(BaseModel):
    state: State
    status: Dict[str, Any] = Field(default_factory=dict)


class JobResultPath(BaseModel):
    name: str
    size: int
    mimetype: str


class CacheMemberModel(BaseModel):
    id: UUID = Field(..., alias="guid")
    filename: str
    mimetype: str
    thumbnail: Optional[Dict[str, str]] = None
