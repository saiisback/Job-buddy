export const fetchQuestions = async (role) => {
    try {
        const response = await fetch('https://gemini.flash.api', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${process.env.GEMINI_API_KEY}` // Use the environment variable here
            },
            body: JSON.stringify({ role }),
        });

        if (!response.ok) throw new Error('Failed to fetch questions');
        return await response.json();
    } catch (error) {
        console.error('Error fetching questions:', error);
        return [];
    }
};