def get_phone_aggregation(number: int):
    ms = 1000
    return [
        {
            "$match": {"phone": number},
        },
        {
            "$addFields": {
                "duration": {"$subtract": ["$end_date", "$start_date"]}
            }
        },
        {
            "$addFields": {
                "price": {"$multiply": ["$duration", 10 / ms]}
            }
        },
        {
            "$unset": ["phone", "start_date", "end_date"]
        },
        {
            "$group": {
                "_id": None,
                "cnt_all_attempts": {"$count": {}},
                "sec_10": {
                    "$sum": {
                        "$cond": [
                            {"$lte": ["$duration", 10 * ms]},
                            1,
                            0,
                        ],
                    },
                },
                "sec_10_30": {
                    "$sum": {
                        "$cond": [
                            {
                                "$and": [
                                    {"$gt": ["$duration", 10 * ms]},
                                    {"$lte": ["$duration", 30 * ms]},
                                ],
                            },
                            1,
                            0,
                        ],
                    },
                },
                "sec_30": {
                    "$sum": {
                        "$cond": [
                            {"$gt": ["$duration", 30 * ms]},
                            1,
                            0
                        ],
                    },
                },
                "min_price_att": {"$min": "$price"},
                "max_price_att": {"$max": "$price"},
                "avg_dur_att": {"$avg": "$price"},
                "sum_price_att_over_15": {
                    "$sum": {
                        "$cond": [
                            {"$gt": ["$duration", 15 * ms]},
                            "$price",
                            0
                        ],
                    },
                },
            },
        },
    ]
