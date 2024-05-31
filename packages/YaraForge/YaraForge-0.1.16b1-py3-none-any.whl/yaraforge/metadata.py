import os
from pathlib import Path
appdata_roaming = Path(os.getenv('APPDATA'))

plugin_path = appdata_roaming / "Hex-Rays" / "IDA Pro" / "plugins"


metadata = {
    "plugin_name": "YaraForge",
    "plugin_dir_name": "yaraforge",
    "authors": [
        {"name": "Zhao Xinn", "email": "zhaoxinzhang0429@gmail.com"},
        {"name": "Tsai YA-HSUAN", "email": "aooood456@gmail.com"},
        {"name": "Ting0525", "email": "zg45154551@gmail.com"},
    ],
    "github_url": "https://github.com/zhaoxinnZ/YaraForge",
    "description": "A plugin for IDA Pro to generate Yara rules from binary files.",
    "python_requires": ">=3.8, <3.12",
    "IDAPython_requires": ">=7.0",
    "capa_version": "7.0.1",
}

yaraforge_base_dir = plugin_path / metadata['plugin_dir_name']
cache_dir = yaraforge_base_dir / "cache"
results_dir = cache_dir / "results"
logger_dir = yaraforge_base_dir / "logs"

pathnames = {
    "yaraforge_dir": yaraforge_base_dir,
    "cache_dir": cache_dir,
    "results_dir": results_dir,
    "logger_dir": logger_dir,
    "pretty_dump_dir": results_dir / "pretty_dump",
    "instructions_dir": results_dir / "instructions",
    "yara_rules_dir": results_dir / "yara_rules",
    "merged_rules_dir": results_dir / "merged_rules",
    "compiled_rules_dir": results_dir / "compiled_rules",
}