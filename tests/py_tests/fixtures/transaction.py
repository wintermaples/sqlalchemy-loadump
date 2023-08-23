from sqlalchemy import URL, Engine
from sqlalchemy.orm import Session


class Transaction:
    def __init__(self, session: Session, engine: Engine):
        self.session = session
        self.engine = engine

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        if exc_type is not None:
            self.session.rollback()
            return False

        self.session.commit()
        return True


class NoCommitTransaction(Transaction):
    def __init__(self, session: Session, engine: Engine):
        super().__init__(session, engine)
        self.session = session
        self.engine = engine

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        if exc_type is not None:
            self.session.rollback()
            return False

        self.session.flush()
        return True
