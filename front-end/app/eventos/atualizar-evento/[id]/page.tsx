'use client';
import Loading from '@/app/components/loading';
import Navbar from '@/app/components/Navbar';
import TitleInput from '@/app/components/title_input';
import { Atividade, restricoesPossiveis } from '@/app/util/types';
import React, { useEffect, useState } from 'react';
import AtividadeCard from '../../[id]/atividade_card';
import AtividadeForm from '@/app/components/atividade_form';
import { useParams } from 'next/navigation';

export default function AtualizarEvento() {
    // PARAMS
    const params = useParams();
    const id = params.id;
    // EVENTO
    const [loading, setLoading] = useState<boolean>(false);
    const [nomeEvento, setNomeEvento] = useState<string>('');
    const [dataEvento, setDataEvento] = useState<string>('');
    const [capacidadeEvento, setCapacidadeEvento] = useState<number>(1);
    const [error, setError] = useState<string>('');

    // ATIVIDADES
    const [atividades, setAtividades] = useState<Atividade[]>([]);
    const [add_atividade, setAddAtividade] = useState<boolean>(false);
    const [descricaoAtividade, setDescricaoAtividade] = useState<string>('');
    const [dataAtividade, setDataAtividade] = useState<string>('');
    const [horaAtividade, setHoraAtividade] = useState<string>('');
    const [localAtividade, setLocalAtividade] = useState<string>('');
    const [restricoes, setRestricoes] = useState<string>('Sem restrições');
    const [errorAtividade, setErrorAtividade] = useState<string>('');

    useEffect(() => {
        getEvento();
    }, []);

    const getEvento = async () => {
        try {
            setLoading(true);
            const token = localStorage.getItem('token');
            const limite = localStorage.getItem('token_limite');
            if (token && limite && Date.now() < parseInt(limite, 10)) {
                const response = await fetch(
                    `http://127.0.0.1:5000/evento/${id}`,
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
                    console.log(data);
                    setNomeEvento(data['nome_evento']);
                    setCapacidadeEvento(data['capacidade_evento']);
                    setDataEvento(data['data_evento']);
                    setAtividades(data['lista_atividades']);
                    setError('');
                } else {
                    const errorData = await response.json();
                    setError(errorData['Erro'] ?? 'Erro desconhecido');
                }
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

    // CRIAR EVENTO
    const handleUpdateEvento = async (e: any) => {
        try {
            e.preventDefault();
            let day = dataEvento.split('-')[2];
            let month = dataEvento.split('-')[1].split('-')[0];
            let year = dataEvento.split('-')[0];
            const eventDate = `${day}/${month}/${year}`;
            setLoading(true);
            const token = localStorage.getItem('token');
            const tipo = localStorage.getItem('tipo');
            const response = await fetch('http://127.0.0.1:5000/criar-evento', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${token}`,
                },
                body: JSON.stringify({
                    user_tipo: tipo,
                    nome_evento: nomeEvento,
                    data_evento: eventDate,
                    capacidade_evento: capacidadeEvento,
                    lista_atividades: atividades,
                }),
            });
            if (response.ok) {
                alert('Evento criado com sucesso');
                window.location.href = '/';
            } else {
                const errorData = await response.json();
                setError(errorData['Erro'] || 'Erro desconhecido');
            }
        } catch (error: any) {
            setError(error.message);
        } finally {
            setLoading(false);
        }
    };
    // CRIAR E VALIDAR ATIVIDADE
    const handleCreateAtividade = async (e: any) => {
        try {
            e.preventDefault();
            let day = dataAtividade.split('-')[2];
            let month = dataAtividade.split('-')[1].split('-')[0];
            let year = dataAtividade.split('-')[0];
            const atividadeDate = `${day}/${month}/${year}`;
            setLoading(true);
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
                let novasAtividades;

                novasAtividades = [
                    ...atividades,
                    {
                        data_atividade: atividadeDate,
                        hora_atividade: horaAtividade,
                        descricao_atividade: descricaoAtividade,
                        localidade_atividade: localAtividade,
                        restricoes: restricoes,
                    } as Atividade,
                ];

                setAtividades(novasAtividades);
                setAddAtividade(false);
                setDescricaoAtividade('');
                setDataAtividade('');
                setHoraAtividade('');
                setLocalAtividade('');
                setRestricoes('Sem restrições');
                setErrorAtividade('');
            } else {
                const errorData = await response.json();
                setErrorAtividade(errorData['Erro'] || 'Erro desconhecido');
            }
        } catch (error: any) {
            setErrorAtividade(error.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <main className="grid grid-rows-[auto_1fr] min-h-[100dvh]">
            <Navbar goBack={true} />
            <form
                className="flex items-center justify-start gap-6 flex-col w-full p-20"
                onSubmit={handleUpdateEvento}
            >
                <aside className="flex items-center justify-start w-full gap-6">
                    <TitleInput
                        titulo="Nome do Evento"
                        valor={nomeEvento}
                        setValor={setNomeEvento}
                        error={error.includes('nome')}
                    />
                    <TitleInput
                        titulo="Capacidade do Evento"
                        valor={capacidadeEvento}
                        setValor={setCapacidadeEvento}
                        inputType="number"
                        error={error.includes('capacidade')}
                    />
                    <TitleInput
                        titulo="Data do Evento"
                        valor={dataEvento}
                        setValor={setDataEvento}
                        inputType="date"
                        error={error.includes('data')}
                    />
                </aside>
                {atividades.length > 0 && (
                    <h1 className="text-xl self-start">Atividades</h1>
                )}
                <aside className="flex items-center justify-start w-full gap-4">
                    {atividades.map((atividade: Atividade, index: number) => (
                        <AtividadeCard
                            key={index}
                            atividade={atividade}
                            eliminavel={true}
                            onDelete={() => {
                                setAtividades(
                                    atividades.filter(
                                        (ativi: Atividade) =>
                                            ativi.identificador !==
                                            atividade.identificador
                                    )
                                );
                                setDataAtividade('');
                                setHoraAtividade('');
                                setLocalAtividade('');
                                setDescricaoAtividade('');
                                setRestricoes('Sem restrições');
                                setErrorAtividade('');
                            }}
                        />
                    ))}
                    <button
                        type="button"
                        onClick={() => setAddAtividade((prev: any) => !prev)}
                        className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded cursor-pointer"
                    >
                        Adicionar Atividade
                    </button>
                </aside>
                <button
                    type="submit"
                    className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded cursor-pointer"
                >
                    Salvar Evento
                </button>
                {error && !error.includes('undefined') && (
                    <p className="text-red-500">{error}</p>
                )}
            </form>
            {add_atividade && (
                <AtividadeForm
                    title="Nova Atividade"
                    handleSubmit={handleCreateAtividade}
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
                    nomeBotao="Salvar"
                />
            )}
            {loading && <Loading />}
        </main>
    );
}
