from mage_ai.api.errors import ApiError
from mage_ai.api.resources.GenericResource import GenericResource
from mage_ai.kernels.default.models import KernelProcess
from mage_ai.kernels.default.utils import get_process_info

TERMINATE_INACTIVE = '__terminate_inactive__'


class KernelProcessResource(GenericResource):
    @classmethod
    async def collection(cls, query, meta, user, **kwargs):
        check_active_status = query.get('check_active_status', [False])
        if check_active_status:
            check_active_status = check_active_status[0]

        return cls.build_result_set(
            KernelProcess.load_all(check_active_status=check_active_status),
            user,
            **kwargs,
        )

    @classmethod
    def member(cls, pk, user, **kwargs):
        if TERMINATE_INACTIVE == pk:
            return cls(KernelProcess.load(pid=TERMINATE_INACTIVE), user, **kwargs)

        query = kwargs.get('query', {})
        check_active_status = query.get('check_active_status', [False])
        if check_active_status:
            check_active_status = check_active_status[0]

        info = get_process_info(pk, check_active_status=check_active_status)

        if not info:
            raise ApiError(ApiError.RESOURCE_NOT_FOUND)

        kernel_process = KernelProcess.load(**info)
        return cls(kernel_process, user, **kwargs)

    async def delete(self, **kwargs):
        if self.model.pid == TERMINATE_INACTIVE:
            KernelProcess.terminate_inactive()

        self.model.terminate()
