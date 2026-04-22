# 🎥 Escala Mídia - Igreja

Um sistema web simples e direto para organizar a escala de voluntários da equipe de mídia da igreja.

## 🚀 O Projeto
O objetivo deste aplicativo é substituir o controle manual de escalas por um sistema onde a liderança cadastra os eventos (com limite de vagas) e os próprios membros acessam pelo celular para sinalizar os dias em que podem servir.

## 🛠️ Tecnologias Utilizadas (MVP)
* **Backend:** Python + Django
* **Banco de Dados:** SQLite (Padrão do Django)
* **Frontend:** HTML/CSS (Templates do Django)

## ⚙️ Como rodar o projeto localmente

Siga os passos abaixo para executar o servidor na sua máquina:

0. Crie o ambiente virtual:
   `python -m venv venv`

1. Ative o ambiente virtual (Windows):
   - Windows: `.\venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

2. Instale as dependências:
   `pip install -r requirements.txt`

3. (Opcional) Aplique as migrações caso tenha baixado o projeto agora:
   `python manage.py migrate`

4. Rode o servidor na porta 8080:
   `python manage.py runserver 8080`

5. Acesse no navegador:
   * Sistema Público: http://127.0.0.1:8080/
   * Painel Administrativo: http://127.0.0.1:8080/admin

## 🔮 Próximos Passos (Roadmap)
- [x] Criação do Banco de Dados (Eventos, Membros, Escalas)
- [x] Regra de limite de vagas por evento
- [x] Tela pública de voluntariado
- [ ] Melhorias na interface (Mensagens de sucesso e tratamento de erros)
- [ ] Containerização com Docker
- [ ] Deploy no Homelab