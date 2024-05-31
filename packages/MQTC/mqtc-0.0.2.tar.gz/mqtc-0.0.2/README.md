# Question Type Classification

<p align="center">
    🤗 <a href="">Hugging Face</a> | 📑 <a href="">Technical Report</a> ｜ 🖥️ <a href="">Demo</a>
</p>
<br>

We introduce Question Type Classification, an AI solution for mathematics question type classification (MQTC). This
solution has 4 methods of classifying mathematics question type, 
## News and Updates

* [2024/06] Release package for Math Type Classification.

## Models and Performance

* Model Mathematics Question Type Classification
 
| Model Version | Accuracy | F1-Score | Precision |  Recall  | Test Size |
|:-------------:|:--------:|:--------:|:---------:|:--------:|:---------:|
|   MQTC 2.0    |   **0.8725**   |   **0.7927**   |   **0.7874**    |   **0.8226**   |    800    |


## Table of Contents

* [Installation](#Installation)
* [Quick Start](#quick-start)
* [Evaluation](#evaluation)
* [Training](#training)
* [Development](#development)
* [Demo](#demo)
* [API](#api)
* [Limitation](#limitation)
* [FAQ](#faq)
* [Citation](#citation)


## Installation

Install latest version.


## Quick Start
```bash
from question_type_cls import math_type_cls

text = '1+1'

mathtype = math_type_cls.math_type_cls(text, model_type='model-based')

texts = ['1+1', '1+2']

mathtype = math_type_cls.math_type_cls(texts, model_type='model-based')
mathtype = math_type_cls.math_type_cls(texts, model_type='rule-based')
```

## Limitation


## FAQ

If you meet problems, please refer to [FAQ](FAQ.md) and the issues first to search a solution before you launch a new
issue.

## Citation

Please cite the repo if you find the repository helpful.

```
@misc{mathgpt,
    title={Question Type Classification Technical Report},
    author={FTECH-AI},
    year={2023-2024}
}
```

## Outlook

We are constantly fine-tuning our models and gearing up to unveil some exciting updates. Stay tuned for the latest and
greatest from our end!
