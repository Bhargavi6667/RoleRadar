import React, { useState, useMemo } from 'react';
import {
  Container, Box, Typography, Grid, Card, CardContent, Chip, Button, LinearProgress, Tabs, Tab, Alert,
} from '@mui/material';
import { Link, Navigate } from 'react-router-dom';
import {
  Target, CheckCircle2, XCircle, Lightbulb, Building2, MapPin, Briefcase, ExternalLink, Search, RefreshCw, FileText, ListChecks, MessageSquare,
} from 'lucide-react';
import { RESULT_KEY } from '../components/ResumeUploader';

const scoreColor = (s) => (s >= 75 ? '#10b981' : s >= 55 ? '#84cc16' : s >= 35 ? '#f59e0b' : '#ef4444');
const PRIORITY = {
  High: { bg: 'rgba(239, 68, 68, 0.14)', fg: '#f87171' },
  Medium: { bg: 'rgba(245, 158, 11, 0.14)', fg: '#fbbf24' },
  Low: { bg: 'rgba(56, 189, 248, 0.14)', fg: '#38bdf8' },
};
const cardSx = { background: 'rgba(32, 23, 20, 0.7)', border: '1px solid rgba(255,255,255,0.08)', borderRadius: 3, height: '100%' };

function loadResult() {
  try {
    const raw = localStorage.getItem(RESULT_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

function ScoreDial({ value, label, size = 150 }) {
  const c = scoreColor(value);
  const inner = size - 26;
  return (
    <Box sx={{
      width: size, height: size, borderRadius: '50%', mx: 'auto',
      background: `conic-gradient(${c} ${value * 3.6}deg, rgba(255,255,255,0.07) 0deg)`,
      display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: `0 0 30px ${c}33`,
    }}>
      <Box sx={{ width: inner, height: inner, borderRadius: '50%', background: '#140d0b', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
        <Typography sx={{ fontWeight: 800, color: '#fff', lineHeight: 1, fontSize: size > 120 ? '2.4rem' : '1.6rem' }}>{value}%</Typography>
        <Typography variant="caption" sx={{ color: '#94a3b8', fontWeight: 600, mt: 0.5 }}>{label}</Typography>
      </Box>
    </Box>
  );
}

function VacancyCard({ v }) {
  const live = `https://www.linkedin.com/jobs/search/?keywords=${encodeURIComponent(`${v.title} ${v.company}`)}&location=India`;
  return (
    <Card sx={{ ...cardSx, backgroundColor: 'rgba(20, 13, 11, 0.6)' }}>
      <CardContent sx={{ p: 2.5, display: 'flex', flexDirection: 'column', height: '100%' }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 0.5 }}>
          <Building2 size={16} color="#fb923c" />
          <Typography variant="subtitle2" sx={{ color: '#fed7aa', fontWeight: 700 }}>{v.company}</Typography>
        </Box>
        <Typography variant="subtitle1" sx={{ color: '#f8fafc', fontWeight: 700, lineHeight: 1.3, mb: 1 }}>{v.title}</Typography>
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2, color: '#94a3b8', mb: 1.5 }}>
          <Typography variant="caption" sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}><MapPin size={13} /> {v.location}</Typography>
          <Typography variant="caption" sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}><Briefcase size={13} /> {v.experience}</Typography>
        </Box>
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.7, mb: 2 }}>
          {v.skills?.map((s) => (
            <Chip key={s} label={s} size="small" sx={{ backgroundColor: 'rgba(255,255,255,0.06)', color: '#cbd5e1', fontSize: '0.72rem' }} />
          ))}
        </Box>
        <Box sx={{ mt: 'auto', display: 'flex', gap: 1 }}>
          <Button component="a" href={live} target="_blank" rel="noopener noreferrer" size="small" variant="contained" startIcon={<Search size={14} />}
            sx={{ textTransform: 'none', fontWeight: 600, background: 'linear-gradient(135deg, #f97316 0%, #ec4899 100%)' }}>
            Find openings
          </Button>
          <Button component="a" href={v.careersUrl} target="_blank" rel="noopener noreferrer" size="small" variant="outlined" endIcon={<ExternalLink size={14} />}
            sx={{ textTransform: 'none', fontWeight: 600, borderColor: 'rgba(255,255,255,0.2)', color: '#cbd5e1' }}>
            Careers page
          </Button>
        </Box>
      </CardContent>
    </Card>
  );
}

