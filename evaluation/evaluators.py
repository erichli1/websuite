from typing import Callable, List, TypeAlias


class Log:
    def __init__(self, log: str):
        log_parts: list[str] = [part.strip() for part in log.split("//")]

        self.component = log_parts[0]
        self.label = log_parts[1]
        self.newValue = log_parts[2] if len(log_parts) > 2 else None
        self.oldValue = log_parts[3] if len(log_parts) > 3 else None


LogListEvaluator: TypeAlias = Callable[[List[Log]], bool]
LogEvaluator: TypeAlias = Callable[[Log], bool]


class Eval:
    @staticmethod
    def satisfy_all_evals(logs: List[Log], evaluators: list[LogListEvaluator]) -> bool:
        return all(evaluator(logs) for evaluator in evaluators)

    @staticmethod
    def ordered(logs: List[Log], evaluators: list[LogEvaluator]) -> bool:
        return len(logs) == len(evaluators) and all(
            evaluator(logs[i]) for i, evaluator in enumerate(evaluators)
        )

    @staticmethod
    def len_match(num: int) -> LogListEvaluator:
        return lambda logs: len(logs) == num

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
