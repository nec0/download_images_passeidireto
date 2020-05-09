import time
import os
import urllib.request
import img2pdf

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.firefox.options import Options


def open_url(url, nome, quant_paginas):
    option = Options()
    option.headless = True
    browser = webdriver.Chrome(chrome_options=option)
    # driver = webdriver.Firefox(options=option)

    browser.maximize_window()
    browser.get(url)
    
    src = browser.find_element_by_xpath("/html/body/div[1]/div/main/div/div/section/div[1]/div/div/div[1]/div/div/img").get_attribute("src")
    info = src[41:77]

    os.mkdir(nome)

    for page in range(1, quant_paginas+1):
        url_ = f'https://files.passeidireto.com/{info}/bg{page}.png'
        browser.get(url_)

        time.sleep(3)
        src = browser.find_element_by_xpath("/html/body/img").get_attribute("src")

        time.sleep(2)
        urllib.request.urlretrieve(src, f'./{nome}/{nome}_{page}.png') 
        print(f'{nome}_{page}.png -> Salva')


def img_pdf(nome):
    # A4
    a4inpt = (img2pdf.mm_to_pt(210),img2pdf.mm_to_pt(297))
    layout_fun = img2pdf.get_layout_fun(a4inpt)

    dirname = str(os.path.abspath(os.path.dirname(__file__))+f"/{nome}")
    with open(f"{nome}.pdf","wb") as f:
        imgs = []
        for fname in os.listdir(dirname):
            if not fname.endswith(".png"):
                continue
            path = os.path.join(dirname, fname)
            if os.path.isdir(path):
                continue
            imgs.append(path)
        f.write(img2pdf.convert(imgs, layout_fun=layout_fun))


def main():
    print(("\nDOWNLOAD DE IMAGENS DO PASSEIDIRETO\n\n")
            +('Passo a passo:\n')
            +('[1] Insira a Url do material\n')
            +('[2] Nome para identificar as imagens baixadas\n')
            +('[3] Quantidade de páginas\n')
            +('[4] Reuna as imagens com auxilio da ferramenta nativa do windows, imprimir -> pdf -> salvar \n')
            +('[+] Leia o README\n'))

    time.sleep(3)
    print('-> INFORMAÇÕES <-')
    url = str(input('URL: '))
    nome = str(input('Nome: '))
    quant_paginas = int(input('Quantidade de páginas: '))

    open_url(url, nome, quant_paginas)

    convert_pdf = str(input('\nCONVERTER EM PDF? (SIM/NÃO) ')).upper()
    if convert_pdf == 'SIM':
        img_pdf(nome)
        print('Imagens e PDF salvos!')
    else:
        print('Ok, imagens salvas!')


main()
