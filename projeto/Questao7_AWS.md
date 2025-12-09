A relação entre esses componentes é hierárquica e de segurança, fundamental para o isolamento e controle de tráfego na nuvem AWS.

1. Definições e Hierarquia

    VPC (Virtual Private Cloud): É a camada macro. Representa uma rede virtual isolada logicamente dentro da nuvem AWS, onde definimos o intervalo de endereços IP (CIDR block) para todos os recursos (Ex: 10.0.0.0/16). É o "container" de rede da sua infraestrutura.

    Subnets (Sub-redes): São segmentações da VPC. A VPC é dividida em subnets para organizar recursos e definir rotas de tráfego. Cada subnet reside em uma única Zona de Disponibilidade (AZ).

        Exemplo: Uma "Subnet Pública" (com acesso à internet via Internet Gateway) para o Load Balancer e uma "Subnet Privada" (sem acesso direto externo) para o Banco de Dados.

    Security Groups (Grupos de Segurança): Atuam como um firewall virtual a nível de instância (interface de rede). Eles não operam na subnet inteira, mas sim protegendo o recurso específico (como uma instância EC2 ou RDS) que está dentro da subnet.

2. A Relação entre eles

A relação funciona da seguinte forma:

    Você cria uma VPC para estabelecer sua rede privada.

    Dentro da VPC, você cria Subnets para segregar sua rede (ex: separar camadas web de camadas de dados).

    Ao lançar uma instância (servidor), você a coloca obrigatoriamente dentro de uma Subnet.

    Para proteger essa instância, você associa um Security Group a ela. O Security Group funciona como a última linha de defesa, permitindo explicitamente apenas o tráfego necessário (ex: permitir porta 80 para web e bloquear todo o resto), independentemente das regras da Subnet.

Portanto, a VPC é a rede, a Subnet é a segmentação dessa rede, e o Security Group é o firewall que protege o recurso individual hospedado nessa subnet.