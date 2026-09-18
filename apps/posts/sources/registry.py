from .ssc import fetch_ssc_updates
from .upsc import fetch_upsc_updates
from .generic import fetch_generic_source


SOURCE_REGISTRY = {

    "SSC": {
        "enabled": True,
        "type": "custom",
        "fetcher": fetch_ssc_updates,
    },

    "UPSC": {
        "enabled": True,
        "type": "custom",
        "fetcher": fetch_upsc_updates,
    },

    "IBPS": {
        "enabled": False,
        "type": "generic",
        "url": "https://www.ibps.in/",
        "selectors": {
            "container": "a",
        },
    },

    "RRB": {
        "enabled": False,
        "type": "generic",
        "url": "https://www.rrbcdg.gov.in/",
        "selectors": {
            "container": "a",
        },
    },

    "NTA": {
        "enabled": False,
        "type": "generic",
        "url": "https://www.nta.ac.in/",
        "selectors": {
            "container": "a",
        },
    },

    "SBI": {
        "enabled": False,
        "type": "generic",
        "url": "https://sbi.co.in/web/careers",
        "selectors": {
            "container": "a",
        },
    },

    "India Post": {
        "enabled": False,
        "type": "generic",
        "url": "https://www.indiapost.gov.in/",
        "selectors": {
            "container": "a",
        },
    },

    "UPPSC": {
        "enabled": False,
        "type": "generic",
        "url": "https://uppsc.up.nic.in/",
        "selectors": {
            "container": "a",
        },
    },

    "UPSSSC": {
        "enabled": False,
        "type": "generic",
        "url": "https://upsssc.gov.in/",
        "selectors": {
            "container": "a",
        },
    },
}


def run_source(source_name, config):

    source_type = config.get("type")

    if source_type == "custom":

        fetcher = config.get("fetcher")

        if not fetcher:
            return {
                "success": False,
                "source": source_name,
                "created": 0,
                "updated": 0,
                "total": 0,
                "items": [],
                "error": "Custom fetcher not configured.",
            }

        return fetcher()

    if source_type == "generic":

        return fetch_generic_source(
            source_name=source_name,
            url=config.get("url"),
            selectors=config.get("selectors"),
        )

    return {
        "success": False,
        "source": source_name,
        "created": 0,
        "updated": 0,
        "total": 0,
        "items": [],
        "error": f"Unknown source type: {source_type}",
    }