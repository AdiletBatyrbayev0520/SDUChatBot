# User Stories
# SDU AI Chatbot Platform

**Document Version:** 1.0  
**Last Updated:** December 19, 2025  
**Document Owner:** SDU ChatBot Development Team  
**Product Owner:** Maksut Gaitat, Director of Admission Committee

---

## Overview

This document contains user stories for the SDU AI Chatbot Platform MVP. Each story follows the standard format: "As a [role], I want to [action], so I can [result]." Stories are organized by user role and include measurable acceptance criteria that cover the full MVP scope.

---

## Table of Contents

1. [Prospective Student Stories](#prospective-student-stories)
2. [Current Student Stories](#current-student-stories)
3. [Parent/Guardian Stories](#parentguardian-stories)
4. [Faculty/Staff Stories](#facultystaff-stories)
5. [Administrator Stories](#administrator-stories)
6. [Guest User Stories](#guest-user-stories)

---

## Prospective Student Stories

### Story 1: Account Creation and Authentication

**As a** prospective student, **I want to** create an account using my Google credentials, **so I can** access personalized university information and save my conversation history.

**Acceptance Criteria:**
- System accepts Google OAuth authentication
- User profile is created with email, name, and basic information from Google
- User is redirected to main chat interface after successful login
- Session remains active for 24 hours
- User can access conversation history across sessions
- System displays welcome message for new users

---

### Story 2: Admission Requirements Inquiry

**As a** prospective student, **I want to** ask questions about admission requirements in my preferred language, **so I can** understand what documents and qualifications I need to apply.

**Acceptance Criteria:**
- System responds to admission-related questions in English, Kazakh, or Russian
- Response includes specific document requirements with deadlines
- System provides source attribution from official admission policies
- Response time is under 3 seconds for 95% of queries
- System maintains conversation context for follow-up questions
- User receives comprehensive checklist of required documents

---

### Story 3: Program Information Discovery

**As a** prospective student, **I want to** learn about specific academic programs and their requirements, **so I can** choose the right program for my career goals.

**Acceptance Criteria:**
- System provides detailed information about degree programs
- Response includes curriculum overview, duration, and career prospects
- System can compare multiple programs when requested
- Information is current and matches official university catalogs
- System provides contact information for program coordinators
- Response includes tuition fees and scholarship opportunities

---

### Story 4: Application Process Guidance

**As a** prospective student, **I want to** get step-by-step guidance through the application process, **so I can** submit my application correctly and on time.

**Acceptance Criteria:**
- System provides chronological application timeline
- Each step includes required documents and deadlines
- System offers application form links and submission instructions
- User receives reminders about important deadlines
- System explains application status tracking process
- Response includes contact information for application support

---

### Story 5: Campus and Facilities Information

**As a** prospective student, **I want to** learn about campus facilities and student life, **so I can** understand what to expect as an SDU student.

**Acceptance Criteria:**
- System provides information about dormitories, libraries, and recreational facilities
- Response includes campus maps and location details
- System describes student organizations and extracurricular activities
- Information includes dining options and campus services
- System provides virtual tour links or campus visit scheduling
- Response covers transportation and parking information

---

## Current Student Stories

### Story 6: Academic Policy Clarification

**As a** current student, **I want to** ask questions about academic policies and procedures, **so I can** understand my rights and responsibilities as a student.

**Acceptance Criteria:**
- System provides accurate information about grading policies
- Response covers attendance requirements and academic standing
- System explains academic leave and withdrawal procedures
- Information includes appeal processes and academic integrity policies
- System provides relevant form links and submission procedures
- Response includes contact information for academic advisors

---

### Story 7: Course Registration Assistance

**As a** current student, **I want to** get help with course registration and scheduling, **so I can** plan my academic semester effectively.

**Acceptance Criteria:**
- System provides course registration deadlines and procedures
- Response includes prerequisite information and course availability
- System explains add/drop policies and refund procedures
- Information covers course scheduling conflicts and solutions
- System provides academic calendar with important dates
- Response includes registration system access instructions

---

### Story 8: Student Services Navigation

**As a** current student, **I want to** find information about student services and support resources, **so I can** access help when needed.

**Acceptance Criteria:**
- System provides comprehensive list of student services
- Response includes counseling, health, and financial aid services
- System explains how to access each service with contact information
- Information covers service hours and location details
- System provides emergency contact information
- Response includes online service access instructions

---

### Story 9: Conversation History Management

**As a** current student, **I want to** view and manage my previous conversations, **so I can** reference past information and continue discussions.

**Acceptance Criteria:**
- User can view list of all previous chat sessions
- Each conversation shows title, date, and message count
- User can search conversations by keyword or date
- System maintains conversation context when resuming chats
- User can delete conversations they no longer need
- Conversation history is preserved across different devices

---

### Story 10: Multiple Chat Sessions

**As a** current student, **I want to** create separate chat sessions for different topics, **so I can** organize my inquiries and keep conversations focused.

**Acceptance Criteria:**
- User can create new chat sessions with custom titles
- System maintains separate context for each conversation
- User can switch between active conversations seamlessly
- Each session preserves its own message history
- System suggests relevant titles based on conversation content
- User can rename chat sessions after creation

---

## Parent/Guardian Stories

### Story 11: University Information Access

**As a** parent, **I want to** access university information in my preferred language, **so I can** understand the educational environment for my child.

**Acceptance Criteria:**
- System responds in Kazakh, Russian, English, Turkish, or German
- Response provides comprehensive university overview
- Information includes academic reputation and accreditation details
- System explains university values and educational philosophy
- Response covers safety and security measures on campus
- Information includes parent communication channels

---

### Story 12: Financial Information Inquiry

**As a** parent, **I want to** understand tuition costs and payment options, **so I can** plan financially for my child's education.

**Acceptance Criteria:**
- System provides current tuition fees by program
- Response includes all additional costs (housing, meals, books)
- System explains payment schedules and methods
- Information covers scholarship and financial aid opportunities
- System provides payment portal access instructions
- Response includes refund policies and procedures

---

### Story 13: Student Support Services

**As a** parent, **I want to** learn about student support services available to my child, **so I can** ensure they have access to necessary resources.

**Acceptance Criteria:**
- System describes academic support and tutoring services
- Response covers health and counseling services
- Information includes emergency procedures and contacts
- System explains parent notification policies
- Response covers student accommodation services
- Information includes career counseling and job placement support

---

## Faculty/Staff Stories

### Story 14: Administrative Template Access

**As a** faculty member, **I want to** access administrative forms and templates, **so I can** complete required paperwork efficiently.

**Acceptance Criteria:**
- System provides downloadable forms and templates
- Response includes completion instructions for each form
- System explains submission procedures and deadlines
- Information covers approval processes and timelines
- System provides contact information for administrative support
- Response includes digital signature and submission options

---

### Story 15: Policy and Procedure Information

**As a** faculty member, **I want to** access current university policies and procedures, **so I can** ensure compliance with institutional requirements.

**Acceptance Criteria:**
- System provides up-to-date policy documents
- Response includes policy effective dates and version numbers
- System explains policy changes and implementation timelines
- Information covers compliance requirements and reporting procedures
- System provides policy interpretation guidance
- Response includes contact information for policy clarification

---

### Story 16: Student Information Guidelines

**As a** faculty member, **I want to** understand guidelines for student information and support, **so I can** provide appropriate assistance to students.

**Acceptance Criteria:**
- System explains student privacy and confidentiality requirements
- Response covers appropriate student interaction guidelines
- Information includes referral procedures for student support services
- System provides emergency response procedures
- Response covers academic accommodation procedures
- Information includes reporting requirements for student issues

---

## Administrator Stories

### Story 17: System Usage Analytics

**As an** administrator, **I want to** view system usage statistics and analytics, **so I can** monitor platform performance and user engagement.

**Acceptance Criteria:**
- Dashboard displays daily, weekly, and monthly usage metrics
- System shows user registration and retention statistics
- Analytics include most common questions and response accuracy
- Dashboard displays system performance metrics (response time, uptime)
- System provides user satisfaction ratings and feedback
- Analytics can be exported for reporting purposes

---

### Story 18: Content Management

**As an** administrator, **I want to** manage the knowledge base content, **so I can** ensure information accuracy and relevance.

**Acceptance Criteria:**
- System allows content upload and synchronization from Google Drive
- Administrator can review and approve content updates
- System tracks content version history and changes
- Interface allows content categorization and tagging
- System provides content usage analytics and effectiveness metrics
- Administrator can schedule content reviews and updates

---

### Story 19: User Management

**As an** administrator, **I want to** manage user accounts and permissions, **so I can** control system access and maintain security.

**Acceptance Criteria:**
- System displays user list with registration dates and activity
- Administrator can activate, deactivate, or delete user accounts
- System allows role assignment (student, faculty, admin)
- Interface provides user activity logs and session history
- Administrator can reset user passwords and manage authentication
- System sends notifications for user account changes

---

### Story 20: System Health Monitoring

**As an** administrator, **I want to** monitor system health and performance, **so I can** ensure reliable service for all users.

**Acceptance Criteria:**
- Dashboard shows real-time system status and uptime
- System alerts administrator to performance issues or errors
- Monitoring includes AI service connectivity and response times
- Dashboard displays database performance and storage usage
- System provides error logs and troubleshooting information
- Administrator receives automated alerts for critical issues

---

## Guest User Stories

### Story 21: Basic University Information

**As a** guest user, **I want to** access basic university information without creating an account, **so I can** learn about SDU before deciding to apply.

**Acceptance Criteria:**
- System responds to general university questions without authentication
- Response includes basic program information and admission overview
- System provides contact information and website links
- Information covers university location and campus details
- System explains how to create an account for detailed information
- Response time remains under 3 seconds for basic queries

---

### Story 22: Language Selection

**As a** guest user, **I want to** select my preferred language for interaction, **so I can** understand information in my native language.

**Acceptance Criteria:**
- System offers language selection (English, Kazakh, Russian, Turkish, German)
- Interface elements display in selected language
- System maintains language preference throughout session
- Response content is provided in selected language
- System handles mixed-language queries appropriately
- Language selection is prominently displayed and easily changeable

---

### Story 23: Account Creation Guidance

**As a** guest user, **I want to** understand the benefits of creating an account, **so I can** decide whether to register for full access.

**Acceptance Criteria:**
- System explains account benefits (conversation history, personalized responses)
- Response includes simple account creation instructions
- System demonstrates additional features available to registered users
- Information covers data privacy and security measures
- System provides clear call-to-action for account creation
- Response explains authentication options (Google OAuth, developer login)

---

## Cross-Functional Stories

### Story 24: Multilingual Support

**As any** user, **I want to** interact with the system in my preferred language, **so I can** communicate effectively and understand responses clearly.

**Acceptance Criteria:**
- System automatically detects user language from input
- Response maintains consistent language throughout conversation
- System handles code-switching between languages appropriately
- Translation accuracy is verified by native speakers
- System provides language-specific cultural context when relevant
- User can change language preference at any time

---

### Story 25: Mobile Responsiveness

**As any** user, **I want to** access the chatbot from my mobile device, **so I can** get information while on the go.

**Acceptance Criteria:**
- Interface adapts to mobile screen sizes (320px to 768px)
- Touch interactions work smoothly on mobile devices
- Text remains readable without horizontal scrolling
- Chat interface is optimized for thumb navigation
- System performance remains consistent on mobile networks
- Mobile users can access all core functionality

---

### Story 26: Error Handling and Recovery

**As any** user, **I want to** receive helpful error messages when something goes wrong, **so I can** understand the issue and know how to proceed.

**Acceptance Criteria:**
- System provides clear, non-technical error messages
- Error messages include suggested actions for resolution
- System gracefully handles network connectivity issues
- User can retry failed actions without losing conversation context
- System provides alternative contact methods when service is unavailable
- Error messages are displayed in user's preferred language

---

### Story 27: Conversation Context Maintenance

**As any** user, **I want to** have the system remember our conversation context, **so I can** ask follow-up questions naturally without repeating information.

**Acceptance Criteria:**
- System maintains context for at least 10 previous message exchanges
- Follow-up questions receive contextually appropriate responses
- System can reference previous topics and answers in the conversation
- Context is preserved when user returns to conversation after break
- System handles context switches when user changes topics
- Context memory works consistently across different user sessions

---

### Story 28: Source Attribution and Transparency

**As any** user, **I want to** see the sources of information provided by the AI, **so I can** verify accuracy and access original documents.

**Acceptance Criteria:**
- System provides source document names for all factual responses
- Sources are clickable links when documents are publicly accessible
- System indicates confidence level in provided information
- User can request additional sources or clarification
- System distinguishes between official university sources and general information
- Source attribution is provided in user's preferred language

---

### Story 29: Performance and Reliability

**As any** user, **I want to** receive fast and reliable responses, **so I can** get information efficiently without delays.

**Acceptance Criteria:**
- System responds within 3 seconds for 95% of queries
- Service maintains 99.5% uptime during business hours
- System handles 100+ concurrent users without performance degradation
- Response quality remains consistent under load
- System provides status indicators during processing
- Backup systems activate automatically during service interruptions

---

### Story 30: Feedback and Improvement

**As any** user, **I want to** provide feedback on system responses, **so I can** help improve the service quality for everyone.

**Acceptance Criteria:**
- System provides thumbs up/down rating for each response
- User can submit detailed feedback with specific suggestions
- Feedback form is accessible and easy to use
- System acknowledges feedback submission with confirmation
- User can see how their feedback contributes to improvements
- Feedback is processed and reviewed by administrators regularly

---

## Story Prioritization

### High Priority (MVP Release)
- Stories 1-6: Core authentication and basic inquiry functionality
- Stories 9-10: Conversation management
- Stories 21-23: Guest user access
- Stories 24-29: Cross-functional requirements

### Medium Priority (Post-MVP)
- Stories 7-8: Advanced student services
- Stories 11-16: Parent and faculty features
- Story 30: Feedback system

### Low Priority (Future Releases)
- Stories 17-20: Administrative features
- Advanced analytics and reporting
- Integration with external systems

---

## Success Metrics

### User Engagement
- 80% of users complete their primary task successfully
- Average session duration of 5-10 minutes
- 70% of users return within 30 days

### System Performance
- 95% of responses delivered within 3 seconds
- 99.5% system uptime during business hours
- 90% user satisfaction rating

### Business Impact
- 60% reduction in manual consultation costs
- 50% decrease in repetitive support queries
- 85% accuracy rate in information provided

---

**Document Approval:**
- **Product Requirements:** Maksut Gaitat, Director of Admission Committee
- **Technical Feasibility:** Meraliyev Meraryslan, Head of Information Systems Department
- **User Experience Review:** SDU ChatBot Development Team
- **Next Review Date:** March 2026