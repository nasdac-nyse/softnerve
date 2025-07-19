from ebooklib import epub

def export_epub(chapters, title="My Book"):
    book = epub.EpubBook()
    book.set_title(title)
    book.set_language("en")

    for i, text in enumerate(chapters):
        chap = epub.EpubHtml(title=f"Chapter {i+1}", file_name=f"chap_{i+1}.xhtml", content=f"<h1>Chapter {i+1}</h1><p>{text}</p>")
        book.add_item(chap)
        book.spine.append(chap)

    epub.write_epub(f"{title}.epub", book)
