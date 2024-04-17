from typing import Callable, List, TypeAlias


Evaluator: TypeAlias = Callable[[List[str]], bool]


class Eval:
    @staticmethod
    def all(logs: List[str], evaluators: list[Callable]) -> bool:
        return all(evaluator(logs) for evaluator in evaluators)

    @staticmethod
    def len_match(num: int) -> Evaluator:
        return lambda logs: len(logs) == num

    @staticmethod
    def contains_exact_match(match: str) -> Evaluator:
        return lambda logs: any(match == line for line in logs)

    @staticmethod
    def contains_partial_match(match: str) -> Evaluator:
        return lambda logs: any(match in line for line in logs)
