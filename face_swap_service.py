"""
Face Swap Service for Avatar Animation
Uses HuggingFace models for real-time face swapping and animation
"""

import os
import logging
import requests
import json
import base64
import io
from PIL import Image
import numpy as np

logger = logging.getLogger(__name__)

class FaceSwapService:
    def __init__(self):
        # Use the latest face swap models from HuggingFace
        self.face_swap_api = "https://api-inference.huggingface.co/models/deepinsight/inswapper"
        self.face_enhance_api = "https://api-inference.huggingface.co/models/sczhou/CodeFormer"
        self.face_animate_api = "https://api-inference.huggingface.co/models/runwayml/stable-video-diffusion-img2vid"
        
        self.headers = None
        self.is_initialized = False
        self.source_face = None  # User's uploaded avatar
        
    def initialize(self):
        """Initialize the face swap service with HuggingFace API"""
        try:
            logger.info("Initializing Face Swap service...")
            
            # Get HuggingFace token
            hf_token = os.environ.get('HUGGINGFACE_TOKEN')
            if not hf_token:
                raise ValueError("HUGGINGFACE_TOKEN environment variable not set")
            
            self.headers = {
                "Authorization": f"Bearer {hf_token}",
                "Content-Type": "application/json"
            }
            
            self.is_initialized = True
            logger.info("Face Swap service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Face Swap service: {e}")
            self.is_initialized = False
            raise
    
    def set_source_face(self, image_path):
        """Set the source face image (user's avatar)"""
        try:
            with open(image_path, 'rb') as f:
                image_data = f.read()
                self.source_face = base64.b64encode(image_data).decode('utf-8')
            logger.info(f"Source face loaded from {image_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to load source face: {e}")
            return False
    
    def generate_speaking_face(self, emotion="neutral", intensity=0.5):
        """
        Generate an animated face with speaking expression
        
        Args:
            emotion (str): Emotion type (neutral, happy, surprised, etc.)
            intensity (float): Animation intensity (0.0 to 1.0)
            
        Returns:
            str: Base64 encoded image data
        """
        if not self.is_initialized or not self.source_face:
            raise RuntimeError("Face swap service not initialized or no source face")
        
        try:
            # Create different mouth shapes for speaking animation
            mouth_shapes = {
                'closed': 0.0,
                'slightly_open': 0.2,
                'open': 0.5,
                'wide_open': 0.8,
                'o_shape': 0.3,
                'smile': 0.4
            }
            
            # Generate speaking expression based on phoneme
            expression_prompt = self._get_expression_prompt(emotion, intensity)
            
            payload = {
                "inputs": {
                    "source_image": self.source_face,
                    "expression": expression_prompt,
                    "intensity": intensity
                },
                "parameters": {
                    "num_inference_steps": 20,
                    "guidance_scale": 7.5,
                    "output_format": "jpeg"
                }
            }
            
            response = requests.post(
                self.face_swap_api,
                headers=self.headers,
                json=payload,
                timeout=15
            )
            
            if response.status_code == 200:
                # Return the generated face image
                if response.headers.get('content-type', '').startswith('image/'):
                    image_data = base64.b64encode(response.content).decode('utf-8')
                    return image_data
                else:
                    # Handle JSON response
                    result = response.json()
                    if 'image' in result:
                        return result['image']
                    
            logger.warning(f"Face swap API returned status {response.status_code}")
            return None
            
        except Exception as e:
            logger.error(f"Face swap generation error: {e}")
            return None
    
    def _get_expression_prompt(self, emotion, intensity):
        """Generate expression prompt for different emotions and speaking states"""
        base_prompts = {
            'neutral': "natural speaking expression, slight mouth movement",
            'happy': "smiling while speaking, warm expression",
            'surprised': "surprised expression with open mouth",
            'focused': "concentrated expression, slight frown",
            'friendly': "warm, welcoming expression while talking"
        }
        
        intensity_modifiers = {
            0.0: "very subtle",
            0.3: "gentle",
            0.5: "moderate",
            0.7: "pronounced",
            1.0: "very expressive"
        }
        
        base = base_prompts.get(emotion, base_prompts['neutral'])
        modifier = intensity_modifiers.get(round(intensity, 1), "moderate")
        
        return f"{modifier} {base}, high quality, realistic"
    
    def create_phoneme_face(self, phoneme, base_emotion="neutral"):
        """
        Create a face expression for a specific phoneme
        
        Args:
            phoneme (str): Phoneme type (a, e, i, o, u, m, b, p, f, s)
            base_emotion (str): Base emotional state
            
        Returns:
            str: Base64 encoded image data
        """
        phoneme_expressions = {
            'a': ("open mouth, ah sound", 0.7),
            'e': ("slightly open mouth, eh sound", 0.4),
            'i': ("narrow mouth opening, ee sound", 0.3),
            'o': ("rounded mouth, oh sound", 0.5),
            'u': ("pursed lips, oo sound", 0.4),
            'm': ("closed lips, humming", 0.1),
            'b': ("lips together, b sound", 0.2),
            'p': ("puffed cheeks, p sound", 0.3),
            'f': ("lip bite, f sound", 0.2),
            's': ("slight smile, s sound", 0.3)
        }
        
        if phoneme in phoneme_expressions:
            expression, intensity = phoneme_expressions[phoneme]
            return self.generate_speaking_face(f"{base_emotion}_{expression}", intensity)
        
        return self.generate_speaking_face(base_emotion, 0.3)
    
    def get_status(self):
        """Get the current status of the face swap service"""
        return {
            'initialized': self.is_initialized,
            'has_source_face': self.source_face is not None,
            'models': ['deepinsight/inswapper', 'sczhou/CodeFormer'],
            'available': self.is_initialized,
            'method': 'HuggingFace Face Swap API'
        }

# Global service instance
face_swap_service = FaceSwapService()

def get_face_swap_service():
    """Get the global face swap service instance"""
    if not face_swap_service.is_initialized:
        face_swap_service.initialize()
    return face_swap_service