from dataclasses import dataclass, asdict
from datetime import datetime, timezone, timedelta
import math


def utc(value):
    if isinstance(value, str):
        value = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("Timestamp deve conter fuso horário")
    return value.astimezone(timezone.utc)


@dataclass(frozen=True)
class Reading:
    sensorId: int
    measuredAt: str
    temperatureCelsius: float | None
    airHumidityPercent: float | None
    soilMoisturePercent: float | None
    batteryPercent: float | None = 100
    source: str = "SIMULATED"
    rainfallMillimeters: float | None = None
    rainfallIntervalStart: str | None = None

    def validate(self, now=None):
        if self.sensorId < 1 or self.source != "SIMULATED":
            raise ValueError("Sensor positivo e origem SIMULATED obrigatórios")
        timestamp = utc(self.measuredAt)
        if timestamp > utc(now or datetime.now(timezone.utc)) + timedelta(minutes=5):
            raise ValueError("Timestamp ultrapassa tolerância futura")
        for name, lower, upper in [("temperatureCelsius", -50, 70), ("airHumidityPercent", 0, 100),
                                    ("soilMoisturePercent", 0, 100), ("batteryPercent", 0, 100),
                                    ("rainfallMillimeters", 0, 999999.999)]:
            value = getattr(self, name)
            if value is not None and (not math.isfinite(value) or not lower <= value <= upper):
                raise ValueError(f"Valor inválido: {name}")
        if all(getattr(self, n) is None for n in ("temperatureCelsius", "airHumidityPercent",
                                               "soilMoisturePercent", "rainfallMillimeters", "batteryPercent")):
            raise ValueError("Ao menos uma medição é obrigatória")
        if self.rainfallMillimeters is not None:
            if self.rainfallIntervalStart is None or utc(self.rainfallIntervalStart) >= timestamp:
                raise ValueError("Chuva requer intervalo válido")
        elif self.rainfallIntervalStart is not None:
            raise ValueError("Intervalo sem medição de chuva")
        return self

    def payload(self):
        return {k: v for k, v in asdict(self).items() if v is not None}
