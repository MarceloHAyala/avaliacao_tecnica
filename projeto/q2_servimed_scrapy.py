import sys
import json
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.http import Request

class ServimedSpider(scrapy.Spider):
    name = 'servimed'
    allowed_domains = ['servimed.com.br']

    def __init__(self, pedido_id=None, *args, **kwargs):
        super(ServimedSpider, self).__init__(*args, **kwargs)
        self.pedido_id = pedido_id
        self.output_data = {} 

    def start_requests(self):
        login_url = 'https://pedidoeletronico.servimed.com.br/api/auth/login'
        
        payload = {
            'username': 'juliano@farmaprevonline.com.br',
            'password': 'a007299A'                        
        }

        yield Request(
            url=login_url,
            method='POST',
            body=json.dumps(payload),
            headers={'Content-Type': 'application/json'},
            callback=self.after_login,
            errback=self.login_error,
            dont_filter=True
        )

    def after_login(self, response):
        if response.status == 200:
            token = json.loads(response.text).get('token')
            pedido_url = f'https://pedidoeletronico.servimed.com.br/api/pedidos/{self.pedido_id}'
            
            yield Request(
                url=pedido_url,
                headers={
                    'Authorization': f'Bearer {token}',
                    'Content-Type': 'application/json'
                },
                callback=self.parse_pedido,
                errback=self.pedido_error
            )
        else:
            self.logger.warning("Login não autorizado.")

    def parse_pedido(self, response):
        try:
            data = json.loads(response.text)
            
            self.output_data = {
                "pedido": self.pedido_id,
                "motivo": data.get('status', 'Status Desconhecido'),
                "itens": []
            }
            
            for item in data.get('itens', []):
                self.output_data['itens'].append({
                    "codigo_produto": item.get('codigo'),
                    "descricao": item.get('descricao'),
                    "quantidade_faturada": item.get('qtd_faturada', 0)
                })
                
        except Exception as e:
            self.output_data = {"erro": f"Falha ao processar JSON do pedido: {str(e)}"}

    def login_error(self, failure):
        self.logger.error(f"Erro de conexão no Login: {failure.value}")

    def pedido_error(self, failure):
        self.logger.error(f"Erro ao buscar pedido {self.pedido_id}: {failure.value}")
        self.output_data = {"erro": "Pedido não encontrado no site."}

    def closed(self, reason):
        filename = f"pedido_{self.pedido_id}.json"
        
        if not self.output_data:
            self.output_data = {
                "pedido": self.pedido_id,
                "erro": "Não foi possível extrair dados (Login falhou ou erro na requisição)."
            }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.output_data, f, ensure_ascii=False, indent=4)
        
        self.logger.info(f"Arquivo gerado: {filename}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("ERRO: Informe o número do pedido.")
        sys.exit(1)

    pedido_arg = sys.argv[1]

    process = CrawlerProcess(settings={
        'LOG_LEVEL': 'INFO',
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)',
        'FEED_EXPORT_ENCODING': 'utf-8'
    })

    process.crawl(ServimedSpider, pedido_id=pedido_arg)
    process.start()