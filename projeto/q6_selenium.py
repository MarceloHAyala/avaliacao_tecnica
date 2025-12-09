import sys
import json
import logging
from time import sleep

# Importações do Selenium e WebDriver Manager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Configuração de Logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger("Q6_Selenium")

class QuotesBot:
    def __init__(self):
        self.base_url = "http://quotes.toscrape.com"
        
        # Configurações do Chrome para rodar no Docker (Headless)
        chrome_options = Options()
    
        # O modo headless é obrigatório em ambientes Docker sem interface gráfica
        chrome_options.add_argument("--headless=new") 
        # ---------------------
        
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        # Instalação automática do driver correto
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def scrape_author(self, author_name):
        logger.info(f"Iniciando busca por: {author_name}")
        self.driver.get(self.base_url)
        
        quotes_data = []
        author_info = {}
        found_author = False

        while True:
            # 1. Captura todas as citações da página atual
            quotes = self.driver.find_elements(By.CLASS_NAME, "quote")
            
            for quote in quotes:
                try:
                    # Verifica se a citação é do autor solicitado
                    name = quote.find_element(By.CLASS_NAME, "author").text
                    
                    if name == author_name:
                        found_author = True
                        text = quote.find_element(By.CLASS_NAME, "text").text
                        tags = [tag.text for tag in quote.find_elements(By.CLASS_NAME, "tag")]
                        
                        quotes_data.append({
                            "text": text,
                            "tags": tags
                        })

                        # 2. Se ainda não temos a biografia, clicamos no "about"
                        if not author_info:
                            logger.info("Autor encontrado. Acessando biografia...")
                            
                            # Estratégia: Pegar o link e abrir em nova aba
                            link_element = quote.find_element(By.LINK_TEXT, "(about)")
                            link_url = link_element.get_attribute("href")
                            
                            # Abre nova janela
                            self.driver.execute_script("window.open('');")
                            self.driver.switch_to.window(self.driver.window_handles[1])
                            self.driver.get(link_url)
                            
                            # Extrai os dados da página About
                            author_info = {
                                "name": self.driver.find_element(By.CLASS_NAME, "author-title").text,
                                "birth_date": self.driver.find_element(By.CLASS_NAME, "author-born-date").text,
                                "birth_location": self.driver.find_element(By.CLASS_NAME, "author-born-location").text,
                                "description": self.driver.find_element(By.CLASS_NAME, "author-description").text[:200] + "..."
                            }
                            
                            # Fecha a aba da bio e volta para a principal
                            self.driver.close()
                            self.driver.switch_to.window(self.driver.window_handles[0])

                except Exception as e:
                    logger.error(f"Erro ao processar item: {e}")

            # 3. Paginação: Tenta encontrar e clicar no botão 'Next'
            try:
                next_btn = self.driver.find_element(By.CLASS_NAME, "next")
                link_next = next_btn.find_element(By.TAG_NAME, "a")
                logger.info("Indo para a próxima página...")
                link_next.click()
                sleep(1) 
            except:
                logger.info("Fim das páginas ou botão 'Next' não encontrado.")
                break
        
        self.driver.quit()
        
        if not found_author:
            logger.warning("Autor não encontrado no site.")
            return None

        return {
            "author": author_info,
            "quotes": quotes_data
        }

if __name__ == "__main__":
    target_author = sys.argv[1] if len(sys.argv) > 1 else "J.K. Rowling"
    
    bot = QuotesBot()
    data = bot.scrape_author(target_author)
    
    if data:
        print(json.dumps(data, indent=4, ensure_ascii=False))
        
        with open("quotes_author.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            logger.info("Arquivo quotes_author.json salvo com sucesso.")