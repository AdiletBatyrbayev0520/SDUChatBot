# SDU Chat Bot - Frontend

## Product Overview

SDU Chat Bot is a modern web-based chat application designed for Sdu Daryn University. This MVP provides an intelligent conversational interface that enables users to interact with an AI-powered chatbot through a clean, responsive user interface. The application features real-time messaging, conversation history management, and secure authentication.

## Problem and Solution

**Problem:** Students and staff at SDU need quick, accessible answers to common questions about university services, admissions, academic programs, and campus information. Traditional support channels can be slow and require human intervention for routine inquiries.

**Solution:** SDU Chat Bot provides an intelligent, 24/7 available conversational interface that can instantly respond to user queries. The application offers:
- Instant responses to common questions
- Conversation history for reference
- Multi-session support for organizing different topics
- Secure authentication through university credentials
- Mobile-responsive design for access anywhere

## Target Users

- **Students:** Seeking information about courses, admissions, schedules, and campus services
- **Prospective Students:** Inquiring about admission requirements and university programs
- **Staff and Faculty:** Accessing quick information about university policies and procedures
- **Administrators:** Managing and monitoring chat interactions

## Tech Stack

### Frontend
- **React 19.1.0** - UI library for building interactive interfaces
- **TypeScript 5.8.3** - Type-safe JavaScript development
- **Vite 6.3.5** - Fast build tool and development server
- **React Router 7.6.2** - Client-side routing
- **Redux Toolkit 2.8.2** - State management with RTK Query for API calls
- **Tailwind CSS 4.1.10** - Utility-first CSS framework
- **Axios 1.10.0** - HTTP client for API requests

### Development Tools
- **ESLint** - Code linting and quality checks
- **Docker** - Containerization for consistent environments
- **Nginx** - Production web server

## System Requirements

- **Node.js:** 18.x or higher
- **npm:** 9.x or higher
- **Docker:** (optional) for containerized deployment
- **Modern web browser:** Chrome, Firefox, Safari, or Edge (latest versions)

## Running the Project Locally

### 1. Clone the Repository

```bash
git clone <repository-url>
cd sdu-chat-front
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
VITE_API_URL=https://chat-back.sdu.edu.kz/api
```

**Environment Variables Description:**
- `VITE_API_URL` - Backend API base URL for chat services

### 4. Start Development Server

```bash
npm run dev
```

The application will be available at `http://localhost:5173`

### 5. Build for Production

```bash
npm run build
```

The production-ready files will be generated in the `dist` directory.

### 6. Preview Production Build

```bash
npm run preview
```

## Running with Docker

### Development Mode

```bash
docker-compose up
```

The application will be available at `http://localhost:5173`

### Production Mode

```bash
docker build -f Dockerfile.prod -t sdu-chat-front:prod .
docker run -p 80:80 sdu-chat-front:prod
```

## Available Scripts

- `npm run dev` - Start development server with hot reload
- `npm run build` - Build production bundle
- `npm run preview` - Preview production build locally
- `npm run lint` - Run ESLint to check code quality

## Testing Instructions

Currently, this MVP does not include automated tests. To manually test the application:

1. **Authentication Flow:**
   - Navigate to `/login`
   - Complete the login process
   - Verify redirect to main chat interface

2. **Chat Functionality:**
   - Send a message and verify response
   - Create a new chat session
   - Switch between different chat sessions
   - Verify message history persistence

3. **Responsive Design:**
   - Test on desktop (1920x1080, 1366x768)
   - Test on tablet (768x1024)
   - Test on mobile (375x667, 414x896)

4. **Error Handling:**
   - Test with network disconnection
   - Verify error messages display correctly
   - Test token refresh on 401 errors

## Project Structure

```
sdu-chat-front/
├── public/                      # Static assets
│   └── vite.svg                # Vite logo
├── src/
│   ├── components/             # React components
│   │   ├── chat/              # Chat-related components
│   │   │   ├── AlertModal.tsx        # Alert/confirmation modals
│   │   │   ├── Chat.tsx              # Main chat container
│   │   │   ├── ChatHeader.tsx        # Chat header with title
│   │   │   ├── MessageBubble.tsx     # Individual message display
│   │   │   ├── MessageInput.tsx      # Message input field
│   │   │   ├── MessageList.tsx       # Message list container
│   │   │   ├── TextFormatter.tsx     # Text formatting utilities
│   │   │   └── WelcomeScreen.tsx     # Initial welcome screen
│   │   └── chat-side-bar/     # Sidebar components
│   │       ├── AccountInfo.tsx       # User account information
│   │       ├── ChatList.tsx          # List of chat sessions
│   │       ├── ChatSidebar.tsx       # Main sidebar container
│   │       ├── ConnectionStatus.tsx  # Connection status indicator
│   │       ├── CreateNewChat.tsx     # New chat creation button
│   │       └── SidebarHeader.tsx     # Sidebar header
│   ├── pages/                  # Page components
│   │   ├── ErrorPage.tsx      # 404 and error page
│   │   ├── LoginCallBackPage.tsx # OAuth callback handler
│   │   ├── LoginPage.tsx      # Login page
│   │   └── MainPage.tsx       # Main application page
│   ├── route/                  # Routing configuration
│   │   ├── AppRouter.tsx      # Main router setup
│   │   └── ProtectedRoute.tsx # Authentication guard
│   ├── services/               # API services
│   │   ├── auth/              # Authentication services
│   │   ├── chat/              # Chat API services
│   │   ├── baseApi.ts         # RTK Query base API with auth
│   │   └── baseTypes.ts       # Shared TypeScript types
│   ├── store/                  # Redux store
│   │   ├── authSlice.ts       # Authentication state
│   │   ├── chatSlice.ts       # Chat state
│   │   └── store.ts           # Store configuration
│   ├── main.tsx               # Application entry point
│   ├── main.css               # Global styles
│   └── vite-env.d.ts          # Vite type definitions
├── .dockerignore              # Docker ignore rules
├── .gitignore                 # Git ignore rules
├── Dockerfile                 # Development Docker image
├── Dockerfile.prod            # Production Docker image
├── docker-compose.yml         # Docker Compose configuration
├── eslint.config.js           # ESLint configuration
├── index.html                 # HTML entry point
├── nginx.conf                 # Nginx configuration for production
├── package.json               # Project dependencies
├── tsconfig.json              # TypeScript configuration
├── tsconfig.app.json          # App-specific TypeScript config
├── tsconfig.node.json         # Node-specific TypeScript config
└── vite.config.ts             # Vite configuration
```

### Key Directories

- **`src/components/`** - Reusable React components organized by feature
- **`src/pages/`** - Top-level page components for routing
- **`src/services/`** - API integration layer with RTK Query
- **`src/store/`** - Redux state management configuration
- **`src/route/`** - Application routing and navigation guards

## Additional Documentation

- [API Documentation](docs/API.md) - Backend API endpoints and integration
- [Deployment Guide](docs/DEPLOYMENT.md) - Production deployment instructions
- [Contributing Guidelines](docs/CONTRIBUTING.md) - How to contribute to the project
- [Architecture Overview](docs/ARCHITECTURE.md) - System design and architecture decisions

## Features

- ✅ Secure authentication with token refresh
- ✅ Real-time chat interface
- ✅ Multiple chat session management
- ✅ Conversation history
- ✅ Responsive design (mobile, tablet, desktop)
- ✅ Message formatting and display
- ✅ Connection status monitoring
- ✅ User account information display

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## License

This project is private and proprietary to SDU (Sdu Daryn University).

## Support

For issues, questions, or contributions, please contact the development team or create an issue in the repository.
