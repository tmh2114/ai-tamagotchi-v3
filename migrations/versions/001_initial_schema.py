"""Initial database schema

Revision ID: 001
Revises: 
Create Date: 2025-01-02 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create users table
    op.create_table('users',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('username', sa.String(50), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('display_name', sa.String(100), nullable=True),
        sa.Column('avatar_url', sa.String(500), nullable=True),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('total_playtime_minutes', sa.Integer(), nullable=False, default=0),
        sa.Column('total_tamagotchis_raised', sa.Integer(), nullable=False, default=0),
        sa.Column('current_streak_days', sa.Integer(), nullable=False, default=0),
        sa.Column('longest_streak_days', sa.Integer(), nullable=False, default=0),
        sa.Column('coins', sa.Integer(), nullable=False, default=100),
        sa.Column('gems', sa.Integer(), nullable=False, default=0),
        sa.Column('experience_points', sa.Integer(), nullable=False, default=0),
        sa.Column('player_level', sa.Integer(), nullable=False, default=1),
        sa.Column('preferences', sa.JSON(), nullable=False, default=dict),
        sa.Column('notification_settings', sa.JSON(), nullable=False, default=dict),
        sa.Column('timezone', sa.String(50), nullable=False, default='UTC'),
        sa.Column('language', sa.String(10), nullable=False, default='en'),
        sa.Column('friend_code', sa.String(20), nullable=True),
        sa.Column('is_public_profile', sa.Boolean(), nullable=False, default=False),
        sa.Column('bio', sa.String(500), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('is_premium', sa.Boolean(), nullable=False, default=False),
        sa.Column('premium_expires_at', sa.DateTime(), nullable=True),
        sa.Column('last_login', sa.DateTime(), nullable=True),
        sa.Column('last_activity', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('friend_code')
    )
    
    # Create tamagotchis table
    op.create_table('tamagotchis',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('species', sa.String(50), nullable=False, default='digital_pet'),
        sa.Column('avatar_url', sa.String(500), nullable=True),
        sa.Column('personality_type', sa.String(50), nullable=False, default='friendly'),
        sa.Column('personality_traits', sa.JSON(), nullable=False, default=list),
        sa.Column('voice_style', sa.String(100), nullable=True),
        sa.Column('happiness', sa.Float(), nullable=False, default=50.0),
        sa.Column('health', sa.Float(), nullable=False, default=100.0),
        sa.Column('hunger', sa.Float(), nullable=False, default=50.0),
        sa.Column('energy', sa.Float(), nullable=False, default=100.0),
        sa.Column('cleanliness', sa.Float(), nullable=False, default=100.0),
        sa.Column('experience', sa.Integer(), nullable=False, default=0),
        sa.Column('level', sa.Integer(), nullable=False, default=1),
        sa.Column('evolution_stage', sa.String(50), nullable=False, default='baby'),
        sa.Column('learned_behaviors', sa.JSON(), nullable=False, default=list),
        sa.Column('memory_bank', sa.JSON(), nullable=False, default=dict),
        sa.Column('preferences', sa.JSON(), nullable=False, default=dict),
        sa.Column('current_mood', sa.String(50), nullable=False, default='neutral'),
        sa.Column('current_activity', sa.String(100), nullable=True),
        sa.Column('is_sleeping', sa.Boolean(), nullable=False, default=False),
        sa.Column('is_sick', sa.Boolean(), nullable=False, default=False),
        sa.Column('birth_date', sa.DateTime(), nullable=False),
        sa.Column('last_fed', sa.DateTime(), nullable=True),
        sa.Column('last_played', sa.DateTime(), nullable=True),
        sa.Column('last_cleaned', sa.DateTime(), nullable=True),
        sa.Column('last_medicine', sa.DateTime(), nullable=True),
        sa.Column('last_interaction', sa.DateTime(), nullable=True),
        sa.Column('last_stat_update', sa.DateTime(), nullable=False),
        sa.Column('owner_id', sa.String(36), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create interactions table
    op.create_table('interactions',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('tamagotchi_id', sa.String(36), nullable=False),
        sa.Column('interaction_type', sa.String(50), nullable=False),
        sa.Column('interaction_subtype', sa.String(50), nullable=True),
        sa.Column('user_message', sa.Text(), nullable=True),
        sa.Column('tamagotchi_response', sa.Text(), nullable=True),
        sa.Column('happiness_change', sa.Float(), nullable=False, default=0.0),
        sa.Column('health_change', sa.Float(), nullable=False, default=0.0),
        sa.Column('hunger_change', sa.Float(), nullable=False, default=0.0),
        sa.Column('energy_change', sa.Float(), nullable=False, default=0.0),
        sa.Column('cleanliness_change', sa.Float(), nullable=False, default=0.0),
        sa.Column('experience_gained', sa.Integer(), nullable=False, default=0),
        sa.Column('emotion_before', sa.String(50), nullable=True),
        sa.Column('emotion_after', sa.String(50), nullable=True),
        sa.Column('sentiment_score', sa.Float(), nullable=True),
        sa.Column('metadata', sa.JSON(), nullable=True),
        sa.Column('duration_seconds', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['tamagotchi_id'], ['tamagotchis.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create activities table
    op.create_table('activities',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('tamagotchi_id', sa.String(36), nullable=False),
        sa.Column('activity_type', sa.String(50), nullable=False),
        sa.Column('activity_name', sa.String(100), nullable=False),
        sa.Column('description', sa.String(500), nullable=True),
        sa.Column('is_scheduled', sa.Boolean(), nullable=False, default=False),
        sa.Column('scheduled_time', sa.DateTime(), nullable=True),
        sa.Column('recurrence_pattern', sa.String(50), nullable=True),
        sa.Column('started_at', sa.DateTime(), nullable=True),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('duration_minutes', sa.Integer(), nullable=True),
        sa.Column('was_successful', sa.Boolean(), nullable=True),
        sa.Column('location', sa.String(100), nullable=True),
        sa.Column('participants', sa.JSON(), nullable=True),
        sa.Column('required_items', sa.JSON(), nullable=True),
        sa.Column('rewards', sa.JSON(), nullable=True),
        sa.Column('metadata', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['tamagotchi_id'], ['tamagotchis.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create items table
    op.create_table('items',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('category', sa.String(50), nullable=False),
        sa.Column('subcategory', sa.String(50), nullable=True),
        sa.Column('description', sa.String(500), nullable=True),
        sa.Column('icon_url', sa.String(500), nullable=True),
        sa.Column('rarity', sa.String(20), nullable=False, default='common'),
        sa.Column('cost', sa.Integer(), nullable=False, default=0),
        sa.Column('sell_value', sa.Integer(), nullable=False, default=0),
        sa.Column('is_consumable', sa.Boolean(), nullable=False, default=True),
        sa.Column('max_stack', sa.Integer(), nullable=False, default=99),
        sa.Column('effects', sa.JSON(), nullable=True),
        sa.Column('duration_minutes', sa.Integer(), nullable=True),
        sa.Column('cooldown_minutes', sa.Integer(), nullable=True),
        sa.Column('level_required', sa.Integer(), nullable=False, default=1),
        sa.Column('evolution_stage_required', sa.String(50), nullable=True),
        sa.Column('metadata', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    
    # Create inventory_items table
    op.create_table('inventory_items',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('tamagotchi_id', sa.String(36), nullable=False),
        sa.Column('item_id', sa.String(36), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False, default=1),
        sa.Column('acquired_at', sa.DateTime(), nullable=False),
        sa.Column('last_used', sa.DateTime(), nullable=True),
        sa.Column('times_used', sa.Integer(), nullable=False, default=0),
        sa.Column('is_equipped', sa.Boolean(), nullable=False, default=False),
        sa.Column('is_favorite', sa.Boolean(), nullable=False, default=False),
        sa.Column('custom_name', sa.String(100), nullable=True),
        sa.Column('metadata', sa.JSON(), nullable=True),
        sa.ForeignKeyConstraint(['item_id'], ['items.id'], ),
        sa.ForeignKeyConstraint(['tamagotchi_id'], ['tamagotchis.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create achievements table
    op.create_table('achievements',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('category', sa.String(50), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('icon_url', sa.String(500), nullable=True),
        sa.Column('requirement_type', sa.String(50), nullable=False),
        sa.Column('requirement_value', sa.Integer(), nullable=False, default=1),
        sa.Column('requirement_details', sa.JSON(), nullable=True),
        sa.Column('reward_experience', sa.Integer(), nullable=False, default=0),
        sa.Column('reward_items', sa.JSON(), nullable=True),
        sa.Column('reward_title', sa.String(100), nullable=True),
        sa.Column('reward_badge_url', sa.String(500), nullable=True),
        sa.Column('tier', sa.String(20), nullable=False, default='bronze'),
        sa.Column('points', sa.Integer(), nullable=False, default=10),
        sa.Column('is_hidden', sa.Boolean(), nullable=False, default=False),
        sa.Column('is_repeatable', sa.Boolean(), nullable=False, default=False),
        sa.Column('display_order', sa.Integer(), nullable=False, default=0),
        sa.Column('metadata', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    
    # Create tamagotchi_achievements association table
    op.create_table('tamagotchi_achievements',
        sa.Column('tamagotchi_id', sa.String(36), nullable=False),
        sa.Column('achievement_id', sa.String(36), nullable=False),
        sa.Column('unlocked_at', sa.DateTime(), nullable=False),
        sa.Column('progress', sa.Integer(), nullable=False, default=0),
        sa.Column('is_completed', sa.Boolean(), nullable=False, default=False),
        sa.ForeignKeyConstraint(['achievement_id'], ['achievements.id'], ),
        sa.ForeignKeyConstraint(['tamagotchi_id'], ['tamagotchis.id'], ),
        sa.PrimaryKeyConstraint('tamagotchi_id', 'achievement_id')
    )
    
    # Create indexes for better query performance
    op.create_index('idx_tamagotchis_owner_id', 'tamagotchis', ['owner_id'])
    op.create_index('idx_interactions_tamagotchi_id', 'interactions', ['tamagotchi_id'])
    op.create_index('idx_interactions_created_at', 'interactions', ['created_at'])
    op.create_index('idx_activities_tamagotchi_id', 'activities', ['tamagotchi_id'])
    op.create_index('idx_inventory_items_tamagotchi_id', 'inventory_items', ['tamagotchi_id'])
    op.create_index('idx_inventory_items_item_id', 'inventory_items', ['item_id'])


def downgrade() -> None:
    # Drop indexes
    op.drop_index('idx_inventory_items_item_id', 'inventory_items')
    op.drop_index('idx_inventory_items_tamagotchi_id', 'inventory_items')
    op.drop_index('idx_activities_tamagotchi_id', 'activities')
    op.drop_index('idx_interactions_created_at', 'interactions')
    op.drop_index('idx_interactions_tamagotchi_id', 'interactions')
    op.drop_index('idx_tamagotchis_owner_id', 'tamagotchis')
    
    # Drop tables
    op.drop_table('tamagotchi_achievements')
    op.drop_table('achievements')
    op.drop_table('inventory_items')
    op.drop_table('items')
    op.drop_table('activities')
    op.drop_table('interactions')
    op.drop_table('tamagotchis')
    op.drop_table('users')