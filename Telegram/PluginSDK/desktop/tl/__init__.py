from .codec import TLObject, constructor, decode, encode, load_catalogue, response_type

SCHEMA_SHA256 = load_catalogue(globals())
