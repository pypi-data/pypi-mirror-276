def build_blacklist(name, bid, cwe, qualname, message, level = 'MEDUIM'):
    return {
        "name" : name,
        "bid" : bid,
        "cwe" : cwe,
        "qualname" : qualname,
        "message" :message,
        "level" : level,
    }