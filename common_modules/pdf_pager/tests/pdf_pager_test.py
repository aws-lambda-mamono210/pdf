import shutil
import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

import tempfile
from PyPDF2 import PdfWriter
from PyPDF2 import PdfReader
from common_modules.pdf_merger.pdf_merger import merge_pdfs_in_directory
from common_modules.pdf_utils.pdf_utils import create_pdf_with_text
from common_modules.pdf_pager.pdf_pager import add_page_numbers

class TestPDFMerger(unittest.TestCase):

    def setUp(self):
        # 前回のテストで作成されたPDFファイルを削除
        save_dir = "artifacts"  # 保存先ディレクトリのパスを指定
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        for filename in os.listdir(save_dir):
            if filename.endswith('.pdf'):  # PDFファイルのみを対象とする
                os.remove(os.path.join(save_dir, filename))

        # テスト用の一時ディレクトリを作成
        self.test_dir = tempfile.mkdtemp()

        # サンプルのPDFファイルを3つ作成
        for i in range(3):
            file_path = os.path.join(self.test_dir, f"{i+1:02}_test.pdf")
            create_pdf_with_text(f"Page {i+1}", file_path)

    def tearDown(self):
        # テストが終わったら、テスト用のPDFファイルを'artifacts'ディレクトリに移動
        save_dir = "artifacts"
        for filename in os.listdir(self.test_dir):
            if filename.endswith('.pdf'):
                shutil.move(os.path.join(self.test_dir, filename), os.path.join(save_dir, filename))
        os.rmdir(self.test_dir)

    def test_add_page_numbers(self):
        output_file = os.path.join(self.test_dir, "merged.pdf")
        output_file_with_pages = os.path.join(self.test_dir, "page_added.pdf")

        merge_pdfs_in_directory(self.test_dir, output_file)
        add_page_numbers(output_file, output_file_with_pages, font_size=33)

        # 出力PDFを読み込みます
        reader = PdfReader(output_file_with_pages)

        # ページ数が正しいか確認します
        self.assertEqual(len(reader.pages), 3)

if __name__ == "__main__":
    unittest.main()
