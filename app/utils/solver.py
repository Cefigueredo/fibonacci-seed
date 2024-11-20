from datetime import datetime as dt

import db_gateway  # type: ignore
import settings  # type: ignore
from utils import email_sender  # type: ignore


class Solver:
    def solve(self, datetime: dt | None = None):
        if not datetime:
            datetime = dt.now()

        minutes = datetime.minute
        seconds = datetime.second

        second_digit = minutes % 10
        first_digit = minutes // 10

        db = db_gateway.DBGateway()

        result = self._fibonacci(first_digit, second_digit, seconds)

        db.insert_fibonacci(datetime, result)

        if settings.Settings.ENVIRONMENT == "testing":
            return result
        else:
            self._send_email(datetime, result)

        return result

    def _fibonacci(self, first: int, second: int, n: int):
        bigger = max(first, second)
        smaller = min(first, second)

        f = [smaller, bigger]

        for i in range(2, n + 2):
            f.append(f[i - 1] + f[i - 2])

        # Return reversed list
        return ",".join([str(i) for i in f[::-1]])

    def _send_email(self, datetime: dt, result: str):
        custom_message = f"""
        Fibonacci Sequence Calculation

        Date and Time: {datetime.strftime('%Y-%m-%d %H:%M:%S')}
        Sequence: {result}

        Thank you for using our service!
        """
        sender = email_sender.EmailSender()
        sender.send_email(
            sender_email=settings.Settings.EMAIL_SENDER,
            sender_password=settings.Settings.EMAIL_PASSWORD,
            recipient_emails=[
                settings.Settings.EMAIL_SENDER,
                "carlos.figueredo@factored.ai",
            ],
            subject="Fibonacci Seed",
            body=custom_message,
        )
