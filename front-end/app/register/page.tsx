'use client';
import Link from 'next/link';
import React, { useState } from 'react';

export default function RegisterPage() {
    const [nome, setNome] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    // HANDLE REGISTER
    const register = async (e: any) => {
        e.preventDefault();
        if (nome == '' || password == '') {
            alert('Preencha todos os campos');
            return;
        }
        const response = await fetch('http://127.0.0.1:5000/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                nome: nome,
                email: email,
                password: password,
            }),
        });

        // SALVAR TOKEN E LIMITE
        if (response.ok) {
            alert('Sucesso');
        } else {
            alert('Verifique as suas credenciais');
        }
    };
    return (
        <main className="flex items-center justify-center h-[100dvh]">
            <form
                className="border rounded-2xl shadow-2xl flex items-center justify-center gap-6 flex-col p-10"
                onSubmit={register}
            >
                <h1 className="text-3xl">Criar conta</h1>
                <input
                    className="border-b border-gray-300 w-full outline-none"
                    type="text"
                    placeholder="Nome"
                    onChange={(e) => setNome(e.target.value)}
                />
                <input
                    className="border-b border-gray-300 w-full outline-none"
                    type="text"
                    placeholder="Email"
                    onChange={(e) => setEmail(e.target.value)}
                />
                <input
                    className="border-b border-gray-300 w-full  outline-none"
                    type="text"
                    placeholder="Password"
                    onChange={(e) => setPassword(e.target.value)}
                />
                <button
                    className="border rounded-2xl text-white bg-blue-500 p-4 w-full cursor-pointer"
                    type="submit"
                >
                    Entrar
                </button>
                <h3>
                    Já tem conta?{' '}
                    <Link
                        href={{ pathname: '/login' }}
                        className="underline text-blue-700"
                    >
                        Entrar!
                    </Link>
                </h3>
            </form>
        </main>
    );
}
