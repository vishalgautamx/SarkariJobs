from .ssc import get_ssc_notice_data


SOURCE_ADAPTERS = {
    "SSC": {
        "fetch": get_ssc_notice_data,
    },
}