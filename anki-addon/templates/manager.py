"""
Template and Note Type Manager.
Maps generic CardPayload fields to Anki's internal Note Models (Basic, Reversed, Cloze).
"""

from typing import Any, Dict, List, Optional

try:
    from ..core.constants import SUPPORTED_TEMPLATES
    from ..core.exceptions import ValidationError
    from ..core.logger import logger
    from ..discord.models import CardPayload
except (ImportError, ValueError):
    from core.constants import SUPPORTED_TEMPLATES
    from core.exceptions import ValidationError
    from core.logger import logger
    from discord.models import CardPayload

try:
    from aqt import mw
    ANKI_AVAILABLE = True
except ImportError:
    mw = None
    ANKI_AVAILABLE = False


class TemplateManager:
    """
    Manages note model discovery, template field mapping, and validation.
    """
    def __init__(self) -> None:
        self.default_model_name = "Basic"

    def get_supported_templates(self) -> List[str]:
        """Return list of standard supported templates."""
        return list(SUPPORTED_TEMPLATES)

    def get_available_models_in_anki(self) -> List[str]:
        """Fetch all note types installed in the current Anki collection."""
        if not ANKI_AVAILABLE or mw is None or mw.col is None:
            return list(SUPPORTED_TEMPLATES)

        try:
            return [m["name"] for m in mw.col.models.all()]
        except Exception as e:
            logger.error(f"[TemplateManager] Failed fetching models from Anki: {e}")
            return list(SUPPORTED_TEMPLATES)

    def normalize_template_name(self, template_name: str) -> str:
        """Find best matching Anki model name (case-insensitive fuzzy match)."""
        clean_name = template_name.strip()
        available = self.get_available_models_in_anki()

        # Exact match
        if clean_name in available:
            return clean_name

        # Case-insensitive match
        for model in available:
            if model.lower() == clean_name.lower():
                return model

        # Match Cloze alias
        if clean_name.lower() in ("cloze", "omissao", "lacuna", "cloze deletion"):
            for model in available:
                if "cloze" in model.lower():
                    return model

        # Match Reversed alias
        if clean_name.lower() in ("reversed", "invertido", "basic (reversed)"):
            for model in available:
                if "reversed" in model.lower() and "optional" not in model.lower():
                    return model

        # Fallback to Basic
        for model in available:
            if model.lower() == "basic":
                return model

        return available[0] if available else self.default_model_name

    def map_fields_to_model(self, payload: CardPayload, model_dict: Dict[str, Any]) -> Dict[str, str]:
        """
        Map CardPayload fields (front, back, extra) to the concrete fields of an Anki model.
        """
        field_names = [f["name"] for f in model_dict.get("flds", [])]
        if not field_names:
            raise ValidationError(f"Anki note model '{model_dict.get('name')}' has no fields defined.")

        model_name = model_dict.get("name", "").lower()
        mapped: Dict[str, str] = {}

        # 1. Cloze Model
        if "cloze" in model_name:
            text_field = field_names[0]
            extra_field = field_names[1] if len(field_names) > 1 else None

            mapped[text_field] = payload.front
            if extra_field:
                mapped[extra_field] = payload.back or payload.extra
            return mapped

        # 2. Standard Models with Front / Back naming
        front_field = None
        back_field = None
        for f in field_names:
            fl = f.lower()
            if fl in ("front", "frente", "question", "pergunta", "expression", "prompt") and front_field is None:
                front_field = f
            elif fl in ("back", "verso", "answer", "resposta", "meaning", "definition") and back_field is None:
                back_field = f

        # Assign front
        if front_field:
            mapped[front_field] = payload.front
        else:
            mapped[field_names[0]] = payload.front

        # Assign back
        if back_field:
            mapped[back_field] = payload.back
        elif len(field_names) > 1:
            target = field_names[1] if field_names[1] != mapped.get(field_names[0]) else field_names[-1]
            mapped[target] = payload.back

        # Assign extra if third field exists
        if payload.extra and len(field_names) > 2:
            extra_cand = [f for f in field_names if f not in mapped]
            if extra_cand:
                mapped[extra_cand[0]] = payload.extra

        return mapped


# Global template manager singleton
template_manager = TemplateManager()
