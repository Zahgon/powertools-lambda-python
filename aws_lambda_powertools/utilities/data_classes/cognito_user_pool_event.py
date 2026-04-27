from __future__ import annotations

from typing import Any

from aws_lambda_powertools.utilities.data_classes.common import DictWrapper


class CallerContext(DictWrapper):
    @property
    def aws_sdk_version(self) -> str:
        """The AWS SDK version number."""
        pass

    @property
    def client_id(self) -> str:
        """The ID of the client associated with the user pool."""
        pass


class BaseTriggerEvent(DictWrapper):
    """Common attributes shared by all User Pool Lambda Trigger Events

    Documentation:
    -------------
    https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-identity-pools-working-with-aws-lambda-triggers.html
    """

    @property
    def version(self) -> str:
        """The version number of your Lambda function."""
        return self["version"]

    @property
    def region(self) -> str:
        """The AWS Region, as an AWSRegion instance."""
        pass

    @property
    def user_pool_id(self) -> str:
        """The user pool ID for the user pool."""
        pass

    @property
    def trigger_source(self) -> str:
        """The name of the event that triggered the Lambda function."""
        pass

    @property
    def user_name(self) -> str:
        """The username of the current user."""
        pass

    @property
    def caller_context(self) -> CallerContext:
        """The caller context"""
        pass


class PreSignUpTriggerEventRequest(DictWrapper):
    @property
    def user_attributes(self) -> dict[str, str]:
        """One or more name-value pairs representing user attributes. The attribute names are the keys."""
        pass

    @property
    def validation_data(self) -> dict[str, str]:
        """One or more name-value pairs containing the validation data in the request to register a user."""
        pass

    @property
    def client_metadata(self) -> dict[str, str]:
        """One or more key-value pairs that you can provide as custom input to the Lambda function
        that you specify for the pre sign-up trigger."""
        pass


class PreSignUpTriggerEventResponse(DictWrapper):
    @property
    def auto_confirm_user(self) -> bool:
        pass

    @auto_confirm_user.setter
    def auto_confirm_user(self, value: bool):
        """Set to true to auto-confirm the user, or false otherwise."""
        pass

    @property
    def auto_verify_email(self) -> bool:
        pass

    @auto_verify_email.setter
    def auto_verify_email(self, value: bool):
        """Set to true to set as verified the email of a user who is signing up, or false otherwise."""
        pass

    @property
    def auto_verify_phone(self) -> bool:
        pass

    @auto_verify_phone.setter
    def auto_verify_phone(self, value: bool):
        """Set to true to set as verified the phone number of a user who is signing up, or false otherwise."""
        pass


class PreSignUpTriggerEvent(BaseTriggerEvent):
    """Pre Sign-up Lambda Trigger

    Notes:
    ----
    `triggerSource` can be one of the following:

    - `PreSignUp_SignUp` Pre sign-up.
    - `PreSignUp_AdminCreateUser` Pre sign-up when an admin creates a new user.
    - `PreSignUp_ExternalProvider` Pre sign-up with external provider

    Documentation:
    -------------
    - https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-pre-sign-up.html
    """

    @property
    def request(self) -> PreSignUpTriggerEventRequest:
        pass

    @property
    def response(self) -> PreSignUpTriggerEventResponse:
        return PreSignUpTriggerEventResponse(self["response"])


class PostConfirmationTriggerEventRequest(DictWrapper):
    @property
    def user_attributes(self) -> dict[str, str]:
        """One or more name-value pairs representing user attributes. The attribute names are the keys."""
        pass

    @property
    def client_metadata(self) -> dict[str, str]:
        """One or more key-value pairs that you can provide as custom input to the Lambda function
        that you specify for the post confirmation trigger."""
        pass


class PostConfirmationTriggerEvent(BaseTriggerEvent):
    """Post Confirmation Lambda Trigger

    Notes:
    ----
    `triggerSource` can be one of the following:

    - `PostConfirmation_ConfirmSignUp` Post sign-up confirmation.
    - `PostConfirmation_ConfirmForgotPassword` Post Forgot Password confirmation.

    Documentation:
    -------------
    - https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-post-confirmation.html
    """

    @property
    def request(self) -> PostConfirmationTriggerEventRequest:
        pass


