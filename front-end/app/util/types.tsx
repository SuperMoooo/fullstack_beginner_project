export type Tipo = 'admin' | 'user' | 'participante';

export type Atividade = {
    data_atividade: string;
    hora_atividade: string;
    descricao_atividade: string;
    localidade_atividade: string;
    participantes: Participante[];
};

export type Participante = {
    nome_participante: string;
    email_participante: string;
    data_nascimento_participante: Date;
    tipo_participante: Tipo;
};

export type User = {
    nome_utilizador: string;
    email_utilizador: string;
    data_nascimento_utilizador: string;
    password_utilizador: string;
    tipo_utilizador: Tipo;
    nif_utilizador: string;
    codigo_utilizador: string | undefined;
};

export type Evento = {
    id: number;
    nome_evento: string;
    data_evento: string;
    lista_atividades: Atividade[];
    lista_utilizadores: User[] | undefined;
    comentarios: string[] | undefined;
};
