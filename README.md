# 1. Problema de negócio

A Fome Zero é um marketplace de restaurantes, tendo como principal atribuição promover o encontro e negociações de clientes e restaurantes. Os restaurantes fazem o cadastro dentro da plataforma da Fome Zero, que disponibiliza informações como endereço, tipo de culinária servida, se possui reservas, se faz entregas e também uma nota de avaliação dos serviços e produtos do restaurante, dentre outras informações.

Você acaba de ser contratado como Cientista de Dados da empresa Fome Zero, e a sua principal tarefa nesse momento é ajudar o CEO Kleiton Guerra a identificar pontos chaves da empresa, respondendo às perguntas que ele fizer utilizando análise de dados.

O CEO Guerra também foi recém contratado e precisa entender melhor o negócio para conseguir tomar as melhores decisões estratégicas e alavancar ainda mais a Fome Zero, e para isso, ele precisa que seja feita uma análise nos dados da empresa e que sejam gerados dashboards a partir dessas análises, para responder às seguintes perguntas:

## 1.1. Geral

1. Quantos restaurantes únicos estão registrados?
2. Quantos países únicos estão registrados?
3. Quantas cidades únicas estão registradas?
4. Qual o total de avaliações feitas?
5. Qual o total de tipos de culinária registrados?

## 1.2. País

1. Qual o nome do país que possui mais cidades registradas?
2. Qual o nome do país que possui mais restaurantes registrados?
3. Qual o nome do país que possui mais restaurantes com o nível de preço igual a 4
registrados?
4. Qual o nome do país que possui a maior quantidade de tipos de culinária
distintos?
5. Qual o nome do país que possui a maior quantidade de avaliações feitas?
6. Qual o nome do país que possui a maior quantidade de restaurantes que fazem
entrega?
7. Qual o nome do país que possui a maior quantidade de restaurantes que aceitam
reservas?
8. Qual o nome do país que possui, na média, a maior quantidade de avaliações
registrada?
9. Qual o nome do país que possui, na média, a maior nota média registrada?
10. Qual o nome do país que possui, na média, a menor nota média registrada?
11. Qual a média de preço de um prato para dois por país?

## 1.3. Cidades

1. Qual o nome da cidade que possui mais restaurantes registrados?
2. Qual o nome da cidade que possui mais restaurantes com nota média acima de
4?
3. Qual o nome da cidade que possui mais restaurantes com nota média abaixo de
2.5?
4. Qual o nome da cidade que possui o maior valor médio de um prato para dois?
5. Qual o nome da cidade que possui a maior quantidade de tipos de culinária
distintas?
6. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem
reservas?
7. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem
entregas?
8. Qual o nome da cidade que possui a maior quantidade de restaurantes que
aceitam pedidos online?

## 1.4. Restaurantes

1. Qual o nome do restaurante que possui a maior quantidade de avaliações?
2. Qual o nome do restaurante com a maior nota média?
3. Qual o nome do restaurante que possui o maior valor de uma prato para duas
pessoas?
4. Qual o nome do restaurante de tipo de culinária brasileira que possui a menor
média de avaliação?
5. Qual o nome do restaurante de tipo de culinária brasileira, e que é do Brasil, que
possui a maior média de avaliação?
6. Os restaurantes que aceitam pedido online são também, na média, os
restaurantes que mais possuem avaliações registradas?
7. Os restaurantes que fazem reservas são também, na média, os restaurantes que
possuem o maior valor médio de um prato para duas pessoas?
8. Os restaurantes do tipo de culinária japonesa dos Estados Unidos da América
possuem um valor médio de prato para duas pessoas maior que as churrascarias
americanas (BBQ)?

## 1.5. Culinárias

1. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do
restaurante com a maior média de avaliação?
2. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do
restaurante com a menor média de avaliação?
3. Dos restaurantes que possuem o tipo de culinária americana, qual o nome do
restaurante com a maior média de avaliação?
4. Dos restaurantes que possuem o tipo de culinária americana, qual o nome do
restaurante com a menor média de avaliação?
5. Dos restaurantes que possuem o tipo de culinária árabe, qual o nome do
restaurante com a maior média de avaliação?
6. Dos restaurantes que possuem o tipo de culinária árabe, qual o nome do
restaurante com a menor média de avaliação?
7. Dos restaurantes que possuem o tipo de culinária japonesa, qual o nome do
restaurante com a maior média de avaliação?
8. Dos restaurantes que possuem o tipo de culinária japonesa, qual o nome do
restaurante com a menor média de avaliação?
9. Dos restaurantes que possuem o tipo de culinária caseira, qual o nome do
restaurante com a maior média de avaliação?
10. Dos restaurantes que possuem o tipo de culinária caseira, qual o nome do
restaurante com a menor média de avaliação?
11. Qual o tipo de culinária que possui o maior valor médio de um prato para duas
pessoas?
12. Qual o tipo de culinária que possui a maior nota média?
13. Qual o tipo de culinária que possui mais restaurantes que aceitam pedidos
online e fazem entregas?

O objetivo deste projeto é criar dashboard de forma que exibam essas métricas de maneira mais visual e interativa para que facilite a tomada de decisão do CEO.

# 2. Premissas assumidas para a análise

1. O marketplace foi o modelo de negócio assumido
2. As cinco visões passadas pelo CEO foram divididas em três: Geral, onde há um mapa para promover a interatividade, Regional, onde há as visões de países e cidades e Minimalista, onde há as visões de restaurantes e culinárias.

# 3. Estratégia de solução

O painel estratégico foi desenvolvido utilizando as métricas que refletem as 5 principais visões do modelo de negócio da empresa:

## 3.1. Geral:

1. Quantidade de países cadastrados
2. Quantidade de cidades cadastradas
3. Quantidade de restaurantes cadastrados
4. Quantidade de avaliações registradas
5. Quantidade de culinárias cadastradas

## 3.2. País

1. País com a maior quantidade de cidades registradas
2. País com a maior quantidade de restaurantes registrados
3. País com a maior quantidade de culinárias únicas
4. País com a maior quantidade de restaurantes que fazem entregas
5. País com a maior quantidade de restaurantes que fazem reservas
6. Avaliação média de restaurantes por país
7. Custo médio para duas pessoas por país (em USD)


## 3.3. Cidades

1. 10 cidades com o custo mais alto para duas pessoas
2. 10 cidades com maior variedade de culinárias

## 3.4. Restaurantes

1. Os melhores restaurantes para as culinárias: americana, japonesa, italiana, árabe e caseira com informações de país, cidade e custo médio para duas pessoas
2. Personalizar a culinária para obter o melhor restaurante da culinária de sua escolha

## 3.5. Culinárias

1. As culinárias com a média de avaliação mais alta
2. As culinárias com a média de avaliação mais baixa

# 4. Top 3 insights de dados

1. A Índia é o país que possui mais cidades, restaurantes e culinárias diferentes cadastradas na plataforma.
2. A Singapura é o país com os restaurantes mais caros
3. A média de avaliação dos restaurantes de culinária brasileira é uma das piores (3.47)

# 5. O produto final do projeto

Painel online, hospedado em um Cloud e disponível para acesso em
qualquer dispositivo conectado à internet.

O painel pode ser acessado através desse link: https://caiopolari-fomezero-ftc.streamlit.app/

# 6. Conclusão

O objetivo desse projeto é criar um conjunto de gráficos que exibam essas métricas da melhor forma possível para o CEO.

# 7. Próximos passos

1. Criar mais gráficos que explorem a visão de restaurantes, cidades e países de forma interativa
2. Adicionar mais detalhes no que diz respeito à visão culinárias
