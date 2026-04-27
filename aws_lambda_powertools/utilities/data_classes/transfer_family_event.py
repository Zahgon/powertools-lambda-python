from __future__ import annotations

import json
from typing import Any, Literal

from aws_lambda_powertools.utilities.data_classes.common import (
    DictWrapper,
)


class TransferFamilyAuthorizer(DictWrapper):
    @property
    def username(self) -> str:
        """The username used for authentication"""
        pass

    @property
    def password(self) -> str | None:
        """
        The password used for authentication.
        None in case customer authenticating with certificates
        """
        pass

    @property
    def protocol(self) -> str:
        """The protocol can be SFTP, FTP or FTPS"""
        pass

    @property
    def server_id(self) -> str:
        """The AWS Transfer Family ServerID"""
        pass

    @property
    def source_ip(self) -> str:
        """The customer IP used for connection"""
        pass


class TransferFamilyAuthorizerResponse:
    def _build_authentication_response(
        self,
        role_arn: str,
        policy: str | None = None,
        home_directory: str | None = None,
        home_directory_details: list[dict] | None = None,
        home_directory_type: Literal["LOGICAL", "PATH"] = "PATH",
        user_gid: int | None = None,
        user_uid: int | None = None,
        public_keys: str | None = None,
    ) -> dict[str, Any]:
        pass

    def build_authentication_response_efs(
        self,
        role_arn: str,
        user_gid: int,
        user_uid: int,
        policy: str | None = None,
        home_directory: str | None = None,
        home_directory_details: list[dict] | None = None,
        home_directory_type: Literal["LOGICAL", "PATH"] = "PATH",
        public_keys: str | None = None,
    ) -> dict[str, Any]:
        """
        Build an authentication response for AWS Transfer Family using EFS (Elastic File System).

        Parameters:
        -----------
        role_arn : str
            The Amazon Resource Name (ARN) of the IAM role.
        user_gid : int
            The group ID of the user.
        user_uid : int
            The user ID.
        policy : str | None, optional
            The IAM policy document. Defaults to None.
        home_directory : str | None, optional
            The home directory path. Required if home_directory_type is "PATH". Defaults to None.
        home_directory_details : dict | None, optional
            Details of the home directory. Required if home_directory_type is "LOGICAL". Defaults to None.
        home_directory_type : Literal["LOGICAL", "PATH"], optional
            The type of home directory. Must be either "LOGICAL" or "PATH". Defaults to "PATH".
        public_keys : str | None, optional
            The public keys associated with the user. Defaults to None.

        Returns:
        --------
        dict[str, Any]
            A dictionary containing the authentication response with various details such as
            role ARN, policy, home directory information, and user details.

        Raises:
        -------
        ValueError
            If an invalid home_directory_type is provided or if required parameters are missing
            for the specified home_directory_type.
        """
        pass

    def build_authentication_response_s3(
        self,
        role_arn: str,
        policy: str | None = None,
        home_directory: str | None = None,
        home_directory_details: list[dict] | None = None,
        home_directory_type: Literal["LOGICAL", "PATH"] = "PATH",
        public_keys: str | None = None,
    ) -> dict[str, Any]:
        """
        Build an authentication response for Amazon S3.

        This method constructs an authentication response tailored for S3 access,
        likely by calling an internal method with the provided parameters.

        Parameters:
        -----------
        role_arn : str
            The Amazon Resource Name (ARN) of the IAM role for S3 access.
        policy : str | None, optional
            The IAM policy document for S3 access. Defaults to None.
        home_directory : str | None, optional
            The home directory path in S3. Required if home_directory_type is "PATH". Defaults to None.
        home_directory_details : dict | None, optional
            Details of the home directory in S3. Required if home_directory_type is "LOGICAL". Defaults to None.
        home_directory_type : Literal["LOGICAL", "PATH"], optional
            The type of home directory in S3. Must be either "LOGICAL" or "PATH". Defaults to "PATH".
        public_keys : str | None, optional
            The public keys associated with the user for S3 access. Defaults to None.

        Returns:
        --------
        dict[str, Any]
            A dictionary containing the authentication response with various details such as
            role ARN, policy, home directory information, and potentially other S3-specific attributes.

        Raises:
        -------
        ValueError
            If an invalid home_directory_type is provided or if required parameters are missing
            for the specified home_directory_type.
        """
        pass
