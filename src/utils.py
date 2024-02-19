import csv


def save2csv(fh, row):
    with open(fh, "a") as csvfile:
        writer = csv.writer(
            csvfile,
            delimiter=",",
            quotechar='"',
            quoting=csv.QUOTE_MINIMAL,
            lineterminator="\n",
        )
        writer.writerow(row)
