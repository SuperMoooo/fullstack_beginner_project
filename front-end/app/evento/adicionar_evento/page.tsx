'use client';
import Loading from '@/app/components/loading';
import Navbar from '@/app/components/Navbar';
import Sidebar from '@/app/components/Sidebar';
import TitleInput from '@/app/components/title_input';
import React, { useEffect, useState } from 'react';

export default function AdicionarEvento() {
    const [loading, setLoading] = useState(false);
    const [nomeEvento, setNomeEvento] = useState('');
    const [dataEvento, setDataEvento] = useState('');

    const handleCreateEvento = async (e: any) => {
        try {
            e.preventDefault();
            setLoading(true);
        } catch (error) {
            alert('Erro ao criar evento');
        } finally {
            setLoading(false);
        }
    };
    return (
        <main className="grid grid-cols-[auto_1fr] min-h-[100dvh]">
            <Sidebar selected={0} />
            <div className="grid grid-rows-[auto_1fr]">
                <Navbar />
                <form
                    className="flex items-center justify-between gap-6 flex-col w-full p-20"
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
                    <button
                        type="submit"
                        className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded cursor-pointer"
                    >
                        Criar Evento
                    </button>
                </form>
            </div>
            {loading && <Loading />}
        </main>
    );
}
