from torch.utils.data import DataLoader
from .ETL import ETL
import torch
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
        train_loader: DataLoader,
        val_loader: DataLoader | None,
        device=torch.device("cuda" if torch.cuda.is_available() else "cpu"),
    ) -> None:
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.etl = etl
        self.model = model
        self.device = device

    def validate(self):
        if self.val_loader != None:
            self.model.eval()
            val_loss, val_accuracy = 0, 0
            all_preds, all_labels = [], []

            for batch in self.val_loader:
                batch = tuple(b.to(self.device) for b in batch)
                inputs, masks, labels = batch

                with torch.no_grad():
                    outputs = self.model(inputs, attention_mask=masks, labels=labels)

                loss = outputs.loss
                logits = outputs.logits
                val_loss += loss.item()
                preds = torch.argmax(logits, dim=1)

                all_preds.extend(preds.cpu().numpy())
                all_labels.extend(labels.cpu().numpy())
                val_accuracy += (preds == labels).cpu().numpy().mean()

        return (val_loss / len(self.val_loader), val_accuracy / len(self.val_loader))

    def compute_accuracy(self, logits, labels):
        preds = torch.argmax(logits, dim=-1)
        return torch.mean((preds == labels).type(torch.float)).item()