class UserMigrationTriggerEventRequest(DictWrapper):
    @property
    def password(self) -> str:
        pass

    @property
    def validation_data(self) -> dict[str, str]:
        """One or more name-value pairs containing the validation data in the request to register a user."""
        pass

    @property
    def client_metadata(self) -> dict[str, str]:
        """One or more key-value pairs that you can provide as custom input to the Lambda function
        that you specify for the pre sign-up trigger."""
        pass


class UserMigrationTriggerEventResponse(DictWrapper):
    @property
    def user_attributes(self) -> dict[str, str]:
        pass

    @user_attributes.setter
    def user_attributes(self, value: dict[str, str]):
        """It must contain one or more name-value pairs representing user attributes to be stored in the
        user profile in your user pool. You can include both standard and custom user attributes.
        Custom attributes require the custom: prefix to distinguish them from standard attributes."""
        pass

    @property
    def final_user_status(self) -> str | None:
        pass

    @final_user_status.setter
    def final_user_status(self, value: str):
        """During sign-in, this attribute can be set to CONFIRMED, or not set, to auto-confirm your users and
        allow them to sign in with their previous passwords. This is the simplest experience for the user.

        If this attribute is set to RESET_REQUIRED, the user is required to change his or her password immediately
        after migration at the time of sign-in, and your client app needs to handle the PasswordResetRequiredException
        during the authentication flow."""
        pass

    @property
    def message_action(self) -> str | None:
        pass

    @message_action.setter
    def message_action(self, value: str):
        """This attribute can be set to "SUPPRESS" to suppress the welcome message usually sent by
        Amazon Cognito to new users. If this attribute is not returned, the welcome message will be sent."""
        pass

    @property
    def desired_delivery_mediums(self) -> list[str]:
        pass

    @desired_delivery_mediums.setter
    def desired_delivery_mediums(self, value: list[str]):
        """This attribute can be set to "EMAIL" to send the welcome message by email, or "SMS" to send the
        welcome message by SMS. If this attribute is not returned, the welcome message will be sent by SMS."""
        pass

    @property
    def force_alias_creation(self) -> bool | None:
        pass

    @force_alias_creation.setter
    def force_alias_creation(self, value: bool):
        """If this parameter is set to "true" and the phone number or email address specified in the UserAttributes
        parameter already exists as an alias with a different user, the API call will migrate the alias from the
        previous user to the newly created user. The previous user will no longer be able to log in using that alias.

        If this attribute is set to "false" and the alias exists, the user will not be migrated, and an error is
        returned to the client app.

        If this attribute is not returned, it is assumed to be "false".
        """
        pass

    @property
    def enable_sms_mfa(self) -> bool | None:
        pass

    @enable_sms_mfa.setter
    def enable_sms_mfa(self, value: bool):
        """Set this parameter to "true" to require that your migrated user complete SMS text message multi-factor
        authentication (MFA) to sign in. Your user pool must have MFA enabled. Your user's attributes
        in the request parameters must include a phone number, or else the migration of that user will fail.
        """
        pass


class UserMigrationTriggerEvent(BaseTriggerEvent):
    """Migrate User Lambda Trigger

    Notes:
    ----
    `triggerSource` can be one of the following:

    - `UserMigration_Authentication` User migration at the time of sign in.
    - `UserMigration_ForgotPassword` User migration during forgot-password flow.

    Documentation:
    -------------
    - https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-migrate-user.html
    """

    @property
    def request(self) -> UserMigrationTriggerEventRequest:
        pass

    @property
    def response(self) -> UserMigrationTriggerEventResponse:
        return UserMigrationTriggerEventResponse(self["response"])


class CustomMessageTriggerEventRequest(DictWrapper):
    @property
    def code_parameter(self) -> str:
        """A string for you to use as the placeholder for the verification code in the custom message."""
        pass

    @property
    def link_parameter(self) -> str:
        """A string for you to use as a placeholder for the verification link in the custom message."""
        pass

    @property
    def username_parameter(self) -> str:
        """The username parameter. It is a required request parameter for the admin create user flow."""
        pass

    @property
    def user_attributes(self) -> dict[str, str]:
        """One or more name-value pairs representing user attributes. The attribute names are the keys."""
        pass

    @property
    def client_metadata(self) -> dict[str, str]:
        """One or more key-value pairs that you can provide as custom input to the Lambda function
        that you specify for the pre sign-up trigger."""
        pass


