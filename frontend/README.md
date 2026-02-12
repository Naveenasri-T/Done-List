# Forest Done Log - Frontend

Beautiful, elegant React UI for the Forest Done Log gamified task tracking app.

## Features

✨ **Elegant Design** - Clean, modern interface with forest theme
🌲 **Interactive Forest** - Visual representation of your accomplishments
📊 **Real-time Stats** - Track streaks, levels, and progress
🎨 **Smooth Animations** - Polished user experience
📱 **Responsive** - Works perfectly on desktop and mobile

## Quick Start

### 1. Install Dependencies

```bash
npm install
```

### 2. Start Development Server

```bash
npm run dev
```

The app will be available at `http://localhost:5173`

### 3. Build for Production

```bash
npm run build
```

## Project Structure

```
frontend/
├── src/
│   ├── components/      # Reusable UI components
│   │   ├── Navbar.jsx
│   │   ├── TaskForm.jsx
│   │   ├── ForestDisplay.jsx
│   │   └── StatsPanel.jsx
│   ├── pages/           # Main page components
│   │   ├── Login.jsx
│   │   ├── Register.jsx
│   │   ├── Dashboard.jsx
│   │   └── Profile.jsx
│   ├── App.jsx          # Main app component
│   ├── main.jsx         # Entry point
│   └── index.css        # Global styles
├── index.html
├── vite.config.js
└── package.json
```

## Design Philosophy

- **Simple & Clean** - No clutter, easy to navigate
- **Nature Theme** - Forest colors and tree emojis
- **Smooth UX** - Animated transitions and interactions
- **User-Friendly** - Intuitive interface, clear feedback

## Color Palette

- **Forest Dark**: `#1a3a2e` - Primary text
- **Forest Green**: `#2d5a3f` - Buttons, accents
- **Leaf Green**: `#6fbb8e` - Highlights
- **Cream**: `#f4f1e8` - Backgrounds
- **Gold**: `#f4d03f` - Special badges

## Key Features

### Dashboard
- Quick task entry with effort level selection
- Visual forest display of completed tasks
- Real-time statistics panel
- Today's progress tracking

### Profile
- User information management
- Bio and privacy settings
- Export data (JSON/CSV)
- Journey statistics

### Forest Visualization
- Trees grow based on task effort
- Recent accomplishments list
- Hover effects for details
- Beautiful animations

## Technologies

- **React 18** - UI framework
- **Vite** - Build tool and dev server
- **React Router** - Navigation
- **Axios** - API requests
- **CSS3** - Styling with animations

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## License

MIT
