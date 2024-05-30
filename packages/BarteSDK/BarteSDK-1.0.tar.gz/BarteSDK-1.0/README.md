# BarteSDK

Bem-vindo ao BarteSDK, a solução oficial para integração com as APIs de pagamento da Barte, projetada para simplificar e acelerar o desenvolvimento de aplicações fintech. Com nosso SDK, você pode facilmente integrar funcionalidades de pagamento, assinaturas, e gestão de compradores em sua aplicação.

## Recursos do SDK

O BarteSDK fornece métodos convenientes para interagir com as seguintes APIs:

- **API de Planos**: Facilita o gerenciamento dos planos cadastrados no seu checkout.
- **API de Pedidos**: Permite gerenciar os pedidos cadastrados no seu sistema.
- **API de Compradores**: Auxilia na gestão dos compradores cadastrados.
- **API de Cobranças**: Fornece ferramentas para o gerenciamento das cobranças.
- **API de Assinaturas**: Facilita a criação e gestão de assinaturas.
- **API de Criação de Link de Pagamento**: Permite a geração e gerenciamento de links de pagamento.

## Vantagens do BarteSDK

O BarteSDK foi desenvolvido pensando na eficiência e na otimização do tempo de desenvolvimento, oferecendo uma série de vantagens que vão além da simples integração com nossas APIs. Embora seu uso não seja obrigatório, recomendamos fortemente que você o adote para aproveitar os seguintes benefícios:

- **Mais Eficiência e Redução de Custos**: Implementar nosso SDK significa reduzir custos operacionais e de desenvolvimento. Ele já está pronto para uso e totalmente homologado pela Barte, garantindo que você esteja sempre alinhado com as melhores práticas e padrões do mercado.

- **Instalação Otimizada**: Facilitamos a instalação com nossa solução plug-and-play, que se integra perfeitamente a sistemas de gestão de pacotes como Composer, Gradle, Maven e NPM. Isso agiliza significativamente a integração do SDK ao seu projeto, economizando tempo valioso de desenvolvimento.

- **Construção de Requisições Simplificada**: Simplifique a construção de suas requisições com nossa interface intuitiva. O SDK foi projetado para minimizar a complexidade, otimizar o desenvolvimento e garantir uma implementação eficaz e livre de erros.

- **Segurança de Dados**: A segurança é uma prioridade absoluta no BarteSDK. Utilizamos as melhores práticas e padrões de segurança para proteger todas as informações transmitidas, garantindo a integridade e confidencialidade dos dados dos seus clientes.

Adotar o BarteSDK não é apenas uma questão de conveniência; é uma decisão estratégica que fortalece a segurança, reduz custos e aumenta a eficiência do desenvolvimento de software na sua organização.


## Como Começar

Para começar a usar o BarteSDK, siga os passos abaixo:

1. **Instalação**

   Instale o SDK via pip:

   ```bash
   pip install bartesdk

2. **Uso**

Para usar o charge.list_by_uuid, que lista a cobrança passando como parâmetro o UUID, siga os passos abaixo:

### Código de Exemplo

```python
from bartesdk import BarteSDK

api_key = 'your-api-token'
api_client = BarteSDK(api_key, env="sandbox", api_version="v2")

