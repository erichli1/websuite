from typing import Callable, TypeAlias


class Log:
    def __init__(self, log: str):
        log_parts: list[str] = [part.strip() for part in log.split("//")]

        self.component = log_parts[0]
        self.label = log_parts[1]
        self.newValue = log_parts[2] if len(log_parts) > 2 else None
        self.oldValue = log_parts[3] if len(log_parts) > 3 else None

    def __str__(self):
        return (
            f"{self.component} // {self.label}"
            + (f" // {self.newValue}" if self.newValue else "")
            + (f" // {self.oldValue}" if self.oldValue else "")
        )


LogListEvaluator: TypeAlias = Callable[[list[Log]], bool]
LogEvaluator: TypeAlias = Callable[[Log], bool]


class Eval:
    @staticmethod
    def check_one(log: Log, evaluators: list[LogEvaluator]) -> bool:
        return all(evaluator(log) for evaluator in evaluators)

    @staticmethod
    def no_logs(logs: list[Log]) -> bool:
        return len(logs) == 0

    @staticmethod
    def ordered(logs: list[Log], evaluators: list[LogEvaluator]) -> bool:
        return len(logs) == len(evaluators) and all(
            evaluator(logs[i]) for i, evaluator in enumerate(evaluators)
        )

    @staticmethod
    def unordered(logs: list[Log], evaluators: list[LogEvaluator]) -> bool:
        return len(logs) == len(evaluators) and all(
            any(evaluator(log) for evaluator in evaluators) for log in logs
        )

    @staticmethod
    def at_least_one(logs: list[Log], evaluators: list[LogEvaluator]) -> bool:
        return any(any(evaluator(log) for evaluator in evaluators) for log in logs)

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
    def contains_match(
        component: str | None = None,
        label: str | None = None,
        newValue: str | None = None,
        oldValue: str | None = None,
    ) -> LogEvaluator:
        return (
            lambda log: (component is None or component in log.component)
            and (label is None or label in log.label)
            and (newValue is None or newValue in log.newValue)
            and (oldValue is None or oldValue in log.oldValue)
        )

    @staticmethod
    def compare_values(compare: Callable[[str, str], bool]) -> LogEvaluator:
        return lambda log: compare(log.newValue, log.oldValue)