class CustomMessageTriggerEventResponse(DictWrapper):
    @property
    def sms_message(self) -> str:
        pass

    @sms_message.setter
    def sms_message(self, value: str):
        """The custom SMS message to be sent to your users.
        Must include the codeParameter value received in the request."""
        pass

    @property
    def email_message(self) -> str:
        pass

    @email_message.setter
    def email_message(self, value: str):
        """The custom email message to be sent to your users.
        Must include the codeParameter value received in the request."""
        pass

    @property
    def email_subject(self) -> str:
        pass

    @email_subject.setter
    def email_subject(self, value: str):
        """The subject line for the custom message."""
        pass


class CustomMessageTriggerEvent(BaseTriggerEvent):
    """Custom Message Lambda Trigger

    Notes:
    ----
    `triggerSource` can be one of the following:

    - `CustomMessage_SignUp` To send the confirmation code post sign-up.
    - `CustomMessage_AdminCreateUser` To send the temporary password to a new user.
    - `CustomMessage_ResendCode` To resend the confirmation code to an existing user.
    - `CustomMessage_ForgotPassword` To send the confirmation code for Forgot Password request.
    - `CustomMessage_UpdateUserAttribute` When a user's email or phone number is changed, this trigger sends a
       verification code automatically to the user. Cannot be used for other attributes.
    - `CustomMessage_VerifyUserAttribute`  This trigger sends a verification code to the user when they manually
       request it for a new email or phone number.
    - `CustomMessage_Authentication` To send MFA codes during authentication.

    Documentation:
    --------------
    - https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-custom-message.html
    """

    @property
    def request(self) -> CustomMessageTriggerEventRequest:
        pass

    @property
    def response(self) -> CustomMessageTriggerEventResponse:
        return CustomMessageTriggerEventResponse(self["response"])


class PreAuthenticationTriggerEventRequest(DictWrapper):
    @property
    def user_not_found(self) -> bool | None:
        """This boolean is populated when PreventUserExistenceErrors is set to ENABLED for your User Pool client."""
        pass

    @property
    def user_attributes(self) -> dict[str, str]:
        """One or more name-value pairs representing user attributes."""
        pass

    @property
    def validation_data(self) -> dict[str, str]:
        """One or more key-value pairs containing the validation data in the user's sign-in request."""
        pass


class PreAuthenticationTriggerEvent(BaseTriggerEvent):
    """Pre Authentication Lambda Trigger

    Amazon Cognito invokes this trigger when a user attempts to sign in, allowing custom validation
    to accept or deny the authentication request.

    Notes:
    ----
    `triggerSource` can be one of the following:

    - `PreAuthentication_Authentication` Pre authentication.

    Documentation:
    --------------
    - https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-pre-authentication.html
    """

    @property
    def request(self) -> PreAuthenticationTriggerEventRequest:
        """Pre Authentication Request Parameters"""
        pass


class PostAuthenticationTriggerEventRequest(DictWrapper):
    @property
    def new_device_used(self) -> bool:
        """This flag indicates if the user has signed in on a new device.
        It is set only if the remembered devices value of the user pool is set to `Always` or User `Opt-In`."""
        pass

    @property
    def user_attributes(self) -> dict[str, str]:
        """One or more name-value pairs representing user attributes."""
        pass

    @property
    def client_metadata(self) -> dict[str, str]:
        """One or more key-value pairs that you can provide as custom input to the Lambda function
        that you specify for the post authentication trigger."""
        pass


class PostAuthenticationTriggerEvent(BaseTriggerEvent):
    """Post Authentication Lambda Trigger

    Amazon Cognito invokes this trigger after signing in a user, allowing you to add custom logic
    after authentication.

    Notes:
    ----
    `triggerSource` can be one of the following:

    - `PostAuthentication_Authentication` Post authentication.

    Documentation:
    --------------
    - https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-post-authentication.html
    """

    @property
    def request(self) -> PostAuthenticationTriggerEventRequest:
        """Post Authentication Request Parameters"""
        pass


class GroupOverrideDetails(DictWrapper):
    @property
    def groups_to_override(self) -> list[str]:
        """A list of the group names that are associated with the user that the identity token is issued for."""
        pass

    @property
    def iam_roles_to_override(self) -> list[str]:
        """A list of the current IAM roles associated with these groups."""
        pass

    @property
    def preferred_role(self) -> str | None:
        """A string indicating the preferred IAM role."""
        pass


