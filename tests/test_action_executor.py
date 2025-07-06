from orchestrator.action_executor import execute_action

def test_execute_ping_action_success():
    row = {
        "ACTION": "ping_test",
        "SOURCE": "127.0.0.1",
        "DESTINATION": "127.0.0.1"
    }
    output = execute_action("ping_test", row)
    assert "successful" in output or "failed" in output or "error" in output
