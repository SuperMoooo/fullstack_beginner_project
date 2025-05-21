'use client';
import { useEffect, useState } from 'react';
import Navbar from './components/Navbar';
import Loading from './components/loading';
import Link from 'next/link';
import { Tipo } from './util/types';

export default function Home() {
    const [loading, setLoading] = useState(false);
    const [eventos, setEventos] = useState([]);
    const [tipo, setTipo] = useState<Tipo>('user');

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
            if (token && limite && Date.now() < parseInt(limite, 10)) {
                const response = await fetch(`http://127.0.0.1:5000/eventos`, {
                    method: 'GET',
                    headers: {
                        Authorization: `Bearer ${token}`,
                        'Content-Type': 'application/json',
                    },
                });
                if (response.ok) {
                    const data = await response.json();
                    setEventos(data);
                } else {
                }
            } else {
                alert('Sessão expirada');
            }
        } catch (error) {
            alert('Erro ao carregar evento');
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
                            href={{ pathname: '/evento/adicionar_evento' }}
                            className="bg-green-700 hover:bg-green-800 text-white font-bold py-2 px-4 rounded"
                        >
                            Importar evento .csv
                        </Link>
                        <Link
                            href={{ pathname: '/evento/adicionar_evento' }}
                            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
                        >
                            Adicionar Evento
                        </Link>
                    </aside>
                )}

                <section className="flex items-center justify-center w-full">
                    {loading ? (
                        <Loading />
                    ) : eventos.length > 0 ? (
                        eventos.map((evento, index) => (
                            <article
                                key={evento['nome_evento'] + index}
                                className="flex flex-col items-start justify-center gap-4 p-4 border rounded-2xl shadow-2xl border-gray-200"
                            >
                                <h1 className="text-xl">
                                    {evento['nome_evento']}
                                </h1>
                                <div className="w-full h-[2px] bg-gray-200"></div>
                                <h2 className="text-lg opacity-70">
                                    {evento['data_evento']}
                                </h2>
                                <Link
                                    className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
                                    href={{
                                        pathname: '/evento/',
                                        query: { id: evento['id'] },
                                    }}
                                >
                                    Ver Detalhes
                                </Link>
                            </article>
                        ))
                    ) : (
                        <h1 className="text-2xl">Nenhum evento encontrado</h1>
                    )}
                </section>
            </section>
        </main>
    );
}
