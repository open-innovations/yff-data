import re
def slugify(s):
    #TODO try replace '\W+'
    return re.sub(r'[\*\-\=\(\)\s\,\"\:\(/)]+', '_', s.lower())
