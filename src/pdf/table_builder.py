from reportlab.platypus import (
     Table, TableStyle
)
from reportlab.lib import colors


class TableBuilder:
    def __init__(self):
        self.tables = {}
        self.table_counter = 0

    def create_table(self, data, col_widths=None, style=None):
        # Generate a unique ID for each table
        table_id = f"table_{self.table_counter}"
        self.table_counter += 1

        # Create the table
        table = Table(data, colWidths=col_widths)

        # Apply default style if not provided
        if style is None:
            style = TableStyle([
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),  # First row, first column: LEFT alignment
            ('ALIGN', (1, 0), (1, 0), 'CENTER'),  # First row, second column: CENTER alignment
            ('ALIGN', (2, 0), (2, 0), 'RIGHT'),
            ('LEFTPADDING', (0, 1), (0, 1), 6),  # Increase left padding for second row's first column
            ('LEFTPADDING', (1, 1), (1, 1), -60),
            ('LEFTPADDING', (0, 2), (0, 2), 6),  # Increase left padding for second row's first column
            ('LEFTPADDING', (1, 2), (1, -1), -30),
            ('RIGHTPADDING', (1, 1), (1, -1), 0),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),

        ] )

        # Apply the style
        table.setStyle(style)

        # Store the table for future reference
        self.tables[table_id] = table
        return table_id, table

    def get_table(self, table_id):
        return self.tables.get(table_id)

    def list_tables(self):
        return list(self.tables.keys())
