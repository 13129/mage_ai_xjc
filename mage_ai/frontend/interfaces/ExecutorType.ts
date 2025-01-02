export enum ExecutorTypeEnum {
  K8S = 'k8s',
  LOCAL_PYTHON = 'local_python',
  PYSPARK = 'pyspark',
}

export const EXECUTOR_TYPES = [
  ExecutorTypeEnum.K8S,
  ExecutorTypeEnum.LOCAL_PYTHON,
  ExecutorTypeEnum.PYSPARK,
];
