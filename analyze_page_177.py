import pdfplumber
import sys

if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

pdf_path = r"D:\AGENT\KIMM_DOCS\A phonological analysis and comparison of two Kim Mun varieties in Laos and Vietnam.pdf"

def analyze_wordlist_layout(page_num):
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[page_num]
        words = page.extract_words()
        
        # Sort words by top (y) then x
        sorted_words = sorted(words, key=lambda w: (w['top'], w['x0']))
        
        # Group words by line (approximate y-coordinate)
        lines = []
        if sorted_words:
            current_line = [sorted_words[0]]
            for w in sorted_words[1:]:
                if abs(w['top'] - current_line[0]['top']) < 3:
                    current_line.append(w)
                else:
                    lines.append(current_line)
                    current_line = [w]
            lines.append(current_line)
            
        for line_words in lines:
            line_str = " | ".join([f"{w['text']} x={w['x0']:.0f}" for w in line_words])
            print(line_str)

if __name__ == "__main__":
    analyze_wordlist_layout(176) # PDF Page 177
