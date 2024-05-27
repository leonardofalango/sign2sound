# Sign2Sound

## Descrição
Sign2Sound é um projeto que visa fornecer uma ferramenta de comunicação para pessoas surdas ou com deficiência auditiva. A ferramenta pode ser integrada a softwares de vídeo-chamadas e tem como objetivo reconhecer gestos da Linguagem de Sinais Americana (ASL) e traduzi-los para aqueles que não entendem a linguagem de sinais, facilitando assim a comunicação entre pessoas com e sem deficiência.

## Funcionalidades
- Reconhecimento de gestos da Linguagem de Sinais Americana (ASL).
- Tradução dos gestos reconhecidos para texto ou fala.
- Integração com softwares de vídeo-chamadas.

## Tecnologias Utilizadas
- Python
- Mediapipe
- OpenCV
- Machine Learning
- Neural Networks
- Scikit-learn
- Uvicorn

## Instalação
1. Clone o repositório:
git clone https://github.com/seu-usuario/Sign2Sound.git

2. Navegue até o diretório do projeto:
cd Sign2Sound

3. Instale as dependências:
pip install -r requirements.txt


## Uso
- Execute o script principal do projeto:
python main.py
- Com uvicorn:
uvicorn main:app --host 0.0.0.0 --port 8000
- Sem host
python img_pipeline.py
