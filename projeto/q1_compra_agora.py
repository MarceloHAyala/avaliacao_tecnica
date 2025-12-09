import requests
import json
import logging
import base64
import re
import unicodedata
from bs4 import BeautifulSoup

# Bibliotecas de criptografia obrigatórias do teste
from nacl.public import PublicKey, SealedBox
from nacl.encoding import HexEncoder

# Configuração de Logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [ROOT] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("CompraAgora_Real")

class CompraAgoraScraper:
    def __init__(self):
        self.session = requests.Session()
        # Headers de navegador real para evitar bloqueio imediato (WAF)
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'https://www.compra-agora.com/',
            'Origin': 'https://www.compra-agora.com'
        })
        self.base_url = "https://www.compra-agora.com"

    def _get_public_key(self):
        """
        Tenta encontrar a chave pública necessária para o Pynacl.
        Geralmente fica em uma variável global no HTML (window.settings) ou em uma API de config.
        """
        logger.info("Buscando chave pública de criptografia...")
        try:
            # 1. Tenta buscar na página de login/home
            response = self.session.get(f"{self.base_url}/login")
            response.raise_for_status()
            
            # Procura por padrões comuns de chave pública (Geralmente 64 chars hex)
            # Ex: "publicKey":"abcdef..." ou window.key = "..."
            match = re.search(r'["\']?publicKey["\']?\s*[:=]\s*["\']?([a-fA-F0-9]{64})["\']?', response.text)
            
            if match:
                key = match.group(1)
                logger.info(f"Chave pública encontrada: {key[:10]}...")
                return key
            
            # Se não achar no HTML, tenta um endpoint comum de API (Tentativa)
            api_resp = self.session.get(f"{self.base_url}/api/auth/public-key")
            if api_resp.status_code == 200:
                return api_resp.json().get('publicKey')

            logger.warning("Não foi possível encontrar a chave pública automaticamente.")
            return None
        except Exception as e:
            logger.error(f"Erro ao buscar chave pública: {e}")
            return None

    def _encrypt_password(self, public_key_hex, password):
        """Lógica de criptografia Pynacl (SealedBox) exigida."""
        try:
            server_public_key = PublicKey(public_key_hex, encoder=HexEncoder)
            box = SealedBox(server_public_key)
            encrypted = box.encrypt(password.encode('utf-8'))
            return base64.b64encode(encrypted).decode('utf-8')
        except Exception as e:
            logger.error(f"Falha ao criptografar senha: {e}")
            raise e

    def login(self):
        logger.info("Iniciando processo de autenticação...")
        
        # 1. Busca chave
        public_key = self._get_public_key()
        
        # Credenciais REAIS do prompt
        username = "04.502.445/0001-20"
        password_plain = "85243140"
        
        # Prepara a senha (Criptografada ou Plana se não achou chave)
        if public_key:
            password_final = self._encrypt_password(public_key, password_plain)
        else:
            logger.warning("Tentando login sem criptografia (chave não encontrada).")
            password_final = password_plain

        payload = {
            'username': username,
            'password': password_final
        }

        # 2. Envia Login
        try:
            # Endpoint padrão para SPAs e E-commerces modernos
            login_url = f"{self.base_url}/api/login" 
            
            response = self.session.post(login_url, json=payload)
            
            if response.status_code in [200, 204]:
                logger.info("Login realizado com sucesso (Status 200/204).")
                return True
            elif response.status_code == 401:
                logger.error("Falha no login: Credenciais inválidas ou expiradas.")
                return False
            else:
                logger.error(f"Erro no login. Status: {response.status_code}. Resposta: {response.text[:200]}")
                return False

        except Exception as e:
            logger.critical(f"Erro crítico na conexão de login: {e}")
            return False

    def scrape_categories(self):
        categories = [
            "Alimentos", "Bazar", "Bebidas", "Bomboniere", 
            "Cuidados Pessoais", "Roupa e Casa"
        ]
        
        all_products = []

        for category in categories:
            # Slugify: Transforma "Roupa e Casa" em "roupa-e-casa"
            slug = unicodedata.normalize('NFKD', category).encode('ascii', 'ignore').decode('utf-8').lower()
            slug = re.sub(r'[^a-z0-9]+', '-', slug).strip('-')
            
            url = f"{self.base_url}/categoria/{slug}"
            logger.info(f"Acessando categoria: {category} ({url})")

            try:
                response = self.session.get(url)
                if response.status_code != 200:
                    logger.error(f"Falha ao acessar {category}: Status {response.status_code}")
                    continue

                soup = BeautifulSoup(response.content, 'html.parser')

                products_found = soup.select('.product-item, .card, .product-card, .vtex-product-summary-2-x-container')
                
                if not products_found:
                    logger.warning(f"Nenhum produto encontrado na categoria {category}. O layout pode ter mudado.")
                    continue

                for p in products_found:
                    try:
                        # Tenta extrair dados usando múltiplos seletores comuns
                        nome_el = p.select_one('.product-name, .name, h3, .vtex-product-summary-2-x-productNameContainer')
                        fab_el = p.select_one('.brand, .manufacturer, .vtex-product-summary-2-x-brandName')
                        img_el = p.select_one('img')

                        if nome_el:
                            item = {
                                "descricao": nome_el.get_text(strip=True),
                                "descricao_fabricante": fab_el.get_text(strip=True) if fab_el else "Desconhecido",
                                "image_url": img_el.get('src') or img_el.get('data-src') if img_el else ""
                            }
                            all_products.append(item)
                    except Exception as extract_err:
                        continue # Pula produto com erro

            except Exception as e:
                logger.error(f"Erro ao processar categoria {category}: {e}")

        return all_products

    def save_json(self, data):
        if not data:
            logger.warning("Nenhum dado foi coletado. O arquivo JSON estará vazio.")
        
        filename = "produtos.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        logger.info(f"Arquivo gerado: {filename} com {len(data)} produtos.")

if __name__ == "__main__":
    scraper = CompraAgoraScraper()
    
    # Fluxo Real: Se não logar, não raspa.
    if scraper.login():
        dados = scraper.scrape_categories()
        scraper.save_json(dados)
    else:
        logger.error("Abortando scraping devido a falha no login.")