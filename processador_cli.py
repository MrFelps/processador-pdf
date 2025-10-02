# Arquivo: processador_cli.py (VERSÃO FINAL - PROCESSAMENTO EM LOTE COM FATIAMENTO)
import argparse
from core import PDFCompromissoExtractor

def main():
    """
    Função principal que orquestra o processo.
    """
    parser = argparse.ArgumentParser(
        description="Processa todos os PDFs de uma pasta, fatiando-os em páginas e renomeando cada uma."
    )
    # VOLTAMOS A ACEITAR UM DIRETÓRIO DE ENTRADA
    parser.add_argument(
        "input_dir", 
        type=str, 
        help="O caminho para a pasta contendo os arquivos PDF a serem processados."
    )
    parser.add_argument(
        "-o", "--output", 
        type=str, 
        default="pdfs_renomeados", 
        help="A pasta onde os arquivos processados serão salvos. (Padrão: 'pdfs_renomeados')"
    )
    args = parser.parse_args()

    # Inicializa o extrator
    extractor = PDFCompromissoExtractor(output_dir=args.output)
    
    try:
        # 1. Chama a nova função principal que lida com o diretório
        extractor.process_directory(args.input_dir)
        
        # 2. Gera o relatório final
        report = extractor.generate_report()
        print(report)
    
    finally:
        # 3. Limpa a pasta temporária, aconteça o que acontecer
        extractor.cleanup_temp_dir()

    print("\n🎯 PROCESSAMENTO CONCLUÍDO!")

if __name__ == "__main__":
    main()