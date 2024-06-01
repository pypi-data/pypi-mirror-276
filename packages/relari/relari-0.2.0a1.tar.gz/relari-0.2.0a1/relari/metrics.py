from enum import Enum


class Metric(str, Enum):
    SingleLabelClassification = "SingleLabelClassification"
    CodeStringMatch = "CodeStringMatch"
    PythonASTSimilarity = "PythonASTSimilarity"
    DeterministicFaithfulness = "DeterministicFaithfulness"
    DeterministicAnswerCorrectness = "DeterministicAnswerCorrectness"
    FleschKincaidReadability = "FleschKincaidReadability"
    PrecisionRecallF1 = "PrecisionRecallF1"
    RankedRetrievalMetrics = "RankedRetrievalMetrics"
    ToolSelectionAccuracy = "ToolSelectionAccuracy"
    LLMBasedFaithfulness = "LLMBasedFaithfulness"
    LLMBasedAnswerCorrectness = "LLMBasedAnswerCorrectness"
    LLMBasedAnswerRelevance = "LLMBasedAnswerRelevance"
    LLMBasedStyleConsistency = "LLMBasedStyleConsistency"
    LLMBasedContextPrecision = "LLMBasedContextPrecision"
    LLMBasedContextCoverage = "LLMBasedContextCoverage"
