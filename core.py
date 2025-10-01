#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Extração e Renomeação de PDFs - Comprovantes de Pagamento
Autor: Especialista em Automação de Documentos
Versão: 1.0
"""

import os
import re
import zipfile
import tempfile
import shutil
from pathlib import Path
from typing import List, Tuple, Optional
import logging

# Bibliotecas para processamento de PDF e OCR
try:
    import fitz  # PyMuPDF - mais rápido e robusto
except ImportError:
    import PyPDF2

try:
    from pdf2image import convert_from_path
    import pytesseract
    import cv2
    import numpy as np

    OCR_AVAILABLE = True
except ImportError:
    print(
        "⚠️  Bibliotecas de OCR não instaladas. Apenas PDFs com texto digital serão processados."
    )
    OCR_AVAILABLE = False

# Configuração de logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class PDFCompromissoExtractor:
    """
    Classe principal para extração de números de compromisso de PDFs
    """

    def __init__(self, output_dir: str = "pdfs_renomeados"):
        """
        Inicializa o extrator de compromissos

        Args:
            output_dir: Diretório onde os arquivos renomeados serão salvos
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # Padrões regex para identificação do número
        self.patterns = {
            "estrito": r"\b\d[A-Z]{2}\d{7}\b",  # 1 dígito + 2 letras + 7 dígitos
            "flexivel": r"\b[A-Z0-9]{8,12}\b",  # Alfanumérico 8-12 caracteres
        }

        # Rótulos que precedem o número de compromisso
        self.rotulos_compromisso = [
            r"no\.?\s*compromisso\s*cliente",
            r"no\.?\s*compromisso",
            r"compromisso\s*cliente",
            r"no\s*compromisso",
            r"nº\s*compromisso",
            r"número\s*compromisso",
        ]

        self.processed_files = []
        self.failed_files = []

    def extract_text_pymupdf(self, pdf_path: str) -> str:
        """
        Extrai texto usando PyMuPDF (mais rápido e preciso)
        """
        try:
            doc = fitz.open(pdf_path)
            text = ""
            for page_num in range(doc.page_count):
                page = doc[page_num]
                text += page.get_text()
            doc.close()
            return text
        except Exception as e:
            logger.warning(f"Erro na extração PyMuPDF: {e}")
            return ""

    def extract_text_pypdf2(self, pdf_path: str) -> str:
        """
        Extrai texto usando PyPDF2 (fallback)
        """
        try:
            with open(pdf_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text()
            return text
        except Exception as e:
            logger.warning(f"Erro na extração PyPDF2: {e}")
            return ""

    def preprocess_image_for_ocr(self, image_array: np.ndarray) -> np.ndarray:
        """
        Aplica pré-processamento na imagem para melhorar OCR

        Args:
            image_array: Array numpy da imagem

        Returns:
            Imagem pré-processada
        """
        # Converter para escala de cinza
        if len(image_array.shape) == 3:
            gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
        else:
            gray = image_array

        # Aplicar threshold para binarização
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Remover ruído com operações morfológicas
        kernel = np.ones((1, 1), np.uint8)
        processed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

        return processed

    def extract_text_ocr(self, pdf_path: str) -> str:
        """
        Extrai texto usando OCR para PDFs baseados em imagem
        """
        if not OCR_AVAILABLE:
            logger.warning(
                "OCR não disponível - instale pdf2image, pytesseract e opencv"
            )
            return ""

        try:
            # Converter PDF para imagens com alta resolução
            images = convert_from_path(pdf_path, dpi=300)
            text_complete = ""

            for i, image in enumerate(images):
                logger.info(f"Processando página {i+1} com OCR...")

                # Converter PIL para numpy array
                img_array = np.array(image)

                # Pré-processar imagem
                processed_img = self.preprocess_image_for_ocr(img_array)

                # Configurar pytesseract com whitelist
                custom_config = r"--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-."

                # Extrair texto
                text = pytesseract.image_to_string(processed_img, config=custom_config)
                text_complete += text + "\n"

            return text_complete

        except Exception as e:
            logger.error(f"Erro no OCR: {e}")
            return ""

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Método principal para extração de texto - tenta texto direto primeiro, OCR como fallback
        """
        logger.info(f"Extraindo texto de: {pdf_path}")

        # Primeira tentativa: PyMuPDF
        text = self.extract_text_pymupdf(pdf_path)

        # Fallback: PyPDF2
        if not text or len(text.strip()) < 50:
            text = self.extract_text_pypdf2(pdf_path)

        # Se ainda não temos texto suficiente, usar OCR
        if not text or len(text.strip()) < 50:
            logger.info("Texto insuficiente detectado - executando OCR...")
            text = self.extract_text_ocr(pdf_path)

        return text

    def find_compromisso_number(self, text: str) -> Optional[str]:
        """
        Encontra o número de compromisso no texto usando regex e análise de proximidade
        """
        text_normalized = re.sub(r"\s+", " ", text.upper())

        # Lista para armazenar candidatos encontrados
        candidates = []

        # Buscar por cada rótulo de compromisso
        for rotulo_pattern in self.rotulos_compromisso:
            rotulo_matches = re.finditer(rotulo_pattern, text_normalized, re.IGNORECASE)

            for rotulo_match in rotulo_matches:
                # Área de busca após o rótulo (próximos 200 caracteres)
                search_area = text_normalized[
                    rotulo_match.end() : rotulo_match.end() + 200
                ]

                # Buscar padrão estrito primeiro (alta confiança)
                strict_matches = re.finditer(self.patterns["estrito"], search_area)
                for match in strict_matches:
                    distance = match.start()
                    candidates.append(
                        {
                            "number": match.group(),
                            "confidence": "alta",
                            "distance": distance,
                            "pattern": "estrito",
                        }
                    )

                # Se não encontrou padrão estrito, buscar flexível
                if not list(re.finditer(self.patterns["estrito"], search_area)):
                    flexible_matches = re.finditer(
                        self.patterns["flexivel"], search_area
                    )
                    for match in flexible_matches:
                        distance = match.start()
                        candidates.append(
                            {
                                "number": match.group(),
                                "confidence": "media",
                                "distance": distance,
                                "pattern": "flexivel",
                            }
                        )

        # Ordenar candidatos por confiança e proximidade
        if candidates:
            # Priorizar alta confiança e menor distância
            candidates.sort(key=lambda x: (x["confidence"] != "alta", x["distance"]))
            best_candidate = candidates[0]

            logger.info(
                f"Número encontrado: {best_candidate['number']} "
                f"(confiança: {best_candidate['confidence']}, "
                f"padrão: {best_candidate['pattern']})"
            )

            return best_candidate["number"]

        logger.warning("Nenhum número de compromisso encontrado")
        return None

    def process_single_pdf(self, pdf_path: str) -> bool:
        """
        Processa um único arquivo PDF

        Returns:
            True se processado com sucesso, False caso contrário
        """
        try:
            # Extrair texto
            text = self.extract_text_from_pdf(pdf_path)

            if not text:
                logger.error(f"Não foi possível extrair texto de: {pdf_path}")
                return False

            # Encontrar número de compromisso
            compromisso_number = self.find_compromisso_number(text)

            if not compromisso_number:
                # Renomear com prefixo de não encontrado
                original_name = Path(pdf_path).stem
                new_name = f"COMPROMISSO_NAO_ENCONTRADO_{original_name}.pdf"
                self.failed_files.append(
                    {
                        "original": pdf_path,
                        "new_name": new_name,
                        "reason": "Número não encontrado",
                    }
                )
                return False

            # Renomear arquivo
            new_filename = f"{compromisso_number}.pdf"
            new_path = self.output_dir / new_filename

            # Copiar arquivo para novo local com novo nome
            shutil.copy2(pdf_path, new_path)

            self.processed_files.append(
                {
                    "original": pdf_path,
                    "new_path": str(new_path),
                    "compromisso": compromisso_number,
                }
            )

            logger.info(f"✅ Processado: {Path(pdf_path).name} → {new_filename}")
            return True

        except Exception as e:
            logger.error(f"Erro processando {pdf_path}: {e}")
            return False

    def process_multiple_pdfs(self, pdf_paths: List[str]) -> dict:
        """
        Processa múltiplos arquivos PDF

        Returns:
            Dicionário com estatísticas do processamento
        """
        logger.info(f"Iniciando processamento de {len(pdf_paths)} arquivos...")

        success_count = 0
        for pdf_path in pdf_paths:
            if self.process_single_pdf(pdf_path):
                success_count += 1

        # Copiar arquivos que falharam também
        for failed in self.failed_files:
            failed_path = self.output_dir / failed["new_name"]
            shutil.copy2(failed["original"], failed_path)

        stats = {
            "total": len(pdf_paths),
            "success": success_count,
            "failed": len(self.failed_files),
            "processed_files": self.processed_files,
            "failed_files": self.failed_files,
        }

        return stats

    def create_download_zip(self, zip_name: str = "pdfs_processados.zip") -> str:
        """
        Cria um arquivo ZIP com todos os PDFs processados

        Returns:
            Caminho para o arquivo ZIP criado
        """
        zip_path = self.output_dir / zip_name

        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            # Adicionar arquivos processados com sucesso
            for file_info in self.processed_files:
                file_path = Path(file_info["new_path"])
                if file_path.exists():
                    zipf.write(file_path, file_path.name)

            # Adicionar arquivos que falharam
            for failed in self.failed_files:
                failed_path = self.output_dir / failed["new_name"]
                if failed_path.exists():
                    zipf.write(failed_path, failed_path.split("/")[-1])

        logger.info(f"📦 ZIP criado: {zip_path}")
        return str(zip_path)

    def generate_report(self, stats: dict) -> str:
        """
        Gera relatório detalhado do processamento
        """
        report = f"""
📊 RELATÓRIO DE PROCESSAMENTO DE PDFs
==========================================

📈 Estatísticas Gerais:
• Total de arquivos: {stats['total']}
• Processados com sucesso: {stats['success']}
• Falharam: {stats['failed']}
• Taxa de sucesso: {(stats['success']/stats['total']*100):.1f}%

✅ Arquivos Processados com Sucesso:
"""

        for file_info in stats["processed_files"]:
            original_name = Path(file_info["original"]).name
            report += f"• {original_name} → {file_info['compromisso']}.pdf\n"

        if stats["failed_files"]:
            report += f"\n❌ Arquivos que Falharam:\n"
            for failed in stats["failed_files"]:
                original_name = Path(failed["original"]).name
                report += f"• {original_name} - {failed['reason']}\n"

        report += f"\n📁 Arquivos salvos em: {self.output_dir}"

        return report


# Função principal de uso
def processar_pdfs_compromisso(pdf_directory: str = None, pdf_files: List[str] = None):
    """
    Função principal para processar PDFs de compromisso

    Args:
        pdf_directory: Diretório contendo PDFs para processar
        pdf_files: Lista específica de arquivos PDF para processar
    """

    extractor = PDFCompromissoExtractor()

    # Determinar lista de arquivos para processar
    if pdf_directory:
        pdf_paths = list(Path(pdf_directory).glob("*.pdf"))
        pdf_paths = [str(p) for p in pdf_paths]
    elif pdf_files:
        pdf_paths = pdf_files
    else:
        print("❌ Erro: Especifique pdf_directory ou pdf_files")
        return

    if not pdf_paths:
        print("❌ Nenhum arquivo PDF encontrado")
        return

    print(f"🔍 Encontrados {len(pdf_paths)} arquivos PDF para processar")

    # Processar arquivos
    stats = extractor.process_multiple_pdfs(pdf_paths)

    # Gerar relatório
    report = extractor.generate_report(stats)
    print(report)

    # Criar ZIP para download
    zip_path = extractor.create_download_zip()

    print(f"\n🎯 PROCESSAMENTO CONCLUÍDO!")
    print(f"📦 Download disponível em: {zip_path}")
    print(f"📁 Arquivos individuais em: {extractor.output_dir}")

    return {
        "stats": stats,
        "zip_path": zip_path,
        "output_dir": str(extractor.output_dir),
        "extractor": extractor,
    }


# No final do arquivo processador.py
if __name__ == "__main__":
    print("--- SCRIPT INICIADO, AGUARDE... ---")  # ADICIONE ESTA LINHA

    # Exemplo 1: Processar todos os PDFs de um diretório
    resultado = processar_pdfs_compromisso(pdf_directory="./meus_pdfs")

    # Exemplo 2: Processar arquivos específicos
    # arquivos = ["comprovante1.pdf", "comprovante2.pdf"]
    # resultado = processar_pdfs_compromisso(pdf_files=arquivos)

    print("🚀 Sistema de Extração de Compromissos Pronto!")
    # A linha abaixo foi comentada para teste
    # print("📖 Para usar: processar_pdfs_compromisso(pdf_directory='./seus_pdfs')")