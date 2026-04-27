from __future__ import annotations

import io
import logging
from typing import IO, TYPE_CHECKING, Any, TypeVar

import boto3

from aws_lambda_powertools.shared import user_agent
from aws_lambda_powertools.utilities.streaming.constants import MESSAGE_STREAM_NOT_WRITABLE

if TYPE_CHECKING:
    from collections.abc import Iterable, Sequence
    from mmap import mmap

    from mypy_boto3_s3.client import S3Client

    from aws_lambda_powertools.utilities.streaming.compat import PowertoolsStreamingBody

    _CData = TypeVar("_CData")

logger = logging.getLogger(__name__)


class _S3SeekableIO(IO[bytes]):
    """
    _S3SeekableIO wraps boto3.StreamingBody to allow for seeking. Seeking is achieved by closing the
    existing connection and re-opening a new one, passing the correct HTTP Range header.

    Parameters
    ----------
    bucket: str
        The S3 bucket
    key: str
        The S3 key
    version_id: str, optional
        A version ID of the object, when the S3 bucket is versioned
    boto3_client: boto3 S3 Client, optional
        An optional boto3 S3 client. If missing, a new one will be created.
    sdk_options: dict, optional
        Dictionary of options that will be passed to the S3 Client get_object API call
    """

    def __init__(
        self,
        bucket: str,
        key: str,
        version_id: str | None = None,
        boto3_client: S3Client | None = None,
        **sdk_options,
    ):
        self.bucket = bucket
        self.key = key

        # Holds the current position in the stream
        self._position = 0

        # Stores the closed state of the stream
        self._closed: bool = False

        # Caches the size of the object
        self._size: int | None = None

        self._s3_client = boto3_client
        self._raw_stream: PowertoolsStreamingBody | None = None

        self._sdk_options = sdk_options
        self._sdk_options["Bucket"] = bucket
        self._sdk_options["Key"] = key
        self._has_user_agent = False
        if version_id is not None:
            self._sdk_options["VersionId"] = version_id

    @property
    def s3_client(self) -> S3Client:
        """
        Returns a boto3 S3 client
        """
        pass

    @property
    def size(self) -> int:
        """
        Retrieves the size of the S3 object
        """
        pass

    @property
    def raw_stream(self) -> PowertoolsStreamingBody:
        """
        Returns the boto3 StreamingBody, starting the stream from the sought position.
        """
        pass

    def seek(self, offset: int, whence: int = io.SEEK_SET) -> int:
        """
        Seeks the current object, invalidating the underlying stream if the position changes.
        """
        pass

    def seekable(self) -> bool:
        pass

    def readable(self) -> bool:
        pass

    def writable(self) -> bool:
        pass

    def tell(self) -> int:
        pass

    def read(self, size: int | None = -1) -> bytes:
        size = None if size == -1 else size
        data = self.raw_stream.read(size)
        if data is not None:
            self._position += len(data)
        return data

    def readline(self, size: int | None = None) -> bytes:
        data = self.raw_stream.readline(size)
        self._position += len(data)
        return data

    def readlines(self, hint: int = -1) -> list[bytes]:
        # boto3's StreamingResponse doesn't implement the "hint" parameter
        pass

    @property
    def closed(self) -> bool:
        pass

    def __next__(self):
        return self.raw_stream.__next__()

    def __iter__(self):
        return self.raw_stream.__iter__()

    def __enter__(self):
        return self

    def __exit__(self, *kwargs):
        self.close()

    def close(self) -> None:
        pass

    def fileno(self) -> int:
        raise NotImplementedError("this stream is not backed by a file descriptor")

    def flush(self) -> None:
        raise NotImplementedError(MESSAGE_STREAM_NOT_WRITABLE)

    def isatty(self) -> bool:
        pass

    def truncate(self, size: int | None = 0) -> int:
        raise NotImplementedError(MESSAGE_STREAM_NOT_WRITABLE)

    def write(self, data: bytes | bytearray | memoryview | Sequence[Any] | mmap | _CData) -> int:
        raise NotImplementedError(MESSAGE_STREAM_NOT_WRITABLE)

    def writelines(
        self,
        data: Iterable[bytes | bytearray | memoryview | Sequence[Any] | mmap | _CData],
    ) -> None:
        raise NotImplementedError(MESSAGE_STREAM_NOT_WRITABLE)
