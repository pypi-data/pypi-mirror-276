import lxml.etree as ET
import marcalyx
import random

mapping = {
    "https://nfdi4culture.de/ontology#locationLiteral": ("264", "a"),
    "http://schema.org/url": ("856", "u"),
    "http://www.w3.org/2004/02/skos/core#altLabel": ("240", "a"),
    "http://www.w3.org/2000/01/rdf-schema#label": ("245", "a"),
    "https://nfdi4culture.de/ontology#shelfMark": ("852", "c"),
    "https://nfdi.fiz-karlsruhe.de/ontology#publisher": ("264", "b"),
    "https://nfdi4culture.de/ontology#creationPeriod": ("264", "c"),
    "https://nfdi4culture.de/ontology#elementTypeLiteral": ("653", "a"),
    "https://nfdi4culture.de/ontology#relatedPersonLiteral": ("700", "a"),
}


def parse_marc(filepath: str, data_feed_iri: str = None):
    mrecord = ET.parse(filepath).getroot()
    record = marcalyx.Record(mrecord)
    BF = []

    buf = [
        (
            "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
            "<https://nfdi4culture.de/ontology#DatafeedElement>",
        ),
        (
            "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
            "<http://schema.org/book>",
        ),
    ]

    for k, v in mapping.items():
        for vv in record[v]:
            buf.append((k, vv.value))

    for p in record[("700", "0")]:
        if p.value.startswith("(DE-588)"):
            buf.append(
                (
                    "https://nfdi4culture.de/ontology#relatedPerson",
                    f"<https://d-nb.info/gnd/{p.value.replace('(DE-588)', '')}>",
                )
            )
            buf.append(
                (
                    "https://nfdi4culture.de/ontology#gnd",
                    f"<https://d-nb.info/gnd/{p.value.replace('(DE-588)', '')}>",
                )
            )

    for p in record[("100", "0")]:
        if p.value.startswith("(DE-588)"):
            buf.append(
                (
                    "https://nfdi4culture.de/ontology#relatedPerson",
                    f"<https://d-nb.info/gnd/{p.value.replace('(DE-588)', '')}>",
                )
            )
            buf.append(
                (
                    "https://nfdi4culture.de/ontology#gnd",
                    f"<https://d-nb.info/gnd/{p.value.replace('(DE-588)', '')}>",
                )
            )

    for p in record[("650", "0")]:
        if p.value.startswith("(DE-588)"):
            buf.append(
                (
                    "https://nfdi4culture.de/ontology#relatedPerson",
                    f"<https://d-nb.info/gnd/{p.value.replace('(DE-588)', '')}>",
                )
            )
            buf.append(
                (
                    "https://nfdi4culture.de/ontology#gnd",
                    f"<https://d-nb.info/gnd/{p.value.replace('(DE-588)', '')}>",
                )
            )

    for p in record[("852", "a")]:
        buf.append(
            (
                "https://nfdi4culture.de/ontology#holdingOrganisation",
                "https://sigel.staatsbibliothek-berlin.de/suche?isil=" + p.value,
            )
        )

    for field in ("240", "245"):
        tmp = "".join(
            [b.value for subfield in ("a", "b", "c") for b in record[(field, subfield)]]
        )
        if tmp:
            buf.append(("http://www.w3.org/2004/02/skos/core#altLabel", tmp))
    newbuf = {}
    for field, value in buf:
        newbuf.setdefault(field, []).append(value)

    the_id = None
    # Find the subject from the 856 u
    for u in record[("856", "u")]:
        if u.value.find("urn:") > 0:
            the_id = u.value
    if not the_id:
        print(record["856"])
        return ""

    for field, v in newbuf.items():
        for vv in v:
            if vv.startswith("<http"):
                BF.append(f"<{the_id}> <{field}> {vv} .")
            else:
                vv = vv.replace('"', r"\"")
                BF.append(f'<{the_id}> <{field}> "{vv}" .')

    if data_feed_iri:
        bnode = f"_:{random.randint(0, 1000000)}"
        BF.append(
            f"<{data_feed_iri}> <https://nfdi4culture.de/ontology#hasDatafeedElement> {bnode} ."
        )
        BF.append(
            f"{bnode} <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <https://schema.org/DataFeedItem> ."
        )
        BF.append(f"{bnode} <https://schema.org/item> <{the_id}> .")

    return "\n".join(BF)
