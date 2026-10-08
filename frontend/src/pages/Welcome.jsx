import React from 'react';
import { Container, Box, Typography, Button, Grid, Card, CardContent, Chip } from '@mui/material';
import { Link } from 'react-router-dom';
import { UploadCloud, Sparkles, Target, Lightbulb, Building2, ArrowRight } from 'lucide-react';
import { BRAND } from '../config/brand';

const STEPS = [
  { icon: UploadCloud, color: '#38bdf8', title: '1. Upload your resume', text: 'Drop in your resume as a PDF. Nothing else to fill in.' },
  { icon: Sparkles, color: '#ec4899', title: '2. Click Analyze', text: 'We read your skills and experience and compare them with 13 job families.' },
  { icon: Target, color: '#10b981', title: '3. See your best-fit role', text: 'Get a score for roles like Frontend or Sales, ranked from best to weakest match.' },
  { icon: Lightbulb, color: '#f59e0b', title: '4. Improve and apply', text: 'Get specific suggestions, then browse companies hiring for your matching roles.' },
];

const ROLES = [
  'Frontend', 'Backend', 'Full Stack', 'DevOps / Cloud', 'Data / ML', 'Mobile', 'QA / Testing',
  'UI / UX', 'Sales', 'Digital Marketing', 'HR', 'Finance', 'Customer Support',
];

export default function Welcome() {
  return (
    <Container maxWidth="lg" sx={{ py: { xs: 5, md: 9 } }}>
      {/* Hero */}
      <Box sx={{ textAlign: 'center', maxWidth: 820, mx: 'auto', mb: 8 }}>
        <Box sx={{
          width: 72, height: 72, mx: 'auto', mb: 3, borderRadius: 3,
          background: 'linear-gradient(135deg, #f97316 0%, #ec4899 100%)',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          boxShadow: '0 0 40px rgba(249, 115, 22, 0.55)',
        }}>
          <Target size={38} color="#fff" />
        </Box>
        <Typography variant="overline" sx={{ color: '#fb923c', fontWeight: 700, letterSpacing: 2 }}>
          Welcome to {BRAND.name}
        </Typography>
        <Typography variant="h3" sx={{ fontWeight: 800, color: '#fff', letterSpacing: -1, mt: 1, mb: 2, fontSize: { xs: '2.1rem', md: '3rem' } }}>
          Find the role your resume is built for
        </Typography>
        <Typography variant="h6" sx={{ color: '#94a3b8', fontWeight: 400, mb: 4, lineHeight: 1.6 }}>
          Upload your resume and see how well it fits roles like Frontend or Sales, what to fix,
          and which companies are hiring for them.
        </Typography>
        <Button
          component={Link}
          to="/upload"
          variant="contained"
          size="large"
          endIcon={<ArrowRight size={20} />}
          sx={{
            px: 5, py: 1.6, borderRadius: 3, textTransform: 'none', fontWeight: 700, fontSize: '1.1rem',
            background: 'linear-gradient(135deg, #f97316 0%, #ec4899 100%)',
            boxShadow: '0 6px 28px rgba(249, 115, 22, 0.5)',
            '&:hover': { background: 'linear-gradient(135deg, #ea580c 0%, #db2777 100%)' },
          }}
        >
          Get Started
        </Button>
      </Box>

      {/* How it works */}
      <Typography variant="h5" sx={{ fontWeight: 800, color: '#fff', textAlign: 'center', mb: 3 }}>
        How it works
      </Typography>
      <Grid container spacing={3} sx={{ mb: 7 }}>
        {STEPS.map(({ icon: Icon, color, title, text }) => (
          <Grid item xs={12} sm={6} md={3} key={title}>
            <Card sx={{ height: '100%', background: 'rgba(32, 23, 20, 0.7)', border: '1px solid rgba(255,255,255,0.08)', borderRadius: 3 }}>
              <CardContent sx={{ p: 3 }}>
                <Box sx={{ width: 44, height: 44, borderRadius: 2, mb: 2, backgroundColor: `${color}22`, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                  <Icon size={22} color={color} />
                </Box>
                <Typography variant="subtitle1" sx={{ fontWeight: 700, color: '#f8fafc', mb: 0.5 }}>{title}</Typography>
                <Typography variant="body2" sx={{ color: '#94a3b8' }}>{text}</Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Roles covered */}
      <Box sx={{ textAlign: 'center' }}>
        <Typography variant="subtitle1" sx={{ color: '#cbd5e1', fontWeight: 600, mb: 2, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 1 }}>
          <Building2 size={18} color="#fb923c" /> Roles we match you against
        </Typography>
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, justifyContent: 'center' }}>
          {ROLES.map((r) => (
            <Chip key={r} label={r} sx={{ backgroundColor: 'rgba(249, 115, 22, 0.12)', color: '#ffedd5', border: '1px solid rgba(249, 115, 22, 0.25)', fontWeight: 600 }} />
          ))}
        </Box>
      </Box>
    </Container>
  );
}
