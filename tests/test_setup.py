def test_postgres_container_starts(postgres_container):
    connection_url = postgres_container.get_connection_url()
    print("Container connection URL:", connection_url)
    assert connection_url is not None