import React from 'react';
import { Card, CardContent, Typography, Box, Chip, Button, List, ListItem, ListItemIcon, ListItemText } from '@mui/material';
import { Compass, AlertCircle, Calendar, ArrowRight, CheckCircle2 } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function GapAnalysis({ gaps = [], roadmap = [] }) {
  const defaultGaps = ['Kubernetes', 'AWS (EC2, S3, IAM)', 'Microservices Distributed Tracing'];
  const gapList = gaps.length > 0 ? gaps : defaultGaps;

  const defaultRoadmap = [
    {
      phase: 'Week 1',
      title: 'Container Orchestration Fundamentals',
      topics: ['Kubernetes architecture & components', 'Pods, ReplicaSets, and Deployments', 'Cluster Services & Port Forwarding'],
      practical_project: 'Containerize and deploy your Spring Boot + PostgreSQL app to local Minikube'
    },
    {
      phase: 'Week 2',
      title: 'Configuration, Secrets & Ingress',
      topics: ['ConfigMaps & Secrets management', 'Ingress controllers and TLS routing', 'Resource limits and health probes'],
      practical_project: 'Configure automated rollouts with zero-downtime updates'
    },
    {
      phase: 'Week 3',
      title: 'Cloud Deployment & Monitoring',
      topics: ['AWS EKS / EC2 deployment basics', 'Prometheus & Grafana metrics', 'CI/CD GitHub Actions deployment'],
      practical_project: 'Deploy the full-stack RoleRadar project to AWS with automated pipeline'
    }
  ];

  const roadmapItems = roadmap.length > 0 ? roadmap : defaultRoadmap;

  return (
    <Card sx={{
      background: 'rgba(32, 23, 20, 0.7)',
      border: '1px solid rgba(255, 255, 255, 0.08)',
      borderRadius: 3,
      backdropFilter: 'blur(10px)',
      boxShadow: '0 8px 32px 0 rgba(0, 0, 0, 0.36)'
    }}>
      <CardContent sx={{ p: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
          <Typography variant="h6" sx={{ fontWeight: 700, color: '#f8fafc', display: 'flex', alignItems: 'center', gap: 1 }}>
            <Compass size={20} color="#f59e0b" /> Skill Gaps & Personalized Roadmap
          </Typography>
          <Button
            component={Link}
            to="/interview"
            variant="contained"
            size="small"
            endIcon={<ArrowRight size={16} />}
            sx={{
              background: 'linear-gradient(135deg, #f97316 0%, #ec4899 100%)',
              textTransform: 'none',
              fontWeight: 600,
              boxShadow: '0 4px 14px rgba(249, 115, 22, 0.4)'
            }}
          >
            Start AI Interview
          </Button>
        </Box>

        {/* Missing Skills Chips */}
        <Box sx={{ mb: 3 }}>
          <Typography variant="caption" sx={{ color: '#94a3b8', display: 'block', mb: 1, fontWeight: 600 }}>
            IDENTIFIED REQUIREMENT GAPS
          </Typography>
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
            {gapList.map((gap, index) => (
              <Chip
                key={index}
                icon={<AlertCircle size={14} color="#f87171" />}
                label={gap}
                sx={{
                  backgroundColor: 'rgba(239, 68, 68, 0.12)',
                  color: '#fca5a5',
                  border: '1px solid rgba(239, 68, 68, 0.25)',
                  fontWeight: 600
                }}
              />
            ))}
          </Box>
        </Box>

        {/* Weekly Roadmap Progression */}
        <Typography variant="caption" sx={{ color: '#94a3b8', display: 'block', mb: 1.5, fontWeight: 600 }}>
          CURATED IMPROVEMENT SPRINT
        </Typography>

        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          {roadmapItems.map((step, idx) => (
            <Box
              key={idx}
              sx={{
                p: 2,
                borderRadius: 2,
                backgroundColor: 'rgba(20, 13, 11, 0.5)',
                borderLeft: '4px solid #f97316',
                borderTop: '1px solid rgba(255,255,255,0.05)',
                borderRight: '1px solid rgba(255,255,255,0.05)',
                borderBottom: '1px solid rgba(255,255,255,0.05)'
              }}
            >
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5, mb: 1 }}>
                <Chip
                  size="small"
                  label={step.phase}
                  sx={{ backgroundColor: 'rgba(249, 115, 22, 0.2)', color: '#fed7aa', fontWeight: 700 }}
                />
                <Typography variant="subtitle2" sx={{ fontWeight: 700, color: '#f1f5f9' }}>
                  {step.title}
                </Typography>
              </Box>

              <List dense sx={{ py: 0, mb: 1 }}>
                {(step.topics || []).map((topic, tidx) => (
                  <ListItem key={tidx} sx={{ px: 0, py: 0.2 }}>
                    <ListItemIcon sx={{ minWidth: 22 }}>
                      <CheckCircle2 size={13} color="#10b981" />
                    </ListItemIcon>
                    <ListItemText
                      primary={topic}
                      primaryTypographyProps={{ variant: 'body2', color: '#94a3b8', fontSize: '0.85rem' }}
                    />
                  </ListItem>
                ))}
              </List>

              {step.practical_project && (
                <Box sx={{ p: 1.2, borderRadius: 1.5, backgroundColor: 'rgba(249, 115, 22, 0.08)', border: '1px dashed rgba(249, 115, 22, 0.3)' }}>
                  <Typography variant="caption" sx={{ color: '#cbd5e1', fontWeight: 600, display: 'block' }}>
                    Hands-on Project:
                  </Typography>
                  <Typography variant="caption" sx={{ color: '#94a3b8', display: 'block' }}>
                    {step.practical_project}
                  </Typography>
                </Box>
              )}
            </Box>
          ))}
        </Box>
      </CardContent>
    </Card>
  );
}
