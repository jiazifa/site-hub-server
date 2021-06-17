from app.extensions import db


class BaseModel():
    """可以拓展功能"""

    def save(self, commit=False):
        db.session.add(self)
        if commit:
            db.session.commit()

    def delete(self, logic=True):

        if logic:
            self.is_delete = True
        else:
            db.session.delete(self)
        db.session.commit()

    @staticmethod
    def query_all(Model):
        items = db.session.query(Model).all()
        return items or []