response = api_client.charges.list_by_uuid(
    charge_uuid='fcb169c5-1238-45de-9d44-acdc858b021e'
)
print(response)
```
### Variáveis `api_client`
- `env`: prd ou sandbox.
- `api_version`: Versão da API ( v1 ou v2 ).
- `api_key`: API Token para autenticação.

## `Recursos e Métodos disponíveis`

### `buyers`

Gerencie os perfis dos compradores registrados no seu sistema de maneira eficiente. Esta API permite criar novos registros, listar os existentes, atualizar informações e excluir dados conforme necessário. Facilita a administração completa dos perfis, assegurando que as informações estejam sempre atualizadas e acessíveis.

##### `create`
####
Adicione novos compradores ao sistema com todas as informações necessárias.
####
Parâmetros:

- `document`: RG ou CPF
- `name`: Nome Completo
- `email`: Endereço de e-mail
- `httpMethod`: POST
- `phone`: Telefone no formato ddd+número, exemplo 11954706482

##### `list`
####
Este método retorna uma lista de compradores registrados associados ao usuário logado.
####
Parâmetros:

- `name`: Nome Completo
- `document`: RG ou CPF
- `email`: Endereço de e-mail

##### `listByUuid`
####
Este método retorna os detalhes de um comprador específico identificado pelo seu UUID, caso o registro esteja presente na base de dados.
####
Parâmetros:

- `uuid`: uuid do Buyer

##### `update`
####
Este método atualiza os detalhes de um comprador específico identificado pelo seu UUID, caso o registro exista na base de dados e os parâmetros fornecidos sejam válidos.
####
Parâmetros:

- `uuid`: uuid do Buyer a ser atualizado


### `charges`

Gerencie as cobranças registradas no seu sistema, permitindo a criação, listagem, atualização, estorno e cancelamento de cobranças de forma eficiente e segura.
####

##### `listByUuid`
####
Este método retorna os detalhes de uma cobrança específica identificada pelo seu UUID, caso o UUID esteja presente na base de dados
####
Parâmetros:

- `uuid`: UUID da Cobrança.

##### `list`
####
Este método retorna uma lista de cobranças cadastradas para o usuário logado, permitindo a pesquisa por datas de expiração. Pode filtrar as cobranças a partir de uma data inicial, até uma data final, ou dentro de um intervalo de datas especificado.
####
Parâmetros:

- `paymentMethod`: Método de pagamento.
- `expirationDateInitial`: Data inicial de expiração do pagamento.
- `expirationDateFinal`: Data final de expiração do pagamento.
- `status`: Status atual do pagamento.
- `notificationEmail`: E-mail para notificação sobre o status do pagamento.
- `customerDocument`: Documento de identificação do cliente.

##### `refund`
####
Este método permite estornar (refund) uma cobrança específica identificada pelo seu ID. Ele verifica se o ID da cobrança está presente na base de dados e, em caso afirmativo, processa o estorno da cobrança, marcando-a como fraude se especificado.
####
Parâmetros:

- `uuid`: UUID da Cobrança.

### `plans`

Gerencia os planos de pagamento cadastrados no seu sistema de checkout. Com esta biblioteca, você pode criar novos planos, listar todos os planos cadastrados, atualizar detalhes de planos existentes e excluir planos conforme necessário. Ideal para administrar diversos tipos de planos de assinatura ou pagamento recorrente, garantindo flexibilidade e controle total sobre as opções de pagamento oferecidas aos seus clientes.
####

##### `listByUuid`
####
Retorna os detalhes de um plano específico identificado pelo seu UUID, caso o registro esteja presente na base de dados. É útil para recuperar informações detalhadas de um plano específico usando um identificador único.
####
Parâmetros:

- `uuid`: UUID do plano.

##### `create`
####
Cria um novo plano de pagamento no sistema com base nos parâmetros fornecidos.
####
Parâmetros:

- `title`
- `description`
- `active`
- `bullets`
- `values`
- `acceptPaymentMethods`

Exemplo:


```python
from bartesdk import BarteSDK


api_key = 'your-api-token'
api_client = BarteSDK(api_key, env="sandbox", api_version="v1")


title = "Plano-Mensalidade-ClienteABC"
description = "Plano utilizado para cobrar mensalidades dos alunos ABC"
active = False
bullets = [
    {
        "description": "Descrição do alunos ABC"
    }
]
values = [
    {
        "type": "MONTHLY",
        "valuePerMonth": 1000
    }
]
accept_payment_methods = [
    "CREDIT_CARD",
    "BANK_SLIP",
    "PIX"
]

status_code, response = api_client.plans.create(
    title=title,
    description=description,
    active=active,
    bullets=bullets,
    values=values,
    accept_payment_methods=accept_payment_methods
)

# Verifique o resultado da operação
if status_code == 201:
    print("Plano criado com sucesso.")
    print(response)
else:
    print(f"Falha ao criar o plano. Status Code: {status_code}")
    print(response)
```

##### `list`
####
Retorna uma lista de todos os planos de pagamento cadastrados no sistema para o usuário logado.
####
Exemplo:

```python
from bartesdk import BarteSDK

api_key = 'your-api-token'
api_client = BarteSDK(api_key, env="sandbox", api_version="v2")

response = api_client.plans.list(
)
print(response)
```

##### `update`
####
Atualiza os detalhes de um plano específico identificado pelo seu UUID. Atualiza o plano se o ID estiver presente na base de dados e os parâmetros fornecidos forem válidos.
####
Exemplo:

```python
from bartesdk import BarteSDK

# Defina seu token da API
api_key = 'your-api-token'

# Crie uma instância da classe BarteSDK
api_client = BarteSDK(api_key, env="sandbox", api_version="v1")

# Defina o UUID do plano a ser atualizado
uuid = '251929af-8903-4875-b26e-809913ddd4db'

# Defina os novos dados do plano a ser atualizado
title = "Titulo do Plano852"
description = "Descrição do Plano852"
active = False
bullets = [
    {
        "description": "Atributo de destaque desse plano852"
    }
]
values = [
    {
        "type": "MONTHLY",
        "valuePerMonth": 2000
    }
]
accept_payment_methods = [
    "CREDIT_CARD",
    "BANK_SLIP",
    "PIX"
]

# Chame a função update para atualizar o plano
status_code, response = api_client.plans.update(
    uuid=uuid,
    title=title,
    description=description,
    active=active,
    bullets=bullets,
    values=values,
    accept_payment_methods=accept_payment_methods
)
```

