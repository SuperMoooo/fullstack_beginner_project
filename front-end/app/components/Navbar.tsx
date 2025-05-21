'use client';
import Link from 'next/link';
import React, { useEffect, useState } from 'react';

export default function Navbar() {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [tipo, setTipo] = useState('');

    useEffect(() => {
        const token = localStorage.getItem('token');
        const limite = localStorage.getItem('token_limite');
        const tipo = localStorage.getItem('tipo');

        console.log(token, limite);
        if (token && limite && Date.now() < parseInt(limite, 10)) {
            setIsAuthenticated(true);
            setTipo(tipo!);
        } else {
            // Token is expired or doesn't exist
            localStorage.removeItem('token');
            localStorage.removeItem('token_limite');
            setIsAuthenticated(false);
        }
    }, []);

    return (
        <nav className="flex justify-center items-center p-4 border-b border-gray-200 gap-2">
            {isAuthenticated ? (
                <>
                    <h1 className="border rounded-2xl text-white bg-green-700 p-4 font-bold">
                        Já está autenticado {tipo ? `como ${tipo}` : ''}
                    </h1>
                    <Link
                        href={{ pathname: '/login' }}
                        className="border rounded-2xl text-white bg-blue-500 p-4"
                    >
                        Mudar de conta
                    </Link>
                </>
            ) : (
                <Link
                    href={{ pathname: '/login' }}
                    className="border rounded-2xl text-white bg-blue-500 p-4"
                >
                    Autenticar
                </Link>
            )}
        </nav>
    );
}
