from collections import OrderedDict

class OrderedMatrix:
    def __init__(self):
        self.columns = OrderedDict()
        self.header = []
        self.row_headers = []

    def set_header(self, columns):
        self.header = list(columns)
        self.columns = OrderedDict((col, []) for col in self.header)

    def insert_row(self, row_key: str, row_items: list):
        if not self.header:
            raise ValueError("Header not set. Use set_header() first.")
        
        if row_key in self.row_headers:
            # Find the index of the existing row.
            row_index = self.row_headers.index(row_key)

            # Iterate through the new items and update the matrix.
            # This sets the value to 1 for each specified column at the correct row index.
            for item in row_items:
                if item in self.columns:
                    self.columns[item][row_index] = 1
        else:
            # If the row_key is new, append it to the list of row headers.
            self.row_headers.append(row_key)
            # Append a new value (1 or 0) to the end of each column's list.
            for col in self.header:
                self.columns[col].append(1 if col in row_items else 0)

    def as_rows(self):
        return list(zip(*self.columns.values()))

    def to_dict(self):
        """
        Returns a nested dict: row_header -> {col: value}
        """
        rows = self.as_rows()
        return {
            row_key: dict(zip(self.header, row))
            for row_key, row in zip(self.row_headers, rows)
        }
