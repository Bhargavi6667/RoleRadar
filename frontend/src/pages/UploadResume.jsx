import React from 'react';
import { Container, Box, Typography } from '@mui/material';
import ResumeUploader from '../components/ResumeUploader';

export default function UploadResume() {
  return (
    <Container maxWidth="md" sx={{ py: { xs: 4, md: 7 } }}>
      <Box sx={{ mb: 4, textAlign: 'center' }}>
        <Typography variant="overline" sx={{ color: '#fb923c', fontWeight: 700, letterSpacing: 2 }}>Step 1 of 2</Typography>
        <Typography variant="h4" sx={{ fontWeight: 800, color: '#fff', mb: 1 }}>
          Upload your resume
        </Typography>
        <Typography variant="body1" sx={{ color: '#94a3b8', maxWidth: 560, mx: 'auto' }}>
          Choose your resume as a PDF, then click Analyze. You'll see your best-fit roles, a score,
          suggestions and companies hiring.
        </Typography>
      </Box>
      <ResumeUploader />
      <Typography variant="caption" sx={{ display: 'block', textAlign: 'center', color: '#64748b', mt: 2 }}>
        Tip: use a text-based PDF (exported from Word or Google Docs). Scanned image PDFs can't be read.
      </Typography>
    </Container>
  );
}
