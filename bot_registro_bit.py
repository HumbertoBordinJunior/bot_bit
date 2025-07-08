import time
import cv2
import base64
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.service import Service as EdgeService
from nopecha.api.requests import RequestsAPIClient

# Inicializando lista de telefones
telefones = [
    'Coloque os logins aqui ordenado por , '
]

# Inicializa o cliente NopeCHA
api = RequestsAPIClient("API_KEY_NOPECHA")

# Inicializa o navegador EDGE, com a configuração privado 
options = Options()
options.add_argument('--inprivate')
driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)
driver.set_window_size(1920, 1080)

for telefone in telefones:
    driver.get("https://www.bit-br.com/#/pages/login/register")
    wait = WebDriverWait(driver, 50)
    inputs = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'input')))

    captcha_div = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, 'div[style^="position: absolute;"]')))
    captcha_div.screenshot("captcha.png")
    #Manipulação de imagem com o CV2, para melhor clareza
    img = cv2.imread("captcha.png")
    _, buffer = cv2.imencode('.png', img)
    img_bytes = base64.b64encode(buffer).decode()

    resp = api.recognize_textcaptcha(image_data=[img_bytes])
    texto_captcha = resp.get("data", [""])[0].strip()

    if not texto_captcha:
        print(f" captcha não solucionado para {telefone}, pulando.")
        continue

    dados = [telefone, texto_captcha, "SenhaSegura123", "SenhaSegura123", "618EX70A"]

    for campo, valor in zip(inputs, dados):
        campo.clear()
        campo.send_keys(valor)
        time.sleep(0.2)

    print(f"Usuario {telefone} registrado.")

    time.sleep(3)
    botao = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "submitBtn")))
    botao.click()

    img_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//img[contains(@src, "tab2b.png")]')))
    img_btn.click()
    time.sleep(1)

    especial_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class="item" and contains(text(), "Especial")]')))
    especial_btn.click()
    time.sleep(2)

    agarre_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[contains(@class, "btn") and contains(text(), "Agarre-se")]')))
    agarre_btn.click()
    time.sleep(3)

    confirmar_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[contains(@class, "uni-modal__btn_primary") and contains(text(), "Confirmar")]')))
    confirmar_btn.click()
    time.sleep(4)

driver.quit()