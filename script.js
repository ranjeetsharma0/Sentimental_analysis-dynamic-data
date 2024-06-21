function sendMessage() {
    const userInput = document.getElementById('userInput');
    const chatMessages = document.getElementById('chatMessages');

    if (userInput.value.trim() !== "") {
        const userMessage = document.createElement('div');
        userMessage.classList.add('message', 'user-message');
        userMessage.textContent = userInput.value;
        chatMessages.appendChild(userMessage);

        const botMessage = document.createElement('div');
        botMessage.classList.add('message', 'bot-message');

        console.log(userInput.value);
        fetch("/Stues", {
            method: 'POST',
            headers: { 'Content-Type': 'text/plain' },
            body: userInput.value
        }).then(response => {
            return response.text()
        }).then(botAnswer => {
            botMessage.textContent = botAnswer;
            
        }).then(()=>{
            chatMessages.appendChild(botMessage);
        })
        userInput.value = "";
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
}


