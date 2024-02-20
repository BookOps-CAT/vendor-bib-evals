from pymarc import MARCReader, Record
from random import sample

from utils import save2csv


def get_issn(bib: Record) -> str:
    """
    Extracts ISSN from given record
    """
    try:
        issn = bib.get("022")["a"].strip()
        return issn
    except TypeError:
        return ""


def get_sample(fh: str, out: str, sample_size: int) -> None:
    """
    Selects random n records
    """
    # calulate total number of bibs in the file
    with open(fh, "rb") as marcfile:
        for n, _ in enumerate(MARCReader(marcfile, hide_utf8_warnings=True)):
            pass

    random_records = sample(range(n), sample_size)

    issn_fh = f"{out[:-4]}.csv"

    with open(fh, "rb") as marcfile:
        for n, bib in enumerate(MARCReader(marcfile, hide_utf8_warnings=True)):
            if n in random_records:
                control_no = bib.get("001").value()
                issn = get_issn(bib)
                save2csv(issn_fh, [control_no, issn])
                with open(out, "ab") as outfile:
                    outfile.write(bib.as_marc())


if __name__ == "__main__":
    bib_sample = get_sample("files/ebsco-20230824.mrc", "reports/sample-ebsco.mrc", 50)
