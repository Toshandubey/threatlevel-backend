# Design System Document: Technical Noir Editorial

## 1. Overview & Creative North Star: "The Digital Forensic"
The Creative North Star for this design system is **The Digital Forensic**. We are moving away from the "SaaS Dashboard" trope and toward a high-end, 90s-inspired tech editorial aesthetic. Imagine a high-budget cinematic hacker interface met with the precision of a Swiss typography specimen. 

This system breaks the "template" look through **Extreme Brutalism**—utilizing hard edges (0px border radius), intentional asymmetry, and a monochromatic foundation punctuated by "Aggressive Muted Crimson" and "Icy Mint." We prioritize technical density and data-rich environments while maintaining an elite, minimalist atmosphere.

---

## 2. Colors: Tonal Depth & High-Stakes Signaling
Our palette is rooted in the shadows. We use varying levels of charcoal and slate to create a sense of infinite depth, ensuring the interface feels like a specialized tool, not a consumer app.

### The Palette (Material Design Mapping)
- **Background & Surfaces:** 
  - `surface` (#10141a): The void. Used for the primary canvas.
  - `surface_container_lowest` (#0a0e14): Used for deep-set data wells or "recessed" areas.
  - `surface_container_highest` (#31353c): Used for active overlays or elevated panels.
- **Signal Colors:**
  - `primary_container` (#990000): **Aggressive Muted Crimson.** Reserved exclusively for "PHISHING DETECTED" and critical system breaches.
  - `secondary` (#77dc7a): **Icy Mint Green.** Used for "CLEAN" status and successful validations.
- **Accents:**
  - `tertiary` (#c8c6c5): A muted slate for non-essential technical meta-data.

### The "No-Line" Rule
**Explicit Instruction:** Do not use 1px solid borders to section content. Boundaries must be defined through background color shifts. To separate a sidebar from a main feed, transition from `surface` to `surface_container_low`. 

### Surface Hierarchy & Nesting
Treat the UI as a series of physical, light-absorbing layers. 
- **The Stack:** Place a `surface_container_highest` card atop a `surface_container_low` section. The change in hex value provides all the separation necessary.
- **The "Glass & Gradient" Rule:** For floating technical modals, use `surface_bright` with a 60% opacity and a `20px` backdrop-blur. Apply a subtle linear gradient (from `surface_variant` to `surface`) to headers to give them a "machined metal" feel.

---

## 3. Typography: The Tension of Two Worlds
We use a high-contrast pairing: a clean, authoritative Sans-Serif for headers and a rigorous Monospace for the "truth"—the data.

- **Headlines (Inter):** Bold, tight tracking (-0.02em), and uppercase for labels. These convey the "Editorial" authority.
- **Data (Space Grotesk):** While technically a sans, its "monospaced-feel" and geometric rigour handle the technical strings, email headers, and timestamps.

**Hierarchy Strategy:**
- **Display LG (Inter, 3.5rem):** Use for "threat levels" or large numerical data.
- **Title SM (Space Grotesk, 1rem):** The workhorse for technical logs and email metadata.
- **Label SM (Space Grotesk, 0.6875rem):** Used for micro-annotations, often in 50% opacity for a "low-level system" feel.

---

## 4. Elevation & Depth: Tonal Layering
In a "Digital Forensic" environment, traditional shadows are too soft. We use **Tonal Layering** to create hierarchy.

- **The Layering Principle:** Instead of shadows, "lift" an object by moving it up the `surface-container` tier. 
- **Ambient Shadows:** Only use shadows for "floating" diagnostic windows. Use a large blur (40px) at 8% opacity using the `on_surface` color. It should feel like a faint glow/void, not a drop shadow.
- **The "Ghost Border" Fallback:** If high-density data requires containment, use `outline_variant` at **15% opacity**. It should be barely perceptible—a "whisper" of a line.
- **Zero Roundness:** Every element is `0px` radius. Hard corners imply precision, technicality, and a lack of "consumer fluff."

---

## 5. Components: Precision Primitive Styling

### Buttons
- **Primary (Crimson):** Background: `primary_container`. Text: `on_primary_container`. 0px radius. No gradient. 
- **Secondary (Technical):** Background: `surface_container_high`. Ghost Border (15% opacity).
- **State Change:** On hover, shift the background color by exactly one tier (e.g., `surface_container_high` becomes `surface_bright`).

### Technical Chips
- **Status Chips:** No background. Use a `2px` left-side border of the signal color (`primary_container` for threat, `secondary` for clean) and monospaced text.

### Inputs & Terminal Fields
- **Fields:** Background: `surface_container_lowest`. Forbid rounded corners. 
- **Focus State:** Instead of a blue glow, use a 1px `secondary` (Mint) border on the bottom only.

### Cards & Lists
- **No Dividers:** Use `16px` or `24px` of vertical white space to separate email entries. If distinction is needed, alternate background colors between `surface` and `surface_container_low`.

### Specialized Component: "The Threat Meter"
A custom component for this system: A horizontal bar using `surface_container_highest` as the track, with a segmented (not smooth) progress bar in `primary_container` to indicate threat probability.

---

## 6. Do's and Don'ts

### Do:
- **Do** lean into asymmetry. A 3-column layout where the columns have varying widths (e.g., 15% / 60% / 25%) feels more "technical" than a standard grid.
- **Do** use `0.5 opacity` for secondary technical strings to create visual hierarchy within data-heavy views.
- **Do** use "Icy Mint" (`secondary`) sparingly. It is a reward for a clean system; overusing it dilutes the moody atmosphere.

### Don't:
- **Don't** ever use a border-radius. Even `2px` ruins the cinematic, 90s tech vibe.
- **Don't** use standard blue for links. Links should be `on_surface` with an underline, or "Icy Mint."
- **Don't** use icons with rounded "bubbly" profiles. Use sharp, thin-stroke (1px) technical icons.
- **Don't** use "Information" blues. If it's not a threat or clean, keep it grayscale.