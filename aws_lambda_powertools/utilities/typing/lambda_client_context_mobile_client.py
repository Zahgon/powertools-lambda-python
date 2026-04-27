class LambdaClientContextMobileClient:
    """Mobile Client context that's provided to Lambda by the client application."""

    _installation_id: str
    _app_title: str
    _app_version_name: str
    _app_version_code: str
    _app_package_name: str

    @property
    def installation_id(self) -> str:
        pass

    @property
    def app_title(self) -> str:
        pass

    @property
    def app_version_name(self) -> str:
        pass

    @property
    def app_version_code(self) -> str:
        pass

    @property
    def app_package_name(self) -> str:
        pass
