import React from 'react';
import { 
  Typography, 
  Box, 
  Paper, 
  Card, 
  CardContent, 
  Switch, 
  FormControlLabel, 
  Divider,
  TextField,
  Button,
  Grid
} from '@mui/material';

const Settings = () => {
  return (
    <Box sx={{ mt: 3 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Settings
      </Typography>
      
      <Paper sx={{ p: 3, mb: 4 }}>
        <Typography variant="h5" gutterBottom>
          Application Settings
        </Typography>
        <Divider sx={{ mb: 3 }} />
        
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <FormControlLabel
              control={<Switch defaultChecked />}
              label="Enable automatic trend updates"
            />
          </Grid>
          
          <Grid item xs={12}>
            <FormControlLabel
              control={<Switch defaultChecked />}
              label="Store search history"
            />
          </Grid>
          
          <Grid item xs={12}>
            <FormControlLabel
              control={<Switch />}
              label="Dark mode (coming soon)"
              disabled
            />
          </Grid>
        </Grid>
      </Paper>
      
      <Card sx={{ mb: 4 }}>
        <CardContent>
          <Typography variant="h5" gutterBottom>
            Default Search Settings
          </Typography>
          <Divider sx={{ mb: 3 }} />
          
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <TextField
                label="Default Region"
                defaultValue="IT"
                fullWidth
                disabled
                helperText="In the full implementation, this will be configurable"
              />
            </Grid>
            
            <Grid item xs={12} md={6}>
              <TextField
                label="Default Timeframe"
                defaultValue="Past 3 Months"
                fullWidth
                disabled
                helperText="In the full implementation, this will be configurable"
              />
            </Grid>
          </Grid>
        </CardContent>
      </Card>
      
      <Box sx={{ display: 'flex', justifyContent: 'flex-end', mt: 2 }}>
        <Button variant="contained" color="primary" sx={{ mr: 2 }}>
          Save Settings
        </Button>
        <Button variant="outlined">
          Reset to Defaults
        </Button>
      </Box>
    </Box>
  );
};

export default Settings; 