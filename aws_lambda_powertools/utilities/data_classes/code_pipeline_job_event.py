from __future__ import annotations

import tempfile
import zipfile
from functools import cached_property
from typing import Any
from urllib.parse import unquote_plus

from aws_lambda_powertools.utilities.data_classes.common import DictWrapper


class CodePipelineConfiguration(DictWrapper):
    @property
    def function_name(self) -> str:
        """Function name"""
        pass

    @property
    def user_parameters(self) -> str | None:
        """User parameters"""
        pass

    @cached_property
    def decoded_user_parameters(self) -> dict[str, Any]:
        """Json Decoded user parameters"""
        pass


class CodePipelineActionConfiguration(DictWrapper):
    """CodePipeline Action Configuration"""

    @property
    def configuration(self) -> CodePipelineConfiguration:
        pass


class CodePipelineS3Location(DictWrapper):
    @property
    def bucket_name(self) -> str:
        pass

    @property
    def key(self) -> str:
        """Raw S3 object key"""
        pass

    @property
    def object_key(self) -> str:
        """Unquote plus of the S3 object key"""
        pass


class CodePipelineLocation(DictWrapper):
    @property
    def get_type(self) -> str:
        """Location type eg: S3"""
        pass

    @property
    def s3_location(self) -> CodePipelineS3Location:
        """S3 location"""
        pass


class CodePipelineArtifact(DictWrapper):
    @property
    def name(self) -> str:
        """Name"""
        pass

    @property
    def revision(self) -> str | None:
        pass

    @property
    def location(self) -> CodePipelineLocation:
        pass


class CodePipelineArtifactCredentials(DictWrapper):
    _sensitive_properties = ["secret_access_key", "session_token"]

    @property
    def access_key_id(self) -> str:
        pass

    @property
    def secret_access_key(self) -> str:
        pass

    @property
    def session_token(self) -> str:
        pass

    @property
    def expiration_time(self) -> int | None:
        pass


class CodePipelineEncryptionKey(DictWrapper):
    @property
    def get_id(self) -> str:
        pass

    @property
    def get_type(self) -> str:
        pass


class CodePipelineData(DictWrapper):
    """CodePipeline Job Data"""

    @property
    def action_configuration(self) -> CodePipelineActionConfiguration:
        """CodePipeline action configuration"""
        pass

    @property
    def input_artifacts(self) -> list[CodePipelineArtifact]:
        """Represents a CodePipeline input artifact"""
        pass

    @property
    def output_artifacts(self) -> list[CodePipelineArtifact]:
        """Represents a CodePipeline output artifact"""
        pass

    @property
    def artifact_credentials(self) -> CodePipelineArtifactCredentials:
        """Represents a CodePipeline artifact credentials"""
        pass

    @property
    def continuation_token(self) -> str | None:
        """A continuation token if continuing job"""
        pass

    @property
    def encryption_key(self) -> CodePipelineEncryptionKey | None:
        """Represents a CodePipeline encryption key"""
        pass


class CodePipelineJobEvent(DictWrapper):
    """AWS CodePipeline Job Event

    Documentation:
    -------------
    - https://docs.aws.amazon.com/codepipeline/latest/userguide/actions-invoke-lambda-function.html
    - https://docs.aws.amazon.com/lambda/latest/dg/services-codepipeline.html
    """

    def __init__(self, data: dict[str, Any]):
        super().__init__(data)
        self._job = self["CodePipeline.job"]

    @property
    def get_id(self) -> str:
        """Job id"""
        pass

    @property
    def account_id(self) -> str:
        """Account id"""
        pass

    @property
    def data(self) -> CodePipelineData:
        """Code pipeline jab data"""
        pass

    @property
    def user_parameters(self) -> str | None:
        """Action configuration user parameters"""
        pass

    @property
    def decoded_user_parameters(self) -> dict[str, Any]:
        """Json Decoded action configuration user parameters"""
        pass

    @property
    def input_bucket_name(self) -> str:
        """Get the first input artifact bucket name"""
        pass

    @property
    def input_object_key(self) -> str:
        """Get the first input artifact order key unquote plus"""
        pass

    def setup_s3_client(self):
        """Creates an S3 client

        Uses the credentials passed in the event by CodePipeline. These
        credentials can be used to access the artifact bucket.

        Returns
        -------
        BaseClient
            An S3 client with the appropriate credentials
        """
        pass

    def find_input_artifact(self, artifact_name: str) -> CodePipelineArtifact | None:
        """Find an input artifact by artifact name

        Parameters
        ----------
        artifact_name : str
            The name of the input artifact to look for

        Returns
        -------
        CodePipelineArtifact, None
            Matching CodePipelineArtifact if found
        """
        pass

    def find_output_artifact(self, artifact_name: str) -> CodePipelineArtifact | None:
        """Find an output artifact by artifact name

        Parameters
        ----------
        artifact_name : str
            The name of the output artifact to look for

        Returns
        -------
        CodePipelineArtifact, None
            Matching CodePipelineArtifact if found
        """
        pass

    def get_artifact(self, artifact_name: str, filename: str | None = None) -> str | None:
        """Get a file within an artifact zip on s3

        Parameters
        ----------
        artifact_name : str
            Name of the S3 artifact to download
        filename : str
            The file name within the artifact zip to extract as a string
            If None, this will return the raw object body.

        Returns
        -------
        str, None
            Returns the contents file contents as a string
        """
        pass

    def put_artifact(self, artifact_name: str, body: Any, content_type: str) -> None:
        """Writes an object to an s3 output artifact.

        Parameters
        ----------
        artifact_name : str
            Name of the S3 artifact to upload
        body: Any
            The data to be written. Binary files should use io.BytesIO.
        content_type: str
            The content type of the data.

        Returns
        -------
        None
        """
        pass
