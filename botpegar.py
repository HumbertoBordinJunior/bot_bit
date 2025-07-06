import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Ler o Excel
df = pd.read_excel(r'C:\Users\Chamy\OneDrive\Documentos\Curo JS\Pythom\OCR PROJETO\operadriver_win64\dados.xlsx')
df.columns = df.columns.str.strip()  # Remove espaços das colunas

# Loop pelos usuários
for index, row in df.iterrows():
    try:
        usuario = str(row['usuario'])
        senha = str(row['senha'])

        print(f"\n[→] Iniciando login do usuário: {usuario}")

        # Inicializar navegador em modo anônimo
        options = webdriver.EdgeOptions()
        options.add_argument("--incognito")
        driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)
        wait = WebDriverWait(driver, 15)

        driver.get("https://www.bit-br.com/#/")

        # Preencher o campo de usuário
        campo_usuario = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@type="text" and contains(@class, "uni-input-input")]')))
        campo_usuario.clear()
        campo_usuario.send_keys(usuario)

        # Preencher o campo de senha
        campo_senha = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@type="password" and contains(@class, "uni-input-input")]')))
        campo_senha.clear()
        campo_senha.send_keys(senha)
        time.sleep(2)

        # Clicar no botão "Conecte-se"
        botao_conectar = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[contains(@class, "submitBtn") and text()="Conecte-se"]')))
        botao_conectar.click()
        time.sleep(2)

        # Clicar no botão da navegação
        botao_navegacao = wait.until(EC.element_to_be_clickable((By.XPATH, '//img[contains(@src, "tab3b.png")]')))
        botao_navegacao.click()

        # Clicar em "Especial"
        botao_especial = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class="item" and contains(text(), "Especial")]')))
        botao_especial.click()

        # Clicar no botão "Pegar"
        try:
            botao_pegar = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='txt' and text()='Pegar']")))
            driver.execute_script("arguments[0].scrollIntoView();", botao_pegar)
            botao_pegar.click()
            print(f"[✓] Usuário {usuario}: clique em 'Pegar' realizado com sucesso.")
        except:
            print(f"[!] Usuário {usuario}: não foi possível clicar no botão 'Pegar'.")

        ##confirmar o botao 
        print(f"[✓] Usuário {usuario} finalizado.")
        time.sleep(3)

    except Exception as e:
        print(f"[X] Erro com o usuário {usuario}: {e}")

    finally:
        # Fecha o navegador antes de ir para o próximo
        driver.quit()

