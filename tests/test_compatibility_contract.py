from sovereign_master.core.engine import SovereignMasterEngine
from sovereign_master.core.task_router import TaskRoute, TaskRouter


def test_legacy_process_remains_supported():
    result = SovereignMasterEngine().process("Bonjour", session_id="legacy")
    assert result["success"] is True
    assert result["verified"] is False
    assert "answer" in result


def test_router_exposes_rich_route_without_breaking_classify():
    router = TaskRouter()

    assert router.classify("please calculate 2 + 2") == "math"
    route = router.route("find the latest source")

    assert isinstance(route, TaskRoute)
    assert route.name == "research"
    assert route.requires_retrieval is True
