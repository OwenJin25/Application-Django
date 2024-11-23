# Aplicação de Discussões do Django

## Descrição

Esta aplicação permite aos utilizadores:s
- Criar perfis com biografias e imagens opcionais.
- Publicar tópicos de discussão.
- Comentar em tópicos criados por outros usuários.

O objetivo do sistema é oferecer uma plataforma simples e funcional para interações em tópicos de interesse comum.

---

## Funcionalidades

- **Perfil de Usuário**:
  - Criação automática de perfis para novos usuários.
  - Possibilidade de adicionar uma biografia e uma imagem de perfil.
- **Tópicos de Discussão**:
  - Criação de tópicos com título, descrição e autor.
  - Registro automático da data de criação.
- **Comentários**:
  - Possibilidade de comentar em qualquer tópico.
  - Registro da data e do autor do comentário.

---
## Tecnologias Utilizadas

- **Python 3.8 ou superior**: Linguagem principal do projeto.
- **Django 4.0 ou superior**: Framework web.

## Requisitos

Certifique-se de que você tenha instalado:
- **Python 3.8 ou superior**
- **Django 4.0 ou superior**
- **Pip** 

---

## Instalação e Execução

Siga estas instruções para configurar e executar o projeto no seu ambiente local:

### **1. Clone o Repositório**
Use o seguinte comando para clonar o projeto:
```bash
git clone https://github.com/OwenJin25/Application-Django.git
cd Application-Django
```
### **2. Crie um Ambiente Virtual**

Crie um ambiente virtual para isolar as dependências do projeto.
```bash
python -m venv venv
```

### **3. Instale as Dependências**

Instale todas as bibliotecas necessárias para o projeto usando o arquivo requirements.txt:
```bash
pip install -r requirements.txt
```
### **4. Configure o Base de Dados**

O Django utiliza um Base de dados para armazenar informações. A primeira coisa a fazer é aplicar as migrações para configurar as tabelas no Base de dados.
```bash
## 1. Gerencia as migrações :
python manage.py makemigrations
## 2. Aplique as migrações para configurar as tabelas no base de dados:
python manage.py migrate
```
### **5. Crie um Superutilizador**
Crie um superusuário para acessar o painel administrativo do Django:

```bash
python manage.py createsuperuser
```

### **6. Inicie o Servidor**
Inicie o servidor de desenvolvimento do Django para testar a aplicação localmente:

```bash
python manage.py runserver
```