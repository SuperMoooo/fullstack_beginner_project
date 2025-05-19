'use client';
import React, { useState } from 'react';
import Loading from '../components/loading';

export default function ForgotPassword() {
    const [nome, setNome] = useState('');
    const [password, setPassword] = useState('');
    const [repeatPassword, setRepeatPassword] = useState('');
    const [loading, setLoading] = useState(false);

    const handleResetPassword = async (e: any) => {
        try {
            e.preventDefault();
            setLoading(true);
            if (nome == '' || password == '' || repeatPassword == '') {
                alert('Preencha todos os campos');
                return;
            }
            if (password != repeatPassword) {
                alert('As senhas não coincidem');
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
                window.location.href = '/login';
            } else {
                const errorData = await response.json();
                alert(errorData['Erro'] || 'Erro desconhecido');
            }
        } catch (error) {
            alert('Erro ao resetar password');
        } finally {
            setLoading(false);
        }
    };
    return (
        <main className="flex items-center justify-center h-[100dvh]">
            <form
                className="border rounded-2xl shadow-2xl flex items-center justify-center gap-6 flex-col p-10"
                onSubmit={handleResetPassword}
            >
                <h1 className="text-3xl">Trocar Password</h1>
                <input
                    className="border-b border-gray-300 w-full outline-none"
                    type="text"
                    placeholder="Nome"
                    onChange={(e) => setNome(e.target.value)}
                />
                <input
                    className="border-b border-gray-300 w-full  outline-none"
                    type="text"
                    placeholder="Nova Password"
                    onChange={(e) => setPassword(e.target.value)}
                />
                <input
                    className="border-b border-gray-300 w-full  outline-none"
                    type="text"
                    placeholder="Repete a Password"
                    onChange={(e) => setRepeatPassword(e.target.value)}
                />
                <button
                    className="border rounded-2xl text-white bg-blue-500 p-4 w-full cursor-pointer"
                    type="submit"
                >
                    Trocar Password
                </button>
            </form>
            {loading && <Loading />}
        </main>
    );
}
