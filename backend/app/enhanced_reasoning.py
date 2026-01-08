from typing import List, Dict, Optional
from .core_ai import CoreAI
from dataclasses import dataclass
from enum import Enum

class ReasoningStep(Enum):
    OBSERVATION = "observation"
    HYPOTHESIS = "hypothesis"
    VALIDATION = "validation"
    CONCLUSION = "conclusion"
    REFLECTION = "reflection"

@dataclass
class ReasoningNode:
    step: ReasoningStep
    content: str
    confidence: float
    evidence: List[str]
    dependencies: List[int]

class EnhancedReasoningEngine:
    def __init__(self, core_ai: CoreAI):
        self.core_ai = core_ai
        self.reasoning_chain: List[ReasoningNode] = []

    async def multi_hop_analyze(
        self,
        message: str,
        context: str,
        intent: str,
        max_hops: int = 3
    ) -> Dict:
        self.reasoning_chain = []

        step_1 = await self._observe_facts(message, context, intent)
        self.reasoning_chain.append(step_1)

        step_2 = await self._generate_hypotheses(message, context, step_1)
        self.reasoning_chain.append(step_2)

        step_3 = await self._validate_hypotheses(step_2, context)
        self.reasoning_chain.append(step_3)

        step_4 = await self._draw_conclusion(step_3)
        self.reasoning_chain.append(step_4)

        step_5 = await self._self_reflect(step_4)
        self.reasoning_chain.append(step_5)

        return self._format_reasoning_output()

    async def _observe_facts(self, message: str, context: str, intent: str) -> ReasoningNode:
        if self.core_ai.is_mock:
            return ReasoningNode(
                step=ReasoningStep.OBSERVATION,
                content=f"Observed: Message intent is {intent}. Context available.",
                confidence=0.8,
                evidence=["user query", "system context"],
                dependencies=[]
            )

        prompt = f"""
        As a security analyst, observe and extract key facts from this scenario:

        User Query: {message}
        Intent: {intent}
        Context: {context}

        List all concrete facts, data points, and observations. Be specific.
        """

        response = await self.core_ai.generate_response(
            "You are a security facts extraction expert.",
            prompt
        )

        return ReasoningNode(
            step=ReasoningStep.OBSERVATION,
            content=response,
            confidence=0.9,
            evidence=["direct observation", "context analysis"],
            dependencies=[]
        )

    async def _generate_hypotheses(
        self,
        message: str,
        context: str,
        observations: ReasoningNode
    ) -> ReasoningNode:
        if self.core_ai.is_mock:
            return ReasoningNode(
                step=ReasoningStep.HYPOTHESIS,
                content="Hypothesis: Request is legitimate security assessment inquiry.",
                confidence=0.75,
                evidence=["observation analysis"],
                dependencies=[0]
            )

        prompt = f"""
        Based on these observations:
        {observations.content}

        Generate 2-3 security-focused hypotheses about:
        1. What the user is trying to accomplish
        2. What security risks or opportunities exist
        3. What the best course of action might be

        Format: List each hypothesis clearly.
        """

        response = await self.core_ai.generate_response(
            "You are a security hypothesis generator.",
            prompt
        )

        return ReasoningNode(
            step=ReasoningStep.HYPOTHESIS,
            content=response,
            confidence=0.75,
            evidence=["logical inference", "security expertise"],
            dependencies=[0]
        )

    async def _validate_hypotheses(
        self,
        hypotheses: ReasoningNode,
        context: str
    ) -> ReasoningNode:
        if self.core_ai.is_mock:
            return ReasoningNode(
                step=ReasoningStep.VALIDATION,
                content="Validation: Hypothesis confirmed through context cross-reference.",
                confidence=0.85,
                evidence=["context verification"],
                dependencies=[1]
            )

        prompt = f"""
        Validate these hypotheses against available context:

        Hypotheses:
        {hypotheses.content}

        Available Context:
        {context}

        For each hypothesis, state:
        - CONFIRMED: Strongly supported by evidence
        - PROBABLE: Likely but needs more data
        - REFUTED: Contradicted by evidence
        - UNCERTAIN: Insufficient data

        Provide reasoning for each.
        """

        response = await self.core_ai.generate_response(
            "You are a security hypothesis validator.",
            prompt
        )

        return ReasoningNode(
            step=ReasoningStep.VALIDATION,
            content=response,
            confidence=0.85,
            evidence=["evidence cross-check", "logical consistency"],
            dependencies=[1]
        )

    async def _draw_conclusion(self, validation: ReasoningNode) -> ReasoningNode:
        if self.core_ai.is_mock:
            return ReasoningNode(
                step=ReasoningStep.CONCLUSION,
                content="Conclusion: Proceed with standard security advisory response.",
                confidence=0.9,
                evidence=["validation results"],
                dependencies=[2]
            )

        prompt = f"""
        Based on the validation results:
        {validation.content}

        Draw a clear, actionable conclusion:
        1. What should be done?
        2. What is the recommended action?
        3. What are the risks if not addressed?
        4. What is the confidence level?

        Be specific and security-focused.
        """

        response = await self.core_ai.generate_response(
            "You are a security decision-making expert.",
            prompt
        )

        return ReasoningNode(
            step=ReasoningStep.CONCLUSION,
            content=response,
            confidence=0.9,
            evidence=["validated analysis", "expert judgment"],
            dependencies=[2]
        )

    async def _self_reflect(self, conclusion: ReasoningNode) -> ReasoningNode:
        if self.core_ai.is_mock:
            return ReasoningNode(
                step=ReasoningStep.REFLECTION,
                content="Reflection: Reasoning chain is sound. No contradictions detected.",
                confidence=0.95,
                evidence=["self-consistency check"],
                dependencies=[3]
            )

        prompt = f"""
        Review the following conclusion for potential errors or biases:
        {conclusion.content}

        Reflection checklist:
        1. Are there any logical inconsistencies?
        2. Did we consider alternative explanations?
        3. Are there hidden assumptions?
        4. What could we have missed?
        5. Is the confidence level justified?

        Be critical and honest.
        """

        response = await self.core_ai.generate_response(
            "You are a critical thinking validator.",
            prompt
        )

        return ReasoningNode(
            step=ReasoningStep.REFLECTION,
            content=response,
            confidence=0.95,
            evidence=["self-analysis", "bias detection"],
            dependencies=[3]
        )

    def _format_reasoning_output(self) -> Dict:
        formatted = {
            "reasoning_chain": [],
            "final_confidence": 0.0,
            "trace": ""
        }

        trace_parts = []
        for i, node in enumerate(self.reasoning_chain):
            formatted["reasoning_chain"].append({
                "step": node.step.value,
                "content": node.content,
                "confidence": node.confidence
            })

            trace_parts.append(
                f"[{node.step.value.upper()}] (Confidence: {node.confidence:.2f})\n{node.content}\n"
            )

        formatted["trace"] = "\n".join(trace_parts)
        formatted["final_confidence"] = self.reasoning_chain[-1].confidence if self.reasoning_chain else 0.0

        return formatted

    async def tree_of_thought_analyze(
        self,
        message: str,
        context: str,
        branches: int = 3
    ) -> Dict:
        if self.core_ai.is_mock:
            return {
                "best_branch": 0,
                "branches": [
                    {"reasoning": "Branch 1: Direct approach", "score": 0.85},
                    {"reasoning": "Branch 2: Alternative approach", "score": 0.75},
                    {"reasoning": "Branch 3: Conservative approach", "score": 0.80}
                ],
                "selected_reasoning": "Branch 1: Direct approach"
            }

        prompt = f"""
        Generate {branches} different reasoning paths for this security scenario:

        Query: {message}
        Context: {context}

        For each path, provide:
        1. A different analytical approach
        2. The reasoning steps
        3. The conclusion
        4. A confidence score (0-1)

        Format as JSON array.
        """

        try:
            result = await self.core_ai.generate_structured_response(
                "You are a multi-path security analyst.",
                prompt,
                schema={
                    "branches": [
                        {
                            "approach": "string",
                            "reasoning": "string",
                            "conclusion": "string",
                            "confidence": "float"
                        }
                    ]
                }
            )

            if "branches" in result:
                best_idx = max(
                    range(len(result["branches"])),
                    key=lambda i: result["branches"][i].get("confidence", 0)
                )

                return {
                    "best_branch": best_idx,
                    "branches": result["branches"],
                    "selected_reasoning": result["branches"][best_idx]["reasoning"]
                }

            return result
        except Exception as e:
            print(f"ERROR: Tree of thought analysis failed: {e}")
            return {"error": str(e)}
