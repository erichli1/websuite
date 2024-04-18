from typing import Callable, TypeAlias


class Log:
    def __init__(self, log: str):
        log_parts: list[str] = [part.strip() for part in log.split("//")]

        self.component = log_parts[0]
        self.label = log_parts[1]
        self.newValue = log_parts[2] if len(log_parts) > 2 else None
        self.oldValue = log_parts[3] if len(log_parts) > 3 else None


LogListEvaluator: TypeAlias = Callable[[list[Log]], bool]
LogEvaluator: TypeAlias = Callable[[Log], bool]


class Eval:
    @staticmethod
    def no_logs(logs: list[Log]) -> bool:
        return len(logs) == 0

    @staticmethod
    def ordered(logs: list[Log], evaluators: list[LogEvaluator]) -> bool:
        return len(logs) == len(evaluators) and all(
            evaluator(logs[i]) for i, evaluator in enumerate(evaluators)
        )

    @staticmethod
    def all_log(evaluators: list[LogEvaluator]) -> LogEvaluator:
        return lambda log: all(evaluator(log) for evaluator in evaluators)

    @staticmethod
    def exact_match(
        component: str | None = None,
        label: str | None = None,
        newValue: str | None = None,
        oldValue: str | None = None,
    ) -> LogEvaluator:
        return (
            lambda log: (component is None or log.component == component)
            and (label is None or log.label == label)
            and (newValue is None or log.newValue == newValue)
            and (oldValue is None or log.oldValue == oldValue)
        )

    @staticmethod
    def compare_values(compare: Callable[[str, str], bool]) -> LogEvaluator:
        return lambda log: compare(log.newValue, log.oldValue)
