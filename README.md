# SQUAD ONE - BERYL AGENTIC BUILDER

![SQUAD ONE Logo](https://img.shields.io/badge/SQUAD%20ONE-BERYL%20AGENTIC%20BUILDER-DAA520?style=for-the-badge&logo=artificial-intelligence)

A comprehensive AI agent builder and interaction platform featuring advanced multimodal deployment capabilities with cutting-edge voice synthesis and avatar interaction technologies.

## 🌟 Features

### 🤖 Professional Chat Interface
- **BERYL AI Assistant** - Intelligent conversational agent with dark old gold branding
- **Session Management** - UUID-based conversation tracking
- **Real-time Responses** - Local AI service with no API key dependencies
- **Professional Design** - Tailwind CSS with glass morphism effects

### 🎯 Build Squad Flow Visualizer
- **Project Chimera Integration** - Agentic workflow builder with drag-and-drop interface
- **Custom Character Figurines** - Professional character assets designed for workflow visualization
- **Interactive Canvas** - Real-time workflow creation and modification
- **Export Capabilities** - Save and share workflow configurations

### 🎭 THE ISP Avatar System
- **Real-time Voice Synthesis** - Browser-based speech synthesis with multiple voice options
- **Facial Animation** - Advanced lip sync and facial expression technology
- **Multi-AI Integration** - Support for multiple AI backends and voice models
- **Programming Playground** - Monaco editor integration for live coding
- **LiveKit Integration** - Real-time conversational AI with voice activity detection

### 🚀 One-Click Deployment Generator
- **8 Platform Support** - Replit, Docker, Vercel, Heroku, Railway, Render, Fly.io, DigitalOcean
- **Auto-Configuration** - Automatic generation of deployment files and environment variables
- **Professional Documentation** - Step-by-step deployment guides for each platform
- **Health Checks** - Built-in monitoring and status reporting

## 🛠️ Technology Stack

### Backend
- **Flask 3.0** - Modern Python web framework
- **SQLAlchemy** - Advanced ORM with PostgreSQL/SQLite support
- **Gunicorn** - Production WSGI server
- **Local AI Service** - No external API dependencies

### Frontend
- **Tailwind CSS** - Utility-first CSS framework with custom color scheme
- **React Spectrum UI** - Adobe's professional component library
- **Vanilla JavaScript** - Modern ES6+ features with real-time interactions
- **Monaco Editor** - Full-featured code editor integration

### AI & Voice Technology
- **Local AI Responses** - Intelligent conversation without API keys
- **Web Speech API** - Browser-based voice synthesis
- **Advanced Lip Sync** - FFmpeg-based facial animation
- **CSM Integration Ready** - Sesame CSM-1B ultra-realistic voice model support

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd squad-one-beryl-agentic-builder
   ```

2. **Install dependencies**
   ```bash
   pip install flask flask-sqlalchemy gunicorn psycopg2-binary email-validator requests
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

4. **Access the application**
   - Open your browser to `http://localhost:5000`
   - Main Chat Interface: `/`
   - Build Squad: `/build-squad`
   - THE ISP: `/the-isp`
   - Deployment Generator: `/deployment`

### HuggingFace Spaces Deployment

1. **Download the deployment package**
   - Extract `squad_one_huggingface_deploy.tar.gz`

2. **Upload to HuggingFace Spaces**
   - Create a new Space on HuggingFace
   - Upload all extracted files
   - Rename `huggingface_requirements.txt` to `requirements.txt`

3. **Deploy immediately**
   - No API keys required
   - No additional configuration needed
   - Application will start automatically

## 📁 Project Structure

```
squad-one-beryl-agentic-builder/
├── app.py                    # Flask application factory
├── main.py                   # Application entry point
├── routes.py                 # Route handlers and API endpoints
├── models.py                 # Database models
├── gemini_service.py         # Local AI service
├── templates/                # HTML templates
│   ├── index.html           # Main chat interface
│   ├── build_squad.html     # Flow visualizer
│   ├── the_isp.html         # Avatar system
│   └── deployment.html      # Deployment generator
├── static/                   # Frontend assets
│   ├── css/                 # Stylesheets
│   ├── js/                  # JavaScript modules
│   └── images/              # Image assets
├── deployment_generator.py   # Multi-platform deployment configs
├── instant_lipsync.py       # Lip sync utilities
└── replit.md                # Complete project documentation
```

## 🎮 User Interface

### Main Navigation
- **SQUAD ONE** - Primary chat interface with BERYL AI assistant
- **Build Squad** - Agentic workflow visualizer and builder
- **THE ISP** - Avatar conversation prototype with voice synthesis
- **Deploy** - One-click deployment configuration generator
- **Clear** - Reset conversation history

### Design System
- **Color Scheme**: Black background (#000000), teal green accents (#14B8A6)
- **Branding**: Dark old gold (#DAA520) for "SQUAD ONE" and "BERYL AGENTIC BUILDER"
- **Typography**: Inter font family with professional weight variations
- **Effects**: Glass morphism with subtle shadows and transparency

## 🔧 Configuration

### Environment Variables (Optional)
```bash
# Database (defaults to SQLite if not provided)
DATABASE_URL=postgresql://user:password@localhost/dbname

# Session management (auto-generated if not provided)
SESSION_SECRET=your-session-secret-key

# External integrations (optional for enhanced features)
LIVEKIT_URL=wss://your-livekit-server
LIVEKIT_API_KEY=your-livekit-api-key
LIVEKIT_API_SECRET=your-livekit-api-secret
HUGGINGFACE_TOKEN=your-huggingface-token
GITHUB_TOKEN=your-github-token
DOCKER_API_KEY=your-docker-api-key
```

## 🚀 Deployment Options

### 1. Replit
- Use provided `.replit` configuration
- Automatic dependency installation
- Built-in database and environment management

### 2. Docker
```dockerfile
FROM python:3.11-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
```

### 3. Vercel
```json
{
  "builds": [{"src": "main.py", "use": "@vercel/python"}],
  "routes": [{"src": "/(.*)", "dest": "main.py"}]
}
```

### 4. Railway
```toml
[build]
builder = "NIXPACKS"

[deploy]
startCommand = "gunicorn --bind 0.0.0.0:$PORT main:app"
```

## 🧪 API Endpoints

### Chat API
- `POST /api/chat` - Send message and receive AI response
- `GET /api/history` - Retrieve conversation history
- `POST /api/clear` - Clear conversation history
- `GET /api/status` - Check AI service status

### Voice & Avatar API
- `POST /api/gemini-chat` - Gemini-style chat responses
- `POST /api/speech-synthesis` - Text-to-speech conversion
- `GET /api/csm-status` - CSM model availability
- `POST /api/instant-lipsync` - Quick lip sync processing

### Integration API
- `POST /api/github-integration` - GitHub repository access
- `POST /api/docker-integration` - Docker container management
- `POST /api/deployment-generator` - Generate deployment configs

## 🎯 Advanced Features

### THE ISP Avatar System
- **Multi-Modal Interaction** - Text, voice, and visual avatar responses
- **Real-Time Animation** - Synchronized lip movements and facial expressions
- **Voice Options** - Multiple synthesis engines with quality preferences
- **Programming Integration** - Live coding environment with AI assistance

### Build Squad Flow Visualizer
- **Drag-and-Drop Interface** - Visual workflow creation
- **Custom Components** - Specialized agentic building blocks
- **Export/Import** - Save and share workflow configurations
- **Real-Time Collaboration** - Multi-user workflow editing

### Deployment Generator
- **Multi-Platform Support** - 8 major deployment platforms
- **Auto-Configuration** - Intelligent environment detection
- **Best Practices** - Industry-standard deployment patterns
- **Documentation Generation** - Automatic README and guide creation

## 🔒 Security Features

- **Session Management** - Secure UUID-based session tracking
- **Environment Isolation** - Proper secret and configuration management
- **Input Validation** - Comprehensive request sanitization
- **HTTPS Ready** - SSL/TLS support with proper proxy configuration

## 🧩 Extensibility

### Adding New AI Models
1. Create service class in `services/` directory
2. Implement standard interface methods
3. Add to fallback chain in `routes.py`
4. Update configuration templates

### Custom UI Components
1. Add React components to `src/components/`
2. Update Tailwind configuration
3. Integrate with existing design system
4. Test across all interfaces

### New Deployment Platforms
1. Add platform configuration to `deployment_generator.py`
2. Create platform-specific templates
3. Update documentation
4. Test deployment process

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test thoroughly across all interfaces
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## 🎯 Support

For questions, issues, or contributions:
- Review the complete documentation in `replit.md`
- Check existing issues and discussions
- Create detailed bug reports with reproduction steps
- Suggest enhancements with clear use cases

---

**SQUAD ONE - BERYL AGENTIC BUILDER**  
*Professional AI Agent Development Platform*  
*Ready for immediate deployment across multiple platforms*

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Python](https://img.shields.io/badge/python-3.11+-blue)
![Flask](https://img.shields.io/badge/flask-3.0+-green)
![License](https://img.shields.io/badge/license-MIT-blue)