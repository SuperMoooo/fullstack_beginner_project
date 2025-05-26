'use client';
import Loading from '@/app/components/loading';
import Navbar from '@/app/components/Navbar';
import { Evento } from '@/app/util/types';
import { useParams } from 'next/navigation';
import React, { useEffect, useState } from 'react';

export default function EventoDetalhes() {
    const params = useParams();
    const id = params.id;

    const [evento, setEvento] = useState<Evento>();
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<string>('');

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
                    setEvento(data);
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
    return (
        <main className="grid grid-rows-[auto_1fr] min-h-[100dvh]">
            <Navbar goBack={true} />
            <section className="flex items-center justify-center">
                {loading ? (
                    <Loading />
                ) : (
                    <article className="flex flex-col gap-4 p-4 items-start justify-center w-full">
                        <h1 className="text-4xl font-bold">
                            {evento?.nome_evento}
                        </h1>
                        <div className="w-2/3 h-[2px] bg-gray-200"></div>
                        <h2 className="text-xl opacity-70">
                            {evento?.data_evento}
                        </h2>
                    </article>
                )}
            </section>
        </main>
    );
}
