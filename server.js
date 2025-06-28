const express = require('express');
const cors = require('cors');
const axios = require('axios');

const app = express();
app.use(cors());
app.use(express.json());

const PORT = 5000;
const OPENAI_API_KEY = 'sk-...aJIA';

app.post('/chat', async (req, res) => {
    const userMessage = req.body.message;

    try {
        const response = await axios.post('https://api.openai.com/v1/chat/completions', {
            model: 'gpt-3.5-turbo',
            messages: [
                { role: 'system', content: 'You are a fitness and health assistant. ONLY answer questions related to fitness, exercise, nutrition, recovery, injury prevention, and health. If asked something outside of these topics, politely refuse and remind the user that you can only discuss fitness and health.' },
                { role: 'user', content: userMessage }
            ],
            max_tokens: 500,
        }, {
            headers: {
                'Authorization': `Bearer ${OPENAI_API_KEY}`,
                'Content-Type': 'application/json'
            }
        });

        const aiReply = response.data.choices[0].message.content;
        res.json({ reply: aiReply });

    } catch (error) {
        console.error('Error contacting OpenAI:', error.message);
        res.status(500).json({ reply: 'Sorry, something went wrong. Please try again later.' });
    }
});

app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));
