from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=NAMING_CONVENTION)

# add the MetaData import, the NAMING_CONVENTION dict (copy it exactly — this one's a standard convention, not something to derive yourself), and wire it into Base as shown. Keep your print(Base) at the bottom, run it again, and paste the output — should look the same as before, just confirming it still works with the new metadata attached.
