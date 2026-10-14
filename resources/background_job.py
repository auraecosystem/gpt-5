
"""
LMLM Runtime Configuration
Model registry, hardware detection, Petals networking,
and asynchronous background-job monitoring.
"""

import asyncio
import logging
import os
from dataclasses import dataclass
from typing import Optional

import torch
import cronitor
from cpufeature import CPUFeature
from petals.constants import PUBLIC_INITIAL_PEERS


# --------------------------------------------------
# Logging
# --------------------------------------------------

logging.basicConfig(
    level=os.getenv("LMLM_LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger("lmlm.runtime")


# --------------------------------------------------
# Model Registry
# --------------------------------------------------

@dataclass(frozen=True)
class ModelInfo:
    repo: str
    adapter: Optional[str] = None


MODELS = (
    ModelInfo(repo="web4app/Llama3-450b-hf"),
    ModelInfo(repo="stabilityai/StableBeluga2"),
    ModelInfo(repo="seriki/llama-65b-hf"),
    ModelInfo(
        repo="seriki/llama-65b-hf",
        adapter="timdettmers/guanaco-65b",
    ),
    ModelInfo(repo="web4hub/bloomz"),
)

DEFAULT_MODEL_NAME = "lmlm"


# --------------------------------------------------
# Runtime Configuration
# --------------------------------------------------

PLATFORM_NAME = "Aegis"

# Set LMLM_DEVICE=cpu or LMLM_DEVICE=cuda to override.
DEVICE_OVERRIDE = os.getenv("LMLM_DEVICE", "auto").lower()

STEP_TIMEOUT = 5 * 60
MAX_SESSIONS = 500

INITIAL_PEERS = tuple(PUBLIC_INITIAL_PEERS)


def configure_hardware():
    """Select a supported PyTorch device and tensor dtype."""

    if DEVICE_OVERRIDE == "cuda":
        if not torch.cuda.is_available():
            raise RuntimeError(
                "CUDA was requested, but no CUDA device is available."
            )
        device = torch.device("cuda")

    elif DEVICE_OVERRIDE == "cpu":
        device = torch.device("cpu")

    elif DEVICE_OVERRIDE == "auto":
        device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )

    else:
        raise ValueError(
            f"Unsupported LMLM_DEVICE: {DEVICE_OVERRIDE!r}"
        )

    if device.type == "cuda":
        dtype = (
            torch.bfloat16
            if torch.cuda.is_bf16_supported()
            else torch.float16
        )

    else:
        supports_avx512 = (
            CPUFeature["AVX512f"]
            and CPUFeature["OS_AVX512"]
        )
        dtype = (
            torch.bfloat16
            if supports_avx512
            else torch.float32
        )

    logger.info(
        "Platform=%s | Device=%s | Dtype=%s",
        PLATFORM_NAME,
        device,
        dtype,
    )

    return device, dtype


TORCH_DEVICE, TORCH_DTYPE = configure_hardware()


# --------------------------------------------------
# Cronitor Monitoring
# --------------------------------------------------

MONITOR_NAME = "important-background-job"
monitor = cronitor.Monitor(MONITOR_NAME)


async def perform_job():
    """Execute a monitored background job."""

    try:
        monitor.ping(state="run")
        logger.info("Background job started.")

        # Replace this placeholder with actual LMLM work.
        await asyncio.sleep(2)

        monitor.ping(state="complete")
        logger.info("Background job completed successfully.")

    except Exception:
        logger.exception("Background job failed.")

        try:
            monitor.ping(state="fail")
        except Exception:
            logger.exception("Failed to report job failure to Cronitor.")

        raise


async def main():
    """Application entry point."""

    logger.info("Starting LMLM runtime.")
    logger.info("Registered models: %d", len(MODELS))
    logger.info("Configured initial peers: %d", len(INITIAL_PEERS))
    logger.info("Maximum configured sessions: %d", MAX_SESSIONS)

    await perform_job()


# --------------------------------------------------
# Entry Point
# --------------------------------------------------

if __name__ == "__main__":
    asyncio.run(main())
