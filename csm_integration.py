"""
CSM (Conversational Speech Model) Integration for THE ISP
Advanced speech generation using Sesame AI Labs' state-of-the-art model
"""
import os
import torch
import torchaudio
import logging
from dataclasses import dataclass
from typing import List, Optional
from huggingface_hub import hf_hub_download

@dataclass
class Segment:
    speaker: int
    text: str
    audio: torch.Tensor  # (num_samples,), sample_rate = 24_000

class CSMVoiceAgent:
    """Advanced voice agent using CSM for ultra-realistic speech generation"""
    
    def __init__(self):
        self.generator = None
        self.device = self._get_best_device()
        self.sample_rate = 24000
        self.initialized = False
        self.error = None
        
        # Initialize CSM if possible
        self._init_csm()
    
    def _get_best_device(self):
        """Select the best available device"""
        if torch.cuda.is_available():
            return "cuda"
        elif torch.backends.mps.is_available():
            return "mps"
        else:
            return "cpu"
    
    def _init_csm(self):
        """Initialize the CSM model"""
        try:
            # Set environment for CSM
            os.environ["NO_TORCH_COMPILE"] = "1"
            
            # Import CSM components (only if available)
            from generator import load_csm_1b
            
            logging.info(f"Loading CSM model on {self.device}...")
            self.generator = load_csm_1b(device=self.device)
            self.sample_rate = self.generator.sample_rate
            self.initialized = True
            
            logging.info("CSM voice agent initialized successfully")
            
        except ImportError as e:
            self.error = f"CSM dependencies not available: {e}"
            logging.warning(f"CSM initialization failed: {self.error}")
        except Exception as e:
            self.error = f"CSM initialization error: {e}"
            logging.error(f"CSM initialization failed: {self.error}")
    
    def generate_speech(
        self, 
        text: str, 
        speaker_id: int = 0,
        context: List[Segment] = None,
        max_duration_ms: float = 10000,
        temperature: float = 0.9
    ) -> Optional[torch.Tensor]:
        """
        Generate ultra-realistic speech using CSM
        
        Args:
            text: Text to convert to speech
            speaker_id: Speaker identity (0 or 1)
            context: Previous conversation context for voice consistency
            max_duration_ms: Maximum audio duration in milliseconds
            temperature: Generation creativity (0.1-1.0)
        
        Returns:
            Generated audio tensor or None if failed
        """
        if not self.initialized:
            logging.error("CSM not initialized")
            return None
        
        try:
            # Use provided context or empty list
            if context is None:
                context = []
            
            # Generate speech with CSM
            audio = self.generator.generate(
                text=text,
                speaker=speaker_id,
                context=context,
                max_audio_length_ms=max_duration_ms,
                temperature=temperature,
                topk=50
            )
            
            return audio
            
        except Exception as e:
            logging.error(f"CSM speech generation failed: {e}")
            return None
    
    def create_voice_prompt(self, text: str, audio_path: str, speaker_id: int) -> Optional[Segment]:
        """Create a voice prompt segment from text and audio file"""
        try:
            # Load and resample audio
            audio_tensor, orig_sample_rate = torchaudio.load(audio_path)
            audio_tensor = audio_tensor.squeeze(0)  # Remove channel dimension
            
            # Resample to CSM's expected sample rate
            if orig_sample_rate != self.sample_rate:
                audio_tensor = torchaudio.functional.resample(
                    audio_tensor, 
                    orig_freq=orig_sample_rate, 
                    new_freq=self.sample_rate
                )
            
            return Segment(text=text, speaker=speaker_id, audio=audio_tensor)
            
        except Exception as e:
            logging.error(f"Failed to create voice prompt: {e}")
            return None
    
    def save_audio(self, audio: torch.Tensor, filename: str):
        """Save generated audio to file"""
        try:
            torchaudio.save(
                filename, 
                audio.unsqueeze(0).cpu(), 
                self.sample_rate
            )
            logging.info(f"Audio saved to {filename}")
            return True
        except Exception as e:
            logging.error(f"Failed to save audio: {e}")
            return False
    
    def is_available(self) -> bool:
        """Check if CSM is available and initialized"""
        return self.initialized and self.generator is not None
    
    def get_status(self) -> dict:
        """Get CSM status information"""
        return {
            'initialized': self.initialized,
            'device': self.device,
            'sample_rate': self.sample_rate,
            'error': self.error,
            'model_available': self.generator is not None
        }

# Global CSM instance
csm_agent = None

def get_csm_agent():
    """Get or create the global CSM agent instance"""
    global csm_agent
    if csm_agent is None:
        csm_agent = CSMVoiceAgent()
    return csm_agent

def test_csm_integration():
    """Test CSM integration with a simple example"""
    agent = get_csm_agent()
    
    if not agent.is_available():
        print(f"CSM not available: {agent.error}")
        return False
    
    try:
        # Generate a test sentence
        audio = agent.generate_speech(
            text="Hello from THE ISP! This is advanced speech synthesis using CSM.",
            speaker_id=0,
            max_duration_ms=5000
        )
        
        if audio is not None:
            agent.save_audio(audio, "csm_test.wav")
            print("CSM test successful - audio generated and saved")
            return True
        else:
            print("CSM test failed - no audio generated")
            return False
            
    except Exception as e:
        print(f"CSM test error: {e}")
        return False

if __name__ == "__main__":
    test_csm_integration()