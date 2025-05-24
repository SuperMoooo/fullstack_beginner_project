'use client';
import Link from 'next/link';
import React, { useEffect, useState } from 'react';
import { Tipo } from '../util/types';

export default function Navbar() {
    const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
    const [tipo, setTipo] = useState<Tipo>('user');

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
            setIsAuthenticated(false);
        }
    }, []);

    return (
        <nav className="flex justify-end items-center py-4 px-20 border-b border-gray-200 gap-2">
            {isAuthenticated ? (
                <>
                    <Link
                        href={{ pathname: '/account' }}
                        className="border rounded-full text-black border-black py-2 px-6 hover:bg-black hover:text-white transition duration-300"
                    >
                        Conta
                    </Link>
                </>
            ) : (
                <Link
                    href={{ pathname: '/login' }}
                    className="border rounded-full text-white bg-black py-2 px-6 hover:scale-105 transition duration-300"
                >
                    Autenticar
                </Link>
            )}
        </nav>
    );
}
