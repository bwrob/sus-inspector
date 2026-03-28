# Product Guidelines: sus-inspector

## Design & Aesthetics
### Visual Style
- **Modern and Slick:** Leverage contemporary TUI (Terminal User Interface) features, including shadows, gradients, and subtle animations, to create a polished and high-end feel.
- **Consistent Naming:** Use the 'sus' prefix or short, punchy names consistently throughout the UI and API to reinforce the brand identity.

## User Experience (UX)
### Core Principles
- **Keyboard Dominant Workflow:** Every action and navigation command must have a clearly defined keyboard shortcut to ensure maximum speed and efficiency for power users.
- **Progressive Disclosure Rollout:** Hide complexity by default. Reveal deeper details and nested structures only when explicitly requested by the user to avoid information overload.
- **Playful Introspection Tone:** Maintain a sense of playful introspection (e.g., "suspicious objects," "poking," "searching") while ensuring the tool remains highly functional and reliable.

## Content & Communication
### Prose Style
- **Minimal and Direct:** Documentation and UI labels should be short, punchy, and free of unnecessary fluff. Focus on delivering critical information efficiently.
- **Technical Precision:** While the tone is playful, the terminology must remain precise and accurate to provide clear value to the developer.

## Implementation Guidelines
### Performance
- **Zero-Friction Startup:** The TUI should initialize almost instantly, ensuring no delay between the user calling `sus` and seeing the interface.
- **Lazy Evaluation:** Only parse and render what is currently visible or requested to maintain high performance even with massive data structures.
