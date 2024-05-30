import sqlalchemy as _sa
import sqlalchemy.sql.schema as _sass

# Recommended naming convention used by Alembic, as various different database
# providers will autogenerate vastly different names making migrations more
# difficult. See: http://alembic.zzzcomputing.com/en/latest/naming.html
NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = _sass.MetaData(naming_convention=NAMING_CONVENTION)

User = _sa.Table(
    "user",
    metadata,
    _sa.Column("id", _sa.Integer, primary_key=True),
    _sa.Column("name", _sa.String, nullable=False),
    _sa.Column("email", _sa.String, nullable=True, unique=True),
)

Post = _sa.Table(
    "post",
    metadata,
    _sa.Column("id", _sa.Integer, primary_key=True),
    _sa.Column("user_id", _sa.Integer, _sa.ForeignKey("user.id"), nullable=False),
    _sa.Column(
        "timestamp",
        _sa.DateTime(timezone=True),
        nullable=False,
        server_default=_sa.func.now(),
    ),
    _sa.Column("body", _sa.String, nullable=False),
)
