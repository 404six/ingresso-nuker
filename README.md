# Prova de Conceito de "Falha" no site ingresso.com

## Conceito da Falha

O sistema de compras do site ingresso.com funciona por meio de sessões, onde cada sessão expira em 8 minutos e há um limite de escolha de 8 lugares por sessão. O problema desse sistema é que, se um usuário mal-intencionado replicar o processo completo de criação de sessão e escolha de lugares de forma automática, ele pode abusar do sistema infinitamente, ocupando todos os lugares disponíveis de uma sessão e impossibilitando outros usuários de comprarem ingressos.

## Dá uma olhada:
![7c8ca4c8-ad58-43e6-b9b0-369c491fd302online-video-cutter com-ezgif com-video-to-gif-converter](https://github.com/404six/ingresso-nuker/assets/82246311/8056acca-01ce-4dbd-b676-b7a68c03e12c)


## Requisitos

- Python 3.x
- Biblioteca `requests`

Você pode instalar as dependências necessárias usando:

```bash
pip install -r requirements.txt
