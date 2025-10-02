# Arquivo: processador_cli.py (VERSÃO FINAL COM LÓGICA DE FATIAMENTO)
import argparse
from core import PDFCompromissoExtractor

def main():
    """
    Função principal que orquestra o processo de fatiar e renomear.
    """
    parser = argparse.ArgumentParser(
        description="Fatia um PDF de múltiplas páginas e renomeia cada página com base no número de compromisso."
    )
    parser.add_argument(
        "input_file", 
        type=str, 
        help="O caminho para o arquivo PDF único com várias páginas a ser processado."
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
        # 1. Fatia o PDF principal em vários PDFs de uma página
        split_pdf_paths = extractor.split_pdf(args.input_file)
        
        if split_pdf_paths:
            # 2. Processa a lista de PDFs fatiados para renomeá-los
            extractor.process_multiple_pdfs(split_pdf_paths)
        
        # 3. Gera o relatório final
        report = extractor.generate_report()
        print(report)
    
    finally:
        # 4. Limpa a pasta temporária, aconteça o que acontecer
        extractor.cleanup_temp_dir()

    print("\n🎯 PROCESSAMENTO CONCLUÍDO!")

if __name__ == "__main__":
    main()