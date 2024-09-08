"""add_product_fields

Revision ID: 3a3492c3431a
Revises: 749e4b1672aa
Create Date: 2024-09-05 13:36:32.456791

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '3a3492c3431a'
down_revision = '749e4b1672aa'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('product', sa.Column('in_network_individual_deductible', sa.DECIMAL(10,2)))
    op.add_column('product', sa.Column('in_network_family_deductible', sa.DECIMAL(10,2)))
    op.add_column('product', sa.Column('out_of_network_individual_deductible', sa.DECIMAL(10,2)))
    op.add_column('product', sa.Column('out_of_network_family_deductible', sa.DECIMAL(10,2)))
    op.add_column('product', sa.Column('in_network_individual_oop_limit', sa.DECIMAL(10,2)))
    op.add_column('product', sa.Column('in_network_family_oop_limit', sa.DECIMAL(10,2)))
    op.add_column('product', sa.Column('out_of_network_individual_oop_limit', sa.DECIMAL(10,2)))
    op.add_column('product', sa.Column('out_of_network_family_oop_limit', sa.DECIMAL(10,2)))
    op.add_column('product', sa.Column('plan_name', sa.String(255)))
    op.add_column('product', sa.Column('plan_year', sa.Integer))
    op.add_column('product', sa.Column('plan_status', sa.String(50)))
    op.add_column('product', sa.Column('plan_type', sa.String(50)))
    op.add_column('product', sa.Column('plan_design', sa.String(50)))
    op.add_column('product', sa.Column('metal_level', sa.String(50)))
    op.add_column('product', sa.Column('coverage_type', sa.String(50)))
    op.add_column('product', sa.Column('funding_arrangement', sa.String(50)))
    op.add_column('product', sa.Column('group_size', sa.Integer))
    op.add_column('product', sa.Column('network_type', sa.String(100)))
    op.add_column('product', sa.Column('effective_date', sa.Date))
    op.add_column('product', sa.Column('end_date', sa.Date))
    op.add_column('product', sa.Column('employer_contribution', sa.DECIMAL(10,2)))
    op.add_column('product', sa.Column('actuarial_value', sa.DECIMAL(5,2)))
    op.add_column('product', sa.Column('distribution_channels', sa.String(255)))
    op.add_column('product', sa.Column('provider_network_link', sa.String(255)))
    op.add_column('product', sa.Column('provider_network_phone', sa.String(20)))
    op.add_column('product', sa.Column('plan_marketing_name', sa.String(255)))
    op.add_column('product', sa.Column('market_segment', sa.String(100)))
    op.add_column('product', sa.Column('is_hsa_eligible', sa.Boolean))
    op.add_column('product', sa.Column('deductible_combined_separate', sa.String(50)))
    op.add_column('product', sa.Column('specialist_referral_required', sa.Boolean))
    op.add_column('product', sa.Column('grandfathered_plan', sa.Boolean))
    op.add_column('product', sa.Column('coverage_summary', sa.Text))

def downgrade():
    op.drop_column('product', 'in_network_individual_deductible')
    op.drop_column('product', 'in_network_family_deductible')
    op.drop_column('product', 'out_of_network_individual_deductible')
    op.drop_column('product', 'out_of_network_family_deductible')
    op.drop_column('product', 'in_network_individual_oop_limit')
    op.drop_column('product', 'in_network_family_oop_limit')
    op.drop_column('product', 'out_of_network_individual_oop_limit')
    op.drop_column('product', 'out_of_network_family_oop_limit')
    op.drop_column('product', 'plan_name')
    op.drop_column('product', 'plan_year')
    op.drop_column('product', 'plan_status')
    op.drop_column('product', 'plan_type')
    op.drop_column('product', 'plan_design')
    op.drop_column('product', 'metal_level')
    op.drop_column('product', 'coverage_type')
    op.drop_column('product', 'funding_arrangement')
    op.drop_column('product', 'group_size')
    op.drop_column('product', 'network_type')
    op.drop_column('product', 'effective_date')
    op.drop_column('product', 'end_date')
    op.drop_column('product', 'employer_contribution')
    op.drop_column('product', 'actuarial_value')
    op.drop_column('product', 'distribution_channels')
    op.drop_column('product', 'provider_network_link')
    op.drop_column('product', 'provider_network_phone')
    op.drop_column('product', 'plan_marketing_name')
    op.drop_column('product', 'market_segment')
    op.drop_column('product', 'is_hsa_eligible')
    op.drop_column('product', 'deductible_combined_separate')
    op.drop_column('product', 'specialist_referral_required')
    op.drop_column('product', 'grandfathered_plan')
    op.drop_column('product', 'coverage_summary')
