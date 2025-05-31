export type Tipo = 'Admin' | 'Entreveniente' | 'Participante';

export type Sexo = 'Homem' | 'Mulher' | 'Outro' | 'Prefiro não dizer';

export const restricoesPossiveis = [
    'Sem restrições',
    'Idade mínima de 18 anos',
    'Idade mínima de 16 anos',
    'Idade mínima de 12 anos',
];

export type Atividade = {
    identificador: string;
    data_atividade: string;
    hora_atividade: string;
    descricao_atividade: string;
    localidade_atividade: string;
    restricoes: string;
    entrevenientes: Entreveniente[] | undefined;
    lista_participantes: Participante[] | undefined;
    comentarios: string[] | undefined;
};

export type Entreveniente = {
    nome_participante: string;
    email_participante: string;
    data_nascimento_participante: Date;
    tipo_participante: Tipo;
};

export type Participante = {
    nome_utilizador: string;
    email_utilizador: string;
    data_nascimento_utilizador: string;
    sexo: Sexo;
    nif_utilizador: string;
    password_utilizador: string;
    tipo_utilizador: Tipo;
    codigo_utilizador: string | undefined;
};

export type Evento = {
    id: number;
    nome_evento: string;
    data_evento: string;
    capacidade_evento: number;
    lista_atividades: Atividade[];
};
