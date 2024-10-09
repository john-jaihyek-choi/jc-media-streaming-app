"""
Type annotations for dynamodb service ServiceResource

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/service_resource/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_dynamodb.service_resource import DynamoDBServiceResource
    import mypy_boto3_dynamodb.service_resource as dynamodb_resources

    session = Session()
    resource: DynamoDBServiceResource = session.resource("dynamodb")

    my_table: dynamodb_resources.Table = resource.Table(...)
```
"""

import sys
from datetime import datetime
from typing import Iterator, List, Sequence

from boto3.dynamodb.table import BatchWriter
from boto3.resources.base import ResourceMeta, ServiceResource
from boto3.resources.collection import ResourceCollection

from .client import DynamoDBClient
from .literals import TableStatusType
from .type_defs import (
    ArchivalSummaryTypeDef,
    AttributeDefinitionTypeDef,
    BatchGetItemInputServiceResourceBatchGetItemTypeDef,
    BatchGetItemOutputServiceResourceTypeDef,
    BatchWriteItemInputServiceResourceBatchWriteItemTypeDef,
    BatchWriteItemOutputServiceResourceTypeDef,
    BillingModeSummaryTypeDef,
    CreateTableInputServiceResourceCreateTableTypeDef,
    DeleteItemInputTableDeleteItemTypeDef,
    DeleteItemOutputTableTypeDef,
    DeleteTableOutputTypeDef,
    GetItemInputTableGetItemTypeDef,
    GetItemOutputTableTypeDef,
    GlobalSecondaryIndexDescriptionTypeDef,
    KeySchemaElementTypeDef,
    LocalSecondaryIndexDescriptionTypeDef,
    OnDemandThroughputTypeDef,
    ProvisionedThroughputDescriptionTypeDef,
    PutItemInputTablePutItemTypeDef,
    PutItemOutputTableTypeDef,
    QueryInputTableQueryTypeDef,
    QueryOutputTableTypeDef,
    ReplicaDescriptionTypeDef,
    RestoreSummaryTypeDef,
    ScanInputTableScanTypeDef,
    ScanOutputTableTypeDef,
    SSEDescriptionTypeDef,
    StreamSpecificationTypeDef,
    TableClassSummaryTypeDef,
    UpdateItemInputTableUpdateItemTypeDef,
    UpdateItemOutputTableTypeDef,
    UpdateTableInputTableUpdateTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("DynamoDBServiceResource", "Table", "ServiceResourceTablesCollection")


class ServiceResourceTablesCollection(ResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.ServiceResource.tables)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/service_resource/#serviceresourcetablescollection)
    """

    def all(self) -> "ServiceResourceTablesCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.ServiceResource.tables)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/service_resource/#serviceresourcetablescollection)
        """

    def filter(  # type: ignore
        self, *, ExclusiveStartTableName: str = ..., Limit: int = ...
    ) -> "ServiceResourceTablesCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.ServiceResource.tables)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/service_resource/#serviceresourcetablescollection)
        """

    def limit(self, count: int) -> "ServiceResourceTablesCollection":
        """
        Return at most this many Tables.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.ServiceResource.tables)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/service_resource/#serviceresourcetablescollection)
        """

    def page_size(self, count: int) -> "ServiceResourceTablesCollection":
        """
        Fetch at most this many Tables per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.ServiceResource.tables)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/service_resource/#serviceresourcetablescollection)
        """

    def pages(self) -> Iterator[List["Table"]]:
        """
        A generator which yields pages of Tables.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.ServiceResource.tables)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/service_resource/#serviceresourcetablescollection)
        """

    def __iter__(self) -> Iterator["Table"]:
        """
        A generator which yields Tables.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.ServiceResource.tables)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/service_resource/#serviceresourcetablescollection)
        """


class Table(ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.ServiceResource.Table)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/service_resource/#table)
    """

    attribute_definitions: List[AttributeDefinitionTypeDef]
    table_name: str
    key_schema: List[KeySchemaElementTypeDef]
    table_status: TableStatusType
    creation_date_time: datetime
    provisioned_throughput: ProvisionedThroughputDescriptionTypeDef
    table_size_bytes: int
    item_count: int
    table_arn: str
    table_id: str
    billing_mode_summary: BillingModeSummaryTypeDef
    local_secondary_indexes: List[LocalSecondaryIndexDescriptionTypeDef]
    global_secondary_indexes: List[GlobalSecondaryIndexDescriptionTypeDef]
    stream_specification: StreamSpecificationTypeDef
    latest_stream_label: str
    latest_stream_arn: str
    global_table_version: str
    replicas: List[ReplicaDescriptionTypeDef]
    restore_summary: RestoreSummaryTypeDef
    sse_description: SSEDescriptionTypeDef
    archival_summary: ArchivalSummaryTypeDef
    table_class_summary: TableClassSummaryTypeDef
    deletion_protection_enabled: bool
    on_demand_throughput: OnDemandThroughputTypeDef
    name: str
    meta: "DynamoDBResourceMeta"  # type: ignore

    def batch_writer(self, overwrite_by_pkeys: List[str] = ...) -> BatchWriter:
        """
        Create a batch writer object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Table.batch_writer)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/service_resource/#tablebatch_writer-method)
        """

    def delete(self) -> DeleteTableOutputTypeDef:
        """
        The `DeleteTable` operation deletes a table and all of its items.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Table.delete)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/service_resource/#tabledelete-method)
        """

    def delete_item(
        self, **kwargs: Unpack[DeleteItemInputTableDeleteItemTypeDef]
    ) -> DeleteItemOutputTableTypeDef:
        """
        Deletes a single item in a table by primary key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Table.delete_item)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/service_resource/#tabledelete_item-method)
        """

    def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Table.get_available_subresources)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/service_resource/#tableget_available_subresources-method)
        """

    def get_item(
        self, **kwargs: Unpack[GetItemInputTableGetItemTypeDef]
    ) -> GetItemOutputTableTypeDef:
        """
        The `GetItem` operation returns a set of attributes for the item with the given
        primary
        key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Table.get_item)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/service_resource/#tableget_item-method)
        """

    def load(self) -> None:
        """
        Calls :py:meth:`DynamoDB.Client.describe_table` to update the attributes of the
        Table
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Table.load)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/service_resource/#tableload-method)
        """

    def put_item(
        self, **kwargs: Unpack[PutItemInputTablePutItemTypeDef]
    ) -> PutItemOutputTableTypeDef:
        """
        Creates a new item, or replaces an old item with a new item.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Table.put_item)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/service_resource/#tableput_item-method)
        """

    def query(self, **kwargs: Unpack[QueryInputTableQueryTypeDef]) -> QueryOutputTableTypeDef:
        """
        You must provide the name of the partition key attribute and a single value for
        that
        attribute.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Table.query)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/service_resource/#tablequery-method)
        """

    def reload(self) -> None:
        """
        Calls :py:meth:`DynamoDB.Client.describe_table` to update the attributes of the
        Table
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Table.reload)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/service_resource/#tablereload-method)
        """

    def scan(self, **kwargs: Unpack[ScanInputTableScanTypeDef]) -> ScanOutputTableTypeDef:
        """
        The `Scan` operation returns one or more items and item attributes by accessing
        every item in a table or a secondary
        index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Table.scan)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/service_resource/#tablescan-method)
        """

    def update(self, **kwargs: Unpack[UpdateTableInputTableUpdateTypeDef]) -> "_Table":
        """
        Modifies the provisioned throughput settings, global secondary indexes, or
        DynamoDB Streams settings for a given
        table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Table.update)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/service_resource/#tableupdate-method)
        """

    def update_item(
        self, **kwargs: Unpack[UpdateItemInputTableUpdateItemTypeDef]
    ) -> UpdateItemOutputTableTypeDef:
        """
        Edits an existing item's attributes, or adds a new item to the table if it does
        not already
        exist.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Table.update_item)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/service_resource/#tableupdate_item-method)
        """

    def wait_until_exists(self) -> None:
        """
        Waits until this Table is exists.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Table.wait_until_exists)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/service_resource/#tablewait_until_exists-method)
        """

    def wait_until_not_exists(self) -> None:
        """
        Waits until this Table is not exists.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Table.wait_until_not_exists)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/service_resource/#tablewait_until_not_exists-method)
        """


_Table = Table


class DynamoDBResourceMeta(ResourceMeta):
    client: DynamoDBClient


class DynamoDBServiceResource(ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.ServiceResource)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/service_resource/)
    """

    meta: "DynamoDBResourceMeta"  # type: ignore
    tables: ServiceResourceTablesCollection

    def Table(self, name: str) -> "_Table":
        """
        Creates a Table resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.ServiceResource.Table)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/service_resource/#dynamodbserviceresourcetable-method)
        """

    def batch_get_item(
        self, **kwargs: Unpack[BatchGetItemInputServiceResourceBatchGetItemTypeDef]
    ) -> BatchGetItemOutputServiceResourceTypeDef:
        """
        The `BatchGetItem` operation returns the attributes of one or more items from
        one or more
        tables.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.ServiceResource.batch_get_item)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/service_resource/#dynamodbserviceresourcebatch_get_item-method)
        """

    def batch_write_item(
        self, **kwargs: Unpack[BatchWriteItemInputServiceResourceBatchWriteItemTypeDef]
    ) -> BatchWriteItemOutputServiceResourceTypeDef:
        """
        The `BatchWriteItem` operation puts or deletes multiple items in one or more
        tables.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.ServiceResource.batch_write_item)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/service_resource/#dynamodbserviceresourcebatch_write_item-method)
        """

    def create_table(
        self, **kwargs: Unpack[CreateTableInputServiceResourceCreateTableTypeDef]
    ) -> "_Table":
        """
        The `CreateTable` operation adds a new table to your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.ServiceResource.create_table)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/service_resource/#dynamodbserviceresourcecreate_table-method)
        """

    def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.ServiceResource.get_available_subresources)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_dynamodb/service_resource/#dynamodbserviceresourceget_available_subresources-method)
        """
