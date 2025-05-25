'use client';
import Link from 'next/link';
import React, { useState } from 'react';
import Loading from '../components/loading';
import { useRouter } from 'next/navigation';
import TitleInput from '../components/title_input';

export default function LoginPage() {
    const [nome, setNome] = useState<string>('');
    const [password, setPassword] = useState<string>('');
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<string>('');
    const router = useRouter();

    // HANDLE LOGIN
    const login = async (e: any) => {
        try {
            e.preventDefault();
            setLoading(true);
            if (nome == '' || password == '') {
                alert('Preencha todos os campos!');
                setError('Preencha todos os campos!');
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
                alert('Login realizado com sucesso!');
                const data = await response.json();
                const limite = Date.now() + 60 * 60 * 1000; // 1 hora de limite
                localStorage.setItem('token', data.token);
                localStorage.setItem('token_limite', limite.toString());
                localStorage.setItem('tipo', data.tipo);
                localStorage.setItem('user_nome', nome);
                setError('');
                router.replace('/');
            } else {
                const errorData = await response.json();
                alert(errorData['Erro'] || 'Erro desconhecido');
                setError(errorData['Erro'] || 'Erro desconhecido');
            }
        } catch (error: any) {
            if (error.message.includes('NetworkError')) {
                setError('Servidor Offline');
            } else if (error.message.includes('cursor')) {
                setError('Utilizador não encontrado');
            } else {
                setError(error.message);
            }
        } finally {
            setLoading(false);
        }
    };
    return (
        <main className="grid grid-rows-[auto_1fr] h-[100dvh]">
            <header className="flex justify-start items-center py-4 px-20 border-b border-gray-300">
                <Link
                    href={{ pathname: '/' }}
                    className="text-2xl cursor-pointer"
                >
                    &#60; Voltar
                </Link>
            </header>
            <section className="flex items-center justify-center ">
                <form
                    className="border rounded-2xl shadow-2xl flex items-center justify-center gap-6 flex-col p-10 w-1/3"
                    onSubmit={login}
                >
                    <h1 className="text-3xl">Entrar</h1>
                    <TitleInput titulo="Nome" valor={nome} setValor={setNome} />
                    <TitleInput
                        titulo="Password"
                        valor={password}
                        setValor={setPassword}
                        inputType="password"
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
                    {error && !error.includes('undefined') && (
                        <p className="text-red-500">{error}</p>
                    )}
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
            </section>
        </main>
    );
}
