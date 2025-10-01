# Processador e Renomeador de PDFs v1.0 (Beta)

![Plataformas](https://img.shields.io/badge/Plataforma-Windows%20%7C%20macOS%20%7C%20Linux-blue)
![Python](https://img.shields.io/badge/Python-3.9+-brightgreen.svg)
![Licença](https://img.shields.io/badge/Licen%C3%A7a-MIT-green.svg)

Ferramenta de linha de comando (CLI) para automatizar a extração de dados e renomeação de arquivos PDF em lote.

## A Ideia do Projeto

Em muitos fluxos de trabalho, tarefas aparentemente pequenas consomem um tempo valioso. A renomeação manual de dezenas ou centenas de arquivos é um desses processos. Um funcionário pode levar um período considerável do seu dia abrindo cada PDF, encontrando um código específico e renomeando o arquivo.

A ideia deste projeto é simples: **eliminar completamente esse trabalho manual**. Mesmo que salve "apenas" alguns minutos por dia, o ganho acumulado em produtividade e a redução de tarefas repetitivas representam uma grande diferença no final do mês.

Este sistema foi criado para ser essa solução: uma ferramenta rápida, precisa e automática.

## Status da Versão

> **Versão 1.0 (Beta)**
> Este projeto está em uma versão Beta, o que significa que ele está funcional e cumpre seu objetivo principal, mas ainda está em fase de análise e pode receber melhorias futuras.

## Como o Sistema Interage

A interação com o sistema é feita através da linha de comando, de forma direta e eficiente. O fluxo é o seguinte:
1.  O usuário coloca todos os arquivos PDF que deseja processar em uma pasta designada (`meus_pdfs`).
2.  Executa um único comando no terminal.
3.  O script processa cada PDF, utilizando uma abordagem híbrida de extração de texto e OCR para encontrar o "número de compromisso".
4.  Os arquivos são salvos, já renomeados, em uma pasta de saída (`pdfs_renomeados`), e um relatório completo é exibido no terminal.

O tempo de resposta é rápido, processando múltiplos arquivos em questão de segundos.

## Metodologia de Desenvolvimento

Este projeto foi desenvolvido utilizando um fluxo de trabalho moderno e colaborativo entre homem e máquina. A lógica, a arquitetura da solução e os objetivos foram concebidos por um desenvolvedor humano.

A Inteligência Artificial foi utilizada como uma ferramenta de codificação de alta performance, traduzindo as ideias e os requisitos detalhados em código Python funcional através de prompts iterativos. **Todo o crédito pela inteligência e estrutura do projeto pertence ao processo de ideação e especificação humana que guiou a ferramenta de IA.**

## 💻 Compatibilidade de Sistema

Este script é totalmente compatível com os principais sistemas operacionais:
* **Windows**
* **macOS**
* **Linux**

A única exigência é a instalação das dependências externas, que varia conforme o sistema (instruções abaixo).

## 🚀 Guia de Instalação e Uso

### Pré-requisitos
* Python 3.9+
* Git

### 1. Dependências Externas

Você precisa instalar o **Tesseract** (para OCR) e o **Poppler** (para conversão de PDF para imagem).

<details>
<summary><b>Instrução para Windows</b></summary>

1.  **Tesseract:** Baixe e instale a partir [deste link](https://github.com/UB-Mannheim/tesseract/wiki). Durante a instalação, **marque a opção para adicionar ao PATH do sistema**.
2.  **Poppler:** Baixe o arquivo `.zip` mais recente [deste link](https://github.com/oschwartz10612/poppler-windows/releases/latest), descompacte-o em um local fixo (ex: `C:\poppler`) e adicione a pasta `bin` de dentro dele ao PATH do sistema.

</details>

<details>
<summary><b>Instrução para macOS</b></summary>

Use o Homebrew para instalar:
```bash
brew install tesseract tesseract-lang poppler
```

</details>

<details>
<summary><b>Instrução para Linux (Debian/Ubuntu)</b></summary>

Use o `apt-get` para instalar:
```bash
sudo apt-get update
sudo apt-get install -y tesseract-ocr tesseract-ocr-por poppler-utils
```
</details>

### 2. Configuração do Projeto

```bash
# Clone o repositório
git clone [https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git](https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git)
cd SEU_REPOSITORIO

# Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate  # No macOS/Linux
.\venv\Scripts\Activate.ps1 # No Windows

# Instale as bibliotecas Python
pip install -r requirements.txt
```
*(Nota: Você precisará criar um arquivo `requirements.txt` com o conteúdo das bibliotecas que instalamos)*

### 3. Uso

1.  Adicione seus arquivos PDF na pasta `meus_pdfs`.
2.  Execute o script:
    ```bash
    python processador.py
    ```
