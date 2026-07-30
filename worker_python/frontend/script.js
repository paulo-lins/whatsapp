<!-- Script de Simulação de Navegação e Envio -->
    <script>
        const screenChats = document.getElementById('screen-chats');
        const screenChatRoom = document.getElementById('screen-chat-room');
        const chatMessages = document.getElementById('chat-messages');
        const inputMensagem = document.getElementById('input-mensagem');

        function abrirChat() {
            screenChats.classList.add('hidden');
            screenChatRoom.classList.remove('hidden');
        }

        function fecharChat() {
            screenChatRoom.classList.add('hidden');
            screenChats.classList.remove('hidden');
        }

        function getHoraAtual() {
            const agora = new Date();
            return agora.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        }

        async function enviarMensagem() {
            const texto = inputMensagem.value.trim();
            if (!texto) return;

            const horaEnvio = getHoraAtual();

            // Adiciona a mensagem do usuário na tela
            const msgUserHTML = `
                <div class="bg-[#d9fdd3] p-3 rounded-lg max-w-[80%] self-end shadow-sm text-sm text-gray-800 relative">
                    <p>${texto}</p>
                    <span class="text-[9px] text-gray-500 float-right mt-1 ml-2">${horaEnvio}</span>
                </div>
            `;
            chatMessages.insertAdjacentHTML('beforeend', msgUserHTML);
            inputMensagem.value = '';
            chatMessages.scrollTop = chatMessages.scrollHeight;

            // Faz a chamada real para o FastAPI
            try {
                const response = await fetch('http://127.0.0.1:8000/webhook/whatsapp', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ 
                        from_number: "5585999999999", 
                        message_body: texto 
                    })
                });

                const data = await response.json();
                const horaResposta = getHoraAtual();

                if (data.status === "sucesso") {
                    // Substitui quebras de linha por <br> para a formatação ficar perfeita no HTML
                    const respostaFormatada = data.resposta_whatsapp.replace(/\n/g, '<br>');

                    const msgBotHTML = `
                        <div class="bg-white p-3 rounded-lg max-w-[80%] self-start shadow-sm text-sm text-gray-800 relative">
                            <p>${respostaFormatada}</p>
                            <span class="text-[9px] text-gray-400 float-right mt-1 ml-2">${horaResposta}</span>
                        </div>
                    `;
                    chatMessages.insertAdjacentHTML('beforeend', msgBotHTML);
                } else {
                    const msgErroHTML = `
                        <div class="bg-white p-3 rounded-lg max-w-[80%] self-start shadow-sm text-sm text-red-600 relative">
                            <p>⚠️ Erro ao processar o caso no servidor.</p>
                            <span class="text-[9px] text-gray-400 float-right mt-1 ml-2">${horaResposta}</span>
                        </div>
                    `;
                    chatMessages.insertAdjacentHTML('beforeend', msgErroHTML);
                }
            } catch (error) {
                const horaErro = getHoraAtual();
                const msgErroConexaoHTML = `
                    <div class="bg-white p-3 rounded-lg max-w-[80%] self-start shadow-sm text-sm text-red-600 relative">
                        <p>⚠️ Erro de conexão com a API local do FastAPI.</p>
                        <span class="text-[9px] text-gray-400 float-right mt-1 ml-2">${horaErro}</span>
                    </div>
                `;
                chatMessages.insertAdjacentHTML('beforeend', msgErroConexaoHTML);
            }

            chatMessages.scrollTop = chatMessages.scrollHeight;
        }

        // Permitir envio com a tecla Enter
        inputMensagem.addEventListener('keypress', function (e) {
            if (e.key === 'Enter') {
                enviarMensagem();
            }
        });
    </script>