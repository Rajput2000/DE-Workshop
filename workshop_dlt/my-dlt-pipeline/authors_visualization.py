import marimo

__generated_with = "0.10.6"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    import ibis
    import plotly.express as px
    import dlt
    return dlt, ibis, mo, px


@app.cell
def __(dlt):
    # Connect to the dlt pipeline database using ibis
    pipeline = dlt.pipeline(pipeline_name='open_library_pipeline', destination='duckdb')
    connection = ibis.duckdb.connect(pipeline.sql_client().credentials.database)
    return connection, pipeline


@app.cell
def __(connection):
    # List all tables to see what's available
    tables = connection.list_tables()
    print("Available tables:", tables)
    
    # Filter for authors table
    authors_tables = [t for t in tables if 'authors' in t]
    print("Authors tables:", authors_tables)
    
    return authors_tables, tables


@app.cell
def __(authors_tables, connection):
    # Use the first authors table found
    if authors_tables:
        authors_table = connection.table(authors_tables[0])
        
        # Count books by author and get top 10
        top_authors = (
            authors_table
            .group_by('value')
            .aggregate(book_count=ibis._.count())
            .order_by(ibis.desc('book_count'))
            .limit(10)
            .execute()
        )
        
        top_authors
    else:
        top_authors = None
        print("No authors table found")
    
    return authors_table, top_authors


@app.cell
def __(px, top_authors):
    # Create bar chart visualization if data exists
    if top_authors is not None and len(top_authors) > 0:
        fig = px.bar(
            top_authors, 
            x='value', 
            y='book_count',
            title='Top 10 Authors by Book Count',
            labels={'value': 'Author', 'book_count': 'Number of Books'}
        )
        
        fig.update_layout(xaxis_tickangle=-45)
        fig.show()
    else:
        print("No data to visualize")
        fig = None
    
    return fig,


if __name__ == "__main__":
    app.run()