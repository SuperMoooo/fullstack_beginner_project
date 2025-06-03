'use client';
import Link from 'next/link';
import React, { useEffect, useState } from 'react';
import { Tipo } from '../util/types';

export default function Navbar({
    goBack,
    isConta,
}: {
    goBack?: boolean;
    isConta?: boolean;
}) {
    const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
    const [tipo, setTipo] = useState<Tipo>('Participante');

    useEffect(() => {
        const token = localStorage.getItem('token');
        const limite = localStorage.getItem('token_limite');
        const tipo = localStorage.getItem('tipo');

        if (token && limite && Date.now() < parseInt(limite, 10)) {
            setIsAuthenticated(true);
            if (tipo) {
                setTipo(tipo as Tipo);
            }
        } else {
            // Token is expired or doesn't exist
            localStorage.removeItem('token');
            localStorage.removeItem('token_limite');
            localStorage.removeItem('tipo');
            localStorage.removeItem('user_nome');
            setIsAuthenticated(false);
        }
    }, []);

    return (
        <nav
            className={`flex  items-center py-4 px-20 border-b border-gray-200 gap-2 ${
                goBack ? 'justify-between' : 'justify-end'
            }`}
        >
            {goBack && (
                <button
                    onClick={() => {
                        window.history.back();
                    }}
                    className="text-2xl cursor-pointer"
                >
                    &#60; Voltar
                </button>
            )}
            {!isConta ? (
                isAuthenticated ? (
                    <Link
                        href={{ pathname: '/account' }}
                        className="border rounded-full text-black border-black py-2 px-6 hover:bg-black hover:text-white transition duration-300"
                    >
                        Conta
                    </Link>
                ) : (
                    <Link
                        href={{ pathname: '/login' }}
                        className="border rounded-full text-white bg-black py-2 px-6 hover:scale-105 transition duration-300"
                    >
                        Autenticar
                    </Link>
                )
            ) : (
                <Link
                    href={{ pathname: '/login' }}
                    className="border rounded-full text-black border-black py-2 px-6 hover:bg-black hover:text-white transition duration-300"
                >
                    Mudar de Conta
                </Link>
            )}
        </nav>
    );
}
