from datetime import datetime


def convertDateString(date_string) -> datetime:
    """
    Meant to match how Django displays the date times on the tables of a stock list.
    >> convertDateString("2026-03-23") == "March 23, 2026"
    >> convertDateString("2026-11-23") == "Nov. 23, 2026"
    >> convertDateString("2026-07-01") == "July 1, 2026"
    """
    dt = datetime.strptime(date_string, "%Y-%m-%d")
    name_of_month = dt.strftime("%B")

    formatted_date = ""

    if len(name_of_month) <= 5:
        formatted_date = f"{dt.strftime('%B')} {dt.day}, {dt.year}"
        # return datetime.strptime(date_string, "%Y-%m-%d").strftime("%B %d, %Y")
    else:
        formatted_date = f"{dt.strftime('%b')}. {dt.day}, {dt.year}"
        # return datetime.strptime(date_string, "%Y-%m-%d").strftime("%b. %d, %Y")
    return formatted_date
