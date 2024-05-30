import requests

class Mailbit:
    def __init__(self, api_key, base_url='https://public-api.mailbit.io'):
        if not api_key:
            raise ValueError("API key is required")
        self.api_key = api_key
        self.base_url = base_url

    @staticmethod
    def generate_error_message(code, message):
        return {'code': code, 'message': message}

    def send_email(self, email_data):
        url = f'{self.base_url}/send-email'

        try:
            response = requests.post(url, json=email_data, headers={'token': self.api_key})
            response.raise_for_status()
            data = response.json()
            print('Email sent successfully:', data.get('message'))
            return data
        except requests.exceptions.HTTPError as err:
            if err.response:
                code = err.response.status_code
                message = err.response.json().get('message')
                print(f'Error sending email\nCode: {code}\nMessage: {message}')
                raise ValueError(Mailbit.generate_error_message(code, message))
            else:
                print('Error sending email - General error:', str(err))
                raise ValueError(str(err))
