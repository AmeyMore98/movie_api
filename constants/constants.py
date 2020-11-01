# Regex
POPULARITY_QUERY_REGEX = "^(gt|lt|gte|lte|ne):(\d+|(\d+.\d+))$"
IMDB_SCORE_QUERY_REGEX = "^(gt|lt|gte|lte|ne):(\d{1}|(\d{1}.\d+))$"
SORT_REGEX = "^(-*((popularity)|(imdb_score)|(name)|(director)),)*-*((popularity)|(imdb_score)|(name)|(director))$"

# Messages
RESOURCE_NOT_FOUND = "Resource not found"
OPERATION_NOT_PERMITTED = "Operation not permitted"
INCORRECT_CREDENTIALS = "Incorrect username or password"
CREDENTIALS_NOT_VALID = "Could not validate credentials"
RESOURCE_DELETED = "Resource deleted"
INVALID_TOKEN = "Invalid token"
TOKEN_EXPIRED = "Token expired"
# Keys
DETAIL = "detail"