class PreTokenGenerationTriggerEventRequest(DictWrapper):
    @property
    def group_configuration(self) -> GroupOverrideDetails:
        """The input object containing the current group configuration"""
        pass

    @property
    def user_attributes(self) -> dict[str, str]:
        """One or more name-value pairs representing user attributes."""
        pass

    @property
    def client_metadata(self) -> dict[str, str]:
        """One or more key-value pairs that you can provide as custom input to the Lambda function
        that you specify for the pre token generation trigger."""
        pass


class PreTokenGenerationTriggerV2EventRequest(PreTokenGenerationTriggerEventRequest):
    @property
    def scopes(self) -> list[str]:
        """Your user's OAuth 2.0 scopes. The scopes that are present in an access token are
        the user pool standard and custom scopes that your user requested,
        and that you authorized your app client to issue.
        """
        pass


class ClaimsOverrideBase(DictWrapper):
    @property
    def claims_to_add_or_override(self) -> dict[str, str]:
        pass

    @claims_to_add_or_override.setter
    def claims_to_add_or_override(self, value: dict[str, str]):
        """A map of one or more key-value pairs of claims to add or override.
        For group related claims, use groupOverrideDetails instead."""
        pass

    @property
    def claims_to_suppress(self) -> list[str]:
        pass

    @claims_to_suppress.setter
    def claims_to_suppress(self, value: list[str]):
        """A list that contains claims to be suppressed from the identity token."""
        pass


class GroupConfigurationBase(DictWrapper):
    @property
    def group_configuration(self) -> GroupOverrideDetails | None:
        pass

    @group_configuration.setter
    def group_configuration(self, value: dict[str, Any]):
        """The output object containing the current group configuration.

        It includes groupsToOverride, iamRolesToOverride, and preferredRole.

        The groupOverrideDetails object is replaced with the one you provide. If you provide an empty or null
        object in the response, then the groups are suppressed. To leave the existing group configuration
        as is, copy the value of the request's groupConfiguration object to the groupOverrideDetails object
        in the response, and pass it back to the service.
        """
        pass

    def set_group_configuration_groups_to_override(self, value: list[str]):
        """A list of the group names that are associated with the user that the identity token is issued for."""
        pass

    def set_group_configuration_iam_roles_to_override(self, value: list[str]):
        """A list of the current IAM roles associated with these groups."""
        pass

    def set_group_configuration_preferred_role(self, value: str):
        """A string indicating the preferred IAM role."""
        pass


class ClaimsOverrideDetails(ClaimsOverrideBase, GroupConfigurationBase):
    pass


class TokenClaimsAndScopeOverrideDetails(ClaimsOverrideBase):
    @property
    def scopes_to_add(self) -> list[str]:
        pass

    @scopes_to_add.setter
    def scopes_to_add(self, value: list[str]):
        pass

    @property
    def scopes_to_suppress(self) -> list[str]:
        pass

    @scopes_to_suppress.setter
    def scopes_to_suppress(self, value: list[str]):
        pass


class ClaimsAndScopeOverrideDetails(GroupConfigurationBase):
    @property
    def id_token_generation(self) -> TokenClaimsAndScopeOverrideDetails:
        pass

    @id_token_generation.setter
    def id_token_generation(self, value: dict[str, Any]):
        """The output object containing the current id token's claims and scope configuration.

        It includes claimsToAddOrOverride, claimsToSuppress, scopesToAdd and scopesToSupprress.

        The tokenClaimsAndScopeOverrideDetails object is replaced with the one you provide.
        If you provide an empty or null object in the response, then the groups are suppressed.
        To leave the existing group configuration as is, copy the value of the token's object
        to the tokenClaimsAndScopeOverrideDetails object in the response, and pass it back to the service.
        """
        pass

    @property
    def access_token_generation(self) -> TokenClaimsAndScopeOverrideDetails:
        pass

    @access_token_generation.setter
    def access_token_generation(self, value: dict[str, Any]):
        """The output object containing the current access token's claims and scope configuration.

        It includes claimsToAddOrOverride, claimsToSuppress, scopesToAdd and scopesToSupprress.

        The tokenClaimsAndScopeOverrideDetails object is replaced with the one you provide.
        If you provide an empty or null object in the response, then the groups are suppressed.
        To leave the existing group configuration as is, copy the value of the token's object to
        the tokenClaimsAndScopeOverrideDetails object in the response, and pass it back to the service.
        """
        pass


