'use client';
import { useEffect, useState } from 'react';
import Navbar from '../components/Navbar';
import Loading from '../components/loading';
import Link from 'next/link';
import { Evento, Tipo } from '../util/types';
import EventCard from './event_card';
import TitleInputFile from '../components/title_input_file';

export default function Eventos() {
    const [loading, setLoading] = useState<boolean>(false);
    const [eventos, setEventos] = useState<Evento[]>([]);
    const [tipo, setTipo] = useState<Tipo>('Entreveniente');
    const [error, setError] = useState<string>('');

    // CSV FILE
    const [showImportEvent, setShowImportEvent] = useState<boolean>(false);
    const [csvFile, setCsvFile] = useState<File | null>(null);
    const [importError, setImportError] = useState<string>('');

    useEffect(() => {
        const tipo = localStorage.getItem('tipo');
        setTipo((tipo as Tipo) ?? 'Entreveniente');
        getEventos();
    }, []);

    const getEventos = async () => {
        try {
            setLoading(true);
            const token = localStorage.getItem('token');
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
                setError('');
            } else {
                const errorData = await response.json();
                setError(errorData['Erro'] ?? 'Erro desconhecido');
            }
        } catch (error: any) {
            if (error.message.includes('NetworkError')) {
                setError('Servidor Offline');
                setTipo('Entreveniente');
            } else {
                setError(error.message);
            }
        } finally {
            setLoading(false);
        }
    };

    const handleImportEvent = async (e: any) => {
        try {
            setLoading(true);
            e.preventDefault();
            const token = localStorage.getItem('token');
            if (!csvFile) {
                setImportError('Nenhum arquivo selecionado');
                return;
            }
            if (csvFile.type !== 'text/csv') {
                setImportError('Arquivo inválido');
                return;
            }
            const formData = new FormData();
            formData.append('csvFile', csvFile);

            const response = await fetch(
                `http://127.0.0.1:5000/importar-evento`,
                {
                    method: 'POST',
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                    body: formData,
                }
            );
            if (response.ok) {
                getEventos();
                setImportError('');
                setShowImportEvent((prev: boolean) => !prev);
                setCsvFile(null);
            } else {
                const errorData = await response.json();
                setImportError(errorData['Erro'] ?? 'Erro desconhecido');
            }
        } catch (error: any) {
            if (error.message.includes('NetworkError')) {
                setImportError('Servidor Offline');
            } else {
                setImportError(error.message);
            }
        } finally {
            setLoading(false);
        }
    };
    return (
        <main className="grid grid-rows-[auto_1fr] min-h-[100dvh]">
            <Navbar />
            <section className="flex items-center justify-start gap-6 flex-col w-full p-20">
                {tipo == 'Admin' && (
                    <aside className="flex items-center justify-end w-full gap-4">
                        <button
                            onClick={() =>
                                setShowImportEvent((prev: boolean) => !prev)
                            }
                            className="bg-green-700 hover:bg-green-800 text-white font-bold py-2 px-4 rounded cursor-pointer"
                        >
                            Importar evento
                        </button>
                        <Link
                            href={{ pathname: '/eventos/adicionar_evento' }}
                            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded cursor-pointer"
                        >
                            Adicionar Evento
                        </Link>
                    </aside>
                )}
                {eventos.length > 0 && (
                    <h1 className="text-2xl font-bold self-start">Eventos</h1>
                )}
                <section
                    className={`flex items-center gap-8 flex-wrap ${
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
            {showImportEvent && (
                <section className="top-0 left-0 fixed w-screen h-screen flex items-center justify-center">
                    <div className="bg-black opacity-60 top-0 left-0 fixed h-screen w-screen -z-10"></div>

                    <form
                        onSubmit={handleImportEvent}
                        className="flex items-end justify-center gap-6 flex-col w-1/3 p-10 bg-white rounded-2xl"
                    >
                        <button
                            className="text-5xl cursor-pointer"
                            type="button"
                            onClick={() => {
                                setShowImportEvent((prev: boolean) => !prev);
                                setCsvFile(null);
                                setImportError('');
                            }}
                        >
                            X
                        </button>
                        <h1 className="text-2xl font-bold self-start">
                            Importar Evento
                        </h1>
                        <TitleInputFile
                            setValor={setCsvFile}
                            valor={csvFile}
                            accept={'.csv'}
                        />
                        <button
                            type="submit"
                            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded cursor-pointer"
                        >
                            Importar
                        </button>
                        {importError && (
                            <h1 className="text-red-600">{importError}</h1>
                        )}
                    </form>
                </section>
            )}
        </main>
    );
}
