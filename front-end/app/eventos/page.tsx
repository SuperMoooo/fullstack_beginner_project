'use client';
import { useEffect, useState } from 'react';
import Navbar from '../components/Navbar';
import Loading from '../components/loading';
import Link from 'next/link';
import { Evento, Tipo } from '../util/types';
import EventCard from './event_card';

export default function Eventos() {
    const [loading, setLoading] = useState<boolean>(false);
    const [eventos, setEventos] = useState<Evento[]>([]);
    const [tipo, setTipo] = useState<Tipo>('user');
    const [error, setError] = useState<string>('');

    useEffect(() => {
        getEvento();
        const tipo = localStorage.getItem('tipo');
        setTipo((tipo as Tipo) ?? 'user');
    }, []);

    const getEvento = async () => {
        try {
            setLoading(true);
            const token = localStorage.getItem('token');
            const limite = localStorage.getItem('token_limite');
            const response = await fetch(`http://127.0.0.1:5000/eventos`, {
                method: 'GET',
                headers: {
                    Authorization: `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
            });
            if (response.ok) {
                const data = await response.json();
                setEventos(data['Data']);
                setError('');
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
            <Navbar />
            <section className="flex items-center justify-start gap-6 flex-col w-full p-20">
                {tipo == 'admin' && (
                    <aside className="flex items-center justify-end w-full gap-4">
                        <Link
                            href={{ pathname: '/eventos/adicionar_evento' }}
                            className="bg-green-700 hover:bg-green-800 text-white font-bold py-2 px-4 rounded"
                        >
                            Importar evento
                        </Link>
                        <Link
                            href={{ pathname: '/eventos/adicionar_evento' }}
                            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
                        >
                            Adicionar Evento
                        </Link>
                    </aside>
                )}
                {eventos.length > 0 && (
                    <h1 className="text-2xl font-bold self-start">Eventos</h1>
                )}
                <section
                    className={`flex items-center ${
                        eventos.length > 0 ? 'justify-start' : 'justify-center'
                    }  w-full`}
                >
                    {loading ? (
                        <Loading />
                    ) : error ? (
                        <h1 className="text-2xl text-red-600">{error}</h1>
                    ) : eventos.length > 0 ? (
                        eventos.map((evento, index) => (
                            <EventCard
                                key={evento.nome_evento + index}
                                evento={evento}
                            />
                        ))
                    ) : (
                        <h1 className="text-2xl">Nenhum evento encontrado</h1>
                    )}
                </section>
            </section>
        </main>
    );
}
