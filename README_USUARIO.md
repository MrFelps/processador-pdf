# Guia de Utilização via Terminal

Este documento detalha como configurar e utilizar a ferramenta de renomeação de PDFs diretamente pelo terminal do seu computador (Prompt de Comando, PowerShell, Terminal do macOS/Linux, etc.).

## Parte 1: Pré-requisitos Essenciais

Para que o programa funcione, seu computador **obrigatoriamente** precisa ter os seguintes softwares já instalados e configurados em seu sistema:

* **Python** (versão 3.9 ou superior)
* **Tesseract OCR**
* **Poppler**

> **Atenção:** Este guia assume que os programas acima já estão instalados. A instalação destes softwares não é coberta por este documento. Se ocorrerem erros, verifique primeiro a instalação e a configuração destes pré-requisitos.

---

## Parte 2: Configuração do Projeto (Feito Apenas Uma Vez)

Siga os passos abaixo para preparar o programa para o primeiro uso.

#### Passo 1: Baixar o Projeto
1.  Na página do projeto no GitHub, clique no botão verde **`< > Code`**.
2.  Selecione a opção **`Download ZIP`**.
3.  Salve o arquivo e **descompacte a pasta** em um local de fácil acesso no seu computador (por exemplo, na sua Área de Trabalho ou em `C:\Ferramentas\`).

#### Passo 2: Acessar a Pasta do Projeto via Terminal
1.  Abra o terminal do seu sistema operacional.
    * **Windows:** Pesquise por `cmd` ou `PowerShell` no Menu Iniciar.
    * **macOS/Linux:** Pesquise por `Terminal`.
2.  Use o comando `cd` (change directory) para navegar até a pasta que você descompactou.
    * *Exemplo para Windows:*
        ```powershell
        cd C:\Users\SeuUsuario\Desktop\processador-pdf-python-main
        ```
    * *Exemplo para macOS/Linux:*
        ```bash
        cd /Users/SeuUsuario/Desktop/processador-pdf-python-main
        ```

#### Passo 3: Instalar as Dependências do Projeto
Com o terminal aberto na pasta correta, execute os três comandos abaixo, **um de cada vez**, na ordem exata.

1.  **Crie o ambiente virtual** (uma "caixa" isolada para as bibliotecas do projeto):
    ```
    python -m venv venv
    ```

2.  **Ative o ambiente virtual:**
    * No **Windows**:
        ```powershell
        .\venv\Scripts\Activate.ps1
        ```
    * No **macOS/Linux**:
        ```bash
        source venv/bin/activate
        ```
    * *Após este comando, você verá `(venv)` aparecer no início da linha do terminal.*

3.  **Instale as bibliotecas necessárias:**
    ```
    pip install -r requirements.txt
    ```
    * *Aguarde a conclusão da instalação. Isso pode levar alguns minutos.*

Pronto! A configuração está concluída.

---

## Parte 3: Como Usar no Dia a Dia

Agora que tudo está instalado, o uso é simples.

#### Passo 1: Prepare seus Arquivos
* Crie uma pasta em qualquer lugar do seu computador e coloque nela todos os PDFs que deseja processar.

#### Passo 2: Execute o Programa
1.  Abra um novo terminal e navegue novamente até a pasta do projeto (usando o comando `cd`).
2.  **Ative o ambiente virtual** (passo essencial toda vez que for usar):
    ```powershell
    # No Windows
    .\venv\Scripts\Activate.ps1
    ```
3.  Execute o script com o comando abaixo, **substituindo o caminho de exemplo pelo caminho real da sua pasta de PDFs**:
    ```powershell
    python processador_cli.py "C:\Users\SeuUsuario\Desktop\Comprovantes_Outubro"
    ```

#### Passo 3: Encontre os Resultados
* O terminal mostrará um relatório completo do processamento.
* Os arquivos renomeados e um arquivo `.zip` com tudo dentro estarão na pasta de saída (por padrão, `pdfs_renomeados`, dentro da pasta do projeto).

---

## Importante: Você Não Precisa Editar o Código!

Uma grande vantagem desta ferramenta é que o código-fonte é universal. **Você nunca precisará abrir os arquivos `.py` para alterar caminhos de pastas.**

Pense no script como um GPS: você não modifica o aparelho por dentro para ir a um novo lugar, você apenas digita o endereço na tela. Aqui, o **Terminal é a sua tela**, e os caminhos das pastas são os "endereços" que você informa na hora de usar.

A alteração é feita diretamente no **comando que você digita**, como mostrado abaixo:

* **Para informar onde estão seus PDFs (obrigatório):**
    A primeira parte do comando é sempre o caminho para a pasta com os arquivos originais.
    ```powershell
    python processador_cli.py "C:\Caminho\DA\PASTA\COM\PDFs"
    ```

* **Para informar onde salvar os resultados (opcional):**
    Se você quiser salvar os arquivos em um local específico, use o indicador `-o` (`--output`) seguido do caminho da pasta de destino.
    ```powershell
    python processador_cli.py "C:\Caminho\De\Entrada" -o "C:\Caminho\De\Saida"
    ```
Desta forma, o mesmo script pode ser usado para processar arquivos de qualquer pasta, em qualquer computador, sem nenhuma modificação.
