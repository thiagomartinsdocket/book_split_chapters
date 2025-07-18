import re
from pathlib import Path
from pypdf import PdfReader, PdfWriter # type: ignore

def dividir_livro_em_capitulos(pdf_entrada, pasta_capitulos, pasta_paginas, min_paginas_capitulo=2):
    Path(pasta_capitulos).mkdir(exist_ok=True)
    Path(pasta_paginas).mkdir(exist_ok=True)
    livro = PdfReader(pdf_entrada)
    padrao1 = re.compile(r'cap[íi]tulo\s+[\dIVXLC]+\s+[-]', re.IGNORECASE)
    padrao2 = re.compile(r'cap[íi]tulo\s+[\dIVXLC]+\s*:', re.IGNORECASE)

    escritor = None
    nome_arquivo = "00_introducao"
    paginas_do_capitulo = []

    for i, pagina in enumerate(livro.pages):
        texto = pagina.extract_text() or ""
        achado = padrao1.search(texto) or padrao2.search(texto)

        # Salva cada página individualmente
        salvar_pagina_pdf(pasta_paginas, i + 1, pagina)

        if achado:
            if escritor and len(paginas_do_capitulo) >= min_paginas_capitulo:
                for p in paginas_do_capitulo:
                    escritor.add_page(p)
                salvar_pdf(pasta_capitulos, nome_arquivo, escritor)
            # Se não atingir o mínimo, não salva o capítulo
            nome_arquivo = achado.group(0).replace(" ", "_").lower()
            escritor = PdfWriter()
            paginas_do_capitulo = []

        if not escritor:
            escritor = PdfWriter()

        paginas_do_capitulo.append(pagina)

    # Salva o último capítulo se atingir o mínimo
    if escritor and len(paginas_do_capitulo) >= min_paginas_capitulo:
        for p in paginas_do_capitulo:
            escritor.add_page(p)
        salvar_pdf(pasta_capitulos, nome_arquivo, escritor)

def salvar_pdf(pasta, nome, escritor):
    with open(Path(pasta, f"{nome}.pdf"), "wb") as f:
        escritor.write(f)

def salvar_pagina_pdf(pasta, numero, pagina):
    escritor = PdfWriter()
    escritor.add_page(pagina)
    with open(Path(pasta, f"pagina_{numero:03}.pdf"), "wb") as f:
        escritor.write(f)

# Executa
if __name__ == "__main__":
    dividir_livro_em_capitulos(
        "ebook-logica-de-programacao-iniciantes.pdf",
        "capitulos_extraidos",
        "paginas_separadas",
        min_paginas_capitulo=2  # valor mínimo de páginas para um capítulo ser considerado válido
    )