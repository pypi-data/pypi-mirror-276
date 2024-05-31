"""
Classes supporting the management of user credentials and certificates.
"""
from datetime import datetime, timezone
from typing import Optional, Union, TypeVar
from heaobject import root


class Credentials(root.AbstractDesktopObject):
    """
        Stores a user's secrets, passwords, and keys, and makes them available to applications.
    """

    def __init__(self) -> None:
        super().__init__()
        self.__account: str | None = None
        self.__where:str | None = None
        self.__password: str | None = None
        self.__role: str | None = None

    @property  # type: ignore
    def account(self) -> Optional[str]:
        """
        The username or account name.
        """
        return self.__account

    @account.setter  # type: ignore
    def account(self, account: Optional[str]) -> None:
        self.__account = str(account) if account is not None else None

    @property  # type: ignore
    def where(self) -> Optional[str]:
        """
        The hostname, URL, service, or other location of the account.
        """
        return self.__where

    @where.setter  # type: ignore
    def where(self, where: Optional[str]) -> None:
        self.__where = str(where) if where is not None else None

    @property  # type: ignore
    def password(self) -> Optional[str]:
        """
        The account password or secret
        """
        return self.__password

    @password.setter  # type: ignore
    def password(self, password: Optional[str]) -> None:
        self.__password = str(password) if password is not None else None

    @property
    def type_display_name(self) -> str:
        return "Credentials"

    @property
    def role(self) -> str:
        """A role to assume while logged in with these credentials."""
        return self.__role

    @role.setter
    def role(self, role: str):
        self.__role = str(role) if role is not None else None


CredentialTypeVar = TypeVar('CredentialTypeVar', bound=Credentials)


class AWSCredentials(Credentials):
    def __init__(self) -> None:
        super().__init__()
        self.__session_token: Optional[str] = None
        self.__expiration: Optional[str] = None
        self.__temporary = False


    @property  # type: ignore
    def session_token(self) -> Optional[str]:
        """
        The session token.
        """
        return self.__session_token

    @session_token.setter  # type: ignore
    def session_token(self, session_token: Optional[str]):
        self.__session_token = str(session_token) if session_token is not None else None

    @property  # type: ignore
    def expiration(self) -> Optional[str]:
        """
        The session's expiration time.
        """
        return self.__expiration

    @expiration.setter  # type: ignore
    def expiration(self, expiration: Optional[Union[str, datetime]]) -> None:
        exp_formatted = expiration
        if type(exp_formatted) is datetime:
            exp_formatted = exp_formatted.strftime("%Y-%m-%dT%H:%M:%S%z")
        self.__expiration = str(exp_formatted) if exp_formatted is not None else None

    @property
    def temporary(self) -> bool:
        """Whether or not to use AWS' temporary credentials generation mechanism. The default value is False."""
        return self.__temporary

    @temporary.setter
    def temporary(self, temporary: bool):
        self.__temporary = bool(temporary)

    def has_expired(self, exp_diff: int = 0, parse_pattern: Optional[str] = None):
        """
        This function assumes time will be provided in UTC per aws documentation
        and that the expiration time is a datetime str.
        :param exp_diff: the difference between expiration and current time in minutes (default to zero)
        :param parse_pattern: is the pattern to parse for the expiration field (optional)
        :return: a boolean whether the token has expired or not
        :raise Value Error if expiration field cannot be parsed
        """
        parse_pattern = "%Y-%m-%dT%H:%M:%S%z" if not parse_pattern else parse_pattern
        if not self.expiration:
            #if not field not set allow credentials to generated to set it
            return True
        exp = datetime.strptime(self.expiration, parse_pattern)
        diff = exp - datetime.now(timezone.utc)
        return (diff.total_seconds() / 60) < exp_diff

    @property
    def type_display_name(self) -> str:
        return "AWS Credentials"
