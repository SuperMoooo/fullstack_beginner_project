'use client';
import TitleInput from '@/app/components/title_input';
import { Atividade, Tipo } from '@/app/util/types';
import React, { useEffect, useState } from 'react';

export default function AtividadeCard({
    atividade,
    editavel,
    eliminavel,
    userNome,
    onEdit,
    onDelete,
    tipo,
    addEntreveniente,
    addParticipante,
    revomerEntreveniente,
    revomerParticipante,
    validarParticipante,
    handleComentar,
}: {
    atividade: Atividade;
    editavel?: boolean;
    eliminavel?: boolean;
    userNome?: string;
    onEdit?: () => void;
    onDelete?: () => void;
    tipo?: Tipo;
    addEntreveniente?: () => void;
    addParticipante?: () => void;
    revomerEntreveniente?: () => void;
    revomerParticipante?: () => void;
    validarParticipante?: () => void;
    handleComentar: (id: string, comentario: string) => void;
}) {
    const [userCode, setUserCode] = useState<string>('');
    const [comentario, setComentario] = useState<string>('');
    const estaNaListaEntrevenientes = atividade.lista_entrevenientes?.some(
        (entreveniente) => entreveniente.nome === userNome
    );

    const estaNaListaParticipantes = atividade.lista_participantes?.some(
        (entreveniente) => entreveniente.nome === userNome
    );

    const participante = atividade.lista_participantes?.find(
        (p) => p.nome === userNome
    );
    let codigo = null;
    if (participante) {
        codigo =
            participante.codigos?.find((cod) =>
                cod.includes(atividade.identificador)
            ) ?? '';
    }
    useEffect(() => {
        const getUserCode = async () => {
            try {
                const token = localStorage.getItem('token');
                const nome = localStorage.getItem('user_nome');
                const response = await fetch(
                    `http://127.0.0.1:5000/receber-codigos/${nome}`,
                    {
                        method: 'GET',
                        headers: {
                            Authorization: `Bearer ${token}`,
                            'Content-Type': 'application/json',
                        },
                    }
                );
                if (response.ok) {
                    const data = await response.json();
                    setUserCode(
                        data['codigos'].find((cod: string) =>
                            cod.includes(atividade.identificador)
                        ) ?? ''
                    );
                }
            } catch (error: any) {
                console.log(error.message);
            }
        };
        getUserCode();
    }, [codigo]);

    return (
        <div className="border border-gray-300 p-6 rounded-2xl gap-2 flex flex-col">
            <h1>{atividade.descricao_atividade}</h1>
            <div className="w-full h-[1px] bg-gray-300"></div>
            <h2>
                {atividade.data_atividade} | {atividade.hora_atividade} |{' '}
                {atividade.localidade_atividade}
            </h2>
            <div className="w-full h-[1px] bg-gray-300"></div>
            <h2>{atividade.restricoes}</h2>
            {(atividade.lista_entrevenientes?.length ?? 0) > 0 && (
                <>
                    <div className="w-full h-[1px] bg-gray-300"></div>
                    <h2>Entrevenientes:</h2>
                    <div className="flex flex-col gap-2">
                        {atividade.lista_entrevenientes!.map(
                            (entreveniente, index) => (
                                <h2 key={entreveniente.nome + index}>
                                    {entreveniente.nome}
                                </h2>
                            )
                        )}
                    </div>
                </>
            )}
            {(atividade.comentarios?.length ?? 0) > 0 && (
                <>
                    <div className="w-full h-[1px] bg-gray-300"></div>
                    <h2>Comentários:</h2>
                    <div className="flex flex-col gap-2">
                        {atividade.comentarios!.map((comentario, index) => (
                            <div
                                key={comentario.comentario + index}
                                className="flex flex-col items-start gap-2"
                            >
                                <h2>{comentario.nome}:</h2>
                                <h3>{comentario.comentario}</h3>
                            </div>
                        ))}
                    </div>
                </>
            )}

            {eliminavel && tipo === 'Admin' && (
                <>
                    <div className="w-full h-[1px] bg-gray-300"></div>
                    <div className="flex items-center justify-center gap-4">
                        {editavel && (
                            <button
                                type="button"
                                onClick={onEdit}
                                className="cursor-pointer transition duration-300 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-5"
                            >
                                Editar Atividade
                            </button>
                        )}
                        <button
                            type="button"
                            onClick={onDelete}
                            className="cursor-pointer transition duration-300 bg-red-500 hover:bg-red-900 text-white font-bold py-2 px-4 rounded mt-5"
                        >
                            Eliminar Atividade
                        </button>
                    </div>
                </>
            )}
            {tipo === 'Entreveniente' &&
                (estaNaListaEntrevenientes ? (
                    <button
                        type="button"
                        onClick={revomerEntreveniente}
                        className="cursor-pointer transition duration-300 bg-red-500 hover:bg-red-900 text-white font-bold py-2 px-4 rounded mt-5"
                    >
                        Deixar de Participar
                    </button>
                ) : (
                    <button
                        type="button"
                        onClick={addEntreveniente}
                        className="cursor-pointer transition duration-300 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-5"
                    >
                        Ser Participante
                    </button>
                ))}

            {tipo === 'Participante' &&
                (estaNaListaParticipantes && !userCode?.includes('VALIDADO') ? (
                    <>
                        <button
                            type="button"
                            onClick={revomerParticipante}
                            className="cursor-pointer transition duration-300 bg-red-500 hover:bg-red-900 text-white font-bold py-2 px-4 rounded mt-5"
                        >
                            Deixar de Inscrever
                        </button>
                        <h1>Código para entrada:</h1>
                        <h3>{codigo ?? ''}</h3>
                        <button
                            type="button"
                            onClick={validarParticipante}
                            className="cursor-pointer transition duration-300 bg-green-500 hover:bg-green-600 text-black  py-2 px-4 rounded mt-5"
                        >
                            Entrar / Validar Atividade
                        </button>
                    </>
                ) : userCode?.includes('VALIDADO') ? (
                    <div>
                        <TitleInput
                            titulo="Comentar"
                            valor={comentario}
                            setValor={setComentario}
                        />
                        <button
                            onClick={() => {
                                handleComentar(
                                    atividade.identificador,
                                    comentario
                                );
                                setComentario('');
                            }}
                            type="button"
                            className="cursor-pointer transition duration-300 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-5"
                        >
                            Comentar
                        </button>
                    </div>
                ) : (
                    <button
                        type="button"
                        onClick={addParticipante}
                        className="cursor-pointer transition duration-300 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-5"
                    >
                        Inscrever-se
                    </button>
                ))}
        </div>
    );
}
