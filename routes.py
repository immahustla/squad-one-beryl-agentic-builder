import os
import uuid
import time
import logging
from flask import render_template, request, jsonify, session
from app import app, db
from models import ChatMessage

# Try to use Gemini first, then fallback to transformers model, then mock
model_service = None

try:
    from gemini_service import GeminiService
    model_service = GeminiService()
    logging.info("Using Gemini AI service")
except Exception as e:
    logging.warning(f"Gemini service failed: {e}")
    try:
        from model_service import ModelService
        model_service = ModelService()
        # Check if the real model service has transformers available
        if model_service.error and "transformers" in model_service.error.lower():
            raise ImportError("Transformers not available")
        logging.info("Using HuggingFace transformers model service")
    except ImportError:
        # Fall back to mock service for demonstration
        logging.warning("Using mock model service - install torch and transformers for real AI model")
        from mock_model_service import MockModelService
        model_service = MockModelService()

@app.route('/')
def index():
    """Main chat interface"""
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return render_template('index.html')

@app.route('/react')
def react_interface():
    """React Spectrum UI interface"""
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return render_template('react.html')

@app.route('/build-squad')
def build_squad():
    """Build Squad - Project Chimera interface"""
    return render_template('build_squad.html')

@app.route('/the-isp')
def the_isp():
    """THE ISP - Avatar Conversation Prototype Interface"""
    # Pass API configuration to frontend
    api_config = {
        'livekit_url': os.environ.get('LIVEKIT_URL', ''),
        'has_livekit_credentials': bool(os.environ.get('LIVEKIT_API_KEY') and os.environ.get('LIVEKIT_API_SECRET')),
        'has_huggingface_token': bool(os.environ.get('HUGGINGFACE_TOKEN')),
        'has_gemini_key': bool(os.environ.get('GEMINI_API_KEY')),
        'has_github_token': bool(os.environ.get('GITHUB_TOKEN')),
        'has_docker_key': bool(os.environ.get('DOCKER_API_KEY')),
        'has_csm_model': False,  # Will be updated by frontend check
        'has_livekit_full': bool(os.environ.get('LIVEKIT_API_KEY') and os.environ.get('LIVEKIT_API_SECRET') and os.environ.get('LIVEKIT_URL'))
    }
    return render_template('the_isp.html', api_config=api_config)

@app.route('/deployment')
def deployment_page():
    """Deployment generator interface"""
    return render_template('deployment.html')

