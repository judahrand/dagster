from typing import Any, Optional

from dagster import (
    ConfigurableResource,
    IAttachDifferentObjectToOpContext,
    resource,
)
from pydantic import Field

from .databricks import DatabricksClient


class DatabricksClientResource(ConfigurableResource, IAttachDifferentObjectToOpContext):
    """Resource which provides a Python client for interacting with Databricks within an
    op or asset.
    """

    host: str = Field(description="Databricks host, e.g. uksouth.azuredatabricks.com")
    token: str = Field(description="Databricks access token")
    workspace_id: Optional[str] = Field(
        default=None,
        description=(
            "DEPRECATED: The Databricks workspace ID, as described in"
            " https://docs.databricks.com/workspace/workspace-details.html#workspace-instance-names-urls-and-ids."
            " This is no longer used and will be removed in a future release."
        ),
    )
    legacy_api: bool = Field(
        default=True, description="Whether to use the legacy `databricks_cli` API"
    )

    def get_client(self) -> DatabricksClient:
        return DatabricksClient(
            host=self.host,
            token=self.token,
            workspace_id=self.workspace_id,
            legacy_api=self.legacy_api,
        )

    def get_object_to_set_on_execution_context(self) -> Any:
        return self.get_client()


@resource(config_schema=DatabricksClientResource.to_config_schema())
def databricks_client(init_context) -> DatabricksClient:
    return DatabricksClientResource.from_resource_context(init_context).get_client()
