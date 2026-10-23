"""Regression checks for empty snapshots and dependent views."""
from unittest.mock import MagicMock, patch
from feishu_sync_service import FeishuSyncService
from dataset_transform_service import DatasetTransformService


def service_with_connection():
    service = FeishuSyncService()
    conn = MagicMock()
    service.get_postgres_connection = MagicMock(return_value=conn)
    service.create_target_table = MagicMock(return_value=True)
    service.compare_schema = MagicMock(return_value={})
    service.save_schema_snapshot = MagicMock()
    return service, conn


def run_snapshot(service, records):
    with patch('feishu_sync_service.write_log'), \
         patch('dataset_transform_service.transform_service.run_transforms_by_source_table'), \
         patch('build_dataset_node_index.rebuild_dataset_node_index_for_source_table', return_value={}):
        return service.sync_data_to_postgres(dict(id=999999, target_table="test_gas_snapshot",sync_mode="full"),records)


def test_successful_empty_snapshot_truncates_and_commits():
    service, conn = service_with_connection()
    assert run_snapshot(service, []) is True
    queries = [str(call.args[0]) for call in conn.cursor.return_value.execute.call_args_list]
    assert any("TRUNCATE TABLE" in q for q in queries)
    conn.commit.assert_called_once()
    conn.close.assert_called_once()


def test_failed_fetch_does_not_touch_database():
    service, conn = service_with_connection()
    assert run_snapshot(service, None) is False
    service.get_postgres_connection.assert_not_called()
    conn.commit.assert_not_called()


def test_insert_failure_rolls_back_snapshot():
    service, conn = service_with_connection()
    conn.cursor.return_value.execute.side_effect = [None, RuntimeError("insert failed")]
    assert run_snapshot(service, [{"record_id":"demo-record","fields":{"volume":1}}]) is False
    conn.rollback.assert_called_once()
    conn.commit.assert_not_called()


def test_view_updates_preserve_dependents():
    service = DatasetTransformService()
    conn = MagicMock()
    service._connect = MagicMock(return_value=conn)
    with patch('dataset_transform_service.sql.Identifier') as identifier:
        identifier.return_value.as_string.return_value = '"v_gas_test"'
        statements = service._build_ddl("view","v_gas_test","SELECT 1 AS value")
    assert statements == ['CREATE OR REPLACE VIEW "v_gas_test" AS\nSELECT 1 AS value']
