## Introduction

This is a light backtesting platform for stocks, integrating some well-known tools including Backtrader and Quantstats. 
Backtrader: https://github.com/mementum/backtrader.git
Quantstats: https://github.com/ranaroussi/quantstats.git 

This project will demonstrate an ongoing learning trajectory in the area of quantitative investing from zero, continuously expanding to different asset classes, more useful tools, and more complex strategies.

To be continue...

## Project Tree
```
hello_backtrader
├─ analysis
│  ├─ analyzer.py
│  ├─ reports
│  │  └─ report.html
│  └─ __init__.py
├─ config.yaml
├─ core
│  ├─ backtest_engine.py
│  ├─ data_manager.py
│  ├─ optimization_engine.py
│  ├─ providers
│  │  ├─ stock_provider_akshare.py
│  │  ├─ stock_provider_yahoo.py
│  │  └─ __init__.py
│  ├─ storage
│  │  ├─ sqlite_adapter.py
│  │  └─ __init__.py
│  └─ __init__.py
├─ data
│  └─ AAPL.csv
├─ main.py
├─ README.md
├─ requirements.txt
└─ strategies
   ├─ test_strategy.py
   └─ __init__.py

```

## Author Intro

I'm Peter, currently a final year student in Chinese University of Hong Kong. I study in the major of Quantitative Finance and Risk Management Science, and is now pursuing a career in the quant world. 

My passion is to integrate my cross-disciplinary skills from finance, computer science, and math to solve real-case problems. I enojoy innovating and creating useful tools, and hope to become financially independent by doing something I love to do. 