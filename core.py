# Arquivo: core.py (VERSÃO FINAL - PROCESSAMENTO EM LOTE COM FATIAMENTO)

import os
import re
import zipfile
import shutil
from pathlib import Path
from typing import List, Optional
import logging

try:
    import fitz  # PyMuPDF
    from pdf2image import convert_from_path
    import pytesseract
    import cv2
    import numpy as np
    OCR_AVAILABLE = True
except ImportError:
    print("⚠️  Algumas bibliotecas não foram encontradas. A funcionalidade pode ser limitada.")
    OCR_AVAILABLE = False

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PDFCompromissoExtractor:
    def __init__(self, output_dir: str = "pdfs_renomeados"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.temp_dir = self.output_dir / "temp_pages"
        self.temp_dir.mkdir(exist_ok=True)
        
        self.patterns = {'estrito': r'\b\d[A-Z]{2}\d{7}\b', 'flexivel': r'\b[A-Z0-9]{8,12}\b'}
        self.rotulos_compromisso = [r'no\.?\s*compromisso\s*cliente', r'no\.?\s*compromisso', r'compromisso\s*cliente', r'no\s*compromisso', r'nº\s*compromisso', r'número\s*compromisso']
        self.processed_files = []
        self.failed_files = []

    def _split_single_pdf(self, pdf_path: Path) -> List[str]:
        """(Função interna) Fatia um único PDF em páginas."""
        logger.info(f"Fatiando o arquivo: {pdf_path.name}")
        split_files = []
        try:
            with fitz.open(pdf_path) as doc:
                if doc.page_count == 0:
                    logger.warning(f"O arquivo {pdf_path.name} está vazio ou corrompido.")
                    return []
                
                for i, page in enumerate(doc):
                    page_num = i + 1
                    new_doc = fitz.open()
                    new_doc.insert_pdf(doc, from_page=i, to_page=i)
                    # Nome temporário inclui o nome do arquivo original para evitar conflitos
                    output_path = self.temp_dir / f"{pdf_path.stem}_pagina_{page_num}.pdf"
                    new_doc.save(str(output_path))
                    new_doc.close()
                    split_files.append(str(output_path))
            return split_files
        except Exception as e:
            logger.error(f"Falha ao fatiar o arquivo {pdf_path.name}: {e}")
            return []

    def process_directory(self, input_dir: str):
        """
        NOVA FUNÇÃO PRINCIPAL: Processa todos os PDFs de um diretório,
        fatiando cada um e depois renomeando as páginas.
        """
        input_path = Path(input_dir)
        all_pdfs_in_dir = list(input_path.glob("*.pdf"))

        if not all_pdfs_in_dir:
            logger.warning(f"Nenhum arquivo PDF encontrado em '{input_dir}'")
            return

        logger.info(f"Encontrados {len(all_pdfs_in_dir)} PDFs para fatiar e processar.")
        
        all_split_pages = []
        for pdf_path in all_pdfs_in_dir:
            split_pages = self._split_single_pdf(pdf_path)
            all_split_pages.extend(split_pages)
        
        if not all_split_pages:
            logger.error("Nenhuma página pôde ser extraída dos arquivos PDF.")
            return

        self._process_split_pages(all_split_pages)

    def _process_split_pages(self, pdf_paths: List[str]):
        """(Função interna) Renomeia uma lista de páginas já fatiadas."""
        logger.info(f"Iniciando renomeação de {len(pdf_paths)} páginas...")
        for pdf_path in pdf_paths:
            self._process_single_page(pdf_path)

    def _process_single_page(self, pdf_path: str) -> bool:
        """(Função interna) Processa uma única página fatiada."""
        try:
            text = self._extract_text_from_pdf(pdf_path)
            if not text:
                self.failed_files.append({'original': pdf_path, 'reason': 'Não foi possível extrair texto'})
                return False
            
            compromisso_number = self._find_compromisso_number(text)
            if compromisso_number:
                new_filename = f"{compromisso_number}.pdf"
                new_path = self.output_dir / new_filename
                shutil.copy2(pdf_path, new_path)
                self.processed_files.append({'original': Path(pdf_path).name, 'new_path': new_path})
                logger.info(f"✅ Processado e renomeado: {Path(pdf_path).name} → {new_filename}")
                return True
            else:
                self.failed_files.append({'original': pdf_path, 'reason': 'Número não encontrado'})
                return False
        except Exception as e:
            logger.error(f"Erro inesperado processando {Path(pdf_path).name}: {e}")
            self.failed_files.append({'original': pdf_path, 'reason': str(e)})
            return False

    def _extract_text_from_pdf(self, pdf_path: str) -> str:
        #...(Funções de extração, o nome foi alterado para indicar uso interno)
        logger.info(f"Extraindo texto de: {Path(pdf_path).name}")
        text = self._extract_text_pymupdf(pdf_path)
        if not text or len(text.strip()) < 50:
            logger.info(f"Texto insuficiente em {Path(pdf_path).name} - executando OCR...")
            text = self._extract_text_ocr(pdf_path)
        return text

    def _extract_text_pymupdf(self, pdf_path: str) -> str:
        try:
            with fitz.open(pdf_path) as doc:
                return "".join(page.get_text("text") for page in doc)
        except Exception as e:
            logger.warning(f"Erro na extração PyMuPDF para {Path(pdf_path).name}: {e}")
            return ""

    def _extract_text_ocr(self, pdf_path: str) -> str:
        if not OCR_AVAILABLE: return ""
        try:
            images = convert_from_path(pdf_path, dpi=300)
            text_complete = ""
            config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-.'
            for image in images:
                processed_img = self._preprocess_image_for_ocr(np.array(image))
                text_complete += pytesseract.image_to_string(processed_img, config=config) + "\n"
            return text_complete
        except Exception as e:
            logger.error(f"Erro no OCR para {Path(pdf_path).name}: {e}")
            return ""
            
    def _preprocess_image_for_ocr(self, image_array: np.ndarray) -> np.ndarray:
        if len(image_array.shape) == 3: gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
        else: gray = image_array
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return thresh

    def _find_compromisso_number(self, text: str) -> Optional[str]:
        #...(Funções de extração, o nome foi alterado para indicar uso interno)
        text_normalized = re.sub(r'\s+', ' ', text.upper())
        candidates = []
        for rotulo in self.rotulos_compromisso:
            for match in re.finditer(rotulo, text_normalized, re.IGNORECASE):
                search_area = text_normalized[match.end():match.end() + 200]
                strict_found = False
                for s_match in re.finditer(self.patterns['estrito'], search_area):
                    candidates.append({'number': s_match.group(), 'confidence': 'alta', 'distance': s_match.start()})
                    strict_found = True
                if not strict_found:
                    for f_match in re.finditer(self.patterns['flexivel'], search_area):
                        candidates.append({'number': f_match.group(), 'confidence': 'media', 'distance': f_match.start()})
        if candidates:
            candidates.sort(key=lambda x: (x['confidence'] != 'alta', x['distance']))
            logger.info(f"Número encontrado: {candidates[0]['number']}")
            return candidates[0]['number']
        logger.warning(f"Nenhum número de compromisso encontrado...")
        return None

    def cleanup_temp_dir(self):
        logger.info("Limpando arquivos temporários...")
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def generate_report(self) -> str:
        # ... (código do relatório sem grandes alterações)
        stats = {'total': len(self.processed_files) + len(self.failed_files), 'success': len(self.processed_files), 'failed': len(self.failed_files)}
        report = f"\n📊 RELATÓRIO DE PROCESSAMENTO\n==========================================\n"
        report += f"• Total de páginas processadas: {stats['total']}\n"
        report += f"• Sucesso: {stats['success']}\n"
        report += f"• Falhas: {stats['failed']}\n"
        if self.processed_files:
            report += "\n✅ Arquivos renomeados com Sucesso:\n"
            for file_info in self.processed_files:
                report += f"• {file_info['original']} → {Path(file_info['new_path']).name}\n"
        if self.failed_files:
            report += f"\n❌ Páginas que Falharam:\n"
            for failed in self.failed_files:
                report += f"• Página {Path(failed['original']).name} - {failed['reason']}\n"
        report += f"\n📁 Arquivos salvos em: {self.output_dir.resolve()}"
        return report