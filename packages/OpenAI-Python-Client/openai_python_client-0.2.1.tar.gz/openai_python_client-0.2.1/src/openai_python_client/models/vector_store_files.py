from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.vector_store_files_object import VectorStoreFilesObject
from ..models.vector_store_files_status import VectorStoreFilesStatus

if TYPE_CHECKING:
    from ..models.vector_store_files_last_error_type_0 import VectorStoreFilesLastErrorType0


T = TypeVar("T", bound="VectorStoreFiles")


@_attrs_define
class VectorStoreFiles:
    """A list of files attached to a vector store.

    Attributes:
        id (str): The identifier, which can be referenced in API endpoints.
        object_ (VectorStoreFilesObject): The object type, which is always `vector_store.file`.
        usage_bytes (int): The total vector store usage in bytes. Note that this may be different from the original file
            size.
        created_at (int): The Unix timestamp (in seconds) for when the vector store file was created.
        vector_store_id (str): The ID of the [vector store](/docs/api-reference/vector-stores/object) that the
            [File](/docs/api-reference/files) is attached to.
        status (VectorStoreFilesStatus): The status of the vector store file, which can be either `in_progress`,
            `completed`, `cancelled`, or `failed`. The status `completed` indicates that the vector store file is ready for
            use.
        last_error (Union['VectorStoreFilesLastErrorType0', None]): The last error associated with this vector store
            file. Will be `null` if there are no errors.
    """

    id: str
    object_: VectorStoreFilesObject
    usage_bytes: int
    created_at: int
    vector_store_id: str
    status: VectorStoreFilesStatus
    last_error: Union["VectorStoreFilesLastErrorType0", None]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.vector_store_files_last_error_type_0 import VectorStoreFilesLastErrorType0

        id = self.id

        object_ = self.object_.value

        usage_bytes = self.usage_bytes

        created_at = self.created_at

        vector_store_id = self.vector_store_id

        status = self.status.value

        last_error: Union[Dict[str, Any], None]
        if isinstance(self.last_error, VectorStoreFilesLastErrorType0):
            last_error = self.last_error.to_dict()
        else:
            last_error = self.last_error

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "object": object_,
                "usage_bytes": usage_bytes,
                "created_at": created_at,
                "vector_store_id": vector_store_id,
                "status": status,
                "last_error": last_error,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.vector_store_files_last_error_type_0 import VectorStoreFilesLastErrorType0

        d = src_dict.copy()
        id = d.pop("id")

        object_ = VectorStoreFilesObject(d.pop("object"))

        usage_bytes = d.pop("usage_bytes")

        created_at = d.pop("created_at")

        vector_store_id = d.pop("vector_store_id")

        status = VectorStoreFilesStatus(d.pop("status"))

        def _parse_last_error(data: object) -> Union["VectorStoreFilesLastErrorType0", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                last_error_type_0 = VectorStoreFilesLastErrorType0.from_dict(data)

                return last_error_type_0
            except:  # noqa: E722
                pass
            return cast(Union["VectorStoreFilesLastErrorType0", None], data)

        last_error = _parse_last_error(d.pop("last_error"))

        vector_store_files = cls(
            id=id,
            object_=object_,
            usage_bytes=usage_bytes,
            created_at=created_at,
            vector_store_id=vector_store_id,
            status=status,
            last_error=last_error,
        )

        vector_store_files.additional_properties = d
        return vector_store_files

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
