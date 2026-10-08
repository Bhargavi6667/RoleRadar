import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme, CssBaseline, Box, Typography, Container } from '@mui/material';
import Navbar from './components/Navbar';
import NetworkBackground from './components/NetworkBackground';
import Welcome from './pages/Welcome';
import UploadResume from './pages/UploadResume';
import Results from './pages/Results';
import Interview from './pages/Interview';
import { BRAND } from './config/brand';

const darkTheme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#06b6d4', // Cyan
      light: '#22d3ee',
      dark: '#0891b2',
    },
    secondary: {
      main: '#3b82f6', // Blue
      light: '#60a5fa',
      dark: '#2563eb',
    },
    background: {
      default: 'transparent',
      paper: '#0a3a40',
    },
    text: {
      primary: '#f8fafc',
      secondary: '#94a3b8',
    },
  },
  typography: {
    fontFamily: '"Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
    h4: { fontWeight: 800 },
    h5: { fontWeight: 700 },
    h6: { fontWeight: 700 },
  },
  shape: {
    borderRadius: 12,
  },
});

export default function App() {
  return (
    <ThemeProvider theme={darkTheme}>
      <CssBaseline />
      <NetworkBackground />
      <Router>
        <Box sx={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
          <Navbar />
          <Box sx={{ flex: 1 }}>
            <Routes>
              <Route path="/" element={<Welcome />} />
              <Route path="/upload" element={<UploadResume />} />
              <Route path="/results" element={<Results />} />
              <Route path="/interview" element={<Interview />} />
            </Routes>
          </Box>
          <Box component="footer" sx={{ py: 3, borderTop: '1px solid rgba(255,255,255,0.06)', textAlign: 'center', backgroundColor: '#021215' }}>
            <Container maxWidth="xl">
              <Typography variant="body2" sx={{ color: '#64748b' }}>
                {BRAND.name} &copy; 2026 — Resume analysis, role matching and job openings in one place.
              </Typography>
            </Container>
          </Box>
        </Box>
      </Router>
    </ThemeProvider>
  );
}