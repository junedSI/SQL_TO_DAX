import sqlparse
from sqlparse.sql import IdentifierList, Identifier, Where, Comparison
from sqlparse.tokens import Keyword, DML

class SQLToDAXConverter:
    def __init__(self, sql_query):
        self.sql_query = sql_query
        self.parsed_query = None
        self.dax_query = None
    
    def parse_sql(self):
        self.parsed_query = sqlparse.parse(self.sql_query)[0]
    
    def convert(self):
        if not self.parsed_query:
            self.parse_sql()
        
        # Start conversion
        self.dax_query = "VAR __Result =\n"
        
        # Convert each component
        self.convert_select()
        self.convert_from()
        self.convert_joins()
        self.convert_where()
        self.convert_group_by()
        self.convert_order_by()
        
        self.dax_query += "RETURN\n    __Result"
    
    def convert_select(self):
        select_clause = next((token for token in self.parsed_query.tokens if token.ttype is DML and token.value.upper() == 'SELECT'), None)
        if select_clause:
            select_index = self.parsed_query.token_index(select_clause)
            columns = [token for token in self.parsed_query.tokens[select_index+1:] if isinstance(token, IdentifierList) or isinstance(token, Identifier)]
            self.dax_query += "    EVALUATE\n    SELECTCOLUMNS(\n"
            self.dax_query += ",\n    ".join([f'"{str(col)}"' for col in columns]) + "\n"
            self.dax_query += "    )\n"
    
    def convert_from(self):
        from_clause = next((token for token in self.parsed_query.tokens if token.ttype is Keyword and token.value.upper() == 'FROM'), None)
        if from_clause:
            from_index = self.parsed_query.token_index(from_clause)
            table = next((token for token in self.parsed_query.tokens[from_index+1:] if isinstance(token, Identifier)), None)
            if table:
                self.dax_query += f'    {table}\n'

    def convert_joins(self):
        join_clauses = [token for token in self.parsed_query.tokens if token.ttype is Keyword and 'JOIN' in token.value.upper()]
        for join_clause in join_clauses:
            join_type = join_clause.value.upper()
            join_index = self.parsed_query.token_index(join_clause)
            join_table = next((token for token in self.parsed_query.tokens[join_index+1:] if isinstance(token, Identifier)), None)
            join_condition = next((token for token in self.parsed_query.tokens[join_index+1:] if isinstance(token, Where)), None)
            if join_type == 'INNER JOIN':
                self.dax_query += f'    NATURALINNERJOIN({join_table}, '
            elif join_type == 'LEFT JOIN' or join_type == 'LEFT OUTER JOIN':
                self.dax_query += f'    NATURALLEFTOUTERJOIN({join_table}, '
            # Other join types can be added here similarly
            if join_condition:
                conditions = [str(token) for token in join_condition.tokens if isinstance(token, Comparison)]
                self.dax_query += ",\n    ".join(conditions) + "\n"
                self.dax_query += "    )\n"
    
    def convert_where(self):
        where_clause = next((token for token in self.parsed_query.tokens if isinstance(token, Where)), None)
        if where_clause:
            conditions = [str(token) for token in where_clause.tokens if isinstance(token, Comparison)]
            self.dax_query += "    FILTER(\n"
            self.dax_query += ",\n    ".join(conditions) + "\n"
            self.dax_query += "    )\n"
    
    def convert_group_by(self):
        group_by_clause = next((token for token in self.parsed_query.tokens if token.ttype is Keyword and token.value.upper() == 'GROUP BY'), None)
        if group_by_clause:
            group_by_index = self.parsed_query.token_index(group_by_clause)
            group_by_columns = [token for token in self.parsed_query.tokens[group_by_index+1:] if isinstance(token, IdentifierList) or isinstance(token, Identifier)]
            self.dax_query += "    SUMMARIZE(\n"
            self.dax_query += ",\n    ".join([f'"{str(col)}"' for col in group_by_columns]) + "\n"
            self.dax_query += "    )\n"
    
    def convert_order_by(self):
        order_by_clause = next((token for token in self.parsed_query.tokens if token.ttype is Keyword and token.value.upper() == 'ORDER BY'), None)
        if order_by_clause:
            order_by_index = self.parsed_query.token_index(order_by_clause)
            order_by_columns = [token for token in self.parsed_query.tokens[order_by_index+1:] if isinstance(token, IdentifierList) or isinstance(token, Identifier)]
            self.dax_query += "    ORDER BY(\n"
            self.dax_query += ",\n    ".join([f'"{str(col)}"' for col in order_by_columns]) + "\n"
            self.dax_query += "    )\n"
    
    def get_dax_query(self):
        return self.dax_query

""" test code """
sql_query = "SELECT name, age FROM users INNER JOIN orders ON users.id = orders.user_id WHERE age > 30 GROUP BY age ORDER BY name"
converter = SQLToDAXConverter(sql_query)
converter.convert()
print(converter.get_dax_query())