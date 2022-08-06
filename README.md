# fuzzball

### [Installation](#installation)
### [Usage](#usage)
### [Design Overview](#design)
### [Structure](#structure)

&nbsp;

## Installation
1. `git clone git@github.com:lachlan-waugh/fuzzball.git`
2. `cd fuzzball`
3. `./fuzzer --install`
4. `./fuzzer --help`

&nbsp;

## Usage
3. `./fuzzer binary_name input_name`
4. `./fuzzer --test`
5. `./fuzzer --test <directory containing binaries and their sample input>`

&nbsp;

## Design
* [Fuzzer](#Fuzzer)
* [Harness](#Harness)
* [Strategies](#Strategies)
* [Bootstrap](#Bootstrap)
* [Coverage](#Coverage)

### Fuzzer

### Harness

### Strategies

### Bootstrap

### Coverage

&nbsp;

## Structure
```
├── fuzzer
├── fuzzball
│   ├── fuzzer.py
│   ├── strategies
│   │   ├── common.py
│   │   ├── csv.py
│   │   ├── json.py
│   │   ├── txt.py
│   │   └── xml.py
│   ├── modules
│   │   ├── coverage
│   │   │   ├── coverage.py
│   │   │   └── ptrace.py
│   │   ├── harness
│   │   │   ├── harness.py
│   │   │   └── codes.py
│   │   │   bootstrap.py
│   │   └── helper.py
│   ├── tests
│   │   ├── binaries
│   │   └── coverage
└── README.md
```