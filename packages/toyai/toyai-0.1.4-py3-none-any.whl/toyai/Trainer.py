from .ETL import ETL
from dataclasses import dataclass, field


@dataclass
class TrainResult:
    train_losses: list[float] = field(default_factory=list)
    train_accuracies: list[float] = field(default_factory=list)
    val_losses: list[float] = field(default_factory=list)
    val_accuracies: list[float] = field(default_factory=list)
    epochs: int = field(default_factory=int)


class Trainer:
    model = None

    def __init__(
        self,
        etl: ETL | None,
        model,
        train_loader,
        val_loader,
        device=None,
    ) -> None:
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.etl = etl
        self.model = model
        self.device = device
