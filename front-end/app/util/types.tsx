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
    lista_entrevenientes: Entreveniente[] | undefined;
    lista_participantes: Participante[] | undefined;
    comentarios: string[] | undefined;
};

export type Entreveniente = {
    nome: string;
    email: string;
    data_nascimento: Date;
    tipo: Tipo;
};

export type Participante = {
    nome: string;
    email: string;
    data_nascimento: string;
    sexo: Sexo;
    nif: string;
    password: string;
    tipo: Tipo;
    codigo: string | undefined;
};

export type Evento = {
    id: number;
    nome_evento: string;
    data_evento: string;
    capacidade_evento: number;
    lista_atividades: Atividade[];
};
