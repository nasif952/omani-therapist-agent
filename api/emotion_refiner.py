"""
Advanced Emotion Refinement System using GPT-4.1-nano
Two-stage pipeline for sophisticated emotional expression enhancement
"""

import openai
import re
import logging
from typing import Optional, Dict, Any, List, Tuple
from dataclasses import dataclass
from datetime import datetime
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class EmotionContext:
    """Context information for emotion refinement"""
    user_emotional_state: str  # Current detected user emotion
    conversation_history: List[Dict[str, str]]  # Recent conversation
    crisis_level: str  # none, mild, moderate, severe
    cultural_context: str  # omani, general_arabic, english
    therapeutic_stage: str  # rapport_building, exploration, intervention, closure

@dataclass
class RefinedResponse:
    """Result of emotion refinement process"""
    original_response: str
    refined_response: str
    emotion_enhancements: List[str]
    ssml_markup: str
    confidence_score: float

class EmotionRefiner:
    """
    Advanced emotion refinement using GPT-4.1-nano
    Transforms raw AI responses into naturally expressive, therapeutically appropriate speech
    """
    
    def __init__(self, openai_api_key: str):
        """
        Initialize the EmotionRefiner with OpenAI API
        
        Args:
            openai_api_key: OpenAI API key for GPT-4.1-nano access
        """
        self.client = openai.OpenAI(api_key=openai_api_key)
        self.model = "gpt-4.1-nano"  # Most cost-effective for emotion refinement 
        
        # Emotion refinement prompts
        self.system_prompts = self._create_specialized_prompts()
        
        # Natural expression patterns
        self.arabic_expressions = {
            'hesitation': ['أه...', 'يعني...', 'إم...', 'والله...'],
            'empathy': ['*تنهد خفيف*', 'أفهم شعورك...', 'هذا صعب...'],
            'encouragement': ['ما شاء الله', 'الله يقويك', 'أنت قوي'],
            'pause': ['...', '____', '*وقفة قصيرة*']
        }
        
        self.english_expressions = {
            'hesitation': ['um...', 'well...', 'you know...', 'I mean...'],
            'empathy': ['*soft sigh*', 'I hear you...', 'That sounds difficult...'],
            'encouragement': ['That\'s wonderful', 'You\'re doing great', 'I\'m proud of you'],
            'pause': ['...', '____', '*brief pause*']
        }
    
    def _create_specialized_prompts(self) -> Dict[str, str]:
        """Create specialized system prompts for different emotional refinement scenarios"""
        
        base_prompt = """You are an expert emotional expression enhancer for therapeutic AI conversations. Your role is to take a raw AI therapist response and refine it to include natural emotional expressions, hesitations, sighs, and pauses that make the speech sound genuinely human and therapeutically appropriate.

CRITICAL GUIDELINES:
1. Preserve the core therapeutic message completely
2. Add natural speech patterns (hesitations, pauses, sighs)
3. Maintain cultural sensitivity for Omani/Arabic context
4. Ensure emotional expressions match the conversation context
5. Generate SSML markup for advanced text-to-speech

INPUT FORMAT: You'll receive:
- Original AI response
- User emotional state
- Conversation context
- Crisis level
- Cultural setting

OUTPUT FORMAT: Return a JSON with:
- "refined_response": Enhanced response with natural expressions
- "emotion_enhancements": List of added emotional elements
- "ssml_markup": SSML version with prosody controls
- "confidence_score": Your confidence in the enhancement (0-1)
"""

        return {
            'therapeutic': base_prompt + """
THERAPEUTIC FOCUS:
- Add gentle hesitations before difficult topics
- Include empathetic sighs and pauses
- Use culturally appropriate emotional expressions
- Balance professionalism with human warmth
- Ensure crisis-appropriate emotional intensity

EXAMPLES OF NATURAL ENHANCEMENTS:
- "I understand this is difficult... *soft sigh* ...let's take this step by step"
- "أفهم شعورك... *تنهد خفيف* ...هذا طبيعي جداً"
- "Well... um... that's a really important realization"
""",

            'crisis': base_prompt + """
CRISIS INTERVENTION FOCUS:
- Prioritize calm, steady emotional tone
- Add reassuring pauses and gentle expressions
- Include grounding elements (breathing cues)
- Maintain professional composure with warmth
- Use immediate, supportive language

CRISIS-APPROPRIATE ENHANCEMENTS:
- "Let's take a deep breath together... *pause* ...you're safe right now"
- "I'm here with you... *gentle pause* ...we'll work through this"
- "تنفس معي... *وقفة مطمئنة* ...أنت في أمان الآن"
""",

            'celebration': base_prompt + """
POSITIVE MOMENT FOCUS:
- Add excited but controlled enthusiasm
- Include natural celebratory expressions
- Use culturally appropriate praise
- Maintain therapeutic boundaries while celebrating
- Add joyful vocal variety cues

CELEBRATORY ENHANCEMENTS:
- "Oh my... *excited pause* ...this is such wonderful progress!"
- "ما شاء الله! *وقفة فرحة* ...هذا إنجاز رائع!"
- "You did it... *proud sigh* ...I'm so happy for you"
"""
        }
    
    def refine_emotional_response(
        self, 
        original_response: str, 
        emotion_context: EmotionContext
    ) -> RefinedResponse:
        """
        Main refinement method: Transform raw response into emotionally rich expression
        
        Args:
            original_response: Raw AI therapist response
            emotion_context: Context for emotion refinement
            
        Returns:
            RefinedResponse with enhanced emotional expression
        """
        try:
            # Select appropriate system prompt
            prompt_type = self._select_prompt_type(emotion_context)
            system_prompt = self.system_prompts[prompt_type]
            
            # Prepare context for GPT-4.1-nano
            user_prompt = self._create_refinement_prompt(original_response, emotion_context)
            
            # Call GPT-4.1-nano for emotion refinement
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,  # Balanced creativity for natural expressions
                max_tokens=2000,
                response_format={"type": "json_object"}  # Ensure JSON response
            )
            
            # Parse response
            content = response.choices[0].message.content
            if content is None:
                raise ValueError("GPT-4.1-nano returned empty content")
            result = json.loads(content)
            
            # Create refined response object
            refined = RefinedResponse(
                original_response=original_response,
                refined_response=result.get('refined_response', original_response),
                emotion_enhancements=result.get('emotion_enhancements', []),
                ssml_markup=result.get('ssml_markup', ''),
                confidence_score=result.get('confidence_score', 0.8)
            )
            
            logger.info(f"Successfully refined response with {len(refined.emotion_enhancements)} enhancements")
            return refined
            
        except Exception as e:
            logger.error(f"Emotion refinement failed: {e}")
            # Return original response as fallback
            return RefinedResponse(
                original_response=original_response,
                refined_response=original_response,
                emotion_enhancements=[],
                ssml_markup=self._create_basic_ssml(original_response),
                confidence_score=0.0
            )
    
    def _select_prompt_type(self, context: EmotionContext) -> str:
        """Select appropriate refinement prompt based on context"""
        if context.crisis_level in ['moderate', 'severe']:
            return 'crisis'
        elif context.user_emotional_state in ['excited', 'happy', 'encouraging']:
            return 'celebration'
        else:
            return 'therapeutic'
    
    def _create_refinement_prompt(self, original_response: str, context: EmotionContext) -> str:
        """Create detailed prompt for GPT-4.1-nano refinement"""
        
        # Recent conversation context (last 3 exchanges)
        recent_history = context.conversation_history[-6:] if len(context.conversation_history) > 6 else context.conversation_history
        
        prompt = f"""
REFINEMENT REQUEST:

ORIGINAL AI RESPONSE:
"{original_response}"

CONTEXT INFORMATION:
- User Emotional State: {context.user_emotional_state}
- Crisis Level: {context.crisis_level}
- Cultural Context: {context.cultural_context}
- Therapeutic Stage: {context.therapeutic_stage}

RECENT CONVERSATION:
{self._format_conversation_history(recent_history)}

TASK:
Please refine the original response to include natural emotional expressions, hesitations, pauses, and sighs that make it sound genuinely human while maintaining therapeutic appropriateness. 

Focus on:
1. Adding natural speech patterns for the cultural context
2. Including appropriate emotional expressions
3. Maintaining the core therapeutic message
4. Creating SSML markup for advanced TTS

Return your response as JSON with the specified format.
"""
        return prompt
    
    def _format_conversation_history(self, history: List[Dict[str, str]]) -> str:
        """Format conversation history for context"""
        if not history:
            return "No previous conversation"
        
        formatted = []
        for i, exchange in enumerate(history[-6:]):  # Last 6 messages
            role = "User" if exchange.get('role') == 'user' else "AI"
            content = exchange.get('content', '')[:100] + "..." if len(exchange.get('content', '')) > 100 else exchange.get('content', '')
            formatted.append(f"{role}: {content}")
        
        return "\n".join(formatted)
    
    def _create_basic_ssml(self, text: str) -> str:
        """Create basic SSML markup as fallback"""
        # Clean text and add basic SSML structure
        clean_text = re.sub(r'[*<>]', '', text)
        return f'<speak><prosody rate="medium" pitch="medium">{clean_text}</prosody></speak>'
    
    def batch_refine_responses(
        self, 
        responses: List[Tuple[str, EmotionContext]]
    ) -> List[RefinedResponse]:
        """
        Batch refinement for multiple responses
        Useful for testing and optimization
        """
        results = []
        for original_response, context in responses:
            refined = self.refine_emotional_response(original_response, context)
            results.append(refined)
        
        return results
    
    def get_refinement_stats(self, refined_responses: List[RefinedResponse]) -> Dict[str, Any]:
        """
        Generate statistics about refinement performance
        """
        if not refined_responses:
            return {}
        
        total_enhancements = sum(len(r.emotion_enhancements) for r in refined_responses)
        avg_confidence = sum(r.confidence_score for r in refined_responses) / len(refined_responses)
        
        enhancement_types = {}
        for response in refined_responses:
            for enhancement in response.emotion_enhancements:
                enhancement_types[enhancement] = enhancement_types.get(enhancement, 0) + 1
        
        return {
            'total_responses': len(refined_responses),
            'total_enhancements': total_enhancements,
            'avg_enhancements_per_response': total_enhancements / len(refined_responses),
            'avg_confidence_score': avg_confidence,
            'enhancement_types': enhancement_types,
            'success_rate': len([r for r in refined_responses if r.confidence_score > 0.5]) / len(refined_responses)
        }

# Example usage and testing
if __name__ == "__main__":
    # This would be used for testing the emotion refiner
    pass 