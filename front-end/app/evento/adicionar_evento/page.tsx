'use client';
import Loading from '@/app/components/loading';
import Navbar from '@/app/components/Navbar';
import TitleInput from '@/app/components/title_input';
import { Atividade } from '@/app/util/types';
import React, { useEffect, useState } from 'react';

export default function AdicionarEvento() {
    const [loading, setLoading] = useState<boolean>(false);
    const [nomeEvento, setNomeEvento] = useState<string>('');
    const [dataEvento, setDataEvento] = useState<string>('');
    // ATIVIDADES
    const [atividades, setAtividades] = useState<Atividade[]>([]);
    const [add_atividade, setAddAtividade] = useState<boolean>(false);
    const [nomeAtividade, setNomeAtividade] = useState<string>('');

    const handleCreateEvento = async (e: any) => {
        try {
            e.preventDefault();
            let day = dataEvento.split('-')[2];
            let month = dataEvento.split('-')[1].split('-')[0];
            let year = dataEvento.split('-')[0];
            const eventDate = `${day}/${month}/${year}`;
            setLoading(true);
        } catch (error) {
            alert('Erro ao criar evento');
        } finally {
            setLoading(false);
        }
    };
    return (
        <main className="grid grid-rows-[auto_1fr] min-h-[100dvh]">
            <Navbar />
            <form
                className="flex items-center justify-start gap-6 flex-col w-full p-20"
                onSubmit={handleCreateEvento}
            >
                <aside className="flex items-center justify-start w-full gap-6">
                    <TitleInput
                        titulo="Nome do Evento"
                        valor={nomeEvento}
                        setValor={setNomeEvento}
                    />
                    <TitleInput
                        titulo="Data do Evento"
                        valor={dataEvento}
                        setValor={setDataEvento}
                        inputType="date"
                    />
                </aside>
                <aside className="flex items-center justify-start w-full gap-6">
                    {atividades.map((atividade: any, index: number) => (
                        <div key={index}></div>
                    ))}
                    <button
                        type="button"
                        onClick={() => setAddAtividade(!add_atividade)}
                        className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded cursor-pointer"
                    >
                        Adicionar Atividade
                    </button>
                </aside>
                <button
                    type="submit"
                    className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded cursor-pointer"
                >
                    Criar Evento
                </button>
            </form>
            {add_atividade && (
                <section className="top-0 left-0 fixed w-screen h-screen flex items-center justify-center ">
                    <div className="bg-black opacity-60 top-0 left-0 fixed h-screen w-screen -z-10"></div>

                    <form className="flex items-end justify-center gap-6 flex-col w-1/3 p-10 bg-white rounded-2xl">
                        <button
                            className="text-5xl cursor-pointer"
                            type="button"
                            onClick={() => setAddAtividade(!add_atividade)}
                        >
                            X
                        </button>
                        <div className="flex items-center justify-start w-full">
                            <h1 className="text-4xl">Nova Atividade</h1>
                        </div>
                        <TitleInput
                            titulo="Nome da Atividade"
                            setValor={setNomeAtividade}
                            valor={nomeAtividade}
                        />
                        <button
                            type="submit"
                            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded cursor-pointer"
                        >
                            Adicionar Atividade
                        </button>
                    </form>
                </section>
            )}
            {loading && <Loading />}
        </main>
    );
}
