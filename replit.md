# SQUAD ONE - BERYL AGENTIC BUILDER

## Overview

This is a Flask-based web application that provides a professional chat interface for the BERYL AGENTIC BUILDER AI assistant. The application features comprehensive vision tooling, file upload capabilities, and Project Chimera's Build Squad flow visualizer for creating agentic workflows through an intuitive drag-and-drop interface.

## User Preferences

```
Preferred communication style: Simple, everyday language.
UI Framework: Adobe React Spectrum UI with React components for professional interface and client use.
Color Scheme: Black background with teal green (#14B8A6) accents and white text.
Logo Styling: Both "SQUAD ONE" and "BERYL AGENTIC BUILDER" always displayed in dark old gold (#DAA520) thick font (font-weight: 900).
Vision Tooling: Comprehensive file upload suite (images, audio, documents) with drag-and-drop support.
Build Squad Feature: Project Chimera-inspired agentic flow visualizer with custom professional character figurines designed by user.
THE ISP Feature: Real conversation avatar prototyping using multiple AI backends - Gemini 2.5 voice agents, CSM (Conversational Speech Model) for ultra-realistic speech generation, Model Context Protocol (MCP) for 50-100ms GPU latency, HuggingFace streaming, and LiveKit for lip sync and facial animation. Includes programming playground with Monaco editor, GitHub integration, Docker container management, and comprehensive voice interaction capabilities with speech recognition and synthesis.
```

## System Architecture

The application follows a traditional MVC (Model-View-Controller) pattern built on Flask:

### Backend Architecture
- **Framework**: Flask web framework with SQLAlchemy ORM
- **Language Model Integration**: Hugging Face Transformers with the unsloth/Kimi-K2-Instruct-GGUF model
- **Database**: SQLite (development) with support for PostgreSQL via DATABASE_URL environment variable
- **Session Management**: Flask sessions with UUID-based session tracking

### Frontend Architecture
- **Template Engine**: Jinja2 templates
- **UI Framework**: Tailwind CSS with Spectrum UI-inspired design patterns
- **JavaScript**: Vanilla JavaScript for chat functionality with modern ES6+ features
- **Icons**: Lucide Icons (modern successor to Feather Icons)
- **Fonts**: Google Fonts (Inter)
- **Design System**: Custom implementation inspired by Spectrum UI with glass morphism effects

## Key Components

### 1. Application Core (`app.py`)
- Flask application factory pattern
- Database initialization and configuration
- SQLAlchemy setup with declarative base
- ProxyFix middleware for deployment behind reverse proxies
- Environment-based configuration for database and session secrets

### 2. Models (`models.py`)
- **ChatMessage**: Stores conversation history with session tracking
  - Fields: id, session_id, role (user/assistant), content, timestamp
  - Includes serialization method for API responses

### 3. Model Service (`model_service.py`)
- **ModelService**: Handles AI model loading and inference
  - Loads Kimi-K2-Instruct model using Transformers
  - Supports both CUDA and CPU execution
  - Implements text generation pipeline
  - Includes error handling and loading state management

### 4. Routes (`routes.py`)
- **Main Interface** (`/`): Serves the Tailwind CSS chat UI with session initialization
- **React Interface** (`/react`): Serves the React Spectrum UI chat interface
- **Build Squad** (`/build-squad`): Project Chimera agentic flow visualizer interface
- **THE ISP** (`/the-isp`): Avatar conversation prototype with Gemini 2.5 voice agents, CSM speech synthesis, MCP, HuggingFace streaming and LiveKit
- **Deployment Generator** (`/deployment`): One-click deployment configuration generator for 8 platforms
- **MCP Setup** (`/mcp-setup`): Model Context Protocol setup guide for fast local inference
- **API Endpoints**:
  - `/api/gemini-chat`: Gemini 2.5 voice agent responses with natural conversation
  - `/api/csm-speech`: CSM ultra-realistic speech generation with conversational context
  - `/api/csm-status`: CSM model status and availability check
  - `/api/hf-chat`: HuggingFace Llama-3-8B text-based conversations  
  - `/api/github-integration`: GitHub repository and profile access
  - `/api/docker-integration`: Docker Hub container management and deployment
  - `/api/deployment-generator`: One-click deployment configuration generator for multiple platforms
- **Chat API** (`/api/chat`): Handles message processing and AI responses
  - Validates input messages
  - Saves user messages to database
  - Generates AI responses via ModelService
  - Stores conversation history

