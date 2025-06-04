'use client';
import React, { useState } from 'react';
import Loading from '../components/loading';
import Link from 'next/link';
import TitleInput from '../components/title_input';

export default function ForgotPassword() {
    const [nome, setNome] = useState<string>('');
    const [password, setPassword] = useState<string>('');
    const [repeatPassword, setRepeatPassword] = useState<string>('');
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<string>('');

    // RESETAR PASSWORD
    const handleResetPassword = async (e: any) => {
        try {
            e.preventDefault();
            setLoading(true);
            if (nome == '' || password == '' || repeatPassword == '') {
                setError('Preencha todos os campos!');
                return;
            }
            if (password != repeatPassword) {
                setError('As passwords não coincidem');
                return;
            }
            const response = await fetch(
                'http://127.0.0.1:5000/alterar-password',
                {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        nome: nome,
                        password: password,
                    }),
                }
            );
            if (response.ok) {
                alert('Password alterada com sucesso');
                setError('');
                window.location.href = '/login';
            } else {
                const errorData = await response.json();
                setError(errorData['Erro'] || 'Erro desconhecido');
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
        <main className="grid grid-rows-[auto_1fr] h-[100dvh]">
            <header className="flex justify-start items-center py-4 px-20 border-b border-gray-300">
                <Link
                    href={{ pathname: '/login' }}
                    className="text-2xl cursor-pointer"
                >
                    &#60; Voltar
                </Link>
            </header>
            <section className="flex items-center justify-center">
                <form
                    className="border rounded-2xl shadow-2xl flex items-center justify-center gap-6 flex-col p-10 w-1/3"
                    onSubmit={handleResetPassword}
                >
                    <h1 className="text-3xl">Trocar Password</h1>
                    <TitleInput
                        titulo="Nome"
                        valor={nome}
                        setValor={setNome}
                        error={error.toLocaleLowerCase().includes('nome')}
                    />

                    <TitleInput
                        titulo="Nova Password"
                        valor={password}
                        setValor={setPassword}
                        error={error.toLocaleLowerCase().includes('passwords')}
                        inputType="password"
                    />
                    <TitleInput
                        titulo="Repete a Password"
                        valor={repeatPassword}
                        setValor={setRepeatPassword}
                        error={error.toLocaleLowerCase().includes('passwords')}
                        inputType="password"
                    />
                    <button
                        className="border rounded-2xl text-white bg-blue-500 p-4 w-full cursor-pointer"
                        type="submit"
                    >
                        Trocar Password
                    </button>
                    {error && !error.includes('undefined') && (
                        <p className="text-red-500">{error}</p>
                    )}
                </form>
                {loading && <Loading />}
            </section>
        </main>
    );
}
