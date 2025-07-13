#!/usr/bin/env python3
"""
Voice Activity Detection (VAD) System
=====================================

This system provides intelligent turn detection for natural conversations:
- Accumulates speech segments over time
- Uses configurable silence timeout to determine conversation turns
- Handles natural pauses without premature processing
- Provides real-time feedback on speech activity

Author: AI Assistant
Created: 2024
"""

import asyncio
import time
import logging
from typing import Optional, List, Callable, Dict, Any, Union, Awaitable
from dataclasses import dataclass, field
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

@dataclass
class SpeechSegment:
    """Represents a single speech segment with timing information"""
    text: str
    start_time: float
    end_time: float
    confidence: float = 1.0
    is_final: bool = False

@dataclass
class VADConfig:
    """Configuration for Voice Activity Detection"""
    # Silence timeout in seconds - how long to wait after speech ends before processing
    silence_timeout: float = 2.5
    
    # Minimum speech duration in seconds - ignore very short utterances (deprecated, now using content length)
    min_speech_duration: float = 0.5
    
    # Maximum turn duration in seconds - force processing after this time
    max_turn_duration: float = 60.0
    
    # Minimum silence between words to consider as a pause (not end of turn)
    word_pause_threshold: float = 1.0
    
    # Enable debug logging
    debug_logging: bool = True

