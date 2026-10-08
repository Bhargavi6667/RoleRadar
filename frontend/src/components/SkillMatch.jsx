import React from 'react';
import { Card, CardContent, Typography, Box, LinearProgress, Chip } from '@mui/material';
import { Cpu, CheckCircle2, AlertTriangle, XCircle } from 'lucide-react';

export default function SkillMatch({ skills = [] }) {
  const defaultSkills = [
    { name: 'Java', score: 95, status: 'Strong' },
    { name: 'Spring Boot', score: 90, status: 'Strong' },
    { name: 'React', score: 88, status: 'Strong' },
    { name: 'PostgreSQL / SQL', score: 84, status: 'Strong' },
    { name: 'Docker', score: 62, status: 'Moderate' },
    { name: 'Kubernetes', score: 25, status: 'Missing' },
    { name: 'AWS Cloud', score: 20, status: 'Missing' },
  ];

  const skillList = skills.length > 0 ? skills : defaultSkills;

  const getStatusChip = (status) => {
    switch (status) {
      case 'Strong':
        return (
          <Chip
            size="small"
            icon={<CheckCircle2 size={12} color="#10b981" />}
            label="Strong Evidence"
            sx={{ backgroundColor: 'rgba(16, 185, 129, 0.12)', color: '#34d399', fontWeight: 600, fontSize: '0.72rem' }}
          />
        );
      case 'Moderate':
      case 'Inferred':
        return (
          <Chip
            size="small"
            icon={<AlertTriangle size={12} color="#f59e0b" />}
            label="Moderate / Inferred"
            sx={{ backgroundColor: 'rgba(245, 158, 11, 0.12)', color: '#fbbf24', fontWeight: 600, fontSize: '0.72rem' }}
          />
        );
      default:
        return (
          <Chip
            size="small"
            icon={<XCircle size={12} color="#ef4444" />}
            label="Missing Requirement"
            sx={{ backgroundColor: 'rgba(239, 68, 68, 0.12)', color: '#f87171', fontWeight: 600, fontSize: '0.72rem' }}
          />
        );
    }
  };

  const getBarColor = (score) => {
    if (score >= 80) return '#10b981';
    if (score >= 50) return '#f59e0b';
    return '#ef4444';
  };

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
            <Cpu size={20} color="#fb923c" /> Semantic Skill Matching
          </Typography>
          <Typography variant="caption" sx={{ color: '#94a3b8' }}>
            Semantic vectors vs. exact keywords
          </Typography>
        </Box>

        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2.2 }}>
          {skillList.map((skill) => (
            <Box key={skill.name}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 0.8 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5 }}>
                  <Typography variant="body2" sx={{ fontWeight: 600, color: '#f1f5f9', fontSize: '0.9rem' }}>
                    {skill.name}
                  </Typography>
                  {getStatusChip(skill.status)}
                </Box>
                <Typography variant="body2" sx={{ fontWeight: 700, color: getBarColor(skill.score), fontFamily: 'JetBrains Mono, monospace' }}>
                  {skill.score}%
                </Typography>
              </Box>
              <LinearProgress
                variant="determinate"
                value={skill.score}
                sx={{
                  height: 8,
                  borderRadius: 4,
                  backgroundColor: 'rgba(255, 255, 255, 0.08)',
                  '& .MuiLinearProgress-bar': {
                    backgroundColor: getBarColor(skill.score),
                    borderRadius: 4,
                  }
                }}
              />
            </Box>
          ))}
        </Box>
      </CardContent>
    </Card>
  );
}
