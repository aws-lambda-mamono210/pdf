import os
import re
import PyPDF2
import argparse

def merge_pdfs_in_directory(directory, output_filename):
    # ディレクトリ内の全ファイルを取得
    all_files = os.listdir(directory)

    # 指定の命名規則に合致するファイルだけを抽出
    pattern = re.compile(r'\d{2}_\w+\.pdf')
    matching_files = [f for f in all_files if pattern.match(f)]
    
    # ファイル名の数字部分（例：01, 02）でソート
    sorted_files = sorted(matching_files, key=lambda x: int(x.split('_')[0]))

    # ファイルのフルパスを取得
    full_paths = [os.path.join(directory, f) for f in sorted_files]

    # PDF結合用のマージャーオブジェクトを作成
    pdf_merger = PyPDF2.PdfMerger()

    # 各PDFをマージャーに追加
    for pdf in full_paths:
        with open(pdf, 'rb') as pdf_file:
            pdf_merger.append(pdf_file)

    # マージされたPDFを新しいファイルとして保存
    with open(output_filename, 'wb') as output_file:
        pdf_merger.write(output_file)

def main():
    parser = argparse.ArgumentParser(description='Merge PDFs in a directory.')
    parser.add_argument('directory', type=str, help='Path to the directory containing PDFs.')
    parser.add_argument('output_filename', type=str, help='Name of the output merged PDF file.')
    
    args = parser.parse_args()
    
    merge_pdfs_in_directory(args.directory, args.output_filename)
    print(f'{args.output_filename}にPDFが結合されました。')

if __name__ == "__main__":
    main()
