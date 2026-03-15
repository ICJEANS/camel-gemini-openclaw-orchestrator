import unittest
from src.openclaw_bridge import OpenClawBridge


class TestOpenClawBridgeTargeting(unittest.TestCase):
    def test_uuid_session_maps_to_session_id(self):
        b = OpenClawBridge(session_key='123e4567-e89b-12d3-a456-426614174000', dry_run=False)
        cmd = b._build_cmd('hello', timeout_seconds=30)
        self.assertIn('--session-id', cmd)

    def test_agent_session_key_maps_to_agent(self):
        b = OpenClawBridge(session_key='agent:main:webchat:direct:abc', dry_run=False)
        cmd = b._build_cmd('hello', timeout_seconds=30)
        idx = cmd.index('--agent')
        self.assertEqual(cmd[idx + 1], 'main')

    def test_missing_session_falls_back_to_main_agent(self):
        b = OpenClawBridge(session_key=None, dry_run=False)
        cmd = b._build_cmd('hello', timeout_seconds=30)
        idx = cmd.index('--agent')
        self.assertEqual(cmd[idx + 1], 'main')


if __name__ == '__main__':
    unittest.main()
