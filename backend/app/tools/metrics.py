def get_metrics(service_name):

    metrics = {

        "payment-api": {
            "cpu": "92%",
            "memory": "85%",
            "latency": "2500ms"
        }

    }

    return metrics.get(
        service_name,
        {}
    )
