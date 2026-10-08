import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Box,
  Container,
  Chip,
  Tooltip
} from '@mui/material';
import {
  Target,
  Upload,
  BarChart3,
  Home,
  MessageSquare,
  CheckCircle2,
  AlertCircle
} from 'lucide-react';
import { healthApi } from '../services/api';
import { BRAND } from '../config/brand';

export default function Navbar() {
  const location = useLocation();
  const [backendUp, setBackendUp] = useState(null);

  useEffect(() => {
    healthApi.check()
      .then(() => setBackendUp(true))
      .catch(() => setBackendUp(false));
  }, []);

  const navItems = [
    { label: 'Welcome', path: '/', icon: Home },
    { label: 'Upload Resume', path: '/upload', icon: Upload },
    { label: 'Results', path: '/results', icon: BarChart3 },
    { label: 'Interview Prep', path: '/interview', icon: MessageSquare },
  ];

  return (
    <AppBar position="sticky" sx={{ background: 'rgba(20, 13, 11, 0.85)', backdropFilter: 'blur(12px)', borderBottom: '1px solid rgba(255,255,255,0.08)' }}>
      <Container maxWidth="xl">
        <Toolbar disableGutters sx={{ display: 'flex', justifyContent: 'space-between', py: 1 }}>
          {/* Logo */}
          <Box component={Link} to="/" sx={{ display: 'flex', alignItems: 'center', gap: 1.5, textDecoration: 'none', color: 'inherit' }}>
            <Box sx={{
              width: 40,
              height: 40,
              borderRadius: 2,
              background: 'linear-gradient(135deg, #f97316 0%, #ec4899 100%)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              boxShadow: '0 0 20px rgba(249, 115, 22, 0.5)'
            }}>
              <Target size={24} color="#fff" />
            </Box>
            <Box>
              <Typography variant="h6" sx={{ fontWeight: 800, letterSpacing: -0.5, lineHeight: 1.1, background: 'linear-gradient(90deg, #fff, #cbd5e1)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
                {BRAND.first}<Box component="span" sx={{ color: '#fb923c', WebkitTextFillColor: '#fb923c' }}>{BRAND.second}</Box>
              </Typography>
              <Typography variant="caption" sx={{ color: '#94a3b8', fontSize: '0.68rem', letterSpacing: 0.5 }}>
                {BRAND.tagline}
              </Typography>
            </Box>
          </Box>

          {/* Nav links */}
          <Box sx={{ display: { xs: 'none', md: 'flex' }, gap: 1 }}>
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = location.pathname === item.path;
              return (
                <Button
                  key={item.path}
                  component={Link}
                  to={item.path}
                  startIcon={<Icon size={18} />}
                  sx={{
                    px: 2,
                    py: 1,
                    borderRadius: 2,
                    color: isActive ? '#fff' : '#94a3b8',
                    backgroundColor: isActive ? 'rgba(249, 115, 22, 0.15)' : 'transparent',
                    border: isActive ? '1px solid rgba(249, 115, 22, 0.3)' : '1px solid transparent',
                    textTransform: 'none',
                    fontWeight: 600,
                    '&:hover': {
                      backgroundColor: 'rgba(255, 255, 255, 0.05)',
                      color: '#fff'
                    }
                  }}
                >
                  {item.label}
                </Button>
              );
            })}
          </Box>

          {/* System Status */}
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Tooltip title={backendUp ? "Spring Boot & AI Service connected" : "Backend connecting..."}>
              <Chip
                icon={backendUp ? <CheckCircle2 size={14} color="#10b981" /> : <AlertCircle size={14} color="#f59e0b" />}
                label={backendUp ? "System Live" : "Connecting..."}
                size="small"
                sx={{
                  backgroundColor: backendUp ? 'rgba(16, 185, 129, 0.12)' : 'rgba(245, 158, 11, 0.12)',
                  color: backendUp ? '#34d399' : '#fbbf24',
                  border: `1px solid ${backendUp ? 'rgba(16, 185, 129, 0.25)' : 'rgba(245, 158, 11, 0.25)'}`,
                  fontWeight: 600,
                  fontSize: '0.75rem'
                }}
              />
            </Tooltip>
          </Box>
        </Toolbar>
      </Container>
    </AppBar>
  );
}
