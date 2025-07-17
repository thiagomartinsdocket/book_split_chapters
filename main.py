import re
from pathlib import Path
from pypdf import PdfReader, PdfWriter

def dividir_livro_em_capitulos(pdf_entrada, pasta_capitulos, pasta_paginas):
    Path(pasta_capitulos).mkdir(exist_ok=True)
    Path(pasta_paginas).mkdir(exist_ok=True)
    livro = PdfReader(pdf_entrada)
    padrao = re.compile(r'cap[íi]tulo\s+[\dIVXLC]+\s+-', re.IGNORECASE)
    escritor = None
    nome_arquivo = "00_introducao"

    for i, pagina in enumerate(livro.pages):
        texto = pagina.extract_text() or ""
        achado = padrao.search(texto)

        # Salva cada página individualmente
        salvar_pagina_pdf(pasta_paginas, i + 1, pagina)

        if achado:
            if escritor:
                salvar_pdf(pasta_capitulos, nome_arquivo, escritor)
            nome_arquivo = achado.group(0).replace(" ", "_").lower()
            escritor = PdfWriter()

        if not escritor:
            escritor = PdfWriter()

        escritor.add_page(pagina)

    if escritor:
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
        "paginas_separadas"
    )
