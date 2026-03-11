const chatBox = document.getElementById("chatBox")
const input = document.getElementById("userInput")

function addMessage(text, sender){

    const message = document.createElement("div")
    message.classList.add("message")
    message.classList.add(sender)

    message.innerHTML = marked.parse(text)

    chatBox.appendChild(message)
    chatBox.scrollTop = chatBox.scrollHeight
}

async function sendMessage(){

    const text = input.value.trim()
    if(!text) return

    addMessage(text,"user")
    input.value=""

    const typing = document.createElement("div")
    typing.classList.add("message","bot")
    typing.innerText="Typing..."
    chatBox.appendChild(typing)

    try{

        const res = await fetch("http://127.0.0.1:8000/chat",{
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify({
                message:text
            })
        })

        const data = await res.json()

        typing.remove()

        // Show score reward first
        const scoreDiv = document.createElement("div")
        scoreDiv.classList.add("score-popup")
        scoreDiv.innerText = "+" + data.score_added + " SkillRank"
        chatBox.appendChild(scoreDiv)

        // Update total score in top bar
        document.getElementById("totalScore").innerText = data.total_score

        // Then show bot reply
        addMessage(data.reply,"bot")

    }catch(err){

        typing.remove()
        addMessage("Error connecting to server","bot")

    }
}

input.addEventListener("keypress",function(e){
    if(e.key==="Enter"){
        sendMessage()
    }
})