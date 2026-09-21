from sovereign_master.core.engine import SovereignMasterEngine


def test_engine_chat_uses_modern_orchestration_contract():
    result = SovereignMasterEngine().chat("Bonjour", conversation_id="demo")

    assert result.success is True
    assert result.response
    assert result.classification == "UNCERTAIN"


def test_engine_capabilities_do_not_claim_unimplemented_rag():
    capabilities = SovereignMasterEngine().capabilities()

    assert capabilities["rag"] is False
    assert capabilities["pgvector"] is False
    assert capabilities["location"]["consent_required"] is True
    assert capabilities["location"]["turn_by_turn_navigation"] is False
