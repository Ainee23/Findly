================================================================================
                              FINDLY PROJECT README
================================================================================

Welcome to the Findly Project! This project is a robust, modular Django web 
application focused on item tracking, user engagement, and messaging, built 
with a beautiful modern UI consisting of Tailwind CSS, Inter Font, and 
Bootstrap Icons.

This file serves as a quick guide to the core components of the project.

--------------------------------------------------------------------------------
1. PROJECT APPS AND STRUCTURE
--------------------------------------------------------------------------------
The project is organized into several modular Django apps. Below is a summary 
of each core app and its purpose:

- accounts/
  Handles all user authentication models and views. It uses a custom User 
  model where the primary login identifier is an email address rather than 
  a standard username. Manages login, registration, and user profiles.

- items/
  The core application for item management. Users can browse items, search 
  for specific listings, list their own items, and submit claim requests.

- messaging/
  A robust chat engine enabling direct user-to-user communication. It 
  features a fully responsive WhatsApp-style UI. 
  Key Features:
    * Real-time conversational interface with speech bubbles.
    * Users can cleanly edit their sent messages.
    * Users can delete their sent messages natively without page reloads.

- notifications/
  A centralized alerting system. Delivers dynamically rendered notification 
  cards to users regarding new messages, item claims, system alerts, and 
  other important events.

- dashboard/
  Provides comprehensive overview panels indicating recent activity. It features
  interactive metrics for standard users (their items, active chats) and 
  higher-level system overviews for administrators.

- reviews/
  A system allowing users to leave feedback, ratings, and comments, 
  fostering continuous trust and safety on the platform.

- qr/
  Integrates QR code generation and scanning directly into the application, 
  allowing seamless tracking and identification of physical items or profiles.

- ai/
  A dedicated application for AI-powered features (e.g., smart suggestions, 
  computational views, deep integrations).

- core/
  Contains the foundational templates and fallback views, encompassing standard 
  site logic and core routing behaviors that span multiple models.

--------------------------------------------------------------------------------
2. UI / UX DESIGN PRINCIPLES
--------------------------------------------------------------------------------
* The design uses a unified "TheyMakeDesign" soft, airy aesthetic.
* Tailwind CSS is the primary styling engine via CDN (`cdn.tailwindcss.com`), 
  leveraging utility-first class application.
* Dark Mode and Light Mode are fully supported locally via local storage and 
  system preference detection (`user-preference`).
* Bootstrap Icons are integrated directly into the DOM (e.g., `bi-chat`).
* Dynamic JavaScript features (Edit/Delete modals) utilize asynchronous 
  JSON Fetch API requests without complex dependencies.

--------------------------------------------------------------------------------
3. DEVELOPMENT SETUP COMMANDS
--------------------------------------------------------------------------------
To run the project locally, navigate to the `Findly` directory containing 
`manage.py` and run:

    # 1. Apply any pending database configurations
    python manage.py makemigrations
    python manage.py migrate

    # 2. Start the local development server
    python manage.py runserver

Enjoy developing Findly! If you need to make new structural changes, review 
`Findly/settings.py` for standard configurations.
