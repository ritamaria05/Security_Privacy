# Projects for Security and Privacy 2025

This repository contains three comprehensive assignments focused on security and privacy topics, completed as part of the Security and Privacy course in 2025. Each assignment explores different aspects of data security, privacy assessment, and anonymization techniques.

---

## Assignment #1: Performance Benchmarking of Cryptographic Mechanisms

**Date:** April 2025

### Overview
The purpose of this project is to measure the performance of cryptographic algorithms by analyzing the time AES, RSA, and SHA-256 take to process files of different sizes. This project uses Python implementations for encryption/decryption and hashing mechanisms to provide empirical performance measurements.

### Objectives
- Benchmark symmetric encryption (AES-256) performance
- Benchmark asymmetric encryption (RSA-2048) performance
- Benchmark cryptographic hash function (SHA-256) performance
- Analyze performance across varying file sizes
- Generate statistical confidence intervals for the measurements

### Content of Assignment #1
- **Reading Material**: PDFs to guide the project, including resources on cryptographic implementations
- **Random File Generator** (`file_generation.py`): Python script to generate test files of varying sizes
- **Algorithm Implementations**:
  - `aes_256/`: AES-256 encryption/decryption implementation and performance tests
  - `rsa_2048/`: RSA-2048 encryption/decryption implementation and performance tests
  - `sha_256/`: SHA-256 hash function implementation and performance tests
- **Test Files**: Organized folders containing files of different sizes (2B to 2MB) for each algorithm
- **Code Files** (`codes/`): Consolidated Python implementations
  - `aes256.py`: AES-256 encryption/decryption functions and timing measurements
  - `rsa2048.py`: RSA-2048 encryption/decryption functions and timing measurements
  - `sha256.py`: SHA-256 hash functions and timing measurements
  - `file_generation.py`: File generation utility
- **Charts** (`gráficos/`): Performance visualization for each algorithm with confidence intervals
- **Statistical Analysis** (`intervalosDeConfiança/`): Confidence interval calculations
- **Results** (`resultados/`): Raw performance measurement data
- **Report**: Complete analysis in multiple formats
  - `Relatorio.ipynb`: Jupyter Notebook with interactive analysis
  - `Relatorio.html`: HTML version of the report
  - `Relatorio.pdf`: PDF version of the report
- **Archive** (`codes.zip`, `gráficos.zip`): Compressed files for easy distribution

### Key Findings
The project demonstrates how file size and algorithm type affect cryptographic operation performance, providing valuable insights for selecting appropriate cryptographic mechanisms based on performance requirements.

---

## Assignment #2: Privacy Impact Assessment (PIA)

**Date:** 2025

### Overview
This assignment focuses on conducting a comprehensive Privacy Impact Assessment (PIA) for a healthcare information system. The PIA methodology is used to identify and evaluate privacy risks associated with the processing of personal data, particularly in the context of the COPMODO (Community-based Personalized Management Of Diabetes and Obesity) system.

### Objectives
- Identify privacy risks in data processing systems
- Assess the impact and likelihood of privacy breaches
- Analyze different threat scenarios
- Propose mitigation measures and controls
- Apply PIA principles and best practices

### Content of Assignment #2
- **Assignment Description** (`Assignment2-PIA.pdf`): Official assignment requirements and guidelines
- **PIA Report** (`Privacy Impact Assessment.pdf` and `.docx`): Complete privacy impact assessment documentation
- **Risk Analysis Documents**:
  - `PIA - Acesso ilegítimo dos dados.pdf`: Analysis of unauthorized data access risks
  - `PIA - Desaparecimento de dados.pdf`: Analysis of data loss/disappearance risks
  - `PIA - Modificação Indesejada dos dados.pdf`: Analysis of unwanted data modification risks
  - `PIA - Medidas planeadas ou existentes.pdf`: Planned and existing mitigation measures
  - `PIA - Privacy Impact Assessment.pdf`: Consolidated PIA summary
- **Risk Mappings** (`mapeamentos/`):
  - `MapeamentoRiscoInicial.png`: Initial risk mapping visualization
  - `MapeamentoRiscoFinal.png`: Final risk mapping after mitigation measures
- **Supporting Materials**:
  - `COPMODEdescricao.png`: COPMODO system description diagram
  - `idi-privacy-impact-assessment.pdf`: IDI PIA methodology reference
  - `pia-principles-infography.pdf`: PIA principles infographic
- **Example Documents** (`example docs/`): Reference materials and templates

### Key Components
The PIA addresses three main privacy risks:
1. **Unauthorized Data Access**: Assessment of risks related to illegitimate access to personal health data
2. **Data Loss/Disappearance**: Evaluation of risks associated with data availability and potential loss
3. **Unwanted Data Modification**: Analysis of data integrity risks and unauthorized modifications

