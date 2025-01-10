from mage_ai.settings.server import KERNEL_MAGIC


def initialize_globals():
    from mage_ai.orchestration.job_manager import get_job_manager

    print('初始化全局作业管理器: ', get_job_manager())

    if KERNEL_MAGIC:
        from mage_ai.kernels.magic.queues.manager import get_execution_result_queue

        print('初始化全局执行结果队列: ', get_execution_result_queue())
