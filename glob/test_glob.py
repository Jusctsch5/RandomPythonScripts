import glob
import logging
from pathlib import Path

logging.basicConfig(level=logging.DEBUG)

# Doesn't return data
"""
MINIDUMP_DIR=  "/data/minidump"
md_files = glob.glob("*.dmp", root_dir=MINIDUMP_DIR, recursive=True)
logging.debug(md_files)
print(md_files)

MINIDUMP_DIR=  "/data/minidump/myriad"
md_files = glob.glob("*.dmp", root_dir=MINIDUMP_DIR, recursive=True)
logging.debug(md_files)

MINIDUMP_DIR=  "/data/minidump/myriad"
md_files = glob.glob(f"{MINIDUMP_DIR}.dmp", root_dir=MINIDUMP_DIR, recursive=True)
logging.debug(md_files)
"""
# Returns data
"""
MINIDUMP_DIR=  "/data/minidump/myriad"
md_files = glob.glob(f"{MINIDUMP_DIR}.dmp", recursive=True)
logging.debug(md_files)

MINIDUMP_DIR=  "/data/minidump/myriad"
md_files = glob.glob("/data/minidump/myriad/api/*.dmp", recursive=True)
logging.debug(md_files)

MINIDUMP_DIR=  "/data/minidump/myriad"
md_files = glob.glob("/data/minidump/myriad/api/*", recursive=True)
logging.debug(md_files)

MINIDUMP_DIR=  "/data/minidump/myriad"
md_files = glob.glob("/data/minidump/myriad/api/*")
logging.debug(md_files)
"""

# Don't use root_dir.

MINIDUMP_DIR=  "/data/minidump"

md_files = glob.glob(f"{MINIDUMP_DIR}/**/*.dmp", recursive=True)
logging.debug(md_files)
md_files_basename = [Path(f).name for f in md_files]
logging.debug(md_files_basename)

md_files = glob.glob(f"{MINIDUMP_DIR}/*.dmp", recursive=True)
logging.debug(md_files)
md_files_basename = [Path(f).name for f in md_files]
logging.debug(md_files_basename)

