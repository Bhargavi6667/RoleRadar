import React from 'react';
import { Card, CardContent, Typography, Box, Chip, Grid } from '@mui/material';
import { ShieldCheck, FileCheck, Layers, Sparkles } from 'lucide-react';

export default function EvidenceCard({ evidenceList = [] }) {
  const defaultEvidence = [
    {
      skill: 'Spring Boot',
      status: 'Strong',
      evidence: 'Developed enterprise RESTful APIs using Spring Boot, Spring Data JPA, and PostgreSQL with JWT token security.',
      source: 'Project: Pet Adoption Platform',
      confidence: 0.95
    },
    {
      skill: 'React',
      status: 'Strong',
      evidence: 'Engineered responsive single-page applications with state management, Vite bundling, and Material-UI components.',
      source: 'Project: RoleRadar UI',
      confidence: 0.92
    },
    {
      skill: 'Docker',
      status: 'Moderate',
      evidence: 'Created multi-stage Dockerfiles and orchestrated containers using docker-compose.',
      source: 'Experience: Development Workflow',
      confidence: 0.78
    },
    {
      skill: 'Kubernetes',
      status: 'Missing',
      evidence: 'No direct implementation or cluster management experience found in resume.',
      source: 'Unverified',
      confidence: 0.15
    }
  ];

  const items = evidenceList.length > 0 ? evidenceList : defaultEvidence;

  return (
    <Card sx={{
      background: 'rgba(32, 23, 20, 0.7)',
      border: '1px solid rgba(255, 255, 255, 0.08)',
      borderRadius: 3,
      backdropFilter: 'blur(10px)',
      boxShadow: '0 8px 32px 0 rgba(0, 0, 0, 0.36)'
    }}>
      <CardContent sx={{ p: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 3 }}>
          <Typography variant="h6" sx={{ fontWeight: 700, color: '#f8fafc', display: 'flex', alignItems: 'center', gap: 1 }}>
            <ShieldCheck size={20} color="#10b981" /> Evidence Verification
          </Typography>
          <Typography variant="caption" sx={{ color: '#94a3b8' }}>
            Claims grounded in resume text
          </Typography>
        </Box>

        <Grid container spacing={2}>
          {items.map((item, idx) => {
            const isStrong = item.status === 'Strong';
            const isMissing = item.status === 'Missing';
            return (
              <Grid item xs={12} key={idx}>
                <Box sx={{
                  p: 2,
                  borderRadius: 2,
                  backgroundColor: 'rgba(20, 13, 11, 0.6)',
                  border: `1px solid ${isStrong ? 'rgba(16, 185, 129, 0.2)' : isMissing ? 'rgba(239, 68, 68, 0.2)' : 'rgba(245, 158, 11, 0.2)'}`,
                  transition: 'all 0.2s ease',
                  '&:hover': {
                    backgroundColor: 'rgba(20, 13, 11, 0.9)',
                    borderColor: isStrong ? '#10b981' : isMissing ? '#ef4444' : '#f59e0b'
                  }
                }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5 }}>
                      <Typography variant="subtitle2" sx={{ fontWeight: 700, color: '#fff' }}>
                        {item.skill}
                      </Typography>
                      <Chip
                        size="small"
                        icon={<Layers size={12} />}
                        label={item.source}
                        sx={{ backgroundColor: 'rgba(249, 115, 22, 0.15)', color: '#fed7aa', fontSize: '0.7rem', height: 22 }}
                      />
                    </Box>
                    <Chip
                      size="small"
                      icon={<Sparkles size={12} />}
                      label={`${Math.round((item.confidence || 0.8) * 100)}% Confidence`}
                      sx={{
                        backgroundColor: isStrong ? 'rgba(16, 185, 129, 0.15)' : isMissing ? 'rgba(239, 68, 68, 0.15)' : 'rgba(245, 158, 11, 0.15)',
                        color: isStrong ? '#34d399' : isMissing ? '#f87171' : '#fbbf24',
                        fontWeight: 600,
                        fontSize: '0.72rem'
                      }}
                    />
                  </Box>
                  <Typography variant="body2" sx={{ color: '#94a3b8', fontStyle: 'italic', pl: 1, borderLeft: '2px solid rgba(255,255,255,0.1)' }}>
                    "{item.evidence}"
                  </Typography>
                </Box>
              </Grid>
            );
          })}
        </Grid>
      </CardContent>
    </Card>
  );
}
