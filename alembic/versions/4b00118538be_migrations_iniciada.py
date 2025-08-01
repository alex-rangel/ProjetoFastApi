"""migrations iniciada

Revision ID: 4b00118538be
Revises: 
Create Date: 2025-07-26 13:12:43.332966

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4b00118538be'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('usuarios',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nome', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('senha', sa.String(), nullable=True),
    sa.Column('ativo', sa.Boolean(), nullable=True),
    sa.Column('admin', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pedidos',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('stauts', sa.String(), nullable=True),
    sa.Column('usuario', sa.Integer(), nullable=True),
    sa.Column('preco', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['usuario'], ['usuarios.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('itens pedidos',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('quantidade', sa.Integer(), nullable=True),
    sa.Column('sabor', sa.String(), nullable=True),
    sa.Column('tamanho', sa.String(), nullable=True),
    sa.Column('preco_unitario', sa.Float(), nullable=True),
    sa.Column('pedido', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['pedido'], ['pedidos.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('itens pedidos')
    op.drop_table('pedidos')
    op.drop_table('usuarios')
    # ### end Alembic commands ###
