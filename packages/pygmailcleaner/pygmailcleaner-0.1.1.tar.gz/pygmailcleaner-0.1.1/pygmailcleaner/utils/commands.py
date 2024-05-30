METHODS = [
    {
        "description": "Only include promotions",
        "y_search_term": "category:promotions",
        "n_search_term": "",
        "risk": "low",
        "default": "y",
        "response": "y"
    },
    {
        "description": "Only include unread",
        "y_search_term": "in:unread",
        "n_search_term": "",
        "risk": "high",
        "default": "n",
        "response": "n"
    },
    {
        "description": "Exclude important",
        "y_search_term": "NOT is: important",
        "n_search_term": "",
        "risk": "high",
        "default": "y",
        "response": "y"
    },
    {
        "description": "Exclude attachments",
        "y_search_term": "NOT has:attachment",
        "n_search_term": "",
        "risk": "high",
        "default": "y",
        "response": "y"
    },
]