class VoiceActivityDetector:
    """
    Intelligent Voice Activity Detection system for natural conversation turns
    """
    
    def __init__(self, config: Optional[VADConfig] = None):
        """Initialize the VAD system"""
        self.config = config or VADConfig()
        self.speech_segments: List[SpeechSegment] = []
        self.last_speech_time: Optional[float] = None
        self.turn_start_time: Optional[float] = None
        self.current_turn_text: str = ""
        self.silence_timer_task: Optional[asyncio.Task] = None
        self.is_processing: bool = False
        self.turn_complete_callback: Optional[Callable[[str, List[SpeechSegment]], Union[None, Awaitable[None]]]] = None
        
        # Statistics
        self.total_turns: int = 0
        self.total_speech_duration: float = 0.0
        self.average_turn_length: float = 0.0
        
        logger.info(f"VAD initialized with config: {self.config}")
    
    def set_turn_complete_callback(self, callback: Callable[[str, List[SpeechSegment]], Union[None, Awaitable[None]]]):
        """Set callback function to call when a turn is complete"""
        self.turn_complete_callback = callback
    
    async def add_speech_segment(self, text: str, is_final: bool = False, confidence: float = 1.0):
        """
        Add a new speech segment to the current turn
        
        Args:
            text: The recognized speech text
            is_final: Whether this is a final recognition result
            confidence: Confidence score for the recognition
        """
        current_time = time.time()
        
        # Initialize turn if this is the first speech (only for non-empty speech)
        if self.turn_start_time is None and text.strip():
            self.turn_start_time = current_time
            if self.config.debug_logging:
                logger.info(f"🎤 Starting new conversation turn at {current_time}")
        
        # Create speech segment
        segment = SpeechSegment(
            text=text,
            start_time=current_time,
            end_time=current_time,
            confidence=confidence,
            is_final=is_final
        )
        
        # Update current turn text
        if is_final:
            # For final segments, add to accumulated text
            if text.strip():
                if self.current_turn_text:
                    self.current_turn_text += " " + text.strip()
                else:
                    self.current_turn_text = text.strip()
                
                self.speech_segments.append(segment)
                self.last_speech_time = current_time
                
                if self.config.debug_logging:
                    logger.info(f"📝 Added final segment: '{text}' (total: '{self.current_turn_text}')")
                
                # Reset silence timer only for non-empty speech
                await self._reset_silence_timer()
            else:
                # Empty final segment - just log it but don't reset timer
                if self.config.debug_logging:
                    logger.debug(f"🔇 Ignoring empty final segment during silence")
                
                # If we have no active turn and get empty speech, don't start processing
                if self.turn_start_time is None:
                    return
        else:
            # For partial segments, just log for feedback
            if self.config.debug_logging:
                logger.debug(f"🔄 Partial segment: '{text}'")
    
    async def _reset_silence_timer(self):
        """Reset the silence timer that determines when a turn is complete"""
        # Cancel existing timer
        if self.silence_timer_task and not self.silence_timer_task.done():
            self.silence_timer_task.cancel()
        
        # Start new timer
        self.silence_timer_task = asyncio.create_task(self._silence_timeout_handler())
    
    async def _silence_timeout_handler(self):
        """Handle silence timeout - determines when to process the turn"""
        try:
            await asyncio.sleep(self.config.silence_timeout)
            
            # Check if we have enough speech to process
            if self._should_process_turn():
                await self._complete_turn()
            else:
                if self.config.debug_logging:
                    logger.info(f"⏸️ Silence timeout but insufficient speech, resetting turn state...")
                
                # Reset the turn state if we don't have valid speech
                self._reset_turn_state()
                
        except asyncio.CancelledError:
            # Timer was reset, which is normal
            pass
    
    def _should_process_turn(self) -> bool:
        """Determine if the current turn should be processed"""
        if not self.current_turn_text.strip():
            return False
        
        # Check minimum speech content length (at least 3 characters for meaningful speech)
        if len(self.current_turn_text.strip()) < 3:
            return False
        
        # Check if we've exceeded maximum turn duration
        if self.turn_start_time:
            duration = time.time() - self.turn_start_time
            if duration > self.config.max_turn_duration:
                if self.config.debug_logging:
                    logger.info(f"⏰ Maximum turn duration exceeded ({duration:.1f}s), forcing processing")
                return True
        
        return True
    
    async def _complete_turn(self):
        """Complete the current turn and trigger processing"""
        if self.is_processing:
            return
        
        self.is_processing = True
        
        try:
            # Calculate turn statistics
            turn_duration = 0.0
            if self.turn_start_time and self.last_speech_time:
                turn_duration = self.last_speech_time - self.turn_start_time
            
            self.total_turns += 1
            self.total_speech_duration += turn_duration
            self.average_turn_length = self.total_speech_duration / self.total_turns
            
            if self.config.debug_logging:
                logger.info(f"✅ Turn complete! Duration: {turn_duration:.1f}s, Text: '{self.current_turn_text}'")
                logger.info(f"📊 Stats: Turn #{self.total_turns}, Avg length: {self.average_turn_length:.1f}s")
            
            # Call the callback with the complete turn
            if self.turn_complete_callback and self.current_turn_text.strip():
                result = self.turn_complete_callback(self.current_turn_text, self.speech_segments.copy())
                if asyncio.iscoroutine(result):
                    await result
            
            # Reset for next turn
            self._reset_turn_state()
            
        finally:
            self.is_processing = False
    
    def _reset_turn_state(self):
        """Reset state for the next conversation turn"""
        self.speech_segments.clear()
        self.current_turn_text = ""
        self.turn_start_time = None
        self.last_speech_time = None
        
        # Cancel any pending silence timer
        if self.silence_timer_task and not self.silence_timer_task.done():
            self.silence_timer_task.cancel()
            self.silence_timer_task = None
    
    async def force_complete_turn(self):
        """Force completion of the current turn (useful for manual triggers)"""
        if self.current_turn_text.strip():
            await self._complete_turn()
    
    def get_current_turn_preview(self) -> str:
        """Get a preview of the current turn being built"""
        return self.current_turn_text
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get VAD statistics"""
        return {
            "total_turns": self.total_turns,
            "total_speech_duration": self.total_speech_duration,
            "average_turn_length": self.average_turn_length,
            "current_turn_length": len(self.current_turn_text),
            "is_processing": self.is_processing,
            "has_active_turn": self.turn_start_time is not None
        }
    
    def update_config(self, **kwargs):
        """Update VAD configuration parameters"""
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
                logger.info(f"Updated VAD config: {key} = {value}")
            else:
                logger.warning(f"Unknown VAD config parameter: {key}")
    
    def reset(self):
        """Reset the VAD system completely"""
        self._reset_turn_state()
        self.total_turns = 0
        self.total_speech_duration = 0.0
        self.average_turn_length = 0.0
        logger.info("VAD system reset") 