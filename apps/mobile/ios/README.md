# SDU ChatBot iOS App

## Product Overview

SDU ChatBot is a native iOS application that provides students and staff with an intelligent conversational interface to get information about Suleyman Demirel University (SDU). The app features a modern chat interface with Google authentication, real-time messaging, and source-backed responses to ensure accurate information delivery.

## Problem & Solution

**Problem**: Students and staff at SDU often struggle to find specific information about university services, policies, procedures, and resources scattered across multiple platforms and documents.

**Solution**: SDU ChatBot centralizes university information through an AI-powered conversational interface that provides instant, accurate answers with source citations, making university information easily accessible through natural language queries.

## Target Users

- **Primary**: SDU students seeking information about courses, schedules, policies, and university services
- **Secondary**: SDU staff and faculty needing quick access to institutional information
- **Tertiary**: Prospective students exploring SDU programs and facilities

## Tech Stack

- **Platform**: iOS (SwiftUI)
- **Language**: Swift
- **Architecture**: MVVM (Model-View-ViewModel)
- **Authentication**: Google OAuth 2.0
- **Networking**: URLSession with custom APIClient
- **Storage**: Keychain for secure token storage
- **UI Framework**: SwiftUI with custom components
- **Configuration**: Xcode Configuration Files (.xcconfig)

## System Requirements

- **iOS**: 15.0 or later
- **Xcode**: 15.0 or later
- **macOS**: 13.0 or later (for development)
- **Swift**: 5.9 or later

## Local Development Setup

### Prerequisites

1. Install Xcode from the Mac App Store
2. Ensure you have an active Apple Developer account
3. Access to SDU ChatBot backend API

### Environment Configuration

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd SDUChatBot
   ```

2. **Configure environment variables**:
   
   Update the configuration files with your environment-specific values:
   
   **For Development** (`Config/Dev.xcconfig`):
   ```
   BASE_URL = https://your-dev-domain.com/api
   OAUTH_START_URL = https://your-dev-domain.com/api/auth/google/start
   URL_SCHEME = sduchat
   STATIC_BEARER = your-optional-static-bearer-token
   ```
   
   **For Production** (`Config/Prod.xcconfig`):
   ```
   BASE_URL = https://chat.sdu.edu.kz/api
   OAUTH_START_URL = https://chat.sdu.edu.kz/api/auth/google/start
   URL_SCHEME = sduchat
   STATIC_BEARER = your-optional-static-bearer-token
   ```

3. **Open the project**:
   ```bash
   open SDUChatBot.xcodeproj
   ```

4. **Select build configuration**:
   - For development: Select "Debug" configuration
   - For production: Select "Release" configuration

5. **Build and run**:
   - Select your target device or simulator
   - Press `Cmd + R` to build and run

### Required Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `BASE_URL` | Backend API base URL | Yes |
| `OAUTH_START_URL` | Google OAuth start endpoint | Yes |
| `URL_SCHEME` | App URL scheme for OAuth callback | Yes |
| `STATIC_BEARER` | Optional static bearer token for public API | No |

## Testing

Currently, the project uses manual testing through the iOS Simulator and physical devices. 

### Manual Testing Checklist

1. **Authentication Flow**:
   - Launch app
   - Verify Google login button appears
   - Test OAuth flow completion
   - Verify token storage

2. **Chat Functionality**:
   - Send messages
   - Verify response display
   - Test source citations
   - Check message history
   - Test typing indicators

3. **UI/UX Testing**:
   - Test on different screen sizes
   - Verify dark/light mode compatibility
   - Test keyboard interactions
   - Verify scroll behavior

### Running Tests

```bash
# Build for testing
xcodebuild -project SDUChatBot.xcodeproj -scheme SDUChatBot -destination 'platform=iOS Simulator,name=iPhone 15' build-for-testing

# Run UI tests (when implemented)
xcodebuild -project SDUChatBot.xcodeproj -scheme SDUChatBot -destination 'platform=iOS Simulator,name=iPhone 15' test
```

## Project Structure

```
SDUChatBot/
├── App/                          # Application entry point
│   ├── SDUChatBotApp.swift      # Main app file with scene configuration
│   └── ContentView.swift        # Root content view (currently empty)
│
├── Features/                     # Feature-based modules
│   ├── Auth/                    # Authentication feature
│   │   ├── AuthCoordinator.swift    # Auth navigation coordination
│   │   ├── AuthViewModel.swift      # Auth business logic
│   │   └── LoginView.swift          # Login UI components
│   │
│   └── Chat/                    # Chat feature
│       ├── ChatView.swift           # Main chat interface
│       └── ChatViewModel.swift      # Chat business logic
│
├── Models/                      # Data models and DTOs
│   └── DTO.swift               # API response/request models
│
├── Services/                    # Business services
│   ├── API/                    # API communication layer
│   │   ├── APIClient.swift         # HTTP client with auth
│   │   ├── Env.swift              # Environment configuration
│   │   └── NetLogger.swift        # Network request logging
│   │
│   └── Storage/                # Data persistence (Keychain, etc.)
│
├── Assets.xcassets/            # App assets (images, colors)
│   ├── AppIcon.appiconset/         # App icons
│   ├── sdu_logo.imageset/          # University logo
│   ├── SDUlogo-white.imageset/     # White variant logo
│   ├── Frame.imageset/             # Send button icon
│   ├── sduPrimary.colorset/        # Primary brand color
│   └── AccentColor.colorset/       # System accent color
│
├── Config/                     # Build configurations
│   ├── Dev.xcconfig               # Development environment
│   └── Prod.xcconfig              # Production environment
│
└── Info.plist                 # App configuration and permissions
```

### Key Components Description

- **App/**: Contains the main application entry point and root views
- **Features/**: Organized by feature domains (Auth, Chat) following MVVM pattern
- **Models/**: Codable structs for API communication and data modeling
- **Services/API/**: Centralized API client with authentication and environment management
- **Services/Storage/**: Secure storage services (Keychain integration)
- **Assets.xcassets/**: All visual assets including brand colors and logos
- **Config/**: Environment-specific build configurations for different deployment targets

## Additional Documentation

- [API Documentation](docs/API.md) - Backend API endpoints and integration details
- [Authentication Flow](docs/AUTH.md) - Google OAuth implementation guide
- [UI Components](docs/UI.md) - Custom SwiftUI components documentation
- [Deployment Guide](docs/DEPLOYMENT.md) - App Store deployment process
- [Contributing Guidelines](CONTRIBUTING.md) - Development workflow and standards

## Development Workflow

1. Create feature branches from `main`
2. Follow the existing MVVM architecture pattern
3. Add new features in the `Features/` directory
4. Update configuration files for environment-specific settings
5. Test on both simulator and physical devices
6. Submit pull requests with clear descriptions

## Support

For technical issues or questions:
- Create an issue in the repository
- Contact the development team
- Refer to the additional documentation links above