The assessment includes both initial risk evaluations and final risk states after implementing security and privacy controls.

---

## Assignment #3: Dataset Anonymization

**Date:** 2025

### Overview
This project explores data anonymization techniques applied to sensitive datasets, implementing and analyzing k-anonymity and l-diversity privacy models. The assignment uses real-world datasets to demonstrate how anonymization can protect individual privacy while maintaining data utility for analysis.

### Objectives
- Implement k-anonymity and l-diversity privacy models
- Analyze the trade-off between privacy protection and data utility
- Evaluate anonymization quality at both attribute and dataset levels
- Explore different anonymization parameters and their effects
- Visualize privacy and utility metrics

### Content of Assignment #3
- **Assignment Description** (`Assignment3-Anonymization_of_a_Dataset.pdf`): Official assignment requirements
- **Report** (`Relatorio_trab3.pdf`): Complete anonymization project report
- **Analysis Documents**:
  - `analisesMax.docx`: Analysis documentation (contributor: Max)
  - `analisesRita.docx`: Analysis documentation (contributor: Rita)
  - `relatorio.docx`: Main report document
  - `defesa.pdf`: Project defense presentation
- **Anonymized Datasets**:
  - `example.deid`: Example anonymized dataset
  - `k-anon10_L-div2.deid`: Anonymized dataset with k=10 anonymity and l=2 diversity
- **Plot Generators** (`plotGenerators/`): Python scripts for generating visualization plots
  - `attributeLevelQuality.py`: Attribute-level quality metrics visualization
  - `datasetLevelQuality.py`: Dataset-level quality metrics visualization
  - `dados_iniciais.py`: Initial data analysis plots
  - `threshold.py`: Risk threshold visualization
  - `variacoes_part2.py`: Parameter variation analysis (part 2)
  - `variacoes_parte1.py`: Parameter variation analysis (part 1)
- **Plots** (`plots/`): Generated visualizations including:
  - Attribute-level quality heatmaps for different k and l values
  - Attribute weight analyses for different privacy models
  - Risk metrics (highest risk, success rate, records at risk)
  - Initial risk assessments (journalist and marketer attack scenarios)
  - Comparison plots for k-anonymity with t-closeness vs. l-diversity

### Key Techniques
- **k-Anonymity**: Ensures each record is indistinguishable from at least k-1 other records
- **l-Diversity**: Ensures sensitive attributes have at least l well-represented values
- **Quality Metrics**:
  - Missings percentage
  - Generalization intensity
  - Granularity
  - Non-uniform entropy
  - Squared error
- **Risk Assessment**: Evaluation of re-identification risks under different attacker models

### Key Findings
The project demonstrates the balance between privacy protection (higher k and l values) and data utility (measured through various quality metrics). Multiple configurations were tested and analyzed to understand optimal anonymization strategies.

---

## Repository Structure

```
Security_Privacy/
├── README.md                    # This file
├── assignment#1/                # Cryptographic Performance Benchmarking
│   ├── aes_256/                # AES-256 implementation and tests
│   ├── rsa_2048/               # RSA-2048 implementation and tests
│   ├── sha_256/                # SHA-256 implementation and tests
│   ├── codes/                  # Consolidated code files
│   ├── gráficos/               # Performance charts
│   ├── intervalosDeConfiança/  # Statistical confidence intervals
│   ├── resultados/             # Raw performance data
│   ├── reading_material/       # Reference materials
│   └── Relatorio.*             # Report (ipynb, html, pdf)
├── assignment#2/                # Privacy Impact Assessment
│   ├── mapeamentos/            # Risk mapping visualizations
│   ├── example docs/           # Reference materials
│   └── PIA reports (*.pdf)     # Assessment documents
└── assignment#3/                # Dataset Anonymization
    ├── plotGenerators/         # Python plotting scripts
    ├── plots/                  # Generated visualizations
    └── *.deid                  # Anonymized datasets
```

---

## Technologies Used

- **Python 3**: Primary programming language for all implementations
- **Cryptography Libraries**: For AES, RSA, and SHA-256 implementations
- **Matplotlib/Pandas**: Data visualization and analysis
- **Jupyter Notebook**: Interactive analysis and reporting
- **ARX Data Anonymization Tool**: Dataset anonymization (inferred from .deid files)

---

## Authors

- Rita Maria (ritamaria05)
- Contributors: Max (Assignment #3)

---

## License

This repository contains academic coursework. Please respect academic integrity policies when referencing or using this code.
