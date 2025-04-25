const cron = require('node-cron');
const { OpenAI } = require('openai');
const { sendWhatsAppMessage, sendWhatsAppImage } = require('../services/whatsappService');
const { parseScheduleCommand } = require('../utils/commandParser');
const fs = require('fs');
const path = require('path');

const openai = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY
});

const scheduledTasks = new Map();

async function generateImage(prompt) {
    try {
        const response = await openai.images.generate({
            model: "dall-e-3",
            prompt: prompt,
            n: 1,
            size: "1024x1024",
        });
        return response.data[0].url;
    } catch (error) {
        console.error('Error generating image:', error);
        throw error;
    }
}

async function scheduleMessage(phoneNumber, message, schedule, imagePrompt = null) {
    const task = async () => {
        try {
            if (imagePrompt) {
                const imageUrl = await generateImage(imagePrompt);
                await sendWhatsAppImage(phoneNumber, imageUrl, message);
            } else {
                await sendWhatsAppMessage(phoneNumber, message);
            }
        } catch (error) {
            console.error('Error sending scheduled message:', error);
        }
    };

    if (schedule.type === 'recurring') {
        const cronJob = cron.schedule(schedule.cronExpression, task);
        scheduledTasks.set(`${phoneNumber}-${Date.now()}`, cronJob);
        return `Recurring message scheduled for ${schedule.cronExpression}`;
    } else {
        const taskId = `${phoneNumber}-${Date.now()}`;
        const timeoutId = setTimeout(task, schedule.delay);
        scheduledTasks.set(taskId, { timeoutId, type: 'timeout' });
        
        const scheduledDate = new Date(Date.now() + schedule.delay);
        return `Message scheduled for ${scheduledDate.toLocaleString()}`;
    }
}

async function getLinkedInPostSchedule() {
    try {
        // Look for the latest LinkedIn post plan file
        const filePattern = /linkedin_post_plan_2025_revised.*\.txt$/;
        const rootDir = path.resolve(__dirname, '../../');
        
        const files = fs.readdirSync(rootDir)
            .filter(file => filePattern.test(file))
            .map(file => ({
                name: file,
                path: path.join(rootDir, file),
                time: fs.statSync(path.join(rootDir, file)).mtime.getTime()
            }))
            .sort((a, b) => b.time - a.time);
        
        if (files.length === 0) {
            return "No LinkedIn post schedule found.";
        }
        
        // Read the most recent file
        const content = fs.readFileSync(files[0].path, 'utf8');
        
        // Get the next 3 upcoming posts
        const today = new Date();
        const upcomingPosts = [];
        
        const postRegex = /Post (\d+): ([^\n]+)\nDate: ([^\n]+)\n/g;
        let match;
        
        while ((match = postRegex.exec(content)) !== null) {
            const postDate = new Date(match[3]);
            if (postDate >= today) {
                upcomingPosts.push({
                    number: match[1],
                    title: match[2],
                    date: postDate
                });
                
                if (upcomingPosts.length >= 3) break;
            }
        }
        
        if (upcomingPosts.length === 0) {
            return "No upcoming LinkedIn posts found.";
        }
        
        // Format the response
        let response = "Upcoming LinkedIn posts:\n\n";
        upcomingPosts.forEach(post => {
            response += `Post ${post.number}: ${post.title}\nDate: ${post.date.toDateString()}\n\n`;
        });
        
        return response;
    } catch (error) {
        console.error('Error getting LinkedIn post schedule:', error);
        return "Error retrieving LinkedIn post schedule.";
    }
}

function getHelpText() {
    return `*WhatsApp Assistant Commands*

*Scheduling:*
- Schedule a message: \`schedule "Your message" tomorrow at 3pm\`
- Schedule with image: \`schedule "Your message" tomorrow at 3pm with image a cat playing piano\`
- Recurring options: \`schedule "Good morning!" every day 8am CET\`

*Image Generation:*
- Generate image: \`generate a landscape with mountains and a sunset\`

*LinkedIn Tools:*
- View upcoming posts: \`linkedin posts\`

*Help:*
- Show this menu: \`help\``;
}

async function handleMessage(message) {
    const text = message.text?.body;
    const from = message.from;

    if (!text) {
        return;
    }

    const lowerText = text.toLowerCase();

    try {
        if (lowerText.startsWith('schedule')) {
            const scheduleData = parseScheduleCommand(text);
            const resultMessage = await scheduleMessage(
                from,
                scheduleData.message,
                scheduleData.schedule,
                scheduleData.imagePrompt
            );
            await sendWhatsAppMessage(from, `✅ ${resultMessage}`);
        }
        else if (lowerText.startsWith('generate')) {
            const prompt = text.substring('generate'.length).trim();
            try {
                await sendWhatsAppMessage(from, '🎨 Generating your image, please wait...');
                const imageUrl = await generateImage(prompt);
                await sendWhatsAppImage(from, imageUrl, 'Here\'s your generated image!');
            } catch (error) {
                await sendWhatsAppMessage(from, '❌ Sorry, I couldn\'t generate the image. Please try again.');
            }
        }
        else if (lowerText === 'help' || lowerText === 'commands') {
            await sendWhatsAppMessage(from, getHelpText());
        }
        else if (lowerText === 'linkedin posts' || lowerText.includes('upcoming posts')) {
            const schedule = await getLinkedInPostSchedule();
            await sendWhatsAppMessage(from, schedule);
        }
        else {
            await sendWhatsAppMessage(from, `I didn't understand that command. Type 'help' to see available commands.`);
        }
    } catch (error) {
        console.error('Error handling message:', error);
        await sendWhatsAppMessage(from, 'Sorry, there was an error processing your request. Please try again.');
    }
}

module.exports = {
    handleMessage
}; 