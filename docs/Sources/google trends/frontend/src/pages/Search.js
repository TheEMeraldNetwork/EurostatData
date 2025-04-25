import React, { useState } from 'react';
import { useQuery } from 'react-query';
import { 
  Typography, 
  Box, 
  TextField, 
  Button, 
  Grid, 
  Card, 
  CardContent, 
  FormControl, 
  InputLabel, 
  Select, 
  MenuItem,
  CircularProgress,
  Alert,
  Paper,
  Chip
} from '@mui/material';
import apiService from '../services/api';

// Timeframe options
const timeframeOptions = [
  { value: 'today 1-m', label: 'Past Month' },
  { value: 'today 3-m', label: 'Past 3 Months' },
  { value: 'today 12-m', label: 'Past Year' },
  { value: 'today 5-y', label: 'Past 5 Years' },
];

// Region options (focusing on Italy)
const regionOptions = [
  { value: 'IT', label: 'Italy (All)' },
  { value: 'IT-25', label: 'Lombardia' },
  { value: 'IT-62', label: 'Lazio' },
  { value: 'IT-52', label: 'Toscana' },
  { value: 'IT-21', label: 'Piemonte' },
  { value: 'IT-34', label: 'Veneto' },
];

const Search = () => {
  // State for search parameters
  const [keywords, setKeywords] = useState('');
  const [region, setRegion] = useState('IT');
  const [timeframe, setTimeframe] = useState('today 3-m');
  const [isSearching, setIsSearching] = useState(false);

  // Query state
  const { data, isLoading, error, refetch } = useQuery(
    ['searchTrends', keywords, region, timeframe],
    () => apiService.trends.search({
      keywords: keywords.split(',').map(k => k.trim()),
      geo: region,
      timeframe: timeframe
    }).then(res => res.data),
    {
      enabled: false, // Don't run the query automatically
    }
  );

  // Handle search button click
  const handleSearch = () => {
    if (!keywords) return;
    
    setIsSearching(true);
    refetch().then(() => setIsSearching(false));
  };

  // Handle keyword input
  const handleKeywordsChange = (e) => {
    setKeywords(e.target.value);
  };

  return (
    <Box sx={{ mt: 3 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Search Trends
      </Typography>

      <Paper sx={{ p: 3, mb: 4 }}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <TextField
              label="Keywords (separate with commas)"
              variant="outlined"
              fullWidth
              value={keywords}
              onChange={handleKeywordsChange}
              placeholder="blockchain, nft, crypto"
              helperText="Enter up to 5 keywords"
            />
          </Grid>
          <Grid item xs={12} md={3}>
            <FormControl fullWidth>
              <InputLabel>Region</InputLabel>
              <Select
                value={region}
                label="Region"
                onChange={(e) => setRegion(e.target.value)}
              >
                {regionOptions.map((option) => (
                  <MenuItem key={option.value} value={option.value}>
                    {option.label}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} md={3}>
            <FormControl fullWidth>
              <InputLabel>Timeframe</InputLabel>
              <Select
                value={timeframe}
                label="Timeframe"
                onChange={(e) => setTimeframe(e.target.value)}
              >
                {timeframeOptions.map((option) => (
                  <MenuItem key={option.value} value={option.value}>
                    {option.label}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12}>
            <Button 
              variant="contained" 
              color="primary" 
              onClick={handleSearch}
              disabled={!keywords || isLoading || isSearching}
              sx={{ mr: 2 }}
            >
              {isLoading || isSearching ? (
                <CircularProgress size={24} sx={{ color: 'white', mr: 1 }} />
              ) : null}
              Search
            </Button>
            <Button 
              variant="outlined" 
              onClick={() => {
                setKeywords('');
                setRegion('IT');
                setTimeframe('today 3-m');
              }}
            >
              Clear
            </Button>
          </Grid>
        </Grid>
      </Paper>

      {error && (
        <Alert severity="error" sx={{ mb: 4 }}>
          {error.message || 'An error occurred while searching for trends'}
        </Alert>
      )}

      {isSearching && (
        <Box sx={{ display: 'flex', justifyContent: 'center', my: 4 }}>
          <CircularProgress />
        </Box>
      )}

      {data && !isSearching && (
        <Box>
          <Typography variant="h5" gutterBottom>
            Search Results
          </Typography>

          <Grid container spacing={4}>
            {/* Interest Over Time */}
            <Grid item xs={12}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Interest Over Time
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    This would show a chart of interest over time.
                    In a complete implementation, we would use Chart.js to visualize the data.
                  </Typography>
                  <Box sx={{ mt: 2 }}>
                    <Typography variant="body2">
                      Data points: {data?.data?.interest_over_time?.length || 0}
                    </Typography>
                  </Box>
                </CardContent>
              </Card>
            </Grid>

            {/* Related Topics */}
            <Grid item xs={12} md={6}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Related Topics
                  </Typography>
                  {data?.data?.related_topics ? (
                    Object.keys(data.data.related_topics).map(keyword => (
                      <Box key={keyword} sx={{ mb: 3 }}>
                        <Typography variant="subtitle1">
                          For: {keyword}
                        </Typography>
                        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mt: 1 }}>
                          {data.data.related_topics[keyword]?.top?.slice(0, 5).map((topic, index) => (
                            <Chip 
                              key={index} 
                              label={topic.topic_title} 
                              color="primary" 
                              variant="outlined" 
                            />
                          ))}
                        </Box>
                      </Box>
                    ))
                  ) : (
                    <Typography variant="body2" color="text.secondary">
                      No related topics found
                    </Typography>
                  )}
                </CardContent>
              </Card>
            </Grid>

            {/* Related Queries */}
            <Grid item xs={12} md={6}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Related Queries
                  </Typography>
                  {data?.data?.related_queries ? (
                    Object.keys(data.data.related_queries).map(keyword => (
                      <Box key={keyword} sx={{ mb: 3 }}>
                        <Typography variant="subtitle1">
                          For: {keyword}
                        </Typography>
                        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mt: 1 }}>
                          {data.data.related_queries[keyword]?.top?.slice(0, 5).map((query, index) => (
                            <Chip 
                              key={index} 
                              label={query.query} 
                              color="secondary" 
                              variant="outlined" 
                            />
                          ))}
                        </Box>
                      </Box>
                    ))
                  ) : (
                    <Typography variant="body2" color="text.secondary">
                      No related queries found
                    </Typography>
                  )}
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </Box>
      )}
    </Box>
  );
};

export default Search; 