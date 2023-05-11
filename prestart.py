import subprocess
import sys

from alembic.config import Config
from alembic import command

from app.main import ROOT


alembic_cfg = Config(ROOT / "alembic.ini")

sys.path.append(ROOT)

subprocess.run([sys.executable, "-m", "app.backend_pre_start"])
command.upgrade(alembic_cfg, "head")
subprocess.run([sys.executable, "-m", "app.initial_data"])