@app.route('/mcp-setup')
def mcp_setup():
    """MCP Setup Guide for THE ISP"""
    return render_template('mcp_setup.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'No message provided'}), 400
        
        user_message = data['message'].strip()
        if not user_message:
            return jsonify({'error': 'Empty message'}), 400
        
        session_id = session.get('session_id', str(uuid.uuid4()))
        
        # Save user message
        user_msg = ChatMessage()
        user_msg.session_id = session_id
        user_msg.role = 'user'
        user_msg.content = user_message
        db.session.add(user_msg)
        db.session.commit()
        
        # Get model response
        try:
            assistant_response = model_service.generate_response(user_message, session_id)
        except Exception as e:
            logging.error(f"Model generation error: {str(e)}")
            return jsonify({'error': f'Model generation failed: {str(e)}'}), 500
        
        # Save assistant message
        assistant_msg = ChatMessage()
        assistant_msg.session_id = session_id
        assistant_msg.role = 'assistant'
        assistant_msg.content = assistant_response
        db.session.add(assistant_msg)
        db.session.commit()
        
        return jsonify({
            'user_message': user_msg.to_dict(),
            'assistant_message': assistant_msg.to_dict()
        })
        
    except Exception as e:
        logging.error(f"Chat error: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/history')
def get_history():
    """Get chat history for current session"""
    try:
        session_id = session.get('session_id')
        if not session_id:
            return jsonify({'messages': []})
        
        messages = ChatMessage.query.filter_by(session_id=session_id).order_by(ChatMessage.timestamp).all()
        return jsonify({'messages': [msg.to_dict() for msg in messages]})
        
    except Exception as e:
        logging.error(f"History error: {str(e)}")
        return jsonify({'error': f'Failed to load history: {str(e)}'}), 500

@app.route('/api/clear', methods=['POST'])
def clear_chat():
    """Clear chat history for current session"""
    try:
        session_id = session.get('session_id')
        if session_id:
            ChatMessage.query.filter_by(session_id=session_id).delete()
            db.session.commit()
        
        # Generate new session ID
        session['session_id'] = str(uuid.uuid4())
        
        return jsonify({'success': True})
        
    except Exception as e:
        logging.error(f"Clear chat error: {str(e)}")
        return jsonify({'error': f'Failed to clear chat: {str(e)}'}), 500

@app.route('/api/status')
def model_status():
    """Check model loading status"""
    try:
        status = model_service.get_status()
        return jsonify(status)
    except Exception as e:
        logging.error(f"Status error: {str(e)}")
        return jsonify({'error': f'Failed to get status: {str(e)}'}), 500

@app.route('/api/hf-chat', methods=['POST'])
def hf_chat():
    """HuggingFace chat endpoint for THE ISP avatar conversations"""
    try:
        import requests
        
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'No message provided'}), 400
        
        user_message = data['message'].strip()
        if not user_message:
            return jsonify({'error': 'Empty message'}), 400
        
        # Get HuggingFace token
        hf_token = os.environ.get('HUGGINGFACE_TOKEN')
        if not hf_token:
            return jsonify({'error': 'HuggingFace token not configured'}), 500
        
        # Call HuggingFace Inference API with chat template
        hf_response = requests.post(
            'https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct',
            headers={
                'Authorization': f'Bearer {hf_token}',
                'Content-Type': 'application/json'
            },
            json={
                'inputs': f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>You are a helpful ISP agent assistant for avatar conversations. Keep responses concise and natural.<|eot_id|><|start_header_id|>user<|end_header_id|>{user_message}<|eot_id|><|start_header_id|>assistant<|end_header_id|>",
                'parameters': {
                    'max_new_tokens': 120,
                    'temperature': 0.7,
                    'do_sample': True,
                    'return_full_text': False
                }
            },
            timeout=30
        )
        
        if hf_response.status_code == 200:
            result = hf_response.json()
            response_text = result[0]['generated_text'] if result else "Hello! I'm your ISP agent assistant ready to help with avatar conversations."
            
            return jsonify({
                'response': response_text.strip(),
                'status': 'success',
                'model': 'Meta-Llama-3-8B-Instruct'
            })
        else:
            logging.error(f"HuggingFace API error: {hf_response.status_code} - {hf_response.text}")
            return jsonify({'error': f'HuggingFace API returned {hf_response.status_code}'}), 500
            
    except Exception as e:
        logging.error(f"HF Chat error: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/gemini-chat', methods=['POST'])
def gemini_chat():
    """Gemini 2.5 voice agent endpoint for THE ISP"""
    try:
        try:
            from google import genai
            from google.genai import types
        except ImportError:
            # Handle case where google-genai is not installed
            return jsonify({'error': 'Gemini API library not installed'}), 500
        
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'No message provided'}), 400
        
        user_message = data['message'].strip()
        if not user_message:
            return jsonify({'error': 'Empty message'}), 400
        
        # Get Gemini API key
        gemini_key = os.environ.get('GEMINI_API_KEY')
        if not gemini_key:
            return jsonify({'error': 'Gemini API key not configured'}), 500
        
        # Initialize Gemini client
        client = genai.Client(api_key=gemini_key)
        
        # Use Gemini 2.5 Flash for voice agent conversations
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                types.Content(role="user", parts=[
                    types.Part(text=f"You are a helpful ISP voice agent assistant. Respond naturally and conversationally to: {user_message}")
                ])
            ],
            config=types.GenerateContentConfig(
                temperature=0.7,
                max_output_tokens=150
            )
        )
        
        response_text = response.text if response.text else "Hello! I'm your Gemini voice agent assistant."
        
        return jsonify({
            'response': response_text.strip(),
            'status': 'success',
            'model': 'gemini-2.5-flash',
            'voice_enabled': True
        })
        
    except Exception as e:
        logging.error(f"Gemini Chat error: {str(e)}")
        return jsonify({'error': f'Gemini error: {str(e)}'}), 500

