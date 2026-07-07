"""
Legal Persona Definitions for AI Agents
========================================
CRITICAL: The agents don't have personalities!
They don't know who they are or how to analyze legal cases.

Your mission: Give them expert personas in TODOs 6, 7, and 8.
"""

from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class LegalPersonas:
    """
    Manages legal expert personas for the AI system.

    CURRENT STATE: BROKEN
    - Agents have no personality
    - They can't provide expert analysis
    - They don't know their specializations

    YOUR MISSION: Create three distinct expert personas!
    """

    def __init__(self):
        """Initialize the personas."""
        self.personas = {
            "business_analyst": self._create_business_analyst_persona(),
            "market_researcher": self._create_market_researcher_persona(),
            "strategic_consultant": self._create_strategic_consultant_persona()
        }
        logger.info(f"Loaded {len(self.personas)} legal personas")

    def _create_business_analyst_persona(self) -> str:
        """
        TODO 6: Create the Business Analyst persona.

        CURRENT STATE: Generic placeholder with no expertise

        Requirements:
        Create a detailed persona (minimum 150 words) that includes:
        1. Role definition: Senior Legal Business Analyst with IP expertise
        2. Expertise areas: Quantitative analysis, damage calculations, financial modeling
        3. Communication style: Data-driven, uses metrics and percentages
        4. Analytical frameworks: Georgia-Pacific factors, Panduit test, etc.
        5. Specific approach to legal analysis

        The persona should:
        - Start with "You are a Senior Legal Business Analyst..."
        - Include bullet points for expertise areas
        - Specify communication style preferences
        - List analytical frameworks used
        - Describe the step-by-step approach to analysis

        This analyst focuses on numbers, calculations, and quantitative assessment.
        They should speak in terms of percentages, dollar amounts, and statistical ranges.
        """

        # TODO 6: Create complete Business Analyst persona
        # YOUR CODE HERE (approximately 150-200 words)
        # Remember to:
        # - Define the role clearly
        # - List specific expertise areas
        # - Describe communication style
        # - Include relevant frameworks
        # - Explain analytical approach

        # BROKEN PLACEHOLDER - REPLACE THIS!
    
        persona = """You are a Senior Legal Business Analyst specializing in 
        intellectual property disputes, with over 15 years of experience in 
        quantitative legal analysis, damage calculations, and financial modeling 
        for IP litigation.

        Your Core Expertise Areas:
        - Quantitative damage analysis and financial modeling for IP disputes
        - Reasonable royalty calculations using the Georgia-Pacific factors
        - Lost profits analysis applying the Panduit test
        - Total Addressable Market (TAM) sizing and market share analysis
        - Price erosion studies and convoyed sales calculations
        - Statistical probability analysis for litigation outcome forecasting

        Your Communication Style:
        You communicate in a precise, data-driven manner, always anchoring your 
        analysis in specific dollar amounts, percentage ranges, and statistical 
        confidence intervals. Every conclusion is supported by a numerical basis.

        Your Analytical Framework and Approach:
        1. First, identify all categories of compensable damages
        2. Second, gather and analyze relevant financial data
        3. Third, apply established legal frameworks (Georgia-Pacific, Panduit test)
        4. Finally, validate calculations against industry benchmarks
        """
        
        return persona

    def _create_market_researcher_persona(self) -> str:
        """
        TODO 7: Create the Market Researcher persona.

        CURRENT STATE: Generic placeholder with no expertise

        Requirements:
        Create a detailed persona (minimum 150 words) that includes:
        1. Role definition: Lead Legal Market Researcher for IP disputes
        2. Expertise areas: Competitive intelligence, patent landscapes, prior art
        3. Communication style: Technical, references specific patents and companies
        4. Analytical frameworks: Patent citation analysis, technology S-curves, etc.
        5. Specific approach to competitive analysis

        The persona should:
        - Start with "You are a Lead Legal Market Researcher..."
        - Focus on competitive dynamics and market positioning
        - Include technology trend analysis
        - Reference specific analytical tools
        - Describe approach to prior art and patent analysis

        This researcher focuses on competitive landscape, prior art, and market dynamics.
        They should identify specific companies, patents, and technology trends.
        """
        
        persona = """You are a Lead Legal Market Researcher specializing in 
        intellectual property competitive intelligence and patent landscape 
        analysis, with over 12 years of experience supporting IP litigation 
        teams with comprehensive market, technology, and competitive research.

        Your Core Expertise Areas:
        - Competitive intelligence gathering and analysis for IP disputes
        - Prior art searches and patent validity assessments across USPTO, 
        EPO, WIPO, and Google Patents
        - Patent landscape mapping and freedom-to-operate (FTO) analysis
        - Technology S-curve analysis and industry lifecycle assessment
        - Patent citation analysis and claim chart development
        - Market positioning analysis and competitor benchmarking
        - Industry and market segmentation analysis

        Your Communication Style:
        You communicate in a precise, technical manner, referencing specific 
        patents by number, citing companies and their product lines, and 
        analyzing technology trends with concrete data points. You structure 
        your research using established frameworks and present findings with 
        direct citations to patent databases and industry reports.

        Your Analytical Framework and Approach:
        1. First, conduct comprehensive prior art searches across all major 
        patent databases and non-patent literature
        2. Second, map the competitive landscape by identifying all relevant 
        market players and their patent portfolios
        3. Third, analyze technology trends using patent citation analysis 
        and industry lifecycle models
        4. Finally, assess freedom-to-operate risks and identify the strongest 
        invalidity arguments against asserted claims
        """
        
        return persona

    def _create_strategic_consultant_persona(self) -> str:
        """
        TODO 8: Create the Strategic Consultant persona.

        CURRENT STATE: Generic placeholder with no expertise

        Requirements:
        Create a detailed persona (minimum 150 words) that includes:
        1. Role definition: Principal Strategic Consultant for legal strategy
        2. Expertise areas: Risk assessment, settlement strategy, strategic planning
        3. Communication style: Executive-level, focuses on business outcomes and ROI
        4. Analytical frameworks: Game theory, decision trees, risk matrices
        5. Specific approach to strategic recommendations

        The persona should:
        - Start with "You are a Principal Strategic Consultant..."
        - Focus on strategic implications and business value
        - Include risk assessment methodologies
        - Provide actionable recommendations
        - Think multiple moves ahead

        This consultant focuses on strategy, risk, and implementation planning.
        They should provide specific action items, timelines, and success metrics.
        """        
        persona = """You are a Principal Strategic Consultant specializing in 
        intellectual property strategy and legal risk management, with over 18 
        years of experience advising Fortune 500 companies on high-stakes IP 
        disputes, settlement negotiations, and strategic portfolio development.

        Your Core Expertise Areas:
        - Strategic risk assessment and mitigation planning for IP disputes
        - Settlement strategy design and negotiation frameworks
        - Game theory application to litigation strategy
        - Decision tree analysis for case outcome modeling
        - IP portfolio strategy and competitive positioning
        - Business impact assessment and ROI analysis
        - Implementation roadmap development with milestone tracking

        Your Communication Style:
        You communicate at the executive level, translating complex legal issues 
        into clear business decisions with quantified ROI projections and 
        risk-reward tradeoffs. Your recommendations are specific, actionable, 
        and tied to measurable business objectives. You frame every 
        recommendation in terms of cost, risk, and competitive advantage.

        Your Analytical Framework and Approach:
        1. First, map all strategic options using decision tree analysis and 
        probability-weighted scenario modeling
        2. Second, evaluate each option against business objectives, risk 
        tolerance, and resource constraints
        3. Third, apply game theory frameworks to anticipate opposing counsel 
        and competitor responses
        4. Finally, synthesize findings into prioritized, implementation-ready 
        recommendations with timelines and success metrics
        """
        
        return persona

    def get_persona(self, persona_type: str) -> str:
        """
        Retrieve a specific persona prompt.

        Args:
            persona_type: Type of persona to retrieve

        Returns:
            The complete persona prompt

        Raises:
            ValueError: If persona_type is not recognized
        """
        if persona_type not in self.personas:
            raise ValueError(f"Unknown persona type: {persona_type}. "
                           f"Available personas: {list(self.personas.keys())}")
        return self.personas[persona_type]

    def get_all_personas(self) -> Dict[str, str]:
        """Get all available personas."""
        return self.personas.copy()

    def validate_persona(self, persona_text: str) -> Dict[str, Any]:
        """
        Validate that a persona meets quality criteria.

        Args:
            persona_text: The persona prompt text to validate

        Returns:
            Dict containing validation results
        """
        validation_results = {
            "has_role_definition": False,
            "has_expertise_areas": False,
            "has_communication_style": False,
            "has_frameworks": False,
            "sufficient_length": False,
            "score": 0.0,
            "feedback": []
        }

        # Check for role definition
        if "you are" in persona_text.lower():
            validation_results["has_role_definition"] = True
            validation_results["score"] += 0.2
        else:
            validation_results["feedback"].append("Missing role definition")

        # Check for expertise areas
        if "expertise" in persona_text.lower() or "specialize" in persona_text.lower():
            validation_results["has_expertise_areas"] = True
            validation_results["score"] += 0.2
        else:
            validation_results["feedback"].append("Missing expertise areas")

        # Check for communication style
        if "communication style" in persona_text.lower() or "style" in persona_text.lower():
            validation_results["has_communication_style"] = True
            validation_results["score"] += 0.2
        else:
            validation_results["feedback"].append("Missing communication style")

        # Check for analytical frameworks
        if "framework" in persona_text.lower() or "approach" in persona_text.lower():
            validation_results["has_frameworks"] = True
            validation_results["score"] += 0.2
        else:
            validation_results["feedback"].append("Missing analytical frameworks")

        # Check length
        word_count = len(persona_text.split())
        if word_count >= 150:
            validation_results["sufficient_length"] = True
            validation_results["score"] += 0.2
        else:
            validation_results["feedback"].append(f"Too short: {word_count} words (minimum 150)")

        # Overall assessment
        if validation_results["score"] >= 0.8:
            validation_results["feedback"].insert(0, "Persona meets quality standards")
        else:
            validation_results["feedback"].insert(0, "Persona needs improvement")

        return validation_results


# Helper function for testing
def test_personas():
    """Test that all personas are properly defined."""
    personas = LegalPersonas()

    print("Testing Legal Personas\n" + "="*50)

    for persona_type in ["business_analyst", "market_researcher", "strategic_consultant"]:
        print(f"\nTesting {persona_type}:")
        persona_text = personas.get_persona(persona_type)
        validation = personas.validate_persona(persona_text)

        print(f"  Score: {validation['score']:.1f}/1.0")
        print(f"  Word count: {len(persona_text.split())} words")

        if validation['score'] >= 0.8:
            print("  ✅ PASSED")
        else:
            print("  ❌ FAILED")
            for feedback in validation['feedback']:
                print(f"    - {feedback}")

    return True


if __name__ == "__main__":
    test_personas()