class PreTokenGenerationTriggerEventResponse(DictWrapper):
    @property
    def claims_override_details(self) -> ClaimsOverrideDetails:
        pass


class PreTokenGenerationTriggerV2EventResponse(DictWrapper):
    @property
    def claims_scope_override_details(self) -> ClaimsAndScopeOverrideDetails:
        pass


class PreTokenGenerationTriggerEvent(BaseTriggerEvent):
    """Pre Token Generation Lambda Trigger

    Amazon Cognito invokes this trigger before token generation allowing you to customize identity token claims.

    Notes:
    ----
    `triggerSource` can be one of the following:

    - `TokenGeneration_HostedAuth` Called during authentication from the Amazon Cognito hosted UI sign-in page.
    - `TokenGeneration_Authentication` Called after user authentication flows have completed.
    - `TokenGeneration_NewPasswordChallenge` Called after the user is created by an admin. This flow is invoked
       when the user has to change a temporary password.
    - `TokenGeneration_AuthenticateDevice` Called at the end of the authentication of a user device.
    - `TokenGeneration_RefreshTokens` Called when a user tries to refresh the identity and access tokens.

    Documentation:
    --------------
    - https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-pre-token-generation.html
    """

    @property
    def request(self) -> PreTokenGenerationTriggerEventRequest:
        """Pre Token Generation Request Parameters"""
        pass

    @property
    def response(self) -> PreTokenGenerationTriggerEventResponse:
        """Pre Token Generation Response Parameters"""
        return PreTokenGenerationTriggerEventResponse(self["response"])


class PreTokenGenerationV2TriggerEvent(BaseTriggerEvent):
    """Pre Token Generation Lambda Trigger for the V2 Event

    Amazon Cognito invokes this trigger before token generation allowing you to customize identity token claims.

    Notes:
    ----
    `triggerSource` can be one of the following:

    - `TokenGeneration_HostedAuth` Called during authentication from the Amazon Cognito hosted UI sign-in page.
    - `TokenGeneration_Authentication` Called after user authentication flows have completed.
    - `TokenGeneration_NewPasswordChallenge` Called after the user is created by an admin. This flow is invoked
       when the user has to change a temporary password.
    - `TokenGeneration_AuthenticateDevice` Called at the end of the authentication of a user device.
    - `TokenGeneration_RefreshTokens` Called when a user tries to refresh the identity and access tokens.

    Documentation:
    --------------
    - https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-pre-token-generation.html
    """

    @property
    def request(self) -> PreTokenGenerationTriggerV2EventRequest:
        """Pre Token Generation Request V2 Parameters"""
        pass

    @property
    def response(self) -> PreTokenGenerationTriggerV2EventResponse:
        """Pre Token Generation Response V2 Parameters"""
        return PreTokenGenerationTriggerV2EventResponse(self["response"])


class ChallengeResult(DictWrapper):
    @property
    def challenge_name(self) -> str:
        """The challenge type.

        One of: CUSTOM_CHALLENGE, SRP_A, PASSWORD_VERIFIER, SMS_MFA, DEVICE_SRP_AUTH,
        DEVICE_PASSWORD_VERIFIER, or ADMIN_NO_SRP_AUTH."""
        pass

    @property
    def challenge_result(self) -> bool:
        """Set to true if the user successfully completed the challenge, or false otherwise."""
        pass

    @property
    def challenge_metadata(self) -> str | None:
        """Your name for the custom challenge. Used only if challengeName is CUSTOM_CHALLENGE."""
        pass


class DefineAuthChallengeTriggerEventRequest(DictWrapper):
    @property
    def user_attributes(self) -> dict[str, str]:
        """One or more name-value pairs representing user attributes. The attribute names are the keys."""
        pass

    @property
    def user_not_found(self) -> bool | None:
        """A Boolean that is populated when PreventUserExistenceErrors is set to ENABLED for your user pool client.
        A value of true means that the user id (username, email address, etc.) did not match any existing users."""
        pass

    @property
    def session(self) -> list[ChallengeResult]:
        """An array of ChallengeResult elements, each of which contains the following elements:"""
        pass

    @property
    def client_metadata(self) -> dict[str, str]:
        """One or more key-value pairs that you can provide as custom input to the Lambda function that you specify
        for the defined auth challenge trigger."""
        pass


