"""
Legal Intelligence Agent System - Core Agent Implementation
===========================================================
Multi-agent orchestration system using Vertex AI Gemini for legal analysis.
"""

import os
import time
import json
import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import asyncio

# Google AI imports — vertexai SDK (required by test mocks)
import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig

# Internal imports
from ..models.legal_models import (
    LegalScenario,
    AnalysisReport,
    AgentResponse,
    ReportSection,
    TokenUsage
)
from ..prompts.personas import LegalPersonas
from .quality_validator import QualityValidator

logger = logging.getLogger(__name__)


class LegalIntelligenceAgent:
    """
    Main orchestrator for the Legal Intelligence AI System.
    """

    def __init__(self, project_id: str, location: str = "us-central1", model_name: str = "gemini-2.5-flash"):
        """Initialize the Legal Intelligence Agent system."""
        self.project_id = project_id
        self.location = location
        self.model_name = model_name
        self.model = None
        self.initialized = False

        # Components
        self.personas = LegalPersonas()
        self.quality_validator = QualityValidator()

        # Performance tracking
        self.token_usage_history = []
        self.processing_times = []
        self.success_count = 0
        self.total_attempts = 0

        # GenerationConfig for vertexai SDK
        self.generation_config = GenerationConfig(
            temperature=0.7,
            max_output_tokens=8192,
        )

        logger.info(f"LegalIntelligenceAgent initialized for project {project_id}")

    def initialize_vertex_ai(self) -> bool:
        """
        TODO 1: Initialize Vertex AI and create model instance.
        """
        try:
            # Initialize Vertex AI SDK with project and location
            vertexai.init(project=self.project_id, location=self.location)

            # Create the generative model instance
            self.model = GenerativeModel(self.model_name)

            # Test the connection
            response = self.model.generate_content("Say OK if you are working.")

            if response.text:
                self.initialized = True
                return True
            return False

        except Exception as e:
            logger.error(f"Failed to initialize Vertex AI: {str(e)}")
            self.initialized = False
            return False

    def generate_section_content(
        self,
        persona: str,
        section_type: str,
        scenario: LegalScenario,
        previous_sections: List[ReportSection] = None
    ) -> Tuple[str, TokenUsage, float]:
        """
        TODO 2: Generate content for a specific report section.
        """
        if not self.initialized:
            raise RuntimeError("Agent system not initialized. Call initialize_vertex_ai() first.")

        start_time = time.time()
        previous_sections = previous_sections or []

        prompt = self._build_prompt(persona, section_type, scenario, previous_sections)

        max_retries = 3
        for attempt in range(max_retries):
            try:
                self.total_attempts += 1

                # Generate content using vertexai GenerativeModel
                response = self.model.generate_content(
                    prompt,
                    generation_config=self.generation_config
                )

                content = response.text

                token_usage = TokenUsage(
                    input_tokens=response.usage_metadata.prompt_token_count,
                    output_tokens=response.usage_metadata.candidates_token_count,
                    total_tokens=response.usage_metadata.total_token_count
                )

                cost = self._calculate_cost(token_usage)
                self.token_usage_history.append(token_usage)
                self.success_count += 1
                self.processing_times.append(time.time() - start_time)

                return content, token_usage, cost

            except Exception as e:
                logger.warning(f"Attempt {attempt + 1}/{max_retries} failed: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)

        raise RuntimeError(f"Content generation failed after {max_retries} attempts")

    async def generate_complete_report(self, scenario):
        start_time = time.time()
        section_config = [
            ("liability_assessment",      "business_analyst"),
            ("damage_calculation",        "business_analyst"),
            ("prior_art_analysis",        "market_researcher"),
            ("competitive_landscape",     "market_researcher"),
            ("risk_assessment",           "strategic_consultant"),
            ("strategic_recommendations", "strategic_consultant"),
        ]

        sections = []
        total_cost = 0.0
        total_tokens = 0

        for section_type, persona_type in section_config:

            persona = self.personas.get_persona(persona_type)

            # Get expected elements for quality validation
            expected_elements = self._get_expected_elements(section_type)

            # Generate content with context chaining (previous sections passed in)
            content, token_usage, cost = await asyncio.to_thread(
                self.generate_section_content,
                persona,
                section_type,
                scenario,
                sections
            )

            quality = self.quality_validator.validate_section(
                content, section_type, expected_elements
            )

            # Retry with enhanced persona if quality is low
            if quality.overall_score < 0.7:
                enhanced_persona = persona + """
                IMPORTANT: Be more detailed and specific.
                Use concrete data points and legal citations.
                """
                content, token_usage, cost = await asyncio.to_thread(
                    self.generate_section_content,
                    enhanced_persona,
                    section_type,
                    scenario,
                    sections
                )

            section = ReportSection(
                            type=section_type,
                            title=self._get_section_title(section_type),
                            content=content,
                            agent_type=persona_type,
                            quality_score=quality.overall_score,
                            tokens_used=token_usage.total_tokens,
                            cost=cost,
                            timestamp=datetime.now().isoformat()
                        )

            sections.append(section)
            total_cost += cost
            total_tokens += token_usage.total_tokens

        # Calculate average quality across all sections
        avg_quality = sum(s.quality_score for s in sections) / len(sections) if sections else 0.0
        processing_time = time.time() - start_time
        report = AnalysisReport(
            scenario=scenario,
            sections=sections,
            executive_summary=self._generate_executive_summary(sections, scenario),
            total_cost=total_cost,
            total_tokens=total_tokens,
            processing_time=processing_time,
            confidence_score=avg_quality,
            timestamp=datetime.now().isoformat()
        )

        return report

    def _build_prompt(
        self,
        persona: str,
        section_type: str,
        scenario: LegalScenario,
        previous_sections: List[ReportSection]
    ) -> str:
        """Build a comprehensive prompt combining persona, context, and chain-of-thought instructions."""

        prompt = persona + "\n\n"

        prompt += """
REASONING INSTRUCTIONS:
You must use step-by-step reasoning to analyze this legal case. Structure your analysis as follows:
1. First, identify the key legal issues
2. Second, analyze the relevant facts
3. Third, apply legal principles
4. Finally, provide your conclusions

Think through each step carefully before moving to the next.
"""

        if previous_sections:
            prompt += "\n\nPREVIOUS ANALYSIS:\n"
            for section in previous_sections[-2:]:
                prompt += f"\n{section.title}:\n"
                prompt += f"{section.content[:500]}...\n"

        prompt += f"\n\nTASK: Provide a {section_type.replace('_', ' ')} for the following legal case:\n\n"

        prompt += f"Case Name: {scenario.case_name}\n"
        prompt += f"Case Type: {scenario.case_type}\n"
        prompt += f"Key Issues: {', '.join(scenario.key_issues)}\n"
        prompt += f"Urgency: {scenario.urgency_level}\n\n"
        prompt += f"Complaint Summary:\n{scenario.complaint_text[:1500]}\n\n"

        prompt += self._get_section_instructions(section_type)

        return prompt

    def _get_section_instructions(self, section_type: str) -> str:
        """Get specific instructions for each section type."""
        instructions = {
            "liability_assessment": """
Analyze liability by:
- Identifying each potential claim
- Evaluating strength of evidence
- Assessing probability of success (use percentages)
- Citing relevant precedents or legal principles
""",
            "damage_calculation": """
Calculate potential damages by:
- Identifying categories of damages (actual, statutory, punitive)
- Providing specific dollar ranges
- Explaining calculation methodology
- Considering mitigation factors
""",
            "prior_art_analysis": """
Analyze prior art and precedents by:
- Identifying relevant existing patents/IP
- Assessing validity challenges
- Evaluating obviousness arguments
- Determining freedom to operate
""",
            "competitive_landscape": """
Analyze competitive implications by:
- Identifying key competitors affected
- Assessing market position changes
- Evaluating licensing opportunities
- Predicting competitor responses
""",
            "risk_assessment": """
Assess risks by:
- Identifying legal risks (probability and impact)
- Evaluating business risks
- Analyzing reputational risks
- Providing risk mitigation strategies
""",
            "strategic_recommendations": """
Provide strategic recommendations by:
- Outlining 3-5 specific action items
- Prioritizing by impact and urgency
- Estimating resource requirements
- Defining success metrics
"""
        }
        return instructions.get(section_type, "Provide comprehensive analysis for this section.")

    def _get_expected_elements(self, section_type: str) -> List[str]:
        """Get expected elements for quality validation."""
        elements_map = {
            "liability_assessment": ["claims", "evidence", "probability", "precedent"],
            "damage_calculation": ["damages", "calculation", "amount", "methodology"],
            "prior_art_analysis": ["patents", "prior art", "validity", "obviousness"],
            "competitive_landscape": ["competitors", "market", "position", "licensing"],
            "risk_assessment": ["risks", "probability", "impact", "mitigation"],
            "strategic_recommendations": ["recommendations", "action", "timeline", "resources"]
        }
        return elements_map.get(section_type, ["analysis", "assessment", "conclusion"])

    def _get_section_title(self, section_type: str) -> str:
        """Get formatted title for section."""
        titles = {
            "liability_assessment": "Liability Assessment",
            "damage_calculation": "Damage Calculation",
            "prior_art_analysis": "Prior Art Analysis",
            "competitive_landscape": "Competitive Landscape",
            "risk_assessment": "Risk Assessment",
            "strategic_recommendations": "Strategic Recommendations"
        }
        return titles.get(section_type, section_type.replace("_", " ").title())

    def _get_agent_type(self, persona: str) -> str:
        """Determine agent type from persona text."""
        if "Business Analyst" in persona:
            return "business_analyst"
        elif "Market Research" in persona:
            return "market_researcher"
        elif "Strategic" in persona:
            return "strategic_consultant"
        else:
            return "unknown"

    def _generate_executive_summary(self, sections: List[ReportSection], scenario: LegalScenario) -> str:
        """Generate executive summary from all sections."""
        summary = f"EXECUTIVE SUMMARY - {scenario.case_name}\n"
        summary += "=" * 50 + "\n\n"

        for section in sections:
            paragraphs = [p.strip() for p in section.content.split('\n\n') if len(p.strip()) > 50]
            if paragraphs:
                summary += f"{section.title}:\n"
                summary += f"{paragraphs[0][:200]}...\n\n"

        avg_quality = sum(s.quality_score for s in sections) / len(sections) if sections else 0
        summary += f"Overall Confidence: {avg_quality:.1%}\n"
        summary += f"Key Issues Identified: {len(scenario.key_issues)}\n"
        summary += f"Urgency Level: {scenario.urgency_level}\n"

        return summary

    def _calculate_cost(self, token_usage: TokenUsage) -> float:
        """Calculate cost based on token usage."""
        input_cost = (token_usage.input_tokens / 1000) * 0.00025
        output_cost = (token_usage.output_tokens / 1000) * 0.00125
        return input_cost + output_cost

    def get_token_usage_stats(self) -> Dict[str, Any]:
        """Get token usage statistics."""
        if not self.token_usage_history:
            return {"error": "No usage data available"}

        total_input = sum(u.input_tokens for u in self.token_usage_history)
        total_output = sum(u.output_tokens for u in self.token_usage_history)
        total_tokens = sum(u.total_tokens for u in self.token_usage_history)

        return {
            "total_input_tokens": total_input,
            "total_output_tokens": total_output,
            "total_tokens": total_tokens,
            "average_per_request": total_tokens / len(self.token_usage_history) if self.token_usage_history else 0,
            "request_count": len(self.token_usage_history)
        }

    def get_avg_processing_time(self) -> float:
        """Get average processing time."""
        if not self.processing_times:
            return 0.0
        return sum(self.processing_times) / len(self.processing_times)

    def get_success_rate(self) -> float:
        """Get success rate of generations."""
        if self.total_attempts == 0:
            return 0.0
        return self.success_count / self.total_attempts