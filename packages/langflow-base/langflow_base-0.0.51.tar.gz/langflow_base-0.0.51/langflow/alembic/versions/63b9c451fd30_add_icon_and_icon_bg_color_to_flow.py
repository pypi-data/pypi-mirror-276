"""Add icon and icon_bg_color to Flow

Revision ID: 63b9c451fd30
Revises: bc2f01c40e4a
Create Date: 2024-03-06 10:53:47.148658

"""

from typing import Sequence, Union

import sqlalchemy as sa
import sqlmodel
from alembic import op
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision: str = "63b9c451fd30"
down_revision: Union[str, None] = "bc2f01c40e4a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)  # type: ignore
    table_names = inspector.get_table_names()  # noqa
    column_names = [column["name"] for column in inspector.get_columns("flow")]
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("flow", schema=None) as batch_op:
        if "icon" not in column_names:
            batch_op.add_column(sa.Column("icon", sqlmodel.sql.sqltypes.AutoString(), nullable=True))
        if "icon_bg_color" not in column_names:
            batch_op.add_column(sa.Column("icon_bg_color", sqlmodel.sql.sqltypes.AutoString(), nullable=True))

    # ### end Alembic commands ###


def downgrade() -> None:
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)  # type: ignore
    table_names = inspector.get_table_names()  # noqa
    column_names = [column["name"] for column in inspector.get_columns("flow")]
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("flow", schema=None) as batch_op:
        if "icon" in column_names:
            batch_op.drop_column("icon")
        if "icon_bg_color" in column_names:
            batch_op.drop_column("icon_bg_color")

    # ### end Alembic commands ###
