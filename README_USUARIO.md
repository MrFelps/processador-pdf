# Guia Rápido: Renomeador Automático de PDFs

Este guia explica como instalar e usar a ferramenta de renomeação de PDFs em qualquer computador com Windows, mesmo que você não entenda de programação.

## Parte 1: Instalação (Feito Apenas Uma Vez)

Siga estes 5 passos na ordem. Leva cerca de 10 minutos.

### Passo 1: Instalar o Python
O "motor" que faz nosso programa funcionar.
1.  **Baixe o instalador:** [Clique aqui para baixar o Python (site oficial)](https://www.python.org/downloads/windows/).
2.  **Execute o instalador:**
3.  **MUITO IMPORTANTE:** Na primeira tela da instalação, marque a caixinha na parte de baixo que diz **"Add Python to PATH"**.
    ![Marque a opção 'Add Python to PATH'](https://i.imgur.com/Cw1c4tM.png)
4.  Continue a instalação padrão clicando em "Install Now".

### Passo 2: Instalar o Tesseract (O "Leitor" de Imagens)
O programa que consegue ler o texto de PDFs que são como fotos.
1.  **Baixe o instalador:** [Clique aqui para baixar o Tesseract (versão recomendada)](https://github.com/UB-Mannheim/tesseract/wiki).
2.  Execute o instalador. Pode aceitar todas as opções padrão clicando em "Next".

### Passo 3: Baixar o Projeto
1.  Acesse a página do projeto no GitHub: `[COLOQUE O LINK DO SEU REPOSITÓRIO AQUI]`
2.  Clique no botão verde **"< > Code"** e depois em **"Download ZIP"**.
    ![Como baixar o ZIP](https://i.imgur.com/szpc45Z.png)
3.  Salve o arquivo e **descompacte a pasta** em um local de fácil acesso (ex: na sua Área de Trabalho).

### Passo 4: Preparar o Ambiente (A Mágica)
Dentro da pasta que você descompactou, você encontrará um arquivo chamado `setup.bat`.
1.  Dê um **duplo-clique** no arquivo **`setup.bat`**.
2.  Uma tela preta aparecerá e instalará todas as dependências automaticamente. Aguarde até que ela mostre a mensagem "Setup Concluído!" e se feche sozinha.

## Parte 2: Como Usar no Dia a Dia

Agora que está tudo instalado, usar o programa é muito simples.

### Passo 1: Adicionar os PDFs
* Abra a pasta do projeto e encontre a subpasta chamada **`meus_pdfs`**.
* Copie e cole todos os arquivos PDF que você deseja renomear para dentro desta pasta.

### Passo 2: Executar o Programa
* Na pasta principal do projeto, dê um **duplo-clique** no arquivo **`EXECUTAR.bat`**.
* Uma tela preta aparecerá e mostrará o progresso do trabalho.

### Passo 3: Pegar os Arquivos Prontos
* Quando o processamento terminar, a tela preta mostrará o relatório final e a mensagem "Pressione qualquer tecla para continuar...".
* Você pode fechar a tela preta.
* Seus arquivos renomeados estarão esperando por você na pasta **`pdfs_renomeados`**. Lá também estará um arquivo `.zip` com uma cópia de tudo, para facilitar o envio.

E é só isso! Para processar novos arquivos, basta repetir a "Parte 2".
