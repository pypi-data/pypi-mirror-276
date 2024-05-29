# Krabby - Flashtext package with Rust backend

## Installation

```sh
pip install krabby
```

## Usage

```py
from krabby import KeywordProcessor

keyword_processor = KeywordProcessor(False)
keyword_processor.put("apple")
keyword_processor.put("orange")

keyword_processor.extract("I have an Apple, i have a pencile")
```
