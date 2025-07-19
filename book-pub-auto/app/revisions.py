from app.models import Revision, Session

def save_revision(chapter_id, content, author_type):
    session = Session()
    version = session.query(Revision).filter_by(chapter_id=chapter_id).count() + 1
    rev = Revision(chapter_id=chapter_id, content=content, author_type=author_type, version=version)
    session.add(rev)
    session.commit()
    session.close()
