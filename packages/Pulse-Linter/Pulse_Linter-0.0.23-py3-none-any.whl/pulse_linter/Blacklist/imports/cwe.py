class Cwe:
    NOTSET = 0
    IMPROPER_INPUT_VALIDATION = 20
    PATH_TRAVERSAL = 22
    OS_COMMAND_INJECTION = 78
    XSS = 79
    BASIC_XSS = 80
    SQL_INJECTION = 89
    CODE_INJECTION = 94
    IMPROPER_WILDCARD_NEUTRALIZATION = 155
    HARD_CODED_PASSWORD = 259
    IMPROPER_ACCESS_CONTROL = 284
    IMPROPER_CERT_VALIDATION = 295
    CLEARTEXT_TRANSMISSION = 319
    INADEQUATE_ENCRYPTION_STRENGTH = 326
    BROKEN_CRYPTO = 327
    INSUFFICIENT_RANDOM_VALUES = 330
    INSECURE_TEMP_FILE = 377
    UNCONTROLLED_RESOURCE_CONSUMPTION = 400
    DESERIALIZATION_OF_UNTRUSTED_DATA = 502
    MULTIPLE_BINDS = 605
    IMPROPER_CHECK_OF_EXCEPT_COND = 703
    INCORRECT_PERMISSION_ASSIGNMENT = 732

    MITRE_URL_PATTERN = "https://cwe.mitre.org/data/definitions/%s.html"

    def __init__(self, id=NOTSET):
        self.id = id

    def link(self):
        if self.id == Cwe.NOTSET:
            return ""

        return Cwe.MITRE_URL_PATTERN % str(self.id)

    def __str__(self):
        if self.id == Cwe.NOTSET:
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