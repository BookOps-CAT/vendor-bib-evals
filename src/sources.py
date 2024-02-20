from typing import Iterator, Optional
from pymarc import MARCReader, Record, Field

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


def determine_no_of_fields(bib: Record) -> tuple[int, int]:
    """
    Calculates total number of MARC fields in a bib.
    """
    for n, _ in enumerate(bib):
        pass
    s = len(bib.subjects)
    return n, s


def source_reader(fh: str) -> Iterator[tuple[str, bool, bool, str, str, int, int]]:
    """
    Loops over a MARC file and extracts 040$a and 042 values
    """
    with open(fh, "rb") as marcfile:
        reader = MARCReader(marcfile, hide_utf8_warnings=True)
        for bib in reader:

            try:
                cat_src = bib.get("040")["a"].strip()
            except KeyError:
                cat_src = ""
            auth_bib = is_pcc(bib.get("042"))
            oclc_no = has_oclc_no(bib.get_fields("035"))
            enc_lvl = bib.leader[17]
            desc_cat_form = bib.leader[18]
            fields_len, subj_len = determine_no_of_fields(bib)
            yield (
                cat_src,
                auth_bib,
                oclc_no,
                enc_lvl,
                desc_cat_form,
                fields_len,
                subj_len,
            )


if __name__ == "__main__":
    bibs = source_reader("files/SerialSolutionsSerialsOnly-240219.mrc")
    for row in bibs:
        save2csv("reports/serialsol-bib-sources-raw.csv", row)
