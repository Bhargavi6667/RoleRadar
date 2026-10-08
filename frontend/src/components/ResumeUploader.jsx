import React, { useState, useRef, useEffect } from 'react';
import { Box, Typography, Button, CircularProgress, Alert, Card, CardContent, IconButton, LinearProgress } from '@mui/material';
import { UploadCloud, FileText, X, Sparkles } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { resumeApi, analysisApi } from '../services/api';

const MAX_BYTES = 20 * 1024 * 1024;
const STAGES = [
  'Uploading and reading your PDF...',
  'Detecting skills and experience...',
  'Scoring your fit across roles...',
  'Finding companies hiring for your best-fit roles...',
];

export const RESULT_KEY = 'careerlens_role_fit';

export default function ResumeUploader() {
  const navigate = useNavigate();
  const inputRef = useRef(null);
  const [file, setFile] = useState(null);
  const [dragOver, setDragOver] = useState(false);
  const [loading, setLoading] = useState(false);
  const [stage, setStage] = useState(0);
  const [error, setError] = useState(null);

  // Cycle the status text while the request is running
  useEffect(() => {
    if (!loading) return undefined;
    setStage(0);
    const t = setInterval(() => setStage((s) => Math.min(s + 1, STAGES.length - 1)), 2500);
    return () => clearInterval(t);
  }, [loading]);

  const pickFile = (f) => {
    setError(null);
    if (!f) return;
    if (!f.name.toLowerCase().endsWith('.pdf')) {
      setError('Only PDF files are supported. Please export your resume as a PDF.');
      return;
    }
    if (f.size > MAX_BYTES) {
      setError('That file is larger than 20 MB. Please upload a smaller PDF.');
      return;
    }
    setFile(f);
  };

  const handleAnalyze = async () => {
    if (!file) {
      setError('Please choose a PDF resume first.');
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const uploaded = await resumeApi.uploadFile(file);
      const res = await analysisApi.roleFit({ resumeId: uploaded.data.id });
      localStorage.setItem(RESULT_KEY, JSON.stringify({ ...res.data, fileName: file.name, analyzedAt: Date.now() }));
      navigate('/results');
    } catch (err) {
      console.error(err);
      setError(
        err.response?.data?.message ||
        (err.response ? 'Analysis failed. Please try again.' : 'Cannot reach the server. Make sure the backend and AI service are running.')
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card sx={{
      background: 'rgba(32, 23, 20, 0.7)', border: '1px solid rgba(255, 255, 255, 0.08)',
      borderRadius: 3, backdropFilter: 'blur(10px)', boxShadow: '0 8px 32px 0 rgba(0, 0, 0, 0.36)',
    }}>
      <CardContent sx={{ p: { xs: 2.5, md: 4 } }}>
        {error && <Alert severity="error" sx={{ mb: 3 }} onClose={() => setError(null)}>{error}</Alert>}

        {!file ? (
          <Box
            onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
            onDragLeave={() => setDragOver(false)}
            onDrop={(e) => { e.preventDefault(); setDragOver(false); pickFile(e.dataTransfer.files?.[0]); }}
            onClick={() => inputRef.current?.click()}
            sx={{
              border: `2px dashed ${dragOver ? '#f97316' : 'rgba(255, 255, 255, 0.18)'}`,
              borderRadius: 3, p: { xs: 4, md: 7 }, textAlign: 'center', cursor: 'pointer',
              backgroundColor: dragOver ? 'rgba(249, 115, 22, 0.1)' : 'rgba(20, 13, 11, 0.4)',
              transition: 'all 0.2s ease',
              '&:hover': { borderColor: '#f97316' },
            }}
          >
            <input ref={inputRef} type="file" accept=".pdf,application/pdf" hidden onChange={(e) => pickFile(e.target.files?.[0])} />
            <UploadCloud size={48} color="#fb923c" style={{ margin: '0 auto 14px' }} />
            <Typography variant="h6" sx={{ color: '#fff', fontWeight: 700 }}>
              Click to choose your resume PDF
            </Typography>
            <Typography variant="body2" sx={{ color: '#64748b', mt: 0.5 }}>
              or drag and drop it here. PDF only, up to 20 MB.
            </Typography>
          </Box>
        ) : (
          <Box sx={{
            display: 'flex', alignItems: 'center', gap: 2, p: 2.5, borderRadius: 3,
            border: '1px solid rgba(16, 185, 129, 0.35)', backgroundColor: 'rgba(16, 185, 129, 0.07)',
          }}>
            <FileText size={34} color="#10b981" />
            <Box sx={{ flex: 1, minWidth: 0 }}>
              <Typography variant="subtitle1" noWrap sx={{ color: '#fff', fontWeight: 700 }}>{file.name}</Typography>
              <Typography variant="caption" sx={{ color: '#94a3b8' }}>{(file.size / 1024).toFixed(1)} KB, ready to analyze</Typography>
            </Box>
            <IconButton aria-label="Remove file" disabled={loading} onClick={() => setFile(null)} sx={{ color: '#94a3b8' }}>
              <X size={20} />
            </IconButton>
          </Box>
        )}

        {loading && (
          <Box sx={{ mt: 3 }}>
            <LinearProgress sx={{ height: 6, borderRadius: 3 }} />
            <Typography variant="body2" sx={{ color: '#94a3b8', mt: 1.5, textAlign: 'center' }}>{STAGES[stage]}</Typography>
          </Box>
        )}

        <Box sx={{ mt: 4, display: 'flex', justifyContent: 'center' }}>
          <Button
            variant="contained"
            size="large"
            disabled={loading || !file}
            onClick={handleAnalyze}
            startIcon={loading ? <CircularProgress size={18} color="inherit" /> : <Sparkles size={18} />}
            sx={{
              px: 6, py: 1.6, borderRadius: 3, fontWeight: 700, fontSize: '1.05rem', textTransform: 'none',
              background: 'linear-gradient(135deg, #f97316 0%, #ec4899 100%)',
              boxShadow: '0 4px 20px rgba(249, 115, 22, 0.5)',
              '&:hover': { background: 'linear-gradient(135deg, #ea580c 0%, #db2777 100%)' },
            }}
          >
            {loading ? 'Analyzing...' : 'Analyze Resume'}
          </Button>
        </Box>
      </CardContent>
    </Card>
  );
}
