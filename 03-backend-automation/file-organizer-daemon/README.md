# 📁 Local File Organizer & Meta-Tagger Daemon

An autonomous cross-platform daemon utility that monitors operating system directories and automatically organizes unstructured files.

The system intercepts filesystem events, sorts files into structured directories, enforces consistent naming conventions, and maintains a persistent SQLite-based metadata index.

---

## 🚀 System Features

### ⚡ Event-Driven Architecture

Uses `watchdog` to listen for real-time filesystem events (create/modify) and trigger automated processing workflows.

### 📂 Dynamic Routing Resolution

Automatically classifies files based on extension into categories such as:

* Documents
* Media
* Archives
* Executables
* Other

### 🛡️ Collision-Safe File Handling

Prevents accidental overwrites by:

* Checking existing filenames
* Appending incremental suffixes (`_1`, `_2`, etc.)

### 🗃️ Metadata Indexing Layer

Stores structured file metadata in SQLite, including:

* original file name
* current file path
* file size (bytes)
* detected category
* processing timestamp

---

## ⚙️ Installation & Setup

### 1. Requirements

Ensure Python **3.10+** is installed.

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Run the daemon

```bash
python -m app.core.daemon
```

---

## 📁 Project Behavior Overview

Once started, the daemon will:

1. Monitor the target directory (`./sandbox_monitor`)
2. Detect new or modified files
3. Wait briefly for file write completion
4. Classify file type
5. Normalize filename (snake_case, lowercase)
6. Move file into category folder
7. Store metadata in SQLite database

---

## 🧠 Example Workflow

```
sandbox_monitor/
    User Manual Notes.txt
```

⬇️ becomes

```
sandbox_monitor/
    Documents/
        user_manual_notes.txt
```

And metadata is recorded in:

```
file_catalog.db
```

---

## 📊 Database Schema

Table: `file_catalog`

* `id`
* `original_name`
* `current_path`
* `file_extension`
* `file_size_bytes`
* `detected_category`
* `processed_timestamp`

---

## 🔧 Notes

* Designed for local filesystem automation
* Safe for continuous background execution
* Suitable for personal productivity pipelines or file hygiene tools

---

## 🚀 Future Improvements (optional roadmap)

* Async event processing queue
* GUI dashboard for file analytics
* Cloud sync integration
* Rule-based custom categorization engine
* Systemd / Windows service deployment

---

If you want, I can next help you:

* turn this into a **GitHub-ready repo with badges + CI**
* add a **professional architecture diagram**
* or convert it into a **pip-installable CLI tool (`file-organizer`)**