### 5. Frontend Components
- **HTML Template** (`templates/index.html`): Modern chat interface with Spectrum UI-inspired design using Tailwind CSS
- **React Template** (`templates/react.html`): React-based interface using React Spectrum UI components
- **Build Squad Template** (`templates/build_squad.html`): Interactive agentic flow visualizer with custom character figurines
- **THE ISP Template** (`templates/the_isp.html`): Avatar conversation prototype interface with streaming settings and programming playground
- **Deployment Template** (`templates/deployment.html`): Professional deployment generator interface with platform selection and configuration display
- **CSS Styling**: Tailwind CSS with custom color scheme and glass morphism effects
- **JavaScript** (`static/js/chat.js`): Real-time chat functionality with enhanced UX for Tailwind interface
- **JavaScript** (`static/js/the_isp.js`): Avatar prototype controller with multi-AI backend support, LiveKit integration, and Monaco editor
- **JavaScript** (`static/js/gemini_voice_agent.js`): Comprehensive voice agent with Gemini 2.5, CSM speech synthesis, and multi-platform integration testing
- **Python** (`csm_integration.py`): CSM (Conversational Speech Model) integration for ultra-realistic speech generation with Sesame AI Labs technology
- **React Components**: Native React components with Spectrum UI design system

## Data Flow

1. **User Interaction**: User types message in web interface
2. **Frontend Processing**: JavaScript validates input and sends POST request to `/api/chat`
3. **Backend Processing**: 
   - Flask route receives message
   - Saves user message to database
   - Calls ModelService to generate AI response
   - Saves AI response to database
   - Returns response to frontend
4. **UI Update**: JavaScript updates chat interface with new messages

## External Dependencies

### Python Packages
- **Flask**: Web framework and routing
- **Flask-SQLAlchemy**: Database ORM
- **Transformers**: Hugging Face model loading and inference
- **PyTorch**: Deep learning framework for model execution
- **Werkzeug**: WSGI utilities and middleware

### Frontend Dependencies (CDN)
- **Tailwind CSS**: Utility-first CSS framework for rapid UI development (main interface)
- **React & ReactDOM**: Core React libraries for component-based interface
- **Spectrum CSS**: Adobe's design system CSS for React interface
- **Lucide Icons**: Modern icon library with React-like API (Tailwind interface)
- **Google Fonts**: Typography (Inter font family)
- **Design System**: Both Spectrum UI-inspired (Tailwind) and native Spectrum UI (React)

### AI Models & Voice Technology
- **unsloth/Kimi-K2-Instruct-GGUF**: Language model from Hugging Face
- **CSM (Conversational Speech Model)**: Ultra-realistic speech generation from Sesame AI Labs
  - CSM-1B model with Llama-3.2-1B tokenizer
  - Mimi audio codec for 24kHz high-quality audio
  - Professional watermarking for AI transparency
- **LiveKit Voice AI**: Real-time conversational agents
  - STT-LLM-TTS pipeline with voice activity detection
  - Turn detection and noise cancellation
  - Multi-provider integration (OpenAI, Deepgram, Cartesia)
- Supports both GPU (CUDA) and CPU inference
- Uses GGUF format for efficient loading

## Deployment Strategy

### Configuration
- Environment variables for sensitive data (DATABASE_URL, SESSION_SECRET)
- Support for both development (SQLite) and production (PostgreSQL) databases
- ProxyFix middleware for deployment behind load balancers/reverse proxies

### Database Management
- Automatic table creation on startup
- Connection pooling with health checks (pool_pre_ping)
- Connection recycling every 300 seconds

### Model Loading
- Automatic model initialization on startup
- Device detection (CUDA/CPU) with appropriate memory management
- Error handling for model loading failures

### Development vs Production
- Debug mode enabled for development
- Configurable host and port settings
- Logging configured at DEBUG level for troubleshooting

The application is designed to be easily deployable on platforms like Replit, with minimal configuration required for basic functionality.

## Project Artifacts & Deliverables

### Core Features Implemented
1. **SQUAD ONE Chat Interface** - Professional conversational AI with dark old gold branding
2. **Build Squad Flow Visualizer** - Project Chimera-inspired agentic workflow builder
3. **THE ISP Voice Avatar System** - Advanced multi-modal conversation prototype
4. **Deployment Generator** - One-click deployment configurations for 8 platforms

### Advanced Voice AI Integration
- **CSM (Conversational Speech Model)** - Ultra-realistic speech synthesis from Sesame AI Labs
- **LiveKit Voice AI** - Real-time conversational agents with STT-LLM-TTS pipeline
- **Gemini 2.5 Voice Agents** - Natural conversation with context awareness
- **Professional Audio Pipeline** - 24kHz quality with AI watermarking

### Multi-Platform Deployment Support
- **Replit** - Complete .replit configuration with Nix packages
- **Docker** - Multi-stage builds with health checks and PostgreSQL
- **Vercel** - Serverless deployment with environment variables
- **Heroku** - Procfile with PostgreSQL addon integration
- **Railway** - Nixpacks configuration with auto-deployment
- **Render** - Web service with health check monitoring
- **Fly.io** - Global deployment with auto-rollback
- **DigitalOcean** - App Platform with managed database

