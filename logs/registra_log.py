def registra_log(log, data_hora):
    registro = f"{data_hora}: {log}"
    with open('logs/log.txt', 'a', encoding='utf-8') as f:  # Define a codificação UTF-8
        f.write(registro + '\n')

if __name__ == "__main__":
    registra_log(log="Teste de log com acentuação: çãõ", data_hora="2021-09-01 12:00:00")  # Teste com caracteres especiais
