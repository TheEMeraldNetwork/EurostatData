function verifyWebhook(req) {
    const VERIFY_TOKEN = process.env.VERIFY_TOKEN;
    
    const mode = req.query['hub.mode'];
    const token = req.query['hub.verify_token'];
    
    return mode === 'subscribe' && token === VERIFY_TOKEN;
}

module.exports = {
    verifyWebhook
}; 