def get_logs(service_name):

    logs = {

        "payment-api": [
            "ERROR: Database connection timeout",
            "ERROR: Failed to process payment",
            "500 Internal Server Error"
        ],

        "auth-api": [
            "ERROR: Invalid token validation",
            "Authentication failures increased"
        ]
    }

    return logs.get(
        service_name,
        ["No logs found"]
    )
