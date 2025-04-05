# Django_Projeto_E-commerce
Protótipo de E-commerce desenvolvido com Django. 
Sistema completo com cadastro de usuários, catálogo de produtos, carrinho de compras e painel administrativo. 
A parte de pagamento ainda não foi implementada.

# Protótipo de E-commerce com Django

Este projeto é um protótipo funcional de uma aplicação de e-commerce desenvolvida com o framework **Django**. Ele possui funcionalidades essenciais de uma loja virtual, como cadastro de usuários, catálogo de produtos, carrinho de compras e painel administrativo. A funcionalidade de pagamento ainda não foi implementada, mas a estrutura já está preparada para futuras integrações.

---

## Funcionalidades

- ✅ Cadastro e login de usuários
- ✅ Catálogo de produtos com visualização detalhada
- ✅ Carrinho de compras com adição e remoção de itens
- ✅ Painel administrativo completo (Django Admin)
- ✅ Layout responsivo com HTML, CSS
- 🚫 Pagamento online (em desenvolvimento)

---

## Tecnologias utilizadas

- Python 3
- Django
- SQLite
- HTML5 & CSS3
- Git & GitHub

---

## Como rodar o projeto localmente

### 1. Clone o repositório
git clone https://github.com/seu-usuario/ecommerce-django.git
cd ecommerce-django

### 2. Crie e ative um ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

### 3. Instale as dependências
pip install -r requirements.txt

### 4. Aplique as migrações
python manage.py migrate

### 5. Crie um superusuário (para acessar o admin)
python manage.py createsuperuser

### 6. Inicie o servidor
python manage.py runserver

Acesse a aplicação em: http://localhost:8000
