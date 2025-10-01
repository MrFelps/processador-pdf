# Arquivo: processador_cli.py
# Esta é a interface de linha de comando (CLI) do nosso programa.

from pathlib import Path
import argparse

# A linha mais importante: importa a nossa classe 'motor' do arquivo core.py
from core import PDFCompromissoExtractor

def processar_pdfs_compromisso(pdf_directory: str, output_directory: str):
    """
    Função que usa o extrator para processar os PDFs.
    """
    extractor = PDFCompromissoExtractor(output_dir=output_directory)
    pdf_paths = [str(p) for p in Path(pdf_directory).glob("*.pdf")]
    
    if not pdf_paths:
        print(f"❌ Nenhum arquivo PDF encontrado no diretório: {pdf_directory}")
        return
    
    print(f"🔍 Encontrados {len(pdf_paths)} arquivos PDF para processar...")
    
    stats = extractor.process_multiple_pdfs(pdf_paths)
    report = extractor.generate_report(stats)
    print(report)
    
    if stats.get('total', 0) > 0:
        zip_path = extractor.create_download_zip()
        print(f"\n🎯 PROCESSAMENTO CONCLUÍDO!")
        print(f"📦 ZIP criado em: {zip_path}")
        print(f"📁 Arquivos individuais em: {extractor.output_dir}")

# Este bloco lê os comandos do terminal e inicia o processo
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Processa PDFs para extrair o número de compromisso e renomeá-los.")
    parser.add_argument("input_dir", type=str, help="O caminho para a pasta contendo os arquivos PDF.")
    parser.add_argument("-o", "--output", type=str, default="pdfs_renomeados", help="O caminho para a pasta onde os arquivos processados serão salvos.")
    
    args = parser.parse_args()
    processar_pdfs_compromisso(pdf_directory=args.input_dir, output_directory=args.output)
