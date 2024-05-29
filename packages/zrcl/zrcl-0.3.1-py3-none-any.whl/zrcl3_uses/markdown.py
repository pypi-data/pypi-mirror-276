import pandas as pd
import os
import io


class MarkdownExtractor:
    def __init__(self, text: str | list):
        if isinstance(text, list):
            self.text = "\n".join(text)
        elif len(text) > 2000:
            self.text = text
        elif os.path.exists(text):
            self.text = open(text, "r").read()
        else:
            self.text = text

    @property
    def lines(self):
        return self.text.split("\n")

    def extractTables(self):
        tables = []
        isTable = False
        currTable = []
        for line in self.lines:
            if line.startswith("|") and line.endswith("|"):
                isTable = True
            elif isTable:
                tables.append(currTable)
                currTable = []
                isTable = False

            if isTable:
                currTable.append(line)

        return tables


def markdownTableToDataframe(string: str):
    # Convert Markdown table to CSV format by removing "|", "-", and trimming extra spaces
    csv_string = "\n".join(
        [" ".join(line.split("|")[1:-1]).strip() for line in string.strip().split("\n")]
    )
    csv_list = csv_string.split("\n")
    csv_string = "\n".join(csv_list[:1]) + "\n" + "\n".join(csv_list[2:])

    # Use StringIO to simulate a file-like object for reading into pandas DataFrame
    df = pd.read_csv(io.StringIO(csv_string), sep="\\s{2,}", engine="python")

    return df
