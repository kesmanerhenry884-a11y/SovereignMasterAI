from sovereign_master.core.engine import SovereignMasterEngine


def test_media_route_uses_media_plan():
    result = SovereignMasterEngine().process("create a video", session_id="media-test")
    assert result["route"] == "media"
    assert "media" in result["modules_used"]


def test_empty_message_is_rejected_without_provider_call():
    result = SovereignMasterEngine().process("   ")
    assert result["success"] is False
    assert "empty_input" in result["warnings"]
