"""
Initial event types for the Friday life logger.
These types define the basic categories of life events that can be logged.
"""

INITIAL_EVENT_TYPES = [
    {
        "name": "photo",
        "description": "Captured a photo moment",
        "icon": "camera",
        "color": "#4CAF50",
        "schema": {
            "type": "object",
            "required": ["photo_url"],
            "properties": {
                "photo_url": {
                    "type": "string",
                    "format": "uri",
                },
                "location": {
                    "type": "object",
                    "properties": {
                        "lat": {"type": "number"},
                        "lng": {"type": "number"},
                    },
                },
                "caption": {"type": "string"},
                "tags": {
                    "type": "array",
                    "items": {"type": "string"},
                },
            },
        },
    },
    {
        "name": "meal",
        "description": "Food consumption record",
        "icon": "restaurant",
        "color": "#FF9800",
        "schema": {
            "type": "object",
            "required": ["meal_type", "foods"],
            "properties": {
                "meal_type": {
                    "type": "string",
                    "enum": [
                        "breakfast",
                        "lunch",
                        "dinner",
                        "snack",
                    ],
                },
                "foods": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "quantity": {"type": "string"},
                            "calories": {"type": "number"},
                        },
                    },
                },
                "location": {"type": "string"},
                "mood": {"type": "string"},
            },
        },
    },
    {
        "name": "exercise",
        "description": "Physical activity record",
        "icon": "fitness_center",
        "color": "#2196F3",
        "schema": {
            "type": "object",
            "required": ["type", "duration"],
            "properties": {
                "type": {
                    "type": "string",
                    "enum": [
                        "running",
                        "cycling",
                        "swimming",
                        "weights",
                        "yoga",
                        "other",
                    ],
                },
                "duration": {"type": "number"},
                "distance": {"type": "number"},
                "calories_burned": {"type": "number"},
                "heart_rate": {
                    "type": "object",
                    "properties": {
                        "avg": {"type": "number"},
                        "max": {"type": "number"},
                    },
                },
            },
        },
    },
    {
        "name": "note",
        "description": "Quick text note or thought",
        "icon": "note",
        "color": "#9C27B0",
        "schema": {
            "type": "object",
            "required": ["content"],
            "properties": {
                "content": {"type": "string"},
                "tags": {
                    "type": "array",
                    "items": {"type": "string"},
                },
                "mood": {"type": "string"},
            },
        },
    },
    {
        "name": "sleep",
        "description": "Sleep record",
        "icon": "bedtime",
        "color": "#3F51B5",
        "schema": {
            "type": "object",
            "required": ["start_time", "end_time"],
            "properties": {
                "start_time": {
                    "type": "string",
                    "format": "date-time",
                },
                "end_time": {
                    "type": "string",
                    "format": "date-time",
                },
                "quality": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 5,
                },
                "interruptions": {"type": "integer"},
                "notes": {"type": "string"},
            },
        },
    },
]