export default function Results() {
  const data = useMemo(loadResult, []);
  const [tab, setTab] = useState(0);

  if (!data) return <Navigate to="/upload" replace />;

  const topRoles = data.role_scores.slice(0, 3);
  const activeRole = topRoles[tab] || topRoles[0];
  const vacancies = data.vacancies?.[activeRole.role_id] || [];
  const passed = data.quality_checks.filter((c) => c.passed).length;

  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      {/* Header */}
      <Box sx={{ mb: 3, display: 'flex', flexDirection: { xs: 'column', md: 'row' }, justifyContent: 'space-between', alignItems: { md: 'center' }, gap: 2 }}>
        <Box>
          <Typography variant="overline" sx={{ color: '#fb923c', fontWeight: 700, letterSpacing: 2 }}>Step 2 of 2</Typography>
          <Typography variant="h4" sx={{ fontWeight: 800, color: '#fff' }}>Your resume analysis</Typography>
          {data.fileName && (
            <Typography variant="body2" sx={{ color: '#94a3b8', display: 'flex', alignItems: 'center', gap: 0.7, mt: 0.5 }}>
              <FileText size={15} /> {data.fileName}
            </Typography>
          )}
        </Box>
        <Box sx={{ display: 'flex', gap: 1.5, flexWrap: 'wrap' }}>
          <Button component={Link} to={`/interview?role=${data.best_role_id}`} variant="contained" startIcon={<MessageSquare size={16} />}
            sx={{ textTransform: 'none', fontWeight: 700, background: 'linear-gradient(135deg, #f97316 0%, #ec4899 100%)' }}>
            Practice interview questions
          </Button>
          <Button component={Link} to="/upload" variant="outlined" startIcon={<RefreshCw size={16} />}
            sx={{ textTransform: 'none', fontWeight: 600, borderColor: 'rgba(255,255,255,0.2)', color: '#cbd5e1' }}>
            Analyze another resume
          </Button>
        </Box>
      </Box>

      {data.low_signal && (
        <Alert severity="warning" sx={{ mb: 3 }}>
          We couldn't find many recognisable skills in this resume, so the scores below are low-confidence.
          Check that your Skills section is included as real text in the PDF, and see the suggestions below.
        </Alert>
      )}

      {/* Score + role ranking */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} md={5}>
          <Card sx={cardSx}>
            <CardContent sx={{ p: 3, textAlign: 'center' }}>
              <Typography variant="overline" sx={{ color: '#94a3b8', fontWeight: 700 }}>Best-fit role</Typography>
              <Typography variant="h5" sx={{ color: '#fff', fontWeight: 800, mb: 2 }}>{data.best_role}</Typography>
              <ScoreDial value={data.overall_score} label="ROLE FIT" />
              <Chip label={data.fit_label} sx={{ mt: 2, fontWeight: 700, color: scoreColor(data.overall_score), backgroundColor: `${scoreColor(data.overall_score)}22` }} />
              <Typography variant="body2" sx={{ color: '#cbd5e1', mt: 2 }}>{data.summary}</Typography>
              <Box sx={{ mt: 3, pt: 2.5, borderTop: '1px solid rgba(255,255,255,0.08)', display: 'flex', alignItems: 'center', gap: 2, textAlign: 'left' }}>
                <Box sx={{ minWidth: 76 }}><ScoreDial value={data.resume_quality_score} label="" size={76} /></Box>
                <Box>
                  <Typography variant="subtitle2" sx={{ color: '#f8fafc', fontWeight: 700 }}>Resume quality: {data.resume_quality_score}/100</Typography>
                  <Typography variant="caption" sx={{ color: '#94a3b8' }}>{passed} of {data.quality_checks.length} checks passed (structure, contact info, impact)</Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={7}>
          <Card sx={cardSx}>
            <CardContent sx={{ p: 3 }}>
              <Typography variant="h6" sx={{ fontWeight: 700, color: '#f8fafc', mb: 2.5, display: 'flex', alignItems: 'center', gap: 1 }}>
                <Target size={20} color="#fb923c" /> How you fit each role
              </Typography>
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2.2 }}>
                {data.role_scores.map((r, i) => (
                  <Box key={r.role_id}>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.6 }}>
                      <Typography variant="body2" sx={{ color: i === 0 ? '#fff' : '#cbd5e1', fontWeight: i === 0 ? 700 : 500 }}>
                        {r.role}{i === 0 && <Chip label="Best match" size="small" sx={{ ml: 1, height: 20, fontSize: '0.68rem', backgroundColor: 'rgba(249,115,22,0.25)', color: '#ffedd5' }} />}
                      </Typography>
                      <Typography variant="body2" sx={{ fontWeight: 700, color: scoreColor(r.score), fontFamily: 'JetBrains Mono, monospace' }}>{r.score}%</Typography>
                    </Box>
                    <LinearProgress variant="determinate" value={r.score}
                      sx={{ height: 8, borderRadius: 4, backgroundColor: 'rgba(255,255,255,0.08)', '& .MuiLinearProgress-bar': { backgroundColor: scoreColor(r.score), borderRadius: 4 } }} />
                  </Box>
                ))}
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Skills */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} md={6}>
          <Card sx={cardSx}>
            <CardContent sx={{ p: 3 }}>
              <Typography variant="subtitle1" sx={{ fontWeight: 700, color: '#f8fafc', mb: 2, display: 'flex', alignItems: 'center', gap: 1 }}>
                <CheckCircle2 size={18} color="#10b981" /> Skills we found for {data.best_role}
              </Typography>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                {data.matched_skills.length ? data.matched_skills.map((s) => (
                  <Chip key={s} label={s} sx={{ backgroundColor: 'rgba(16,185,129,0.13)', color: '#34d399', fontWeight: 600 }} />
                )) : <Typography variant="body2" sx={{ color: '#94a3b8' }}>No role-specific skills detected.</Typography>}
              </Box>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={6}>
          <Card sx={cardSx}>
            <CardContent sx={{ p: 3 }}>
              <Typography variant="subtitle1" sx={{ fontWeight: 700, color: '#f8fafc', mb: 2, display: 'flex', alignItems: 'center', gap: 1 }}>
                <XCircle size={18} color="#f59e0b" /> Core skills missing from your resume
              </Typography>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                {data.missing_skills.length ? data.missing_skills.map((s) => (
                  <Chip key={s} label={s} sx={{ backgroundColor: 'rgba(245,158,11,0.13)', color: '#fbbf24', fontWeight: 600 }} />
                )) : <Typography variant="body2" sx={{ color: '#94a3b8' }}>None. You cover all the core skills we look for.</Typography>}
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Suggestions + quality checklist */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={7}>
          <Card sx={cardSx}>
            <CardContent sx={{ p: 3 }}>
              <Typography variant="h6" sx={{ fontWeight: 700, color: '#f8fafc', mb: 2, display: 'flex', alignItems: 'center', gap: 1 }}>
                <Lightbulb size={20} color="#f59e0b" /> Suggestions to improve
              </Typography>
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1.8 }}>
                {data.suggestions.map((s, i) => (
                  <Box key={i} sx={{ display: 'flex', gap: 1.5, alignItems: 'flex-start' }}>
                    <Chip label={s.priority} size="small" sx={{ mt: 0.2, minWidth: 68, fontWeight: 700, fontSize: '0.7rem', backgroundColor: PRIORITY[s.priority]?.bg, color: PRIORITY[s.priority]?.fg }} />
                    <Box>
                      <Typography variant="caption" sx={{ color: '#fb923c', fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.5 }}>{s.category}</Typography>
                      <Typography variant="body2" sx={{ color: '#cbd5e1' }}>{s.text}</Typography>
                    </Box>
                  </Box>
                ))}
              </Box>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={5}>
          <Card sx={cardSx}>
            <CardContent sx={{ p: 3 }}>
              <Typography variant="h6" sx={{ fontWeight: 700, color: '#f8fafc', mb: 2, display: 'flex', alignItems: 'center', gap: 1 }}>
                <ListChecks size={20} color="#38bdf8" /> Resume checklist
              </Typography>
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1.2 }}>
                {data.quality_checks.map((c) => (
                  <Box key={c.label} sx={{ display: 'flex', alignItems: 'center', gap: 1.2 }}>
                    {c.passed ? <CheckCircle2 size={17} color="#10b981" /> : <XCircle size={17} color="#ef4444" />}
                    <Typography variant="body2" sx={{ color: c.passed ? '#cbd5e1' : '#f1f5f9', fontWeight: c.passed ? 400 : 600 }}>{c.label}</Typography>
                  </Box>
                ))}
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Vacancies */}
      <Card sx={{ ...cardSx, height: 'auto' }}>
        <CardContent sx={{ p: 3 }}>
          <Typography variant="h5" sx={{ fontWeight: 800, color: '#fff', mb: 0.5, display: 'flex', alignItems: 'center', gap: 1.2 }}>
            <Building2 size={22} color="#fb923c" /> Companies hiring for your roles
          </Typography>
          <Typography variant="body2" sx={{ color: '#94a3b8', mb: 2 }}>
            Roles these companies typically hire for. "Find openings" searches current listings; "Careers page" goes to the company's own site.
          </Typography>

          <Tabs value={tab} onChange={(_, v) => setTab(v)} variant="scrollable" scrollButtons="auto"
            sx={{ mb: 3, borderBottom: '1px solid rgba(255,255,255,0.08)', '& .MuiTab-root': { textTransform: 'none', fontWeight: 600 } }}>
            {topRoles.map((r) => <Tab key={r.role_id} label={`${r.role} (${r.score}%)`} />)}
          </Tabs>

          {vacancies.length ? (
            <Grid container spacing={2.5}>
              {vacancies.map((v) => (
                <Grid item xs={12} sm={6} lg={4} key={`${v.company}-${v.title}`}><VacancyCard v={v} /></Grid>
              ))}
            </Grid>
          ) : (
            <Typography variant="body2" sx={{ color: '#94a3b8' }}>No companies listed for this role yet.</Typography>
          )}
        </CardContent>
      </Card>
    </Container>
  );
}
