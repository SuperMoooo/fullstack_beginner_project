import React from 'react';
import { Evento } from '../util/types';
import Link from 'next/link';

export default function EventCard({ evento }: { evento: Evento }) {
    return (
        <article className="flex flex-col items-start justify-center gap-1 p-4 border rounded-2xl shadow-2xl border-gray-200">
            <h1 className="text-2xl">{evento['nome_evento']}</h1>
            <div className="w-full h-[2px] bg-gray-200"></div>
            <h2 className="text-md opacity-70">{evento.data_evento}</h2>
            <Link
                className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-5"
                href={`/eventos/${evento.id}`}
            >
                Ver Detalhes
            </Link>
        </article>
    );
}
