# Gerenciador de Cards

Sistema de gerenciamento de cards com autenticação.

## Requisitos

- Python 3.9+
- Flask
- SQLite3

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux
# ou
.\venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure o ambiente:
```bash
cp .env.example .env
# Edite .env com suas configurações
```

5. Execute:
```bash
flask run
```

## Docker

```bash
docker build -t cards-app .
docker run -d -p 5000:5000 cards-app
```

## Uso

1. Acesse http://localhost:5000
2. Login padrão:
   - Usuário: admin
   - Senha: admin123

## Desenvolvimento

Para criar um novo usuário:
```bash
python create_user.py
```

## Contribuindo

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Crie um Pull Request

## Licença

Este projeto está sob a licença MIT.
