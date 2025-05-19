from cassandra.cluster import Cluster

cluster = Cluster(["127.0.0.1"], port=9042)
cassandra = cluster.connect()

cassandra.execute("""
    CREATE KEYSPACE IF NOT EXISTS mercado_livre
    WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'}
""")

cassandra.set_keyspace("mercado_livre")

cassandra.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id UUID PRIMARY KEY,
        name TEXT,
        price INT,
        description TEXT,
        seller_id UUID,
        seller_name TEXT
    ),
    
    CREATE TABLE IF NOT EXISTS sellers (
        id UUID PRIMARY KEY,
        name TEXT,
        email TEXT,
        cpf TEXT,
        phone TEXT
    ),
    
    CREATE TABLE IF NOT EXISTS users (
        id UUID PRIMARY KEY,
        name TEXT,
        cpf TEXT,
        email TEXT,
        phone TEXT,
        address MAP<TEXT, TEXT>,
        favorites LIST<FROZEN<MAP<TEXT, TEXT>>>
    )
    
    CREATE TABLE IF NOT EXISTS ecommerce_ks.purchases (
        id UUID PRIMARY KEY,
        customer_id UUID,
        customer_name TEXT,
        customer_cpf TEXT,
        products LIST<FROZEN<MAP<TEXT, TEXT>>>,
        status TEXT,
        total_price DECIMAL
    )
""")
