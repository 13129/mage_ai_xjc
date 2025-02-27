from typing import Dict

from jupyter_client import KernelClient, KernelManager
from jupyter_client.kernelspec import NoSuchKernel

from mage_ai.data_preparation.models.project import Project
from mage_ai.data_preparation.models.project.constants import FeatureUUID
from mage_ai.server.kernels import DEFAULT_KERNEL_NAME, KernelName, kernel_managers
from mage_ai.server.logger import Logger

logger = Logger().new_server_logger(__name__)


class ActiveKernel:
    def __init__(self):
        self.kernel = kernel_managers[DEFAULT_KERNEL_NAME]
        self.kernel_client = self.kernel.client()


active_kernel = ActiveKernel()


def switch_active_kernel(
        kernel_name: KernelName,
) -> None:
    """
    Switches the active kernel to the specified kernel name, handling its startup and
    shutdown.

    This method logs various information and handles exceptions for different scenarios.

    Returns:
        None: This function does not return anything.

    Raises:
        NoSuchKernel: If the specified kernel is not available.
        Exception: If the specified kernel is PySpark and is not installed,
            it provides instructions for installation.

    Note:
        Ensure the necessary dependencies and configurations are set up for the desired kernels.
    """
    logger.info(f'Switch active kernel: {kernel_name}')
    if kernel_managers[kernel_name].is_alive():
        logger.info(f'Kernel {kernel_name} is already alive.')
        return

    for kernel in kernel_managers.values():
        if kernel.is_alive():
            logger.info(f'Shut down current kernel {kernel}.')
            kernel.request_shutdown()

    try:
        new_kernel = kernel_managers[kernel_name]
        new_kernel.start_kernel()
        active_kernel.kernel = new_kernel
        active_kernel.kernel_client = new_kernel.client()
        if kernel_name == KernelName.PYSPARK:

            should_set_active = True
            auto_creation = True
            cluster_id = None
            project = Project()

            if project.is_feature_enabled(FeatureUUID.COMPUTE_MANAGEMENT):
                ...

            if should_set_active:
                ...
    except NoSuchKernel as e:
        if kernel_name == KernelName.PYSPARK:
            raise Exception(
                'PySpark kernel is not installed. Please follow the instructions in '
                'https://docs.mage.ai/integrations/spark-pyspark '
                'to install it.'
            ) from e
        else:
            raise e


def get_active_kernel() -> KernelManager:
    return active_kernel.kernel


def get_active_kernel_name() -> str:
    return active_kernel.kernel.kernel_name


def get_active_kernel_client() -> KernelClient:
    return active_kernel.kernel_client


def interrupt_kernel() -> None:
    active_kernel.kernel.interrupt_kernel()


def restart_kernel() -> None:
    active_kernel.kernel.restart_kernel()
    active_kernel.kernel_client = active_kernel.kernel.client()


def start_kernel() -> None:
    active_kernel.kernel.start_kernel()
    active_kernel.kernel_client = active_kernel.kernel.client()
