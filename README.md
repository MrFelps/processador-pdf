# Processador de Comprovantes Santander (A/T)

![Plataformas](https://img.shields.io/badge/Plataforma-Windows%20%7C%20macOS%20%7C%20Linux-blue)
![Python](https://img.shields.io/badge/Python-3.9+-brightgreen.svg)
![Licença](https://img.shields.io/badge/Licen%C3%A7a-MIT-green.svg)

Ferramenta de linha de comando (CLI) desenvolvida em Python para automatizar a extração do número de A/T (número de compromisso) de comprovantes de pagamento do Banco Santander.

## Sobre o Projeto

Em muitos fluxos de trabalho, tarefas aparentemente pequenas consomem um tempo valioso. A renomeação manual de dezenas de **comprovantes de pagamento do Banco Santander** é um desses processos. Um funcionário pode levar um período considerável do seu dia abrindo cada PDF para encontrar o **"número de A/T" (número de compromisso)** e usar esse código para renomear o arquivo.

A ideia deste projeto é simples: **eliminar completamente esse trabalho manual**. Mesmo que a automação salve "apenas" alguns minutos por dia, o ganho acumulado em produtividade e a redução de erros representam uma diferença significativa no final do mês.

Esta ferramenta de linha de comando foi criada para ser a solução: um script rápido, preciso e automático que executa essa tarefa em segundos.

## Funcionalidades Principais

* **Extração Híbrida:** Utiliza PyMuPDF para texto digital e Tesseract (via OCR) para PDFs baseados em imagem.
* **Lógica Específica:** As regras de busca são otimizadas para encontrar o "número de compromisso cliente" no padrão dos comprovantes do Santander.
* **Processamento em Lote:** Renomeia múltiplos arquivos de uma só vez.
* **Interface de Terminal (CLI):** Permite o uso flexível com qualquer pasta de entrada e saída através de argumentos de linha de comando.
* **Relatório Detalhado:** Exibe um resumo da execução, informando sucessos e falhas.

## Metodologia de Desenvolvimento

Este projeto foi construído com base em uma arquitetura e lógica concebidas por um desenvolvedor humano. A Inteligência Artificial foi empregada como uma ferramenta de codificação de alta eficiência, materializando as especificações através de prompts detalhados e iterativos.

## Ambiente de Desenvolvimento

### Pré-requisitos
* Python 3.9+
* Git
* Tesseract OCR
* Poppler

### Instalação
1.  Clone o repositório:
    ```bash
    git clone [https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git](https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git)
    cd SEU_REPOSITORIO
    ```
2.  Crie e ative o ambiente virtual:
    ```bash
    # Criar
    python -m venv venv

    # Ativar (Windows)
    .\venv\Scripts\Activate.ps1

    # Ativar (macOS/Linux)
    source venv/bin/activate
    ```
3.  Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

## Uso da Ferramenta

Execute o script `processador_cli.py` a partir do terminal. A principal instrução que você deve fornecer é o caminho para a pasta que contém os PDFs a serem processados.

### Comando Básico

Este comando processa os PDFs de uma pasta de entrada e salva os resultados em um diretório padrão chamado `pdfs_renomeados`.

**Formato:**
```powershell
python processador_cli.py "CAMINHO_PARA_SUA_PASTA_DE_PDFS"
```

**Explicação:**
Você **deve substituir** `"CAMINHO_PARA_SUA_PASTA_DE_PDFS"` pelo caminho real da pasta em seu computador.

**Exemplo Prático:**
Se seus comprovantes estão em uma pasta chamada `Comprovantes_Outubro` na sua Área de Trabalho, o comando no Windows seria:
```powershell
python processador_cli.py "C:\Users\SeuNome\Desktop\Comprovantes_Outubro"
```

### Especificando uma Pasta de Saída (Opcional)

Use o indicador `-o` (ou `--output`) para definir um local específico para salvar os arquivos processados.

**Formato:**
```powershell
python processador_cli.py "CAMINHO_DE_ENTRADA" -o "CAMINHO_DE_SAIDA"
```

**Exemplo Prático:**
```powershell
python processador_cli.py "C:\Users\SeuNome\Desktop\Comprovantes_Outubro" -o "C:\Documentos\Relatorios\Outubro_Processado"
```

### Ver Ajuda

Para ver todas as opções disponíveis, use o argumento `-h`.
```powershell
python processador_cli.py -h
```

## Estrutura do Projeto

O código é separado em dois módulos para melhor organização:

* `core.py`: Contém a classe `PDFCompromissoExtractor`, que é o "motor" com toda a lógica de extração e processamento dos arquivos.
* `processador_cli.py`: Responsável pela interface com o usuário via linha de comando (usando `argparse`) e por orquestrar a execução.
* 
