import unittest
import os
import tempfile
from PyPDF2 import PdfWriter
from PyPDF2 import PdfReader
from pdf_merger import merge_pdfs_in_directory  # この関数は先ほどのスクリプトからインポートします。

class TestPDFMerger(unittest.TestCase):
    
    def setUp(self):
        # テスト用の一時ディレクトリを作成
        self.test_dir = tempfile.mkdtemp()

        # サンプルのPDFファイルを3つ作成
        for i in range(3):
            writer = PdfWriter()
            with open(os.path.join(self.test_dir, f"{i+1:02}_test.pdf"), "wb") as f:
                writer.add_blank_page(width=100, height=100)
                writer.write(f)
                
    def tearDown(self):
        # テストが終わったら一時ディレクトリを削除
        for filename in os.listdir(self.test_dir):
            os.remove(os.path.join(self.test_dir, filename))
        os.rmdir(self.test_dir)
    
    def test_merge_pdfs(self):
        output_file = os.path.join(self.test_dir, "merged.pdf")
        
        # マージ関数を呼び出す
        merge_pdfs_in_directory(self.test_dir, output_file)
        
        # 結果を確認する
        self.assertTrue(os.path.exists(output_file), "Merged PDF does not exist.")
        
        # 3つのPDFをマージしたので、マージされたPDFには3ページ含まれているはず
        with open(output_file, "rb") as f:
            reader = PdfReader(f)
            self.assertEqual(len(reader.pages), 3, "Merged PDF does not have the expected number of pages.")
            
if __name__ == "__main__":
    unittest.main()
