from typing import Any

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

    host: str = Field(
        default=None,
        description="Databricks host, e.g. uksouth.azuredatabricks.com",
    )
    token: Optional[str] = Field(
        default=None,
        description="Databricks access token",
    )

    def get_client(self) -> DatabricksClient:
        return DatabricksClient(host=self.host, token=self.token)

    def get_object_to_set_on_execution_context(self) -> Any:
        return self.get_client()


@resource(config_schema=DatabricksClientResource.to_config_schema())
def databricks_client(init_context) -> DatabricksClient:
    return DatabricksClientResource.from_resource_context(init_context).get_client()
