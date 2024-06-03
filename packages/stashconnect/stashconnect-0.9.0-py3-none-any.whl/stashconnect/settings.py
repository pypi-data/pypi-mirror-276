class Settings:
    def __init__(self, client):
        self.client = client

    def get_settings(self):
        response = self.client._post("/account/settings", data={})
        return response["settings"]

    def get_me(self):
        response = self.client._post("/users/me", data={})
        return response["user"]

    def get_active_devices(self):
        response = self.client._post("/account/list_active_devices", data={})
        return response["devices"]

    def change_password(self, new_password, old_password):
        data = {"new_password": new_password, "old_password": old_password}
        response = self.client._post("/account/change_password", data=data)
        return response

    def resend_verification_email(self, email):
        response = self.client._post(
            "/register/resend_validation_email", data={"email": email}
        )
        return response

    def change_email(self, email):
        response = self.client._post("/account/change_email", data={"email": email})
        return response

    def get_notifications(self, limit=20, offset=0) -> dict:
        data = {"limit": limit, "offset": offset}
        response = self.client._post("notifications/get", data=data)
        return response["notifications"]

    def get_notification_count(self) -> int:
        response = self.client._post("notifications/count", data={})
        return int(response["count"])
