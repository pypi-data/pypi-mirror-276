# Firestore Trigger

Firestore Trigger is a CLI tool designed to automate the creation and updating of channels and triggers in Firestore based on configurations defined in a YAML file.


### Installation

1. Clone the repository:

```bash
git clone https://github.com/airspot-dev/cm-sync.git
cd cm-sync
```

2. Activate the Poetry shell:

```bash
poetry shell
```

3. Install dependencies using Poetry:

```bash
poetry install
```

## Usage

The tool provides commands for syncing channels and triggers with Firestore database.

### To Update:

- Using standard input (stdin)/pipe to pass the YAML content directly:

```bash
cat path/to/your/trigger.yaml | cm-sync
```

- Using a file path to specify the YAML file:

```bash
cm-sync -f path/to/your/trigger.yaml
```
