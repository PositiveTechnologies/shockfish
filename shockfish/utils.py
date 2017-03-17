class Locator:
    services = {}

    @classmethod
    def load(cls, key, service):
        cls.services[key] = service

    @classmethod
    def get(cls, key):
        return cls.services.get(key)


def extractCookies(cookieHeaderValue, config):
    sources = config.sources
    cookies = []
    cookiePairs = []
    try:
        cookiePairs = cookieHeaderValue.split(";")
    except ValueError:
        pass
    for cook in cookiePairs:
        try:
            name, value = cook.split("=",1)
        except ValueError:
            continue
        name = name.strip()
        if (sources.get("cookies") == True or
                name in sources.get("cookies").get("checked", []) or
                not name in sources.get("cookies").get("unchecked", [name])
            ):
            cookies.append({
                            "value": value.encode(),
                            "name" : name,
                            "type": "request_cookie"
                        })
    return cookies


def extractFeatures(request, config):
    args = request.args
    sources = config.sources
    headers  = request.requestHeaders.getAllRawHeaders()
    features = []

    features.append({
        "value" : request.path,
        "name" : "path",
        "type" : "request_path"
    })

    features.append({
        "value" : request.method,
        "name" : "method",
        "type": "request_method"
    })

    features.append({
        "value" : request.uri,
        "name" : "uri",
        "type": "request_uri"
    })

    if headers and sources.get("headers"):
        for header in headers:
            if header[0] == b"Cookie":
                continue
            if not isinstance(header[1], list):
                    header[1] = [header[1]]
            for header_value in header[1]:
                header_name = header[0].decode()
                if (sources.get("headers") == True or
                        header_name in sources.get("headers").get("checked", []) or
                        header_name not in sources.get("headers").get("unchecked", [header_name])
                    ):
                    features.append({
                         "value": header_value,
                         "name" : header_name,
                         "type": "request_header"
                    })

    if args and sources.get("args"):
        for key in args:
            key_name = key.decode()
            if (sources.get("args") == True or
                    key_name in sources.get("args").get("checked", []) or
                    not key_name in sources.get("args").get("unchecked", [key_name]) 
                ):
                storage = args[key]
                if isinstance(storage, list):
                    for single_storage in storage:
                        features.append({
                            "value": single_storage,
                            "name" : key_name,
                            "type": "request_arg"
                        })

    cookies = request.requestHeaders.getRawHeaders('Cookie', [])
    if cookies:
        for cookie in cookies:
            features.extend(extractCookies(cookie, config))

    return features


def getFileContent(filename):
    content = ""
    with open(filename, "rb") as f:
        content = f.read()
    return content

def mergeArgs(dst, src):
    for k,v in src.items():
        if not k in dst:
            dst.update({k: v})
        else:
            dst[k].extend(v)
    return dst
