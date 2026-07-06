def search_runbook(root_cause):

    runbooks = {

        "database": {

            "title":
            "Database Connection Issues",

            "steps":[

                "Check database availability",

                "Increase connection pool size",

                "Restart affected services",

                "Monitor database metrics"
            ]
        },


        "latency": {

            "title":
            "High Latency Issues",

            "steps":[

                "Check CPU usage",

                "Analyze slow queries",

                "Scale service instances"
            ]
        }

    }


    text = root_cause.lower()


    if "database" in text:

        return runbooks["database"]


    if "latency" in text:

        return runbooks["latency"]


    return {
        "title":"General Investigation",

        "steps":[
            "Check logs",
            "Review metrics"
        ]
    }
