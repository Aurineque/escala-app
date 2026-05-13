# 🎥 Escala Mídia - Igreja

> Um sistema web direto e eficiente para organizar e automatizar a escala de voluntários da equipe de mídia e comunicação da igreja.

---

## 📸 Demonstração
![Tela de Eventos](escala-app.png)

*Interface pública listando os cultos, vagas disponíveis, membros escalados com suas respectivas funções e alerta de lotação máxima.*

---

## 🎯 O Problema que Resolvemos

Substituir planilhas manuais e trocas de mensagens confusas por um sistema *self-service*. A liderança cadastra os cultos e eventos com limites de vagas, e os próprios membros acessam a plataforma pelo celular para sinalizar os dias e as funções em que podem servir.

---

## ✨ Principais Funcionalidades

* **Gestão Centralizada (Admin):** Criação de eventos, controle de membros e visualização rápida das escalas.
* **Inscrição Self-Service:** Interface pública simples para o voluntário escolher o evento e a sua respectiva **Função** na equipe (ex: Câmera, Mesa de Som, Transmissão).
* **Feedback Visual:** Alertas de sucesso ao se voluntariar e tratamento de erros na tela para uma melhor experiência do usuário (UX).
* **Regras de Negócio Inteligentes:**
  * Bloqueio automático ao atingir o limite máximo de voluntários por evento.
  * Prevenção de inscrições duplicadas (o mesmo membro não pode se inscrever duas vezes no mesmo culto).
* **Exibição Dinâmica (Time Window):** O painel de eventos exibe a escala do mês vigente. A partir do dia 25 de cada mês, o sistema faz uma transição automática e passa a exibir também os eventos do mês seguinte, facilitando o planejamento prévio da equipe.

---

## 🛠️ Stack Tecnológica

* **Backend:** Python + Django
* **Banco de Dados:** SQLite (Fácil portabilidade e ideal para o escopo do projeto)
* **Frontend:** HTML/CSS (Templates nativos do Django)
* **Infraestrutura:** Docker e Docker Compose

---

## 🐳 Como rodar o projeto com Docker (Recomendado)

A maneira mais rápida de testar a aplicação é utilizando containers. Certifique-se de ter o Docker e o Docker Compose instalados na sua máquina.

**1. Clone o repositório:**
```bash
git clone https://github.com/Aurineque/escala-app.git
cd escala-app
```

2. Suba os containers em segundo plano:

```bash
docker-compose up --build -d
```

3. Acesse a aplicação:

O sistema estará disponível no seu navegador em http://localhost:8080 (ou a porta configurada no seu arquivo docker-compose.yml).

## ⚙️ Como rodar o projeto localmente (Sem Docker)
Caso prefira rodar usando um ambiente virtual Python (Requer Python 3.10+):

1. Crie e ative o ambiente virtual:

Windows:

```powershell
python -m venv venv
.\venv\Scripts\activate
```

Linux/Mac:

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Aplique as migrações:

```bash
python manage.py migrate
```

4. Rode o servidor:

```bash
python manage.py runserver 8080
```
5. Acesse:

Abra o navegador e acesse http://127.0.0.1:8080/

## 🗺️ Roadmap (Status do Projeto)

[x] Criação da modelagem de Banco de Dados (Eventos, Membros, Escalas).

[x] Regra de limite de vagas e prevenção de duplicidade.

[x] Tela pública de voluntariado com seleção de funções.

[x] Lógica de exibição com janela de transição mensal.

[x] Melhorias na interface UX/UI (Mensagens de sucesso e tratamento de erros).

[x] Conteinerização do projeto (Docker / docker-compose).

[x] Deploy do MVP em ambiente Cloud (PythonAnywhere).

[ ] Migração do banco para PostgreSQL.

[ ] Deploy automatizado no servidor.