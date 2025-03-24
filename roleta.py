from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
from collections import Counter

brave_path = 'C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe'

options = Options()
options.binary_location = brave_path

driver = webdriver.Chrome(options=options)

url = 'https://play.livetables.io/roulette/?table_id=241000&game_id=3&identifier=10530023C06683DCEAAAB0E3B5B4FCF0234D2284BFF05D6CBC38CDFA18F500C5F82F196A29BA72B475A0048C&token=C06683DCEAAAB0E3B5B4FCF0234D2284BFF05D6CBC38CDFA18F500C5F82F196A29BA72B475A0048C&limit_id=0&operatorId=10530023'
driver.get(url)
time.sleep(5)

numeros_anteriores = []

def encontrar_numero_mais_repetido(numeros):
    frequencias = Counter(numeros)
    numero_mais_repetido = frequencias.most_common(1)[0][0]
    return numero_mais_repetido

def gerar_apostas_vizinhos(numeros_sorteados, numero_mais_repetido, ultimo_numero_sorteado, primeiro_numero):
    roleta_vizinhos = {
        0: [32, 15, 26, 3], 1: [20, 14, 33, 16], 2: [21, 4, 25, 17], 3: [26, 0, 35, 12], 4: [19, 15, 21, 2],
        5: [24, 16, 10, 23], 6: [34, 17, 27, 13], 7: [28, 12, 29, 18], 8: [30, 11, 23, 10], 9: [22, 18, 31, 14],
        10: [5, 24, 23, 8], 11: [36, 13, 30, 8], 12: [35, 3, 28, 7], 13: [27, 6, 36, 11], 14: [31, 9, 20, 1],
        15: [32, 0, 19, 4], 16: [33, 1, 24, 5], 17: [25, 2, 34, 6], 18: [29, 7, 22, 9], 19: [15, 32, 4, 21],
        20: [14, 31, 1, 33], 21: [4, 19, 2, 25], 22: [18, 29, 9, 31], 23: [10, 5, 8, 30], 24: [16, 33, 5, 10],
        25: [2, 21, 17, 34], 26: [0, 32, 3, 35], 27: [6, 34, 13, 36], 28: [12, 35, 7, 29], 29: [7, 28, 18, 22],
        30: [11, 36, 8, 23], 31: [9, 22, 14, 20], 32: [0, 26, 15, 19], 33: [1, 20, 16, 24], 34: [17, 25, 6, 27],
        35: [12, 28, 3, 26], 36: [13, 27, 11, 30]
    }

    apostas_sugeridas = []

    if primeiro_numero not in apostas_sugeridas:
        apostas_sugeridas.append(primeiro_numero)

    for num in numeros_sorteados:
        if num in roleta_vizinhos:
            for vizinho in roleta_vizinhos[num]:
                if vizinho not in apostas_sugeridas:
                    apostas_sugeridas.append(vizinho)

    if ultimo_numero_sorteado not in apostas_sugeridas:
        apostas_sugeridas.append(ultimo_numero_sorteado)

    if numero_mais_repetido not in apostas_sugeridas:
        apostas_sugeridas.append(numero_mais_repetido)

    return sorted(apostas_sugeridas[:24])

def exibir_apostas(apostas):
    apostax = ", ".join(map(str, apostas)) 
    print(f"Apostas sugeridas: {apostax}")
    print()

def solicitar_autorizacao():
    while True:
        resposta = input("Deseja autorizar as apostas sugeridas? (s/n): ").strip().lower()
        if resposta == "s" or resposta == "sim":
            print(f"\033[0;30;44mROBÔ <HALLYSSON C0D3R> REALIZANDO APOSTA\033[m")
            return True
        elif resposta == "n" or resposta == "nao":
            print("Aguardando novas apostas...")
            print()
            return False
        else:
            print("Resposta inválida. Por favor, digite 's' ou 'n'.")
            print()

try:
    while True:
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        numeros_roleta = soup.find_all('div', attrs={'data-name': 'previous-spins-stack'})

        if not numeros_roleta:
            print("Nenhum número de roleta encontrado. Verifique a estrutura da página.")
        else:
            novos_numeros = []
            for elemento in numeros_roleta:
                for numero in elemento.find_all(['span', 'p', 'div']):
                    if numero.get_text(strip=True).isdigit():
                        novos_numeros.append(int(numero.get_text(strip=True)))

            numeros_novos = [num for num in novos_numeros if num not in numeros_anteriores]

            if numeros_novos:
                numeros_anteriores = novos_numeros + numeros_anteriores
                numeros_str = ", ".join(map(str, numeros_anteriores[:10]))
                print(f"Número que saiu: {numeros_anteriores[0]}")
                print(f"Resultados anteriores: {numeros_str}")

                ultimo_numero_sorteado = novos_numeros[-1]
                numero_mais_repetido = encontrar_numero_mais_repetido(numeros_anteriores)
                primeiro_numero = numeros_anteriores[0]
                apostas = gerar_apostas_vizinhos(numeros_anteriores, numero_mais_repetido, ultimo_numero_sorteado, primeiro_numero)
                exibir_apostas(apostas)

                if solicitar_autorizacao():
                    for numero in apostas:
                        tentativa = 0
                        sucesso = False
                        while tentativa < 100 and not sucesso:
                            try:
                                div_aposta = WebDriverWait(driver, 10).until(
                                    EC.element_to_be_clickable((By.ID, f'index-{100 + numero}'))
                                )
                                div_aposta.click()
                                print(f"Apostando no número {numero}")
                                sucesso = True
                            except Exception as e:
                                tentativa += 1
                                if tentativa >= 100:
                                    print(f"Erro ao tentar apostar no número {numero}. Tentativas esgotadas.")
                    print(f"\033[0;30;44mAPOSTA REALIZADA\033[m")
                    print()

        time.sleep(2)

except KeyboardInterrupt:
    print("Monitoramento interrompido.")
    driver.quit()
