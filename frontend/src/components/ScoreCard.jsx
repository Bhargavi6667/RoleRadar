import React from 'react';
import { Card, CardContent, Typography, Box, Grid, LinearProgress } from '@mui/material';
import { Award, CheckCircle } from 'lucide-react';

export default function ScoreCard({ overallScore = 85, breakdown = {} }) {
  const dimensions = [
    { key: 'skill_match', label: 'Skill Match', weight: '35%', val: breakdown.skill_match ?? 87, color: '#f97316' },
    { key: 'evidence_strength', label: 'Evidence Strength', weight: '20%', val: breakdown.evidence_strength ?? 82, color: '#10b981' },
    { key: 'project_relevance', label: 'Project Relevance', weight: '15%', val: breakdown.project_relevance ?? 91, color: '#3b82f6' },
    { key: 'experience_alignment', label: 'Experience Alignment', weight: '10%', val: breakdown.experience_alignment ?? 75, color: '#f59e0b' },
    { key: 'education_alignment', label: 'Education Alignment', weight: '10%', val: breakdown.education_alignment ?? 90, color: '#ec4899' },
    { key: 'resume_quality', label: 'Resume Quality', weight: '10%', val: breakdown.resume_quality ?? 84, color: '#8b5cf6' },
  ];

  const getScoreColor = (score) => {
    if (score >= 80) return '#10b981';
    if (score >= 60) return '#f59e0b';
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
        <Grid container spacing={3} alignItems="center">
          {/* Main Score Dial */}
          <Grid item xs={12} md={4} sx={{ textAlign: 'center', borderRight: { md: '1px solid rgba(255,255,255,0.08)' } }}>
            <Box sx={{ position: 'relative', display: 'inline-flex', mb: 1 }}>
              <Box sx={{
                width: 140,
                height: 140,
                borderRadius: '50%',
                background: `conic-gradient(${getScoreColor(overallScore)} ${overallScore * 3.6}deg, rgba(255,255,255,0.06) 0deg)`,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                boxShadow: `0 0 30px ${getScoreColor(overallScore)}33`
              }}>
                <Box sx={{
                  width: 116,
                  height: 116,
                  borderRadius: '50%',
                  background: '#140d0b',
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                  justifyContent: 'center'
                }}>
                  <Typography variant="h3" sx={{ fontWeight: 800, color: '#fff', lineHeight: 1 }}>
                    {Math.round(overallScore)}%
                  </Typography>
                  <Typography variant="caption" sx={{ color: '#94a3b8', fontWeight: 600, mt: 0.5 }}>
                    MATCH SCORE
                  </Typography>
                </Box>
              </Box>
            </Box>
            <Typography variant="subtitle2" sx={{ color: '#cbd5e1', fontWeight: 600, mt: 1 }}>
              Evidence-Backed Framework
            </Typography>
            <Typography variant="caption" sx={{ color: '#64748b' }}>
              Transparent multi-dimensional index
            </Typography>
          </Grid>

          {/* 6 Dimensions Breakdown */}
          <Grid item xs={12} md={8}>
            <Typography variant="subtitle1" sx={{ fontWeight: 700, mb: 2, color: '#f1f5f9', display: 'flex', alignItems: 'center', gap: 1 }}>
              <Award size={18} color="#fb923c" /> Transparent Scoring Breakdown
            </Typography>
            <Grid container spacing={2}>
              {dimensions.map((dim) => (
                <Grid item xs={12} sm={6} key={dim.key}>
                  <Box sx={{ mb: 1 }}>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
                      <Typography variant="body2" sx={{ color: '#cbd5e1', fontWeight: 500, fontSize: '0.85rem' }}>
                        {dim.label} <Typography component="span" variant="caption" sx={{ color: '#64748b' }}>({dim.weight})</Typography>
                      </Typography>
                      <Typography variant="body2" sx={{ fontWeight: 700, color: dim.color }}>
                        {dim.val}%
                      </Typography>
                    </Box>
                    <LinearProgress
                      variant="determinate"
                      value={dim.val}
                      sx={{
                        height: 6,
                        borderRadius: 3,
                        backgroundColor: 'rgba(255, 255, 255, 0.08)',
                        '& .MuiLinearProgress-bar': {
                          backgroundColor: dim.color,
                          borderRadius: 3,
                        }
                      }}
                    />
                  </Box>
                </Grid>
              ))}
            </Grid>
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  );
}
