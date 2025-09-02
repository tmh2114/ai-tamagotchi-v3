"""Unit tests for sync service."""
import pytest
import json
import os
from datetime import datetime
from uuid import uuid4
from src.services.sync_service import SyncService
from src.models import User, Tamagotchi, Interaction


class TestSyncService:
    """Test synchronization service."""
    
    @pytest.fixture
    def sync_service(self, tmp_path):
        """Create sync service with temporary cache directory."""
        cache_dir = str(tmp_path / "cache")
        return SyncService(cache_dir=cache_dir)
    
    def test_export_user_data(self, db_session, test_user, test_tamagotchi, sync_service):
        """Test exporting user data."""
        # Create some interactions
        interaction = Interaction(
            id=str(uuid4()),
            tamagotchi_id=test_tamagotchi.id,
            interaction_type="feed",
            happiness_change=5.0,
            created_at=datetime.utcnow()
        )
        db_session.add(interaction)
        db_session.commit()
        
        # Export data
        export_data = sync_service.export_user_data(test_user.id, db_session)
        
        assert export_data["version"] == "1.0"
        assert export_data["user"]["id"] == test_user.id
        assert len(export_data["tamagotchis"]) >= 1
        assert len(export_data["interactions"]) >= 1
        assert "checksum" in export_data
        assert export_data["metadata"]["total_tamagotchis"] >= 1
    
    def test_export_nonexistent_user(self, db_session, sync_service):
        """Test exporting data for non-existent user."""
        with pytest.raises(ValueError) as exc_info:
            sync_service.export_user_data(str(uuid4()), db_session)
        
        assert "not found" in str(exc_info.value)
    
    def test_import_user_data(self, db_session, sync_service):
        """Test importing user data."""
        # Prepare import data
        user_id = str(uuid4())
        tama_id = str(uuid4())
        
        import_data = {
            "version": "1.0",
            "export_date": datetime.utcnow().isoformat(),
            "user": {
                "id": user_id,
                "username": "imported_user",
                "email": "imported@example.com",
                "password_hash": "hash123",
                "coins": 200,
                "player_level": 5
            },
            "tamagotchis": [
                {
                    "id": tama_id,
                    "name": "ImportedPet",
                    "owner_id": user_id,
                    "stats": {
                        "happiness": 80.0,
                        "health": 90.0,
                        "hunger": 60.0,
                        "energy": 70.0,
                        "cleanliness": 85.0
                    },
                    "level": 3,
                    "evolution_stage": "child"
                }
            ],
            "interactions": [],
            "activities": []
        }
        
        # Calculate checksum
        data_str = json.dumps(import_data, sort_keys=True)
        import hashlib
        import_data["checksum"] = hashlib.sha256(data_str.encode()).hexdigest()
        
        # Import data
        results = sync_service.import_user_data(import_data, db_session)
        
        assert results["users_imported"] == 1
        assert results["tamagotchis_imported"] == 1
        assert len(results["errors"]) == 0
        
        # Verify imported data
        imported_user = db_session.query(User).filter(User.id == user_id).first()
        assert imported_user is not None
        assert imported_user.username == "imported_user"
        
        imported_tama = db_session.query(Tamagotchi).filter(Tamagotchi.id == tama_id).first()
        assert imported_tama is not None
        assert imported_tama.name == "ImportedPet"
        assert imported_tama.happiness == 80.0
    
    def test_import_with_invalid_checksum(self, db_session, sync_service):
        """Test importing data with invalid checksum."""
        import_data = {
            "version": "1.0",
            "user": {"id": str(uuid4())},
            "checksum": "invalid_checksum"
        }
        
        with pytest.raises(ValueError) as exc_info:
            sync_service.import_user_data(import_data, db_session)
        
        assert "integrity check failed" in str(exc_info.value)
    
    def test_cache_pending_changes(self, sync_service):
        """Test caching pending changes."""
        changes = [
            {
                "type": "update",
                "entity": "tamagotchi",
                "entity_id": str(uuid4()),
                "data": {"happiness": 90.0}
            },
            {
                "type": "create",
                "entity": "interaction",
                "data": {"interaction_type": "play"}
            }
        ]
        
        # Cache changes
        sync_service.cache_pending_changes(changes)
        
        # Retrieve pending changes
        pending = sync_service.get_pending_changes()
        
        assert len(pending) == 2
        assert all("id" in change for change in pending)
        assert all("timestamp" in change for change in pending)
        assert pending[0]["type"] == "update"
        assert pending[1]["type"] == "create"
    
    def test_clear_pending_changes(self, sync_service):
        """Test clearing pending changes."""
        # Add some changes
        changes = [{"type": "test", "data": "test"}]
        sync_service.cache_pending_changes(changes)
        
        # Get the change IDs
        pending = sync_service.get_pending_changes()
        change_ids = [c["id"] for c in pending]
        
        # Clear specific changes
        sync_service.clear_pending_changes(change_ids)
        
        # Verify cleared
        remaining = sync_service.get_pending_changes()
        assert len(remaining) == 0
    
    def test_clear_all_pending_changes(self, sync_service):
        """Test clearing all pending changes."""
        # Add multiple changes
        changes = [
            {"type": "test1", "data": "data1"},
            {"type": "test2", "data": "data2"}
        ]
        sync_service.cache_pending_changes(changes)
        
        # Clear all
        sync_service.clear_pending_changes()
        
        # Verify all cleared
        remaining = sync_service.get_pending_changes()
        assert len(remaining) == 0
    
    def test_log_sync(self, sync_service):
        """Test logging sync operations."""
        # Log multiple sync operations
        sync_service.log_sync(
            sync_type="export",
            status="success",
            details={"records_exported": 10}
        )
        sync_service.log_sync(
            sync_type="import",
            status="failure",
            details={"error": "Connection timeout"}
        )
        
        # Get sync history
        history = sync_service.get_sync_history(limit=5)
        
        assert len(history) == 2
        assert history[-2]["type"] == "export"
        assert history[-2]["status"] == "success"
        assert history[-1]["type"] == "import"
        assert history[-1]["status"] == "failure"
    
    def test_sync_history_limit(self, sync_service):
        """Test sync history limit."""
        # Log many sync operations
        for i in range(15):
            sync_service.log_sync(
                sync_type="auto",
                status="success",
                details={"iteration": i}
            )
        
        # Get limited history
        history = sync_service.get_sync_history(limit=5)
        
        assert len(history) == 5
        # Should get the most recent ones
        assert history[-1]["details"]["iteration"] == 14