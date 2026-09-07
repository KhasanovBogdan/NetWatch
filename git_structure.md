# Структура Git-репозитория

Актуальная структура репозитория проекта NetWatch.

```text
practice-netwatch/
├── README.md
├── git_structure.md
├── terms.md
│
├── docs/
│   ├── project.md
│   ├── members.md
│   ├── journal.md
│   ├── resources.md
│   ├── llm_report.md
│   ├── partner_report.md
│   ├── netwatch_tutorial.md
│   ├── netwatch_final_report.md
│   └── images/
│       └── architecture.png
│
├── site/
│   ├── index.html
│   ├── about.html
│   ├── members.html
│   ├── journal.html
│   ├── resources.html
│   ├── netwatch.html
│   ├── style.css
│   └── images/
│       └── architecture.png
│
├── src/
│   ├── main.py
│   ├── requirements.txt
│   └── README.md
│
├── reports/
│   ├── practice_report_template.docx
│   ├── practice_report.docx
│   └── practice_report.pdf
│
└── task/
    ├── practice_task.md
    └── templates/
```

## Правила размещения файлов

- Все Markdown-документы, кроме `README.md`, размещаются в `docs/`.
- Бинарные отчёты (DOCX, PDF) — в `reports/`.
- Файлы статического сайта — в `site/`.
- Исходный код программы — в `src/`.
- Задание практики и шаблоны — в `task/`.
