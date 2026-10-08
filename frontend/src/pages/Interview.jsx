import React, { useEffect, useMemo, useState } from 'react';
import {
  Container, Box, Typography, Chip, Accordion, AccordionSummary, AccordionDetails, TextField, Button,
  CircularProgress, Alert, LinearProgress,
} from '@mui/material';
import { useSearchParams, Link } from 'react-router-dom';
import { ChevronDown, Lightbulb, Send, CheckCircle2, XCircle, RefreshCw, MessageSquare } from 'lucide-react';
import { interviewApi } from '../services/api';
import { RESULT_KEY } from '../components/ResumeUploader';

// ids must match the role ids used by the AI service
const ROLE_OPTIONS = [
  ['frontend', 'Frontend Developer'], ['backend', 'Backend Developer'], ['fullstack', 'Full Stack Developer'],
  ['devops', 'DevOps / Cloud Engineer'], ['data', 'Data Scientist / ML Engineer'], ['mobile', 'Mobile App Developer'],
  ['qa', 'QA / Test Engineer'], ['uiux', 'UI / UX Designer'], ['sales', 'Sales / Business Development'],
  ['marketing', 'Digital Marketing'], ['hr', 'HR / Talent Acquisition'], ['finance', 'Finance / Accounting'],
  ['support', 'Customer Support'],
];
const DIFF_COLOR = { Easy: '#10b981', Medium: '#f59e0b', Hard: '#ef4444' };
const fbColor = (s) => (s >= 7.5 ? '#10b981' : s >= 5 ? '#f59e0b' : '#ef4444');

function loadResult() {
  try { return JSON.parse(localStorage.getItem(RESULT_KEY) || 'null'); } catch { return null; }
}

