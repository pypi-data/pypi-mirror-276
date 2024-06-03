class Cwe:
    NOTSET = 0
    INCOMPLETE_URL_SANITIZATION = 20
    TAR_SLIP = 22
    PATH_TRAVERSAL = 23
    COMMAND_INJECTION = 78
    CROSS_SITE_SCRIPTING = 79
    JINJA_AUTO_ESCAPE = 79
    SQL_INJECTION = 89
    CODE_INJECTION = 94
    STATIC_CODE_INJECTION = 96
    SERVER_INFORMATION_EXPOSURE = 209
    HARD_CODED_CREDENTIALS = 259
    HANDLING_OF_INSUFFICIENT_PERMISSION = 280
    IMPROPER_ACCESS_CONTROL = 284
    IMPROPER_AUTHENTICATION = 287
    IMPROPER_CERTIFICATE_VALIDATION = 295
    CRYPTOGRAPHIC_ISSUE = 310
    PLAINTEXT_TRANSMISSION_SENSITIVE_INFORMATION = 310
    HARD_CODED_CRYPTOGRAPHIC_KEYS = 321
    INADEQUATE_ENCRYPTION_STRENGTH = 326
    RISK_CRYPTOGRAPHIC_ALGORITHM = 327
    MISSING_PROTOCOL_SSL = 327
    PREDICTABLE_IV = 329
    ORIGIN_VALIDATION_ERROR = 346
    CROSS_SITE_REQUEST_FORGERY = 352
    UNCONTROLLED_RESOURCE_CONSUMPTION = 400
    INSECURE_DEFAULT_VALUE = 400
    ACTIVE_DEBUG_CODE = 489
    DESERIALIZATION_OF_UNTRUSTED_DATA = 502
    HARD_CODED_SECRET = 547
    OPEN_REDIRECT = 601
    INSECURE_XML_PARSER = 611
    HTTPS_SESSION_WITHOUT_SECURE_ATTRIBUTE = 614
    XPATH_INJECTION = 643
    INSECURE_FILE_PERMISSION = 732
    ALGORITHM_DOWNGRADE = 757
    PASSWORD_HASH_WITHOUT_SUFFICIENT_COMPUTATION = 916
    SERVER_SIDE_REQUEST_FORGERY = 918
    NOSQL_INJECTION = 943
    SENSITIVE_COOKIE_HTTPONLY_FLAG = 1004
    UNMAINTAINED_THIRD_PARTY_COMPONENTS = 1104

    MITRE_URL_PATTERN = "https://cwe.mitre.org/data/definitions/%s.html"

    def __init__(self, id = NOTSET):
        self.id = id

    def link(self):
        if self.id == Cwe2.NOTSET:
            return ""
        return Cwe2.MITRE_URL_PATTERN % str(self.id)
    def __str__(self):
        if self.id == Cwe2.NOTSET:
            return ""
        return "CWE-%i (%s)" % (self.id, self.link())

    def as_dict(self):
        return (
            {"id": self.id, "link": self.link()}
            if self.id != Cwe.NOTSET
            else {}
        )

    def as_jsons(self):
        return str(self.as_dict())

    def from_dict(self, data):
        if "id" in data:
            self.id = int(data["id"])
        else:
            self.id = Cwe.NOTSET

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id

    def __hash__(self):
        return id(self)