class DefineAuthChallengeTriggerEventResponse(DictWrapper):
    @property
    def challenge_name(self) -> str:
        pass

    @challenge_name.setter
    def challenge_name(self, value: str):
        """A string containing the name of the next challenge.
        If you want to present a new challenge to your user, specify the challenge name here."""
        pass

    @property
    def fail_authentication(self) -> bool:
        pass

    @fail_authentication.setter
    def fail_authentication(self, value: bool):
        """Set to true if you want to terminate the current authentication process, or false otherwise."""
        pass

    @property
    def issue_tokens(self) -> bool:
        pass

    @issue_tokens.setter
    def issue_tokens(self, value: bool):
        """Set to true if you determine that the user has been sufficiently authenticated by
        completing the challenges, or false otherwise."""
        pass


class DefineAuthChallengeTriggerEvent(BaseTriggerEvent):
    """Define Auth Challenge Lambda Trigger

    Amazon Cognito invokes this trigger to initiate the custom authentication flow.

    Notes:
    ----
    `triggerSource` can be one of the following:

    - `DefineAuthChallenge_Authentication` Define Auth Challenge.

    Documentation:
    --------------
    - https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-define-auth-challenge.html
    """

    @property
    def request(self) -> DefineAuthChallengeTriggerEventRequest:
        """Define Auth Challenge Request Parameters"""
        pass

    @property
    def response(self) -> DefineAuthChallengeTriggerEventResponse:
        """Define Auth Challenge Response Parameters"""
        return DefineAuthChallengeTriggerEventResponse(self["response"])


class CreateAuthChallengeTriggerEventRequest(DictWrapper):
    @property
    def user_attributes(self) -> dict[str, str]:
        """One or more name-value pairs representing user attributes. The attribute names are the keys."""
        pass

    @property
    def user_not_found(self) -> bool | None:
        """This boolean is populated when PreventUserExistenceErrors is set to ENABLED for your User Pool client."""
        pass

    @property
    def challenge_name(self) -> str:
        """The name of the new challenge."""
        pass

    @property
    def session(self) -> list[ChallengeResult]:
        """An array of ChallengeResult elements, each of which contains the following elements:"""
        pass

    @property
    def client_metadata(self) -> dict[str, str]:
        """One or more key-value pairs that you can provide as custom input to the Lambda function that you
        specify for the creation auth challenge trigger."""
        pass


class CreateAuthChallengeTriggerEventResponse(DictWrapper):
    @property
    def public_challenge_parameters(self) -> dict[str, str]:
        pass

    @public_challenge_parameters.setter
    def public_challenge_parameters(self, value: dict[str, str]):
        """One or more key-value pairs for the client app to use in the challenge to be presented to the user.
        This parameter should contain all the necessary information to accurately present the challenge to
        the user."""
        pass

    @property
    def private_challenge_parameters(self) -> dict[str, str]:
        pass

    @private_challenge_parameters.setter
    def private_challenge_parameters(self, value: dict[str, str]):
        """This parameter is only used by the "Verify Auth Challenge" Response Lambda trigger.
        This parameter should contain all the information that is required to validate the user's
        response to the challenge. In other words, the publicChallengeParameters parameter contains the
        question that is presented to the user and privateChallengeParameters contains the valid answers
        for the question."""
        pass

    @property
    def challenge_metadata(self) -> str:
        pass

    @challenge_metadata.setter
    def challenge_metadata(self, value: str):
        """Your name for the custom challenge, if this is a custom challenge."""
        pass


class CreateAuthChallengeTriggerEvent(BaseTriggerEvent):
    """Create Auth Challenge Lambda Trigger

    Amazon Cognito invokes this trigger after Define Auth Challenge if a custom challenge has been
    specified as part of the "Define Auth Challenge" trigger.
    It creates a custom authentication flow.

    Notes:
    ----
    `triggerSource` can be one of the following:

    - `CreateAuthChallenge_Authentication` Create Auth Challenge.

    Documentation:
    --------------
    - https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-create-auth-challenge.html
    """

    @property
    def request(self) -> CreateAuthChallengeTriggerEventRequest:
        """Create Auth Challenge Request Parameters"""
        pass

    @property
    def response(self) -> CreateAuthChallengeTriggerEventResponse:
        """Create Auth Challenge Response Parameters"""
        return CreateAuthChallengeTriggerEventResponse(self["response"])


