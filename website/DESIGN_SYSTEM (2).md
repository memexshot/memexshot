# Lottie Lottery Design System

## Overview
This document outlines the design system and visual language for the Lottie Lottery decentralized application. It serves as a reference for maintaining consistency across all UI components, pages, and future features.

## Core Design Principles

### 1. Dark Theme Foundation
- Primary background: `bg-gradient-to-br from-gray-900 via-blue-900/20 to-gray-900`
- Card backgrounds: Glass morphism with `gradient-card` class
- Text hierarchy using gray shades

### 2. Gradient-First Approach
- Orange to blue gradients as primary visual elements
- Animated gradients for interactive elements
- Subtle gradient overlays for depth

### 3. Consistent Animation
- Pulse effects for live/active states
- Hover transformations for interactive elements
- Floating particles for visual interest

## Color Palette

### Primary Colors
```css
--primary-orange: #FF6B35;
--primary-orange-dark: #E85A2C;
--primary-orange-light: #FF8554;

--primary-blue: #1E3A5F;
--primary-blue-dark: #152A47;
--primary-blue-light: #2C4C7D;
```

### Background Colors
```css
--bg-dark: #0A0E1B;
--bg-card: #131825;
--bg-card-hover: #1A2232;
```

### Text Colors
```css
--text-primary: #E5E7EB;
--text-secondary: #9CA3AF;
--text-muted: #6B7280;
```

### Accent Colors
```css
--accent-orange: #FFA366;
--accent-blue: #4B6B9A;
--success: #10B981;
--warning: #F59E0B;
--error: #EF4444;
```

## Typography

### Headers
```jsx
// Main page titles
<h1 className="text-4xl font-bold bg-gradient-to-r from-orange-500 to-blue-500 bg-clip-text text-transparent mb-1">
  Title
</h1>
<p className="text-xs text-gray-500">Subtitle</p>

// Card titles (Prize Pool style)
<h2 className="text-3xl font-bold gradient-text mb-6">Card Title</h2>

// Section titles
<h3 className="text-xl font-bold gradient-text mb-4">Section Title</h3>
```

### Body Text
- Primary text: `text-white` or `text-gray-300`
- Secondary text: `text-gray-400`
- Muted text: `text-gray-500`
- Small text: `text-xs` or `text-sm`

## Component Patterns

### 1. Page Layout
```jsx
<div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900/20 to-gray-900">
  <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    {/* Content */}
  </div>
</div>
```

### 2. Card Component (Prize Pool Pattern)
```jsx
<div className="relative overflow-hidden">
  {/* Background Animation */}
  <div className="absolute inset-0 bg-gradient-to-br from-orange-500/10 via-transparent to-blue-500/10 animate-pulse" />
  
  {/* Main Content */}
  <div className="relative gradient-card rounded-2xl p-8">
    <h2 className="text-3xl font-bold gradient-text mb-6">Title</h2>
    {/* Card content */}
  </div>
</div>
```

### 3. Primary Button (Create deLot Style)
```jsx
<button className="relative px-6 py-2.5 rounded-lg transition-all duration-300 font-semibold transform hover:scale-105">
  {/* Animated gradient background */}
  <div className="absolute inset-0 bg-gradient-to-r from-orange-600 via-orange-500 to-blue-600 rounded-lg opacity-100 animate-gradient-x"></div>
  
  {/* Glow effect */}
  <div className="absolute inset-0 bg-gradient-to-r from-orange-600 to-blue-600 rounded-lg blur-lg opacity-50 animate-pulse"></div>
  
  {/* Button content */}
  <div className="relative flex items-center gap-2 text-white">
    <svg className="w-5 h-5 animate-pulse" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M12 4v16m8-8H4" />
    </svg>
    <span>Button Text</span>
  </div>
</button>
```

### 4. Secondary Button
```jsx
<button className="px-5 py-2.5 rounded-lg transition-all duration-200 font-medium bg-gray-800/50 text-gray-300 hover:bg-gray-700/50 hover:text-white">
  Button Text
</button>
```

