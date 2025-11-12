# Executive Summary

Nomi is a technical learning project that provides a **reusable architectural template** for building modern full-stack applications with React and Python. The project demonstrates enterprise-grade patterns (server-side OAuth2, BFF architecture, session-based security, single-server deployment) in a realistic but manageable context - complex enough to prove real-world patterns, simple enough to understand and adapt for future projects.

The application uses a familiar todo list domain intentionally - not to compete with existing products, but to allow complete focus on architectural patterns without getting lost in complex requirements discovery. By the end, you'll have a reference implementation that answers "how do I properly structure this?" for authentication, state management, API design, and deployment in a React + Python stack.

## What Makes This Special

**The "Goldilocks" Architectural Template**

Most code examples are either:
- **Too trivial:** "Hello World" tutorials that don't demonstrate real authentication, state management, or deployment
- **Too complex:** Enterprise codebases with overwhelming abstractions, microservices, and infrastructure that obscure the core patterns

Nomi sits in the sweet spot - **just right complexity**:
- Real EntraID authentication with maximum security (server-side OAuth2, HTTP-only cookies, zero token exposure)
- Production-ready patterns (BFF architecture, proper state management, session handling)
- Single-server deployment that eliminates CORS complexity while remaining production-viable
- Clean separation of concerns without over-engineering
- Fully functional application that can be deployed, used, and shown to others

**The magic moment:** Opening the codebase 6 months from now when starting a new project and thinking "I know exactly how to structure this because I proved it in Nomi" - then copying architectural patterns with confidence instead of second-guessing or over-Googling.

---
