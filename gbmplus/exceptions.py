# USER_NAME, USER_PASSWORD or CLIENT_ID error
class UserError(Exception):
    def __init__(self):
        self.message = "User email, password and client_id need to be defined"
        super(UserError, self).__init__(self.message)

    def __repr__(self):
        return self.message

# Authentication error
class AuthenticationError(Exception):
    def __init__(self):
        self.message = "There was an authentication error. Verify that email, password and client_id are correct"
        super(AuthenticationError, self).__init__(self.message)

    def __repr__(self):
        return self.message


# To catch exceptions while making API calls
class APIError(Exception):
    def __init__(self, metadata, response):
        self.response = response
        self.tag = metadata["tags"][0]
        self.operation = metadata["operation"]
        self.status = (
            self.response.status_code
            if self.response is not None and self.response.status_code
            else None
        )
        self.reason = (
            self.response.reason
            if self.response is not None and self.response.reason
            else None
        )
        try:
            self.message = (
                self.response.json()
                if self.response is not None and self.response.json()
                else None
            )
        except ValueError:
            self.message = self.response.content[:100].decode("UTF-8").strip()
            if (
                type(self.message) == str
                and self.status == 404
                and self.reason == "Not Found"
            ):
                self.message += (
                    "404 Not Found"
                )
        super(APIError, self).__init__(
            f"{self.tag}, {self.operation} - {self.status} {self.reason}, {self.message}"
        )

    def __repr__(self):
        return f"{self.tag}, {self.operation} - {self.status} {self.reason}, {self.message}"
    

# Order format error
class OrderFormatError(Exception):
    def __init__(self, message):
        self.message = "There was a formatting error in the order. " + message
        super(OrderFormatError, self).__init__(self.message)

    def __repr__(self):
        return self.message