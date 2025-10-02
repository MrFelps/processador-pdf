# Guia de Utilização via Terminal

Este documento detalha como configurar e utilizar a ferramenta de renomeação de PDFs diretamente pelo terminal do seu computador.

## Parte 1: Pré-requisitos Essenciais

Para que o programa funcione, seu computador **obrigatoriamente** precisa ter os seguintes softwares já instalados e configurados em seu sistema:

* **Python** (versão 3.9 ou superior)
* **Tesseract OCR**
* **Poppler**

> **Atenção:** Este guia assume que os programas acima já estão instalados. A instalação destes softwares não é coberta por este documento. Se ocorrerem erros durante o uso, a causa mais provável é a ausência ou má configuração de um desses pré-requisitos.

---

## Parte 2: Configuração do Projeto (Feito Apenas Uma Vez)

Siga os passos abaixo para preparar o programa para o primeiro uso.

#### Passo 1: Baixar o Projeto
1.  Na página do projeto no GitHub, clique no botão verde **`< > Code`**.
2.  Selecione a opção **`Download ZIP`**.
3.  Salve o arquivo e **descompacte a pasta** em um local de fácil acesso no seu computador (por exemplo, na sua Área de Trabalho).

#### Passo 2: Acessar a Pasta do Projeto via Terminal
1.  Abra o terminal do seu sistema operacional (ex: `PowerShell` no Windows).
2.  Use o comando `cd` (change directory) para navegar até a pasta que você descompactou.
    * *Exemplo para Windows:*
        ```powershell
        cd C:\Users\SeuUsuario\Desktop\processador-pdf-python-main
        ```

#### Passo 3: Instalar as Dependências do Projeto
Com o terminal aberto na pasta correta, execute os três comandos abaixo, **um de cada vez**, na ordem exata.

1.  **Crie o ambiente virtual:**
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
    * *Aguarde a conclusão da instalação.*

Pronto! A configuração está concluída.

---

## Parte 3: Como Usar no Dia a Dia

Depois que a configuração inicial foi feita, o uso diário se resume a seguir os 3 passos abaixo.

### Os 3 Comandos Para Executar (Resumo Rápido)

Toda vez que você for usar o programa, abra o terminal e siga estes três passos:

**1. Navegue até a pasta do projeto:**
*(Substitua pelo caminho real da sua pasta)*
```powershell
cd C:\Caminho\Para\Sua\Pasta\DoProjeto
```

**2. Ative o ambiente virtual:**
*(O `(venv)` deve aparecer no início da linha)*
```powershell
.\venv\Scripts\Activate.ps1
```

**3. Execute o processamento:**
*(Este comando processa tudo o que está na pasta `meus_pdfs`)*
```powershell
python processador_cli.py "meus_pdfs"
```

---
### Detalhes do Processo

#### Passo 1: Adicionar os PDFs
* Antes de executar os comandos acima, coloque todos os seus arquivos PDF (sejam eles de uma ou várias páginas) dentro da pasta **`meus_pdfs`**, que já existe no projeto.

#### Passo 2: Executar os Comandos
* Siga o "Resumo Rápido" de 3 comandos mostrado acima. O terminal mostrará um relatório completo do processamento.

#### Passo 3: Encontrar os Resultados
* Seus arquivos finais, já fatiados e renomeados, estarão na pasta **`pdfs_renomeados`**.
