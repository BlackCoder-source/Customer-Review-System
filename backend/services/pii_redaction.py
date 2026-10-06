"""PII Redaction service using Microsoft Presidio.

Uses presidio-analyzer (NER + pattern recognisers) and
presidio-anonymizer to detect and replace PII entities in review
text before the text is returned by any API endpoint.

Entities redacted: PERSON, EMAIL_ADDRESS, PHONE_NUMBER.
Replacements use the format  <ENTITY_TYPE>  (angle-bracket tags).

The Presidio AnalyzerEngine is initialised eagerly at module load
time so the spaCy model is only loaded once and all subsequent
calls to redact_text are fast.
"""

from __future__ import annotations

import logging
import re
from typing import Optional

logger = logging.getLogger(__name__)

# PII entity types to detect
_ENTITIES = ["PERSON", "EMAIL_ADDRESS", "PHONE_NUMBER"]

# Fast regex patterns for immediate PII redaction (always available)
EMAIL_REGEX = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")
PHONE_REGEX = re.compile(r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b")


# ---------------------------------------------------------------------------
# Eager initialisation of Presidio engines (runs once at import time)
# ---------------------------------------------------------------------------

def _init_analyzer():
    """Initialise the Presidio AnalyzerEngine with a spaCy model."""
    try:
        import spacy
        from presidio_analyzer import AnalyzerEngine
        from presidio_analyzer.nlp_engine import SpacyNlpEngine

        for model in ("en_core_web_sm", "en_core_web_lg"):
            try:
                if spacy.util.is_package(model):
                    nlp = spacy.load(model)
                    # Ensure lang_code metadata is set for Presidio compatibility
                    if not nlp.meta.get("lang"):
                        nlp.meta["lang"] = "en"
                    nlp_engine = SpacyNlpEngine(models={"en": model})
                    analyzer = AnalyzerEngine(nlp_engine=nlp_engine)
                    logger.info(
                        "Presidio AnalyzerEngine initialised with spaCy model '%s'.",
                        model,
                    )
                    return analyzer
            except (Exception, SystemExit, OSError) as exc:
                logger.warning(
                    "spaCy model '%s' loading failed (%s), trying next.", model, exc
                )

        # Fallback: regex + pattern only, no NER
        analyzer = AnalyzerEngine()
        logger.warning(
            "No spaCy model available. Presidio running with pattern-only recognisers."
        )
        return analyzer

    except (ImportError, Exception, SystemExit) as exc:
        logger.error("presidio-analyzer issue – PII redaction falling back. %s", exc)
        return None


def _init_anonymizer():
    """Initialise the Presidio AnonymizerEngine."""
    try:
        from presidio_anonymizer import AnonymizerEngine

        anonymizer = AnonymizerEngine()
        logger.info("Presidio AnonymizerEngine initialised.")
        return anonymizer
    except ImportError as exc:
        logger.error(
            "presidio-anonymizer is not installed – PII redaction disabled. %s", exc
        )
        return None


# Singletons – loaded once at import time
_analyzer = _init_analyzer()
_anonymizer = _init_anonymizer()

# Pre-import OperatorConfig if available
try:
    from presidio_anonymizer.entities import OperatorConfig as _OperatorConfig
except ImportError:
    _OperatorConfig = None


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

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

    # Step 2: Presidio NER for deep entity detection (PERSON names, etc.)
    if _analyzer and _anonymizer and _OperatorConfig:
        try:
            results = _analyzer.analyze(
                text=redacted, entities=_ENTITIES, language="en"
            )
            if results:
                operators = {
                    entity: _OperatorConfig("replace", {"new_value": f"<{entity}>"})
                    for entity in _ENTITIES
                }
                anonymized = _anonymizer.anonymize(
                    text=redacted, analyzer_results=results, operators=operators
                )
                return anonymized.text
        except Exception as exc:
            logger.debug("Presidio NER scan failed for a review: %s", exc)

    return redacted
