import re


class InvalidAuthorization(Exception):
    """Exception raised when an invalid authorization occurs."""

    pass


class Users:
    """
    A class to manage users on the DokuWiki platform.

    Attributes:
        DOMAIN (str): The domain URL of the DokuWiki instance.
        STATUS_LIST (list): A list of possible status messages.
        SEC_TOK_REGEX (str): The regular expression to extract the security token.

    Methods:
        __init__(self, context):
            Initializes the Users class with a context.

        _det_payload(self, req, *args, **kwargs):
            Determines the payload for different requests.

        _parse_response(self, text, status):
            Parses the response text based on the status.

        get_user(self, username):
            Retrieves the details of a specific user.

        get_users(self):
            Retrieves the list of all users.

        _get_sec_tok(self):
            Extracts the security token from the user manager page.

        add_user(self, userid, username, password, email, notify=True, groups=["user"]):
            Adds a new user to the DokuWiki.

        delete_user(self, userid):
            Deletes a user from the DokuWiki.
    """

    DOMAIN = "https://wm.swt.ds.usace.army.mil/wiki"
    STATUS_LIST = ["success", "error", "warning"]
    SEC_TOK_REGEX = r'<input type="hidden" name="sectok" value="([^"]+)" />'

    def __init__(self, context):
        """
        Initializes the Users class with a context.

        Args:
            context: The context containing session and other necessary information.
        """
        self.context = context

    def _det_payload(self, req, *args, **kwargs):
        """
        Determines the payload for different requests.

        Args:
            req (str): The type of request (e.g., "add", "export", "delete").
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            dict: The payload dictionary for the request.
        """
        payload = {"page": "usermanager", "do": "admin", "start": "0"}
        if req == "add":
            payload.update(
                {
                    "sectok": self._get_sec_tok(),
                    "login": kwargs.get("userid"),
                    "fullname": kwargs.get("username"),
                    "email": kwargs.get("email"),
                    "do": "register",
                    "save": "1",
                }
            )
        elif req == "export":
            payload.update(
                {
                    "sectok": self._get_sec_tok(),
                    "userid": "",
                    "username": "",
                    "usermail": "",
                    "usergroups": "",
                    "fn[export]": ":",
                    "page": "usermanager",
                }
            )
        elif req == "delete":
            payload.update(
                {
                    "sectok": self._get_sec_tok(),
                    "userid": "",
                    "username": "",
                    "usermail": "",
                    "do": "admin",
                    "usergroups": "",
                    f'delete[{kwargs.get("userid")}]': "on",
                    "fn[delete]": "",
                    "page": "usermanager",
                    "start": "0",
                }
            )
        return payload

    def _parse_response(self, text, status):
        """
        Parses the response text based on the status.

        Args:
            text (str): The response text to be parsed.
            status (str): The status type to parse (e.g., "success", "error").

        Returns:
            str: The parsed response text if found, otherwise False.

        Raises:
            Exception: If the status is invalid or if specific errors are found in the text.
            InvalidAuthorization: If the user lacks admin authorization.
        """
        if status not in self.STATUS_LIST:
            raise Exception(
                f"Invalid Status: {status} - To parse a response you must select from {self.STATUS_LIST}"
            )
        status_tag = f'<div class="{status}">'
        if text.find(status_tag) >= 0:
            if text.find("admins only") >= 0:
                raise InvalidAuthorization(f'You must have "admin" to create users.')
            if text.find("failed deleting") >= 0:
                raise Exception("Failed to delete user.")
            return text.split(status_tag)[1].split("</div>")[0]
        return False

    def get_user(self, username):
        """
        Retrieves the details of a specific user.

        Args:
            username (str): The username of the user to retrieve.

        Returns:
            str: The HTML content of the user's page.

        Raises:
            requests.exceptions.HTTPError: If the request fails.
        """
        user_url = f"{self.DOMAIN}/doku.php?id=user:{username}"
        response = self.context.session.get(user_url)
        response.raise_for_status()
        return response.text

    def get_users(self):
        """
        Retrieves the list of all users.

        Returns:
            list: A list of all users.

        Raises:
            requests.exceptions.HTTPError: If the request fails.
        """
        users_url = f"{self.DOMAIN}/doku.php?id=start"
        response = self.context.session.post(
            users_url,
            headers={
                "Cache-Control": "no-cache",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            data=self._det_payload(req="export"),
        )
        response.raise_for_status()
        file_contents = response.content.decode("utf-8")
        print(file_contents)
        return [u for u in file_contents.split("\n") if u]

    def _get_sec_tok(self):
        """
        Extracts the security token from the user manager page.

        Returns:
            str: The security token.

        Raises:
            Exception: If the security token cannot be extracted.
        """
        response = self.context.session.get(
            f"{self.DOMAIN}/doku.php?id=start&do=admin&page=usermanager"
        )
        with open("sec_tok.html", "w") as f:
            f.write(response.text)
        match = re.search(self.SEC_TOK_REGEX, response.text)
        if match:
            SEC_TOK = match.group(1)
            if not SEC_TOK:
                raise Exception("Failed to get security token!")
            return SEC_TOK
        return False

    def add_user(self, userid, username, password, email, notify=True, groups=["user"]):
        """
        Adds a new user to the DokuWiki.

        Args:
            userid (str): The user ID.
            username (str): The username.
            password (str): The user's password.
            email (str): The user's email.
            notify (bool): Whether to notify the user.
            groups (list): The groups the user belongs to.

        Returns:
            bool: True if the user is added successfully.

        Raises:
            requests.exceptions.HTTPError: If the request fails.
            InvalidAuthorization: If the user lacks admin authorization.
            Exception: If there is an error creating the user.
        """
        print(f"\tCreating user {userid}...")
        response = self.context.session.post(
            f"{self.DOMAIN}/wiki/doku.php?id=start&do=register",
            data=self._det_payload(
                req="add",
                userid=userid,
                username=username,
                password=password,
                email=email,
                notify=notify,
                groups=groups,
            ),
            headers={
                "Cache-Control": "no-cache",
                "Content-Type": "application/x-www-form-urlencoded",
            },
        )
        response.raise_for_status()
        with open("add.html", "w") as f:
            f.write(response.text)
        if self._parse_response(response.text, "error"):
            self.error = response.text.split('<div class="error">')[1].split("</div>")[0]
            if self.error.find("admins only") >= 0:
                raise InvalidAuthorization(f'You must have "admin" to create users.')
            raise Exception(f"Error Creating User: {self.error}")
        print(f"\tDone! User Created!")
        return True

    def delete_user(self, userid):
        """
        Deletes a user from the DokuWiki.

        Args:
            userid (str): The user ID of the user to be deleted.

        Returns:
            bool: True if the user is deleted successfully.

        Raises:
            requests.exceptions.HTTPError: If the request fails.
        """
        print(f"\tDeleting user {userid}...")
        response = self.context.session.post(
            f"{self.DOMAIN}/doku.php?id=start",
            data=self._det_payload(req="delete", userid=userid),
            headers={
                "Cache-Control": "no-cache",
                "Content-Type": "application/x-www-form-urlencoded",
            },
        )
        response.raise_for_status()
        with open("delete.html", "w") as f:
            f.write(response.text)
        self._parse_response(response.text, "success")
        self._parse_response(response.text, "error")
        return True
