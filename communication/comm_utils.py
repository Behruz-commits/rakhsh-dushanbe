# path: communication/comm_utils.py
import json
import logging
from datetime import datetime

logger = logging.getLogger("rakhsh.comm")

def encode_message(data: dict) -> str:
    return json.dumps(data, ensure_ascii=False)

def decode_message(payload: str) -> dict:
    try:
        return json.loads(payload)
    except Exception as e:
        logger.exception("decode_message failed")
        return {}

def log_event(level: str, tag: str, msg: str, **kwargs):
    payload = {
        "ts": datetime.utcnow().isoformat()+"Z",
        "tag": tag,
        "msg": msg,
        **kwargs
    }
    logger.info(json.dumps(payload, ensure_ascii=False))