export default function Interview() {
  const [params, setParams] = useSearchParams();
  const result = useMemo(loadResult, []);
  const roleId = params.get('role') || result?.best_role_id || 'frontend';
  const roleLabel = ROLE_OPTIONS.find(([id]) => id === roleId)?.[1] || roleId;

  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [category, setCategory] = useState('All');
  const [answers, setAnswers] = useState({});
  const [feedback, setFeedback] = useState({});
  const [busyId, setBusyId] = useState(null);
  const [reload, setReload] = useState(0);

  // skills for this role come from the analysis, if there is one
  const roleInfo = result?.role_scores?.find((r) => r.role_id === roleId);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError(null);
    setCategory('All');
    interviewApi.roleQuestions({
      role_id: roleId,
      role: roleLabel,
      matched_skills: roleInfo?.matched_skills || [],
      missing_skills: roleInfo?.missing_skills || [],
      resume_id: result?.resume_id ?? undefined,
    })
      .then((res) => { if (!cancelled) { setData(res.data); setAnswers({}); setFeedback({}); } })
      .catch((e) => {
        if (!cancelled) setError(e.response?.data?.message || 'Could not load questions. Make sure the backend and AI service are running.');
      })
      .finally(() => { if (!cancelled) setLoading(false); });
    return () => { cancelled = true; };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [roleId, reload]);

  const categories = useMemo(() => ['All', ...Array.from(new Set((data?.questions || []).map((q) => q.category)))], [data]);
  const shown = (data?.questions || []).filter((q) => category === 'All' || q.category === category);

  const getFeedback = async (q) => {
    setBusyId(q.id);
    try {
      const res = await interviewApi.evaluate({ role_id: roleId, role: roleLabel, question: q.question, answer: answers[q.id] || '' });
      setFeedback((f) => ({ ...f, [q.id]: res.data }));
    } catch (e) {
      setFeedback((f) => ({ ...f, [q.id]: { error: e.response?.data?.message || 'Could not get feedback. Please try again.' } }));
    } finally {
      setBusyId(null);
    }
  };

  const done = Object.values(feedback).filter((f) => f && !f.error).length;

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Box sx={{ mb: 3 }}>
        <Typography variant="overline" sx={{ color: '#fb923c', fontWeight: 700, letterSpacing: 2 }}>Interview prep</Typography>
        <Typography variant="h4" sx={{ fontWeight: 800, color: '#fff', display: 'flex', alignItems: 'center', gap: 1.2 }}>
          <MessageSquare size={30} color="#fb923c" /> Practice for {roleLabel}
        </Typography>
        <Typography variant="body2" sx={{ color: '#94a3b8', mt: 0.5 }}>
          Open a question, write your answer, and get feedback. Pick a different role below any time.
        </Typography>
        {!result && (
          <Alert severity="info" sx={{ mt: 2 }}>
            Questions will be more personal after you <Link to="/upload" style={{ color: 'inherit', fontWeight: 700 }}>analyze your resume</Link>.
          </Alert>
        )}
      </Box>

      {/* Role picker */}
      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mb: 3 }}>
        {ROLE_OPTIONS.map(([id, label]) => (
          <Chip key={id} label={label} clickable onClick={() => setParams({ role: id })}
            sx={{
              fontWeight: 600,
              backgroundColor: id === roleId ? '#f97316' : 'rgba(255,255,255,0.06)',
              color: id === roleId ? '#fff' : '#cbd5e1',
              '&:hover': { backgroundColor: id === roleId ? '#ea580c' : 'rgba(255,255,255,0.12)' },
            }} />
        ))}
      </Box>

      {error && <Alert severity="error" sx={{ mb: 3 }}>{error}</Alert>}
      {loading && <LinearProgress sx={{ mb: 3, borderRadius: 2 }} />}

      {data && !loading && (
        <>
          <Box sx={{ display: 'flex', flexWrap: 'wrap', alignItems: 'center', gap: 1, mb: 1 }}>
            {categories.map((c) => (
              <Chip key={c} label={c} size="small" clickable onClick={() => setCategory(c)} variant={c === category ? 'filled' : 'outlined'}
                sx={{ fontWeight: 600, color: c === category ? '#fff' : '#cbd5e1', backgroundColor: c === category ? 'rgba(249, 115, 22, 0.35)' : 'transparent', borderColor: 'rgba(255,255,255,0.2)' }} />
            ))}
            <Box sx={{ flex: 1 }} />
            <Typography variant="caption" sx={{ color: '#94a3b8' }}>{done} of {data.questions.length} practised</Typography>
            <Button size="small" startIcon={<RefreshCw size={14} />} onClick={() => setReload((n) => n + 1)} sx={{ textTransform: 'none', color: '#cbd5e1' }}>
              New set
            </Button>
          </Box>
          <Typography variant="caption" sx={{ display: 'block', color: '#64748b', mb: 2 }}>
            {data.ai_generated
              ? 'Questions include AI-generated ones tailored to your resume.'
              : 'Curated questions for this role, personalised with the skills found in your resume.'}
          </Typography>

          {shown.map((q) => {
            const fb = feedback[q.id];
            return (
              <Accordion key={q.id} disableGutters
                sx={{ mb: 1.5, background: 'rgba(32, 23, 20, 0.7)', border: '1px solid rgba(255,255,255,0.08)', borderRadius: '12px !important', '&:before': { display: 'none' }, color: '#f1f5f9' }}>
                <AccordionSummary expandIcon={<ChevronDown color="#94a3b8" />}>
                  <Box>
                    <Box sx={{ display: 'flex', gap: 1, mb: 0.8, alignItems: 'center' }}>
                      <Chip label={q.category} size="small" sx={{ height: 22, fontSize: '0.7rem', fontWeight: 700, backgroundColor: 'rgba(249, 115, 22, 0.2)', color: '#fed7aa' }} />
                      <Chip label={q.difficulty} size="small" sx={{ height: 22, fontSize: '0.7rem', fontWeight: 700, color: DIFF_COLOR[q.difficulty] || '#94a3b8', backgroundColor: `${DIFF_COLOR[q.difficulty] || '#94a3b8'}22` }} />
                      {fb && !fb.error && <CheckCircle2 size={16} color="#10b981" />}
                    </Box>
                    <Typography sx={{ fontWeight: 600 }}>{q.question}</Typography>
                  </Box>
                </AccordionSummary>
                <AccordionDetails sx={{ pt: 0 }}>
                  {q.tip && (
                    <Box sx={{ display: 'flex', gap: 1, p: 1.5, mb: 2, borderRadius: 2, backgroundColor: 'rgba(245, 158, 11, 0.08)' }}>
                      <Lightbulb size={16} color="#f59e0b" style={{ flexShrink: 0, marginTop: 2 }} />
                      <Typography variant="body2" sx={{ color: '#fcd34d' }}>{q.tip}</Typography>
                    </Box>
                  )}
                  <TextField
                    multiline minRows={4} fullWidth placeholder="Type your answer here as you would say it in the interview..."
                    value={answers[q.id] || ''} onChange={(e) => setAnswers((a) => ({ ...a, [q.id]: e.target.value }))}
                    sx={{ '& .MuiOutlinedInput-root': { color: '#f1f5f9', backgroundColor: 'rgba(0,0,0,0.25)' } }}
                  />
                  <Button variant="contained" disabled={busyId === q.id || (answers[q.id] || '').trim().length < 5}
                    onClick={() => getFeedback(q)}
                    startIcon={busyId === q.id ? <CircularProgress size={16} color="inherit" /> : <Send size={16} />}
                    sx={{ mt: 1.5, textTransform: 'none', fontWeight: 700, background: 'linear-gradient(135deg, #f97316 0%, #ec4899 100%)' }}>
                    Get feedback
                  </Button>

                  {fb?.error && <Alert severity="error" sx={{ mt: 2 }}>{fb.error}</Alert>}
                  {fb && !fb.error && (
                    <Box sx={{ mt: 2.5, p: 2, borderRadius: 2, border: `1px solid ${fbColor(fb.score)}55`, backgroundColor: `${fbColor(fb.score)}0f` }}>
                      <Typography sx={{ fontWeight: 800, color: fbColor(fb.score), mb: 1 }}>
                        {fb.score}/10 · {fb.verdict}
                      </Typography>
                      {fb.strengths?.map((s) => (
                        <Typography key={s} variant="body2" sx={{ color: '#cbd5e1', display: 'flex', gap: 1, mb: 0.5 }}><CheckCircle2 size={16} color="#10b981" style={{ flexShrink: 0, marginTop: 2 }} /> {s}</Typography>
                      ))}
                      {fb.improvements?.map((s) => (
                        <Typography key={s} variant="body2" sx={{ color: '#cbd5e1', display: 'flex', gap: 1, mb: 0.5 }}><XCircle size={16} color="#f59e0b" style={{ flexShrink: 0, marginTop: 2 }} /> {s}</Typography>
                      ))}
                      {fb.model_answer_tip && (
                        <Typography variant="body2" sx={{ color: '#94a3b8', mt: 1.5 }}><b>A strong answer includes:</b> {fb.model_answer_tip}</Typography>
                      )}
                      {!fb.ai_generated && (
                        <Typography variant="caption" sx={{ display: 'block', color: '#64748b', mt: 1.5 }}>
                          Basic feedback: this checks detail, structure and specifics, not whether the content is technically correct. Add an OpenAI key to the AI service for full AI feedback.
                        </Typography>
                      )}
                    </Box>
                  )}
                </AccordionDetails>
              </Accordion>
            );
          })}
        </>
      )}
    </Container>
  );
}
