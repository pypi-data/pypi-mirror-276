import requests

class LoginException(Exception):
    pass

class Login:
    def __init__(self, username, password, domain):
        self.session = None
        self.username = username
        self.password = password
        self.domain = domain

    def login(self, username=None, password=None):
        response = None
        try:
            if username:
                self.username = username
            if password:
                self.password = password
            login_url = f"{self.domain}/doku.php"
            login_data = {
                "id": "start",
                "do": "login",
                "u": self.username,
                "p": self.password,
            }
            self.session = requests.Session()
            response = self.session.post(login_url, data=login_data, verify=False)
            response.raise_for_status()
            print("Login Successful!")
            self.logged_in = True
            return self
        except Exception as e:
            print(f"Error Logging In: {e}")
            self.logged_in = False
            if response:
                print(response.text)
                print("status: ", response.status_code)
            raise LoginException(
                f"Error Logging In as {self.username} to {self.domain}: {e}"
            )

    def logout(self):
        self.session = None
        self.logged_in = False

    def is_logged_in(self):
        return self.logged_in

    def get_username(self):
        return self.username

    def __enter__(self):
        return self.login()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logout()


# Test the Login Code
if __name__ == "__main__":
    input("Press Enter to test Login...")
    username = input("Enter Username: ")
    password = input("Enter Password: ")

    try:
        with Login(username, password) as login_session:
            if login_session.is_logged_in():
                print(f"Successfully logged in as {login_session.get_username()}")
                # Perform actions using login_session.session
            else:
                print("Login failed")
    except LoginException as e:
        print(e)
