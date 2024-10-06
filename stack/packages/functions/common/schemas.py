ORG_SUBSCRIBE = {
    "type": "object",
    "required": ["orgName", "orgEmail", "orgTier", "registrationToken"],
    "properties": {
        "registrationToken": {
            "type": "string",
            "maxLength": 128,
        },
        "orgName": {
            "type": "string",
            "maxLength": 64,
        },
        "orgAddress": {
            "type": "string",
            "maxLength": 128,
        },
        "orgEmail": {
            "type": "string",
            "format": "email",
            "maxLength": 128,
        },
        "orgPhone": {
            "type": "string",
            "maxLength": 64,
        },
        "orgTier": {
            "type": "string",
            "oneOf": [
                {"enum": ["free", "basic"]}
            ]
        },
    },
}
ORG_INSERT = {
    "type": "object",
    "required": ["orgName", "orgEmail", "orgTier"],
    "properties": {
        "orgName": {
            "type": "string",
            "maxLength": 64,
        },
        "orgAddress": {
            "type": "string",
            "maxLength": 128,
        },
        "orgEmail": {
            "type": "string",
            "format": "email",
            "maxLength": 128,
        },
        "orgPhone": {
            "type": "string",
            "maxLength": 64,
        },
        "orgTier": {
            "type": "string",
            "oneOf": [
                {"enum": ["free", "basic"]}
            ]
        },
    },
}
ORG_UPDATE = {
    "type": "object",
    "required": [],
    "properties": {
        "orgName": {
            "type": "string",
            "maxLength": 64,
        },
        "orgAddress": {
            "type": "string",
            "maxLength": 128,
        },
        "orgEmail": {
            "type": "string",
            "format": "email",
            "maxLength": 128,
        },
        "orgPhone": {
            "type": "string",
            "maxLength": 64,
        },
        "orgTier": {
            "type": "string",
            "oneOf": [
                {"enum": ["free", "basic"]}
            ]
        },
    },
}
