autonomous-incident-commander/
│
├── app/
│   ├── main.py                 # Entry point
│   ├── config.py              # Env variables
│
│   ├── simulator/
│   │   └── log_simulator.py
│
│   ├── parser/
│   │   └── log_parser.py
│
│   ├── router/
│   │   └── router.py
│
│   ├── agents/
│   │   ├── logs_agent.py
│   │   ├── metrics_agent.py
│   │   └── commander_agent.py
│
│   ├── intelligence/
│   │   └── resolution_engine.py
│
│   ├── alerting/
│   │   └── email_alert.py
│
│   └── models/
│       └── log_model.py
│
├── data/
│   └── logs.txt
│
├── .env
├── requirements.txt
├── Dockerfile
└── README.md