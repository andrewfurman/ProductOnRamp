"""change_column_types_to_text

Revision ID: 62632e51d6c1
Revises: 
Create Date: 2024-09-04 17:34:55.987101

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'abcdef123456'
down_revision = None  # or 'previous_revision_id'
branch_labels = None
depends_on = None

def upgrade():
    # Change column types to text
    op.alter_column('product', 'name', type_=sa.Text(), existing_type=sa.String())
    op.alter_column('product', 'url', type_=sa.Text(), existing_type=sa.String())
    op.alter_column('product', 'summary_of_benefits', type_=sa.Text(), existing_type=sa.String())
    op.alter_column('product', 'line_of_business', type_=sa.Text(), existing_type=sa.String())

def downgrade():
    # Change column types back to varchar
    op.alter_column('product', 'name', type_=sa.String(), existing_type=sa.Text())
    op.alter_column('product', 'url', type_=sa.String(), existing_type=sa.Text())
    op.alter_column('product', 'summary_of_benefits', type_=sa.String(), existing_type=sa.Text())
    op.alter_column('product', 'line_of_business', type_=sa.String(), existing_type=sa.Text())
