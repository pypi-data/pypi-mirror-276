import orjson
import base64
from dataclasses import dataclass, asdict
from enum import Enum, auto, Flag


# @dataclass
# class ReportJobEvent:
#     report_jod_id: int
#     symbol: str
#     past_months: int


class NotificationType(Flag):
    EMAIL = auto()
    SMS = auto()
    TELEGRAM = auto()


@dataclass
class ReportJobEvent:
    report_jod_id: int
    symbol: str
    past_months: int

    notification_type: NotificationType
    mobile: None | str = None
    email: None | str = None

    @classmethod
    def from_dict(cls, d: dict):
        return cls(
            report_jod_id=d["report_jod_id"],
            symbol=d["symbol"],
            past_months=d["past_months"],
            notification_type=NotificationType(d["notification_type"]),
            mobile=d.get("mobile"),
            email=d.get("email"),
        )

    @classmethod
    def from_base64_str(cls, s: str):
        base64_decoded_bytes: bytes = base64.b64decode(s)
        d: dict = orjson.loads(base64_decoded_bytes)
        return cls(
            report_jod_id=d["report_jod_id"],
            symbol=d["symbol"],
            past_months=d["past_months"],
            notification_type=NotificationType(d["notification_type"]),
            mobile=d["mobile"],
            email=d["email"],
        )

    def to_bytes(self) -> bytes:
        return orjson.dumps(asdict(self), option=orjson.OPT_NAIVE_UTC)

    def to_dict(self) -> dict:
        d = asdict(self)
        d["notification_type"] = self.notification_type.value
        return d


@dataclass
class StockAnalysisEvent:
    symbol: str
    start: str
    end: str
    email: str

    @property
    def get_key(self):
        return f"{self.symbol}_{self.start}_{self.end}"


@dataclass
class NotificationEvent:
    title: str
    msg: str

    notification_type: NotificationType
    mobile: None | str = None
    email: None | str = None

    @classmethod
    def from_dict(cls, d: dict):
        return cls(
            title=d["title"],
            msg=d["msg"],
            notification_type=NotificationType(d["notification_type"]),
            mobile=d.get("mobile"),
            email=d.get("email"),
        )

    @classmethod
    def from_base64_str(cls, s: str):
        base64_decoded_bytes: bytes = base64.b64decode(s)
        d: dict = orjson.loads(base64_decoded_bytes)
        return cls(
            title=d["title"],
            msg=d["msg"],
            notification_type=NotificationType(d["notification_type"]),
            mobile=d["mobile"],
            email=d["email"],
        )

    def to_bytes(self) -> bytes:
        return orjson.dumps(asdict(self), option=orjson.OPT_NAIVE_UTC)
