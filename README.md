# roleta-api
Este projeto automatiza apostas em uma roleta online utilizando a biblioteca Selenium para interagir com a página da roleta para extrair os números sorteados. O objetivo é sugerir apostas baseadas nos números anteriores, no número mais repetido e nas vizinhanças dos números sorteados.

# Requisitos
- Python 3.x
- Selenium
- BeautifulSoup4
- ChromeDriver (ou outro driver de navegador compatível)

# Dependências
pip install selenium
pip install bs4

Uso o navegador Brave, achei melhor por ele.
A plataforma é a Esporte Da Sorte, uso a roleta EZUGI, e não se esqueça de alterar para 0 colunas (antes de apostar) igual no vídeo.
Em apostas_sugeridas[:24] é a quantidade de números que ele verifica e aposta baseado nos vizinhos.
Se quiser pode aumentar ou baixar, deixei esse que é uma boa média.
