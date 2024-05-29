from __future__ import annotations
import enum
import itertools


class _Logic:
    def resolve(self, interpretation: dict) -> bool:
        if isinstance(self, Term):
            if self.inverted:
                return not interpretation[self.name]

            return interpretation[self.name]

        elif isinstance(self, Sentence):
            lhs = self.lhs.resolve(interpretation)
            rhs = self.rhs.resolve(interpretation)

            if self.operator == Connective.CONJUNCTION:
                result = lhs and rhs

            elif self.operator == Connective.DISJUNCTION:
                result = lhs or rhs

            elif self.operator == Connective.IMPLIES:
                result = not lhs or rhs

            if self.inverted:
                return not result

            return result

        elif isinstance(self, QuantifiedSentence):
            if self.quantifier == Quantifier.FORALL:
                for value in [True, False]:
                    interpretation[self.term.name] = value
                    if not self.sentence.resolve(interpretation):
                        result = False
                        break

                else:
                    result = True

                if self.inverted:
                    return not result

                return result

            elif self.quantifier == Quantifier.EXISTS:
                for value in [True, False]:
                    interpretation[self.term.name] = value
                    if self.sentence.resolve(interpretation):
                        result = True
                        break

                else:
                    result = False

                if self.inverted:
                    return not result

                return result

    def get_unbound_terms(self) -> set:
        if isinstance(self, Term):
            return {self.name}

        elif isinstance(self, Sentence):
            return self.lhs.get_unbound_terms() | self.rhs.get_unbound_terms()

        elif isinstance(self, QuantifiedSentence):
            return self.sentence.get_unbound_terms() - {self.term.name}

    def is_valid(self) -> bool:
        unbound_terms = list(self.get_unbound_terms())
        interpretations = itertools.product([True, False], repeat=len(unbound_terms))
        for interpretation in interpretations:
            if not self.resolve(dict(zip(unbound_terms, interpretation))):
                return False

        return True

    def is_satisfiable(self) -> bool:
        unbound_terms = list(self.get_unbound_terms())
        interpretations = itertools.product([True, False], repeat=len(unbound_terms))
        for interpretation in interpretations:
            if self.resolve(dict(zip(unbound_terms, interpretation))):
                return True

        return False

    def __and__(self, other):
        if isinstance(self, (Term, Sentence, QuantifiedSentence)) and isinstance(
            other, (Term, Sentence, QuantifiedSentence)
        ):
            return Sentence(self, other, Connective.CONJUNCTION)

        return NotImplemented

    def __or__(self, other):
        if isinstance(self, (Term, Sentence, QuantifiedSentence)) and isinstance(
            other, (Term, Sentence, QuantifiedSentence)
        ):
            return Sentence(self, other, Connective.DISJUNCTION)

        return NotImplemented

    def __rshift__(self, other):
        if isinstance(self, (Term, Sentence, QuantifiedSentence)) and isinstance(
            other, (Term, Sentence, QuantifiedSentence)
        ):
            return Sentence(self, other, Connective.IMPLIES)

        return NotImplemented

    def __invert__(self):
        if isinstance(self, Term):
            return Term(self.name, inverted=not self.inverted)

        elif isinstance(self, (Sentence, QuantifiedSentence)):
            self.inverted = not self.inverted
            return self

        return NotImplemented

    def __matmul__(self, other):
        if isinstance(self, self.__class__) and isinstance(other, dict):
            return self.resolve(other)

        return NotImplemented


class Sentence(_Logic):
    def __init__(
        self,
        lhs: Term | Sentence | QuantifiedSentence,
        rhs: Term | Sentence | QuantifiedSentence,
        operator: Connective,
        inverted: bool = False,
    ) -> None:
        self.lhs = lhs
        self.rhs = rhs
        self.operator = operator
        self.inverted = inverted

    def __repr__(self):
        if self.inverted:
            return f"~({self.lhs} {self.operator.value} {self.rhs})"

        return f"({self.lhs} {self.operator.value} {self.rhs})"


class Term(_Logic):
    def __init__(self, name: str, inverted: bool = False) -> None:
        self.name = name
        self.inverted = inverted

    def __repr__(self):
        if self.inverted:
            return f"~{self.name}"

        return self.name


class Quantifier(enum.Enum):
    FORALL = "∀"
    EXISTS = "∃"


class Connective(enum.Enum):
    CONJUNCTION = "&"
    DISJUNCTION = "|"
    IMPLIES = ">>"


class QuantifiedSentence(_Logic):
    def __init__(
        self,
        quantifier: Quantifier,
        term: Term,
        sentence: Term | Sentence | QuantifiedSentence,
        inverted: bool = False,
    ) -> None:
        self.quantifier = quantifier
        self.term = term
        self.sentence = sentence
        self.inverted = inverted

    def __repr__(self):
        if self.inverted:
            return f"~({self.quantifier.value} {self.term}: {self.sentence})"

        return f"({self.quantifier.value} {self.term}: {self.sentence})"


def ForAll(term: Term, sentence: Term | Sentence | QuantifiedSentence):
    return QuantifiedSentence(Quantifier.FORALL, term, sentence)


def Exists(term: Term, sentence: Term | Sentence | QuantifiedSentence):
    return QuantifiedSentence(Quantifier.EXISTS, term, sentence)