class VerifyAuthChallengeResponseTriggerEventRequest(DictWrapper):
    @property
    def user_attributes(self) -> dict[str, str]:
        """One or more name-value pairs representing user attributes. The attribute names are the keys."""
        pass

    @property
    def private_challenge_parameters(self) -> dict[str, str]:
        """This parameter comes from the Create Auth Challenge trigger, and is
        compared against a user’s challengeAnswer to determine whether the user passed the challenge."""
        pass

    @property
    def challenge_answer(self) -> Any:
        """The answer from the user's response to the challenge."""
        pass

    @property
    def client_metadata(self) -> dict[str, str]:
        """One or more key-value pairs that you can provide as custom input to the Lambda function that
        you specify for the "Verify Auth Challenge" trigger."""
        pass

    @property
    def user_not_found(self) -> bool | None:
        """This boolean is populated when PreventUserExistenceErrors is set to ENABLED for your User Pool client."""
        pass


class VerifyAuthChallengeResponseTriggerEventResponse(DictWrapper):
    @property
    def answer_correct(self) -> bool:
        pass

    @answer_correct.setter
    def answer_correct(self, value: bool):
        """Set to true if the user has successfully completed the challenge, or false otherwise."""
        pass


class VerifyAuthChallengeResponseTriggerEvent(BaseTriggerEvent):
    """Verify Auth Challenge Response Lambda Trigger

    Amazon Cognito invokes this trigger to verify if the response from the end user for a custom
    Auth Challenge is valid or not.
    It is part of a user pool custom authentication flow.

    Notes:
    ----
    `triggerSource` can be one of the following:

    - `VerifyAuthChallengeResponse_Authentication` Verify Auth Challenge Response.

    Documentation:
    --------------
    - https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-verify-auth-challenge-response.html
    """

    @property
    def request(self) -> VerifyAuthChallengeResponseTriggerEventRequest:
        """Verify Auth Challenge Request Parameters"""
        pass

    @property
    def response(self) -> VerifyAuthChallengeResponseTriggerEventResponse:
        """Verify Auth Challenge Response Parameters"""
        return VerifyAuthChallengeResponseTriggerEventResponse(self["response"])


class CustomEmailSenderTriggerEventRequest(DictWrapper):
    @property
    def type(self) -> str:
        """The request version. For a custom email sender event, the value of this string
        is always customEmailSenderRequestV1.
        """
        pass

    @property
    def code(self) -> str:
        """The encrypted code that your function can decrypt and send to your user."""
        pass

    @property
    def user_attributes(self) -> dict[str, str]:
        """One or more name-value pairs representing user attributes. The attribute names are the keys."""
        pass

    @property
    def client_metadata(self) -> dict[str, str]:
        """One or more key-value pairs that you can provide as custom input to the
        custom email sender Lambda function trigger. To pass this data to your Lambda function,
        you can use the ClientMetadata parameter in the AdminRespondToAuthChallenge and
        RespondToAuthChallenge API actions. Amazon Cognito doesn't include data from the
        ClientMetadata parameter in AdminInitiateAuth and InitiateAuth API operations
        in the request that it passes to the post authentication function.
        """
        pass


class CustomEmailSenderTriggerEvent(BaseTriggerEvent):
    @property
    def request(self) -> CustomEmailSenderTriggerEventRequest:
        """Custom Email Sender Request Parameters"""
        pass


class CustomSMSSenderTriggerEventRequest(DictWrapper):
    @property
    def type(self) -> str:
        """The request version. For a custom SMS sender event, the value of this string is always
        customSMSSenderRequestV1.
        """
        pass

    @property
    def code(self) -> str:
        """The encrypted code that your function can decrypt and send to your user."""
        pass

    @property
    def user_attributes(self) -> dict[str, str]:
        """One or more name-value pairs representing user attributes. The attribute names are the keys."""
        pass

    @property
    def client_metadata(self) -> dict[str, str]:
        """One or more key-value pairs that you can provide as custom input to the
        custom SMS sender Lambda function trigger. To pass this data to your Lambda function,
        you can use the ClientMetadata parameter in the AdminRespondToAuthChallenge and
        RespondToAuthChallenge API actions. Amazon Cognito doesn't include data from the
        ClientMetadata parameter in AdminInitiateAuth and InitiateAuth API operations
        in the request that it passes to the post authentication function.
        """
        pass


class CustomSMSSenderTriggerEvent(BaseTriggerEvent):
    @property
    def request(self) -> CustomSMSSenderTriggerEventRequest:
        """Custom SMS Sender Request Parameters"""
        pass
