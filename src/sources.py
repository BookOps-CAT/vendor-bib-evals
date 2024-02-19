from typing import Iterator, Optional
from pymarc import MARCReader, Field

from utils import save2csv


def is_pcc(field: Optional[Field]) -> bool:
    """
    Determines if the 042 field existis and record was authenicated
    """
    if field:
        if "pcc" in field.value():
            return True
        else:
            return False
    else:
        return False


def has_oclc_no(fields: list[Field]) -> bool:
    """
    Determines if given 035s include OCLC numbers
    """
    for f in fields:
        if "(OCoLC)" in f.value():
            return True
    return False


def source_reader(fh: str) -> Iterator[tuple[str, bool, bool]]:
    """
    Loops over a MARC file and extracts 040$a and 042 values
    """
    with open(fh, "rb") as marcfile:
        reader = MARCReader(marcfile, hide_utf8_warnings=True)
        for bib in reader:
            cat_src = bib.get("040")["a"].strip()
            auth_bib = is_pcc(bib.get("042"))
            oclc_no = has_oclc_no(bib.get_fields("035"))
            enc_lvl = bib.leader[17]
            desc_cat_form = bib.leader[18]
            yield (cat_src, auth_bib, oclc_no, enc_lvl, desc_cat_form)


if __name__ == "__main__":
    bibs = source_reader("files/ebsco-20230824.mrc")
    for row in bibs:
        save2csv("reports/ebsco-bib-sources-raw.csv", row)
