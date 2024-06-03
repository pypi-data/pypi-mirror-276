from pulse_linter.Blacklist.imports.base_dictionary import build_blacklist
from pulse_linter.Blacklist.imports.cwe import Cwe


class Blacklist:
    @staticmethod
    def gen_blacklist():
        sets = []
        sets.append(
            build_blacklist("pickle",
                                      "B301",
                                      Cwe.DESERIALIZATION_OF_UNTRUSTED_DATA,
                                      [
                                          "pickle.loads",
                                          "pickle.load",
                                          "pickle.Unpickler",
                                          "dill.loads",
                                          "dill.load",
                                          "dill.Unpickler",
                                          "shelve.open",
                                          "shelve.DbfilenameShelf",
                                          "jsonpickle.decode",
                                          "jsonpickle.unpickler.decode",
                                          "jsonpickle.unpickler.Unpickler",
                                          "pandas.read_pickle",
                                      ],
                                      "Pickle and modules that wrap it can be unsafe when used to "
                                      "deserialize untrusted data, possible security ",
                                      ))
        sets.append(
            build_blacklist(
                "marshal",
                "B302",
                Cwe.DESERIALIZATION_OF_UNTRUSTED_DATA,
                ["marshal.load", "marshal.loads"],
                "Deserialization with the marshal module is possibly dangerous.",
            )
        )

        sets.append(
            build_blacklist(
                "md5",
                "B303",
                Cwe.BROKEN_CRYPTO,
                [
                    "Crypto.Hash.MD2.new",
                    "Crypto.Hash.MD4.new",
                    "Crypto.Hash.MD5.new",
                    "Crypto.Hash.SHA.new",
                    "Cryptodome.Hash.MD2.new",
                    "Cryptodome.Hash.MD4.new",
                    "Cryptodome.Hash.MD5.new",
                    "Cryptodome.Hash.SHA.new",
                    "cryptography.hazmat.primitives.hashes.MD5",
                    "cryptography.hazmat.primitives.hashes.SHA1",
                ],
                "Use of insecure MD2, MD4, MD5, or SHA1 hash function.",
            )
        )

        sets.append(
            build_blacklist(
                "md5",
                "B303",
                Cwe.BROKEN_CRYPTO,
                [
                    "hashlib.md4",
                    "hashlib.md5",
                    "hashlib.sha",
                    "hashlib.sha1",
                    "Crypto.Hash.MD2.new",
                    "Crypto.Hash.MD4.new",
                    "Crypto.Hash.MD5.new",
                    "Crypto.Hash.SHA.new",
                    "Cryptodome.Hash.MD2.new",
                    "Cryptodome.Hash.MD4.new",
                    "Cryptodome.Hash.MD5.new",
                    "Cryptodome.Hash.SHA.new",
                    "cryptography.hazmat.primitives.hashes.MD5",
                    "cryptography.hazmat.primitives.hashes.SHA1",
                ],
                "Use of insecure MD2, MD4, MD5, or SHA1 hash function.",
            )
        )
        sets.append(
            build_blacklist(
                "ciphers",
                "B304",
                Cwe.BROKEN_CRYPTO,
                [
                    "Crypto.Cipher.ARC2.new",
                    "Crypto.Cipher.ARC4.new",
                    "Crypto.Cipher.Blowfish.new",
                    "Crypto.Cipher.DES.new",
                    "Crypto.Cipher.XOR.new",
                    "Cryptodome.Cipher.ARC2.new",
                    "Cryptodome.Cipher.ARC4.new",
                    "Cryptodome.Cipher.Blowfish.new",
                    "Cryptodome.Cipher.DES.new",
                    "Cryptodome.Cipher.XOR.new",
                    "cryptography.hazmat.primitives.ciphers.algorithms.ARC4",
                    "cryptography.hazmat.primitives.ciphers.algorithms.Blowfish",
                    "cryptography.hazmat.primitives.ciphers.algorithms.IDEA",
                ],
                "Use of insecure cipher {name}. Replace with a known secure"
                " cipher such as AES.",
                "HIGH",
            )
        )

        sets.append(
            build_blacklist(
                "cipher_modes",
                "B305",
                Cwe.BROKEN_CRYPTO,
                ["cryptography.hazmat.primitives.ciphers.modes.ECB"],
                "Use of insecure cipher mode {name}.",
            )
        )

        sets.append(
            build_blacklist(
                "mktemp_q",
                "B306",
                Cwe.INSECURE_TEMP_FILE,
                ["tempfile.mktemp"],
                "Use of insecure and deprecated function (mktemp).",
            )
        )

        sets.append(
            build_blacklist(
                "eval",
                "B307",
                Cwe.OS_COMMAND_INJECTION,
                ["eval"],
                "Use of possibly insecure function - consider using safer "
                "ast.literal_eval.",
            )
        )

        sets.append(
            build_blacklist(
                "mark_safe",
                "B308",
                Cwe.XSS,
                ["django.utils.safestring.mark_safe"],
                "Use of mark_safe() may expose cross-site scripting "
                "vulnerabilities and should be reviewed.",
            )
        )

        # skipped B309 as the check for a call to httpsconnection has been removed

        sets.append(
            build_blacklist(
                "urllib_urlopen",
                "B310",
                Cwe.PATH_TRAVERSAL,
                [
                    "urllib.request.urlopen",
                    "urllib.request.urlretrieve",
                    "urllib.request.URLopener",
                    "urllib.request.FancyURLopener",
                    "six.moves.urllib.request.urlopen",
                    "six.moves.urllib.request.urlretrieve",
                    "six.moves.urllib.request.URLopener",
                    "six.moves.urllib.request.FancyURLopener",
                ],
                "Audit url open for permitted schemes. Allowing use of file:/ or "
                "custom schemes is often unexpected.",
            )
        )

        sets.append(
            build_blacklist(
                "random",
                "B311",
                Cwe.INSUFFICIENT_RANDOM_VALUES,
                [
                    "random.Random",
                    "random.random",
                    "random.randrange",
                    "random.randint",
                    "random.choice",
                    "random.choices",
                    "random.uniform",
                    "random.triangular",
                    "random.randbytes",
                ],
                "Standard pseudo-random generators are not suitable for "
                "security/cryptographic purposes.",
                "LOW",
            )
        )

        sets.append(
            build_blacklist(
                "telnetlib",
                "B312",
                Cwe.CLEARTEXT_TRANSMISSION,
                ["telnetlib.*"],
                "Telnet-related functions are being called. Telnet is considered "
                "insecure. Use SSH or some other encrypted protocol.",
                "HIGH",
            )
        )
        xml_msg = (
            "Using {name} to parse untrusted XML data is known to be "
            "vulnerable to XML attacks. Replace {name} with its "
            "defusedxml equivalent function or make sure "
            "defusedxml.defuse_stdlib() is called"
        )
        sets.append(
            build_blacklist(
                "xml_bad_cElementTree",
                "B313",
                Cwe.IMPROPER_INPUT_VALIDATION,
                [
                    "xml.etree.cElementTree.parse",
                    "xml.etree.cElementTree.iterparse",
                    "xml.etree.cElementTree.fromstring",
                    "xml.etree.cElementTree.XMLParser",
                ],
                xml_msg,
            )
        )

        sets.append(
            build_blacklist(
                "xml_bad_ElementTree",
                "B314",
                Cwe.IMPROPER_INPUT_VALIDATION,
                [
                    "xml.etree.ElementTree.parse",
                    "xml.etree.ElementTree.iterparse",
                    "xml.etree.ElementTree.fromstring",
                    "xml.etree.ElementTree.XMLParser",
                ],
                xml_msg,
            )
        )

        sets.append(
            build_blacklist(
                "xml_bad_expatreader",
                "B315",
                Cwe.IMPROPER_INPUT_VALIDATION,
                ["xml.sax.expatreader.create_parser"],
                xml_msg,
            )
        )

        sets.append(
            build_blacklist(
                "xml_bad_expatbuilder",
                "B316",
                Cwe.IMPROPER_INPUT_VALIDATION,
                ["xml.dom.expatbuilder.parse", "xml.dom.expatbuilder.parseString"],
                xml_msg,
            )
        )

        sets.append(
            build_blacklist(
                "xml_bad_sax",
                "B317",
                Cwe.IMPROPER_INPUT_VALIDATION,
                ["xml.sax.parse", "xml.sax.parseString", "xml.sax.make_parser"],
                xml_msg,
            )
        )

        sets.append(
            build_blacklist(
                "xml_bad_minidom",
                "B318",
                Cwe.IMPROPER_INPUT_VALIDATION,
                ["xml.dom.minidom.parse", "xml.dom.minidom.parseString"],
                xml_msg,
            )
        )

        sets.append(
            build_blacklist(
                "xml_bad_pulldom",
                "B319",
                Cwe.IMPROPER_INPUT_VALIDATION,
                ["xml.dom.pulldom.parse", "xml.dom.pulldom.parseString"],
                xml_msg,
            )
        )

        sets.append(
            build_blacklist(
                "xml_bad_etree",
                "B320",
                Cwe.IMPROPER_INPUT_VALIDATION,
                [
                    "lxml.etree.parse",
                    "lxml.etree.fromstring",
                    "lxml.etree.RestrictedElement",
                    "lxml.etree.GlobalParserTLS",
                    "lxml.etree.getDefaultParser",
                    "lxml.etree.check_docinfo",
                ],
                (
                    "Using {name} to parse untrusted XML data is known to be "
                    "vulnerable to XML attacks. Replace {name} with its "
                    "defusedxml equivalent function."
                ),
            )
        )

        # end of XML tests

        sets.append(
            build_blacklist(
                "ftplib",
                "B321",
                Cwe.CLEARTEXT_TRANSMISSION,
                ["ftplib.*"],
                "FTP-related functions are being called. FTP is considered "
                "insecure. Use SSH/SFTP/SCP or some other encrypted protocol.",
                "HIGH",
            )
        )

        # skipped B322 as the check for a call to input() has been removed

        sets.append(
            build_blacklist(
                "unverified_context",
                "B323",
                Cwe.IMPROPER_CERT_VALIDATION,
                ["ssl._create_unverified_context"],
                "By default, Python will create a secure, verified ssl context for"
                " use in such classes as HTTPSConnection. However, it still allows"
                " using an insecure context via the _create_unverified_context "
                "that  reverts to the previous behavior that does not validate "
                "certificates or perform hostname checks.",
            )
        )

        return sets

    def full_blacklist(self):
        blist = self.gen_blacklist()
        result = {item['name']: item for item in blist}
        return result

# tester function:
#
# instance = Blacklist()
# blist = instance.gen_blacklist()
# blacklist = instance.full_blacklist()
# print(blist)