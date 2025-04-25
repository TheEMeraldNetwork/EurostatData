import React from 'react';
import { useQuery } from 'react-query';
import { 
  Typography, 
  Grid, 
  Card, 
  CardContent, 
  CardHeader,
  Button,
  Box,
  CircularProgress,
  List,
  ListItem,
  ListItemText,
  Chip,
  Paper,
  Divider
} from '@mui/material';
import { TrendingUp, ArrowUpward } from '@mui/icons-material';
import apiService from '../services/api';

const Dashboard = () => {
  // Fetch current trends
  const { data: trendData, isLoading, error } = useQuery(
    'currentTrends', 
    () => apiService.trends.getCurrent({ geo: 'IT' }).then(res => res.data)
  );

  // Handle loading state
  if (isLoading) {
    return (
      <Box 
        sx={{ 
          display: 'flex', 
          justifyContent: 'center', 
          alignItems: 'center', 
          height: '50vh' 
        }}
      >
        <CircularProgress />
      </Box>
    );
  }

  // Handle error state
  if (error) {
    return (
      <Box sx={{ mt: 3 }}>
        <Typography variant="h5" color="error" gutterBottom>
          Error loading trends
        </Typography>
        <Typography variant="body1">
          {error.message || 'An unknown error occurred'}
        </Typography>
      </Box>
    );
  }

  // Get trends if data exists
  const trends = trendData?.data || [];

  return (
    <Box sx={{ mt: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Dashboard
        </Typography>
        <Button 
          variant="contained" 
          color="primary"
          onClick={() => window.location.reload()}
        >
          Refresh Data
        </Button>
      </Box>

      <Grid container spacing={4}>
        {/* Trending Topics Card */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardHeader 
              title="Current Trending Topics" 
              subheader="Italy"
              avatar={<TrendingUp color="primary" />}
            />
            <Divider />
            <CardContent>
              {trends.length > 0 ? (
                <List>
                  {trends.slice(0, 5).map((trend, index) => (
                    <ListItem 
                      key={index}
                      secondaryAction={
                        trend.details?.rising && (
                          <Chip 
                            icon={<ArrowUpward />} 
                            label="Rising" 
                            color="secondary" 
                            size="small" 
                          />
                        )
                      }
                    >
                      <ListItemText
                        primary={trend.topic}
                        secondary={`Interest: ${trend.details?.current_interest || 'Unknown'}`}
                      />
                    </ListItem>
                  ))}
                </List>
              ) : (
                <Typography variant="body1" color="text.secondary">
                  No trending topics available
                </Typography>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Quick Actions Card */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardHeader title="Quick Actions" />
            <Divider />
            <CardContent>
              <Grid container spacing={2}>
                <Grid item xs={12}>
                  <Button 
                    variant="outlined" 
                    fullWidth
                    onClick={() => window.location.href = '/search'}
                  >
                    Search Trends
                  </Button>
                </Grid>
                <Grid item xs={12}>
                  <Button 
                    variant="outlined" 
                    fullWidth
                    onClick={() => window.location.href = '/content'}
                  >
                    Generate Content Ideas
                  </Button>
                </Grid>
                <Grid item xs={12}>
                  <Button 
                    variant="outlined" 
                    fullWidth
                    onClick={() => window.location.href = '/saved'}
                  >
                    View Saved Trends
                  </Button>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        {/* Additional Stats */}
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h5" gutterBottom>System Overview</Typography>
            <Grid container spacing={3}>
              <Grid item xs={12} sm={4}>
                <Box sx={{ textAlign: 'center', p: 2 }}>
                  <Typography variant="h3" color="primary">{trends.length}</Typography>
                  <Typography variant="body1">Active Trends</Typography>
                </Box>
              </Grid>
              <Grid item xs={12} sm={4}>
                <Box sx={{ textAlign: 'center', p: 2 }}>
                  <Typography variant="h3" color="primary">
                    {trends.filter(t => t.details?.rising).length}
                  </Typography>
                  <Typography variant="body1">Rising Trends</Typography>
                </Box>
              </Grid>
              <Grid item xs={12} sm={4}>
                <Box sx={{ textAlign: 'center', p: 2 }}>
                  <Typography variant="h3" color="primary">0</Typography>
                  <Typography variant="body1">Saved Searches</Typography>
                </Box>
              </Grid>
            </Grid>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard; 