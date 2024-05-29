import json
from datetime import datetime

import requests

URL = "http://a56bc77e426d84b93b3d720c7be5dc89-1384963031.ap-northeast-2.elb.amazonaws.com/log"


class PromtailLogger:
    @staticmethod
    def send_log(level, message, service, user_id, operation, status):
        timestamp = datetime.now().isoformat() + "Z"

        log_data = {
            "timestamp": timestamp,
            "level": level,
            "message": message,
            "service": service,
            "details": {
                "user_id": user_id,
                "operation": operation,
                "status": status,
            },
        }

        response = requests.post(
            URL, data=json.dumps(log_data), headers={"Content-Type": "application/json"}
        )

        if response.status_code == 200:
            print("Log sent successfully")
        else:
            print(f"Failed to send log: {response.status_code} - {response.text}")


if __name__ == "__main__":
    PromtailLogger.send_log(
        level="INFO",
        message="test_messsage",
        service="test_finter",
        user_id="test_user",
        operation="test_operation",
        status="success",
    )