### 5. Status Badges
```jsx
// Live status
<div className="inline-flex items-center space-x-2 bg-gray-800/50 backdrop-blur-sm px-3 py-1.5 rounded-full border border-green-500/30">
  <div className="w-2 h-2 bg-gradient-to-r from-green-400 to-emerald-400 rounded-full animate-pulse" />
  <span className="text-xs font-semibold text-green-400 uppercase tracking-wider">LIVE</span>
</div>

// Ended status
<div className="inline-flex items-center space-x-2 bg-gray-800/50 backdrop-blur-sm px-3 py-1.5 rounded-full border border-red-500/30">
  <div className="w-2 h-2 bg-gradient-to-r from-red-400 to-rose-400 rounded-full" />
  <span className="text-xs font-semibold text-red-400 uppercase tracking-wider">ENDED</span>
</div>
```

### 6. Input Fields
```jsx
<input
  type="text"
  className="w-full px-4 py-3 bg-gray-800/50 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-orange-500 transition-colors"
  placeholder="Enter value"
/>
```

### 7. Stats Display
```jsx
<div className="bg-gray-800/50 backdrop-blur-sm rounded-xl p-3 border border-gray-700/50">
  <p className="text-xs text-gray-400 mb-1">Label</p>
  <p className="text-lg font-bold gradient-text">Value</p>
</div>
```

## Utility Classes

### Gradients
```css
/* Orange-blue gradient for text */
.gradient-text {
  background: linear-gradient(135deg, var(--primary-orange) 0%, var(--accent-blue) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* Card background with glass effect */
.gradient-card {
  background: linear-gradient(135deg, rgba(255, 107, 53, 0.1) 0%, rgba(30, 58, 95, 0.1) 100%);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 107, 53, 0.2);
}

/* Animated gradient */
.animate-gradient-x {
  background-size: 200% 200%;
  animation: gradient-x 3s ease infinite;
}
```

### Animations
```css
/* Floating animation */
.animate-float {
  animation: float 6s ease-in-out infinite;
}

/* Pulse animation (built-in Tailwind) */
.animate-pulse

/* Scale on hover */
.hover:scale-105
```

## Common Patterns

### 1. Page Headers
- Use gradient text for main titles
- Keep subtitles small and muted
- Center align for landing pages
- Left align for detail pages

### 2. Card Hierarchy
- Primary cards: Use Prize Pool pattern with animated background
- Secondary cards: Simple gradient-card without animation
- Nested cards: Use `bg-gray-800/30` or `bg-gray-800/50`

### 3. Interactive Elements
- All clickable elements should have hover states
- Primary actions use animated gradient buttons
- Secondary actions use subtle gray buttons
- Links use `text-gray-400 hover:text-orange-400` pattern

### 4. Loading States
```jsx
<div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
```

### 5. Empty States
- Use centered layout
- Include an icon
- Provide helpful message
- Add action button if applicable

## Spacing Guidelines

### Padding
- Page container: `py-8`
- Card padding: `p-8` for large cards, `p-6` for medium, `p-4` for small
- Button padding: `px-6 py-2.5` for primary, `px-4 py-2` for secondary

### Margins
- Page sections: `mb-8`
- Card titles: `mb-6`
- Form groups: `mb-4`
- Small elements: `mb-2`

## Responsive Design

### Breakpoints
- Mobile: Default
- Tablet: `md:` (768px)
- Desktop: `lg:` (1024px)

### Grid Layouts
```jsx
// Two column on desktop, stack on mobile
<div className="grid lg:grid-cols-2 gap-8">

// Three column on desktop, stack on mobile
<div className="grid lg:grid-cols-3 gap-6">

// Four column responsive
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
```

## Best Practices

1. **Consistency**: Always use the established patterns
2. **Hierarchy**: Use size, color, and spacing to create clear hierarchy
3. **Accessibility**: Ensure sufficient color contrast
4. **Performance**: Limit animations on lower-end devices
5. **Feedback**: Provide visual feedback for all interactions

## Component Library Reference

### Navigation
- Header: Sticky top navigation with gradient logo and center nav buttons
- Active state: Use `gradient-border` class for active nav items

### Cards
- Lottery Card: Interactive card with hover effects
- Stats Card: Simple display card with gradient text
- Prize Pool Card: Premium card with animated background

### Forms
- Create Form: Multi-section form with validation
- Preview Card: Live preview with gradient styling

### Modals
- Use backdrop blur
- Center positioning
- Smooth transitions
- Click outside to close

## Future Considerations

When adding new features or components:

1. Check if existing patterns can be reused
2. Maintain the gradient-first aesthetic
3. Ensure animations are smooth and purposeful
4. Test on both light and dark backgrounds
5. Consider mobile-first design
6. Keep accessibility in mind

This design system should be treated as a living document and updated as new patterns emerge or existing ones evolve.