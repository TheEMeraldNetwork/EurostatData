const chrono = require('chrono-node');

function parseScheduleCommand(text) {
    const parts = text.substring('schedule'.length).trim().split(' with image ');
    const messageAndTime = parts[0];
    const imagePrompt = parts.length > 1 ? parts[1].trim() : null;

    // Extract message content (text between quotes)
    const messageMatch = messageAndTime.match(/"([^"]+)"/);
    if (!messageMatch) {
        throw new Error('Message must be enclosed in quotes');
    }
    const message = messageMatch[1];

    // Remove the message from the string to parse the time
    const timeString = messageAndTime.replace(/"[^"]+"/, '').trim();

    let schedule;
    if (timeString.startsWith('every')) {
        // Handle recurring schedule
        const recurringPattern = timeString.substring('every'.length).trim();
        schedule = parseRecurringSchedule(recurringPattern);
    } else {
        // Handle one-time schedule
        const date = chrono.parseDate(timeString);
        if (!date) {
            throw new Error('Invalid date/time format');
        }
        
        // Ensure the date is in the future
        if (date.getTime() <= Date.now()) {
            throw new Error('Scheduled time must be in the future');
        }
        
        schedule = {
            type: 'one-time',
            delay: date.getTime() - Date.now()
        };
    }

    return {
        message,
        schedule,
        imagePrompt
    };
}

function parseRecurringSchedule(pattern) {
    // Extract day of week, time, and timezone if provided
    const timeMatch = pattern.match(/(\d{1,2}):(\d{2})\s*(am|pm)?/i);
    const dayMatch = pattern.match(/monday|tuesday|wednesday|thursday|friday|saturday|sunday/i);
    
    // Common patterns
    const commonPatterns = {
        'day 8am cet': '0 8 * * *',
        'day 8am': '0 8 * * *',
        'day 9am cet': '0 9 * * *',
        'day 9am': '0 9 * * *',
        'morning 8am cet': '0 8 * * *',
        'morning 8am': '0 8 * * *',
        'day': '0 8 * * *', // Default to 8am if only day is specified
        'week': '0 8 * * 1', // Every Monday at 8am
        'monday': '0 8 * * 1',
        'tuesday': '0 8 * * 2',
        'wednesday': '0 8 * * 3',
        'thursday': '0 8 * * 4',
        'friday': '0 8 * * 5',
        'saturday': '0 8 * * 6',
        'sunday': '0 8 * * 0',
        'weekday': '0 8 * * 1-5', // Monday through Friday at 8am
        'weekend': '0 10 * * 0,6', // Saturday and Sunday at 10am
        'month': '0 8 1 * *' // First day of every month at 8am
    };
    
    // First check if pattern exactly matches a common pattern
    const patternLower = pattern.toLowerCase();
    if (commonPatterns[patternLower]) {
        return {
            type: 'recurring',
            cronExpression: commonPatterns[patternLower]
        };
    }
    
    // Try to construct a cron expression from components
    let hour = 8; // Default hour
    let minute = 0; // Default minute
    let dayOfWeek = '*'; // Default is every day
    
    // Extract time if provided
    if (timeMatch) {
        hour = parseInt(timeMatch[1], 10);
        minute = parseInt(timeMatch[2], 10);
        
        // Handle AM/PM
        if (timeMatch[3] && timeMatch[3].toLowerCase() === 'pm' && hour < 12) {
            hour += 12;
        }
        
        // Handle 12 AM as 0
        if (timeMatch[3] && timeMatch[3].toLowerCase() === 'am' && hour === 12) {
            hour = 0;
        }
    }
    
    // Extract day of week if provided
    if (dayMatch) {
        const days = {
            'sunday': 0,
            'monday': 1,
            'tuesday': 2,
            'wednesday': 3,
            'thursday': 4,
            'friday': 5,
            'saturday': 6
        };
        
        dayOfWeek = days[dayMatch[0].toLowerCase()];
    }
    
    // Construct cron expression
    const cronExpression = `${minute} ${hour} * * ${dayOfWeek}`;
    
    return {
        type: 'recurring',
        cronExpression
    };
}

module.exports = {
    parseScheduleCommand
}; 