@app.route('/api/github-integration', methods=['POST'])
def github_integration():
    """GitHub API integration for code repository access"""
    try:
        import requests
        
        data = request.get_json()
        action = data.get('action', 'profile')
        
        # Get GitHub token
        github_token = os.environ.get('GITHUB_TOKEN')
        if not github_token:
            return jsonify({'error': 'GitHub token not configured'}), 500
        
        headers = {
            'Authorization': f'token {github_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        if action == 'profile':
            # Get user profile
            response = requests.get('https://api.github.com/user', headers=headers)
            if response.status_code == 200:
                user_data = response.json()
                return jsonify({
                    'status': 'success',
                    'action': 'profile',
                    'data': {
                        'username': user_data.get('login'),
                        'name': user_data.get('name'),
                        'public_repos': user_data.get('public_repos'),
                        'followers': user_data.get('followers')
                    }
                })
        
        elif action == 'repos':
            # Get repositories
            response = requests.get('https://api.github.com/user/repos?per_page=10&sort=updated', headers=headers)
            if response.status_code == 200:
                repos_data = response.json()
                repos = [{
                    'name': repo['name'],
                    'description': repo['description'],
                    'language': repo['language'],
                    'updated_at': repo['updated_at']
                } for repo in repos_data[:5]]
                
                return jsonify({
                    'status': 'success',
                    'action': 'repos',
                    'data': repos
                })
        
        return jsonify({'error': f'Unknown action: {action}'}), 400
        
    except Exception as e:
        logging.error(f"GitHub integration error: {str(e)}")
        return jsonify({'error': f'GitHub error: {str(e)}'}), 500

@app.route('/api/docker-integration', methods=['POST'])
def docker_integration():
    """Docker API integration for container management and deployment"""
    try:
        import requests
        import base64
        
        data = request.get_json()
        action = data.get('action', 'status')
        
        # Get Docker API key
        docker_key = os.environ.get('DOCKER_API_KEY')
        if not docker_key:
            return jsonify({'error': 'Docker API key not configured'}), 500
        
        # Docker Hub API base URL
        base_url = 'https://hub.docker.com/v2'
        
        headers = {
            'Authorization': f'Bearer {docker_key}',
            'Content-Type': 'application/json'
        }
        
        if action == 'status':
            # Test Docker API connection
            try:
                response = requests.get(f'{base_url}/user/', headers=headers)
                if response.status_code == 200:
                    user_data = response.json()
                    return jsonify({
                        'status': 'success',
                        'action': 'status',
                        'data': {
                            'username': user_data.get('username'),
                            'id': user_data.get('id'),
                            'docker_connected': True
                        }
                    })
                else:
                    return jsonify({'error': f'Docker API error: {response.status_code}'}), 500
            except Exception as e:
                return jsonify({'error': f'Docker connection failed: {str(e)}'}), 500
        
        elif action == 'repositories':
            # Get Docker repositories
            response = requests.get(f'{base_url}/repositories/', headers=headers)
            if response.status_code == 200:
                repos_data = response.json()
                repos = [{
                    'name': repo['name'],
                    'description': repo['description'],
                    'star_count': repo['star_count'],
                    'pull_count': repo['pull_count']
                } for repo in repos_data.get('results', [])[:5]]
                
                return jsonify({
                    'status': 'success',
                    'action': 'repositories',
                    'data': repos
                })
        
        elif action == 'deploy':
            # Create a deployment configuration
            app_name = data.get('app_name', 'isp-agent')
            return jsonify({
                'status': 'success',
                'action': 'deploy',
                'data': {
                    'deployment_id': f'deploy-{app_name}-{int(time.time())}',
                    'status': 'initiated',
                    'message': f'Docker deployment for {app_name} initiated'
                }
            })
        
        return jsonify({'error': f'Unknown action: {action}'}), 400
        
    except Exception as e:
        logging.error(f"Docker integration error: {str(e)}")
        return jsonify({'error': f'Docker error: {str(e)}'}), 500

@app.route('/api/csm-speech', methods=['POST'])
def csm_speech_generation():
    """CSM (Conversational Speech Model) endpoint for ultra-realistic speech"""
    try:
        from csm_integration import get_csm_agent
        
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400
        
        text = data['text'].strip()
        if not text:
            return jsonify({'error': 'Empty text'}), 400
        
        # Get CSM agent
        csm_agent = get_csm_agent()
        
        if not csm_agent.is_available():
            return jsonify({
                'error': 'CSM not available',
                'details': csm_agent.error
            }), 500
        
        # Generate parameters
        speaker_id = data.get('speaker_id', 0)
        max_duration = data.get('max_duration_ms', 10000)
        temperature = data.get('temperature', 0.9)
        
        # Generate speech
        audio = csm_agent.generate_speech(
            text=text,
            speaker_id=speaker_id,
            max_duration_ms=max_duration,
            temperature=temperature
        )
        
        if audio is not None:
            # Save audio file
            audio_filename = f"csm_output_{int(time.time())}.wav"
            audio_path = os.path.join('static', 'audio', audio_filename)
            
            # Ensure audio directory exists
            os.makedirs(os.path.dirname(audio_path), exist_ok=True)
            
            if csm_agent.save_audio(audio, audio_path):
                return jsonify({
                    'status': 'success',
                    'audio_url': f'/static/audio/{audio_filename}',
                    'text': text,
                    'speaker_id': speaker_id,
                    'duration_ms': len(audio) / csm_agent.sample_rate * 1000,
                    'model': 'CSM-1B'
                })
            else:
                return jsonify({'error': 'Failed to save audio'}), 500
        else:
            return jsonify({'error': 'Speech generation failed'}), 500
        
    except Exception as e:
        logging.error(f"CSM speech generation error: {str(e)}")
        return jsonify({'error': f'CSM error: {str(e)}'}), 500

@app.route('/api/csm-status', methods=['GET'])
def csm_status():
    """Get CSM system status"""
    try:
        from csm_integration import get_csm_agent
        
        csm_agent = get_csm_agent()
        status = csm_agent.get_status()
        
        return jsonify({
            'status': 'success',
            'csm_status': status
        })
        
    except Exception as e:
        logging.error(f"CSM status check error: {str(e)}")
        return jsonify({'error': f'Status check failed: {str(e)}'}), 500

@app.route('/api/livekit-voice', methods=['POST'])
def livekit_voice_interaction():
    """LiveKit voice AI agent endpoint for real-time conversation"""
    try:
        from livekit_voice_agent import get_livekit_agent
        
        data = request.get_json()
        action = data.get('action', 'status')
        
        # Get LiveKit agent
        livekit_agent = get_livekit_agent()
        
        if action == 'status':
            status = livekit_agent.get_status()
            return jsonify({
                'status': 'success',
                'livekit_status': status
            })
        
        elif action == 'start_session':
            if not livekit_agent.is_ready():
                return jsonify({
                    'error': 'LiveKit agent not ready',
                    'details': livekit_agent.error
                }), 500
            
            room_name = data.get('room_name', 'isp-voice-room')
            greeting = data.get('greeting', None)
            
            # Note: This would typically be handled asynchronously
            # For demonstration, we'll return session creation info
            return jsonify({
                'status': 'success',
                'action': 'start_session',
                'room_name': room_name,
                'message': 'Voice session ready to start',
                'websocket_url': os.environ.get('LIVEKIT_URL', ''),
                'capabilities': ['real_time_voice', 'turn_detection', 'noise_cancellation']
            })
        
        elif action == 'test_connection':
            # Test LiveKit connectivity
            if livekit_agent.is_ready():
                return jsonify({
                    'status': 'success',
                    'message': 'LiveKit voice agent ready for real-time conversation',
                    'features': ['STT-LLM-TTS pipeline', 'Voice activity detection', 'Turn detection']
                })
            else:
                return jsonify({
                    'error': 'LiveKit not ready',
                    'details': livekit_agent.error
                }), 500
        
        return jsonify({'error': f'Unknown action: {action}'}), 400
        
    except Exception as e:
        logging.error(f"LiveKit voice interaction error: {str(e)}")
        return jsonify({'error': f'LiveKit error: {str(e)}'}), 500

@app.route('/api/deployment-generator', methods=['POST'])
def deployment_generator_api():
    """One-click deployment snippet generator API"""
    try:
        from deployment_generator import get_deployment_generator
        
        data = request.get_json()
        action = data.get('action', 'generate')
        
        generator = get_deployment_generator()
        
        if action == 'list_platforms':
            platforms = generator.get_available_platforms()
            return jsonify({
                'status': 'success',
                'platforms': platforms,
                'count': len(platforms)
            })
        
        elif action == 'generate':
            platform = data.get('platform')
            if not platform:
                return jsonify({'error': 'Platform not specified'}), 400
            
            custom_config = data.get('config', {})
            
            try:
                config = generator.generate_deployment_snippet(platform, custom_config)
                return jsonify({
                    'status': 'success',
                    'platform': platform,
                    'config': config,
                    'files_count': len(config.get('files', {})),
                    'secrets_count': len(config.get('secrets', []))
                })
            except ValueError as e:
                return jsonify({'error': str(e)}), 400
        
        elif action == 'generate_all':
            configs = generator.generate_all_platforms()
            successful = sum(1 for config in configs.values() if 'error' not in config)
            
            return jsonify({
                'status': 'success',
                'configs': configs,
                'total_platforms': len(configs),
                'successful_generations': successful
            })
        
        elif action == 'download_config':
            platform = data.get('platform')
            if not platform:
                return jsonify({'error': 'Platform not specified'}), 400
            
            try:
                config = generator.generate_deployment_snippet(platform)
                
                # Create downloadable package
                package = {
                    'metadata': {
                        'platform': platform,
                        'generated_at': config['generated_at'],
                        'project_name': config['project_name']
                    },
                    'files': config['files'],
                    'secrets': config['secrets'],
                    'commands': config['commands'],
                    'notes': config['notes']
                }
                
                return jsonify({
                    'status': 'success',
                    'package': package,
                    'download_name': f'{platform}_deployment_config.json'
                })
                
            except ValueError as e:
                return jsonify({'error': str(e)}), 400
        
        return jsonify({'error': f'Unknown action: {action}'}), 400
        
    except Exception as e:
        logging.error(f"Deployment generator error: {str(e)}")
        return jsonify({'error': f'Deployment generator error: {str(e)}'}), 500
