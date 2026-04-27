from __future__ import annotations

import io
from collections.abc import Sequence
from typing import IO, TYPE_CHECKING, Any, Literal, TypeVar, cast, overload

from aws_lambda_powertools.utilities.streaming._s3_seekable_io import _S3SeekableIO
from aws_lambda_powertools.utilities.streaming.constants import MESSAGE_STREAM_NOT_WRITABLE
from aws_lambda_powertools.utilities.streaming.transformations import (
    CsvTransform,
    GzipTransform,
)
from aws_lambda_powertools.utilities.streaming.types import T

if TYPE_CHECKING:
    from collections.abc import Iterable
    from mmap import mmap

    from mypy_boto3_s3.client import S3Client

    from aws_lambda_powertools.utilities.streaming.transformations.base import BaseTransform

    _CData = TypeVar("_CData")


# Maintenance: almost all this logic should be moved to a base class
class S3Object(IO[bytes]):
    """
    Seekable and streamable S3 Object reader.

    S3Object implements the IO[bytes], backed by a seekable S3 streaming.

    Parameters
    ----------
    bucket: str
        The S3 bucket
    key: str
        The S3 key
    version_id: str, optional
        A version ID of the object, when the S3 bucket is versioned
    boto3_client: S3Client, optional
        An optional boto3 S3 client. If missing, a new one will be created.
    is_gzip: bool, optional
        Enables the Gunzip data transformation
    is_csv: bool, optional
        Enables the CSV data transformation
    sdk_options: dict, optional
        Dictionary of options that will be passed to the S3 Client get_object API call

    Example
    -------

    **Reads a line from an S3, loading as little data as necessary:**

        >>> from aws_lambda_powertools.utilities.streaming import S3Object
        >>>
        >>> line: bytes = S3Object(bucket="bucket", key="key").readline()
        >>>
        >>> print(line)
    """

    def __init__(
        self,
        bucket: str,
        key: str,
        version_id: str | None = None,
        boto3_client: S3Client | None = None,
        is_gzip: bool | None = False,
        is_csv: bool | None = False,
        **sdk_options,
    ):
        self.bucket = bucket
        self.key = key
        self.version_id = version_id

        # The underlying seekable IO, where all the magic happens
        self.raw_stream = _S3SeekableIO(
            bucket=bucket,
            key=key,
            version_id=version_id,
            boto3_client=boto3_client,
            **sdk_options,
        )

        # Stores the list of data transformations
        self._data_transformations: list[BaseTransform] = []
        if is_gzip:
            self._data_transformations.append(GzipTransform())
        if is_csv:
            self._data_transformations.append(CsvTransform())

        # Stores the cached transformed stream
        self._transformed_stream: IO[bytes] | None = None

    @property
    def size(self) -> int:
        """
        Retrieves the size of the underlying S3 object
        """
        pass

    @property
    def transformed_stream(self) -> IO[bytes]:
        """
        Returns a IO[bytes] stream with all the data transformations applied in order
        """
        pass

    @overload
    def transform(self, transformations: BaseTransform[T] | Sequence[BaseTransform[T]], in_place: Literal[True]) -> T:
        pass

    @overload
    def transform(
        self,
        transformations: BaseTransform[T] | Sequence[BaseTransform[T]],
        in_place: Literal[False],
    ) -> None:
        pass

    @overload
    def transform(self, transformations: BaseTransform[T] | Sequence[BaseTransform[T]]) -> T:
        pass

    def transform(
        self,
        transformations: BaseTransform[T] | Sequence[BaseTransform[T]],
        in_place: bool | None = False,
    ) -> T | None:
        """
        Applies one or more data transformations to the stream.

        Parameters
        ----------
        transformations: BaseTransform[T] | Sequence[BaseTransform[T]]
            One or more transformations to apply. Transformations are applied in the same order as they are declared.
        in_place: bool, optional
            Transforms the stream in place, instead of returning a new stream object. Defaults to false.

        Returns
        -------
        T[bound=IO[bytes]], optional
            If in_place is False, returns an IO[bytes] object representing the transformed stream
        """
        # Make transformations always be a sequence to make mypy happy
        if not isinstance(transformations, Sequence):
            transformations = [transformations]

        # Scenario 1: user wants to transform the stream in place.
        # In this case, we store the transformations and invalidate any existing transformed stream.
        # This way, the transformed_stream is re-created on the next IO operation.
        # This can happen when the user calls .transform multiple times before they start reading data
        #
        #   >>> s3object.transform(GzipTransform(), in_place=True)
        #   >>> s3object.seek(0, io.SEEK_SET) <- this creates a transformed stream
        #   >>> s3object.transform(CsvTransform(), in_place=True) <- need to re-create transformed stream
        #   >>> s3object.read...
        if in_place:
            self._data_transformations.extend(transformations)

            # Invalidate any existing transformed stream.
            # It will be created again next time it's accessed.
            self._transformed_stream = None
            return None
        else:
            # Tell mypy that raw_stream actually implements T (bound to IO[bytes])
            stream = cast(T, self.raw_stream)
            for transformation in transformations:
                stream = transformation.transform(stream)
            return stream

    # From this point on, we're just implementing all the standard methods on the IO[bytes] type.
    # There's no magic here, just delegating all the calls to our transformed_stream.
    def seek(self, offset: int, whence: int = io.SEEK_SET) -> int:
        pass

    def seekable(self) -> bool:
        pass

    def readable(self) -> bool:
        pass

    def writable(self) -> bool:
        pass

    def tell(self) -> int:
        pass

    @property
    def closed(self) -> bool:
        pass

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def close(self):
        # Scenario 1: S3Object = SeekableIO, because there are no data transformations applied
        # In this scenario, we can only close the raw_stream. If we tried to also close the transformed_stream we would
        # get an error, since they are the same object, and we can't close the same stream twice.
        pass

    def read(self, size: int = -1) -> bytes:
        return self.transformed_stream.read(size)

    def readline(self, size: int | None = -1) -> bytes:
        return self.transformed_stream.readline()

    def readlines(self, hint: int = -1) -> list[bytes]:
        pass

    def __next__(self):
        return self.transformed_stream.__next__()

    def __iter__(self):
        return self.transformed_stream.__iter__()

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
