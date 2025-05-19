'use client';
import Link from 'next/link';
import React, { useState } from 'react';
import Loading from '../components/loading';
import { useRouter } from 'next/navigation';

export default function LoginPage() {
    const [nome, setNome] = useState<string>('');
    const [password, setPassword] = useState<string>('');
    const [loading, setLoading] = useState<boolean>(false);
    const router = useRouter();

    // HANDLE LOGIN
    const login = async (e: any) => {
        try {
            e.preventDefault();
            setLoading(true);
            if (nome == '' || password == '') {
                alert('Preencha todos os campos');
                return;
            }
            const response = await fetch('http://127.0.0.1:5000/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    nome: nome,
                    password: password,
                }),
            });

            // SALVAR TOKEN E LIMITE
            if (response.ok) {
                const data = await response.json();
                const limite = Date.now() + 60 * 60 * 1000; // 1 hora de limite
                localStorage.setItem('token', data.token);
                localStorage.setItem('token_limite', limite.toString());
                router.replace('/');
            } else {
                const errorData = await response.json();
                alert(errorData['Erro'] || 'Erro desconhecido');
            }
        } catch (error) {
            alert('Erro ao fazer login');
        } finally {
            setLoading(false);
        }
    };
    return (
        <main className="flex items-center justify-center h-[100dvh]">
            <form
                className="border rounded-2xl shadow-2xl flex items-center justify-center gap-6 flex-col p-10"
                onSubmit={login}
            >
                <h1 className="text-3xl">Entrar</h1>
                <input
                    className="border-b border-gray-300 w-full outline-none"
                    type="text"
                    placeholder="Nome"
                    onChange={(e) => setNome(e.target.value)}
                />
                <input
                    className="border-b border-gray-300 w-full  outline-none"
                    type="password"
                    placeholder="Password"
                    onChange={(e) => setPassword(e.target.value)}
                />
                <div className="flex items-cente justify-start w-full">
                    <Link
                        href={{ pathname: '/forgot_password' }}
                        className="text-xs text-black opacity-40 underline cursor-pointer"
                    >
                        Esqueci Password
                    </Link>
                </div>

                <button
                    className="border rounded-2xl text-white bg-blue-500 p-4 w-full cursor-pointer"
                    type="submit"
                >
                    Entrar
                </button>
                <h3>
                    Não tem conta?{' '}
                    <Link
                        href={{ pathname: '/register' }}
                        className="underline text-blue-700"
                    >
                        Crie uma!
                    </Link>
                </h3>
            </form>
            {loading && <Loading />}
        </main>
    );
}
