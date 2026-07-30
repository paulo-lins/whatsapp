-- Criação dos Tipos Enumerados (ENUM) para garantir consistência
CREATE TYPE tipo_remetente AS ENUM ('cliente', 'bot', 'advogado');
CREATE TYPE status_atendimento AS ENUM ('triagem', 'encaminhado', 'finalizado');

-- 1. Tabela de Usuários (Clientes)
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(150),
    telefone VARCHAR(20) UNIQUE NOT NULL,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Tabela de Advogados (Especialistas simulados)
CREATE TABLE advogados (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    especialidade VARCHAR(100) NOT NULL,
    whatsapp VARCHAR(20) NOT NULL,
    disponivel BOOLEAN DEFAULT TRUE,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Tabela de Atendimentos (Sessões de conversa)
CREATE TABLE atendimentos (
    id SERIAL PRIMARY KEY,
    usuario_id INT REFERENCES usuarios(id),
    advogado_id INT REFERENCES advogados(id),
    categoria_inferida VARCHAR(100),
    status status_atendimento DEFAULT 'triagem',
    resumo_ia TEXT,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Tabela de Mensagens (Onde o texto bruto é persistido)
CREATE TABLE mensagens (
    id SERIAL PRIMARY KEY,
    atendimento_id INT REFERENCES atendimentos(id) ON DELETE CASCADE,
    remetente tipo_remetente NOT NULL,
    conteudo TEXT NOT NULL,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Inserindo alguns advogados iniciais para simulação de triagem
INSERT INTO advogados (nome, especialidade, whatsapp) VALUES
('Dr. Carlos Silva', 'Direito Trabalhista', '5585999991111'),
('Dra. Ana Souza', 'Direito de Família', '5585999992222'),
('Dr. Roberto Mendes', 'Direito Civil e Consumidor', '5585999993333');