def busca_data_agora():
    import datetime as dt

    data_agora = dt.datetime.now()
    data_agora = data_agora.strftime("%Y-%m-%d %H:%M:%S")

    return data_agora