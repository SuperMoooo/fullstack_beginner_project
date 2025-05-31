'use client';
import Loading from '@/app/components/loading';
import Navbar from '@/app/components/Navbar';
import { Atividade, Evento, restricoesPossiveis } from '@/app/util/types';
import { useParams } from 'next/navigation';
import React, { use, useEffect, useState } from 'react';
import AtividadeCard from './atividade_card';
import QuestionModal from '@/app/components/question_modal';
import AtividadeForm from '@/app/components/atividade_form';
import Link from 'next/link';

export default function EventoDetalhes() {
    const params = useParams();
    const id = params.id;

    const [evento, setEvento] = useState<Evento>();
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<string>('');
    const [exportarLingua, setExportarLingua] = useState<string>('pt');

    // MODALS
    const [showDeleteEvento, setShowDeleteEvento] = useState<boolean>(false);
    const [showDeleteAtividade, setShowDeleteAtividade] =
        useState<boolean>(false);
    const [showExportarEvento, setShowExportarEvento] =
        useState<boolean>(false);

    // ATIVIDADES
    const [add_atividade, setAddAtividade] = useState<boolean>(false);
    const [descricaoAtividade, setDescricaoAtividade] = useState<string>('');
    const [dataAtividade, setDataAtividade] = useState<string>('');
    const [horaAtividade, setHoraAtividade] = useState<string>('');
    const [localAtividade, setLocalAtividade] = useState<string>('');
    const [restricoes, setRestricoes] = useState<string>('Sem restrições');
    const [errorAtividade, setErrorAtividade] = useState<string>('');
    const [atividadeIdentificador, setAtividadeIdentificador] =
        useState<string>('');
    const [totalParticipantes, setTotalParticipantes] = useState<number>(0);

    useEffect(() => {
        getEvento();
    }, []);

    const getEvento = async () => {
        try {
            setLoading(true);
            const token = localStorage.getItem('token');

            const response = await fetch(`http://127.0.0.1:5000/evento/${id}`, {
                method: 'GET',
                headers: {
                    Authorization: `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
            });
            if (response.ok) {
                const data = await response.json();
                setEvento(data);
                setError('');
                let total: number = 0;
                for (let i = 0; i < data['lista_atividades'].length; i++) {
                    total +=
                        data['lista_atividades'][i]['lista_participantes']
                            .length;
                }
                setTotalParticipantes(total);
            } else {
                const errorData = await response.json();
                setError(errorData['Erro'] ?? 'Erro desconhecido');
            }
        } catch (error: any) {
            if (error.message.includes('NetworkError')) {
                setError('Servidor Offline');
            } else {
                setError(error.message);
            }
        } finally {
            setLoading(false);
        }
    };

    // ABRIR MODAL PARA EDITAR ATIVIDADE
    const handleEditAtividade = (atividade: Atividade) => {
        setAtividadeIdentificador(atividade.identificador);
        setDescricaoAtividade(atividade.descricao_atividade);
        setDataAtividade(atividade.data_atividade);
        setHoraAtividade(atividade.hora_atividade);
        setLocalAtividade(atividade.localidade_atividade);
        setRestricoes(atividade.restricoes);
        setAddAtividade(true);
    };

    // ATUALIZAR ATIVIDADE
    const handleUpdateAtividade = async (e: any) => {
        try {
            e.preventDefault();
            setLoading(true);
            let day = dataAtividade.split('-')[2];
            let month = dataAtividade.split('-')[1].split('-')[0];
            let year = dataAtividade.split('-')[0];
            const atividadeDate = `${day}/${month}/${year}`;

            const token = localStorage.getItem('token');
            const response = await fetch(
                'http://127.0.0.1:5000/validar-atividade',
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        Authorization: `Bearer ${token}`,
                    },
                    body: JSON.stringify({
                        data_atividade: atividadeDate,
                        hora_atividade: horaAtividade,
                        descricao_atividade: descricaoAtividade,
                        localidade_atividade: localAtividade,
                        restricoes: restricoes,
                    }),
                }
            );
            if (response.ok) {
                const response2 = await fetch(
                    `http://127.0.0.1:5000/atualizar-atividade/${atividadeIdentificador}`,
                    {
                        method: 'PUT',
                        headers: {
                            Authorization: `Bearer ${token}`,
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            descricao_atividade: descricaoAtividade,
                            data_atividade: atividadeDate,
                            hora_atividade: horaAtividade,
                            localidade_atividade: localAtividade,
                            restricoes: restricoes,
                        }),
                    }
                );
                if (response2.ok) {
                    setAddAtividade(false);
                    getEvento();
                } else {
                    const errorData = await response.json();
                    setErrorAtividade(errorData['Erro'] ?? 'Erro desconhecido');
                }
            } else {
                const errorData = await response.json();
                setErrorAtividade(errorData['Erro'] ?? 'Erro desconhecido');
            }
        } catch (error: any) {
            if (error.message.includes('NetworkError')) {
                setErrorAtividade('Servidor Offline');
            } else {
                setErrorAtividade(error.message);
            }
        } finally {
            setLoading(false);
        }
    };

    const handleDeleteAtividade = async () => {
        try {
            setLoading(true);
            const token = localStorage.getItem('token');
            const response = await fetch(
                `http://127.0.0.1:5000/eliminar-atividade/${atividadeIdentificador}`,
                {
                    method: 'PUT',
                    headers: {
                        Authorization: `Bearer ${token}`,
                        'Content-Type': 'application/json',
                    },
                }
            );
            if (response.ok) {
                setShowDeleteAtividade(false);
                getEvento();
            } else {
                const errorData = await response.json();
                setError(errorData['Erro'] ?? 'Erro desconhecido');
            }
        } catch (error: any) {
            if (error.message.includes('NetworkError')) {
                setError('Servidor Offline');
            } else {
                setError(error.message);
            }
        } finally {
            setLoading(false);
        }
    };

    const handleDeleteEvento = async () => {
        try {
            setLoading(true);
            const token = localStorage.getItem('token');
            const response = await fetch(
                `http://127.0.0.1:5000/eliminar-evento/${id}`,
                {
                    method: 'DELETE',
                    headers: {
                        Authorization: `Bearer ${token}`,
                        'Content-Type': 'application/json',
                    },
                }
            );
            if (response.ok) {
                setShowDeleteEvento(false);
                window.location.href = '/';
            } else {
                const errorData = await response.json();
                setError(errorData['Erro'] ?? 'Erro desconhecido');
            }
        } catch (error: any) {
            if (error.message.includes('NetworkError')) {
                setError('Servidor Offline');
            } else {
                setError(error.message);
            }
        } finally {
            setLoading(false);
        }
    };

    const handleExportEvento = async () => {
        try {
            setLoading(true);
            const token = localStorage.getItem('token');
            const response = await fetch(
                `http://127.0.0.1:5000/exportar-evento-pdf/${id}/${exportarLingua}`,
                {
                    method: 'GET',
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }
            );
            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const link = document.createElement('a');
                link.href = url;
                link.setAttribute('download', 'evento.pdf');
                document.body.appendChild(link);
                link.click();
                link.parentNode?.removeChild(link);
            } else {
                const errorData = await response.json();
                setError(errorData['Erro'] ?? 'Erro desconhecido');
            }
        } catch (error: any) {
            if (error.message.includes('NetworkError')) {
                setError('Servidor Offline');
            } else {
                setError(error.message);
            }
        } finally {
            setLoading(false);
        }
    };
    return (
        <main className="grid grid-rows-[auto_1fr] min-h-[100dvh]">
            <Navbar goBack={true} />
            <section className="flex items-start justify-center p-20">
                {loading ? (
                    <Loading />
                ) : (
                    <article className="flex flex-col gap-2 p-4 items-start justify-center w-full">
                        <div className="flex justify-between items-center w-full">
                            <h1 className="text-4xl font-bold">
                                {evento?.nome_evento}
                            </h1>
                            <div className="flex items-center justify-center gap-4">
                                <button
                                    onClick={() =>
                                        setShowExportarEvento((prev) => !prev)
                                    }
                                    className="cursor-pointer transition duration-300 bg-orange-500 hover:bg-orange-900 text-white font-bold py-2 px-4 rounded mt-5"
                                >
                                    Exportar Evento PDF
                                </button>
                                <Link
                                    href={{
                                        pathname: `/eventos/atualizar-evento/${id}`,
                                    }}
                                    className="cursor-pointer transition duration-300 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-5"
                                >
                                    Editar Evento
                                </Link>
                                <button
                                    onClick={() =>
                                        setShowDeleteEvento((prev) => !prev)
                                    }
                                    className="cursor-pointer transition duration-300 bg-red-500 hover:bg-red-900 text-white font-bold py-2 px-4 rounded mt-5"
                                >
                                    Eliminar Evento
                                </button>
                            </div>
                        </div>
                        <div className="w-full h-[2px] bg-gray-200"></div>
                        <h2 className="text-xl opacity-70">
                            {evento?.data_evento} | {totalParticipantes}/
                            {evento?.capacidade_evento}
                        </h2>
                        <section className="flex flex-col gap-4 items-start justify-center mt-6">
                            <h1 className="text-2xl">Atividades</h1>
                            <aside className="flex items-center justify-start gap-2">
                                {evento?.lista_atividades.map(
                                    (atividade, index) => (
                                        <AtividadeCard
                                            key={index}
                                            atividade={atividade}
                                            editavel={true}
                                            eliminavel={true}
                                            onEdit={() =>
                                                handleEditAtividade(atividade)
                                            }
                                            onDelete={() => {
                                                setAtividadeIdentificador(
                                                    atividade.identificador
                                                );
                                                setShowDeleteAtividade(true);
                                            }}
                                        />
                                    )
                                )}
                            </aside>
                        </section>
                    </article>
                )}
                {add_atividade && (
                    <AtividadeForm
                        title={`Editar Atividade`}
                        handleSubmit={handleUpdateAtividade}
                        setAddAtividade={setAddAtividade}
                        descricaoAtividade={descricaoAtividade}
                        setDescricaoAtividade={setDescricaoAtividade}
                        dataAtividade={dataAtividade}
                        setDataAtividade={setDataAtividade}
                        horaAtividade={horaAtividade}
                        setHoraAtividade={setHoraAtividade}
                        localAtividade={localAtividade}
                        setLocalAtividade={setLocalAtividade}
                        restricoesPossiveis={restricoesPossiveis}
                        setRestricoes={setRestricoes}
                        restricaoInicial={restricoes}
                        errorAtividade={errorAtividade}
                        nomeBotao="Salvar Atividade"
                    />
                )}
            </section>
            <QuestionModal
                title="Eliminar Evento"
                message="Tem certeza que deseja eliminar este evento?"
                onConfirm={handleDeleteEvento}
                onCancel={() => setShowDeleteEvento((prev: boolean) => !prev)}
                show={showDeleteEvento}
            />
            <QuestionModal
                title="Eliminar Atividade"
                message="Tem certeza que deseja eliminar esta atividade?"
                onConfirm={handleDeleteAtividade}
                onCancel={() =>
                    setShowDeleteAtividade((prev: boolean) => !prev)
                }
                show={showDeleteAtividade}
            />
            {showExportarEvento && (
                <main className="fixed flex items-center justify-center h-screen w-screen bg-black/50">
                    <section className="w-fit flex flex-col gap-6 items-center justify-center *:text-center bg-white rounded-2xl p-6">
                        <div
                            className="self-end cursor-pointer text-4xl"
                            onClick={() =>
                                setShowExportarEvento((prev) => !prev)
                            }
                        >
                            X
                        </div>
                        <h1 className="text-2xl self-start">
                            Escolha a linguagem:
                        </h1>
                        <div className="flex items-center justify-center gap-4 *:cursor-pointer *:transition *:duration-300 *:border *:border-blue-500 *:hover:border-blue-900 *:text-black *:font-bold *:py-2 *:px-4 *:rounded ">
                            <button
                                onClick={() => setExportarLingua('pt')}
                                className={`${
                                    exportarLingua == 'pt' &&
                                    'border-3! border-green-500!'
                                }`}
                            >
                                🇵🇹 Português
                            </button>
                            <button
                                onClick={() => setExportarLingua('en')}
                                className={`${
                                    exportarLingua == 'en' &&
                                    'border-3! border-green-500!'
                                }`}
                            >
                                🇬🇧 Inglês
                            </button>

                            <button
                                onClick={() => setExportarLingua('it')}
                                className={`${
                                    exportarLingua == 'it' &&
                                    'border-3! border-green-500!'
                                }`}
                            >
                                🇮🇹 Italiano
                            </button>
                        </div>
                        <button
                            type="button"
                            onClick={handleExportEvento}
                            className="cursor-pointer transition duration-300 border bg-blue-500 hover:bg-blue-900 text-white font-bold py-2 px-4 rounded self-end"
                        >
                            Exportar
                        </button>
                    </section>
                </main>
            )}
        </main>
    );
}
