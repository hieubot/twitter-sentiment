from torch import nn
from transformers import BertModel

import config


class SentimentClassifier(nn.Module):
    def __init__(self, n_classes: int):
        super(SentimentClassifier, self).__init__()
        self.model = BertModel.from_pretrained(config.PRETRAINED_MODEL_NAME)
        self.dropout = nn.Dropout(p=0.3)
        self.out = nn.Linear(self.bert.config.hidden_size, n_classes)
        self.softmax = nn.Softmax(dim=1)

    def forward(self, input_ids, attention_mask):
        _, pooled_output = self.model(
            input_ids=input_ids, attention_mask=attention_mask
        )
        output = self.drop(pooled_output)
        output_ = self.out(output)
        return self.softmax(output_)