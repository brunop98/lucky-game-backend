from sqlalchemy.orm import Session

from app.db.models.content_patches import ContentPatch


def get_active_patch(db: Session) -> dict | None:
    """
    Retorna o patch ativo no formato de contrato do frontend.
    Retorna None se não houver patch ativo.
    """

    patch = db.query(ContentPatch).filter(ContentPatch.active == True).first()

    if not patch:
        return None

    return {
        "appVersionMin": patch.app_version_min,
        "appVersionMax": patch.app_version_max,
        "contentVersion": patch.content_version,
        "mandatory": patch.mandatory,
        "download": {
            "catalogUrl": patch.catalog_url,
            "baseUrl": patch.base_url,
        },
        "sizeMb": patch.size_mb,
        "checksum": patch.checksum,
    }
