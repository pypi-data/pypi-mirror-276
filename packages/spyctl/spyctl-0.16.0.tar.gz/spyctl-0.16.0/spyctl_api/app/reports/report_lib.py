from typing import Any, Literal, Optional, Protocol

from pydantic import BaseModel, Field

STATUSES = Literal["scheduled", "generated", "published", "failed"]
FORMATS = Literal["md", "json", "yaml", "pdf", "html"]


class ReportGenerateInput(BaseModel):
    api_key: str = Field(
        title="API Key to access the backend data apis for the report"
    )
    api_url: str = Field(
        title="API URL to access the backend data apis for the report"
    )
    report_id: str = Field(title="Id of the report to generate")
    report_args: dict[str, str | float | int | bool] = Field(
        title="A dictionary of name/value pair arguments"
    )
    report_format: Optional[FORMATS] = Field(
        default="md", title="Format of the report to generate"
    )
    report_tags: Optional[dict[str, Any]] = Field(
        title="Tags to attach to the report", default={}
    )

    generate_user: Optional[str] = Field(
        title="User who requested the report", default=None
    )


class ReportInput(BaseModel):
    org_uid: str = Field(
        title="Organization Unique Id to generate the report for", default=None
    )
    report_id: str = Field(title="Id of the report to generate")
    report_args: dict[str, str | float | int | bool] = Field(
        title="A dictionary of name/value pair arguments"
    )
    report_tags: Optional[dict[str, Any]] = Field(
        title="Tags to attach to the report", default={}
    )


class ReportSpecArgument(BaseModel):
    name: str = Field(title="Name of the argument")
    short: str = Field(title="Short form description of the argument")
    description: str = Field(title="Description of the argument")
    required: bool = Field(title="Is the argument required")
    type: Literal["cluster", "clustername", "timestamp"] = Field(
        title="Type of the argument"
    )
    default: Optional[Any] = Field(
        title="Suggested default value of the argument", default=None
    )


class ReportSpec(BaseModel):
    id: str = Field(title="Name of the report")
    short: str = Field(title="Short form description of the report")
    description: str = Field(title="Long form description of the report")
    args: list[ReportSpecArgument] = Field(
        title="List of arguments for the report"
    )
    supported_formats: list[FORMATS] = Field(
        title="List of supported formats for the report"
    )


class ReportInventory(BaseModel):
    inventory: list[ReportSpec] = Field(title="List of available reports")


class ReportListInput(BaseModel):
    scheduled_time_from: Optional[float] = Field(
        title="Scheduled time from", default=None
    )
    scheduled_time_to: Optional[float] = Field(
        title="Scheduled time to", default=None
    )
    continuation_token: Optional[str] = Field(
        title="Token to continue the list of reports", default=None
    )