### API Integrations
- **GitHub Integration** - Repository access and profile management
- **Docker Hub Integration** - Container management and deployment
- **HuggingFace Streaming** - Real-time model inference
- **Multi-Provider AI** - OpenAI, Anthropic, Google Gemini support

### Professional UI Components
- **Tailwind CSS Design System** - Custom color scheme with glass morphism
- **React Spectrum UI** - Adobe's professional component library
- **Monaco Editor** - Full programming environment integration
- **Responsive Design** - Landscape format optimized for professional use

### Security & Production Features
- **Environment Variable Management** - Secure API key handling
- **Session Management** - UUID-based conversation tracking
- **Database Abstraction** - SQLite development, PostgreSQL production
- **Error Handling** - Comprehensive logging and diagnostics
- **Health Checks** - Application monitoring and status reporting

### Technical Architecture
- **Flask Backend** - Python 3.11 with SQLAlchemy ORM
- **Modern Frontend** - Vanilla JavaScript with ES6+ features
- **Database Layer** - Flexible SQLite/PostgreSQL support
- **AI Model Integration** - Multiple provider support with fallbacks
- **Voice Processing** - Advanced audio synthesis and recognition

### Deployment Ready Status
✅ All compilation issues resolved - Application running stable
✅ Complete platform configuration files generated for 8 platforms
✅ Environment variable templates provided with secure handling
✅ Professional deployment documentation with step-by-step guides
✅ One-click deployment capability with automated config generation
✅ Production-ready architecture with optimized dependencies
✅ Gemini AI service integration active and operational
✅ Voice AI pipeline ready for real-time conversations
✅ Professional UI with dark old gold branding implemented
✅ Multi-modal interaction capabilities fully functional

### Recent Deployment Fixes (January 2025)
- **Restored Full Application**: Reverted from simplified Kimi-3 experiment back to complete SQUAD ONE system
- **Database Configuration**: Fixed SQLAlchemy database URI with SQLite fallback for development
- **Route Integration**: Restored full routing system with all templates and API endpoints
- **Gemini AI Service**: Re-enabled primary AI backend with fallback chain (Gemini → Transformers → Mock)
- **Complete Feature Set**: All SQUAD ONE features restored including Build Squad, THE ISP, and deployment tools

### Voice System Enhancements (January 2025)
- **Browser Speech Synthesis**: Implemented reliable voice functionality using Web Speech API
- **Real-time Lip Sync**: Added visual mouth animation synchronized with speech output
- **CSM-1B Integration Ready**: Sesame CSM-1B ultra-realistic voice model integration prepared
- **Dual Voice Options**: Gold button for browser voice, brown button for CSM-1B (when available)
- **Professional Audio Pipeline**: 24kHz quality with automatic fallback systems
- **Conversation System Fixed**: Removed environment initialization requirement for immediate voice access

### Critical Lip Sync Repair Solution (January 2025) - IMPLEMENTED
- **Root Cause Identified**: Face-anchor mis-scaling and 256×256 crop losing mouth region in wav2lip-2
- **Critical Issue**: "The mouth simply isn't inside the square crop that the lip-syncer is expecting"
- **Problem**: 45% forehead + 55% upper lip = top lip flicker only, no lower lip motion
- **Solution Applied**: FFmpeg crop filter with precise coordinates (h*0.45:0.75, w*0.35:0.65)
- **Implementation**: `crop=iw*0.30:ih*0.30:iw*0.35:ih*0.45,scale=256:256` in instant_lipsync.py
- **Result**: Mouth properly positioned INSIDE the 256×256 square for accurate lip sync
- **Status**: COMPLETED - Both instant and advanced solutions implemented

### Backup Instant Lip Sync (Zero-Coding Solution)
- **Files Added**: mouth_roi.jpg and sync.mp4 from Sesame CSM-1B utilities
- **11-Line Solution**: instant_lipsync.py provides immediate lip sync using FFmpeg only
- **API Endpoints**: /instant-lipsync for immediate results, /lip-sync-repair for advanced processing
- **Deployment Ready**: Works with any 22kHz 16-bit WAV, outputs 256×256 MP4 overlay
- **Fallback Strategy**: Zero dependencies, instant deployment, adjustable with drag slider

### Live Feature Status
🟢 **Core Application**: Running stable on port 5000
🟢 **Chat Interface**: Operational with Gemini AI backend
🟢 **Build Squad**: Ready for agentic workflow creation
🟢 **THE ISP Voice System**: Active with multi-AI integration
🟢 **Deployment Generator**: Functional with 8-platform support
🟢 **API Endpoints**: All services responding correctly
🟢 **Database**: SQLAlchemy ORM with session management active
🟢 **Security**: Environment variable handling and session tracking operational

The project represents a comprehensive AI agent builder platform with state-of-the-art voice capabilities, professional deployment options, and enterprise-ready features. Successfully deployed and operational as of January 2025.