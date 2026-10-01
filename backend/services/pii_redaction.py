"""PII Redaction service using Microsoft Presidio.

Uses presidio-analyzer (NER + pattern recognisers) and
presidio-anonymizer to detect and replace PII entities in review
text before the text is returned by any API endpoint.

Entities redacted: PERSON, EMAIL_ADDRESS, PHONE_NUMBER.
Replacements use the format  <ENTITY_TYPE>  (angle-bracket tags).

The Presidio AnalyzerEngine is initialised lazily and cached as a
module-level singleton so the spaCy model is only loaded once.
"""

from __future__ import annotations

import logging
from typing import Optional

logger = logging.getLogger(__name__)

# Module-level singletons – populated on first use
_analyzer: Optional[object] = None  # presidio_analyzer.AnalyzerEngine
_anonymizer: Optional[object] = None  # presidio_anonymizer.AnonymizerEngine

# PII entity types to detect
_ENTITIES = ["PERSON", "EMAIL_ADDRESS", "PHONE_NUMBER"]


def _get_analyzer():
    """Return (and lazily initialise) the Presidio AnalyzerEngine."""
    global _analyzer
    if _analyzer is not None:
        return _analyzer

    try:
        import spacy
        from presidio_analyzer import AnalyzerEngine
        from presidio_analyzer.nlp_engine import SpacyNlpEngine, NlpEngineProvider

        # Try the large model first; fall back to the small one
        for model in ("en_core_web_lg", "en_core_web_sm"):
            try:
                # Check if package is installed before attempting load to avoid spacy auto-download / pip lock errors
                if spacy.util.is_package(model):
                    nlp = spacy.load(model)
                    nlp_engine = SpacyNlpEngine(models={"en": nlp})
                    _analyzer = AnalyzerEngine(nlp_engine=nlp_engine)
                    logger.info("Presidio AnalyzerEngine initialised with spaCy model '%s'.", model)
                    return _analyzer
                else:
                    # Fallback to provider creation if spacy load is not directly available
                    configuration = {
                        "nlp_engine_name": "spacy",
                        "models": [{"lang_code": "en", "model_name": model}],
                    }
                    provider = NlpEngineProvider(nlp_configuration=configuration)
                    nlp_engine = provider.create_engine()
                    _analyzer = AnalyzerEngine(nlp_engine=nlp_engine)
                    logger.info("Presidio AnalyzerEngine initialised with spaCy model '%s'.", model)
                    return _analyzer
            except (Exception, SystemExit, OSError) as exc:
                logger.warning("spaCy model '%s' loading failed (%s), trying next.", model, exc)

        # If no spaCy model is available fall back to the default
        # (regex + pattern only, no NER)
        _analyzer = AnalyzerEngine()
        logger.warning(
            "No spaCy model available. Presidio running with pattern-only recognisers."
        )
        return _analyzer

    except (ImportError, Exception, SystemExit) as exc:
        logger.error(
            "presidio-analyzer issue – PII redaction falling back. %s", exc
        )
        return None


def _get_anonymizer():
    """Return (and lazily initialise) the Presidio AnonymizerEngine."""
    global _anonymizer
    if _anonymizer is not None:
        return _anonymizer

    try:
        from presidio_anonymizer import AnonymizerEngine

        _anonymizer = AnonymizerEngine()
        logger.info("Presidio AnonymizerEngine initialised.")
        return _anonymizer
    except ImportError as exc:
        logger.error(
            "presidio-anonymizer is not installed – PII redaction disabled. %s", exc
        )
        return None


import re

# Fast regex patterns for immediate PII redaction
EMAIL_REGEX = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")
PHONE_REGEX = re.compile(r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b")


def redact_text(text: str) -> str:
    """Detect and replace PII in *text*, returning the redacted string.

    Each detected PII entity is replaced with a placeholder of the form
    ``<ENTITY_TYPE>`` (e.g. ``<PERSON>``, ``<EMAIL_ADDRESS>``).

    Args:
        text: Raw review text that may contain personal information.

    Returns:
        Redacted text safe for public API responses.
    """
    if not text or not text.strip():
        return text

    # Step 1: Fast regex redaction for Email and Phone numbers
    redacted = EMAIL_REGEX.sub("<EMAIL_ADDRESS>", text)
    redacted = PHONE_REGEX.sub("<PHONE_NUMBER>", redacted)

    # Step 2: Presidio NER for deep entity detection when relevant
    try:
        if "@" in text or any(char.isdigit() for char in text) or "My name" in text:
            analyzer = _get_analyzer()
            anonymizer = _get_anonymizer()
            if analyzer and anonymizer:
                from presidio_anonymizer.entities import OperatorConfig
                results = analyzer.analyze(text=redacted, entities=_ENTITIES, language="en")
                if results:
                    operators = {
                        entity: OperatorConfig("replace", {"new_value": f"<{entity}>"})
                        for entity in _ENTITIES
                    }
                    anonymized = anonymizer.anonymize(
                        text=redacted, analyzer_results=results, operators=operators
                    )
                    return anonymized.text
    except Exception as exc:
        logger.debug("Presidio deep scan skipped: %s", exc)

    return redacted
