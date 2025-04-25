import React from 'react';
import { Typography, Box, Paper, Card, CardContent } from '@mui/material';

const SavedTrends = () => {
  return (
    <Box sx={{ mt: 3 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Saved Trends
      </Typography>
      <Paper sx={{ p: 3, mb: 4 }}>
        <Typography variant="body1">
          This page will display your saved trend searches and historical data.
          In the full implementation, it will include:
        </Typography>
        <ul>
          <li>
            <Typography variant="body1">
              List of saved trend searches
            </Typography>
          </li>
          <li>
            <Typography variant="body1">
              Historical trend data visualization
            </Typography>
          </li>
          <li>
            <Typography variant="body1">
              Comparison tools for multiple trends
            </Typography>
          </li>
          <li>
            <Typography variant="body1">
              Export options for saved data
            </Typography>
          </li>
        </ul>
      </Paper>
      
      <Card>
        <CardContent>
          <Typography variant="h5" gutterBottom>
            No Saved Trends
          </Typography>
          <Typography variant="body1">
            You haven't saved any trends yet. Use the Search page to find and save trends.
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default SavedTrends; 