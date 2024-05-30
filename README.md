# SQL to DAX Converter

This Python script converts SQL queries into DAX (Data Analysis Expressions) queries. It allows users to seamlessly translate SQL queries typically used in relational databases into DAX queries used in Power BI and other analytics platforms.

## Features

- **Conversion of Basic SQL Constructs**: The converter currently supports conversion of SELECT, FROM, INNER JOIN, LEFT JOIN, WHERE, GROUP BY, and ORDER BY clauses commonly found in SQL queries.
- **Easy-to-Use Interface**: Users can simply input their SQL query into the provided Python class and obtain the corresponding DAX query.
- **Readable DAX Output**: The DAX queries generated maintain readability and structure similar to the original SQL query for ease of understanding.

## Usage

To use the SQL to DAX Converter, follow these steps:

1. Clone or download the repository to your local machine.
2. Ensure you have Python installed.
3. Run the script `sql_to_dax_converter.py`.
4. Input your SQL query when prompted.
5. The DAX equivalent of your SQL query will be displayed.

## Dependencies

This project depends on the following Python libraries:
- `sqlparse`: For parsing SQL queries into tokens.
- `sqlparse.sql`: Provides classes for representing SQL query components.
- `sqlparse.tokens`: Contains token definitions for SQL parsing.

## Example

```python
sql_query = "SELECT name, age FROM users INNER JOIN orders ON users.id = orders.user_id WHERE age > 30 GROUP BY age ORDER BY name"
converter = SQLToDAXConverter(sql_query)
converter.convert()
print(converter.get_dax_query())

## Contribution
Contributions to this project are welcome! If you encounter any bugs or have suggestions for improvements, feel free to open an issue or submit a pull request.
