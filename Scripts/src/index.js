require('dotenv').config();
const express = require('express');
const { handleMessage } = require('./handlers/messageHandler');
const { verifyWebhook } = require('./utils/webhookVerifier');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

// Webhook verification endpoint
app.get('/webhook', (req, res) => {
    const verified = verifyWebhook(req);
    if (verified) {
        res.status(200).send(req.query['hub.challenge']);
    } else {
        res.sendStatus(403);
    }
});

// Webhook message handling endpoint
app.post('/webhook', async (req, res) => {
    try {
        const { entry } = req.body;
        
        if (!entry || !entry[0].changes || !entry[0].changes[0].value.messages) {
            return res.sendStatus(200);
        }

        const message = entry[0].changes[0].value.messages[0];
        await handleMessage(message);
        
        res.sendStatus(200);
    } catch (error) {
        console.error('Error processing webhook:', error);
        res.sendStatus(500);
    }
});

app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
}); 